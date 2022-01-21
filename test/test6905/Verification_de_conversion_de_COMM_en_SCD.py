# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2022 EDF R&D
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
"COMM/TUI/SCD/YACS: Conversion utilities verification"

import sys, glob
import unittest
import numpy

fichiers = glob.glob("*.comm")+glob.glob("snippets*_Convert_XXX_to_YYY/*.comm")

# ==============================================================================
class Test_Adao(unittest.TestCase):
    def test1(self):
        self.maxDiff = None
        print("""
        Conversion utilities verification (COM->SCD)
        ++++++++++++++++++++++++++++++++++++++++++++
        """)
        #
        import numpy
        from adao import adaoBuilder
        #
        for fichier in fichiers:
            basename = fichier.rstrip(".comm")
            #
            print("        Processing \"%s\""%basename)
            with open(basename+".comm") as fid:
                comm_content = fid.read()
                #
                comm_content = comm_content.replace("test001_ADAO_External_variables", "test914_Xternal_3_Variables")
                comm_content = comm_content.replace("test020_Observation_and_Simulation", "test914_Xternal_4_Variables")
                comm_content = comm_content.replace("test033_ADAO_Elementary_FunctionTest_Operators", "test914_Xternal_5_Variables")
                #
                case = adaoBuilder.New()
                case.load( Content=comm_content, Formater="COM" )
                texte = case.dump(Formater="SCD")
                del case
                #
                print("        ---> Ok, SCD file of COMM conversion is correct\n")

# ==============================================================================
if __name__ == '__main__':
    print("\nAUTODIAGNOSTIC\n==============")
    sys.stderr = sys.stdout
    unittest.main(verbosity=2)
