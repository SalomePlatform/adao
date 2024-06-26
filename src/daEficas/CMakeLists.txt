# Copyright (C) 2008-2024 EDF R&D
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

SALOME_CONFIGURE_FILE(prefs_ADAO.py.in prefs_ADAO.py)

set(DAEFICAS_FILES
  configuration_ADAO.py
  convert_adao.py
  generator_adao.py
  __init__.py
  ${CMAKE_CURRENT_BINARY_DIR}/prefs_ADAO.py
  prefs.py
  traduitADAOsansToV9_13_0.py
  traduitADAOV7_4_0ToV9_13_0.py
  traduitADAOV7_5_0ToV9_13_0.py
  traduitADAOV7_5_1ToV9_13_0.py
  traduitADAOV7_6_0ToV9_13_0.py
  traduitADAOV7_7_0ToV9_13_0.py
  traduitADAOV7_8_0ToV9_13_0.py
  traduitADAOV8_1_0ToV9_13_0.py
  traduitADAOV8_2_0ToV9_13_0.py
  traduitADAOV8_3_0ToV9_13_0.py
  traduitADAOV8_4_0ToV9_13_0.py
  traduitADAOV8_5_0ToV9_13_0.py
  traduitADAOV8_6_0ToV9_13_0.py
  traduitADAOV9_2_0ToV9_13_0.py
  traduitADAOV9_3_0ToV9_13_0.py
  traduitADAOV9_4_0ToV9_13_0.py
  traduitADAOV9_5_0ToV9_13_0.py
  traduitADAOV9_6_0ToV9_13_0.py
  traduitADAOV9_7_0ToV9_13_0.py
  traduitADAOV9_8_0ToV9_13_0.py
  traduitADAOV9_9_0ToV9_13_0.py
  traduitADAOV9_10_0ToV9_13_0.py
  traduitADAOV9_11_0ToV9_13_0.py
  traduitADAOV9_12_0ToV9_13_0.py
  )

install(FILES ${DAEFICAS_FILES} DESTINATION "${ADAO_SCRIPT_PYTHON}/adao/daEficas")
