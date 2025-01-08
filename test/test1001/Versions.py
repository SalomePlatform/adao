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
"Test du système et des versions de modules"

import sys
import unittest

# ==============================================================================
#
# Versions minimales pour ADAO
# ----------------------------
minimal_python_version     = "3.5.0"
minimal_numpy_version      = "1.14.0"
minimal_scipy_version      = "0.19.0"
minimal_matplotlib_version = "2.2.0"
minimal_nlopt_version      = "2.4.2"
#
# ==============================================================================
class Test_Versions(unittest.TestCase):
    def test1_minimalVersion(self):
        "Affichage des versions minimales"
        print("  Les versions minimales attendues sont :")
        print("    - Python systeme....: %s"%minimal_python_version)
        print("    - Numpy.............: %s"%minimal_numpy_version)
        print("    - Scipy.............: %s"%minimal_scipy_version)
        print("    - NLopt.............: %s"%minimal_nlopt_version)
        print("    - Matplotlib........: %s"%minimal_matplotlib_version)
        print("")

    def test2_Version(self):
        "Test du système et des versions de modules"
        print("  Les versions disponibles sont :")
        v=sys.version.split()
        print("    - Python systeme....: %s"%v[0])
        assert compare_versions(sys.version.split()[0], minimal_python_version)

    def test3_Version(self):
        try:
            import numpy
            print("    - Numpy.............: %s"%numpy.version.version)
            assert compare_versions(numpy.version.version, minimal_numpy_version)
        except ImportError as e:
            raise ImportError(str(e))

    def test4_Version(self):
        try:
            import scipy
            print("    - Scipy.............: %s"%scipy.version.version)
            assert compare_versions(scipy.version.version, minimal_scipy_version)
        except ImportError as e:
            raise ImportError(str(e))

    def test5_Version(self):
        try:
            import nlopt
            __version = "%s.%s.%s"%(
                nlopt.version_major(),
                nlopt.version_minor(),
                nlopt.version_bugfix(),
                )
            print("    - NLopt.............: %s"%__version)
            assert compare_versions(__version, minimal_nlopt_version)
        except ImportError as e:
            raise ImportError(str(e))

    def test6_Version(self):
        try:
            import matplotlib
            mplversion = matplotlib.__version__
            print("    - Matplotlib........: %s"%mplversion)
            assert compare_versions(mplversion, minimal_matplotlib_version)
            #
            print("")
            backends_OK = []
            backends_KO = []
            backend_now = matplotlib.get_backend()

            for backend in [
                'bidon', # Pour vérifier le test uniquement
                'Agg',
                'Cocoa',
                'CocoaAgg',
                'GTK',
                'GTKAgg',
                'Qt5',
                'Qt5Agg',
                'Template',
                'TkAgg',
                'emf',
                'gdk',
                'pdf',
                'pgf',
                'ps',
                'svg',
                ]:
                try:
                    matplotlib.use(backend)
                    backends_OK.append(backend)
                except ValueError:
                    backends_KO.append(backend)
            backends_OK.sort()
            backends_KO.sort()
            #
            print("  Backends disponibles pour Matplotlib %s :"%mplversion)
            print("    Defaut initial......: '%s'"%backend_now)
            print("    Fonctionnant........:")
            for b in backends_OK:
                print("                          '%s'"%b)
            print("    Non fonctionnant....:")
            for b in backends_KO:
                print("                          '%s'"%b)
            print("    (Le backend 'bidon' n'est ici que pour verifier le test, il n'existe pas)")
        except ImportError as e:
            raise ImportError(str(e))
        print("")
        print("  Les résultats obtenus sont corrects.")
        print("")

def compare_versions(v1,v2):
    "Comparaison v1 >= v2"
    for s in ['+', 'rc1', 'rc2', 'rc3']:
        v1 = v1.replace(s,'',1)
        v2 = v2.replace(s,'',1)
    v11,v12,v13 = list(map(float,v1.split('.')))
    v21,v22,v23 = list(map(float,v2.split('.')))
    lv1 = 1e6*v11 + 1e3*v12 + v13
    lv2 = 1e6*v21 + 1e3*v22 + v23
    return lv1 >= lv2

#===============================================================================
if __name__ == "__main__":
    print("\nAUTODIAGNOSTIC\n==============")
    sys.stderr = sys.stdout
    unittest.main(verbosity=2)
