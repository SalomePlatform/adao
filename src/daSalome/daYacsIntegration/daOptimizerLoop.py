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

import SALOMERuntime
import pilot
import pickle
import numpy
import threading

from daCore.AssimilationStudy import AssimilationStudy
from daYacsIntegration import daStudy

class OptimizerHooks:

  def __init__(self, optim_algo):
    self.optim_algo = optim_algo

    # Gestion du compteur
    self.sample_counter = 0
    self.counter_lock = threading.Lock()

  def create_sample(self, data, method):
    sample = pilot.StructAny_New(self.optim_algo.runtime.getTypeCode('SALOME_TYPES/ParametricInput'))

    # TODO Input, Output VarList
    inputVarList  = pilot.SequenceAny_New(self.optim_algo.runtime.getTypeCode("string"))
    outputVarList = pilot.SequenceAny_New(self.optim_algo.runtime.getTypeCode("string"))
    for var in self.optim_algo.da_study.InputVariables:
      inputVarList.pushBack(var)
    for var in self.optim_algo.da_study.OutputVariables:
      outputVarList.pushBack(var)
    sample.setEltAtRank("inputVarList", inputVarList)
    sample.setEltAtRank("outputVarList", outputVarList)

    # Les parametres specifiques à ADAO
    specificParameters = pilot.SequenceAny_New(self.optim_algo.runtime.getTypeCode("SALOME_TYPES/Parameter"))
    method_name = pilot.StructAny_New(self.optim_algo.runtime.getTypeCode('SALOME_TYPES/Parameter'))
    method_name.setEltAtRank("name", "method")
    method_name.setEltAtRank("value", method)
    specificParameters.pushBack(method_name)
    sample.setEltAtRank("specificParameters", specificParameters)

    # Les données
    # TODO à faire
    #print data
    #print data.ndim
    #print data.shape
    #print data[:,0]
    #print data.flatten()
    #print data.flatten().shape

    variable          = pilot.SequenceAny_New(self.optim_algo.runtime.getTypeCode("double"))
    variable_sequence = pilot.SequenceAny_New(variable.getType())
    state_sequence    = pilot.SequenceAny_New(variable_sequence.getType())
    time_sequence     = pilot.SequenceAny_New(state_sequence.getType())

    #print "Input Data", data
    if isinstance(data, type((1,2))):
      self.add_parameters(data[0], variable_sequence)
      self.add_parameters(data[1], variable_sequence, Output=True) # Output == Y
    else:
      self.add_parameters(data, variable_sequence)
    state_sequence.pushBack(variable_sequence)
    time_sequence.pushBack(state_sequence)
    sample.setEltAtRank("inputValues", time_sequence)
    return sample

  def add_parameters(self, data, variable_sequence, Output=False):
    param = pilot.SequenceAny_New(self.optim_algo.runtime.getTypeCode("double"))
    elt_list = 0 # index dans la liste des arguments
    val_number = 0 # nbre dans l'argument courant
    if not Output:
      val_end = self.optim_algo.da_study.InputVariables[self.optim_algo.da_study.InputVariablesOrder[elt_list]] # nbr de l'argument courant (-1 == tout)
    else:
      val_end = self.optim_algo.da_study.OutputVariables[self.optim_algo.da_study.OutputVariablesOrder[elt_list]] # nbr de l'argument courant (-1 == tout)

    it = data.flat
    for val in it:
      param.pushBack(val)
      val_number += 1
      # Test si l'argument est ok
      if val_end != -1:
        if val_number == val_end:
          variable_sequence.pushBack(param)
          param = pilot.SequenceAny_New(self.optim_algo.runtime.getTypeCode("double"))
          val_number = 0
          elt_list += 1
          if not Output:
            if elt_list < len(self.optim_algo.da_study.InputVariablesOrder):
              val_end = self.optim_algo.da_study.InputVariables[self.optim_algo.da_study.InputVariablesOrder[elt_list]]
            else:
              break
          else:
            if elt_list < len(self.optim_algo.da_study.OutputVariablesOrder):
              val_end = self.optim_algo.da_study.OutputVariables[self.optim_algo.da_study.OutputVariablesOrder[elt_list]]
            else:
              break
    if val_end == -1:
      variable_sequence.pushBack(param)

  def get_data_from_any(self, any_data):
    error = any_data["returnCode"].getIntValue()
    if error != 0:
      self.optim_algo.setError(any_data["errorMessage"].getStringValue())

    data = []
    outputValues = any_data["outputValues"]
    #print outputValues
    for variable in outputValues[0][0]:
      for i in range(variable.size()):
        data.append(variable[i].getDoubleValue())

    matrix = numpy.matrix(data).T
    return matrix

  def Direct(self, X, sync = 1):
    #print "Call Direct OptimizerHooks"
    if sync == 1:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      sample = self.create_sample(X, "Direct")
      self.optim_algo.pool.pushInSample(local_counter, sample)

      # 3: Wait
      while 1:
        #print "waiting"
        self.optim_algo.signalMasterAndWait()
        #print "signal"
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.optim_algo.pool.getCurrentId()
          if sample_id == local_counter:
            # 4: Data is ready
            any_data = self.optim_algo.pool.getOutSample(local_counter)
            Y = self.get_data_from_any(any_data)

            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.counter_lock.release()
            return Y
    else:
      #print "sync false is not yet implemented"
      self.optim_algo.setError("sync == false not yet implemented")

  def Tangent(self, X, sync = 1):
    #print "Call Tangent OptimizerHooks"
    if sync == 1:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      sample = self.create_sample(X, "Tangent")
      self.optim_algo.pool.pushInSample(local_counter, sample)

      # 3: Wait
      while 1:
        self.optim_algo.signalMasterAndWait()
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.optim_algo.pool.getCurrentId()
          if sample_id == local_counter:
            # 4: Data is ready
            any_data = self.optim_algo.pool.getOutSample(local_counter)
            Y = self.get_data_from_any(any_data)

            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.counter_lock.release()
            return Y
    else:
      #print "sync false is not yet implemented"
      self.optim_algo.setError("sync == false not yet implemented")

  def Adjoint(self, (X, Y), sync = 1):
    #print "Call Adjoint OptimizerHooks"
    if sync == 1:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      sample = self.create_sample((X,Y), "Adjoint")
      self.optim_algo.pool.pushInSample(local_counter, sample)

      # 3: Wait
      while 1:
        #print "waiting"
        self.optim_algo.signalMasterAndWait()
        #print "signal"
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.optim_algo.pool.getCurrentId()
          if sample_id == local_counter:
            # 4: Data is ready
            any_data = self.optim_algo.pool.getOutSample(local_counter)
            Z = self.get_data_from_any(any_data)

            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.counter_lock.release()
            return Z
    else:
      #print "sync false is not yet implemented"
      self.optim_algo.setError("sync == false not yet implemented")

