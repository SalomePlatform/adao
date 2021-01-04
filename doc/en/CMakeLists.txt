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

set(DOC_LANG en)
set(DOC_DESTINATION "share/doc/gui/ADAO")

file(COPY ../${DOC_LANG} DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY ${CMAKE_SOURCE_DIR}/bin/module_version.py DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/${DOC_LANG})

set(_cmd_options -c ${CMAKE_CURRENT_BINARY_DIR}/${DOC_LANG} -b html -d doctrees ${CMAKE_CURRENT_BINARY_DIR}/${DOC_LANG} html/${DOC_LANG})
SALOME_ACCUMULATE_ENVIRONMENT(PYTHONPATH ${CMAKE_CURRENT_BINARY_DIR}/${DOC_LANG}/${DOC_LANG}) # for module_version.py for conf.py for sphinx
SALOME_GENERATE_ENVIRONMENT_SCRIPT(_cmd env_script "${SPHINX_EXECUTABLE}" "${_cmd_options}")
add_custom_target(${DOC_LANG}_doc COMMAND ${_cmd})
install(CODE "EXECUTE_PROCESS(COMMAND \"${CMAKE_COMMAND}\" --build ${PROJECT_BINARY_DIR} --target ${DOC_LANG}_doc)")

install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/html/${DOC_LANG}" DESTINATION ${DOC_DESTINATION})
