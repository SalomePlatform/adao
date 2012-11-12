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
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

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
            message  = "Minimiseur utilis�",
            listval  = ["LBFGSB","TNC", "CG", "NCG", "BFGS", "LM"],
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
            message  = "Diminution relative minimale du cout lors de l'arr�t",
            )
        self.defineRequiredParameter(
            name     = "ProjectedGradientTolerance",
            default  = -1,
            typecast = float,
            message  = "Maximum des composantes du gradient projet� lors de l'arr�t",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "GradientNormTolerance",
            default  = 1.e-05,
            typecast = float,
            message  = "Maximum des composantes du gradient lors de l'arr�t",
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou interm�diaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs suppl�mentaires � stocker et/ou effectuer",
            listval  = ["BMA", "OMA", "OMB", "Innovation"]
            )

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        #
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Param�tres de pilotage
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
        # Op�rateur d'observation
        # -----------------------
        Hm = H["Direct"].appliedTo
        Ha = H["Adjoint"].appliedInXTo
        #
        # Utilisation �ventuelle d'un vecteur H(Xb) pr�calcul�
        # ----------------------------------------------------
        if H["AppliedToX"] is not None and H["AppliedToX"].has_key("HXb"):
            HXb = H["AppliedToX"]["HXb"]
        else:
            HXb = Hm( Xb )
        HXb = numpy.asmatrix(numpy.ravel( HXb )).T
        #
        # Calcul de l'innovation
        # ----------------------
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        d  = Y - HXb
        #
        # Pr�calcul des inversions de B et R
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
            if self._parameters["Minimizer"] == "LM":
                RdemiI = numpy.linalg.cholesky(R).I
        elif self._parameters["R_scalar"] is not None:
            RI = 1.0 / self._parameters["R_scalar"]
            if self._parameters["Minimizer"] == "LM":
                import math
                RdemiI = 1.0 / math.sqrt( self._parameters["R_scalar"] )
        else:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        #
        # D�finition de la fonction-co�t
        # ------------------------------
        def CostFunction(x):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            Jb  = 0.
            Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            J   = float( Jb ) + float( Jo )
            if self._parameters["StoreInternalVariables"]:
                self.StoredVariables["CurrentState"].store( _X.A1 )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            return J
        #
        def GradientOfCostFunction(x):
            _X      = numpy.asmatrix(numpy.ravel( x )).T
            _HX     = Hm( _X )
            _HX     = numpy.asmatrix(numpy.ravel( _HX )).T
            GradJb  = 0.
            GradJo  = - Ha( (_X, RI * (Y - _HX)) )
            GradJ   = numpy.asmatrix( numpy.ravel( GradJb ) + numpy.ravel( GradJo ) ).T
            return GradJ.A1
        #
        def CostFunctionLM(x):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            Jb  = 0.
            Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
            J   = float( Jb ) + float( Jo )
            if self._parameters["StoreInternalVariables"]:
                self.StoredVariables["CurrentState"].store( _X.A1 )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            #
            return numpy.ravel( RdemiI*(Y - _HX) )
        #
        def GradientOfCostFunctionLM(x):
            _X      = numpy.asmatrix(numpy.ravel( x )).T
            _HX     = Hm( _X )
            _HX     = numpy.asmatrix(numpy.ravel( _HX )).T
            GradJb  = 0.
            GradJo  = - Ha( (_X, RI * (Y - _HX)) )
            GradJ   = numpy.asmatrix( numpy.ravel( GradJb ) + numpy.ravel( GradJo ) ).T
            return - RdemiI*H["Tangent"].asMatrix( _X )
        #
        # Point de d�marrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if type(Xb) is type(numpy.matrix([])):
            Xini = Xb.A1.tolist()
        else:
            Xini = list(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        n0 = self.StoredVariables["CostFunctionJ"].stepnumber()
        #
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
        elif self._parameters["Minimizer"] == "LM":
            Minimum, cov_x, infodict, mesg, rc = scipy.optimize.leastsq(
                func        = CostFunctionLM,
                x0          = Xini,
                Dfun        = GradientOfCostFunctionLM,
                args        = (),
                ftol        = self._parameters["CostDecrementTolerance"],
                maxfev      = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                full_output = True,
                )
            nfeval = infodict['nfev']
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        StepMin = numpy.argmin( self.StoredVariables["CostFunctionJ"].valueserie()[n0:] )
        MinJ    = self.StoredVariables["CostFunctionJ"].valueserie(step = StepMin)
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        # ----------------------------------------------------------------
        if self._parameters["StoreInternalVariables"]:
            Minimum = self.StoredVariables["CurrentState"].valueserie(step = StepMin)
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( Minimum )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        # Calculs et/ou stockages suppl�mentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb - Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(Y - Hm(Xa)) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        #
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Termin�"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
