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
"Verification de la disponibilite de l'ensemble des algorithmes"

# ==============================================================================
import adaoBuilder, numpy
def test1():
    """Verification de la disponibilite de l'ensemble des algorithmes"""
    Xa = {}
    for algo in ("3DVAR", "Blue", "ExtendedBlue", "LinearLeastSquares", "NonLinearLeastSquares", ):
        print
        msg = "Algorithme en test : %s"%algo
        print msg+"\n"+"="*len(msg)
        #
        adaopy = adaoBuilder.New()
        adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"EpsilonMinimumExponent":-10, })
        adaopy.setBackground         (Vector = [0,1,2])
        adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
        adaopy.setObservation        (Vector = [0.5,1.5,2.5])
        adaopy.setObservationError   (DiagonalSparseMatrix = "1 1 1")
        adaopy.setObservationOperator(Matrix = "1 0 0;0 2 0;0 0 3")
        adaopy.setObserver("Analysis",Template="ValuePrinter")
        adaopy.execute()
        Xa[algo] = adaopy.get("Analysis")[-1]
        del adaopy
    #
    for algo in ("ExtendedKalmanFilter", "KalmanFilter", "UnscentedKalmanFilter", "4DVAR"):
        print
        msg = "Algorithme en test : %s"%algo
        print msg+"\n"+"="*len(msg)
        #
        adaopy = adaoBuilder.New()
        adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"EpsilonMinimumExponent":-10, })
        adaopy.setBackground         (Vector = [0,1,2])
        adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
        adaopy.setObservation        (Vector = [0.5,1.5,2.5])
        adaopy.setObservationError   (DiagonalSparseMatrix = "1 1 1")
        adaopy.setObservationOperator(Matrix = "1 0 0;0 1 0;0 0 1")
        adaopy.setEvolutionModel     (Matrix = "1 0 0;0 1 0;0 0 1")
        adaopy.setEvolutionError     (ScalarSparseMatrix = 1.)
        adaopy.setObserver("Analysis",Template="ValuePrinter")
        adaopy.execute()
        Xa[algo] = adaopy.get("Analysis")[-1]
        del adaopy
    #
    for algo in ("ParticleSwarmOptimization", "QuantileRegression", ):
        print
        msg = "Algorithme en test : %s"%algo
        print msg+"\n"+"="*len(msg)
        #
        adaopy = adaoBuilder.New()
        adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"BoxBounds":3*[[-1,3]], "SetSeed":1000, })
        adaopy.setBackground         (Vector = [0,1,2])
        adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
        adaopy.setObservation        (Vector = [0.5,1.5,2.5])
        adaopy.setObservationError   (DiagonalSparseMatrix = "1 1 1")
        adaopy.setObservationOperator(Matrix = "1 0 0;0 1 0;0 0 1")
        adaopy.setEvolutionModel     (Matrix = "1 0 0;0 1 0;0 0 1")
        adaopy.setEvolutionError     (ScalarSparseMatrix = 1.)
        adaopy.setObserver("Analysis",Template="ValuePrinter")
        adaopy.execute()
        Xa[algo] = adaopy.get("Analysis")[-1]
        del adaopy
    #
    for algo in ("EnsembleBlue", ):
        print
        msg = "Algorithme en test : %s"%algo
        print msg+"\n"+"="*len(msg)
        #
        adaopy = adaoBuilder.New()
        adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"SetSeed":1000, })
        adaopy.setBackground         (VectorSerie = 100*[[0,1,2]])
        adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
        adaopy.setObservation        (Vector = [0.5,1.5,2.5])
        adaopy.setObservationError   (DiagonalSparseMatrix = "1 1 1")
        adaopy.setObservationOperator(Matrix = "1 0 0;0 1 0;0 0 1")
        adaopy.setEvolutionModel     (Matrix = "1 0 0;0 1 0;0 0 1")
        adaopy.setEvolutionError     (ScalarSparseMatrix = 1.)
        adaopy.setObserver("Analysis",Template="ValuePrinter")
        adaopy.execute()
        del adaopy
    #
    print
    msg = "Tests des ecarts"
    print msg+"\n"+"="*len(msg)
    verify_similarity_of_algo_results(("3DVAR", "Blue", "ExtendedBlue"), Xa)
    verify_similarity_of_algo_results(("LinearLeastSquares", "NonLinearLeastSquares"), Xa)
    verify_similarity_of_algo_results(("ExtendedKalmanFilter", "KalmanFilter", "UnscentedKalmanFilter"), Xa)
    print
    #
    return 0

def almost_equal_vectors(v1, v2, precision = 1.e-15, msg = ""):
    """Comparaison de deux vecteurs"""
    print "  Difference maximale %s: %.2e"%(msg, max(abs(v2 - v1)))
    return max(abs(v2 - v1)) < precision

def verify_similarity_of_algo_results(serie = [], Xa = {}):
    print "Camparaisons :"
    for algo1 in serie:
        for algo2 in serie:
            if algo1 is algo2: break
            assert almost_equal_vectors( Xa[algo1], Xa[algo2], 1.e-5, "entre %s et %s "%(algo1, algo2) )
    print "Algorithmes dont les resultats sont similaires : %s\n"%(serie,)

#===============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    test1()
