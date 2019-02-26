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
# Author: Anthony Geay, anthony.geay@edf.fr, EDF R&D

set(EFICAS_DIR "${EFICAS_ROOT_DIR}")
set(PYTHON_SITE "${CMAKE_INSTALL_PREFIX}/${ADAO_SCRIPT_PYTHON}")
SALOME_CONFIGURE_FILE(qtEficas_adao_study.py.in qtEficas_adao_study.py)

install(FILES AdaoYacsSchemaCreator.py ${CMAKE_CURRENT_BINARY_DIR}/qtEficas_adao_study.py DESTINATION ${ADAO_BIN})

INSTALL( CODE "MACRO(GENERATE_EFICAS_CATA_FOR_ADAO  PY_EXE_CATA ADAO_CATA_GEN_FILE OUTPUT_DIR CATA_ADD_PYTHONPATH)
set(ENV{PYTHONPATH} \${CATA_ADD_PYTHONPATH}:\$ENV{PYTHONPATH})
EXECUTE_PROCESS(COMMAND \${PY_EXE_CATA} \${ADAO_CATA_GEN_FILE} \${OUTPUT_DIR} ADAO_Cata_V0.py)
ENDMACRO(GENERATE_EFICAS_CATA_FOR_ADAO)" )

INSTALL(CODE "GENERATE_EFICAS_CATA_FOR_ADAO( \"${PYTHON_EXECUTABLE}\" \"${CMAKE_CURRENT_SOURCE_DIR}/AdaoCatalogGenerator.py\" \"${CMAKE_INSTALL_PREFIX}/${ADAO_SCRIPT_PYTHON_SALOME}/adao\" \"${CMAKE_INSTALL_PREFIX}/${ADAO_SCRIPT_PYTHON_SALOME}:${ADAO_PYTHON_ROOT_DIR}/${ADAO_SCRIPT_PYTHON}\" )")
