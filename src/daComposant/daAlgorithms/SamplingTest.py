# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2023 EDF R&D
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

import numpy, logging, itertools
from daCore import BasicObjects, NumericObjects
from daCore.PlatformInfo import PlatformInfo
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "SAMPLINGTEST")
        self.defineRequiredParameter(
            name     = "SampleAsnUplet",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par une liste de n-uplet",
            )
        self.defineRequiredParameter(
            name     = "SampleAsExplicitHyperCube",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonnages de chaque variable comme une liste",
            )
        self.defineRequiredParameter(
            name     = "SampleAsMinMaxStepHyperCube",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonnages de chaque variable par un triplet [min,max,step]",
            )
        self.defineRequiredParameter(
            name     = "SampleAsIndependantRandomVariables",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont les points sur chaque axe proviennent de l'échantillonnage indépendant de la variable selon la spécification ['distribution',[parametres],nombre]",
            )
        self.defineRequiredParameter(
            name     = "QualityCriterion",
            default  = "AugmentedWeightedLeastSquares",
            typecast = str,
            message  = "Critère de qualité utilisé",
            listval  = [
                "DA",
                "AugmentedWeightedLeastSquares", "AWLS",
                "WeightedLeastSquares","WLS",
                "LeastSquares", "LS", "L2",
                "AbsoluteValue", "L1",
                "MaximumError", "ME", "Linf",
                ],
            listadv  = [
                "AugmentedPonderatedLeastSquares", "APLS",
                "PonderatedLeastSquares", "PLS",
                ],
            )
        self.defineRequiredParameter(
            name     = "SetDebug",
            default  = False,
            typecast = bool,
            message  = "Activation du mode debug lors de l'exécution",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "CurrentState",
                "InnovationAtCurrentState",
                "SimulatedObservationAtCurrentState",
                ]
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "HO"),
            )
        self.setAttributes(tags=(
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        Hm = HO["Direct"].appliedTo
        #
        X0 = numpy.ravel( Xb )
        Y0 = numpy.ravel( Y  )
        #
        # ---------------------------
        sampleList = NumericObjects.BuildComplexSampleList(
            self._parameters["SampleAsnUplet"],
            self._parameters["SampleAsExplicitHyperCube"],
            self._parameters["SampleAsMinMaxStepHyperCube"],
            self._parameters["SampleAsIndependantRandomVariables"],
            X0,
            )
        # ----------
        BI = B.getI()
        RI = R.getI()
        def CostFunction(x, HmX, QualityMeasure="AugmentedWeightedLeastSquares"):
            if numpy.any(numpy.isnan(HmX)):
                _X  = numpy.nan
                _HX = numpy.nan
                Jb, Jo, J = numpy.nan, numpy.nan, numpy.nan
            else:
                _X  = numpy.ravel( x )
                _HX = numpy.ravel( HmX )
                if QualityMeasure in ["AugmentedWeightedLeastSquares","AWLS","AugmentedPonderatedLeastSquares","APLS","DA"]:
                    if BI is None or RI is None:
                        raise ValueError("Background and Observation error covariance matrix has to be properly defined!")
                    Jb  = float( 0.5 *  (_X - X0).T * (BI * (_X - X0))  )
                    Jo  = float( 0.5 * (Y0 - _HX).T * (RI * (Y0 - _HX)) )
                elif QualityMeasure in ["WeightedLeastSquares","WLS","PonderatedLeastSquares","PLS"]:
                    if RI is None:
                        raise ValueError("Observation error covariance matrix has to be properly defined!")
                    Jb  = 0.
                    Jo  = float( 0.5 * (Y0 - _HX).T * (RI * (Y0 - _HX)) )
                elif QualityMeasure in ["LeastSquares","LS","L2"]:
                    Jb  = 0.
                    Jo  = float( 0.5 * (Y0 - _HX).T @ (Y0 - _HX) )
                elif QualityMeasure in ["AbsoluteValue","L1"]:
                    Jb  = 0.
                    Jo  = float( numpy.sum( numpy.abs(Y0 - _HX), dtype=mfp ) )
                elif QualityMeasure in ["MaximumError","ME", "Linf"]:
                    Jb  = 0.
                    Jo  = numpy.max( numpy.abs(Y0 - _HX) )
                #
                J   = Jb + Jo
            if self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( _X )
            if self._toStore("InnovationAtCurrentState"):
                self.StoredVariables["InnovationAtCurrentState"].store( Y0 - _HX )
            if self._toStore("SimulatedObservationAtCurrentState"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            return J, Jb, Jo
        # ----------
        if self._parameters["SetDebug"]:
            CUR_LEVEL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.DEBUG)
            print("===> Beginning of evaluation, activating debug\n")
            print("     %s\n"%("-"*75,))
        #
        # ----------
        for i,Xx in enumerate(sampleList):
            if self._parameters["SetDebug"]:
                print("===> Launching evaluation for state %i"%i)
            try:
                Yy = Hm( numpy.ravel( Xx ) )
            except:
                Yy = numpy.nan
            #
            J, Jb, Jo = CostFunction( Xx, Yy,  self._parameters["QualityCriterion"])
        # ----------
        #
        if self._parameters["SetDebug"]:
            print("\n     %s\n"%("-"*75,))
            print("===> End evaluation, deactivating debug if necessary\n")
            logging.getLogger().setLevel(CUR_LEVEL)
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
