#-*- coding: utf-8 -*-

import SALOMERuntime
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

  def Direct(self, X, sync = 1):
    print "Call Direct OptimizerHooks"
    if sync == 1:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      computation = {}
      computation["method"] = "Direct"
      computation["data"] = X
      computation = pickle.dumps(computation)
      self.optim_algo.pool.pushInSample(local_counter, computation)

      # 3: Wait
      while 1:
        print "waiting"
        self.optim_algo.signalMasterAndWait()
        print "signal"
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.optim_algo.pool.getCurrentId()
          if sample_id == local_counter:
            # 4: Data is ready
            matrix_from_pool = self.optim_algo.pool.getOutSample(local_counter).getStringValue()

            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.counter_lock.release()

            # 6: return results
            Y = pickle.loads(matrix_from_pool)
            return Y
    else:
      print "sync false is not yet implemented"
      raise daStudy.daError("sync == false not yet implemented")

  def Tangent(self, X, sync = 1):
    print "Call Tangent OptimizerHooks"
    if sync == 1:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      computation = {}
      computation["method"] = "Tangent"
      computation["data"] = X
      computation = pickle.dumps(computation)
      self.optim_algo.pool.pushInSample(local_counter, computation)

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
            matrix_from_pool = self.optim_algo.pool.getOutSample(local_counter).getStringValue()

            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.counter_lock.release()

            # 6: return results
            Y = pickle.loads(matrix_from_pool)
            return Y
    else:
      print "sync false is not yet implemented"
      raise daStudy.daError("sync == false not yet implemented")

  def Adjoint(self, (X, Y), sync = 1):
    print "Call Adjoint OptimizerHooks"
    if sync == 1:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      computation = {}
      computation["method"] = "Adjoint"
      computation["data"] = (X, Y)
      computation = pickle.dumps(computation)
      self.optim_algo.pool.pushInSample(local_counter, computation)

      # 3: Wait
      while 1:
        print "waiting"
        self.optim_algo.signalMasterAndWait()
        print "signal"
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.optim_algo.pool.getCurrentId()
          if sample_id == local_counter:
            # 4: Data is ready
            matrix_from_pool = self.optim_algo.pool.getOutSample(local_counter).getStringValue()

            # 5: Release lock
            # Have to be done before but need a new implementation
            # of the optimizer loop
            self.counter_lock.release()

            # 6: return results
            Z = pickle.loads(matrix_from_pool)
            return Z
    else:
      print "sync false is not yet implemented"
      raise daStudy.daError("sync == false not yet implemented")

class AssimilationAlgorithm_asynch(SALOMERuntime.OptimizerAlgASync):

  def __init__(self):
    SALOMERuntime.RuntimeSALOME_setRuntime()
    SALOMERuntime.OptimizerAlgASync.__init__(self, None)
    self.runtime = SALOMERuntime.getSALOMERuntime()

    # Definission des types d'entres et de sorties pour le code de calcul
    self.tin  = self.runtime.getTypeCode("pyobj")
    self.tout = self.runtime.getTypeCode("pyobj")

    self.optim_hooks = OptimizerHooks(self)

  # input vient du port algoinit, input est un Any YACS !
  def initialize(self,input):
    print "Algorithme initialize"

    # get the daStudy
    #print "[Debug] Input is ", input
    str_da_study = input.getStringValue()
    self.da_study = pickle.loads(str_da_study)
    #print "[Debug] da_study is ", self.da_study
    self.da_study.initAlgorithm()
    self.ADD = self.da_study.getAssimilationStudy()

  def startToTakeDecision(self):
    print "Algorithme startToTakeDecision"

    # Check if ObservationOperator is already set
    if self.da_study.getObservationOperatorType("Direct") == "Function" or self.da_study.getObservationOperatorType("Tangent") == "Function" or self.da_study.getObservationOperatorType("Adjoint") == "Function" :
      print "Set Hooks"
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
    print "ADD analyze"
    self.ADD.analyze()

    # Assimilation Study is finished
    self.pool.destroyAll()

  def getAlgoResult(self):
    print "getAlgoResult"
    self.ADD.prepare_to_pickle()
    result = pickle.dumps(self.da_study)
    return result

  # Obligatoire ???
  def finish(self):
    print "Algorithme finish"
  def parseFileToInit(self,fileName):
    print "Algorithme parseFileToInit"

  # Fonctions qui ne changent pas
  def setPool(self,pool):
    self.pool=pool
  def getTCForIn(self):
    return self.tin
  def getTCForOut(self):
    return self.tout
  def getTCForAlgoInit(self):
    return self.tin
  def getTCForAlgoResult(self):
    return self.tout

