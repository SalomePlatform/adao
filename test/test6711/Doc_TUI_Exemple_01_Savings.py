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

import sys, os, tempfile
import unittest

# ==============================================================================
class Test_Adao(unittest.TestCase):
    def test1(self):
        """Test"""
        print("""Exemple de la doc :

        Cas-test vérifiant les conversions
        ++++++++++++++++++++++++++++++++++\n""")
        #-----------------------------------------------------------------------
        from numpy import array, matrix
        from adao import adaoBuilder
        case = adaoBuilder.New()
        case.set( 'AlgorithmParameters', Algorithm='3DVAR' )
        case.set( 'Background',          Vector=[0, 1, 2] )
        case.set( 'BackgroundError',     ScalarSparseMatrix=1.0 )
        case.set( 'Observation',         Vector=array([0.5, 1.5, 2.5]) )
        case.set( 'ObservationError',    DiagonalSparseMatrix='1 1 1' )
        case.set( 'ObservationOperator', Matrix='1 0 0;0 2 0;0 0 3' )
        case.set( 'Observer',            Variable="Analysis", Template="ValuePrinter" )
        #
        case.setObserver("Analysis", String="print('  ==> Nombre d analyses   : %i'%len(var))")
        #
        case.execute()
        #
        #-----------------------------------------------------------------------
        print("")
        print("  #============================================================")
        print("  #=== Export du cas")
        print("  #============================================================")
        with tempfile.TemporaryDirectory() as tmpdirname:
            base_file = os.path.join(tmpdirname, "output_test6711")
            print("  #=== Répertoire temporaire créé")
            #
            fname = base_file+"_TUI.py"
            case.dump(FileName=fname, Formater="TUI")
            print("  #=== Restitution en fichier TUI")
            if os.path.exists(fname) and filesize(fname) > 500:
                print("  #    Fichier TUI correctement généré, de taille %i bytes"%filesize(fname))
            else:
                raise ValueError("Fichier TUI incorrect ou inexistant")
            #
            fname = base_file+"_SCD.py"
            case.dump(FileName=fname, Formater="SCD")
            print("  #=== Restitution en fichier SCD")
            if os.path.exists(fname) and filesize(fname) > 500:
                print("  #    Fichier SCD correctement généré, de taille %i bytes"%filesize(fname))
            else:
                raise ValueError("Fichier SCD incorrect ou inexistant")
            #
            try:
                fname = base_file+"_YACS.xml"
                case.dump(FileName=fname, Formater="YACS")
                print("  #=== Restitution en fichier YACS")
                if os.path.exists(fname) and filesize(fname) > 500:
                    print("  #    Fichier YACS correctement généré, de taille %i bytes"%filesize(fname))
                else:
                    raise ValueError("Fichier YACS incorrect ou inexistant")
            except:
                pass
        print("  #=== Répertoire temporaire supprimé")
        print("  #============================================================")
        print("")
        #-----------------------------------------------------------------------
        xa = case.get("Analysis")[-1]
        ecart = assertAlmostEqualArrays(xa, [0.25, 0.80, 0.95], places = 5)
        #
        print("  L'écart absolu maximal obtenu lors du test est de %.2e."%ecart)
        print("  Les résultats obtenus sont corrects.")
        print("")

# ==============================================================================
def filesize(name):
    statinfo = os.stat(name)
    return statinfo.st_size # Bytes

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
