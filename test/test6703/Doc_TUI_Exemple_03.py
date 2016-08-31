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
"Verification d'un exemple de la documentation"

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
# Observations obtenues par simulation
# ------------------------------------
observations = simulation((2, 3, 4))

# ==============================================================================
def test1():
    "Exemple"
    import numpy
    import adaoBuilder
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
            "MaximumNumberOfSteps":100,
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
        OneFunction = simulation,
        Parameters  = {"DifferentialIncrement":0.0001},
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
    print
    print "Number of internal iterations...: %i"%len(J_values)
    print "Initial state...................:",numpy.ravel(Xbackground)
    print "Optimal state...................:",numpy.ravel(Xoptimum)
    print "Simulation at optimal state.....:",numpy.ravel(FX_at_optimum)
    print
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    print """Exemple de la doc :

    Exploitation independante des resultats d'un cas de calcul
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """
    test1()
