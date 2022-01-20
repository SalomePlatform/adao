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
# Author: Anthony Geay, anthony.geay@edf.fr, EDF R&D

if(ADAO_SALOME_MODULE)

  install(FILES ADAOGUI.py ADAO.py ADAO_SalomeSessionless.py DESTINATION ${ADAO_SCRIPT_PYTHON_SALOME})

else(ADAO_SALOME_MODULE)

  install(FILES daUtils/__init__.py daUtils/adaoEficasEvent.py daUtils/adaoLogger.py daUtils/enumerate.py DESTINATION "${ADAO_SCRIPT_PYTHON}/adao/daUtils")

  install(FILES daGuiImpl/__init__.py daGuiImpl/ADAOGUI_impl.py daGuiImpl/adaoGuiManager.py daGuiImpl/adaoGuiHelper.py daGuiImpl/adaoModuleHelper.py daGuiImpl/adaoStudyEditor.py daGuiImpl/adaoCase.py DESTINATION "${ADAO_SCRIPT_PYTHON}/adao/daGuiImpl")

  install(FILES daEficasWrapper/__init__.py daEficasWrapper/adaoEficasWrapper.py DESTINATION "${ADAO_SCRIPT_PYTHON}/adao/daEficasWrapper")

endif(ADAO_SALOME_MODULE)

