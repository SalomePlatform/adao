#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2013 EDF R&D
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
        BasicObjects.Algorithm.__init__(self, "KALMANFILTER")
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs suppl�mentaires � stocker et/ou effectuer",
            listval  = ["APosterioriCovariance", "Innovation"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Op�rateurs
        # ----------
        if B is None:
            raise ValueError("Background error covariance matrix has to be properly defined!")
        if R is None:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        Hm = HO["Tangent"].asMatrix(None)
        Ha = HO["Adjoint"].asMatrix(None)
        #
        Mm = EM["Tangent"].asMatrix(None)
        Mt = EM["Adjoint"].asMatrix(None)
        #
        if CM is not None and U is not None:
            Cm = CM["Tangent"].asMatrix(None)
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
        if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["APosterioriCovariance"].store( Pn )
        #
        for step in range(duration-1):
            if CM is not None and U is not None:
                if hasattr(U,"store") and len(U)>1:
                    Xn_predicted = Mm * Xn + Cm * numpy.asmatrix(numpy.ravel( U[step] )).T
                elif hasattr(U,"store") and len(U)==1:
                    Xn_predicted = Mm * Xn + Cm * numpy.asmatrix(numpy.ravel( U[0] )).T
                else:
                    Xn_predicted = Mm * Xn + Cm * numpy.asmatrix(numpy.ravel( U )).T
            else:
                Xn_predicted = Mm * Xn
            Pn_predicted = Mm * Pn * Mt + Q
            #
            d  = numpy.asmatrix(numpy.ravel( Y[step+1] )).T - Hm * Xn_predicted
            K  = Pn_predicted * Ha * (Hm * Pn_predicted * Ha + R).I
            Xn = Xn_predicted + K * d
            Pn = Pn_predicted - K * Hm * Pn_predicted
            #
            self.StoredVariables["Analysis"].store( Xn.A1 )
            if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["Innovation"].store( numpy.ravel( d.A1 ) )
            if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["APosterioriCovariance"].store( Pn )
        #
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Termin�"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
