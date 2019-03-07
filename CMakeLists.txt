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

cmake_minimum_required(VERSION 2.6)

# Ensure a proper linker behavior:
CMAKE_POLICY(SET CMP0003 NEW)

project(ADAO)

include(CMakeDependentOption)

option(ADAO_PYTHON_MODULE "Build and install ADAO python module files only." ON)
option(ADAO_BUILD_DOC "Build and install ADAO documentation." ON)
cmake_dependent_option(ADAO_SALOME_MODULE "Build and install ADAO SALOME module files based on ADAO python module." ON "NOT ADAO_PYTHON_MODULE" OFF)

find_package(PythonInterp)

if(NOT PYTHONINTERP_FOUND)
  message(FATAL_ERROR "Python interp not found ! We absolutely need it !")
endif(NOT PYTHONINTERP_FOUND)

set(ADAO_SCRIPT_PYTHON "lib/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages")
set(ADAO_SCRIPT_PYTHON_SALOME "${ADAO_SCRIPT_PYTHON}/salome")
set(ADAO_LIB "lib/salome")
set(ADAO_RES "share/salome/resources/adao")
set(ADAO_BIN "bin/salome")
set(ADAO_BIN_TEST "bin/salome/test")

if(ADAO_PYTHON_MODULE)
  
  add_subdirectory(src)
  
else(ADAO_PYTHON_MODULE)

  # ADAO_SALOME_MODULE
  set(CONFIGURATION_ROOT_DIR $ENV{CONFIGURATION_ROOT_DIR} CACHE PATH "Path to the Salome CMake configuration files")
  if(EXISTS ${CONFIGURATION_ROOT_DIR})
    list(APPEND CMAKE_MODULE_PATH "${CONFIGURATION_ROOT_DIR}/cmake")
    include(SalomeMacros)

    if(ADAO_BUILD_DOC)
      find_package(SalomeSphinx)
      if(NOT SPHINX_FOUND)
	message(FATAL_ERROR "Sphinx has not been found !")
      endif(NOT SPHINX_FOUND)
    endif(ADAO_BUILD_DOC)
    
  else()
    message(FATAL_ERROR "We absolutely need the Salome CMake configuration files, please define CONFIGURATION_ROOT_DIR !")
  endif()

  find_package(SalomeOmniORB REQUIRED)
  find_package(SalomeOmniORBPy REQUIRED)
  find_package(SalomeKERNEL REQUIRED)
  KERNEL_WITH_CORBA()
  
  if(NOT ADAO_PYTHON_ROOT_DIR)
    message(FATAL_ERROR "ADAO_PYTHON_ROOT_DIR cmake variable has to be set if ADAO_SALOME_MODULE option is ON.")
  endif(NOT ADAO_PYTHON_ROOT_DIR)
  find_file(FILE_OF_ADAO_PYTHON_MODULE "daCore/__init__.py" PATHS "${ADAO_PYTHON_ROOT_DIR}/${ADAO_SCRIPT_PYTHON_SALOME}/adao")
  if(NOT FILE_OF_ADAO_PYTHON_MODULE)
    message(FATAL_ERROR "Could not locate daCore/__init__.py into specified ADAO_PYTHON_ROOT_DIR directory ! Sounds bad !")
  endif(NOT FILE_OF_ADAO_PYTHON_MODULE)

  if(NOT EFICAS_ROOT_DIR)
    message(FATAL_ERROR "EFICAS_ROOT_DIR is absolutely needed !")
  endif(NOT EFICAS_ROOT_DIR)
  
  find_file(FILE_OF_EFICAS "generator/__init__.py" PATHS ${EFICAS_ROOT_DIR})

  if(NOT FILE_OF_EFICAS)
    message(FATAL_ERROR "Could not locate generator/__init__.py into EFICAS_ROOT_DIR")
  endif(NOT FILE_OF_EFICAS)
  
  add_subdirectory(src)
  add_subdirectory(idl)
  add_subdirectory(resources)
  add_subdirectory(bin)
  add_subdirectory(examples)
  add_subdirectory(test)
  add_subdirectory(i18n)
  add_subdirectory(doc)
  
endif(ADAO_PYTHON_MODULE)