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
    self.EvolutionModelType = {}
    self.FunctionObservationOperator = {}

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
      logging.debug("ADD.setAlgorithm : "+str(self.algorithm_dict))
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
      raise daError("[daStudy::setBackgroundType] Type is unkown : " + Type + " Types are : Vector")

  def setBackground(self, Background):
    try:
      self.BackgroundType
    except AttributeError:
      raise daError("[daStudy::setBackground] Type is not defined !")
    self.Background = Background
    if self.BackgroundType == "Vector":
      self.ADD.setBackground(asVector = Background)

  def getBackground(self):
    return self.Background

  #--------------------------------------

  def setCheckingPointType(self, Type):
    if Type == "Vector":
      self.CheckingPointType = Type
    else:
      raise daError("[daStudy::setCheckingPointType] Type is unkown : " + Type + " Types are : Vector")

  def setCheckingPoint(self, CheckingPoint):
    try:
      self.CheckingPointType
    except AttributeError:
      raise daError("[daStudy::setCheckingPoint] Type is not defined !")
    self.CheckingPoint = CheckingPoint
    if self.CheckingPointType == "Vector":
      self.ADD.setBackground(asVector = CheckingPoint)

  #--------------------------------------

  def setBackgroundError(self, BackgroundError):
    self.ADD.setBackgroundError(asCovariance = BackgroundError)

  #--------------------------------------

  def setObservationType(self, Type):
    if Type == "Vector":
      self.ObservationType = Type
    else:
      raise daError("[daStudy::setObservationType] Type is unkown : " + Type + " Types are : Vector")

  def setObservation(self, Observation):
    try:
      self.ObservationType
    except AttributeError:
      raise daError("[daStudy::setObservation] Type is not defined !")
    if self.ObservationType == "Vector":
      self.ADD.setObservation(asVector = Observation)

  #--------------------------------------

  def setObservationError(self, ObservationError):
    self.ADD.setObservationError(asCovariance = ObservationError)

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
      raise daError("[daStudy::setObservationOperatorType] Type is unkown : " + Type + " Types are : Matrix, Function")

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
      raise daError("[daStudy::setEvolutionModelType] Type is unkown : " + Type + " Types are : Matrix, Function")

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
