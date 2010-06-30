#-*-coding:iso-8859-1-*-
#  Copyright (C) 2010 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public
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
# --
# Author : André RIBES (EDF R&D)
# --


# -- Infos pour le parser --

AnalysisData = {}
AnalysisFromList = ["String", "File"]

# -- Infos from daCore --
AssimData = ["Background", "BackgroundError",
             "Observation", "ObservationError", "ObservationOperator", "ObservationOperatorAppliedToX",
             "EvolutionModel", "EvolutionError"]

AssimType = {}
AssimType["Background"] = ["Vector"]
AssimType["BackgroundError"] = ["Matrix"]
AssimType["Observation"] = ["Vector"]
AssimType["ObservationError"] = ["Matrix"]
AssimType["ObservationOperator"] = ["Matrix", "Function"]
AssimType["ObservationOperatorAppliedToX"] = ["List"]

FromNumpyList = {}
FromNumpyList["Vector"] = ["String", "Script"]
FromNumpyList["Matrix"] = ["String", "Script"]
FromNumpyList["Function"] = ["Dict"]
FromNumpyList["List"] = ["List"]
FromNumpyList["Dict"] = ["Script"]

# -- Infos from daAlgorithms --
AssimAlgos = ["Blue", "EnsembleBlue", "Kalman", "LinearLeastSquares", "3DVAR"]

AlgoDataRequirements = {}
AlgoDataRequirements["Blue"] = ["Background", "BackgroundError",
                                "Observation", "ObservationOperator", "ObservationError"]

AlgoDataRequirements["3DVAR"] = ["Background", "BackgroundError",
                                 "Observation", "ObservationOperator", "ObservationError"]
AlgoType = {}
#AlgoType["Blue"] = "Direct"
AlgoType["Blue"] = "Optim"
AlgoType["3DVAR"] = "Optim"
