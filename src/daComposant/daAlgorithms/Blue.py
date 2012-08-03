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

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "BLUE")
        self.defineRequiredParameter(
            name     = "CalculateAPosterioriCovariance",
            default  = False,
            typecast = bool,
            message  = "Calcul de la covariance a posteriori",
            )

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul de l'estimateur BLUE (ou Kalman simple, ou Interpolation Optimale)
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Op�rateur d'observation
        # -----------------------
        Hm = H["Direct"].asMatrix()
        Ha = H["Adjoint"].asMatrix()
        #
        # Utilisation �ventuelle d'un vecteur H(Xb) pr�calcul�
        # ----------------------------------------------------
        if H["AppliedToX"] is not None and H["AppliedToX"].has_key("HXb"):
            logging.debug("%s Utilisation de HXb"%self._name)
            HXb = H["AppliedToX"]["HXb"]
        else:
            logging.debug("%s Calcul de Hm * Xb"%self._name)
            HXb = Hm * Xb
        HXb = numpy.asmatrix(HXb).flatten().T
        #
        # Pr�calcul des inversions de B et R
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
        logging.debug("%s Innovation d = %s"%(self._name, d))
        #
        # Calcul de la matrice de gain et de l'analyse
        # --------------------------------------------
        if Y.size <= Xb.size:
            if self._parameters["R_scalar"] is not None:
                R = self._parameters["R_scalar"] * numpy.eye(len(Y), dtype=numpy.float)
            logging.debug("%s Calcul de K dans l'espace des observations"%self._name)
            K  = B * Ha * (Hm * B * Ha + R).I
        else:
            logging.debug("%s Calcul de K dans l'espace d'�bauche"%self._name)
            K = (Ha * RI * Hm + BI).I * Ha * RI
        Xa = Xb + K*d
        logging.debug("%s Analyse Xa = %s"%(self._name, Xa))
        #
        # Calcul de la fonction co�t
        # --------------------------
        Jb  = 0.5 * (Xa - Xb).T * BI * (Xa - Xb)
        Jo  = 0.5 * d.T * RI * d
        J   = float( Jb ) + float( Jo )
        logging.debug("%s CostFunction Jb = %s"%(self._name, Jb))
        logging.debug("%s CostFunction Jo = %s"%(self._name, Jo))
        logging.debug("%s CostFunction J  = %s"%(self._name, J))
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        self.StoredVariables["Innovation"].store( d.A1 )
        self.StoredVariables["CostFunctionJb"].store( Jb )
        self.StoredVariables["CostFunctionJo"].store( Jo )
        self.StoredVariables["CostFunctionJ" ].store( J )
        #
        # Calcul de la covariance d'analyse
        # ---------------------------------
        if self._parameters["CalculateAPosterioriCovariance"]:
            A = ( 1.0 -  K * Hm ) * B
            self.StoredVariables["APosterioriCovariance"].store( A )
        #
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        logging.debug("%s Termin�"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
