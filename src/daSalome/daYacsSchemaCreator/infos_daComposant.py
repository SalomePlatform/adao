#-*- coding: utf-8 -*-
# Copyright (C) 2010-2011 EDF R&D
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
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D


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
AssimType["ObservationOperator"] = ["Matrix", "Function"]
AssimType["AlgorithmParameters"] = ["Dict"]
AssimType["UserDataInit"] = ["Dict"]
#AssimType["ObservationOperatorAppliedToX"] = ["List"]

FromNumpyList = {}
FromNumpyList["Vector"] = ["String", "Script"]
FromNumpyList["Matrix"] = ["String", "Script"]
FromNumpyList["Function"] = ["FunctionDict"]
FromNumpyList["Dict"] = ["Script"]

# -- Infos from daAlgorithms --
AssimAlgos = ["Blue", "EnsembleBlue", "KalmanFilter", "LinearLeastSquares", "3DVAR"]

AlgoDataRequirements = {}
AlgoDataRequirements["Blue"] = ["Background", "BackgroundError",
                                "Observation", "ObservationOperator", "ObservationError"]

AlgoDataRequirements["3DVAR"] = ["Background", "BackgroundError",
                                 "Observation", "ObservationOperator", "ObservationError"]
AlgoType = {}
AlgoType["Blue"] = "Optim"
AlgoType["3DVAR"] = "Optim"
AlgoType["EnsembleBlue"] = "Optim"
AlgoType["KalmanFilter"] = "Optim"
AlgoType["LinearLeastSquares"] = "Optim"
#AlgoType["Blue"] = "Direct"


# Variables qui sont partagés avec le générateur de
# catalogue Eficas

# Basic data types
BasicDataInputs = ["String", "Script", "FunctionDict"]

# Data input dict
DataTypeDict = {}
DataTypeDict["Vector"]   = ["String", "Script"]
DataTypeDict["Matrix"]   = ["String", "Script"]
DataTypeDict["Function"] = ["FunctionDict"]
DataTypeDict["Dict"]     = ["Script"]

DataTypeDefaultDict = {}
DataTypeDefaultDict["Vector"]   = "Script"
DataTypeDefaultDict["Matrix"]   = "Script"
DataTypeDefaultDict["Function"] = "FunctionDict"
DataTypeDefaultDict["Dict"]     = "Script"

# Assimilation data input
AssimDataDict = {}
AssimDataDict["Background"] = ["Vector"]
AssimDataDict["BackgroundError"] = ["Matrix"]
AssimDataDict["Observation"] = ["Vector"]
AssimDataDict["ObservationError"] = ["Matrix"]
AssimDataDict["ObservationOperator"] = ["Matrix", "Function"]
AssimDataDict["AlgorithmParameters"] = ["Dict"]
AssimDataDict["UserDataInit"] = ["Dict"]

AssimDataDefaultDict = {}
AssimDataDefaultDict["Background"]          = "Vector"
AssimDataDefaultDict["BackgroundError"]     = "Matrix"
AssimDataDefaultDict["Observation"]         = "Vector"
AssimDataDefaultDict["ObservationError"]    = "Matrix"
AssimDataDefaultDict["ObservationOperator"] = "Function"
AssimDataDefaultDict["AlgorithmParameters"] = "Dict"
AssimDataDefaultDict["UserDataInit"]        = "Dict"

# Assimilation optional nodes
OptDict = {}
OptDict["UserPostAnalysis"]   = ["String", "Script"]
OptDefaultDict = {}
OptDefaultDict["UserPostAnalysis"]   = "Script"


# Observers
ObserversList = ["CostFunctionJ","CostFunctionJb","CostFunctionJo","GradientOfCostFunctionJ","GradientOfCostFunctionJb","GradientOfCostFunctionJo","CurrentState","Analysis","Innovation","SigmaObs2","SigmaBck2","OMA","OMB","BMA","CovarianceAPosteriori"]
