# Copyright (C) 2008-2026 EDF R&D
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

install(
    FILES AdaoYacsSchemaCreator.py
    DESTINATION ${ADAO_BIN}
)
install(
    FILES gui_Adao_QT_Eficas.py
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ
    DESTINATION ${ADAO_BIN}
)
IF(WIN32)
  SET(SEP "\\;")
ELSE(WIN32)
  SET(SEP ":")
ENDIF(WIN32)
