# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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

import logging
from daCore import BasicObjects
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "TABUSEARCH")
        self.defineRequiredParameter(
            name     = "MaximumNumberOfSteps",
            default  = 50,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = 1,
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
            listval  = ["Gaussian","Uniform"],
            )
        self.defineRequiredParameter(
            name     = "QualityCriterion",
            default  = "AugmentedWeightedLeastSquares",
            typecast = str,
            message  = "Critère de qualité utilisé",
            listval  = ["AugmentedWeightedLeastSquares","AWLS","DA",
                        "WeightedLeastSquares","WLS",
                        "LeastSquares","LS","L2",
                        "AbsoluteValue","L1",
                        "MaximumError","ME"],
            )
        self.defineRequiredParameter(
            name     = "NoiseHalfRange",
            default  = [],
            typecast = numpy.matrix,
            message  = "Demi-amplitude des perturbations uniformes centrées d'état pour chaque composante de l'état",
            )
        self.defineRequiredParameter(
            name     = "StandardDeviation",
            default  = [],
            typecast = numpy.matrix,
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
                "CurrentState",
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "Innovation",
                "OMA",
                "OMB",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                ]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            )
        self.setAttributes(tags=(
            "Optimization",
            "NonLinear",
            "MetaHeuristic",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        if self._parameters["NoiseDistribution"] == "Uniform":
            nrange = numpy.ravel(self._parameters["NoiseHalfRange"]) # Vecteur
            if nrange.size != Xb.size:
                raise ValueError("Noise generation by Uniform distribution requires range for all variable increments. The actual noise half range vector is:\n%s"%nrange)
        elif self._parameters["NoiseDistribution"] == "Gaussian":
            sigma = numpy.ravel(self._parameters["StandardDeviation"]) # Vecteur
            if sigma.size != Xb.size:
                raise ValueError("Noise generation by Gaussian distribution requires standard deviation for all variable increments. The actual standard deviation vector is:\n%s"%sigma)
        #
        # Opérateur d'observation
        # -----------------------
        Hm = HO["Direct"].appliedTo
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # Définition de la fonction de deplacement
        # ----------------------------------------
        def Tweak( x, NoiseDistribution, NoiseAddingProbability ):
            _X  = numpy.matrix(numpy.ravel( x )).T
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
        #
        def StateInList( x, TL ):
            _X  = numpy.ravel( x )
            _xInList = False
            for state in TL:
                if numpy.all(numpy.abs( _X - numpy.ravel(state) ) <= 1e-16*numpy.abs(_X)):
                    _xInList = True
            # if _xInList: import sys ; sys.exit()
            return _xInList
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        _n = 0
        _S = Xb
        # _qualityS = CostFunction( _S, self._parameters["QualityCriterion"] )
        _qualityS = BasicObjects.CostFunction3D(
                   _S,
            _Hm  = Hm,
            _BI  = BI,
            _RI  = RI,
            _Xb  = Xb,
            _Y   = Y,
            _SSC = self._parameters["StoreSupplementaryCalculations"],
            _QM  = self._parameters["QualityCriterion"],
            _SSV = self.StoredVariables,
            _sSc = False,
            )
        _Best, _qualityBest   =   _S, _qualityS
        _TabuList = []
        _TabuList.append( _S )
        while _n < self._parameters["MaximumNumberOfSteps"]:
            _n += 1
            if len(_TabuList) > self._parameters["LengthOfTabuList"]:
                _TabuList.pop(0)
            _R = Tweak( _S, self._parameters["NoiseDistribution"], self._parameters["NoiseAddingProbability"] )
            # _qualityR = CostFunction( _R, self._parameters["QualityCriterion"] )
            _qualityR = BasicObjects.CostFunction3D(
                       _R,
                _Hm  = Hm,
                _BI  = BI,
                _RI  = RI,
                _Xb  = Xb,
                _Y   = Y,
                _SSC = self._parameters["StoreSupplementaryCalculations"],
                _QM  = self._parameters["QualityCriterion"],
                _SSV = self.StoredVariables,
                _sSc = False,
                )
            for nbt in range(self._parameters["NumberOfElementaryPerturbations"]-1):
                _W = Tweak( _S, self._parameters["NoiseDistribution"], self._parameters["NoiseAddingProbability"] )
                # _qualityW = CostFunction( _W, self._parameters["QualityCriterion"] )
                _qualityW = BasicObjects.CostFunction3D(
                           _W,
                    _Hm  = Hm,
                    _BI  = BI,
                    _RI  = RI,
                    _Xb  = Xb,
                    _Y   = Y,
                    _SSC = self._parameters["StoreSupplementaryCalculations"],
                    _QM  = self._parameters["QualityCriterion"],
                    _SSV = self.StoredVariables,
                    _sSc = False,
                    )
                if (not StateInList(_W, _TabuList)) and ( (_qualityW < _qualityR) or StateInList(_R,_TabuList) ):
                    _R, _qualityR   =   _W, _qualityW
            if (not StateInList( _R, _TabuList )) and (_qualityR < _qualityS):
                _S, _qualityS   =   _R, _qualityR
                _TabuList.append( _S )
            if _qualityS < _qualityBest:
                _Best, _qualityBest   =   _S, _qualityS
            #
            if self._parameters["StoreInternalVariables"] or self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( _Best )
            if self._toStore("SimulatedObservationAtCurrentState"):
                _HmX = Hm( numpy.asmatrix(numpy.ravel( _Best )).T )
                _HmX = numpy.asmatrix(numpy.ravel( _HmX )).T
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HmX )
            self.StoredVariables["CostFunctionJb"].store( 0. )
            self.StoredVariables["CostFunctionJo"].store( 0. )
            self.StoredVariables["CostFunctionJ" ].store( _qualityBest )
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( _Best )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        if self._toStore("Innovation") or \
            self._toStore("OMB") or \
            self._toStore("SimulatedObservationAtBackground"):
            HXb = Hm(Xb)
            d = Y - HXb
        if self._toStore("OMA") or \
           self._toStore("SimulatedObservationAtOptimum"):
            HXa = Hm(Xa)
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if self._toStore("SimulatedObservationAtBackground"):
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
