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

  def setInputVariable(self, name, size):
    self.InputVariables[name] = size
    self.InputVariablesOrder.append(name)

  def setOutputVariable(self, name, size):
    self.OutputVariables[name] = size
    self.OutputVariablesOrder.append(name)

  def setAlgorithmParameters(self, parameters):
    self.algorithm_dict = parameters

  def initAlgorithm(self):

    self.ADD.setAlgorithm(choice=self.algorithm)
    if self.algorithm_dict != None:
      self.ADD.setAlgorithmParameters(asDico=self.algorithm_dict)

  def getAssimilationStudy(self):

    return self.ADD

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

  def setBackgroundError(self, BackgroundError):

    self.ADD.setBackgroundError(asCovariance = BackgroundError)

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

  def setObservationError(self, ObservationError):
    self.ADD.setObservationError(asCovariance = ObservationError)


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
      raise daError("[daStudy::setObservationOperatorType] Type is unkown : " + Type + " Types are : Matrix")

  def setObservationOperator(self, Name, ObservationOperator):
    try:
      self.ObservationOperatorType[Name]
    except AttributeError:
      raise daError("[daStudy::setObservationOperator] Type is not defined !")

    if self.ObservationOperatorType[Name] == "Matrix":
      self.ADD.setObservationOperator(asMatrix = ObservationOperator)
    elif self.ObservationOperatorType[Name] == "Function":
      self.FunctionObservationOperator[Name] = ObservationOperator

  def addObserver(self, name, scheduler, info):
    observers_dict[name] = {}
    observers_dict[name]["scheduler"] = scheduler
    observers_dict[name]["info"] = info

  def getObservers(self):
    return self.observers_dict
