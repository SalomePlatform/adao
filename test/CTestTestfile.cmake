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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

SET(ADAO_ENGINE_ROOT_DIR $ENV{ADAO_ENGINE_ROOT_DIR})

if(NOT ADAO_ENGINE_ROOT_DIR)
  message(FATAL_ERROR "ADAO_ENGINE_ROOT_DIR environment variable has to be set before launching the tests.")
endif(NOT ADAO_ENGINE_ROOT_DIR)

SET(COMPONENT_NAME ADAO)
SET(TIMEOUT        500)

# Add all test subdirs
SUBDIRS(
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test1001
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test1002
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6701
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6702
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6703
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6704
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6711
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6901
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6902
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6903
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6904
    ${ADAO_ENGINE_ROOT_DIR}/share/test/adao/test6905
    )
