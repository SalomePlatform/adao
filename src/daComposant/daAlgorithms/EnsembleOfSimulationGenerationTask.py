# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2023 EDF R&D
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
from daAlgorithms.Atoms import eosg

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ENSEMBLEOFSIMULATIONGENERATION")
        self.defineRequiredParameter(
            name     = "SampleAsnUplet",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par une liste de n-uplet",
            )
        self.defineRequiredParameter(
            name     = "SampleAsExplicitHyperCube",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonnages de chaque variable comme une liste",
            )
        self.defineRequiredParameter(
            name     = "SampleAsMinMaxStepHyperCube",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonnages de chaque variable par un triplet [min,max,step]",
            )
        self.defineRequiredParameter(
            name     = "SampleAsIndependantRandomVariables",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont les points sur chaque axe proviennent de l'échantillonnage indépendant de la variable selon la spécification ['distribution',[parametres],nombre]",
            )
        self.defineRequiredParameter(
            name     = "SetDebug",
            default  = False,
            typecast = bool,
            message  = "Activation du mode debug lors de l'exécution",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = ["EnsembleOfSimulations",],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "EnsembleOfSimulations",
                "EnsembleOfStates",
                ]
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "HO"),
            optional = (),
            )
        self.setAttributes(tags=(
            "Reduction",
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        #--------------------------
        eosg.eosg(self, Xb, HO)
        #--------------------------
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')