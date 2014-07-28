#-*- coding: utf-8 -*-
# Copyright (C) 2010-2014 EDF R&D
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
             "CheckingPoint", "ControlInput",
             ]

AssimType = {}
AssimType["Background"]          = ["Vector", "VectorSerie"]
AssimType["BackgroundError"]     = ["Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"]
AssimType["Observation"]         = ["Vector", "VectorSerie"]
AssimType["ObservationError"]    = ["Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"]
AssimType["ObservationOperator"] = ["Matrix", "Function"]
AssimType["EvolutionModel"]      = ["Matrix", "Function"]
AssimType["EvolutionError"]      = ["Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"]
AssimType["AlgorithmParameters"] = ["Dict"]
AssimType["UserDataInit"]        = ["Dict"]
AssimType["CheckingPoint"]       = ["Vector"]
AssimType["ControlInput"]        = ["Vector", "VectorSerie"]

FromNumpyList = {}
FromNumpyList["Vector"]               = ["String", "Script"]
FromNumpyList["VectorSerie"]          = ["String", "Script"]
FromNumpyList["Matrix"]               = ["String", "Script"]
FromNumpyList["ScalarSparseMatrix"]   = ["String", "Script"]
FromNumpyList["DiagonalSparseMatrix"] = ["String", "Script"]
FromNumpyList["Function"]             = ["ScriptWithOneFunction", "ScriptWithFunctions", "ScriptWithSwitch", "FunctionDict"]
FromNumpyList["Dict"]                 = ["String", "Script"]

# -- Infos from daAlgorithms --
AssimAlgos = [
    "3DVAR",
    "Blue",
    "ExtendedBlue",
    "EnsembleBlue",
    "KalmanFilter",
    "ExtendedKalmanFilter",
    "UnscentedKalmanFilter",
    "LinearLeastSquares",
    "NonLinearLeastSquares",
    "QuantileRegression",
    "ParticleSwarmOptimization",
    ]
CheckAlgos = [
    "FunctionTest",
    "LinearityTest",
    "GradientTest",
    "AdjointTest",
    "ObserverTest",
    "TangentTest",
    "SamplingTest",
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
AlgoDataRequirements["ExtendedBlue"] = [
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
    ]
AlgoDataRequirements["ExtendedKalmanFilter"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["UnscentedKalmanFilter"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
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

AlgoDataRequirements["FunctionTest"] = [
    "CheckingPoint",
    "ObservationOperator",
    ]
AlgoDataRequirements["LinearityTest"] = [
    "CheckingPoint",
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
AlgoDataRequirements["ObserverTest"] = [
    "Observers",
    ]
AlgoDataRequirements["TangentTest"] = [
    "CheckingPoint",
    "ObservationOperator",
    ]
AlgoDataRequirements["SamplingTest"] = [
    "CheckingPoint", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]

AlgoType = {}
AlgoType["3DVAR"] = "Optim"
AlgoType["Blue"] = "Optim"
AlgoType["ExtendedBlue"] = "Optim"
AlgoType["EnsembleBlue"] = "Optim"
AlgoType["KalmanFilter"] = "Optim"
AlgoType["ExtendedKalmanFilter"] = "Optim"
AlgoType["UnscentedKalmanFilter"] = "Optim"
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
DataTypeDict["Vector"]               = ["String", "Script"]
DataTypeDict["VectorSerie"]          = ["String", "Script"]
DataTypeDict["Matrix"]               = ["String", "Script"]
DataTypeDict["ScalarSparseMatrix"]   = ["String", "Script"]
DataTypeDict["DiagonalSparseMatrix"] = ["String", "Script"]
DataTypeDict["Function"]             = ["ScriptWithOneFunction", "ScriptWithFunctions", "ScriptWithSwitch", "FunctionDict"]
DataTypeDict["Dict"]                 = ["String", "Script"]

DataTypeDefaultDict = {}
DataTypeDefaultDict["Vector"]               = "Script"
DataTypeDefaultDict["VectorSerie"]          = "Script"
DataTypeDefaultDict["Matrix"]               = "Script"
DataTypeDefaultDict["ScalarSparseMatrix"]   = "String"
DataTypeDefaultDict["DiagonalSparseMatrix"] = "String"
DataTypeDefaultDict["Function"]             = "ScriptWithOneFunction"
DataTypeDefaultDict["Dict"]                 = "Script"

# Assimilation data input
AssimDataDict = {}
AssimDataDict["Background"]          = ["Vector", "VectorSerie"]
AssimDataDict["BackgroundError"]     = ["Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"]
AssimDataDict["Observation"]         = ["Vector", "VectorSerie"]
AssimDataDict["ObservationError"]    = ["Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"]
AssimDataDict["ObservationOperator"] = ["Matrix", "Function"]
AssimDataDict["EvolutionModel"]      = ["Matrix", "Function"]
AssimDataDict["EvolutionError"]      = ["Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"]
AssimDataDict["AlgorithmParameters"] = ["Dict"]
AssimDataDict["UserDataInit"]        = ["Dict"]
AssimDataDict["CheckingPoint"]       = ["Vector"]
AssimDataDict["ControlInput"]        = ["Vector", "VectorSerie"]

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
AssimDataDefaultDict["ControlInput"]        = "Vector"

StoredAssimData = ["Vector", "VectorSerie", "Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"]

# Assimilation optional nodes
OptDict = {}
OptDict["UserPostAnalysis"]   = ["String", "Script", "Template"]
OptDefaultDict = {}
OptDefaultDict["UserPostAnalysis"]   = "Template"

# Observers
ObserversList = [
    "Analysis",
    "CurrentState",
    "Innovation",
    "ObservedState",
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
