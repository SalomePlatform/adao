#-*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
#
# This file is part of SALOME ADAO module
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
AssimData = [
    "Background",
    "BackgroundError",
    "Observation",
    "ObservationError",
    "ObservationOperator",
    "EvolutionModel",
    "EvolutionError",
    "AlgorithmParameters",
    "CheckingPoint",
    "ControlInput",
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
FromNumpyList["Vector"]               = ["String", "Script", "DataFile"]
FromNumpyList["VectorSerie"]          = ["String", "Script", "DataFile"]
FromNumpyList["Matrix"]               = ["String", "Script"]
FromNumpyList["ScalarSparseMatrix"]   = ["String", "Script"]
FromNumpyList["DiagonalSparseMatrix"] = ["String", "Script"]
FromNumpyList["Function"]             = ["ScriptWithOneFunction", "ScriptWithFunctions", "ScriptWithSwitch", "FunctionDict"]
FromNumpyList["Dict"]                 = ["String", "Script"]

# -- Infos from daAlgorithms --
AssimAlgos = [
    "3DVAR",
    "4DVAR",
    "Blue",
    "DerivativeFreeOptimization",
    "DifferentialEvolution",
    "EnsembleBlue",
    "EnsembleKalmanFilter",
    "ExtendedBlue",
    "ExtendedKalmanFilter",
    "KalmanFilter",
    "LinearLeastSquares",
    "NonLinearLeastSquares",
    "ParticleSwarmOptimization",
    "QuantileRegression",
    "TabuSearch",
    "UnscentedKalmanFilter",
    ]
OptimizationAlgos = [
    "Blue",
    "3DVAR",
    "DerivativeFreeOptimization",
    "DifferentialEvolution",
    "KalmanFilter",
    "LinearLeastSquares",
    "NonLinearLeastSquares",
    "ParticleSwarmOptimization",
    "TabuSearch",
    ]
ReductionAlgos = [
    "EnsembleBlue",
    "EnsembleKalmanFilter",
    "UnscentedKalmanFilter",
    ]
CheckAlgos = [
    "FunctionTest",
    "LinearityTest",
    "GradientTest",
    "AdjointTest",
    "TangentTest",
    "LocalSensitivityTest",
    "ObservationSimulationComparisonTest",
    "SamplingTest",
    "ParallelFunctionTest",
    "ControledFunctionTest",
    "InputValuesTest",
    "ObserverTest",
    ]
TaskAlgos = []

AlgoDataRequirements = {}
AlgoDataRequirements["3DVAR"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["4DVAR"] = [
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
    "ObservationOperator",
    ]
AlgoDataRequirements["ExtendedKalmanFilter"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["EnsembleKalmanFilter"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["UnscentedKalmanFilter"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["QuantileRegression"] = [
    "Background",
    "Observation",
    "ObservationOperator",
    ]
AlgoDataRequirements["DerivativeFreeOptimization"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["ParticleSwarmOptimization"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["DifferentialEvolution"] = [
    "Background", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["TabuSearch"] = [
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
AlgoDataRequirements["TangentTest"] = [
    "CheckingPoint",
    "ObservationOperator",
    ]
AlgoDataRequirements["LocalSensitivityTest"] = [
    "CheckingPoint",
    "Observation",
    "ObservationOperator",
    ]
AlgoDataRequirements["ObservationSimulationComparisonTest"] = [
    "CheckingPoint",
    "Observation",
    "ObservationOperator",
    ]
AlgoDataRequirements["SamplingTest"] = [
    "CheckingPoint", "BackgroundError",
    "Observation", "ObservationError",
    "ObservationOperator",
    ]
AlgoDataRequirements["ParallelFunctionTest"] = [
    "CheckingPoint",
    "ObservationOperator",
    ]
AlgoDataRequirements["ControledFunctionTest"] = [
    "CheckingPoint",
    "ObservationOperator",
    ]
AlgoDataRequirements["ObserverTest"] = [
    "Observers",
    ]
AlgoDataRequirements["InputValuesTest"] = [
    "CheckingPoint",
    ]

AlgoType = {}
AlgoType["3DVAR"] = "Optim"
AlgoType["4DVAR"] = "Optim"
AlgoType["Blue"] = "Optim"
AlgoType["ExtendedBlue"] = "Optim"
AlgoType["EnsembleBlue"] = "Optim"
AlgoType["KalmanFilter"] = "Optim"
AlgoType["ExtendedKalmanFilter"] = "Optim"
AlgoType["EnsembleKalmanFilter"] = "Optim"
AlgoType["UnscentedKalmanFilter"] = "Optim"
AlgoType["QuantileRegression"] = "Optim"
AlgoType["DerivativeFreeOptimization"] = "Optim"
AlgoType["ParticleSwarmOptimization"] = "Optim"
AlgoType["DifferentialEvolution"] = "Optim"
AlgoType["TabuSearch"] = "Optim"
AlgoType["LinearLeastSquares"] = "Optim"
AlgoType["NonLinearLeastSquares"] = "Optim"

# Variables qui sont partages avec le generateur de
# catalogue Eficas

# Basic data types
BasicDataInputs = ["String", "Script", "ScriptWithOneFunction", "ScriptWithFunctions", "ScriptWithSwitch", "FunctionDict"]

# Data input dict
DataTypeDict = {}
DataTypeDict["Vector"]               = ["String", "Script", "DataFile"]
DataTypeDict["VectorSerie"]          = ["String", "Script", "DataFile"]
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

DataSValueDefaultDict = {}
DataSValueDefaultDict["ScalarSparseMatrix"]   = "1."

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
AssimDataDefaultDict["BackgroundError"]     = "ScalarSparseMatrix"
AssimDataDefaultDict["Observation"]         = "Vector"
AssimDataDefaultDict["ObservationError"]    = "ScalarSparseMatrix"
AssimDataDefaultDict["ObservationOperator"] = "Function"
AssimDataDefaultDict["EvolutionModel"]      = "Function"
AssimDataDefaultDict["EvolutionError"]      = "ScalarSparseMatrix"
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
    "Innovation",
    "InnovationAtCurrentState",
    "CurrentState",
    "CurrentOptimum",
    "IndexOfOptimum",
    "SimulatedObservationAtBackground",
    "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum",
    "SimulatedObservationAtCurrentOptimum",
    "BMA",
    "OMA",
    "OMB",
    "CostFunctionJ",
    "CostFunctionJb",
    "CostFunctionJo",
    "GradientOfCostFunctionJ",
    "GradientOfCostFunctionJb",
    "GradientOfCostFunctionJo",
    "SigmaObs2",
    "SigmaBck2",
    "APosterioriCorrelations",
    "APosterioriCovariance",
    "APosterioriStandardDeviations",
    "APosterioriVariances",
    "Residu",
    ]

# Global regulation of separate container execution with priority on user:
#   0 for no separate execution container possibility
#   1 for separate execution container possibility
UseSeparateContainer = 1
