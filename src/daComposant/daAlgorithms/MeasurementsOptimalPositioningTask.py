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
from daAlgorithms.Atoms import ecweim
from daAlgorithms.Atoms import eosg

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "MEASUREMENTSOPTIMALPOSITIONING")
        self.defineRequiredParameter(
            name     = "Variant",
            default  = "PositioningBylcEIM",
            typecast = str,
            message  = "Variant ou formulation de la méthode",
            listval  = [
                "PositioningByEIM",
                "PositioningBylcEIM",
                ],
            )
        self.defineRequiredParameter(
            name     = "EnsembleOfSnapshots",
            default  = [],
            typecast = numpy.array,
            message  = "Ensemble de vecteurs d'état physique (snapshots), 1 état par colonne",
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfLocations",
            default  = 1,
            typecast = int,
            message  = "Nombre maximal de positions",
            minval   = 0,
            )
        self.defineRequiredParameter(
            name     = "ExcludeLocations",
            default  = [],
            typecast = tuple,
            message  = "Liste des positions exclues selon la numérotation interne d'un snapshot",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "ErrorNorm",
            default  = "L2",
            typecast = str,
            message  = "Norme d'erreur utilisée pour le critère d'optimalité des positions",
            listval  = ["L2", "Linf"]
            )
        self.defineRequiredParameter(
            name     = "ErrorNormTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Valeur limite inférieure du critère d'optimalité forçant l'arrêt",
            minval   = 0.,
            )
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
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "EnsembleOfSimulations",
                "EnsembleOfStates",
                "OptimalPoints",
                "ReducedBasis",
                "Residus",
                ]
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.requireInputArguments(
            mandatory= (),
            optional = ("Xb", "HO"),
            )
        self.setAttributes(tags=(
            "Reduction",
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        #--------------------------
        if   self._parameters["Variant"] == "PositioningBylcEIM":
            if len(self._parameters["EnsembleOfSnapshots"]) > 0:
                if self._toStore("EnsembleOfSimulations"):
                    self.StoredVariables["EnsembleOfSimulations"].store( self._parameters["EnsembleOfSnapshots"] )
                ecweim.EIM_offline(self, self._parameters["EnsembleOfSnapshots"])
            elif isinstance(HO, dict):
                ecweim.EIM_offline(self, eosg.eosg(self, Xb, HO))
            else:
                raise ValueError("Snapshots or Operator have to be given in order to launch the analysis")
        #
        elif self._parameters["Variant"] == "PositioningByEIM":
            if len(self._parameters["EnsembleOfSnapshots"]) > 0:
                if self._toStore("EnsembleOfSimulations"):
                    self.StoredVariables["EnsembleOfSimulations"].store( self._parameters["EnsembleOfSnapshots"] )
                ecweim.EIM_offline(self, self._parameters["EnsembleOfSnapshots"])
            elif isinstance(HO, dict):
                ecweim.EIM_offline(self, eosg.eosg(self, Xb, HO))
            else:
                raise ValueError("Snapshots or Operator have to be given in order to launch the analysis")
        #
        #--------------------------
        else:
            raise ValueError("Error in Variant name: %s"%self._parameters["Variant"])
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')