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
"Verification d'un exemple de la documentation"

import sys, os, tempfile
import unittest

# ==============================================================================
class Test_Adao(unittest.TestCase):
    def test1(self):
        """Test"""
        from numpy import array, matrix
        from adao import adaoBuilder
        #-----------------------------------------------------------------------
        # Analyse avec les paramètres de casse correcte
        print("\nCase 1")
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'AlgorithmParameters',
            Algorithm = '3DVAR',
            Parameters = {
                "Minimizer":"CG",
                "MaximumNumberOfIterations":3,
                "CostDecrementTolerance":1.e-2,
                "SetSeed":1234567,
                "StoreSupplementaryCalculations":[
                    "CostFunctionJAtCurrentOptimum",
                    "SimulatedObservationAtCurrentOptimum",
                    ],
                }
            )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
        case.set( 'Observer',            Variable="CostFunctionJAtCurrentOptimum", Template="ValuePrinter" )
        case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
        case.execute()
        xa1 = case.get("Analysis")[-1]
        del case
        #
        #-----------------------------------------------------------------------
        # Analyse avec les paramètres de casse quelconque
        print("\nCase 2")
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters',
            Algorithm = '3DVAR',
            Parameters = {
                "MINIMIZER":"CG",
                "MaximumNumberOfIterations":3,
                "COSTDecrementTOLERANCE":1.e-2,
                "STORESUPPLEMENTARYCALCULATIONS":[
                    "CostFunctionJAtCurrentOptimum",
                    "SimulatedObservationAtCurrentOptimum",
                    ],
                }
            )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
        case.set( 'Observer',            Variable="CostFunctionJAtCurrentOptimum", Template="ValuePrinter" )
        case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
        case.execute()
        xa2 = case.get("Analysis")[-1]
        del case
        #
        #-----------------------------------------------------------------------
        ecart = assertAlmostEqualArrays(xa1, xa2, places = 15)
        #
        print("\nTest correct")

# ==============================================================================
def filesize(name):
    statinfo = os.stat(name)
    return statinfo.st_size # Bytes

def assertAlmostEqualArrays(first, second, places=7, msg=None, delta=None):
    "Compare two vectors, like unittest.assertAlmostEqual"
    import numpy
    if msg is not None:
        print(msg)
    if delta is not None:
        if ( numpy.abs(numpy.asarray(first) - numpy.asarray(second)) > float(delta) ).any():
            raise AssertionError("%s != %s within %s places"%(first,second,delta))
    else:
        if ( numpy.abs(numpy.asarray(first) - numpy.asarray(second)) > 10**(-int(places)) ).any():
            raise AssertionError("%s != %s within %i places"%(first,second,places))
    return max(abs(numpy.asarray(first) - numpy.asarray(second)))

# ==============================================================================
if __name__ == "__main__":
    print('\nAUTODIAGNOSTIC\n')
    sys.stderr = sys.stdout
    unittest.main(verbosity=2)
