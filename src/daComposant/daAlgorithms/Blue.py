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
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "BLUE")
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
                "Innovation",
                "MahalanobisConsistency",
                "OMA",
                "OMB",
                "SigmaBck2",
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
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            )
        self.setAttributes(tags=(
            "DataAssimilation",
            "Linear",
            "Filter",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        Hm = HO["Tangent"].asMatrix(Xb)
        Hm = Hm.reshape(Y.size,Xb.size) # ADAO & check shape
        Ha = HO["Adjoint"].asMatrix(Xb)
        Ha = Ha.reshape(Xb.size,Y.size) # ADAO & check shape
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
            HXb = HO["AppliedInX"]["HXb"]
        else:
            HXb = Hm * Xb
        HXb = numpy.asmatrix(numpy.ravel( HXb )).T
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Calcul de l'innovation
        # ----------------------
        d  = Y - HXb
        #
        # Calcul de la matrice de gain et de l'analyse
        # --------------------------------------------
        if Y.size <= Xb.size:
            _A = R + numpy.dot(Hm, B * Ha)
            _u = numpy.linalg.solve( _A , d )
            Xa = Xb + B * Ha * _u
        else:
            _A = BI + numpy.dot(Ha, RI * Hm)
            _u = numpy.linalg.solve( _A , numpy.dot(Ha, RI * d) )
            Xa = Xb + _u
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        # Calcul de la fonction coût
        # --------------------------
        if self._parameters["StoreInternalVariables"] or \
            self._toStore("CostFunctionJ")  or self._toStore("CostFunctionJAtCurrentOptimum") or \
            self._toStore("CostFunctionJb") or self._toStore("CostFunctionJbAtCurrentOptimum") or \
            self._toStore("CostFunctionJo") or self._toStore("CostFunctionJoAtCurrentOptimum") or \
            self._toStore("OMA") or \
            self._toStore("SigmaObs2") or \
            self._toStore("MahalanobisConsistency") or \
            self._toStore("SimulatedObservationAtCurrentOptimum") or \
            self._toStore("SimulatedObservationAtCurrentState") or \
            self._toStore("SimulatedObservationAtOptimum") or \
            self._toStore("SimulationQuantiles"):
            HXa = Hm * Xa
            oma = Y - HXa
        if self._parameters["StoreInternalVariables"] or \
            self._toStore("CostFunctionJ")  or self._toStore("CostFunctionJAtCurrentOptimum") or \
            self._toStore("CostFunctionJb") or self._toStore("CostFunctionJbAtCurrentOptimum") or \
            self._toStore("CostFunctionJo") or self._toStore("CostFunctionJoAtCurrentOptimum") or \
            self._toStore("MahalanobisConsistency"):
            Jb  = float( 0.5 * (Xa - Xb).T * BI * (Xa - Xb) )
            Jo  = float( 0.5 * oma.T * RI * oma )
            J   = Jb + Jo
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( Jb )
            self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( Jo )
            self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( J )
        #
        # Calcul de la covariance d'analyse
        # ---------------------------------
        if self._toStore("APosterioriCovariance") or \
            self._toStore("SimulationQuantiles"):
            if   (Y.size <= Xb.size): K  = B * Ha * (R + numpy.dot(Hm, B * Ha)).I
            elif (Y.size >  Xb.size): K = (BI + numpy.dot(Ha, RI * Hm)).I * Ha * RI
            A = B - K * Hm * B
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
        if self._parameters["StoreInternalVariables"] or self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( numpy.ravel(Xa) )
        if self._toStore("CurrentOptimum"):
            self.StoredVariables["CurrentOptimum"].store( numpy.ravel(Xa) )
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( numpy.ravel(oma) )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if self._toStore("SigmaObs2"):
            TraceR = R.trace(Y.size)
            self.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(oma)).T)) ) / TraceR )
        if self._toStore("SigmaBck2"):
            self.StoredVariables["SigmaBck2"].store( float( (d.T * Hm * (Xa - Xb))/(Hm * B * Hm.T).trace() ) )
        if self._toStore("MahalanobisConsistency"):
            self.StoredVariables["MahalanobisConsistency"].store( float( 2.*J/d.size ) )
        if self._toStore("SimulationQuantiles"):
            nech = self._parameters["NumberOfSamplesForQuantiles"]
            YfQ  = None
            for i in range(nech):
                if self._parameters["SimulationForQuantiles"] == "Linear":
                    dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                    dYr = numpy.matrix(numpy.ravel( Hm * dXr )).T
                    Yr = HXa + dYr
                elif self._parameters["SimulationForQuantiles"] == "NonLinear":
                    Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                    Yr = numpy.matrix(numpy.ravel( Hm * Xr )).T
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
        if self._toStore("SimulatedObservationAtCurrentState"):
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(HXa) )
        if self._toStore("SimulatedObservationAtCurrentOptimum"):
            self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( numpy.ravel(HXa) )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
