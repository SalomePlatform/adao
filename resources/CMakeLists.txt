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

if(ADAO_SALOME_MODULE)

  install(FILES ADAOCatalog.xml DESTINATION ${ADAO_RES_SALOME})
  SALOME_CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/SalomeApp.xml.in ${CMAKE_CURRENT_BINARY_DIR}/SalomeApp.xml INSTALL ${ADAO_RES_SALOME})
  SALOME_CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/SalomeApp.xml.in ${CMAKE_CURRENT_BINARY_DIR}/SalomeAppSL.xml INSTALL ${ADAO_RES_SALOME})

else(ADAO_SALOME_MODULE)

  install(FILES ADAOSchemaCatalog.xml DESTINATION ${ADAO_RES})
  file(GLOB_RECURSE BUTTONS1 "${CMAKE_SOURCE_DIR}/doc/fr/resources/*.png")
  install(FILES ${BUTTONS1} DESTINATION ${ADAO_RES})
  file(GLOB_RECURSE BUTTONS2 "${CMAKE_SOURCE_DIR}/doc/fr/images/eficas*.png")
  install(FILES ${BUTTONS2} DESTINATION ${ADAO_RES})
  file(GLOB_RECURSE BUTTONS3 "${CMAKE_SOURCE_DIR}/doc/en/images/eficas*.png")
  install(FILES ${BUTTONS3} DESTINATION ${ADAO_RES})

endif(ADAO_SALOME_MODULE)
