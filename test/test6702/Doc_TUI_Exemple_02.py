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
def test1():

    from numpy import array, matrix
    import adaoBuilder
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
    return case.get("Analysis")[-1]

def test2():

    from numpy import array, matrix
    import adaoBuilder
    case = adaoBuilder.New()
    case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
    case.set( 'Background',          Vector=[0, 1, 2] )
    case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
    case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
    case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
    def simulation(x):
        import numpy
        __x = numpy.matrix(numpy.ravel(numpy.matrix(x))).T
        __H = numpy.matrix("1 0 0;0 2 0;0 0 3")
        return __H * __x
    #
    case.set( 'ObservationOperator',
        OneFunction = simulation,
        Parameters  = {"DifferentialIncrement":0.01},
        )
    case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
    case.execute()
    #
    return case.get("Analysis")[-1]

def almost_equal_vectors(v1, v2):
    print "\nMaximum of differences between the two :",max(abs(v2 - v1))
    return max(abs(v2 - v1)) < 1.e-15

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    print """Exemple de la doc :

    Creation detaillee d'un cas de calcul TUI ADAO
    ++++++++++++++++++++++++++++++++++++++++++++++
    Les deux resultats sont testes pour etre identiques.
    """
    xa1 = test1()
    xa2 = test2()
    assert almost_equal_vectors( xa1, xa2 )
