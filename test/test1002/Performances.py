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
"Test de fonctionnement et de performances de Numpy et Scipy"

import sys
import time
import unittest
import numpy
import scipy
numpy.set_printoptions(precision=5)

# ==============================================================================
class Test_Adao(unittest.TestCase):
    def test1_Systeme(self):
        "Test Système"
        print()
        print("  %s"%self.test1_Systeme.__doc__)
        print("    Les caracteristiques des applications et outils systeme :")
        import sys ; v=sys.version.split() ; print("    - Python systeme....: %s"%v[0])
        import numpy ; print("    - Numpy.............: %s"%numpy.version.version)
        try:
            import scipy ; print("    - Scipy.............: %s"%scipy.version.version)
        except:
            print("    - Scipy.............: %s"%("absent",))
        if tuple(map(int,numpy.version.version.split("."))) < (1,23,0):
            import numpy.distutils.system_info as sysinfo
            la = sysinfo.get_info('lapack')
            if 'libraries' in la:
                print('    - Lapack............: %s/lib%s.so'%(la['library_dirs'][0],la['libraries'][0]))
            else:
                print('    - Lapack............: absent')
        else:
            print('    - Lapack............: numpy n\'indique plus où le trouver')
        print("")

    #~ @unittest.skip("Debug")
    def test_Numpy01(self, dimension = 10000, precision = 1.e-17, repetitions = 10):
        "Test Numpy"
        __d = int(dimension)
        print("  %s"%self.test_Numpy01.__doc__)
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

    #~ @unittest.skip("Debug")
    def test_Numpy02(self, dimension = 3000, precision = 1.e-17, repetitions = 100):
        "Test Numpy"
        __d = int(dimension)
        print("  %s"%self.test_Numpy02.__doc__)
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

    #~ @unittest.skip("Debug")
    def test_Scipy01(self, dimension = 3000, precision = 1.e-17, repetitions = 10):
        "Test Scipy"
        __d = int(dimension)
        print("  %s"%self.test_Scipy01.__doc__)
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

# ==============================================================================
if __name__ == "__main__":
    numpy.random.seed(1000)
    print("\nAUTODIAGNOSTIC\n==============")
    sys.stderr = sys.stdout
    unittest.main(verbosity=2)
    print("")
    print("  Les résultats obtenus sont corrects.")
    print("")
