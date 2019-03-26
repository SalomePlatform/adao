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

set(prefix ${CMAKE_INSTALL_PREFIX})

SALOME_CONFIGURE_FILE(daSalome/test003_ADAO_JDC_using_scripts.comm.in test003_ADAO_JDC_using_scripts.comm)
SALOME_CONFIGURE_FILE(daSalome/test003_bis_ADAO_JDC_using_user_data_init.comm.in test003_bis_ADAO_JDC_using_user_data_init.comm)
SALOME_CONFIGURE_FILE(daSalome/test005_ADAO_Operators.comm.in test005_ADAO_Operators.comm)

SALOME_CONFIGURE_FILE(daSalome/test004_ADAO_JDC_using_scripts.comm.in test004_ADAO_JDC_using_scripts.comm)
SALOME_CONFIGURE_FILE(daSalome/test006_Observers.comm.in test006_Observers.comm)


SALOME_CONFIGURE_FILE(daSalome/test003_ADAO_JDC_using_scripts.py.in test003_ADAO_JDC_using_scripts.py)
SALOME_CONFIGURE_FILE(daSalome/test003_bis_ADAO_JDC_using_user_data_init.py.in test003_bis_ADAO_JDC_using_user_data_init.py)
SALOME_CONFIGURE_FILE(daSalome/test005_ADAO_Operators.py.in test005_ADAO_Operators.py)

SALOME_CONFIGURE_FILE(daSalome/test004_ADAO_JDC_using_scripts.py.in test004_ADAO_JDC_using_scripts.py)
SALOME_CONFIGURE_FILE(daSalome/test006_Observers.py.in test006_Observers.py)

set(EXAMPLES_FILES_TO_INSTALL
  daSalome/test001_ADAO_JDC_using_strings.comm
  daSalome/test001_ADAO_JDC_using_strings.py
  daSalome/test002_ADAO_JDC_using_strings.comm
  daSalome/test002_ADAO_JDC_using_strings.py
  ${CMAKE_CURRENT_BINARY_DIR}/test003_ADAO_JDC_using_scripts.comm
  ${CMAKE_CURRENT_BINARY_DIR}/test003_ADAO_JDC_using_scripts.py
  daSalome/test003_ADAO_scripts_for_JDC.py
  ${CMAKE_CURRENT_BINARY_DIR}/test003_bis_ADAO_JDC_using_user_data_init.comm
  ${CMAKE_CURRENT_BINARY_DIR}/test003_bis_ADAO_JDC_using_user_data_init.py
  daSalome/test003_bis_ADAO_user_data_init.py
  ${CMAKE_CURRENT_BINARY_DIR}/test004_ADAO_JDC_using_scripts.comm
  ${CMAKE_CURRENT_BINARY_DIR}/test004_ADAO_JDC_using_scripts.py
  ${CMAKE_CURRENT_BINARY_DIR}/test005_ADAO_Operators.comm
  ${CMAKE_CURRENT_BINARY_DIR}/test005_ADAO_Operators.py
  daSalome/test005_ADAO_scripts_for_JDC.py
  ${CMAKE_CURRENT_BINARY_DIR}/test006_Observers.comm
  ${CMAKE_CURRENT_BINARY_DIR}/test006_Observers.py
  daSalome/test006_Observers_Observation_Operator.py
  daSalome/test006_Observers_observer_with_file.py
  daSalome/test006_Observers_var.py
  daSalome/test008_ADAO_Elementary_GradientTest.comm
  daSalome/test008_ADAO_Elementary_GradientTest.py
  daSalome/test009_ADAO_Simple_GradientTest.comm
  daSalome/test009_ADAO_Simple_GradientTest.py
  daSalome/test010_ADAO_Simple_AdjointTest.comm
  daSalome/test010_ADAO_Simple_AdjointTest.py
  )

install(FILES ${EXAMPLES_FILES_TO_INSTALL} DESTINATION "share/adao_examples/daSalome")

SALOME_CONFIGURE_FILE(daSkeletons/External_data_definition_by_scripts/ADAO_Case.comm.in ADAO_Case.comm)

set(SKELETON_FILES_TO_INSTALL
  ${CMAKE_CURRENT_BINARY_DIR}/ADAO_Case.comm
  daSkeletons/External_data_definition_by_scripts/Physical_data_and_covariance_matrices.py
  daSkeletons/External_data_definition_by_scripts/Script_AlgorithmParameters.py
  daSkeletons/External_data_definition_by_scripts/Script_Background_xb.py
  daSkeletons/External_data_definition_by_scripts/Script_ObservationOperator_H.py
  daSkeletons/External_data_definition_by_scripts/Script_UserPostAnalysis.py
  daSkeletons/External_data_definition_by_scripts/Physical_simulation_functions.py
  daSkeletons/External_data_definition_by_scripts/Script_BackgroundError_B.py
  daSkeletons/External_data_definition_by_scripts/Script_ObservationError_R.py
  daSkeletons/External_data_definition_by_scripts/Script_Observation_yo.py
  )

install(FILES ${SKELETON_FILES_TO_INSTALL} DESTINATION "share/adao_examples/daSkeletons/External_data_definition_by_scripts")
