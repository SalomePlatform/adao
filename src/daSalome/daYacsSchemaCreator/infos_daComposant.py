#-*- coding: utf-8 -*-
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
AnalysisFromList = ["String", "Script"]

# -- Infos from daCore --
#AssimData = ["Background", "BackgroundError",
#             "Observation", "ObservationError", "ObservationOperator", "ObservationOperatorAppliedToX",
#             "EvolutionModel", "EvolutionError", "AlgorithmParameters"]

AssimData = ["Background", "BackgroundError",
             "Observation", "ObservationError", "ObservationOperator",
             "EvolutionModel", "EvolutionError", "AlgorithmParameters"]


AssimType = {}
AssimType["Background"] = ["Vector"]
AssimType["BackgroundError"] = ["Matrix"]
AssimType["Observation"] = ["Vector"]
AssimType["ObservationError"] = ["Matrix"]
AssimType["ObservationOperator"] = ["Matrix", "FunctionDict"]
AssimType["AlgorithmParameters"] = ["Dict"]
#AssimType["ObservationOperatorAppliedToX"] = ["List"]

FromNumpyList = {}
FromNumpyList["Vector"] = ["String", "Script"]
FromNumpyList["Matrix"] = ["String", "Script"]
FromNumpyList["Function"] = ["FunctionDict"]
FromNumpyList["Dict"] = ["Script"]

# -- Infos from daAlgorithms --
AssimAlgos = ["Blue", "EnsembleBlue", "Kalman", "LinearLeastSquares", "3DVAR"]

AlgoDataRequirements = {}
AlgoDataRequirements["Blue"] = ["Background", "BackgroundError",
                                "Observation", "ObservationOperator", "ObservationError"]

AlgoDataRequirements["3DVAR"] = ["Background", "BackgroundError",
                                 "Observation", "ObservationOperator", "ObservationError"]
AlgoType = {}
AlgoType["Blue"] = "Optim"
AlgoType["3DVAR"] = "Optim"
AlgoType["EnsembleBlue"] = "Optim"
AlgoType["Kalman"] = "Optim"
AlgoType["LinearLeastSquares"] = "Optim"
#AlgoType["Blue"] = "Direct"

# Basic data types
BasicDataInputs = ["String", "Script", "FunctionDict"]

# Data input dict
DataTypeDict = {}
DataTypeDict["Vector"]   = ["String", "Script"]
DataTypeDict["Matrix"]   = ["String", "Script"]
DataTypeDict["Function"] = ["FunctionDict"]
DataTypeDict["Dict"]     = ["Script"]

# Assimilation data input
AssimDataDict = {}
AssimDataDict["Background"] = ["Vector"]
AssimDataDict["BackgroundError"] = ["Matrix"]
AssimDataDict["Observation"] = ["Vector"]
AssimDataDict["ObservationError"] = ["Matrix"]
AssimDataDict["ObservationOperator"] = ["Matrix", "Function"]
AssimDataDict["AlgorithmParameters"] = ["Dict"]

# Assimilation optional nodes
OptDict = {}
OptDict["Analysis"]   = ["String", "Script"]
