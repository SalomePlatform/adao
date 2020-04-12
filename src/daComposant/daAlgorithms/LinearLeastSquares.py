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
            listval  = [
                "Analysis",
                "CostFunctionJ",
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJb",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJo",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentOptimum",
                "CurrentState",
                "OMA",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                ]
            )
        self.requireInputArguments(
            mandatory= ("Y", "HO", "R"),
            )
        self.setAttributes(tags=(
            "Optimization",
            "Linear",
            "Variational",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
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
            self._toStore("CostFunctionJ")  or self._toStore("CostFunctionJAtCurrentOptimum") or \
            self._toStore("CostFunctionJb") or self._toStore("CostFunctionJbAtCurrentOptimum") or \
            self._toStore("CostFunctionJo") or self._toStore("CostFunctionJoAtCurrentOptimum") or \
            self._toStore("OMA") or \
            self._toStore("SimulatedObservationAtCurrentOptimum") or \
            self._toStore("SimulatedObservationAtCurrentState") or \
            self._toStore("SimulatedObservationAtOptimum"):
            HXa = Hm * Xa
            oma = Y - HXa
        if self._parameters["StoreInternalVariables"] or \
            self._toStore("CostFunctionJ")  or self._toStore("CostFunctionJAtCurrentOptimum") or \
            self._toStore("CostFunctionJb") or self._toStore("CostFunctionJbAtCurrentOptimum") or \
            self._toStore("CostFunctionJo") or self._toStore("CostFunctionJoAtCurrentOptimum"):
            Jb  = 0.
            Jo  = float( 0.5 * oma.T * RI * oma )
            J   = Jb + Jo
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( Jb )
            self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( Jo )
            self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( J )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._parameters["StoreInternalVariables"] or self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( numpy.ravel(Xa) )
        if self._toStore("CurrentOptimum"):
            self.StoredVariables["CurrentOptimum"].store( numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( numpy.ravel(oma) )
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
