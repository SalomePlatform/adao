#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2011  EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import logging
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

import numpy
import scipy.optimize

if logging.getLogger().level < 30:
    iprint  = 1
    message = scipy.optimize.tnc.MSG_ALL
    disp    = 1
else:
    iprint  = -1
    message = scipy.optimize.tnc.MSG_NONE
    disp    = 0

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self)
        self._name = "3DVAR"
        logging.debug("%s Initialisation"%self._name)

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul de l'estimateur 3D-VAR
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Opérateur d'observation
        # -----------------------
        Hm = H["Direct"].appliedTo
        Ht = H["Adjoint"].appliedInXTo
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if H["AppliedToX"] is not None and H["AppliedToX"].has_key("HXb"):
            logging.debug("%s Utilisation de HXb"%self._name)
            HXb = H["AppliedToX"]["HXb"]
        else:
            logging.debug("%s Calcul de Hm(Xb)"%self._name)
            HXb = Hm( Xb )
        HXb = numpy.asmatrix(HXb).flatten().T
        #
        # Calcul du préconditionnement
        # ----------------------------
	# Bdemi = numpy.linalg.cholesky(B)
        #
        # Calcul de l'innovation
        # ----------------------
        d  = Y - HXb
        logging.debug("%s Innovation d = %s"%(self._name, d))
        #
        # Précalcul des inversion appellée dans les fonction-coût et gradient
        # -------------------------------------------------------------------
        BI = B.I
        RI = R.I
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x):
            _X  = numpy.asmatrix(x).flatten().T
            logging.info("%s CostFunction X  = %s"%(self._name, numpy.asmatrix( _X ).flatten()))
            _HX = Hm( _X )
            _HX = numpy.asmatrix(_HX).flatten().T
            Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
            Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            J   = float( Jb ) + float( Jo )
            logging.info("%s CostFunction Jb = %s"%(self._name, Jb))
            logging.info("%s CostFunction Jo = %s"%(self._name, Jo))
            logging.info("%s CostFunction J  = %s"%(self._name, J))
            self.StoredVariables["CurrentState"].store( _X.A1 )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            return float( J )
        #
        def GradientOfCostFunction(x):
            _X      = numpy.asmatrix(x).flatten().T
            logging.info("%s GradientOfCostFunction X      = %s"%(self._name, numpy.asmatrix( _X ).flatten()))
            _HX     = Hm( _X )
            _HX     = numpy.asmatrix(_HX).flatten().T
            GradJb  = BI * (_X - Xb)
            GradJo  = - Ht( (_X, RI * (Y - _HX)) )
            GradJ   = numpy.asmatrix( GradJb ).flatten().T + numpy.asmatrix( GradJo ).flatten().T
            logging.debug("%s GradientOfCostFunction GradJb = %s"%(self._name, numpy.asmatrix( GradJb ).flatten()))
            logging.debug("%s GradientOfCostFunction GradJo = %s"%(self._name, numpy.asmatrix( GradJo ).flatten()))
            logging.debug("%s GradientOfCostFunction GradJ  = %s"%(self._name, numpy.asmatrix( GradJ  ).flatten()))
            return GradJ.A1
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if type(Xb) is type(numpy.matrix([])):
            Xini = Xb.A1.tolist()
        else:
            Xini = list(Xb)
        logging.debug("%s Point de démarrage Xini = %s"%(self._name, Xini))
        #
        # Paramètres de pilotage
        # ----------------------
        # Potentiels : "Bounds", "Minimizer", "MaximumNumberOfSteps", "ProjectedGradientTolerance", "GradientNormTolerance", "InnerMinimizer"
        if Parameters.has_key("Bounds") and (type(Parameters["Bounds"]) is type([]) or type(Parameters["Bounds"]) is type(())) and (len(Parameters["Bounds"]) > 0):
            Bounds = Parameters["Bounds"]
        else:
            Bounds = None
        MinimizerList = ["LBFGSB","TNC", "CG", "NCG", "BFGS"]
        if Parameters.has_key("Minimizer") and (Parameters["Minimizer"] in MinimizerList):
            Minimizer = str( Parameters["Minimizer"] )
        else:
            logging.warning("%s Minimiseur inconnu ou non fourni, remplacé par la valeur par défaut"%self._name)
            Minimizer = "LBFGSB"
        logging.debug("%s Minimiseur utilisé = %s"%(self._name, Minimizer))
        if Parameters.has_key("MaximumNumberOfSteps") and (Parameters["MaximumNumberOfSteps"] > -1):
            maxiter = int( Parameters["MaximumNumberOfSteps"] )
        else:
            maxiter = 15000
        logging.debug("%s Nombre maximal de pas d'optimisation = %s"%(self._name, str(maxiter)))
        if Parameters.has_key("CostDecrementTolerance") and (Parameters["CostDecrementTolerance"] > 0):
            ftol  = float(Parameters["CostDecrementTolerance"])
            factr = 1./ftol
        else:
            ftol  = 1.e-7
            factr = 1./ftol
        logging.debug("%s Diminution relative minimale du cout lors de l'arret = %s"%(self._name, str(1./factr)))
        if Parameters.has_key("ProjectedGradientTolerance") and (Parameters["ProjectedGradientTolerance"] > -1):
            pgtol = float(Parameters["ProjectedGradientTolerance"])
        else:
            pgtol = -1
        logging.debug("%s Maximum des composantes du gradient projete lors de l'arret = %s"%(self._name, str(pgtol)))
        if Parameters.has_key("GradientNormTolerance") and (Parameters["GradientNormTolerance"] > -1):
            gtol = float(Parameters["GradientNormTolerance"])
        else:
            gtol = 1.e-05
        logging.debug("%s Maximum des composantes du gradient lors de l'arret = %s"%(self._name, str(gtol)))
        InnerMinimizerList = ["CG", "NCG", "BFGS"]
        if Parameters.has_key("InnerMinimizer") and (Parameters["InnerMinimizer"] in InnerMinimizerList):
            InnerMinimizer = str( Parameters["Minimizer"] )
        else:
            InnerMinimizer = "BFGS"
        logging.debug("%s Minimiseur interne utilisé = %s"%(self._name, InnerMinimizer))
        logging.debug("%s Norme du gradient lors de l'arret = %s"%(self._name, str(gtol)))
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        if Minimizer == "LBFGSB":
            Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = Bounds,
                maxfun      = maxiter,
                factr       = factr,
                pgtol       = pgtol,
                iprint      = iprint,
                )
            nfeval = Informations['funcalls']
            rc     = Informations['warnflag']
        elif Minimizer == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = Bounds,
                maxfun      = maxiter,
                pgtol       = pgtol,
                ftol        = ftol,
                messages    = message,
                )
        elif Minimizer == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = maxiter,
                gtol        = gtol,
                disp        = disp,
                full_output = True,
                )
        elif Minimizer == "NCG":
            Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = maxiter,
                avextol     = ftol,
                disp        = disp,
                full_output = True,
                )
        elif Minimizer == "BFGS":
            Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = maxiter,
                gtol        = gtol,
                disp        = disp,
                full_output = True,
                )
        else:
            raise ValueError("Error in Minimizer name: %s"%Minimizer)
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        # ----------------------------------------------------------------
        StepMin = numpy.argmin( self.StoredVariables["CostFunctionJ"].valueserie() )
        MinJ    = self.StoredVariables["CostFunctionJ"].valueserie(step = StepMin)
        Minimum = self.StoredVariables["CurrentState"].valueserie(step = StepMin)
        #
        logging.debug("%s %s Step of min cost  = %s"%(self._name, Minimizer, StepMin))
        logging.debug("%s %s Minimum cost      = %s"%(self._name, Minimizer, MinJ))
        logging.debug("%s %s Minimum state     = %s"%(self._name, Minimizer, Minimum))
        logging.debug("%s %s Nb of F           = %s"%(self._name, Minimizer, nfeval))
        logging.debug("%s %s RetCode           = %s"%(self._name, Minimizer, rc))
        #
        # Calcul  de l'analyse
        # --------------------
        Xa = numpy.asmatrix(Minimum).T
        logging.debug("%s Analyse Xa = %s"%(self._name, Xa))
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        self.StoredVariables["Innovation"].store( d.A1 )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("MB")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
