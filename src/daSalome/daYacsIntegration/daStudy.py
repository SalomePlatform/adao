#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2010-2013 EDF R&D
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

from daCore.AssimilationStudy import AssimilationStudy
from daCore import Logging
import logging

class daError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class daStudy:

  def __init__(self, name, algorithm, debug):

    self.ADD = AssimilationStudy(name)
    self.ADD.setControls()
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

  #--------------------------------------

  def setInputVariable(self, name, size):
    self.InputVariables[name] = size
    self.InputVariablesOrder.append(name)

  def setOutputVariable(self, name, size):
    self.OutputVariables[name] = size
    self.OutputVariablesOrder.append(name)

  #--------------------------------------

  def setAlgorithmParameters(self, parameters):
    self.algorithm_dict = parameters

  #--------------------------------------

  def initAlgorithm(self):
    self.ADD.setAlgorithm(choice=self.algorithm)
    if self.algorithm_dict != None:
      logging.debug("DASTUDY AlgorithmParameters: "+str(self.algorithm_dict))
      self.ADD.setAlgorithmParameters(asDico=self.algorithm_dict)

  #--------------------------------------

  def getAssimilationStudy(self):
    return self.ADD

  #--------------------------------------
  # Methods to initialize AssimilationStudy

  def setBackgroundType(self, Type):
    if Type == "Vector":
      self.BackgroundType = Type
    else:
      raise daError("[daStudy::setBackgroundType] Type is unkown : " + Type + ". Types are : Vector")

  def setBackgroundStored(self, Stored):
    if Stored:
      self.BackgroundStored = True
    else:
      self.BackgroundStored = False

  def setBackground(self, Background):
    try:
      self.BackgroundType
      self.BackgroundStored
    except AttributeError:
      raise daError("[daStudy::setBackground] Type or Storage is not defined !")
    self.Background = Background
    if self.BackgroundType == "Vector":
      self.ADD.setBackground(asVector = Background, toBeStored = self.BackgroundStored)

  def getBackground(self):
    return self.Background

  #--------------------------------------

  def setCheckingPointType(self, Type):
    if Type == "Vector":
      self.CheckingPointType = Type
    else:
      raise daError("[daStudy::setCheckingPointType] Type is unkown : " + Type + ". Types are : Vector")

  def setCheckingPointStored(self, Stored):
    if Stored:
      self.CheckingPointStored = True
    else:
      self.CheckingPointStored = False

  def setCheckingPoint(self, CheckingPoint):
    try:
      self.CheckingPointType
      self.CheckingPointStored
    except AttributeError:
      raise daError("[daStudy::setCheckingPoint] Type or Storage is not defined !")
    self.CheckingPoint = CheckingPoint
    if self.CheckingPointType == "Vector":
      self.ADD.setBackground(asVector = CheckingPoint, toBeStored = self.CheckingPointStored)

  #--------------------------------------

  def setBackgroundErrorStored(self, Stored):
    if Stored:
      self.BackgroundErrorStored = True
    else:
      self.BackgroundErrorStored = False

  def setBackgroundError(self, BackgroundError):
    try:
      self.BackgroundErrorStored
    except AttributeError:
      raise daError("[daStudy::setBackgroundError] Storage is not defined !")
    self.ADD.setBackgroundError(asCovariance = BackgroundError, toBeStored = self.BackgroundErrorStored)

  #--------------------------------------

  def setControlInputType(self, Type):
    if Type == "Vector" or Type == "VectorSerie":
      self.ControlInputType = Type
    else:
      raise daError("[daStudy::setControlInputType] Type is unkown : " + Type + ". Types are : Vector, VectorSerie")

  def setControlInputStored(self, Stored):
    if Stored:
      self.ControlInputStored = True
    else:
      self.ControlInputStored = False

  def setControlInput(self, ControlInput):
    try:
      self.ControlInputType
      self.ControlInputStored
    except AttributeError:
      raise daError("[daStudy::setControlInput] Type or Storage is not defined !")
    if self.ControlInputType == "Vector":
      self.ADD.setControlInput(asVector = ControlInput, toBeStored = self.ControlInputStored)
    if self.ControlInputType == "VectorSerie":
      self.ADD.setControlInput(asPersistentVector = ControlInput, toBeStored = self.ControlInputStored)

  #--------------------------------------

  def setObservationType(self, Type):
    if Type == "Vector" or Type == "VectorSerie":
      self.ObservationType = Type
    else:
      raise daError("[daStudy::setObservationType] Type is unkown : " + Type + ". Types are : Vector, VectorSerie")

  def setObservationStored(self, Stored):
    if Stored:
      self.ObservationStored = True
    else:
      self.ObservationStored = False

  def setObservation(self, Observation):
    try:
      self.ObservationType
      self.ObservationStored
    except AttributeError:
      raise daError("[daStudy::setObservation] Type or Storage is not defined !")
    if self.ObservationType == "Vector":
      self.ADD.setObservation(asVector = Observation, toBeStored = self.ObservationStored)
    if self.ObservationType == "VectorSerie":
      self.ADD.setObservation(asPersistentVector = Observation, toBeStored = self.ObservationStored)

  #--------------------------------------

  def setObservationErrorStored(self, Stored):
    if Stored:
      self.ObservationErrorStored = True
    else:
      self.ObservationErrorStored = False

  def setObservationError(self, ObservationError):
    try:
      self.ObservationErrorStored
    except AttributeError:
      raise daError("[daStudy::setObservationError] Storage is not defined !")
    self.ADD.setObservationError(asCovariance = ObservationError, toBeStored = self.ObservationErrorStored)

  #--------------------------------------

  def getObservationOperatorType(self, Name):
    rtn = None
    try:
      rtn = self.ObservationOperatorType[Name]
    except:
      pass
    return rtn

  def setObservationOperatorType(self, Name, Type):
    if Type == "Matrix":
      self.ObservationOperatorType[Name] = Type
    elif Type == "Function":
      self.ObservationOperatorType[Name] = Type
    else:
      raise daError("[daStudy::setObservationOperatorType] Type is unkown : " + Type + ". Types are : Matrix, Function")

  def setObservationOperator(self, Name, ObservationOperator):
    try:
      self.ObservationOperatorType[Name]
    except AttributeError:
      raise daError("[daStudy::setObservationOperator] Type is not defined !")
    if self.ObservationOperatorType[Name] == "Matrix":
      self.ADD.setObservationOperator(asMatrix = ObservationOperator)
    elif self.ObservationOperatorType[Name] == "Function":
      self.FunctionObservationOperator[Name] = ObservationOperator

  #--------------------------------------

  def setEvolutionErrorStored(self, Stored):
    if Stored:
      self.EvolutionErrorStored = True
    else:
      self.EvolutionErrorStored = False

  def setEvolutionError(self, EvolutionError):
    try:
      self.EvolutionErrorStored
    except AttributeError:
      raise daError("[daStudy::setEvolutionError] Storage is not defined !")
    self.ADD.setEvolutionError(asCovariance = EvolutionError, toBeStored = self.EvolutionErrorStored)

  #--------------------------------------

  def getEvolutionModelType(self, Name):
    rtn = None
    try:
      rtn = self.EvolutionModelType[Name]
    except:
      pass
    return rtn

  def setEvolutionModelType(self, Name, Type):
    if Type == "Matrix":
      self.EvolutionModelType[Name] = Type
    elif Type == "Function":
      self.EvolutionModelType[Name] = Type
    else:
      raise daError("[daStudy::setEvolutionModelType] Type is unkown : " + Type + ". Types are : Matrix, Function")

  def setEvolutionModel(self, Name, EvolutionModel):
    try:
      self.EvolutionModelType[Name]
    except AttributeError:
      raise daError("[daStudy::setEvolutionModel] Type is not defined !")
    if self.EvolutionModelType[Name] == "Matrix":
      self.ADD.setEvolutionModel(asMatrix = EvolutionModel)
    elif self.EvolutionModelType[Name] == "Function":
      self.FunctionEvolutionModel[Name] = EvolutionModel

  #--------------------------------------

  def addObserver(self, name, scheduler, info, number):
    self.observers_dict[name] = {}
    self.observers_dict[name]["scheduler"] = scheduler
    self.observers_dict[name]["info"] = info
    self.observers_dict[name]["number"] = number

  def getObservers(self):
    return self.observers_dict
