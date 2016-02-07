#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2016 EDF R&D
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
        BasicObjects.Algorithm.__init__(self, "LINEARLEASTSQUARES")
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
            listval  = ["OMA", "CurrentState", "CostFunctionJ", "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Opérateur d'observation
        # -----------------------
        Hm = HO["Tangent"].asMatrix(None)
        Hm = Hm.reshape(Y.size,-1) # ADAO & check shape
        Ha = HO["Adjoint"].asMatrix(None)
        Ha = Ha.reshape(-1,Y.size) # ADAO & check shape
        #
        RI = R.getI()
        #
        # Calcul de la matrice de gain et de l'analyse
        # --------------------------------------------
        K = (Ha * RI * Hm).I * Ha * RI
        Xa =  K * Y
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        # Calcul de la fonction coût
        # --------------------------
        if self._parameters["StoreInternalVariables"] or \
           "CostFunctionJ"                 in self._parameters["StoreSupplementaryCalculations"] or \
           "OMA"                           in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            HXa = Hm * Xa
            oma = Y - HXa
        if self._parameters["StoreInternalVariables"] or \
           "CostFunctionJ"                 in self._parameters["StoreSupplementaryCalculations"]:
            Jb  = 0.
            Jo  = 0.5 * oma.T * RI * oma
            J   = float( Jb ) + float( Jo )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._parameters["StoreInternalVariables"] or "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["CurrentState"].store( numpy.ravel(Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(oma) )
        if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(HXa) )
        if "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
