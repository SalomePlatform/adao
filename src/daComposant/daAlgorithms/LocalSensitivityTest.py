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

import sys, logging
from daCore import BasicObjects, PlatformInfo
import numpy, copy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "LOCALSENSITIVITYTEST")
        self.defineRequiredParameter(
            name     = "SetDebug",
            default  = False,
            typecast = bool,
            message  = "Activation du mode debug lors de l'exécution",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = ["JacobianMatrixAtCurrentState",],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "CurrentState",
                "JacobianMatrixAtCurrentState",
                "SimulatedObservationAtCurrentState",
                ]
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO"),
            )
        self.setAttributes(tags=(
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        if self._parameters["SetDebug"]:
            CUR_LEVEL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.DEBUG)
            print("===> Beginning of evaluation, activating debug\n")
            print("     %s\n"%("-"*75,))
        #
        # ----------
        Ht = HO["Tangent"].asMatrix( Xb )
        Ht = Ht.reshape(Y.size,Xb.size) # ADAO & check shape
        # ----------
        #
        if self._parameters["SetDebug"]:
            print("\n     %s\n"%("-"*75,))
            print("===> End evaluation, deactivating debug if necessary\n")
            logging.getLogger().setLevel(CUR_LEVEL)
        #
        if self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( Xb )
        if self._toStore("JacobianMatrixAtCurrentState"):
            self.StoredVariables["JacobianMatrixAtCurrentState"].store( Ht )
        if self._toStore("SimulatedObservationAtCurrentState"):
            if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
                HXb = HO["AppliedInX"]["HXb"]
            else:
                HXb = Ht * Xb
            HXb = numpy.asmatrix(numpy.ravel( HXb )).T
            if Y.size != HXb.size:
                raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
            if max(Y.shape) != max(HXb.shape):
                raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( HXb )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
