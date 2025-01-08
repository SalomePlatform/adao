#-*-coding:utf-8-*-
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

from daCore.Aidsm import Aidsm
#from daCore import Logging
import logging

class daError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class daStudy:

  def __init__(self, name, algorithm, debug):

    self.ADD = Aidsm(name)
    self.algorithm = algorithm
    self.algorithm_dict = None
    self.Background = None
    self.CheckingPoint = None
    self.InputVariables = {}
    self.OutputVariables = {}
    self.InputVariablesOrder = []
    self.OutputVariablesOrder = []
    self.observers_dict = {}

    self.debug = debug
    if self.debug:
      logging.getLogger().setLevel(logging.DEBUG)
    else:
      logging.getLogger().setLevel(logging.WARNING)

    # Observation Management
    self.ObservationOperatorType = {}
    self.FunctionObservationOperator = {}

    # Evolution Management
    self.EvolutionModelType = {}
    self.FunctionEvolutionModel = {}

  def setYIInputVariable(self, name, size):
    self.InputVariables[name] = size
    self.InputVariablesOrder.append(name)

  def setYIOutputVariable(self, name, size):
    self.OutputVariables[name] = size
    self.OutputVariablesOrder.append(name)

  def setYIAlgorithmParameters(self, parameters):
    self.algorithm_dict = parameters

  def initYIAlgorithm(self):
    self.ADD.setAlgorithmParameters(Algorithm=self.algorithm)
    if self.algorithm_dict != None:
      logging.debug("DASTUDY AlgorithmParameters: "+str(self.algorithm_dict))
      self.ADD.updateAlgorithmParameters(Parameters=self.algorithm_dict)

  def YI_prepare_to_pickle(self):
    return self.ADD.prepare_to_pickle()

  #--------------------------------------

  def __dir__(self):
    return ['getResults', '__doc__', '__init__', '__module__']

  def getResults(self):
    "Unique méthode à ne pas inclure YI"
    return self.ADD

  #--------------------------------------
  # Methods to initialize assimilation study

  def setYIBackgroundType(self, Type):
    if Type == "Vector":
      self.BackgroundType = Type
    else:
      raise daError("[daStudy::setYIBackgroundType] The following type is unkown : %s. Authorized types are : Vector"%(Type,))

  def setYIBackgroundStored(self, Stored):
    if Stored:
      self.BackgroundStored = True
    else:
      self.BackgroundStored = False

  def setYIBackground(self, Background):
    try:
      self.BackgroundType
      self.BackgroundStored
    except AttributeError:
      raise daError("[daStudy::setYIBackground] Type or Storage is not defined !")
    self.Background = Background
    if self.BackgroundType == "Vector":
      self.ADD.setBackground(Vector = Background, Stored = self.BackgroundStored)

  def getYIBackground(self):
    return self.Background

  #--------------------------------------

  def setYICheckingPointType(self, Type):
    if Type == "Vector":
      self.CheckingPointType = Type
    else:
      raise daError("[daStudy::setYICheckingPointType] The following type is unkown : %s. Authorized types are : Vector"%(Type,))

  def setYICheckingPointStored(self, Stored):
    if Stored:
      self.CheckingPointStored = True
    else:
      self.CheckingPointStored = False

  def setYICheckingPoint(self, CheckingPoint):
    try:
      self.CheckingPointType
      self.CheckingPointStored
    except AttributeError:
      raise daError("[daStudy::setYICheckingPoint] Type or Storage is not defined !")
    self.CheckingPoint = CheckingPoint
    if self.CheckingPointType == "Vector":
      self.ADD.setBackground(Vector = CheckingPoint, Stored = self.CheckingPointStored)

  #--------------------------------------

  def setYIBackgroundErrorType(self, Type):
    if Type in ("Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"):
      self.BackgroundErrorType = Type
    else:
      raise daError("[daStudy::setYIBackgroundErrorType] The following type is unkown : %s. Authorized types are : Matrix, ScalarSparseMatrix, DiagonalSparseMatrix"%(Type,))

  def setYIBackgroundErrorStored(self, Stored):
    if Stored:
      self.BackgroundErrorStored = True
    else:
      self.BackgroundErrorStored = False

  def setYIBackgroundError(self, BackgroundError):
    try:
      self.BackgroundErrorType
      self.BackgroundErrorStored
    except AttributeError:
      raise daError("[daStudy::setYIBackgroundError] Type or Storage is not defined !")
    if self.BackgroundErrorType == "Matrix":
      self.ADD.setBackgroundError(Matrix = BackgroundError, Stored = self.BackgroundErrorStored)
    if self.BackgroundErrorType == "ScalarSparseMatrix":
      self.ADD.setBackgroundError(ScalarSparseMatrix = BackgroundError, Stored = self.BackgroundErrorStored)
    if self.BackgroundErrorType == "DiagonalSparseMatrix":
      self.ADD.setBackgroundError(DiagonalSparseMatrix = BackgroundError, Stored = self.BackgroundErrorStored)

  #--------------------------------------

  def setYIControlInputType(self, Type):
    if Type in ("Vector", "VectorSerie"):
      self.ControlInputType = Type
    else:
      raise daError("[daStudy::setYIControlInputType] The following type is unkown : %s. Authorized types are : Vector, VectorSerie"%(Type,))

  def setYIControlInputStored(self, Stored):
    if Stored:
      self.ControlInputStored = True
    else:
      self.ControlInputStored = False

  def setYIControlInput(self, ControlInput):
    try:
      self.ControlInputType
      self.ControlInputStored
    except AttributeError:
      raise daError("[daStudy::setYIControlInput] Type or Storage is not defined !")
    if self.ControlInputType == "Vector":
      self.ADD.setControlInput(Vector = ControlInput, Stored = self.ControlInputStored)
    if self.ControlInputType == "VectorSerie":
      self.ADD.setControlInput(VectorSerie = ControlInput, Stored = self.ControlInputStored)

  #--------------------------------------

  def setYIObservationType(self, Type):
    if Type in ("Vector", "VectorSerie"):
      self.ObservationType = Type
    else:
      raise daError("[daStudy::setYIObservationType] The following type is unkown : %s. Authorized types are : Vector, VectorSerie"%(Type,))

  def setYIObservationStored(self, Stored):
    if Stored:
      self.ObservationStored = True
    else:
      self.ObservationStored = False

  def setYIObservation(self, Observation):
    try:
      self.ObservationType
      self.ObservationStored
    except AttributeError:
      raise daError("[daStudy::setYIObservation] Type or Storage is not defined !")
    if self.ObservationType == "Vector":
      self.ADD.setObservation(Vector = Observation, Stored = self.ObservationStored)
    if self.ObservationType == "VectorSerie":
      self.ADD.setObservation(VectorSerie = Observation, Stored = self.ObservationStored)

  #--------------------------------------

  def setYIObservationErrorType(self, Type):
    if Type in ("Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"):
      self.ObservationErrorType = Type
    else:
      raise daError("[daStudy::setYIObservationErrorType] The following type is unkown : %s. Authorized types are : Matrix, ScalarSparseMatrix, DiagonalSparseMatrix"%(Type,))

  def setYIObservationErrorStored(self, Stored):
    if Stored:
      self.ObservationErrorStored = True
    else:
      self.ObservationErrorStored = False

  def setYIObservationError(self, ObservationError):
    try:
      self.ObservationErrorType
      self.ObservationErrorStored
    except AttributeError:
      raise daError("[daStudy::setYIObservationError] Type or Storage is not defined !")
    if self.ObservationErrorType == "Matrix":
      self.ADD.setObservationError(Matrix = ObservationError, Stored = self.ObservationErrorStored)
    if self.ObservationErrorType == "ScalarSparseMatrix":
      self.ADD.setObservationError(ScalarSparseMatrix = ObservationError, Stored = self.ObservationErrorStored)
    if self.ObservationErrorType == "DiagonalSparseMatrix":
      self.ADD.setObservationError(DiagonalSparseMatrix = ObservationError, Stored = self.ObservationErrorStored)

  #--------------------------------------

  def getYIObservationOperatorType(self, Name):
    rtn = None
    try:
      rtn = self.ObservationOperatorType[Name]
    except:
      pass
    return rtn

  def setYIObservationOperatorType(self, Name, Type):
    if Type in ("Matrix", "Function"):
      self.ObservationOperatorType[Name] = Type
    else:
      raise daError("[daStudy::setYIObservationOperatorType] The following type is unkown : %s. Authorized types are : Matrix, Function"%(Type,))

  def setYIObservationOperator(self, Name, ObservationOperator):
    try:
      self.ObservationOperatorType[Name]
    except AttributeError:
      raise daError("[daStudy::setYIObservationOperator] Type is not defined !")
    if self.ObservationOperatorType[Name] == "Matrix":
      self.ADD.setObservationOperator(Matrix = ObservationOperator)
    elif self.ObservationOperatorType[Name] == "Function":
      self.FunctionObservationOperator[Name] = ObservationOperator

  #--------------------------------------

  def setYIEvolutionErrorType(self, Type):
    if Type in ("Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix"):
      self.EvolutionErrorType = Type
    else:
      raise daError("[daStudy::setYIEvolutionErrorType] The following type is unkown : %s. Authorized types are : Matrix, ScalarSparseMatrix, DiagonalSparseMatrix"%(Type,))

  def setYIEvolutionErrorStored(self, Stored):
    if Stored:
      self.EvolutionErrorStored = True
    else:
      self.EvolutionErrorStored = False

  def setYIEvolutionError(self, EvolutionError):
    try:
      self.EvolutionErrorType
      self.EvolutionErrorStored
    except AttributeError:
      raise daError("[daStudy::setYIEvolutionError] Type or Storage is not defined !")
    if self.EvolutionErrorType == "Matrix":
      self.ADD.setEvolutionError(Matrix = EvolutionError, Stored = self.EvolutionErrorStored)
    if self.EvolutionErrorType == "ScalarSparseMatrix":
      self.ADD.setEvolutionError(ScalarSparseMatrix = EvolutionError, Stored = self.EvolutionErrorStored)
    if self.EvolutionErrorType == "DiagonalSparseMatrix":
      self.ADD.setEvolutionError(DiagonalSparseMatrix = EvolutionError, Stored = self.EvolutionErrorStored)

  #--------------------------------------

  def getYIEvolutionModelType(self, Name):
    rtn = None
    try:
      rtn = self.EvolutionModelType[Name]
    except:
      pass
    return rtn

  def setYIEvolutionModelType(self, Name, Type):
    if Type in ("Matrix", "Function"):
      self.EvolutionModelType[Name] = Type
    else:
      raise daError("[daStudy::setYIEvolutionModelType] The following type is unkown : %s. Authorized types are : Matrix, Function"%(Type,))

  def setYIEvolutionModel(self, Name, EvolutionModel):
    try:
      self.EvolutionModelType[Name]
    except AttributeError:
      raise daError("[daStudy::setYIEvolutionModel] Type is not defined !")
    if self.EvolutionModelType[Name] == "Matrix":
      self.ADD.setEvolutionModel(Matrix = EvolutionModel)
    elif self.EvolutionModelType[Name] == "Function":
      self.FunctionEvolutionModel[Name] = EvolutionModel

  #--------------------------------------

  def addYIObserver(self, name, scheduler, info, number):
    self.observers_dict[name] = {}
    self.observers_dict[name]["scheduler"] = scheduler
    self.observers_dict[name]["info"] = info
    self.observers_dict[name]["number"] = number

