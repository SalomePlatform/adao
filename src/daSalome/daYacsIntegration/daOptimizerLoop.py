#-*-coding:iso-8859-1-*-

import SALOMERuntime
import pickle
import numpy
import threading

from daCore.AssimilationStudy import AssimilationStudy

class OptimizerHooks:

  def __init__(self, optim_algo):
    self.optim_algo = optim_algo

    # Gestion du compteur
    self.sample_counter = 0
    self.counter_lock = threading.Lock()

  def Direct(self, X, sync = true):
    print "Call Direct OptimizerHooks"
    if sync == true:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      matrix_to_pool = pickle.dumps(X)
      self.optim_algo.pool.pushInSample(local_counter, matrix_to_pool)

      # 3: Wait
      while 1:
        self.optim_algo.signalMasterAndWait()
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.pool.getCurrentId()
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
      raise ValueError("sync == false not yet implemented")

  def Tangent(self, X, sync = true):
    print "Call Tangent OptimizerHooks"
    if sync == true:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      matrix_to_pool = pickle.dumps(X)
      self.optim_algo.pool.pushInSample(local_counter, matrix_to_pool)

      # 3: Wait
      while 1:
        self.optim_algo.signalMasterAndWait()
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.pool.getCurrentId()
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
      raise ValueError("sync == false not yet implemented")

  def Adjoint(self, (X, Y), sync = true):
    print "Call Adjoint OptimizerHooks"
    if sync == true:
      # 1: Get a unique sample number
      self.counter_lock.acquire()
      self.sample_counter += 1
      local_counter = self.sample_counter

      # 2: Put sample in the job pool
      matrix_to_pool = pickle.dumps(Y)
      self.optim_algo.pool.pushInSample(local_counter, matrix_to_pool)

      # 3: Wait
      while 1:
        self.optim_algo.signalMasterAndWait()
        if self.optim_algo.isTerminationRequested():
          self.optim_algo.pool.destroyAll()
          return
        else:
          # Get current Id
          sample_id = self.pool.getCurrentId()
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
      raise ValueError("sync == false not yet implemented")

class AssimilationAlgorithm_asynch_3DVAR(SALOMERuntime.OptimizerAlgASync):

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

  def startToTakeDecision(self):
    print "Algorithme startToTakeDecision"

    TODO !!

    precision = 1.e-13
    dimension = 3

    xt = numpy.matrix(numpy.arange(dimension)).T
    Eo = numpy.matrix(numpy.zeros((dimension,))).T
    Eb = numpy.matrix(numpy.zeros((dimension,))).T
    H  = numpy.matrix(numpy.core.identity(dimension))
    xb = xt + Eb
    yo = FunctionH( xt ) + Eo
    xb = xb.A1
    yo = yo.A1
    R  = numpy.matrix(numpy.core.identity(dimension)).T
    B  = numpy.matrix(numpy.core.identity(dimension)).T

    ADD = AssimilationStudy()
    ADD.setBackground         (asVector     = xb )
    ADD.setBackgroundError    (asCovariance = B )
    ADD.setObservation        (asVector     = yo )
    ADD.setObservationError   (asCovariance = R )
    ADD.setObservationOperator(asFunction   = {"Tangent":FunctionH,
                                               "Adjoint":AdjointH} )
    ADD.setControls()
    ADD.setAlgorithm(choice="3DVAR")
    ADD.analyze()

    xa = numpy.array(ADD.get("Analysis").valueserie(0))
    d  = numpy.array(ADD.get("Innovation").valueserie(0))
    if max(abs(xa - xb)) > precision:
        raise ValueError("Résultat du test erroné (1)")
    elif max(abs(d)) > precision:
        raise ValueError("Résultat du test erroné (2)")
    else:
        print "    Test correct, erreur maximale inférieure à %s"%precision
        print
    # On a fini !
    self.pool.destroyAll()

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
