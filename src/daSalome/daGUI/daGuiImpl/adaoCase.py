# -*- coding: utf-8 -*-
# Copyright (C) 2008-2018 EDF R&D
#
# This file is part of SALOME ADAO module
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

import os
import subprocess
import traceback
import SalomePyQt

import eficasSalome
from Ihm import CONNECTOR
from . import adaoGuiHelper
from . import adaoStudyEditor

class AdaoCase:

  def __init__(self):

    self.name = "not yet defined"           # Name of the case

    self.filename = "not yet defined"       # Python filename generated by Eficas
    self.yacs_filename = "not yet defined"  # Yacs schema filename

    self.salome_study_id = -1               # Study of the case
    self.salome_study_item = None           # Study item object

    self.eficas_editor = None               # Editor object from Eficas
    self.arbreOuvert = False

  def setEditor(self, editor):
    if editor is not self.eficas_editor:
      self.eficas_editor = editor
      # Connect to the jdc
      CONNECTOR.Connect(self.eficas_editor.jdc, "valid", self.editorValidEvent, ())

  # Rq on notera que l'on utilise isValid dans isOk
  #    et que isOk appelle editorValidEvent
  #    il n'y a pas de boucle infini car isValid n'émet
  #    son signal que si l'état a changé
  def editorValidEvent(self):
    adaoStudyEditor.updateItem(self.salome_study_id, self.salome_study_item, self)
    adaoGuiHelper.refreshObjectBrowser()

  def isOk(self):
    if self.eficas_editor.jdc:
      return self.eficas_editor.jdc.isValid()
    return False

  def createYACSFile(self):
    rtn = ""
    if (self.filename == ""):
      return "You need to save your case to export it."

    self.yacs_filename = self.filename[:self.filename.rfind(".")] + '.xml'
    yacs_filename_backup = self.filename[:self.filename.rfind(".")] + '.xml.back'
    if os.path.exists(self.yacs_filename):
      os.rename(self.yacs_filename, yacs_filename_backup)

    self.eficas_editor.modified = True
    self.eficas_editor.saveFile()
    filename = self.filename[:self.filename.rfind(".")] + '.py'
    if not os.path.exists(filename):
      msg =  "Cannot find the COMM/PY associated EFICAS/Python files for YACS\n"
      msg += "generation. Is your case correct? Try to close and re-open the\n"
      msg += "case with the ADAO/EFICAS editor."
      return msg

    if "ADAO_ROOT_DIR" not in os.environ:
      return "Please add ADAO_ROOT_DIR to your environnement."

    adao_path = os.environ["ADAO_ROOT_DIR"]
    adao_exe = adao_path + "/bin/salome/AdaoYacsSchemaCreator.py"
    args = ["python", adao_exe, filename, self.yacs_filename]
    p = subprocess.Popen(args)
    (stdoutdata, stderrdata) = p.communicate()
    if not os.path.exists(self.yacs_filename):
      msg  = "An error occured during the execution of the ADAO YACS Schema\n"
      msg += "Creator. If SALOME GUI is launched by command line, see errors\n"
      msg += "details in your terminal.\n"
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
      yacs_swig.loadSchema(self.yacs_filename, 1, 1)
    except:
      msg =  "Please install YACS module, error was: \n"
      msg += traceback.format_exc()
      return msg
    return rtn

  def validationReportforJDC(self):
    rtn = "<i>Validation report is empty.</i>"
    if self.eficas_editor.jdc:
      rtn  = u"Validation report for the selected ADAO case:\n\n"
      rtn += unicode( self.eficas_editor.jdc.report())
    return rtn

  def showTreeAdaoCase(self):
    if self.eficas_editor:
      if self.arbreOuvert:
        self.eficas_editor.fermeArbre()
        self.arbreOuvert = False
      else:
        self.eficas_editor.ouvreArbre()
        self.arbreOuvert = True
    return self.arbreOuvert
