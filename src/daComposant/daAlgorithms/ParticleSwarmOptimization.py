# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2022 EDF R&D
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

import numpy, logging, copy
from daCore import BasicObjects

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "PARTICLESWARMOPTIMIZATION")
        self.defineRequiredParameter(
            name     = "MaximumNumberOfIterations",
            default  = 50,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = 0,
            oldname  = "MaximumNumberOfSteps",
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfFunctionEvaluations",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal d'évaluations de la fonction",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter(
            name     = "NumberOfInsects",
            default  = 100,
            typecast = int,
            message  = "Nombre d'insectes dans l'essaim",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "SwarmVelocity",
            default  = 1.,
            typecast = float,
            message  = "Vitesse de groupe imposée par l'essaim",
            minval   = 0.,
            )
        self.defineRequiredParameter(
            name     = "GroupRecallRate",
            default  = 0.5,
            typecast = float,
            message  = "Taux de rappel au meilleur insecte du groupe (entre 0 et 1)",
            minval   = 0.,
            maxval   = 1.,
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
        self.defineRequiredParameter( # Pas de type
            name     = "BoxBounds",
            message  = "Liste des valeurs de bornes d'incréments de paramètres",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            )
        self.setAttributes(tags=(
            "Optimization",
            "NonLinear",
            "MetaHeuristic",
            "Population",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        if ("BoxBounds" in self._parameters) and isinstance(self._parameters["BoxBounds"], (list, tuple)) and (len(self._parameters["BoxBounds"]) > 0):
            BoxBounds = self._parameters["BoxBounds"]
            logging.debug("%s Prise en compte des bornes d'incréments de paramètres effectuée"%(self._name,))
        else:
            raise ValueError("Particle Swarm Optimization requires bounds on all variables increments to be truly given (BoxBounds).")
        BoxBounds   = numpy.array(BoxBounds)
        if numpy.isnan(BoxBounds).any():
            raise ValueError("Particle Swarm Optimization requires bounds on all variables increments to be truly given (BoxBounds), \"None\" is not allowed. The actual increments bounds are:\n%s"%BoxBounds)
        #
        Phig = float( self._parameters["GroupRecallRate"] )
        Phip = 1. - Phig
        logging.debug("%s Taux de rappel au meilleur insecte du groupe (entre 0 et 1) = %s et à la meilleure position précédente (son complémentaire à 1) = %s"%(self._name, str(Phig), str(Phip)))
        #
        Hm = HO["Direct"].appliedTo
        #
        BI = B.getI()
        RI = R.getI()
        #
        def CostFunction(x, QualityMeasure="AugmentedWeightedLeastSquares"):
            _X  = numpy.ravel( x ).reshape((-1,1))
            _HX = numpy.ravel( Hm( _X ) ).reshape((-1,1))
            _Innovation = Y - _HX
            #
            if QualityMeasure in ["AugmentedWeightedLeastSquares","AWLS","DA"]:
                if BI is None or RI is None:
                    raise ValueError("Background and Observation error covariance matrices has to be properly defined!")
                Jb  = 0.5 * (_X - Xb).T @ (BI @ (_X - Xb))
                Jo  = 0.5 * _Innovation.T @ (RI @ _Innovation)
            elif QualityMeasure in ["WeightedLeastSquares","WLS"]:
                if RI is None:
                    raise ValueError("Observation error covariance matrix has to be properly defined!")
                Jb  = 0.
                Jo  = 0.5 * _Innovation.T @ (RI @ _Innovation)
            elif QualityMeasure in ["LeastSquares","LS","L2"]:
                Jb  = 0.
                Jo  = 0.5 * _Innovation.T @ _Innovation
            elif QualityMeasure in ["AbsoluteValue","L1"]:
                Jb  = 0.
                Jo  = numpy.sum( numpy.abs(_Innovation) )
            elif QualityMeasure in ["MaximumError","ME", "Linf"]:
                Jb  = 0.
                Jo  = numpy.max( numpy.abs(_Innovation) )
            #
            J   = float( Jb ) + float( Jo )
            #
            return J
        #
        if Xb is not None:
            Xini = numpy.ravel(Xb)
        else:
            Xini = numpy.zeros(len(BoxBounds[:,0]))
        #
        SpaceUp  = BoxBounds[:,1] + Xini
        SpaceLow = BoxBounds[:,0] + Xini
        nbparam  = len(SpaceUp)
        #
        # Initialisation de l'essaim
        # --------------------------
        NumberOfFunctionEvaluations = 0
        LimitVelocity = numpy.abs(SpaceUp-SpaceLow)
        #
        PosInsect = []
        VelocityInsect = []
        for i in range(nbparam) :
            PosInsect.append(numpy.random.uniform(low=SpaceLow[i], high=SpaceUp[i], size=self._parameters["NumberOfInsects"]))
            VelocityInsect.append(numpy.random.uniform(low=-LimitVelocity[i], high=LimitVelocity[i], size=self._parameters["NumberOfInsects"]))
        VelocityInsect = numpy.array(VelocityInsect)
        PosInsect = numpy.array(PosInsect)
        #
        BestPosInsect = numpy.array(PosInsect)
        qBestPosInsect = []
        _Best = copy.copy(SpaceLow)
        _qualityBest = CostFunction(_Best,self._parameters["QualityCriterion"])
        NumberOfFunctionEvaluations += 1
        #
        for i in range(self._parameters["NumberOfInsects"]):
            insect  = numpy.ravel(PosInsect[:,i])
            quality = CostFunction(insect,self._parameters["QualityCriterion"])
            NumberOfFunctionEvaluations += 1
            qBestPosInsect.append(quality)
            if quality < _qualityBest:
                _Best  = copy.copy( insect )
                _qualityBest = copy.copy( quality )
        logging.debug("%s Initialisation, Insecte = %s, Qualité = %s"%(self._name, str(_Best), str(_qualityBest)))
        #
        self.StoredVariables["CurrentIterationNumber"].store( len(self.StoredVariables["CostFunctionJ"]) )
        if self._parameters["StoreInternalVariables"] or self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( _Best )
        self.StoredVariables["CostFunctionJb"].store( 0. )
        self.StoredVariables["CostFunctionJo"].store( 0. )
        self.StoredVariables["CostFunctionJ" ].store( _qualityBest )
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        for n in range(self._parameters["MaximumNumberOfIterations"]):
            for i in range(self._parameters["NumberOfInsects"]) :
                insect  = numpy.ravel(PosInsect[:,i])
                rp = numpy.random.uniform(size=nbparam)
                rg = numpy.random.uniform(size=nbparam)
                for j in range(nbparam) :
                    VelocityInsect[j,i] = self._parameters["SwarmVelocity"]*VelocityInsect[j,i] +  Phip*rp[j]*(BestPosInsect[j,i]-PosInsect[j,i]) +  Phig*rg[j]*(_Best[j]-PosInsect[j,i])
                    PosInsect[j,i] = PosInsect[j,i]+VelocityInsect[j,i]
                quality = CostFunction(insect,self._parameters["QualityCriterion"])
                NumberOfFunctionEvaluations += 1
                if quality < qBestPosInsect[i]:
                    BestPosInsect[:,i] = copy.copy( insect )
                    qBestPosInsect[i]  = copy.copy( quality )
                    if quality < _qualityBest :
                        _Best  = copy.copy( insect )
                        _qualityBest = copy.copy( quality )
            logging.debug("%s Etape %i, Insecte = %s, Qualité = %s"%(self._name, n, str(_Best), str(_qualityBest)))
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
            if NumberOfFunctionEvaluations > self._parameters["MaximumNumberOfFunctionEvaluations"]:
                logging.debug("%s Stopping search because the number %i of function evaluations is exceeding the maximum %i."%(self._name, NumberOfFunctionEvaluations, self._parameters["MaximumNumberOfFunctionEvaluations"]))
                break
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
            HXa = Hm(Xa)
        if self._toStore("Innovation") or \
            self._toStore("OMB") or \
            self._toStore("SimulatedObservationAtBackground"):
            HXb = Hm(Xb)
            Innovation = Y - HXb
        if self._toStore("Innovation"):
            self.StoredVariables["Innovation"].store( Innovation )
        if self._toStore("OMB"):
            self.StoredVariables["OMB"].store( Innovation )
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if self._toStore("OMA"):
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if self._toStore("SimulatedObservationAtBackground"):
            self.StoredVariables["SimulatedObservationAtBackground"].store( HXb )
        if self._toStore("SimulatedObservationAtOptimum"):
            self.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
