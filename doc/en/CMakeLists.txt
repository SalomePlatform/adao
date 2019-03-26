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

set(DOCLANG en)
set(DOC_DESTINATION "share/doc/gui/ADAO/${DOCLANG}")

file(GLOB_RECURSE BEAUTIFUL_PNGS "${CMAKE_SOURCE_DIR}/doc/${DOCLANG}/*.png")
install(FILES ${BEAUTIFUL_PNGS} DESTINATION ${ADAO_RES})
file(COPY conf.py DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY ${CMAKE_SOURCE_DIR}/bin/module_version.py DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(GLOB_RECURSE RST_FILES "${CMAKE_SOURCE_DIR}/doc/${DOCLANG}/*.rst")
file(COPY ${RST_FILES} DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY resources snippets images DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

set(_cmd_options -c ${CMAKE_CURRENT_BINARY_DIR} -b html -d doctrees -D latex_paper_size=a4 ${CMAKE_CURRENT_BINARY_DIR} html)
SALOME_ACCUMULATE_ENVIRONMENT(PYTHONPATH ${CMAKE_CURRENT_BINARY_DIR}) # for module_version.py for conf.py for sphinx
SALOME_GENERATE_ENVIRONMENT_SCRIPT(_cmd env_script "${SPHINX_EXECUTABLE}" "${_cmd_options}")      
add_custom_target(en_tutorial_doc COMMAND ${_cmd})
install(CODE "EXECUTE_PROCESS(COMMAND \"${CMAKE_COMMAND}\" --build ${PROJECT_BINARY_DIR} --target en_tutorial_doc)")

file(GLOB_RECURSE BEAUTIFUL_PNGS2 "${CMAKE_SOURCE_DIR}/doc/${DOCLANG}/images/*.png")
INSTALL(CODE "file(GLOB BEAUTIFUL_HTML \"${CMAKE_CURRENT_BINARY_DIR}/html/*.html\")
file(COPY \${BEAUTIFUL_HTML} DESTINATION ${CMAKE_INSTALL_PREFIX}/${DOC_DESTINATION})")
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/html/_static" DESTINATION ${DOC_DESTINATION})
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/html/snippets" DESTINATION ${DOC_DESTINATION})
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/html/_sources" DESTINATION ${DOC_DESTINATION})
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/html/searchindex.js" DESTINATION ${DOC_DESTINATION})
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/html/objects.inv" DESTINATION ${DOC_DESTINATION})
install(FILES ${BEAUTIFUL_PNGS2} DESTINATION ${DOC_DESTINATION}/_images)
