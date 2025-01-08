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

import SALOMERuntime
import pilot
try:
    import cPickle as pickle
except:
    import pickle
import numpy
import threading
import sys
import traceback
import codecs

# Pour disposer des classes dans l'espace de nommage lors du pickle
from daCore.Aidsm import Aidsm
from daCore.AssimilationStudy import AssimilationStudy # JPA à résorber
from daYacsIntegration import daStudy

def dumps( data ):
  return str(codecs.encode(pickle.dumps(data), "base64").decode())
def loads( data ):
  return pickle.loads(codecs.decode(data.encode(), "base64"))

class OptimizerHooks:

  def __init__(self, optim_algo, switch_value=-1):
    self.optim_algo = optim_algo
    self.switch_value = str(int(switch_value))

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
    method_name.setEltAtRank("value", dumps(method))
    specificParameters.pushBack(method_name)
    # print self.optim_algo.has_observer
    if self.optim_algo.has_observer:
      obs_switch = pilot.StructAny_New(self.optim_algo.runtime.getTypeCode('SALOME_TYPES/Parameter'))
      obs_switch.setEltAtRank("name", "switch_value")
      obs_switch.setEltAtRank("value", dumps("1"))
      specificParameters.pushBack(obs_switch)
    if self.optim_algo.has_evolution_model:
      obs_switch = pilot.StructAny_New(self.optim_algo.runtime.getTypeCode('SALOME_TYPES/Parameter'))
      obs_switch.setEltAtRank("name", "switch_value")
      obs_switch.setEltAtRank("value", dumps(self.switch_value))
      specificParameters.pushBack(obs_switch)
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

    if data is None:
        it = []
    else:
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
    # print "Call Direct OptimizerHooks"
    if sync == 1:
      # 1: Get a unique sample number
      self.optim_algo.counter_lock.acquire()
      self.optim_algo.sample_counter += 1
      local_counter = self.optim_algo.sample_counter

      # 2: Put sample in the job pool
      sample = self.create_sample(X, "Direct")
      self.optim_algo.pool.pushInSample(local_counter, sample)

      # 3: Wait
      while True:
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
            self.optim_algo.counter_lock.release()
            return Z
    else:
      #print "sync false is not yet implemented"
      self.optim_algo.setError("sync == false not yet implemented")

  def Tangent(self, xxx_todo_changeme, sync = 1):
    # print "Call Tangent OptimizerHooks"
    (X, dX) = xxx_todo_changeme
    if sync == 1:
      # 1: Get a unique sample number
      self.optim_algo.counter_lock.acquire()
      self.optim_algo.sample_counter += 1
      local_counter = self.optim_algo.sample_counter

      # 2: Put sample in the job pool
      sample = self.create_sample((X,dX) , "Tangent")
      self.optim_algo.pool.pushInSample(local_counter, sample)

      # 3: Wait
      while True:
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
            Z = self.get_data_from_any(any_data)

            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.optim_algo.counter_lock.release()
            return Z
    else:
      #print "sync false is not yet implemented"
      self.optim_algo.setError("sync == false not yet implemented")

  def Adjoint(self, xxx_todo_changeme1, sync = 1):
    # print "Call Adjoint OptimizerHooks"
    (X, Y) = xxx_todo_changeme1
    if sync == 1:
      # 1: Get a unique sample number
      self.optim_algo.counter_lock.acquire()
      self.optim_algo.sample_counter += 1
      local_counter = self.optim_algo.sample_counter

      # 2: Put sample in the job pool
      sample = self.create_sample((X,Y), "Adjoint")
      self.optim_algo.pool.pushInSample(local_counter, sample)

      # 3: Wait
      while True:
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
            self.optim_algo.counter_lock.release()
            return Z
    else:
      #print "sync false is not yet implemented"
      self.optim_algo.setError("sync == false not yet implemented")

