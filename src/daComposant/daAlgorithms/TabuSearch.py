#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2016 EDF R&D
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
            message  = "Graine fix�e pour le g�n�rateur al�atoire",
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
            message  = "Nombre de perturbations �l�mentaires pour choisir une perturbation d'�tat",
            minval   = 1,
            )
        self.defineRequiredParameter(
            name     = "NoiseDistribution",
            default  = "Uniform",
            typecast = str,
            message  = "Distribution pour g�n�rer les perturbations d'�tat",
            listval  = ["Gaussian","Uniform"],
            )
        self.defineRequiredParameter(
            name     = "QualityCriterion",
            default  = "AugmentedWeightedLeastSquares",
            typecast = str,
            message  = "Crit�re de qualit� utilis�",
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
            message  = "Demi-amplitude des perturbations uniformes centr�es d'�tat pour chaque composante de l'�tat",
            )
        self.defineRequiredParameter(
            name     = "StandardDeviation",
            default  = [],
            typecast = numpy.matrix,
            message  = "Ecart-type des perturbations gaussiennes d'�tat pour chaque composante de l'�tat",
            )
        self.defineRequiredParameter(
            name     = "NoiseAddingProbability",
            default  = 1.,
            typecast = float,
            message  = "Probabilit� de perturbation d'une composante de l'�tat",
            minval   = 0.,
            maxval   = 1.,
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou interm�diaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs suppl�mentaires � stocker et/ou effectuer",
            listval  = ["BMA", "OMA", "OMB", "CurrentState", "CostFunctionJ", "Innovation", "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        if self._parameters.has_key("Bounds") and (type(self._parameters["Bounds"]) is type([]) or type(self._parameters["Bounds"]) is type(())) and (len(self._parameters["Bounds"]) > 0):
            Bounds = self._parameters["Bounds"]
            logging.debug("%s Prise en compte des bornes effectuee"%(self._name,))
        else:
            Bounds = None
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
        # Op�rateur d'observation
        # -----------------------
        Hm = HO["Direct"].appliedTo
        #
        # Pr�calcul des inversions de B et R
        # ----------------------------------
        BI = B.getI()
        RI = R.getI()
        #
        # D�finition de la fonction de deplacement
        # ----------------------------------------
        def Tweak( x, NoiseDistribution, NoiseAddingProbability ):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            if NoiseDistribution == "Uniform":
                for i in xrange(_X.size):
                    if NoiseAddingProbability >= numpy.random.uniform():
                        _increment = numpy.random.uniform(low=-nrange[i], high=nrange[i])
                        # On ne traite pas encore le d�passement des bornes ici
                        _X[i] += _increment
            elif NoiseDistribution == "Gaussian":
                for i in xrange(_X.size):
                    if NoiseAddingProbability >= numpy.random.uniform():
                        _increment = numpy.random.normal(loc=0., scale=sigma[i])
                        # On ne traite pas encore le d�passement des bornes ici
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
            if _xInList: sys.exit()
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
                #�_qualityW = CostFunction( _W, self._parameters["QualityCriterion"] )
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
            if self._parameters["StoreInternalVariables"] or "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentState"].store( _Best )
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
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
        if "Innovation"                       in self._parameters["StoreSupplementaryCalculations"] or \
           "OMB"                              in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulatedObservationAtBackground" in self._parameters["StoreSupplementaryCalculations"]:
            HXb = Hm(Xb)
            d = Y - HXb
        if "OMA"                           in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            HXa = Hm(Xa)
        #
        # Calculs et/ou stockages suppl�mentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if "SimulatedObservationAtBackground" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
        if "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
