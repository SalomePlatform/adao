# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
#
# Copyright (C) 2007-2008  CEA/DEN, EDF R&D, OPEN CASCADE
#
# Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
# CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
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

__author__ = "gboulant"
__date__ = "$1 avr. 2010 09:08:02$"

class Enumerate(object):
    """
    This class emulates a C-like enum for python.
    """
    def __init__(self, keys, offset=0):
        """
        Canonical constructor
        @keys a list of keys string to be used as the enum symbols
        """
        self._dict_keynumbers = {}
        for number, key in enumerate(keys):
            value = offset+number
            setattr(self, key, value)
            self._dict_keynumbers[key] = value


    def contains(self, key):
        """
        Return true if this enumerate contains the specified key
        @key a key to test
        """
        return (key in self._dict_keynumbers.keys())

    def isValid(self, value):
        return (value in self._dict_keynumbers.values())

    def listkeys(self):
        return sorted(self._dict_keynumbers.keys())

    def listvalues(self):
        return sorted(self._dict_keynumbers.values())

#
# ==============================================================================
# Basic use cases and unit test functions
# ==============================================================================
#

def TEST_simple():
    TYPES_LIST=Enumerate([
        'SEP',
        'OTHER'
    ])
    print(TYPES_LIST.listvalues())
    return True

def TEST_createFromList():
    codes = Enumerate([
        'KERNEL', # This should take the value 0
        'GUI', # This should take the value 1
        'GEOM', # ...
        'MED',
        'SMESH'])

    print(codes.KERNEL)
    print(codes.GEOM)
    if (codes.KERNEL == 0 and codes.GEOM == 2):
        return True
    else:
        return False

def TEST_createFromString():
    aList = "KERNEL GUI GEOM MED"

    codes = Enumerate(aList.split())

    print(codes.KERNEL)
    print(codes.GEOM)
    if (codes.KERNEL == 0 and codes.GEOM == 2):
        return True
    else:
        return False

def TEST_contains():
    codes = Enumerate([
        'KERNEL', # This should take the value 0
        'GUI', # This should take the value 1
        'GEOM', # ...
        'MED',
        'SMESH'])

    print("VISU in enumerate?", codes.contains("VISU"))
    if ( not codes.contains("VISU") ):
        return True
    else:
        return False

def TEST_isValid():
    codes = Enumerate([
        'KERNEL', # This should take the value 0
        'GUI', # This should take the value 1
        'GEOM', # ...
        'MED',
        'SMESH'])

    if ( not codes.isValid(23) ):
        return True
    else:
        return False

def TEST_offset():
    codes = Enumerate([
        'KERNEL', # This should take the value 0
        'GUI', # This should take the value 1
        'GEOM', # ...
        'MED',
        'SMESH'], offset=20)

    print(codes.KERNEL)
    print(codes.GEOM)
    if (codes.KERNEL == 20 and codes.GEOM == 22):
        return True
    else:
        return False

def TEST_listvalues():
    codes = Enumerate([
        'KERNEL', # This should take the value 0
        'GUI', # This should take the value 1
        'GEOM', # ...
        'MED',
        'SMESH'], offset=20)

    print(codes.listvalues())
    if codes.listvalues() != [20,21,22,23,24]:
        return False
    return True


if __name__ == "__main__":
    import unittester
    unittester.run("enumerate","TEST_simple")
    unittester.run("enumerate","TEST_createFromList")
    unittester.run("enumerate","TEST_createFromString")
    unittester.run("enumerate","TEST_contains")
    unittester.run("enumerate","TEST_isValid")
    unittester.run("enumerate","TEST_offset")
    unittester.run("enumerate","TEST_listvalues")
