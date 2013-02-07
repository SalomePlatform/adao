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
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = ["APosterioriCovariance", "CostFunctionJ", "Innovation"]
            )
        self.defineRequiredParameter(
            name     = "EstimationType",
            default  = "State",
            typecast = str,
            message  = "Estimation d'etat ou de parametres",
            listval  = ["State", "Parameters"],
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Opérateurs
        # ----------
        if B is None:
            raise ValueError("Background error covariance matrix has to be properly defined!")
        if R is None:
            raise ValueError("Observation error covariance matrix has to be properly defined!")
        #
        Ht = HO["Tangent"].asMatrix(Xb)
        Ha = HO["Adjoint"].asMatrix(Xb)
        #
        if self._parameters["EstimationType"] == "State":
            Mt = EM["Tangent"].asMatrix(Xb)
            Ma = EM["Adjoint"].asMatrix(Xb)
        #
        if CM is not None and CM.has_key("Tangent") and U is not None:
            Cm = CM["Tangent"].asMatrix(Xb)
        else:
            Cm = None
        #
        # Nombre de pas du Kalman identique au nombre de pas d'observations
        # -----------------------------------------------------------------
        if hasattr(Y,"stepnumber"):
            duration = Y.stepnumber()
        else:
            duration = 2
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if "CostFunctionJ" in self._parameters["StoreSupplementaryCalculations"]:
            if B is not None:
                BI = B.I
            elif self._parameters["B_scalar"] is not None:
                BI = 1.0 / self._parameters["B_scalar"]
            #
            if R is not None:
                RI = R.I
            elif self._parameters["R_scalar"] is not None:
                RI = 1.0 / self._parameters["R_scalar"]
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
            Ynpu = numpy.asmatrix(numpy.ravel( Y[step+1] )).T
            #
            if U is not None:
                if hasattr(U,"store") and len(U)>1:
                    Un = numpy.asmatrix(numpy.ravel( U[step] )).T
                elif hasattr(U,"store") and len(U)==1:
                    Un = numpy.asmatrix(numpy.ravel( U[0] )).T
                else:
                    Un = numpy.asmatrix(numpy.ravel( U )).T
            else:
                Un = None
            #
            if self._parameters["EstimationType"] == "State" and Cm is not None and Un is not None:
                Xn_predicted = Mt * Xn + Cm * Un
                Pn_predicted = Mt * Pn * Ma + Q
            elif self._parameters["EstimationType"] == "State" and (Cm is None or Un is None):
                Xn_predicted = Mt * Xn
                Pn_predicted = Mt * Pn * Ma + Q
            elif self._parameters["EstimationType"] == "Parameters":
                # Xn_predicted = Mt * Xn
                # Pn_predicted = Mt * Pn * Ma + Q
                # --- > Par principe, M = Id, Q = 0
                Xn_predicted = Xn
                Pn_predicted = Pn
            #
            if self._parameters["EstimationType"] == "Parameters" and Cm is not None and Un is not None:
                d  = Ynpu - Ht * Xn_predicted - Cm * Un
            else:
                d  = Ynpu - Ht * Xn_predicted
            #
            K  = Pn_predicted * Ha * (Ht * Pn_predicted * Ha + R).I
            Xn = Xn_predicted + K * d
            Pn = Pn_predicted - K * Ht * Pn_predicted
            #
            self.StoredVariables["Analysis"].store( Xn.A1 )
            if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["Innovation"].store( numpy.ravel( d.A1 ) )
            if "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["APosterioriCovariance"].store( Pn )
            if "CostFunctionJ" in self._parameters["StoreSupplementaryCalculations"]:
                Jb  = 0.5 * (Xn - Xb).T * BI * (Xn - Xb)
                Jo  = 0.5 * d.T * RI * d
                J   = float( Jb ) + float( Jo )
                self.StoredVariables["CostFunctionJb"].store( Jb )
                self.StoredVariables["CostFunctionJo"].store( Jo )
                self.StoredVariables["CostFunctionJ" ].store( J )
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
