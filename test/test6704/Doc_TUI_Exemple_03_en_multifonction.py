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
#
# Construction artificielle d'un exemple de donnees utilisateur
# -------------------------------------------------------------
alpha = 5.
beta = 7
gamma = 9.0
#
alphamin, alphamax = 0., 10.
betamin,  betamax  = 3, 13
gammamin, gammamax = 1.5, 15.5
#
def simulation(x):
    "Fonction de simulation H pour effectuer Y=H(X)"
    import numpy
    __x = numpy.ravel(x)
    __H = numpy.array([[1,0,0],[0,2,0],[0,0,3],[1,2,3]])
    return __H @ __x
#
def multisimulation( xserie ):
    yserie = []
    for x in xserie:
        yserie.append( simulation( x ) )
    return yserie
#
# Observations obtenues par simulation
# ------------------------------------
observations = simulation((2, 3, 4))

# ==============================================================================
class Test_Adao(unittest.TestCase):
    def test1(self):
        "Test"
        print("""Exemple de la doc :

        Exploitation independante des resultats d'un cas de calcul
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        """)
        #---------------------------------------------------------------------------
        import numpy
        from adao import adaoBuilder
        #
        # Mise en forme des entrees
        # -------------------------
        Xb = (alpha, beta, gamma)
        Bounds = (
            (alphamin, alphamax),
            (betamin,  betamax ),
            (gammamin, gammamax))
        #
        # TUI ADAO
        # --------
        case = adaoBuilder.New()
        case.set(
            'AlgorithmParameters',
            Algorithm = '3DVAR',
            Parameters = {
                "Bounds":Bounds,
                "MaximumNumberOfIterations":100,
                "StoreSupplementaryCalculations":[
                    "CostFunctionJ",
                    "CurrentState",
                    "SimulatedObservationAtOptimum",
                    ],
                }
            )
        case.set( 'Background', Vector = numpy.array(Xb), Stored = True )
        case.set( 'Observation', Vector = numpy.array(observations) )
        case.set( 'BackgroundError', ScalarSparseMatrix = 1.0e10 )
        case.set( 'ObservationError', ScalarSparseMatrix = 1.0 )
        case.set(
            'ObservationOperator',
            OneFunction = multisimulation,
            Parameters  = {"DifferentialIncrement":0.0001},
            InputFunctionAsMulti = True,
            )
        case.set( 'Observer', Variable="CurrentState", Template="ValuePrinter" )
        case.execute()
        #
        # Exploitation independante
        # -------------------------
        Xbackground   = case.get("Background")
        Xoptimum      = case.get("Analysis")[-1]
        FX_at_optimum = case.get("SimulatedObservationAtOptimum")[-1]
        J_values      = case.get("CostFunctionJ")[:]
        print("")
        print("Number of internal iterations...: %i"%len(J_values))
        print("Initial state...................: %s"%(numpy.ravel(Xbackground),))
        print("Optimal state...................: %s"%(numpy.ravel(Xoptimum),))
        print("Simulation at optimal state.....: %s"%(numpy.ravel(FX_at_optimum),))
        print("")
        #
        #---------------------------------------------------------------------------
        xa = case.get("Analysis")[-1]
        ecart = assertAlmostEqualArrays(xa, [ 2., 3., 4.])
        #
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
