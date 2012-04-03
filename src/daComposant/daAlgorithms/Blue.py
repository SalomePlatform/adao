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
        BasicObjects.Algorithm.__init__(self)
        self._name = "BLUE"
        logging.debug("%s Initialisation"%self._name)

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul de l'estimateur BLUE (ou Kalman simple, ou Interpolation Optimale)
        """
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        Hm = H["Direct"].asMatrix()
        Ht = H["Adjoint"].asMatrix()
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if H["AppliedToX"] is not None and H["AppliedToX"].has_key("HXb"):
            logging.debug("%s Utilisation de HXb"%self._name)
            HXb = H["AppliedToX"]["HXb"]
        else:
            logging.debug("%s Calcul de Hm * Xb"%self._name)
            HXb = Hm * Xb
        HXb = numpy.asmatrix(HXb).flatten().T
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if B is not None:
            BI = B.I
        elif Parameters["B_scalar"] is not None:
            BI = 1.0 / Parameters["B_scalar"]
            B = Parameters["B_scalar"]
        if R is not None:
            RI = R.I
        elif Parameters["R_scalar"] is not None:
            RI = 1.0 / Parameters["R_scalar"]
            R = Parameters["R_scalar"]
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
        # Paramètres de pilotage
        # ----------------------
        # Potentiels : "CalculateAPosterioriCovariance"
        if Parameters.has_key("CalculateAPosterioriCovariance"):
            CalculateAPosterioriCovariance = bool(Parameters["CalculateAPosterioriCovariance"])
        else:
            CalculateAPosterioriCovariance = False
        logging.debug("%s Calcul de la covariance a posteriori = %s"%(self._name, CalculateAPosterioriCovariance))
        #
        # Calcul de la matrice de gain dans l'espace le plus petit et de l'analyse
        # ------------------------------------------------------------------------
        if Y.size <= Xb.size:
            logging.debug("%s Calcul de K dans l'espace des observations"%self._name)
            K  = B * Ht * (Hm * B * Ht + R).I
        else:
            logging.debug("%s Calcul de K dans l'espace d'ébauche"%self._name)
            K = (Ht * RI * Hm + BI).I * Ht * RI
        Xa = Xb + K*d
        logging.debug("%s Analyse Xa = %s"%(self._name, Xa))
        #
        # Calcul de la fonction coût
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
        if CalculateAPosterioriCovariance:
            A = ( 1.0 -  K * Hm ) * B
            self.StoredVariables["APosterioriCovariance"].store( A )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("MB")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
