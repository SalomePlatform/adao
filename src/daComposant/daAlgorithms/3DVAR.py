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
        BasicObjects.Algorithm.__init__(self, "3DVAR")
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
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = ["APosterioriCovariance", "BMA", "OMA", "OMB", "Innovation", "SigmaObs2", "MahalanobisConsistency"]
            )

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
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
        # Précalcul des inversions de B et R
        # ----------------------------------
        if B is not None:
            BI = B.I
        elif self._parameters["B_scalar"] is not None:
            BI = 1.0 / self._parameters["B_scalar"]
        else:
            raise ValueError("Background error covariance matrix has to be properly defined!")
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
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
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
            GradJb  = BI * (_X - Xb)
            GradJo  = - Ha( (_X, RI * (Y - _HX)) )
            GradJ   = numpy.asmatrix( numpy.ravel( GradJb ) + numpy.ravel( GradJo ) ).T
            return GradJ.A1
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if type(Xb) is type(numpy.matrix([])):
            Xini = Xb.A1.tolist()
        else:
            Xini = list(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = self.StoredVariables["CostFunctionJ"].stepnumber()
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
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        StepMin = numpy.argmin( self.StoredVariables["CostFunctionJ"].valueserie()[nbPreviousSteps:] ) + nbPreviousSteps
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
        # Calcul de la covariance d'analyse
        # ---------------------------------
        if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
            HtM = H["Tangent"].asMatrix(ValueForMethodForm = Xa)
            HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
            HaM = H["Adjoint"].asMatrix(ValueForMethodForm = Xa)
            HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
            HessienneI = []
            nb = Xa.size
            for i in range(nb):
                _ee    = numpy.matrix(numpy.zeros(nb)).T
                _ee[i] = 1.
                _HtEE  = numpy.dot(HtM,_ee)
                _HtEE  = numpy.asmatrix(numpy.ravel( _HtEE )).T
                HessienneI.append( numpy.ravel( numpy.dot(BI,_ee) + numpy.dot(HaM,numpy.dot(RI,_HtEE)) ) )
            HessienneI = numpy.matrix( HessienneI )
            A = HessienneI.I
            if min(A.shape) != max(A.shape):
                raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(self._name,str(A.shape)))
            if (numpy.diag(A) < 0).any():
                raise ValueError("The %s a posteriori covariance matrix A has at least one negative value on its diagonal. There is an error in the observation operator, please check it."%(self._name,))
            if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
                try:
                    L = numpy.linalg.cholesky( A )
                except:
                    raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(self._name,))
            self.StoredVariables["APosterioriCovariance"].store( A )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(Hm(Xa)) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if "SigmaObs2" in self._parameters["StoreSupplementaryCalculations"]:
            if R is not None:
                TraceR = R.trace()
            elif self._parameters["R_scalar"] is not None:
                TraceR =  float(self._parameters["R_scalar"]*Y.size)
            self.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(Y)).T-numpy.asmatrix(numpy.ravel(Hm(Xa))).T)) ) / TraceR )
        if "MahalanobisConsistency" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
