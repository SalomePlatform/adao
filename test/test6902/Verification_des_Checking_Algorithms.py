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

import sys
import unittest
import numpy
from adao import adaoBuilder

# ==============================================================================
class Test_Adao(unittest.TestCase):
    def test1(self):
        for algo in ("AdjointTest", "FunctionTest", "GradientTest", "LinearityTest", "TangentTest"):
            print("")
            msg = "Algorithme en test : %s"%algo
            print(msg+"\n"+"-"*len(msg))
            #
            adaopy = adaoBuilder.New()
            adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"EpsilonMinimumExponent":-10,"NumberOfRepetition":2, "SetSeed":1000})
            adaopy.setCheckingPoint      (Vector = [0,1,2])
            adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
            adaopy.setObservation        (Vector = [0.5,1.5,2.5])
            adaopy.setObservationError   (DiagonalSparseMatrix = "1 1 1")
            adaopy.setObservationOperator(Matrix = "1 0 0;0 2 0;0 0 3")
            adaopy.execute()
            del adaopy
        #
        for algo in ("ObserverTest", ):
            print("")
            msg = "Algorithme en test : %s"%algo
            print(msg+"\n"+"-"*len(msg))
            #
            adaopy = adaoBuilder.New()
            adaopy.setAlgorithmParameters(Algorithm=algo)
            adaopy.setCheckingPoint      (Vector = [0,1,2])
            adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
            adaopy.setObservation        (Vector = [0.5,1.5,2.5])
            adaopy.setObservationError   (DiagonalSparseMatrix = "1 1 1")
            adaopy.setObservationOperator(Matrix = "1 0 0;0 2 0;0 0 3")
            adaopy.setObserver("Analysis",Template="ValuePrinter")
            adaopy.execute()
            del adaopy
        #
        for algo in ("SamplingTest", ):
            print("")
            msg = "Algorithme en test : %s"%algo
            print(msg+"\n"+"-"*len(msg))
            #
            adaopy = adaoBuilder.New()
            adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={
                "StoreSupplementaryCalculations":["CostFunctionJ","CurrentState",],
                "SampleAsMinMaxStepHyperCube":[[-1.,1.,1.],[0,2,1],[1,3,1]],
                })
            adaopy.setCheckingPoint      (Vector = [0,1,2])
            adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
            adaopy.setObservation        (Vector = [0.5,1.5,2.5])
            adaopy.setObservationError   (DiagonalSparseMatrix = "1 1 1")
            adaopy.setObservationOperator(Matrix = "1 0 0;0 2 0;0 0 3")
            adaopy.setObserver           ("CurrentState",Template="ValuePrinter")
            adaopy.execute()
            del adaopy
        #
        for algo in ("AdjointTest", "FunctionTest", "GradientTest", "LinearityTest", "TangentTest"):
            print("")
            msg = "Algorithme en test : %s"%algo
            print(msg+"\n"+"-"*len(msg))
            #
            def simulation( arguments ):
                _X = arguments
                X = numpy.ravel( _X )
                H = numpy.array([[1,0,0],[0,2,0],[0,0,3],[1,2,3]])
                return numpy.dot(H,X)
            #
            adaopy = adaoBuilder.New()
            adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"EpsilonMinimumExponent":-10,"NumberOfRepetition":2, "SetSeed":1000})
            adaopy.setCheckingPoint      (Vector = [0,1,2])
            adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
            adaopy.setObservationOperator(OneFunction = simulation)
            adaopy.execute()
            del adaopy

#===============================================================================
if __name__ == "__main__":
    print("\nAUTODIAGNOSTIC\n==============")
    sys.stderr = sys.stdout
    unittest.main(verbosity=2)
