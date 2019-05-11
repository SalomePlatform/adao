#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2019 EDF R&D
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

"""
   Launching the standalone EFICAS/ADAO interface
"""

import os, sys

# ==============================================================================
# Chemin pour l'installation (ordre important)
if "EFICAS_ROOT" in os.environ:
    EFICAS_ROOT = os.environ["EFICAS_ROOT"]
    __path_ok = True
else:
    print("\nKeyError:\n"+\
        "  the required environment variable EFICAS_ROOT is unknown.\n"+\
        "  You have either to be in SALOME environment, or to set this\n"+\
        "  variable in your environment to the right path \"<...>\" to find\n"+\
        "  an installed EFICAS application. For example:\n"+\
        "    EFICAS_ROOT=\"<...>\" %s"%__file__
        )
    __path_ok = False
try:
    import adao
    __path_ok = True
except ImportError:
    print("\nImportError:\n"+\
        "  the required ADAO library can not be found to be imported.\n"+\
        "  You have either to be in ADAO environment, or to be in SALOME\n"+\
        "  environment, or to set manually in your Python 3 environment the\n"+\
        "  right path \"<...>\" to find an installed ADAO application. For\n"+\
        "  example:\n"+\
        "    PYTHONPATH=\"<...>:${PYTHONPATH}\" %s"%__file__
        )
    __path_ok = False
try:
    import PyQt5
    __path_ok = True
except ImportError:
    print("\nImportError:\n"+\
        "  the required PyQt5 library can not be found to be imported.\n"+\
        "  You have either to have a raisonable up-to-date Python 3\n"+\
        "  installation (less than 5 years), or to be in SALOME environment."
        )
    __path_ok = False
if not __path_ok:
    print("\nWarning:\n"+\
        "  It seems you have some troubles with your installation. It may\n"+\
        "  exists other errors than are not explained as above, like some\n"+\
        "  incomplete or obsolete Python 3 and module installation.\n"+\
        "  \n"+\
        "  Please correct the above error(s) before launching the\n"+\
        "  standalone EFICAS/ADAO interface \"%s\"\n"%__file__
          )
    sys.exit(2)
else:
    print("Launching the standalone EFICAS/ADAO interface...")
sys.path.insert(0,EFICAS_ROOT)
sys.path.insert(0,os.path.join(adao.adao_py_dir,"daEficas"))

# ==============================================================================
# Préférences et module EFICAS
from daEficas import prefs
from InterfaceQT4 import eficas_go

eficas_go.lanceEficas(code=prefs.code)
# ==============================================================================
