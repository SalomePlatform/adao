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
from daCore import BasicObjects, NumericObjects
from daAlgorithms.Atoms import mmqr

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "QUANTILEREGRESSION")
        self.defineRequiredParameter(
            name     = "Quantile",
            default  = 0.5,
            typecast = float,
            message  = "Quantile pour la régression de quantile",
            minval   = 0.,
            maxval   = 1.,
        )
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "MMQR",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = ["MMQR",],
        )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfIterations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = 1,
            oldname  = "MaximumNumberOfSteps",
        )
        self.defineRequiredParameter(
            name     = "CostDecrementTolerance",
            default  = 1.e-6,
            typecast = float,
            message  = "Maximum de variation de la fonction d'estimation lors de l'arrêt",
        )
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
                "BMA",
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "CurrentIterationNumber",
                "CurrentState",
                "Innovation",
                "OMA",
                "OMB",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
            ]
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
        )
        self.defineRequiredParameter(
            name     = "InitializationPoint",
            typecast = numpy.ravel,
            message  = "État initial imposé (par défaut, c'est l'ébauche si None)",
        )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO" ),
        )
        self.setAttributes(
            tags=(
                "Optimization",
                "Risk",
                "Variational",
            ),
            features=(
                "LocalOptimization",
                "DerivativeNeeded",
                "ConvergenceOnBoth",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        self._parameters["Bounds"] = NumericObjects.ForceNumericBounds( self._parameters["Bounds"] )
        #
        Hm = HO["Direct"].appliedTo

        def CostFunction(x):
            _X = numpy.asarray(x).reshape((-1, 1))
            if self._parameters["StoreInternalVariables"] or \
                    self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( _X )
            _HX = numpy.asarray(Hm( _X )).reshape((-1, 1))
            if self._toStore("SimulatedObservationAtCurrentState"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            Jb  = 0.
            Jo  = 0.
            J   = Jb + Jo
            #
            self.StoredVariables["CurrentIterationNumber"].store( len(self.StoredVariables["CostFunctionJ"]) )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            return _HX

        def GradientOfCostFunction(x):
            _X = numpy.asarray(x).reshape((-1, 1))
            Hg = HO["Tangent"].asMatrix( _X )
            return Hg
        #
        Xini = self._parameters["InitializationPoint"]
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        if self._parameters["Minimizer"] == "MMQR":
            Minimum, J_optimal, Informations = mmqr.mmqr(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                bounds      = self._parameters["Bounds"],
                quantile    = self._parameters["Quantile"],
                maxfun      = self._parameters["MaximumNumberOfIterations"],
                toler       = self._parameters["CostDecrementTolerance"],
                y           = Y,
            )
        else:
            raise ValueError("Error in minimizer name: %s is unkown"%self._parameters["Minimizer"])
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = Minimum
        #
        self.StoredVariables["Analysis"].store( Xa )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("OMA") or \
                self._toStore("SimulatedObservationAtOptimum"):
            HXa = Hm(Xa).reshape((-1, 1))
        if self._toStore("Innovation") or \
                self._toStore("OMB") or \
                self._toStore("SimulatedObservationAtBackground"):
            HXb = Hm(Xb).reshape((-1, 1))
            Innovation = Y - HXb
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( Innovation )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( Innovation )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( Y - HXa )
        if self._toStore("SimulatedObservationAtBackground"):
            self.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
