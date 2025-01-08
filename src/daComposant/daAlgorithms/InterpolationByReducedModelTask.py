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
from daAlgorithms.Atoms import ecweim

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "INTERPOLATIONBYREDUCEDMODEL")
        self.defineRequiredParameter(
            name     = "ReducedBasis",
            default  = [],
            typecast = numpy.array,
            message  = "Base réduite, 1 vecteur par colonne",
        )
        self.defineRequiredParameter(
            name     = "OptimalLocations",
            default  = [],
            typecast = numpy.array,
            message  = "Liste des indices ou noms de positions optimales de mesure selon l'ordre interne d'un vecteur de base",  # noqa: E501
        )
        self.defineRequiredParameter(
            name     = "ObservationsAlreadyRestrictedOnOptimalLocations",
            default  = True,
            typecast = bool,
            message  = "Stockage des mesures restreintes a priori aux positions optimales de mesure ou non",
        )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "Analysis",
                "ReducedCoordinates",
            ]
        )
        self.requireInputArguments(
            mandatory= ("Y",),
            optional = (),
        )
        self.setAttributes(
            tags=(
                "Reduction",
                "Interpolation",
            ),
            features=(
                "DerivativeFree",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        # --------------------------
        __rb = self._parameters["ReducedBasis"]
        __ip = self._parameters["OptimalLocations"]
        if len(__ip) != __rb.shape[1]:
            raise ValueError("The number of optimal measurement locations (%i) and the dimension of the RB (%i) has to be the same."%(len(__ip), __rb.shape[1]))  # noqa: E501
        #
        # Nombre de pas identique au nombre de pas d'observations
        if hasattr(Y, "stepnumber"):
            duration = Y.stepnumber()
        else:
            duration = 2
        #
        for step in range(0, duration - 1):
            #
            # La boucle sur les mesures permet une interpolation par jeu de mesure,
            # sans qu'il y ait de lien entre deux jeux successifs de mesures.
            #
            # Important : les observations sont données sur tous les points
            # possibles ou déjà restreintes aux points optimaux de mesure, mais
            # ne sont utilisés qu'aux points optimaux
            if hasattr(Y, "store"):
                _Ynpu = numpy.ravel( Y[step + 1] ).reshape((-1, 1))
            else:
                _Ynpu = numpy.ravel( Y ).reshape((-1, 1))
            if self._parameters["ObservationsAlreadyRestrictedOnOptimalLocations"]:
                __rm = _Ynpu
            else:
                __rm = _Ynpu[__ip]
            #
            # Interpolation
            ecweim.EIM_online(self, __rb, __rm, __ip)
        # --------------------------
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
