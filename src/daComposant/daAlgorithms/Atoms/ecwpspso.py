# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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

__doc__ = """
    Standard Particle Swarm Optimization 2011 (//SIS)
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, logging
from daCore.NumericObjects import ApplyBounds, VariablesAndIncrementsBounds
from daCore.NumericObjects import GenerateRandomPointInHyperSphere
from daCore.NumericObjects import GetNeighborhoodTopology
from daCore.PlatformInfo import vfloat
from numpy.random import uniform as rand

# ==============================================================================
def ecwpspso(selfA, Xb, Y, HO, R, B):
    #
    Hm = HO["Direct"].appliedTo
    #
    BI = B.getI()
    RI = R.getI()
    #
    Xini = selfA._parameters["InitializationPoint"]
    #
    Bounds, BoxBounds = VariablesAndIncrementsBounds(
        selfA._parameters["Bounds"],
        selfA._parameters["BoxBounds"],
        Xini,
        selfA._name,
        0.5,
    )

    def CostFunction(x, hm, QualityMeasure="AugmentedWeightedLeastSquares"):
        _X  = numpy.asarray( x ).reshape((-1, 1))
        _HX = numpy.asarray( hm ).reshape((-1, 1))
        _Innovation = Y - _HX
        #
        if QualityMeasure in ["AugmentedWeightedLeastSquares", "AWLS", "DA"]:
            if BI is None or RI is None:
                raise ValueError("Background and Observation error covariance matrices has to be properly defined!")
            Jb  = 0.5 * (_X - Xb).T @ (BI @ (_X - Xb))
            Jo  = 0.5 * _Innovation.T @ (RI @ _Innovation)
        elif QualityMeasure in ["WeightedLeastSquares", "WLS"]:
            if RI is None:
                raise ValueError("Observation error covariance matrix has to be properly defined!")
            Jb  = 0.
            Jo  = 0.5 * _Innovation.T @ (RI @ _Innovation)
        elif QualityMeasure in ["LeastSquares", "LS", "L2"]:
            Jb  = 0.
            Jo  = 0.5 * _Innovation.T @ _Innovation
        elif QualityMeasure in ["AbsoluteValue", "L1"]:
            Jb  = 0.
            Jo  = numpy.sum( numpy.abs(_Innovation) )
        elif QualityMeasure in ["MaximumError", "ME", "Linf"]:
            Jb  = 0.
            Jo  = numpy.max( numpy.abs(_Innovation) )
        #
        J   = vfloat( Jb ) + vfloat( Jo )
        #
        return J, vfloat( Jb ), vfloat( Jo )

    def KeepRunningCondition(__step, __nbfct):
        if __step >= selfA._parameters["MaximumNumberOfIterations"]:
            logging.debug("%s Stopping search because the number %i of evolving iterations is exceeding the maximum %i."%(selfA._name, __step, selfA._parameters["MaximumNumberOfIterations"]))  # noqa: E501
            return False
        elif __nbfct >= selfA._parameters["MaximumNumberOfFunctionEvaluations"]:
            logging.debug("%s Stopping search because the number %i of function evaluations is exceeding the maximum %i."%(selfA._name, __nbfct, selfA._parameters["MaximumNumberOfFunctionEvaluations"]))  # noqa: E501
            return False
        else:
            return True
    #
    # Paramètres internes
    # -------------------
    __nbI = selfA._parameters["NumberOfInsects"]
    __nbP = len(Xini)  # Dimension ou nombre de paramètres
    #
    __iw = float( selfA._parameters["InertiaWeight"] )
    __sa = float( selfA._parameters["SocialAcceleration"] )
    __ca = float( selfA._parameters["CognitiveAcceleration"] )
    __vc = float( selfA._parameters["VelocityClampingFactor"] )
    logging.debug("%s Cognitive acceleration (recall to the best previously known value of the insect) = %s"%(selfA._name, str(__ca)))  # noqa: E501
    logging.debug("%s Social acceleration (recall to the best insect value of the group) = %s"%(selfA._name, str(__sa)))
    logging.debug("%s Inertial weight = %s"%(selfA._name, str(__iw)))
    logging.debug("%s Velocity clamping factor = %s"%(selfA._name, str(__vc)))
    #
    # Initialisation de l'essaim
    # --------------------------
    LimitPlace = Bounds
    LimitSpeed = BoxBounds
    #
    nbfct = 1  # Nb d'évaluations
    HX = Hm( Xini )
    JXini, JbXini, JoXini = CostFunction(Xini, HX, selfA._parameters["QualityCriterion"])
    if selfA._parameters["StoreInitialState"]:
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJ" ].store( JXini  )
        selfA.StoredVariables["CostFunctionJb"].store( JbXini )
        selfA.StoredVariables["CostFunctionJo"].store( JoXini )
        if selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xini )
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX )
    #
    Swarm  = numpy.zeros((__nbI, 4, __nbP))  # 4 car (x,v,gbest,lbest)
    for __p in range(__nbP):
        Swarm[:, 0, __p] = rand( low=LimitPlace[__p, 0], high=LimitPlace[__p, 1], size=__nbI)  # Position
        Swarm[:, 1, __p] = rand( low=LimitSpeed[__p, 0], high=LimitSpeed[__p, 1], size=__nbI)  # Velocity
    logging.debug("%s Initialisation of the swarm with %i insects of size %i "%(selfA._name, Swarm.shape[0], Swarm.shape[2]))  # noqa: E501
    #
    __nbh = GetNeighborhoodTopology( selfA._parameters["SwarmTopology"], list(range(__nbI)) )
    #
    qSwarm = JXini * numpy.ones((__nbI, 6))  # Qualités (J, Jb, Jo) par insecte + par voisinage
    __EOS = Hm(
        numpy.vsplit(Swarm[:, 0, :], __nbI),
        argsAsSerie = True,
        returnSerieAsArrayMatrix = False,
    )
    for __i in range(__nbI):
        nbfct += 1
        JTest, JbTest, JoTest = CostFunction(Swarm[__i, 0, :], __EOS[__i], selfA._parameters["QualityCriterion"])
        if JTest < JXini:
            Swarm[__i, 2, :] = Swarm[__i, 0, :]  # xBest
            qSwarm[__i, :3 ] = (JTest, JbTest, JoTest)
        else:
            Swarm[__i, 2, :] = Xini  # xBest
            qSwarm[__i, :3 ] = (JXini, JbXini, JoXini)
    logging.debug("%s Initialisation of the best previous insects"%selfA._name)
    #
    iBest = numpy.argmin(qSwarm[:, 0])
    xBest = Swarm[iBest, 2, :]
    for __i in range(__nbI):
        Swarm[__i, 3, :] = xBest  # lBest
        qSwarm[__i, 3: ] = qSwarm[iBest, :3]
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        selfA.StoredVariables["CurrentState"].store( xBest )
    selfA.StoredVariables["CostFunctionJ" ].store( qSwarm[iBest, 0]  )
    selfA.StoredVariables["CostFunctionJb"].store( qSwarm[iBest, 1] )
    selfA.StoredVariables["CostFunctionJo"].store( qSwarm[iBest, 2] )
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalStates"):
        selfA.StoredVariables["InternalStates"].store( Swarm[:, 0, :].T )
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalCostFunctionJ"):
        selfA.StoredVariables["InternalCostFunctionJ"].store( qSwarm[:, 0] )
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalCostFunctionJb"):
        selfA.StoredVariables["InternalCostFunctionJb"].store( qSwarm[:, 1] )
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalCostFunctionJo"):
        selfA.StoredVariables["InternalCostFunctionJo"].store( qSwarm[:, 2] )
    #
    selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    step = 0
    while KeepRunningCondition(step, nbfct):
        step += 1
        #
        __EOS = Hm(
            numpy.vsplit(Swarm[:, 0, :], __nbI),
            argsAsSerie = True,
            returnSerieAsArrayMatrix = False,
        )
        for __i in range(__nbI):
            # Évalue
            JTest, JbTest, JoTest = CostFunction(Swarm[__i, 0, :], __EOS[__i], selfA._parameters["QualityCriterion"])
            # Maj lbest
            if JTest < qSwarm[__i, 0]:
                Swarm[__i, 2, :] = Swarm[__i, 0, :]
                qSwarm[__i, :3 ]  = (JTest, JbTest, JoTest)
        #
        for __i in range(__nbI):
            # Maj gbest
            __im = numpy.argmin( [qSwarm[__v, 0] for __v in __nbh[__i]] )
            __il = __nbh[__i][__im]  # Best in NB
            if qSwarm[__il, 0] < qSwarm[__i, 3]:
                Swarm[__i, 3, :] = Swarm[__il, 2, :]
                qSwarm[__i, 3: ] = qSwarm[__il, :3]
        #
        for __i in range(__nbI - 1, 0 - 1, -1):
            __rct = rand(size=__nbP)
            __rst = rand(size=__nbP)
            __xPoint = Swarm[__i, 0, :]
            # Points
            __pPoint = __xPoint + __ca * __rct * (Swarm[__i, 2, :] - __xPoint)
            __lPoint = __xPoint + __sa * __rst * (Swarm[__i, 3, :] - __xPoint)
            __gPoint = (__xPoint + __pPoint + __lPoint) / 3
            __radius = numpy.linalg.norm(__gPoint - __xPoint)
            __rPoint = GenerateRandomPointInHyperSphere( __gPoint, __radius  )
            # Maj vitesse
            __value  = __iw * Swarm[__i, 1, :] + __rPoint - __xPoint
            Swarm[__i, 1, :] = ApplyBounds( __value, LimitSpeed )
            # Maj position
            __value  = __xPoint + Swarm[__i, 1, :]
            Swarm[__i, 0, :] = ApplyBounds( __value, LimitPlace )
            #
            nbfct += 1
        #
        iBest = numpy.argmin(qSwarm[:, 0])
        xBest = Swarm[iBest, 2, :]
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( xBest )
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( Hm( xBest ) )
        selfA.StoredVariables["CostFunctionJ" ].store( qSwarm[iBest, 0]  )
        selfA.StoredVariables["CostFunctionJb"].store( qSwarm[iBest, 1] )
        selfA.StoredVariables["CostFunctionJo"].store( qSwarm[iBest, 2] )
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalStates"):
            selfA.StoredVariables["InternalStates"].store( Swarm[:, 0, :].T )
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalCostFunctionJ"):
            selfA.StoredVariables["InternalCostFunctionJ"].store( qSwarm[:, 0] )
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalCostFunctionJb"):
            selfA.StoredVariables["InternalCostFunctionJb"].store( qSwarm[:, 1] )
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("InternalCostFunctionJo"):
            selfA.StoredVariables["InternalCostFunctionJo"].store( qSwarm[:, 2] )
        logging.debug("%s Step %i: insect %i is the better one with J =%.7f"%(selfA._name, step, iBest, qSwarm[iBest, 0]))  # noqa: E501
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = xBest
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("OMA") or \
            selfA._toStore("SimulatedObservationAtOptimum"):
        HXa = Hm(Xa)
    if selfA._toStore("Innovation") or \
            selfA._toStore("OMB") or \
            selfA._toStore("SimulatedObservationAtBackground"):
        HXb = Hm(Xb)
        Innovation = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( Innovation )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( Innovation )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    selfA._post_run(HO)
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