class AssimilationAlgorithm_asynch(SALOMERuntime.OptimizerAlgASync):

  def __init__(self):
    SALOMERuntime.RuntimeSALOME_setRuntime()
    SALOMERuntime.OptimizerAlgASync.__init__(self, None)
    self.runtime = SALOMERuntime.getSALOMERuntime()

    # Definission des types d'entres et de sorties pour le code de calcul
    self.tin      = self.runtime.getTypeCode("SALOME_TYPES/ParametricInput")
    self.tout     = self.runtime.getTypeCode("SALOME_TYPES/ParametricOutput")
    self.pyobject = self.runtime.getTypeCode("pyobj")

    self.optim_hooks = OptimizerHooks(self)

  # input vient du port algoinit, input est un Any YACS !
  def initialize(self,input):
    #print "Algorithme initialize"

    # get the daStudy
    #print "[Debug] Input is ", input
    str_da_study = input.getStringValue()
    self.da_study = pickle.loads(str_da_study)
    #print "[Debug] da_study is ", self.da_study
    self.da_study.initAlgorithm()
    self.ADD = self.da_study.getAssimilationStudy()

  def startToTakeDecision(self):
    #print "Algorithme startToTakeDecision"

    # Check if ObservationOperator is already set
    if self.da_study.getObservationOperatorType("Direct") == "Function" or self.da_study.getObservationOperatorType("Tangent") == "Function" or self.da_study.getObservationOperatorType("Adjoint") == "Function" :
      #print "Set Hooks"
      # Use proxy function for YACS
      self.hooks = OptimizerHooks(self)
      direct = tangent = adjoint = None
      if self.da_study.getObservationOperatorType("Direct") == "Function":
        direct = self.hooks.Direct
      if self.da_study.getObservationOperatorType("Tangent") == "Function" :
        tangent = self.hooks.Tangent
      if self.da_study.getObservationOperatorType("Adjoint") == "Function" :
        adjoint = self.hooks.Adjoint

      # Set ObservationOperator
      self.ADD.setObservationOperator(asFunction = {"Direct":direct, "Tangent":tangent, "Adjoint":adjoint})


    # Start Assimilation Study
    #print "ADD analyze"
    self.ADD.analyze()

    # Assimilation Study is finished
    self.pool.destroyAll()

  def getAlgoResult(self):
    #print "getAlgoResult"
    self.ADD.prepare_to_pickle()
    result = pickle.dumps(self.da_study)
    return result

  # Obligatoire ???
  def finish(self):
    #print "Algorithme finish"
  def parseFileToInit(self,fileName):
    #print "Algorithme parseFileToInit"

  # Fonctions qui ne changent pas
  def setPool(self,pool):
    self.pool=pool
  def getTCForIn(self):
    return self.tin
  def getTCForOut(self):
    return self.tout
  def getTCForAlgoInit(self):
    return self.pyobject
  def getTCForAlgoResult(self):
    return self.pyobject

