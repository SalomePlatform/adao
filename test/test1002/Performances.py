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
"Test de fonctionnement et de performances de Numpy et Scipy"

# ==============================================================================
import numpy, time
numpy.set_printoptions(precision=5)

def testSysteme():
    print("  Les caracteristiques des applications et outils systeme :")
    import sys ; v=sys.version.split() ; print("    - Python systeme....: %s"%v[0])
    import numpy ; print("    - Numpy.............: %s"%numpy.version.version)
    try:
        import scipy ; print("    - Scipy.............: %s"%scipy.version.version)
    except:
        print("    - Scipy.............: %s"%("absent",))
    try:
        import numpy.distutils.system_info as sysinfo ; la = sysinfo.get_info('lapack') ; print("    - Lapack............: %s/lib%s.so"%(la['library_dirs'][0],la['libraries'][0]))
    except:
        print("    - Lapack............: %s"%("absent",))
    print("")
    return True

def testNumpy01(dimension = 3, precision = 1.e-17, repetitions = 10):
    "Test Numpy"
    __d = int(dimension)
    print("    Taille du test..................................: %.0e"%__d)
    t_init = time.time()
    A = numpy.array([numpy.arange(dimension)+1.,]*__d)
    x = numpy.arange(__d)+1.
    print("    La duree elapsed moyenne de l'initialisation est: %4.1f s"%(time.time()-t_init))
    #
    t_init = time.time()
    for i in range(repetitions):
        b = numpy.dot(A,x)
    print("    La duree elapsed pour %3i produits est de.......: %4.1f s"%(repetitions, time.time()-t_init))
    r = [__d*(__d+1.)*(2.*__d+1.)/6.,]*__d
    if max(abs(b-r)) > precision:
        raise ValueError("Resultat du test errone (1)")
    else:
        print("    Test correct, erreur maximale inferieure a %s"%precision)
    print("")
    del A, x, b

def testNumpy02(dimension = 3, precision = 1.e-17, repetitions = 100):
    "Test Numpy"
    __d = int(dimension)
    print("    Taille du test..................................: %.0e"%__d)
    t_init = time.time()
    A = numpy.random.normal(0.,1.,size=(__d,__d))
    x = numpy.random.normal(0.,1.,size=(__d,))
    print("    La duree elapsed moyenne de l'initialisation est: %4.1f s"%(time.time()-t_init))
    #
    t_init = time.time()
    for i in range(repetitions):
        b = numpy.dot(A,x)
    print("    La duree elapsed pour %3i produits est de.......: %4.1f s"%(repetitions, time.time()-t_init))
    print("")
    del A, x, b

# ==============================================================================
if __name__ == "__main__":
    print('\nAUTODIAGNOSTIC\n')
    testSysteme()
    numpy.random.seed(1000)
    testNumpy01(dimension = 1.e4)
    testNumpy02(dimension = 3.e3)
    print("")
