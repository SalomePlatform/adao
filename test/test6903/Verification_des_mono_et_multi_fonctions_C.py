# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2018 EDF R&D
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
"Verification du fonctionnement correct d'entrees en mono ou multi-fonctions"

# ==============================================================================
import numpy, sys
from adao import adaoBuilder

M = numpy.matrix("1 0 0;0 2 0;0 0 3")
def MonoFonction( x ):
    return M * numpy.asmatrix(numpy.ravel( x )).T

def MultiFonction( xserie ):
    _mulHX = []
    for _subX in xserie:
        _mulHX.append( M * numpy.asmatrix(numpy.ravel( _subX )).T )
    return _mulHX

# ==============================================================================
def test1():
    """
    Verification du fonctionnement identique pour les algorithmes autres
    en utilisant une fonction lineaire et carree
    """
    print(test1.__doc__)
    Xa = {}
    #
    for algo in ("ParticleSwarmOptimization", "QuantileRegression", ):
        print("")
        msg = "Algorithme en test en MonoFonction : %s"%algo
        print(msg+"\n"+"-"*len(msg))
        #
        adaopy = adaoBuilder.New()
        adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"BoxBounds":3*[[-1,3]], "SetSeed":1000})
        adaopy.setBackground         (Vector = [0,1,2])
        adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
        adaopy.setObservation        (Vector = [0.5,1.5,2.5])
        adaopy.setObservationError   (DiagonalSparseMatrix = "1 2 3")
        adaopy.setObservationOperator(OneFunction = MonoFonction)
        adaopy.setObserver("Analysis",Template="ValuePrinter")
        adaopy.execute()
        Xa["Mono/"+algo] = adaopy.get("Analysis")[-1]
        del adaopy
    #
    for algo in ("ParticleSwarmOptimization", "QuantileRegression", ):
        print("")
        msg = "Algorithme en test en MultiFonction : %s"%algo
        print(msg+"\n"+"-"*len(msg))
        #
        adaopy = adaoBuilder.New()
        adaopy.setAlgorithmParameters(Algorithm=algo, Parameters={"BoxBounds":3*[[-1,3]], "SetSeed":1000})
        adaopy.setBackground         (Vector = [0,1,2])
        adaopy.setBackgroundError    (ScalarSparseMatrix = 1.)
        adaopy.setObservation        (Vector = [0.5,1.5,2.5])
        adaopy.setObservationError   (DiagonalSparseMatrix = "1 2 3")
        adaopy.setObservationOperator(OneFunction = MultiFonction, InputAsMF = True)
        adaopy.setObserver("Analysis",Template="ValuePrinter")
        adaopy.execute()
        Xa["Multi/"+algo] = adaopy.get("Analysis")[-1]
        del adaopy
    #
    print("")
    msg = "Tests des ecarts attendus :"
    print(msg+"\n"+"="*len(msg))
    for algo in ("ParticleSwarmOptimization", "QuantileRegression"):
        verify_similarity_of_algo_results(("Multi/"+algo, "Mono/"+algo), Xa, 1.e-20)
    print("  Les resultats obtenus sont corrects.")
    print("")
    #
    return 0

# ==============================================================================
def almost_equal_vectors(v1, v2, precision = 1.e-15, msg = ""):
    """Comparaison de deux vecteurs"""
    print("    Difference maximale %s: %.2e"%(msg, max(abs(v2 - v1))))
    return max(abs(v2 - v1)) < precision

def verify_similarity_of_algo_results(serie = [], Xa = {}, precision = 1.e-15):
    print("  Comparaisons :")
    for algo1 in serie:
        for algo2 in serie:
            if algo1 is algo2: break
            assert almost_equal_vectors( Xa[algo1], Xa[algo2], precision, "entre %s et %s "%(algo1, algo2) )
    print("  Algorithmes dont les resultats sont similaires a %.0e : %s\n"%(precision, serie,))
    sys.stdout.flush()

#===============================================================================
if __name__ == "__main__":
    print('\nAUTODIAGNOSTIC\n')
    test1()
