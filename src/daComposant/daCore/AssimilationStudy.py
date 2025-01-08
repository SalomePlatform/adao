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

"""
    Normalized interface for ADAO scripting (full version API)
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["AssimilationStudy"]

from daCore.Aidsm import Aidsm as _Aidsm


# ==============================================================================
class AssimilationStudy(_Aidsm):
    """
    Generic ADAO TUI builder
    """

    __slots__ = ()

    def __init__(self, name=""):
        _Aidsm.__init__(self, name)


# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
