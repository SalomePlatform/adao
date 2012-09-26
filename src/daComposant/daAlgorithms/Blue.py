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

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "BLUE")
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = ["APosterioriCovariance", "BMA", "OMA", "OMB", "Innovation", "SigmaBck2", "SigmaObs2"]
            )

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Opérateur d'observation
        # -----------------------
        Hm = H["Tangent"].asMatrix(None)
        Ha = H["Adjoint"].asMatrix(None)
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if H["AppliedToX"] is not None and H["AppliedToX"].has_key("HXb"):
            HXb = H["AppliedToX"]["HXb"]
        else:
            HXb = Hm * Xb
        HXb = numpy.asmatrix(numpy.ravel( HXb )).T
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if B is not None:
            BI = B.I
        elif self._parameters["B_scalar"] is not None:
            BI = 1.0 / self._parameters["B_scalar"]
            B = self._parameters["B_scalar"]
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
            if self._parameters["R_scalar"] is not None:
                R = self._parameters["R_scalar"] * numpy.eye(len(Y), dtype=numpy.float)
            K  = B * Ha * (Hm * B * Ha + R).I
        else:
            K = (Ha * RI * Hm + BI).I * Ha * RI
        Xa = Xb + K*d
        #
        # Calcul de la fonction coût
        # --------------------------
        oma = Y - Hm * Xa
        Jb  = 0.5 * (Xa - Xb).T * BI * (Xa - Xb)
        Jo  = 0.5 * oma.T * RI * oma
        J   = float( Jb ) + float( Jo )
        self.StoredVariables["Analysis"].store( Xa.A1 )
        self.StoredVariables["CostFunctionJb"].store( Jb )
        self.StoredVariables["CostFunctionJo"].store( Jo )
        self.StoredVariables["CostFunctionJ" ].store( J )
        #
        # Calcul de la covariance d'analyse
        # ---------------------------------
        if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
            A = B - K * Hm * B
            if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
                try:
                    L = numpy.linalg.cholesky( A )
                except:
                    raise ValueError("The BLUE a posteriori covariance matrix A is not symmetric positive-definite. Check your B and R a priori covariances.")
            self.StoredVariables["APosterioriCovariance"].store( A )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb - Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(oma) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if "SigmaObs2" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SigmaObs2"].store( float( (d.T * (Y-Hm*Xa)) / R.trace() ) )
        if "SigmaBck2" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SigmaBck2"].store( float( (d.T * Hm * (Xa - Xb))/(Hm * B * Hm.T).trace() ) )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
