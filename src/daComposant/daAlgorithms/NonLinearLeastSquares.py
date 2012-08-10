#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2012 EDF R&D
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

if logging.getLogger().level < logging.WARNING:
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
        BasicObjects.Algorithm.__init__(self, "NONLINEARLEASTSQUARES")
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "LBFGSB",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = ["LBFGSB","TNC", "CG", "NCG", "BFGS"],
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfSteps",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "CostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du cout lors de l'arrêt",
            )
        self.defineRequiredParameter(
            name     = "ProjectedGradientTolerance",
            default  = -1,
            typecast = float,
            message  = "Maximum des composantes du gradient projeté lors de l'arrêt",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "GradientNormTolerance",
            default  = 1.e-05,
            typecast = float,
            message  = "Maximum des composantes du gradient lors de l'arrêt",
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
            )

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul de l'estimateur moindres carrés pondérés non linéaires
        (assimilation variationnelle sans ébauche)
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        if self._parameters.has_key("Bounds") and (type(self._parameters["Bounds"]) is type([]) or type(self._parameters["Bounds"]) is type(())) and (len(self._parameters["Bounds"]) > 0):
            Bounds = self._parameters["Bounds"]
            logging.debug("%s Prise en compte des bornes effectuee"%(self._name,))
        else:
            Bounds = None
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        if self._parameters.has_key("Minimizer") is "TNC":
            self.setParameterValue("StoreInternalVariables",True)
        #
        # Opérateur d'observation
        # -----------------------
        Hm = H["Direct"].appliedTo
        Ha = H["Adjoint"].appliedInXTo
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
        # Calcul de l'innovation
        # ----------------------
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        d  = Y - HXb
        logging.debug("%s Innovation d = %s"%(self._name, d))
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        # if B is not None:
        #     BI = B.I
        # elif self._parameters["B_scalar"] is not None:
        #     BI = 1.0 / self._parameters["B_scalar"]
        # else:
        #     raise ValueError("Background error covariance matrix has to be properly defined!")
        #
        if R is not None:
            RI = R.I
        elif self._parameters["R_scalar"] is not None:
            RI = 1.0 / self._parameters["R_scalar"]
        else:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x):
            _X  = numpy.asmatrix(x).flatten().T
            logging.debug("%s CostFunction X  = %s"%(self._name, numpy.asmatrix( _X ).flatten()))
            _HX = Hm( _X )
            _HX = numpy.asmatrix(_HX).flatten().T
            Jb  = 0.
            Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            J   = float( Jb ) + float( Jo )
            logging.debug("%s CostFunction Jb = %s"%(self._name, Jb))
            logging.debug("%s CostFunction Jo = %s"%(self._name, Jo))
            logging.debug("%s CostFunction J  = %s"%(self._name, J))
            if self._parameters["StoreInternalVariables"]:
                self.StoredVariables["CurrentState"].store( _X.A1 )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            return float( J )
        #
        def GradientOfCostFunction(x):
            _X      = numpy.asmatrix(x).flatten().T
            logging.debug("%s GradientOfCostFunction X      = %s"%(self._name, numpy.asmatrix( _X ).flatten()))
            _HX     = Hm( _X )
            _HX     = numpy.asmatrix(_HX).flatten().T
            GradJb  = 0.
            GradJo  = - Ha( (_X, RI * (Y - _HX)) )
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
        # Minimisation de la fonctionnelle
        # --------------------------------
        if self._parameters["Minimizer"] == "LBFGSB":
            Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = Bounds,
                maxfun      = self._parameters["MaximumNumberOfSteps"]-1,
                factr       = self._parameters["CostDecrementTolerance"]*1.e14,
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                iprint      = iprint,
                )
            nfeval = Informations['funcalls']
            rc     = Informations['warnflag']
        elif self._parameters["Minimizer"] == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = Bounds,
                maxfun      = self._parameters["MaximumNumberOfSteps"],
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                messages    = message,
                )
        elif self._parameters["Minimizer"] == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                disp        = disp,
                full_output = True,
                )
        elif self._parameters["Minimizer"] == "NCG":
            Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                avextol     = self._parameters["CostDecrementTolerance"],
                disp        = disp,
                full_output = True,
                )
        elif self._parameters["Minimizer"] == "BFGS":
            Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                disp        = disp,
                full_output = True,
                )
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        StepMin = numpy.argmin( self.StoredVariables["CostFunctionJ"].valueserie() )
        MinJ    = self.StoredVariables["CostFunctionJ"].valueserie(step = StepMin)
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        # ----------------------------------------------------------------
        if self._parameters["StoreInternalVariables"]:
            Minimum = self.StoredVariables["CurrentState"].valueserie(step = StepMin)
        #
        logging.debug("%s %s Step of min cost  = %s"%(self._name, self._parameters["Minimizer"], StepMin))
        logging.debug("%s %s Minimum cost      = %s"%(self._name, self._parameters["Minimizer"], MinJ))
        logging.debug("%s %s Minimum state     = %s"%(self._name, self._parameters["Minimizer"], Minimum))
        logging.debug("%s %s Nb of F           = %s"%(self._name, self._parameters["Minimizer"], nfeval))
        logging.debug("%s %s RetCode           = %s"%(self._name, self._parameters["Minimizer"], rc))
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(Minimum).flatten().T
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
