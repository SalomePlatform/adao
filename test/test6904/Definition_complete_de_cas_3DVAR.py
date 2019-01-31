# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2019 EDF R&D
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
import numpy
from utExtend import assertAlmostEqualArrays

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
    __x = numpy.matrix(numpy.ravel(numpy.matrix(x))).T
    __H = numpy.matrix("1 0 0;0 2 0;0 0 3; 1 2 3")
    return __H * __x
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
class InTest(unittest.TestCase):
    def test1(self):
        print("""Exemple de la doc :

        Exploitation independante des resultats d'un cas de calcul
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
            Algorithm = '3DVAR',                  # Mots-clé réservé
            Parameters = {                        # Dictionnaire
                "Bounds":Bounds,                  # Liste de paires de Real ou de None
                "MaximumNumberOfSteps":100,       # Int >= 0
                "CostDecrementTolerance":1.e-7,   # Real > 0
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
            Vector = numpy.array(Xb),             # array, list, tuple, matrix
            Stored = True,                        # Bool
            )
        case.set( 'Observation',
            Vector = numpy.array(observations),   # array, list, tuple, matrix
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
        ecart = assertAlmostEqualArrays(Xoptimum, [ 2., 3., 4.])
        #
        print("  L'écart absolu maximal obtenu lors du test est de %.2e."%ecart)
        print("  Les résultats obtenus sont corrects.")
        print("")
        #
        return Xoptimum

# ==============================================================================
if __name__ == '__main__':
    print("\nAUTODIAGNOSTIC\n==============")
    unittest.main()
