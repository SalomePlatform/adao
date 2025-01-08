# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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

import numpy
from daCore import BasicObjects

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "OBSERVERTEST")
        self.setAttributes(
            tags=(
                "Checking",
            ),
            features=(
                "DerivativeFree",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        print("Results of observer check on all potential variables or commands,")
        print("         only activated on selected ones by explicit association.")
        print("")
        #
        __Xa = 1. + numpy.arange(3.)
        __Xb = numpy.zeros(3)
        __YY = 1. + numpy.arange(5.)
        #
        # Activation des observers sur toutes les variables stockables
        # ------------------------------------------------------------
        self.StoredVariables["Analysis"].store( __Xa )
        self.StoredVariables["CurrentState"].store( __Xa )
        self.StoredVariables["CurrentOptimum"].store( __Xa )
        #
        self.StoredVariables["CostFunctionJb"].store( 1. )
        self.StoredVariables["CostFunctionJo"].store( 2. )
        self.StoredVariables["CostFunctionJ" ].store( 3. )
        self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( 4. )
        self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( 5. )
        self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( 6. )
        self.StoredVariables["IndexOfOptimum"].store( 1 )
        #
        self.StoredVariables["APosterioriCovariance"].store( numpy.diag(__Xa) )
        self.StoredVariables["APosterioriVariances"].store( __Xa )
        self.StoredVariables["APosterioriStandardDeviations"].store( __Xa )
        self.StoredVariables["APosterioriCorrelations"].store( numpy.diag(__Xa) )
        self.StoredVariables["BMA"].store( __Xb - __Xa )
        self.StoredVariables["OMA"].store( __YY )
        self.StoredVariables["OMB"].store( __YY )
        self.StoredVariables["Innovation"].store( __YY )
        self.StoredVariables["InnovationAtCurrentState"].store( __YY )
        self.StoredVariables["SigmaObs2"].store( 1. )
        self.StoredVariables["SigmaBck2"].store( 1. )
        self.StoredVariables["MahalanobisConsistency"].store( 1. )
        self.StoredVariables["SimulationQuantiles"].store( numpy.array((__YY, __YY, __YY)) )
        self.StoredVariables["SimulatedObservationAtBackground"].store( __YY )
        self.StoredVariables["SimulatedObservationAtCurrentState"].store( __YY )
        self.StoredVariables["SimulatedObservationAtOptimum"].store( __YY )
        self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( __YY )
        #
        print("")
        self._post_run()
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
