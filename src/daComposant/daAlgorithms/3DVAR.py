# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects
import numpy, scipy.optimize, scipy.version

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
            message  = "Diminution relative minimale du coût lors de l'arrêt",
            minval   = 0.,
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
            minval   = 0.,
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
            listval  = [
                "Analysis",
                "APosterioriCorrelations",
                "APosterioriCovariance",
                "APosterioriStandardDeviations",
                "APosterioriVariances",
                "BMA",
                "CostFunctionJ",
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJb",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJo",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentOptimum",
                "CurrentState",
                "IndexOfOptimum",
                "Innovation",
                "InnovationAtCurrentState",
                "JacobianMatrixAtBackground",
                "JacobianMatrixAtOptimum",
                "KalmanGainAtOptimum",
                "MahalanobisConsistency",
                "OMA",
                "OMB",
                "SigmaObs2",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                "SimulationQuantiles",
                ]
            )
        self.defineRequiredParameter(
            name     = "Quantiles",
            default  = [],
            typecast = tuple,
            message  = "Liste des valeurs de quantiles",
            minval   = 0.,
            maxval   = 1.,
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter(
            name     = "NumberOfSamplesForQuantiles",
            default  = 100,
            typecast = int,
            message  = "Nombre d'échantillons simulés pour le calcul des quantiles",
            minval   = 1,
            )
        self.defineRequiredParameter(
            name     = "SimulationForQuantiles",
            default  = "Linear",
            typecast = str,
            message  = "Type de simulation pour l'estimation des quantiles",
            listval  = ["Linear", "NonLinear"]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B" ),
            )
        self.setAttributes(tags=(
            "DataAssimilation",
            "NonLinear",
            "Variational",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        if "Minimizer" in self._parameters and self._parameters["Minimizer"] == "TNC":
            self.setParameterValue("StoreInternalVariables",True)
        #
        # Opérateurs
        # ----------
        Hm = HO["Direct"].appliedTo
        Ha = HO["Adjoint"].appliedInXTo
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
            HXb = Hm( Xb, HO["AppliedInX"]["HXb"] )
        else:
            HXb = Hm( Xb )
        HXb = numpy.asmatrix(numpy.ravel( HXb )).T
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        #
        if self._toStore("JacobianMatrixAtBackground"):
            HtMb = HO["Tangent"].asMatrix(ValueForMethodForm = Xb)
            HtMb = HtMb.reshape(Y.size,Xb.size) # ADAO & check shape
            self.StoredVariables["JacobianMatrixAtBackground"].store( HtMb )
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            if self._parameters["StoreInternalVariables"] or \
                self._toStore("CurrentState") or \
                self._toStore("CurrentOptimum"):
                self.StoredVariables["CurrentState"].store( _X )
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            _Innovation = Y - _HX
            if self._toStore("SimulatedObservationAtCurrentState") or \
                self._toStore("SimulatedObservationAtCurrentOptimum"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            if self._toStore("InnovationAtCurrentState"):
                self.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
            #
            Jb  = float( 0.5 * (_X - Xb).T * BI * (_X - Xb) )
            Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
            J   = Jb + Jo
            #
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            if self._toStore("IndexOfOptimum") or \
                self._toStore("CurrentOptimum") or \
                self._toStore("CostFunctionJAtCurrentOptimum") or \
                self._toStore("CostFunctionJbAtCurrentOptimum") or \
                self._toStore("CostFunctionJoAtCurrentOptimum") or \
                self._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if self._toStore("IndexOfOptimum"):
                self.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if self._toStore("CurrentOptimum"):
                self.StoredVariables["CurrentOptimum"].store( self.StoredVariables["CurrentState"][IndexMin] )
            if self._toStore("SimulatedObservationAtCurrentOptimum"):
                self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
            if self._toStore("CostFunctionJbAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJb"][IndexMin] )
            if self._toStore("CostFunctionJoAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJo"][IndexMin] )
            if self._toStore("CostFunctionJAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( self.StoredVariables["CostFunctionJ" ][IndexMin] )
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
        Xini = numpy.ravel(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = self.StoredVariables["CostFunctionJ"].stepnumber()
        #
        if self._parameters["Minimizer"] == "LBFGSB":
            # Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
            if "0.19" <= scipy.version.version <= "1.1.0":
                import lbfgsbhlt as optimiseur
            else:
                import scipy.optimize as optimiseur
            Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = self._parameters["Bounds"],
                maxfun      = self._parameters["MaximumNumberOfSteps"]-1,
                factr       = self._parameters["CostDecrementTolerance"]*1.e14,
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                iprint      = self._parameters["optiprint"],
                )
            nfeval = Informations['funcalls']
            rc     = Informations['warnflag']
        elif self._parameters["Minimizer"] == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = self._parameters["Bounds"],
                maxfun      = self._parameters["MaximumNumberOfSteps"],
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                messages    = self._parameters["optmessages"],
                )
        elif self._parameters["Minimizer"] == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                disp        = self._parameters["optdisp"],
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
                disp        = self._parameters["optdisp"],
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
                disp        = self._parameters["optdisp"],
                full_output = True,
                )
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = self.StoredVariables["CostFunctionJ"][IndexMin]
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        # ----------------------------------------------------------------
        if self._parameters["StoreInternalVariables"] or self._toStore("CurrentState"):
            Minimum = self.StoredVariables["CurrentState"][IndexMin]
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( Minimum )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        if self._toStore("OMA") or \
            self._toStore("SigmaObs2") or \
            self._toStore("SimulationQuantiles") or \
            self._toStore("SimulatedObservationAtOptimum"):
            if self._toStore("SimulatedObservationAtCurrentState"):
                HXa = self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
            elif self._toStore("SimulatedObservationAtCurrentOptimum"):
                HXa = self.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
            else:
                HXa = Hm( Xa )
        #
        # Calcul de la covariance d'analyse
        # ---------------------------------
        if self._toStore("APosterioriCovariance") or \
            self._toStore("SimulationQuantiles") or \
            self._toStore("JacobianMatrixAtOptimum") or \
            self._toStore("KalmanGainAtOptimum"):
            HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
            HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
        if self._toStore("APosterioriCovariance") or \
            self._toStore("SimulationQuantiles") or \
            self._toStore("KalmanGainAtOptimum"):
            HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
            HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
        if self._toStore("APosterioriCovariance") or \
            self._toStore("SimulationQuantiles"):
            HessienneI = []
            nb = Xa.size
            for i in range(nb):
                _ee    = numpy.matrix(numpy.zeros(nb)).T
                _ee[i] = 1.
                _HtEE  = numpy.dot(HtM,_ee)
                _HtEE  = numpy.asmatrix(numpy.ravel( _HtEE )).T
                HessienneI.append( numpy.ravel( BI*_ee + HaM * (RI * _HtEE) ) )
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
        if self._toStore("APosterioriCovariance"):
            self.StoredVariables["APosterioriCovariance"].store( A )
        if self._toStore("JacobianMatrixAtOptimum"):
            self.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
        if self._toStore("KalmanGainAtOptimum"):
            if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
            elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
            self.StoredVariables["KalmanGainAtOptimum"].store( KG )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("Innovation") or \
            self._toStore("SigmaObs2") or \
            self._toStore("MahalanobisConsistency") or \
            self._toStore("OMB"):
            d  = Y - HXb
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if self._toStore("SigmaObs2"):
            TraceR = R.trace(Y.size)
            self.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(Y)).T-numpy.asmatrix(numpy.ravel(HXa)).T)) ) / TraceR )
        if self._toStore("MahalanobisConsistency"):
            self.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
        if self._toStore("SimulationQuantiles"):
            nech = self._parameters["NumberOfSamplesForQuantiles"]
            HXa  = numpy.matrix(numpy.ravel( HXa )).T
            YfQ  = None
            for i in range(nech):
                if self._parameters["SimulationForQuantiles"] == "Linear":
                    dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                    dYr = numpy.matrix(numpy.ravel( HtM * dXr )).T
                    Yr = HXa + dYr
                elif self._parameters["SimulationForQuantiles"] == "NonLinear":
                    Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                    Yr = numpy.matrix(numpy.ravel( Hm( Xr ) )).T
                if YfQ is None:
                    YfQ = Yr
                else:
                    YfQ = numpy.hstack((YfQ,Yr))
            YfQ.sort(axis=-1)
            YQ = None
            for quantile in self._parameters["Quantiles"]:
                if not (0. <= float(quantile) <= 1.): continue
                indice = int(nech * float(quantile) - 1./nech)
                if YQ is None: YQ = YfQ[:,indice]
                else:          YQ = numpy.hstack((YQ,YfQ[:,indice]))
            self.StoredVariables["SimulationQuantiles"].store( YQ )
        if self._toStore("SimulatedObservationAtBackground"):
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
