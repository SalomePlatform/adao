# -*- coding: iso-8859-1 -*-
#  Copyright (C) 2010 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import os
import subprocess
import traceback
import SalomePyQt

class AdaoCase:

  def __init__(self):
    self.__name = "new_case"
    self.__filename = ""
    self.__yacs_filename = ""

  def get_name(self):
    return self.__name

  def set_name(self, name):
    self.__name = str(name)

  def get_filename(self):
    return self.__filename

  def set_filename(self, name):
    self.__filename = str(name)

  def createYACSFile(self):
    rtn = ""
    if (self.__filename == ""):
      return "You need to save your case to export it"

    filename = self.__filename[:self.__filename.rfind(".")] + '.py'
    if not os.path.exists(filename):
      msg =  "Cannot find the py file for YACS generation \n"
      msg += "Is your case correct ? \n"
      msg += "(Try to load: " + filename + ")"
      return msg

    if not os.environ.has_key("ADAO_ROOT_DIR"):
      return "Please add ADAO_ROOT_DIR to your environnement"

    adao_path = os.environ["ADAO_ROOT_DIR"]
    adao_exe = adao_path + "/bin/salome/AdaoYacsSchemaCreator.py"
    self.__yacs_filename = self.__filename[:self.__filename.rfind(".")] + '.xml'
    args = [adao_exe, filename, self.__yacs_filename]
    p = subprocess.Popen(args)
    (stdoutdata, stderrdata) = p.communicate()
    if not os.path.exists(self.__yacs_filename):
      msg  = "An error occured during the execution of AdaoYacsSchemaCreator.py \n"
      msg += "See erros details in your terminal \n"
      return msg
    return rtn

  def exportCaseToYACS(self):
    rtn = ""
    rtn = self.createYACSFile()
    if rtn != "":
      return rtn

    try:
      import libYACS_Swig
      yacs_swig = libYACS_Swig.YACS_Swig()
      yacs_swig.loadSchema(self.__yacs_filename)
    except:
      msg =  "Please install YACS module, error was: \n"
      msg += traceback.format_exc()
      return msg
    return rtn

