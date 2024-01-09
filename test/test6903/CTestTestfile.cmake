# Copyright (C) 2008-2024 EDF R&D
#
# This file is part of SALOME ADAO module
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
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

SET(TEST_NAMES
  Verification_des_mono_et_multi_fonctions_A
  Verification_des_mono_et_multi_fonctions_B
  Verification_des_mono_et_multi_fonctions_C
  Verification_des_mono_et_multi_fonctions_D
  Verification_des_mono_et_multi_fonctions_E
  Verification_des_mono_et_multi_fonctions_F
  )

FOREACH(tfile ${TEST_NAMES})
  SET(TEST_NAME ADAO_${tfile})
  ADD_TEST(${TEST_NAME} python ${tfile}.py)
  #ADD_TEST(${TEST_NAME} python ${SALOME_TEST_DRIVER} ${TIMEOUT} ${tfile}.py)
  SET_TESTS_PROPERTIES(${TEST_NAME} PROPERTIES LABELS "${COMPONENT_NAME}")
ENDFOREACH()
