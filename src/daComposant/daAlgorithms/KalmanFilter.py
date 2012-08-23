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

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "KALMANFILTER")
        self.defineRequiredParameter(
            name     = "CalculateAPosterioriCovariance",
            default  = False,
            typecast = bool,
            message  = "Calcul de la covariance a posteriori",
            )

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Calcul de l'estimateur du filtre de Kalman

        Remarque : les observations sont exploitées à partir du pas de temps 1,
        et sont utilisées dans Yo comme rangées selon ces indices. Donc le pas 0
        n'est pas utilisé puisque la première étape de Kalman passe de 0 à 1
        avec l'observation du pas 1.
        """
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
        if B is None:
            raise ValueError("Background error covariance matrix has to be properly defined!")
        if R is None:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        #
        # Opérateur d'évolution
        # ---------------------
        Mm = M["Tangent"].asMatrix(None)
        Mt = M["Adjoint"].asMatrix(None)
        #
        # Nombre de pas du Kalman identique au nombre de pas d'observations
        # -----------------------------------------------------------------
        duration = Y.stepnumber()
        #
        # Initialisation
        # --------------
        Xn = Xb
        Pn = B
        self.StoredVariables["Analysis"].store( Xn.A1 )
        if self._parameters["CalculateAPosterioriCovariance"]:
            self.StoredVariables["APosterioriCovariance"].store( Pn )
        #
        for step in range(duration-1):
            logging.debug("%s Etape de Kalman %i (i.e. %i->%i) sur un total de %i"%(self._name, step+1, step,step+1, duration-1))
            #
            # Etape de prédiction
            # -------------------
            Xn_predicted = Mm * Xn
            Pn_predicted = Mm * Pn * Mt + Q
            #
            # Etape de correction
            # -------------------
            d  = Y.valueserie(step+1) - Hm * Xn_predicted
            K  = Pn_predicted * Ha * (Hm * Pn_predicted * Ha + R).I
            Xn = Xn_predicted + K * d
            Pn = Pn_predicted - K * Hm * Pn_predicted
            #
            self.StoredVariables["Analysis"].store( Xn.A1 )
            self.StoredVariables["Innovation"].store( d.A1 )
            if self._parameters["CalculateAPosterioriCovariance"]:
                self.StoredVariables["APosterioriCovariance"].store( Pn )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
