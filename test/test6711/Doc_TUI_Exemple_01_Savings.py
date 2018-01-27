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
"Verification d'un exemple de la documentation"

import os, pprint
from utExtend import assertAlmostEqualArrays

# ==============================================================================
def test1():
    """Test"""
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
    #
    case.setObserver("Analysis", String="print('==> Nombre d analyses   : %i'%len(var))")
    #
    case.execute()
    #
    base_file = "output_test6711"
    print("")
    print("#===============================================================================")
    print("#=== Restitution en dictionnaire basique =======================================")
    case.get()
    print("#===============================================================================")
    print("#=== Restitution en fichier TUI ================================================")
    # print(case.dump(FileName=base_file+"_TUI.py", Formater="TUI"))
    case.dump(FileName=base_file+"_TUI.py", Formater="TUI")
    print("#===============================================================================")
    print("#=== Restitution en fichier DIC ================================================")
    # print(case.dump(FileName=base_file+"_DIC.py", Formater="DIC"))
    case.dump(FileName=base_file+"_DIC.py", Formater="DIC")
    print("#===============================================================================")
    print("#=== Restitution en fichier YACS ===============================================")
    # print(case.dump(FileName=base_file+"_YACS.xml", Formater="YACS"))
    case.dump(FileName=base_file+"_YACS.xml", Formater="YACS")
    print("#===============================================================================")
    #
    print("")
    cwd = os.getcwd()
    for f in [
        base_file+"_TUI.py",
        base_file+"_DIC.py",
        base_file+"_YACS.xml",
        ]:
        if os.path.exists(os.path.abspath(cwd+"/"+f)):
            print("#=== Fichier \"%s\" correctement généré"%f)
            os.remove(os.path.abspath(cwd+"/"+f))
        else:
            raise ValueError("Fichier \"%s\" inexistant"%f)
    print("")
    #
    return case.get("Analysis")[-1]

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
    print("""Exemple de la doc :

    Cas-test vérifiant les conversions
    ++++++++++++++++++++++++++++++++++
""")
    xa = test1()
    assertAlmostEqualArrays(xa, [0.25, 0.80, 0.95], places = 5)
