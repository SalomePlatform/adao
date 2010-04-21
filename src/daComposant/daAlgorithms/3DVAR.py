#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2009  EDF R&D
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
__doc__ = """
    Algorithme variationnel statique (3D-VAR)
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2009"

import sys ; sys.path.insert(0, "../daCore")
import logging
import Persistence
from BasicObjects import Algorithm
import PlatformInfo ; m = PlatformInfo.SystemUsage()

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
class ElementaryAlgorithm(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self._name = "3DVAR"
        logging.debug("%s Initialisation"%self._name)

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Par=None):
        """
        Calcul de l'estimateur 3D-VAR
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
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
            # self.StoredVariables["GradientOfCostFunctionJb"].store( Jb )
            # self.StoredVariables["GradientOfCostFunctionJo"].store( Jo )
            # self.StoredVariables["GradientOfCostFunctionJ" ].store( J )
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
        if Par.has_key("Bounds") and (type(Par["Bounds"]) is type([]) or type(Par["Bounds"]) is type(())) and (len(Par["Bounds"]) > 0):
            Bounds = Par["Bounds"]
        else:
            Bounds = None
        MinimizerList = ["LBFGSB","TNC", "CG", "BFGS"]
        if Par.has_key("Minimizer") and (Par["Minimizer"] in MinimizerList):
            Minimizer = str( Par["Minimizer"] )
        else:
            Minimizer = "LBFGSB"
        logging.debug("%s Minimiseur utilisé = %s"%(self._name, Minimizer))
        if Par.has_key("MaximumNumberOfSteps") and (Par["MaximumNumberOfSteps"] > -1):
            maxiter = int( Par["MaximumNumberOfSteps"] )
        else:
            maxiter = 15000
        logging.debug("%s Nombre maximal de pas d'optimisation = %s"%(self._name, maxiter))
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
                iprint      = iprint,
                )
            logging.debug("%s %s Minimum = %s"%(self._name, Minimizer, Minimum))
            logging.debug("%s %s Nb of F = %s"%(self._name, Minimizer, Informations['funcalls']))
            logging.debug("%s %s RetCode = %s"%(self._name, Minimizer, Informations['warnflag']))
        elif Minimizer == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = Bounds,
                maxfun      = maxiter,
                messages    = message,
                )
            logging.debug("%s %s Minimum = %s"%(self._name, Minimizer, Minimum))
            logging.debug("%s %s Nb of F = %s"%(self._name, Minimizer, nfeval))
            logging.debug("%s %s RetCode = %s"%(self._name, Minimizer, rc))
        elif Minimizer == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = maxiter,
                disp        = disp,
                full_output = True,
                )
            logging.debug("%s %s Minimum = %s"%(self._name, Minimizer, Minimum))
            logging.debug("%s %s Nb of F = %s"%(self._name, Minimizer, nfeval))
            logging.debug("%s %s RetCode = %s"%(self._name, Minimizer, rc))
        elif Minimizer == "BFGS":
            Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = maxiter,
                disp        = disp,
                full_output = True,
                )
            logging.debug("%s %s Minimum = %s"%(self._name, Minimizer, Minimum))
            logging.debug("%s %s Nb of F = %s"%(self._name, Minimizer, nfeval))
            logging.debug("%s %s RetCode = %s"%(self._name, Minimizer, rc))
        else:
            raise ValueError("Error in Minimizer name: %s"%Minimizer)
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
