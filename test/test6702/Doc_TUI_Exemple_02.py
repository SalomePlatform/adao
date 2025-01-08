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

import sys
import unittest

# ==============================================================================
class Test_Adao(unittest.TestCase):
    results = []
    def test1(self):
        """Test"""
        print("""Exemple de la doc :

        Creation detaillee d'un cas de calcul TUI ADAO
        ++++++++++++++++++++++++++++++++++++++++++++++
        Les deux resultats sont testes pour etre identiques.
        """)
        from numpy import array
        from adao import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
        case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
        case.execute()
        #
        xa = case.get("Analysis")[-1]
        Test_Adao.results.append( xa )

    def test2(self):
        """Test"""
        from numpy import array
        from adao import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        def simulation(x):
            import numpy
            __x = numpy.ravel(x)
            __H = numpy.diag([1.,2.,3.])
            return __H @ __x
        #
        case.set( 'ObservationOperator',
            OneFunction = simulation,
            Parameters  = {"DifferentialIncrement":0.01},
            )
        case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
        case.execute()
        #
        xa = case.get("Analysis")[-1]
        Test_Adao.results.append( xa )

    def test3(self):
        """Test"""
        xa2 = Test_Adao.results.pop()
        xa1 = Test_Adao.results.pop()
        ecart = assertAlmostEqualArrays(xa1, xa2, places = 15)
        print("")
        print("  L'écart absolu maximal obtenu lors du test est de %.2e."%ecart)
        print("  Les résultats obtenus sont corrects.")
        print("")

# ==============================================================================
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