class AssimilationAlgorithm_asynch(SALOMERuntime.OptimizerAlgASync):

  def __init__(self):
    SALOMERuntime.RuntimeSALOME_setRuntime()
    SALOMERuntime.OptimizerAlgASync.__init__(self, None)
    self.runtime = SALOMERuntime.getSALOMERuntime()

    self.has_evolution_model = False
    self.has_observer = False

    # Gestion du compteur
    self.sample_counter = 0
    self.counter_lock = threading.Lock()

    # Definission des types d'entres et de sorties pour le code de calcul
    self.tin      = self.runtime.getTypeCode("SALOME_TYPES/ParametricInput")
    self.tout     = self.runtime.getTypeCode("SALOME_TYPES/ParametricOutput")
    self.pyobject = self.runtime.getTypeCode("pyobj")

    # Absolument indispensable de definir ainsi "self.optim_hooks"
    # (sinon on a une "Unknown Exception" sur l'attribut "finish")
    self.optim_hooks = OptimizerHooks(self)

  # input vient du port algoinit, input est un Any YACS !
  def initialize(self,input):
    #print "Algorithme initialize"

    # get the daStudy
    # print "[Debug] Input is ", input
    if sys.version_info.major < 3:
        str_da_study = input.getStringValue()
    else:
        str_da_study = input.getBytes()
    try:
        self.da_study = pickle.loads(str_da_study)
    except ValueError as e:
        raise ValueError("\n\n  Handling internal error in study exchange (message: \"%s\").\n  The case is probably too big (bigger than the physical plus the virtual memory available).\n  Try if possible to store the covariance matrices in sparse format.\n"%(str(e),))
    #print "[Debug] da_study is ", self.da_study
    self.da_study.initYIAlgorithm()
    self.ADD = self.da_study.getResults()

  def startToTakeDecision(self):
    # print "Algorithme startToTakeDecision"

    # Check if ObservationOperator is already set
    if self.da_study.getYIObservationOperatorType("Direct") == "Function" or self.da_study.getYIObservationOperatorType("Tangent") == "Function" or self.da_study.getYIObservationOperatorType("Adjoint") == "Function" :
      # print "Set Hooks for ObservationOperator"
      # Use proxy function for YACS
      self.hooksOO = OptimizerHooks(self, switch_value=1)
      direct = tangent = adjoint = None
      if self.da_study.getYIObservationOperatorType("Direct") == "Function":
        direct = self.hooksOO.Direct
      if self.da_study.getYIObservationOperatorType("Tangent") == "Function" :
        tangent = self.hooksOO.Tangent
      if self.da_study.getYIObservationOperatorType("Adjoint") == "Function" :
        adjoint = self.hooksOO.Adjoint

      # Set ObservationOperator
      self.ADD.setObservationOperator(ThreeFunctions = {"Direct":direct, "Tangent":tangent, "Adjoint":adjoint})
    # else:
      # print "Not setting Hooks for ObservationOperator"

    # Check if EvolutionModel is already set
    if self.da_study.getYIEvolutionModelType("Direct") == "Function" or self.da_study.getYIEvolutionModelType("Tangent") == "Function" or self.da_study.getYIEvolutionModelType("Adjoint") == "Function" :
      self.has_evolution_model = True
      # print "Set Hooks for EvolutionModel"
      # Use proxy function for YACS
      self.hooksEM = OptimizerHooks(self, switch_value=2)
      direct = tangent = adjoint = None
      if self.da_study.getYIEvolutionModelType("Direct") == "Function":
        direct = self.hooksEM.Direct
      if self.da_study.getYIEvolutionModelType("Tangent") == "Function" :
        tangent = self.hooksEM.Tangent
      if self.da_study.getYIEvolutionModelType("Adjoint") == "Function" :
        adjoint = self.hooksEM.Adjoint

      # Set EvolutionModel
      self.ADD.setEvolutionModel(ThreeFunctions = {"Direct":direct, "Tangent":tangent, "Adjoint":adjoint})
    # else:
      # print "Not setting Hooks for EvolutionModel"

    # Set Observers
    for observer_name in list(self.da_study.observers_dict.keys()):
      # print "observers %s found" % observer_name
      self.has_observer = True
      if self.da_study.observers_dict[observer_name]["scheduler"] != "":
        self.ADD.setObserver(Variable = observer_name, ObjectFunction = self.obs, Scheduler = self.da_study.observers_dict[observer_name]["scheduler"], Info = observer_name)
      else:
        self.ADD.setObserver(Variable = observer_name, ObjectFunction = self.obs, Info = observer_name)

    # Start Assimilation Study
    print("Launching the analysis\n")
    try:
        self.ADD.execute()
    except Exception as e:
        if isinstance(e, type(SyntaxError())): msg = "at %s: %s"%(e.offset, e.text)
        else: msg = ""
        raise ValueError("during execution, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the YACS GUI or in the launching terminal."%(str(e),msg))

    # Assimilation Study is finished
    self.pool.destroyAll()

  def obs(self, var, info):
    # print("Call observer %s with var type %s" %(info,type(var))
    sample = pilot.StructAny_New(self.runtime.getTypeCode('SALOME_TYPES/ParametricInput'))

    # Fake data
    inputVarList  = pilot.SequenceAny_New(self.runtime.getTypeCode("string"))
    outputVarList = pilot.SequenceAny_New(self.runtime.getTypeCode("string"))
    inputVarList.pushBack("a")
    outputVarList.pushBack("a")
    sample.setEltAtRank("inputVarList", inputVarList)
    sample.setEltAtRank("outputVarList", outputVarList)
    variable          = pilot.SequenceAny_New(self.runtime.getTypeCode("double"))
    variable_sequence = pilot.SequenceAny_New(variable.getType())
    state_sequence    = pilot.SequenceAny_New(variable_sequence.getType())
    time_sequence     = pilot.SequenceAny_New(state_sequence.getType())
    variable.pushBack(1.0)
    variable_sequence.pushBack(variable)
    state_sequence.pushBack(variable_sequence)
    time_sequence.pushBack(state_sequence)
    sample.setEltAtRank("inputValues", time_sequence)

    # Add observer values in specific parameters
    specificParameters = pilot.SequenceAny_New(self.runtime.getTypeCode("SALOME_TYPES/Parameter"))

    # Switch Value
    obs_switch = pilot.StructAny_New(self.runtime.getTypeCode('SALOME_TYPES/Parameter'))
    obs_switch.setEltAtRank("name", "switch_value")
    obs_switch.setEltAtRank("value", dumps(self.da_study.observers_dict[info]["number"]))
    specificParameters.pushBack(obs_switch)

    # Var
    var_struct = pilot.StructAny_New(self.runtime.getTypeCode('SALOME_TYPES/Parameter'))
    var_struct.setEltAtRank("name", "var")

    # Remove Data Observer, so you can ...
    var.removeDataObserver(self.obs)
    # Pickle then ...
    var_struct.setEltAtRank("value", dumps(var))
    specificParameters.pushBack(var_struct)
    # Add Again Data Observer
    if self.da_study.observers_dict[info]["scheduler"] != "":
      self.ADD.setObserver(Variable = info, ObjectFunction = self.obs, Scheduler = self.da_study.observers_dict[info]["scheduler"], Info = info)
    else:
      self.ADD.setObserver(Variable = info, ObjectFunction = self.obs, Info = info)

    # Info
    info_struct = pilot.StructAny_New(self.runtime.getTypeCode('SALOME_TYPES/Parameter'))
    info_struct.setEltAtRank("name", "info")
    info_struct.setEltAtRank("value", dumps(self.da_study.observers_dict[info]["info"]))
    specificParameters.pushBack(info_struct)

    sample.setEltAtRank("specificParameters", specificParameters)

    self.counter_lock.acquire()
    self.sample_counter += 1
    local_counter = self.sample_counter
    self.pool.pushInSample(local_counter, sample)

    # Wait
    try:
      while True:
        self.signalMasterAndWait()
        if self.isTerminationRequested():
          self.pool.destroyAll()
        else:
          # Get current Id
          sample_id = self.pool.getCurrentId()
          if sample_id == local_counter:
            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.counter_lock.release()
            break
    except:
      print("Exception in user code:")
      print('-'*60)
      traceback.print_exc(file=sys.stdout)
      print('-'*60)

  def getAlgoResult(self):
#     # Remove data observers, required to pickle assimilation study object
#     for observer_name in list(self.da_study.observers_dict.keys()):
#       self.ADD.removeDataObserver(observer_name, self.obs)
    if sys.version_info.major < 3:
        self.da_study.YI_prepare_to_pickle()
        return pickle.dumps(self.da_study)
    else:
        return pickle.dumps(self.da_study.YI_prepare_to_pickle())

  # Obligatoire ???
  def finish(self):
    pass
  def parseFileToInit(self,fileName):
    pass

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

