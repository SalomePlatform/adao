#-*- coding: utf-8 -*-
# Copyright (C) 2010-2012 EDF R&D
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
# Author: Andre Ribes, andre.ribes@edf.fr, EDF R&D


# -- Infos pour le parser --

AnalysisData = {}
AnalysisFromList = ["String", "Script"]

# -- Infos from daCore --
AssimData = ["Background", "BackgroundError",
             "Observation", "ObservationError",
             "ObservationOperator",
             "EvolutionModel", "EvolutionError",
             "AlgorithmParameters",
             "CheckingPoint",
             ]

AssimType = {}
AssimType["Background"]          = ["Vector"]
AssimType["BackgroundError"]     = ["Matrix"]
AssimType["Observation"]         = ["Vector", "VectorSerie"]
AssimType["ObservationError"]    = ["Matrix"]
AssimType["ObservationOperator"] = ["Matrix", "Function"]
AssimType["EvolutionModel"]      = ["Matrix", "Function"]
AssimType["EvolutionError"]      = ["Matrix"]
AssimType["AlgorithmParameters"] = ["Dict"]
AssimType["UserDataInit"]        = ["Dict"]
AssimType["CheckingPoint"]       = ["Vector"]

FromNumpyList = {}
FromNumpyList["Vector"]      = ["String", "Script"]
FromNumpyList["VectorSerie"] = ["String", "Script"]
FromNumpyList["Matrix"]      = ["String", "Script"]
FromNumpyList["Function"]    = ["ScriptWithOneFunction", "ScriptWithFunctions", "ScriptWithSwitch", "FunctionDict"]
FromNumpyList["Dict"]        = ["Script"]

# -- Infos from daAlgorithms --
AssimAlgos = [
    "3DVAR",
    "Blue",
    "EnsembleBlue",
    "KalmanFilter",
    "LinearLeastSquares",
    "NonLinearLeastSquares",
    "QuantileRegression",
    "ParticleSwarmOptimization",
    ]
CheckAlgos = [
    "GradientTest",
    "AdjointTest",
    ]

AlgoDataRequirements = {}
AlgoDataRequirements["3DVAR"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["Blue"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["EnsembleBlue"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["KalmanFilter"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "EvolutionModel", "EvolutionError",
    "ObservationOperator",
    ]
AlgoDataRequirements["LinearLeastSquares"] = [
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["NonLinearLeastSquares"] = [
    "Background",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["ParticleSwarmOptimization"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["QuantileRegression"] = [
    "Background",
    "Observation",
    "ObservationOperator",
    ]

AlgoDataRequirements["GradientTest"] = [
    "CheckingPoint",
    "ObservationOperator",
    ]
AlgoDataRequirements["AdjointTest"] = [
    "CheckingPoint",
    "ObservationOperator",
    ]

AlgoType = {}
AlgoType["3DVAR"] = "Optim"
AlgoType["Blue"] = "Optim"
AlgoType["EnsembleBlue"] = "Optim"
AlgoType["KalmanFilter"] = "Optim"
AlgoType["LinearLeastSquares"] = "Optim"
AlgoType["NonLinearLeastSquares"] = "Optim"
AlgoType["ParticleSwarmOptimization"] = "Optim"
AlgoType["QuantileRegression"] = "Optim"

# Variables qui sont partages avec le generateur de
# catalogue Eficas

# Basic data types
BasicDataInputs = ["String", "Script", "ScriptWithOneFunction", "ScriptWithFunctions", "ScriptWithSwitch", "FunctionDict"]

# Data input dict
DataTypeDict = {}
DataTypeDict["Vector"]      = ["String", "Script"]
DataTypeDict["VectorSerie"] = ["String", "Script"]
DataTypeDict["Matrix"]      = ["String", "Script"]
DataTypeDict["Function"]    = ["ScriptWithOneFunction", "ScriptWithFunctions", "ScriptWithSwitch", "FunctionDict"]
DataTypeDict["Dict"]        = ["Script"]

DataTypeDefaultDict = {}
DataTypeDefaultDict["Vector"]      = "Script"
DataTypeDefaultDict["VectorSerie"] = "Script"
DataTypeDefaultDict["Matrix"]      = "Script"
DataTypeDefaultDict["Function"]    = "ScriptWithOneFunction"
DataTypeDefaultDict["Dict"]        = "Script"

# Assimilation data input
AssimDataDict = {}
AssimDataDict["Background"]          = ["Vector"]
AssimDataDict["BackgroundError"]     = ["Matrix"]
AssimDataDict["Observation"]         = ["Vector", "VectorSerie"]
AssimDataDict["ObservationError"]    = ["Matrix"]
AssimDataDict["ObservationOperator"] = ["Matrix", "Function"]
AssimDataDict["EvolutionModel"]      = ["Matrix", "Function"]
AssimDataDict["EvolutionError"]      = ["Matrix"]
AssimDataDict["AlgorithmParameters"] = ["Dict"]
AssimDataDict["UserDataInit"]        = ["Dict"]
AssimDataDict["CheckingPoint"]       = ["Vector"]

AssimDataDefaultDict = {}
AssimDataDefaultDict["Background"]          = "Vector"
AssimDataDefaultDict["BackgroundError"]     = "Matrix"
AssimDataDefaultDict["Observation"]         = "Vector"
AssimDataDefaultDict["ObservationError"]    = "Matrix"
AssimDataDefaultDict["ObservationOperator"] = "Function"
AssimDataDefaultDict["EvolutionModel"]      = "Function"
AssimDataDefaultDict["EvolutionError"]      = "Matrix"
AssimDataDefaultDict["AlgorithmParameters"] = "Dict"
AssimDataDefaultDict["UserDataInit"]        = "Dict"
AssimDataDefaultDict["CheckingPoint"]       = "Vector"

StoredAssimData = ["Vector", "VectorSerie", "Matrix"]

# Assimilation optional nodes
OptDict = {}
OptDict["UserPostAnalysis"]   = ["String", "Script"]
OptDefaultDict = {}
OptDefaultDict["UserPostAnalysis"]   = "Script"

# Observers
ObserversList = [
    "Analysis",
    "CurrentState",
    "Innovation",
    "OMA",
    "OMB",
    "BMA",
    "CostFunctionJ",
    "CostFunctionJb",
    "CostFunctionJo",
    "GradientOfCostFunctionJ",
    "GradientOfCostFunctionJb",
    "GradientOfCostFunctionJo",
    "SigmaObs2",
    "SigmaBck2",
    "APosterioriCovariance",
    ]
