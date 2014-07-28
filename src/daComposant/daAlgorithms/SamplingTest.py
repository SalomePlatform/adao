#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2014 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects
import numpy, copy, itertools

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "SAMPLINGTEST")
        self.defineRequiredParameter(
            name     = "SampleAsnUplet",
            default  = [],
            typecast = list,
            message  = "Points de calcul définis par une liste de n-uplet",
            )
        self.defineRequiredParameter(
            name     = "SampleAsExplicitHyperCube",
            default  = [],
            typecast = list,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonages de chaque variable comme une liste",
            )
        self.defineRequiredParameter(
            name     = "SampleAsMinMaxStepHyperCube",
            default  = [],
            typecast = list,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonages de chaque variable par un triplet [min,max,step]",
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
            listval  = ["CostFunctionJ","CurrentState","Innovation","ObservedState"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        self.setParameters(Parameters)
        #
        Hm = HO["Direct"].appliedTo
        #
        Xn = copy.copy( Xb )
        #
        # ---------------------------
        if len(self._parameters["SampleAsnUplet"]) > 0:
            sampleList = self._parameters["SampleAsnUplet"]
            for i,Xx in enumerate(sampleList):
                if numpy.ravel(Xx).size != Xn.size:
                    raise ValueError("The size %i of the %ith state X in the sample and %i of the checking point Xb are different, they have to be identical."%(numpy.ravel(Xx).size,i+1,Xn.size))
        elif len(self._parameters["SampleAsExplicitHyperCube"]) > 0:
            sampleList = itertools.product(*list(self._parameters["SampleAsExplicitHyperCube"]))
        elif len(self._parameters["SampleAsMinMaxStepHyperCube"]) > 0:
            coordinatesList = []
            for i,dim in enumerate(self._parameters["SampleAsMinMaxStepHyperCube"]):
                if len(dim) != 3:
                    raise ValueError("For dimension %i, the variable definition %s is incorrect, it should be [min,max,step]."%(i,dim))
                else:
                    coordinatesList.append(numpy.linspace(*dim))
            sampleList = itertools.product(*coordinatesList)
        else:
            sampleList = iter([Xn,])
        # ----------
        BI = B.getI()
        RI = R.getI()
        def CostFunction(x,HmX):
            if numpy.any(numpy.isnan(HmX)):
                _X  = numpy.nan
                _HX = numpy.nan
                Jb, Jo, J = numpy.nan, numpy.nan, numpy.nan
            else:
                _X  = numpy.asmatrix(numpy.ravel( x )).T
                _HX = numpy.asmatrix(numpy.ravel( HmX )).T
                Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
                Jo  = 0.5 * (Y - _HX).T * RI * (Y - _HX)
                J   = float( Jb ) + float( Jo )
            if "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentState"].store( _X )
            if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["Innovation"].store( Y - _HX )
            if "ObservedState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["ObservedState"].store( _HX )
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
            __Xn = numpy.asmatrix(numpy.ravel( Xx )).T
            try:
                Yn = Hm( __Xn )
            except:
                Yn = numpy.nan
            #
            J, Jb, Jo = CostFunction(__Xn,Yn)
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
    print '\n AUTODIAGNOSTIC \n'
