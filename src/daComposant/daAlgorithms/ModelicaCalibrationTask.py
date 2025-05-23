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

import os
from daCore import BasicObjects

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "MODELICACALIBRATIONTASK")
        # Modelica specific parameters
        self.defineRequiredParameter(
            name     = "ConfigurationFile",
            default  = "",
            typecast = os.path.expanduser,
            message  = "Nom de fichier maître pour le calage d'une simulation 0D/1D",
        )
        self.requireInputArguments(
            mandatory= (),
            optional = (),
        )
        self.setAttributes(
            tags=(
                "Calibration",
                "Dynamic",
                "DataAssimilation",
                "NonLinear",
            ),
            features=(
                "NonLocalOptimization",
                "DerivativeNeeded",
                "ParallelDerivativesOnly",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        if not os.path.exists(self._parameters["ConfigurationFile"]):
            raise ValueError("Configuration file not found with the name: %s"%self._parameters["ConfigurationFile"])
        #
        currdir = os.path.abspath(os.getcwd())
        workdir = os.path.abspath(os.path.dirname(self._parameters["ConfigurationFile"]))
        with open(self._parameters["ConfigurationFile"]) as fid:
            os.chdir(workdir)
            exec(fid.read(), {'__name__':'__main__'})
        os.chdir(currdir)
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
