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
"Full definition of a use case for the standard user"

import sys
import unittest
import numpy

# ==============================================================================
#
# Artificial user data example
# ----------------------------
alpha = 5.
beta = 7
gamma = 9.0
#
alphamin, alphamax = 0., 10.
betamin,  betamax  = 3, 13
gammamin, gammamax = 1.5, 15.5
#
def simulation(x):
    "Observation operator H for Y=H(X)"
    import numpy
    __x = numpy.ravel(x)
    __H = numpy.array([[1, 0, 0], [0, 2, 0], [0, 0, 3], [1, 2, 3]])
    return numpy.dot(__H,__x)
#
def multisimulation( xserie ):
    yserie = []
    for x in xserie:
        yserie.append( simulation( x ) )
    return yserie
#
# Twin experiment observations
# ----------------------------
observations = simulation((2, 3, 4))

# ==============================================================================
class Test_Adao(unittest.TestCase):
    def test1(self):
        print("""
        Full definition of a use case for the standard user
        +++++++++++++++++++++++++++++++++++++++++++++++++++
        """)
        #
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
        case.set( 'AlgorithmParameters',
            Algorithm = 'Blue',                   # Mots-clé réservé
            Parameters = {                        # Dictionnaire
                "StoreSupplementaryCalculations":[# Liste de mots-clés réservés
                    "CostFunctionJAtCurrentOptimum",
                    "CostFunctionJoAtCurrentOptimum",
                    "CurrentOptimum",
                    "SimulatedObservationAtCurrentOptimum",
                    "SimulatedObservationAtOptimum",
                    ],
                }
            )
        case.set( 'Background',
            Vector = Xb,                          # array, list, tuple, matrix
            Stored = True,                        # Bool
            )
        case.set( 'Observation',
            Vector = observations,                # array, list, tuple, matrix
            Stored = False,                       # Bool
            )
        case.set( 'BackgroundError',
            Matrix = None,                        # None ou matrice carrée
            ScalarSparseMatrix = 1.0e10,          # None ou Real > 0
            DiagonalSparseMatrix = None,          # None ou vecteur
            )
        case.set( 'ObservationError',
            Matrix = None,                        # None ou matrice carrée
            ScalarSparseMatrix = 1.0,             # None ou Real > 0
            DiagonalSparseMatrix = None,          # None ou vecteur
            )
        case.set( 'ObservationOperator',
            OneFunction = multisimulation,        # MultiFonction [Y] = F([X])
            Parameters  = {                       # Dictionnaire
                "DifferentialIncrement":0.0001,   # Real > 0
                "CenteredFiniteDifference":False, # Bool
                },
            InputFunctionAsMulti = True,          # Bool
            )
        case.set( 'Observer',
            Variable = "CurrentState",            # Mot-clé
            Template = "ValuePrinter",            # Mot-clé
            String   = None,                      # None ou code Python
            Info     = None,                      # None ou string

            )
        case.execute()
        #
        # Exploitation independante
        # -------------------------
        Xbackground   = case.get("Background")
        Xoptimum      = case.get("Analysis")[-1]
        FX_at_optimum = case.get("SimulatedObservationAtOptimum")[-1]
        J_values      = case.get("CostFunctionJAtCurrentOptimum")[:]
        print("")
        print("Number of internal iterations...: %i"%len(J_values))
        print("Initial state...................: %s"%(numpy.ravel(Xbackground),))
        print("Optimal state...................: %s"%(numpy.ravel(Xoptimum),))
        print("Simulation at optimal state.....: %s"%(numpy.ravel(FX_at_optimum),))
        print("")
        #
        # Fin du cas
        # ----------
        ecart = assertAlmostEqualArrays(Xoptimum, [ 2., 3., 4.])
        #
        print("The maximal absolute error in the test is of %.2e."%ecart)
        print("The results are correct.")
        print("")
        #
        #  return Xoptimum

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
if __name__ == '__main__':
    print("\nAUTODIAGNOSTIC\n==============")
    sys.stderr = sys.stdout
    unittest.main(verbosity=2)
