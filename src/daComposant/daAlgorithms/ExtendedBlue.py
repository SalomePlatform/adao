#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2015 EDF R&D
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
from daCore import BasicObjects
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "EXTENDEDBLUE")
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
            listval  = ["APosterioriCovariance", "BMA", "OMA", "OMB", "Innovation", "SigmaBck2", "SigmaObs2", "MahalanobisConsistency", "SimulationQuantiles"]
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
            message  = "Graine fix�e pour le g�n�rateur al�atoire",
            )
        self.defineRequiredParameter(
            name     = "NumberOfSamplesForQuantiles",
            default  = 100,
            typecast = int,
            message  = "Nombre d'�chantillons simul�s pour le calcul des quantiles",
            minval   = 1,
            )
        self.defineRequiredParameter(
            name     = "SimulationForQuantiles",
            default  = "Linear",
            typecast = str,
            message  = "Type de simulation pour l'estimation des quantiles",
            listval  = ["Linear", "NonLinear"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Op�rateur d'observation
        # -----------------------
        Hm = HO["Tangent"].asMatrix(Xb)
        Hm = Hm.reshape(Y.size,Xb.size) # ADAO & check shape
        Ha = HO["Adjoint"].asMatrix(Xb)
        Ha = Ha.reshape(Xb.size,Y.size) # ADAO & check shape
        H  = HO["Direct"].appliedTo
        #
        # Utilisation �ventuelle d'un vecteur H(Xb) pr�calcul�
        # ----------------------------------------------------
        if HO["AppliedToX"] is not None and HO["AppliedToX"].has_key("HXb"):
            HXb = HO["AppliedToX"]["HXb"]
        else:
            HXb = H( Xb )
        HXb = numpy.asmatrix(numpy.ravel( HXb )).T
        #
        # Pr�calcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Calcul de l'innovation
        # ----------------------
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        d  = Y - HXb
        #
        # Calcul de la matrice de gain et de l'analyse
        # --------------------------------------------
        if Y.size <= Xb.size:
            if Y.size > 100: # len(R)
                _A = R + Hm * B * Ha
                _u = numpy.linalg.solve( _A , d )
                Xa = Xb + B * Ha * _u
            else:
                K  = B * Ha * (R + Hm * B * Ha).I
                Xa = Xb + K*d
        else:
            if Y.size > 100: # len(R)
                _A = BI + Ha * RI * Hm
                _u = numpy.linalg.solve( _A , Ha * RI * d )
                Xa = Xb + _u
            else:
                K = (BI + Ha * RI * Hm).I * Ha * RI
                Xa = Xb + K*d
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        # Calcul de la fonction co�t
        # --------------------------
        if self._parameters["StoreInternalVariables"] or \
           "OMA" in self._parameters["StoreSupplementaryCalculations"] or \
           "SigmaObs2" in self._parameters["StoreSupplementaryCalculations"] or \
           "MahalanobisConsistency" in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulationQuantiles" in self._parameters["StoreSupplementaryCalculations"]:
            HXa  = numpy.matrix(numpy.ravel( H( Xa ) )).T
            oma = Y - HXa
        if self._parameters["StoreInternalVariables"] or \
           "MahalanobisConsistency" in self._parameters["StoreSupplementaryCalculations"]:
            Jb  = 0.5 * (Xa - Xb).T * BI * (Xa - Xb)
            Jo  = 0.5 * oma.T * RI * oma
            J   = float( Jb ) + float( Jo )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
        #
        # Calcul de la covariance d'analyse
        # ---------------------------------
        if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulationQuantiles" in self._parameters["StoreSupplementaryCalculations"]:
            if   (Y.size <= Xb.size) and (Y.size > 100): K  = B * Ha * (R + Hm * B * Ha).I
            elif (Y.size >  Xb.size) and (Y.size > 100): K = (BI + Ha * RI * Hm).I * Ha * RI
            else:                                        pass # K deja calcule
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
        # Calculs et/ou stockages suppl�mentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(oma) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if "SigmaObs2" in self._parameters["StoreSupplementaryCalculations"]:
            TraceR = R.trace(Y.size)
            self.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(oma)).T)) ) / TraceR )
        if "SigmaBck2" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SigmaBck2"].store( float( (d.T * Hm * (Xa - Xb))/(Hm * B * Hm.T).trace() ) )
        if "MahalanobisConsistency" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["MahalanobisConsistency"].store( float( 2.*J/d.size ) )
        if "SimulationQuantiles" in self._parameters["StoreSupplementaryCalculations"]:
            Qtls = self._parameters["Quantiles"]
            nech = self._parameters["NumberOfSamplesForQuantiles"]
            HtM  = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
            HtM  = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
            YfQ  = None
            for i in range(nech):
                if self._parameters["SimulationForQuantiles"] == "Linear":
                    dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                    dYr = numpy.matrix(numpy.ravel( HtM * dXr )).T
                    Yr = HXa + dYr
                elif self._parameters["SimulationForQuantiles"] == "NonLinear":
                    Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                    Yr = numpy.matrix(numpy.ravel( H( Xr ) )).T
                if YfQ is None:
                    YfQ = Yr
                else:
                    YfQ = numpy.hstack((YfQ,Yr))
            YfQ.sort(axis=-1)
            YQ = None
            for quantile in Qtls:
                if not (0. <= quantile <= 1.): continue
                indice = int(nech * quantile - 1./nech)
                if YQ is None: YQ = YfQ[:,indice]
                else:          YQ = numpy.hstack((YQ,YfQ[:,indice]))
            self.StoredVariables["SimulationQuantiles"].store( YQ )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
