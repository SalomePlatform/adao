# Copyright (C) 2008-2021 EDF R&D
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

if(ADAO_SALOME_MODULE)

  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/CTestTestfile.cmake DESTINATION ${ADAO_BIN_TEST})

else(ADAO_SALOME_MODULE)

  install(DIRECTORY test1001 test1002 test6701 test6702 test6703 test6704 test6711 test6901 test6902 test6903 test6904 test6905 DESTINATION ${ADAO_TEST})

endif(ADAO_SALOME_MODULE)
