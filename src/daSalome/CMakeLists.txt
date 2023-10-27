# Copyright (C) 2008-2023 EDF R&D
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
# Author: Anthony Geay, anthony.geay@edf.fr, EDF R&D

add_subdirectory(daGUI)

if( NOT ADAO_SALOME_MODULE)

  install(DIRECTORY daYacsSchemaCreator daYacsIntegration DESTINATION "${ADAO_SCRIPT_PYTHON}/adao")
  install(FILES __init__.py adaoBuilder.py DESTINATION "${ADAO_SCRIPT_PYTHON}/adao")

else(NOT ADAO_SALOME_MODULE)

  INSTALL(CODE "
    FILE(WRITE ${CMAKE_INSTALL_PREFIX}/${ADAO_SCRIPT_PYTHON_SALOME}/salome/adao/__init__.py
    \"import adao\n__version__ = adao.__version__\n__sha1__ = \'\'\"
    )
  ")

endif(NOT ADAO_SALOME_MODULE)
