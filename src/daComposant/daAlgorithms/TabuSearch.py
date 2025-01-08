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

import numpy
from daCore import BasicObjects
from daCore.PlatformInfo import vfloat

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "TABUSEARCH")
        self.defineRequiredParameter(
            name     = "MaximumNumberOfIterations",
            default  = 50,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = 1,
            oldname  = "MaximumNumberOfSteps",
        )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
        )
        self.defineRequiredParameter(
            name     = "LengthOfTabuList",
            default  = 50,
            typecast = int,
            message  = "Longueur de la liste tabou",
            minval   = 1,
        )
        self.defineRequiredParameter(
            name     = "NumberOfElementaryPerturbations",
            default  = 1,
            typecast = int,
            message  = "Nombre de perturbations élémentaires pour choisir une perturbation d'état",
            minval   = 1,
        )
        self.defineRequiredParameter(
            name     = "NoiseDistribution",
            default  = "Uniform",
            typecast = str,
            message  = "Distribution pour générer les perturbations d'état",
            listval  = ["Gaussian", "Uniform"],
        )
        self.defineRequiredParameter(
            name     = "QualityCriterion",
            default  = "AugmentedWeightedLeastSquares",
            typecast = str,
            message  = "Critère de qualité utilisé",
            listval  = [
                "AugmentedWeightedLeastSquares", "AWLS", "DA",
                "WeightedLeastSquares", "WLS",
                "LeastSquares", "LS", "L2",
                "AbsoluteValue", "L1",
                "MaximumError", "ME", "Linf",
            ],
        )
        self.defineRequiredParameter(
            name     = "NoiseHalfRange",
            default  = [],
            typecast = numpy.ravel,
            message  = "Demi-amplitude des perturbations uniformes centrées d'état pour chaque composante de l'état",
        )
        self.defineRequiredParameter(
            name     = "StandardDeviation",
            default  = [],
            typecast = numpy.ravel,
            message  = "Ecart-type des perturbations gaussiennes d'état pour chaque composante de l'état",
        )
        self.defineRequiredParameter(
            name     = "NoiseAddingProbability",
            default  = 1.,
            typecast = float,
            message  = "Probabilité de perturbation d'une composante de l'état",
            minval   = 0.,
            maxval   = 1.,
        )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
        )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "Analysis",
                "BMA",
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "CurrentIterationNumber",
                "CurrentState",
                "Innovation",
                "OMA",
                "OMB",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
            ]
        )
        self.defineRequiredParameter(  # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
        )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
        )
        self.setAttributes(
            tags=(
                "Optimization",
                "NonLinear",
                "MetaHeuristic",
            ),
            features=(
                "NonLocalOptimization",
                "DerivativeFree",
                "ConvergenceOnNumbers",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        if self._parameters["NoiseDistribution"] == "Uniform":
            nrange = self._parameters["NoiseHalfRange"]  # Vecteur
            if nrange.size != Xb.size:
                raise ValueError("Noise generation by Uniform distribution requires range for all variable increments. The actual noise half range vector is:\n%s"%nrange)  # noqa: E501
        elif self._parameters["NoiseDistribution"] == "Gaussian":
            sigma = numpy.ravel(self._parameters["StandardDeviation"])  # Vecteur
            if sigma.size != Xb.size:
                raise ValueError("Noise generation by Gaussian distribution requires standard deviation for all variable increments. The actual standard deviation vector is:\n%s"%sigma)  # noqa: E501
        #
        Hm = HO["Direct"].appliedTo
        #
        BI = B.getI()
        RI = R.getI()

        def Tweak( x, NoiseDistribution, NoiseAddingProbability ):
            _X  = numpy.array( x, dtype=float, copy=True ).ravel().reshape((-1, 1))
            if NoiseDistribution == "Uniform":
                for i in range(_X.size):
                    if NoiseAddingProbability >= numpy.random.uniform():
                        _increment = numpy.random.uniform(low=-nrange[i], high=nrange[i])
                        # On ne traite pas encore le dépassement des bornes ici
                        _X[i] += _increment
            elif NoiseDistribution == "Gaussian":
                for i in range(_X.size):
                    if NoiseAddingProbability >= numpy.random.uniform():
                        _increment = numpy.random.normal(loc=0., scale=sigma[i])
                        # On ne traite pas encore le dépassement des bornes ici
                        _X[i] += _increment
            #
            return _X

        def StateInList( x, _TL ):
            _X  = numpy.ravel( x )
            _xInList = False
            for state in _TL:
                if numpy.all(numpy.abs( _X - numpy.ravel(state) ) <= 1e-16 * numpy.abs(_X)):
                    _xInList = True
            # if _xInList: import sys ; sys.exit()
            return _xInList

        def CostFunction(x, QualityMeasure="AugmentedWeightedLeastSquares"):
            _X  = numpy.ravel( x ).reshape((-1, 1))
            _HX = numpy.ravel( Hm( _X ) ).reshape((-1, 1))
            _Innovation = Y - _HX
            #
            if QualityMeasure in ["AugmentedWeightedLeastSquares", "AWLS", "DA"]:
                if BI is None or RI is None:
                    raise ValueError("Background and Observation error covariance matrices has to be properly defined!")
                Jb  = vfloat(0.5 * (_X - Xb).T @ (BI @ (_X - Xb)))
                Jo  = vfloat(0.5 * _Innovation.T @ (RI @ _Innovation))
            elif QualityMeasure in ["WeightedLeastSquares", "WLS"]:
                if RI is None:
                    raise ValueError("Observation error covariance matrix has to be properly defined!")
                Jb  = 0.
                Jo  = vfloat(0.5 * _Innovation.T @ (RI @ _Innovation))
            elif QualityMeasure in ["LeastSquares", "LS", "L2"]:
                Jb  = 0.
                Jo  = vfloat(0.5 * _Innovation.T @ _Innovation)
            elif QualityMeasure in ["AbsoluteValue", "L1"]:
                Jb  = 0.
                Jo  = vfloat(numpy.sum( numpy.abs(_Innovation) ))
            elif QualityMeasure in ["MaximumError", "ME", "Linf"]:
                Jb  = 0.
                Jo  = vfloat(numpy.max( numpy.abs(_Innovation) ))
            #
            J   = Jb + Jo
            #
            return J
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        _n = 0
        _S = Xb
        _qualityS = CostFunction( _S, self._parameters["QualityCriterion"] )
        _Best, _qualityBest = _S, _qualityS
        _TabuList = []
        _TabuList.append( _S )
        while _n < self._parameters["MaximumNumberOfIterations"]:
            _n += 1
            if len(_TabuList) > self._parameters["LengthOfTabuList"]:
                _TabuList.pop(0)
            _R = Tweak( _S, self._parameters["NoiseDistribution"], self._parameters["NoiseAddingProbability"] )
            _qualityR = CostFunction( _R, self._parameters["QualityCriterion"] )
            for nbt in range(self._parameters["NumberOfElementaryPerturbations"] - 1):
                _W = Tweak( _S, self._parameters["NoiseDistribution"], self._parameters["NoiseAddingProbability"] )
                _qualityW = CostFunction( _W, self._parameters["QualityCriterion"] )
                if (not StateInList(_W, _TabuList)) and ( (_qualityW < _qualityR) or StateInList(_R, _TabuList) ):
                    _R, _qualityR = _W, _qualityW
            if (not StateInList( _R, _TabuList )) and (_qualityR < _qualityS):
                _S, _qualityS = _R, _qualityR
                _TabuList.append( _S )
            if _qualityS < _qualityBest:
                _Best, _qualityBest = _S, _qualityS
            #
            self.StoredVariables["CurrentIterationNumber"].store( len(self.StoredVariables["CostFunctionJ"]) )
            if self._parameters["StoreInternalVariables"] or self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( _Best )
            if self._toStore("SimulatedObservationAtCurrentState"):
                _HmX = Hm( _Best )
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HmX )
            self.StoredVariables["CostFunctionJb"].store( 0. )
            self.StoredVariables["CostFunctionJo"].store( 0. )
            self.StoredVariables["CostFunctionJ" ].store( _qualityBest )
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = _Best
        #
        self.StoredVariables["Analysis"].store( Xa )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("OMA") or \
                self._toStore("SimulatedObservationAtOptimum"):
            HXa = Hm(Xa).reshape((-1, 1))
        if self._toStore("Innovation") or \
                self._toStore("OMB") or \
                self._toStore("SimulatedObservationAtBackground"):
            HXb = Hm(Xb).reshape((-1, 1))
            Innovation = Y - HXb
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( Innovation )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( Innovation )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( Y - HXa )
        if self._toStore("SimulatedObservationAtBackground"):
            self.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
