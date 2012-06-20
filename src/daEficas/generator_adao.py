# -*- coding: utf-8 -*-
# Copyright (C) 2010-2011 EDF R&D
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
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

from generator.generator_python import PythonGenerator
import traceback
import logging

def entryPoint():
   """
      Retourne les informations necessaires pour le chargeur de plugins

      Ces informations sont retournees dans un dictionnaire
   """
   return {
        # Le nom du plugin
        'name' : 'adao',
        # La factory pour creer une instance du plugin
          'factory' : AdaoGenerator,
          }

class AdaoGenerator(PythonGenerator):

  def __init__(self,cr=None):
    PythonGenerator.__init__(self, cr)
    self.dictMCVal={}
    self.text_comm = ""
    self.text_da = ""
    self.text_da_status = False
    self.logger = logging.getLogger('ADAO EFICAS GENERATOR')
    self.logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    self.logger.addHandler(ch)

  def gener(self,obj,format='brut',config=None):
    self.logger.debug("method gener called")
    self.text_comm = PythonGenerator.gener(self, obj, format, config)
    for key, value in self.dictMCVal.iteritems():
      self.logger.debug("dictMCVAl %s %s" % (key,value))

    try :
      self.text_da_status = False
      self.generate_da()
      self.text_da_status = True
    except:
      self.logger.info("Case is not correct, python command file for YACS schema generation cannot be created")
      self.logger.debug(self.text_da)
      self.dictMCVal = {}
      traceback.print_exc()
    return self.text_comm

  def writeDefault(self, fn):
    if self.text_da_status:
      print "write adao python command file"
      filename = fn[:fn.rfind(".")] + '.py'
      f = open( str(filename), 'wb')
      f.write( self.text_da )
      f.close()

  def generMCSIMP(self,obj) :
    """
    Convertit un objet MCSIMP en texte python
    """
    clef=""
    for i in obj.get_genealogie() :
      clef=clef+"__"+i
    self.dictMCVal[clef]=obj.valeur

    s=PythonGenerator.generMCSIMP(self,obj)
    return s

  def generate_da(self):
  
    if "__CHECKING_STUDY__Study_name" in self.dictMCVal.keys():
      self.type_of_study = "CHECKING_STUDY"
    else:
      self.type_of_study = "ASSIMILATION_STUDY"
        
    self.text_da += "#-*-coding:iso-8859-1-*- \n"
    self.text_da += "study_config = {} \n"

    # Extraction de Study_type
    self.text_da += "study_config['StudyType'] = '" + self.type_of_study + "'\n"
    # Extraction de Study_name
    self.text_da += "study_config['Name'] = '" + self.dictMCVal["__"+self.type_of_study+"__Study_name"] + "'\n"
    # Extraction de Debug
    self.text_da += "study_config['Debug'] = '" + str(self.dictMCVal["__"+self.type_of_study+"__Debug"]) + "'\n"
    # Extraction de Algorithm
    self.text_da += "study_config['Algorithm'] = '" + self.dictMCVal["__"+self.type_of_study+"__Algorithm"] + "'\n"

    if "__"+self.type_of_study+"__Background__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("Background")
    if "__"+self.type_of_study+"__BackgroundError__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("BackgroundError")
    if "__"+self.type_of_study+"__Observation__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("Observation")
    if "__"+self.type_of_study+"__ObservationError__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("ObservationError")
    if "__"+self.type_of_study+"__CheckingPoint__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("CheckingPoint")
    self.add_data("ObservationOperator")

    self.add_variables()
    # Parametres optionnels

    # Extraction du Study_repertory
    if "__"+self.type_of_study+"__Study_repertory" in self.dictMCVal.keys():
      self.text_da += "study_config['Repertory'] = '" + self.dictMCVal["__"+self.type_of_study+"__Study_repertory"] + "'\n"
    # Extraction de AlgorithmParameters
    if "__"+self.type_of_study+"__AlgorithmParameters__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_algorithm_parameters()
    # Extraction de UserPostAnalysis
    if "__"+self.type_of_study+"__UserPostAnalysis__FROM" in self.dictMCVal.keys():
      self.add_UserPostAnalysis()
    if "__"+self.type_of_study+"__UserDataInit__INIT_FILE" in self.dictMCVal.keys():
      self.add_init()
    if "__"+self.type_of_study+"__Observers__SELECTION" in self.dictMCVal.keys():
      self.add_observers()

  def add_data(self, data_name):

    # Extraction des données
    search_text = "__"+self.type_of_study+"__" + data_name + "__"
    data_type = self.dictMCVal[search_text + "INPUT_TYPE"]
    search_type = search_text + data_type + "__data__"
    from_type = self.dictMCVal[search_type + "FROM"]
    data = ""
    if from_type == "String":
      data = self.dictMCVal[search_type + "STRING_DATA__STRING"]
    elif from_type == "Script":
      data = self.dictMCVal[search_type + "SCRIPT_DATA__SCRIPT_FILE"]
    elif from_type == "FunctionDict":
      data = self.dictMCVal[search_type + "FUNCTIONDICT_DATA__FUNCTIONDICT_FILE"]
    else:
      raise Exception('From Type unknown', from_type)

    if from_type == "String" or from_type == "Script":
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = '" + data_type + "'\n"
      self.text_da += data_name + "_config['From'] = '" + from_type + "'\n"
      self.text_da += data_name + "_config['Data'] = '" + data      + "'\n"
      self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"

    if from_type == "FunctionDict":
      self.text_da += data_name + "_FunctionDict = {}\n"
      self.text_da += data_name + "_FunctionDict['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"
      self.text_da += data_name + "_FunctionDict['Script'] = {}\n"
      self.text_da += data_name + "_FunctionDict['Script']['Direct'] = '"  + data + "'\n"
      self.text_da += data_name + "_FunctionDict['Script']['Tangent'] = '" + data + "'\n"
      self.text_da += data_name + "_FunctionDict['Script']['Adjoint'] = '" + data + "'\n"
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = 'Function'\n"
      self.text_da += data_name + "_config['From'] = 'FunctionDict'\n"
      self.text_da += data_name + "_config['Data'] = " + data_name + "_FunctionDict\n"
      self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"

  def add_algorithm_parameters(self):

    data_name = "AlgorithmParameters"
    data_type = "Dict"
    from_type = "Script"
    data = self.dictMCVal["__"+self.type_of_study+"__AlgorithmParameters__Dict__data__SCRIPT_DATA__SCRIPT_FILE"]

    self.text_da += data_name + "_config = {} \n"
    self.text_da += data_name + "_config['Type'] = '" + data_type + "'\n"
    self.text_da += data_name + "_config['From'] = '" + from_type + "'\n"
    self.text_da += data_name + "_config['Data'] = '" + data + "'\n"
    self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"

  def add_init(self):

      init_file_data = self.dictMCVal["__"+self.type_of_study+"__UserDataInit__INIT_FILE"]
      init_target_list = self.dictMCVal["__"+self.type_of_study+"__UserDataInit__TARGET_LIST"]

      self.text_da += "Init_config = {}\n"
      self.text_da += "Init_config['Type'] = 'Dict'\n"
      self.text_da += "Init_config['From'] = 'Script'\n"
      self.text_da += "Init_config['Data'] = '" + init_file_data + "'\n"
      self.text_da += "Init_config['Target'] = ["
      if type(init_target_list) is type("str"):
        self.text_da +=  "'" + init_target_list + "',"
      else:
        for target in init_target_list:
          self.text_da += "'" + target + "',"
      self.text_da += "]\n"
      self.text_da += "study_config['UserDataInit'] = Init_config\n"

  def add_UserPostAnalysis(self):

    from_type = self.dictMCVal["__"+self.type_of_study+"__UserPostAnalysis__FROM"]
    data = ""
    if from_type == "String":
      data = self.dictMCVal["__"+self.type_of_study+"__UserPostAnalysis__STRING_DATA__STRING"]
      self.text_da += "Analysis_config = {}\n"
      self.text_da += "Analysis_config['From'] = 'String'\n"
      self.text_da += "Analysis_config['Data'] = \"\"\"" + data + "\"\"\"\n"
      self.text_da += "study_config['UserPostAnalysis'] = Analysis_config\n"
    elif from_type == "Script":
      data = self.dictMCVal["__"+self.type_of_study+"__UserPostAnalysis__SCRIPT_DATA__SCRIPT_FILE"]
      self.text_da += "Analysis_config = {}\n"
      self.text_da += "Analysis_config['From'] = 'Script'\n"
      self.text_da += "Analysis_config['Data'] = '" + data + "'\n"
      self.text_da += "study_config['UserPostAnalysis'] = Analysis_config\n"
    else:
      raise Exception('From Type unknown', from_type)

  def add_variables(self):

    # Input variables
    if "__"+self.type_of_study+"__InputVariables__NAMES" in self.dictMCVal.keys():
      names = []
      sizes = []
      if isinstance(self.dictMCVal["__"+self.type_of_study+"__InputVariables__NAMES"], type("")):
        names.append(self.dictMCVal["__"+self.type_of_study+"__InputVariables__NAMES"])
      else:
        names = self.dictMCVal["__"+self.type_of_study+"__InputVariables__NAMES"]
      if isinstance(self.dictMCVal["__"+self.type_of_study+"__InputVariables__SIZES"], type(1)):
        sizes.append(self.dictMCVal["__"+self.type_of_study+"__InputVariables__SIZES"])
      else:
        sizes = self.dictMCVal["__"+self.type_of_study+"__InputVariables__SIZES"]

      self.text_da += "inputvariables_config = {}\n"
      self.text_da += "inputvariables_config['Order'] = %s\n" % list(names)
      for name, size in zip(names, sizes):
        self.text_da += "inputvariables_config['%s'] = %s\n" % (name,size)
      self.text_da += "study_config['InputVariables'] = inputvariables_config\n"
    else:
      self.text_da += "inputvariables_config = {}\n"
      self.text_da += "inputvariables_config['Order'] =['adao_default']\n"
      self.text_da += "inputvariables_config['adao_default'] = -1\n"
      self.text_da += "study_config['InputVariables'] = inputvariables_config\n"

    # Output variables
    if "__"+self.type_of_study+"__OutputVariables__NAMES" in self.dictMCVal.keys():
      names = []
      sizes = []
      if isinstance(self.dictMCVal["__"+self.type_of_study+"__OutputVariables__NAMES"], type("")):
        names.append(self.dictMCVal["__"+self.type_of_study+"__OutputVariables__NAMES"])
      else:
        names = self.dictMCVal["__"+self.type_of_study+"__OutputVariables__NAMES"]
      if isinstance(self.dictMCVal["__"+self.type_of_study+"__OutputVariables__SIZES"], type(1)):
        sizes.append(self.dictMCVal["__"+self.type_of_study+"__OutputVariables__SIZES"])
      else:
        sizes = self.dictMCVal["__"+self.type_of_study+"__OutputVariables__SIZES"]

      self.text_da += "outputvariables_config = {}\n"
      self.text_da += "outputvariables_config['Order'] = %s\n" % list(names)
      for name, size in zip(names, sizes):
        self.text_da += "outputvariables_config['%s'] = %s\n" % (name,size)
      self.text_da += "study_config['OutputVariables'] = outputvariables_config\n"
    else:
      self.text_da += "outputvariables_config = {}\n"
      self.text_da += "outputvariables_config['Order'] = ['adao_default']\n"
      self.text_da += "outputvariables_config['adao_default'] = -1\n"
      self.text_da += "study_config['OutputVariables'] = outputvariables_config\n"

  def add_observers(self):
    observers = {}
    observer = self.dictMCVal["__"+self.type_of_study+"__Observers__SELECTION"]
    if isinstance(observer, type("")):
      self.add_observer_in_dict(observer, observers)
    else:
      for observer in self.dictMCVal["__"+self.type_of_study+"__Observers__SELECTION"]:
        self.add_observer_in_dict(observer, observers)

    # Write observers in the python command file
    number = 1
    self.text_da += "observers = {}\n"
    for observer in observers.keys():
      number += 1
      self.text_da += "observers[\"" + observer + "\"] = {}\n"
      self.text_da += "observers[\"" + observer + "\"][\"number\"] = " + str(number) + "\n"
      self.text_da += "observers[\"" + observer + "\"][\"nodetype\"] = \"" + observers[observer]["nodetype"] + "\"\n"
      if observers[observer]["nodetype"] == "String":
        self.text_da += "observers[\"" + observer + "\"][\"String\"] = \"\"\"" + observers[observer]["script"] + "\"\"\"\n"
      else:
        self.text_da += "observers[\"" + observer + "\"][\"Script\"] = \"" + observers[observer]["file"] + "\"\n"
      if "scheduler" in observers[observer].keys():
        self.text_da += "observers[\"" + observer + "\"][\"scheduler\"] = \"\"\"" + observers[observer]["scheduler"] + "\"\"\"\n"
    self.text_da += "study_config['Observers'] = observers\n"

  def add_observer_in_dict(self, observer, observers):
    """
      Add observer in the observers dict.
    """
    observers[observer] = {}
    observers[observer]["name"] = observer
    observer_eficas_name = "__"+self.type_of_study+"__Observers__" + observer + "__" + observer + "_data__"
    # NodeType
    node_type_key_name = observer_eficas_name + "NodeType"
    observers[observer]["nodetype"] = self.dictMCVal[node_type_key_name]

    # NodeType script/file
    if observers[observer]["nodetype"] == "String":
      observers[observer]["script"] = self.dictMCVal[observer_eficas_name + "PythonScript__Value"]
    else:
      observers[observer]["file"] = self.dictMCVal[observer_eficas_name + "UserFile__Value"]

    # Scheduler
    scheduler_key_name = observer_eficas_name + "Scheduler"
    if scheduler_key_name in self.dictMCVal.keys():
      observers[observer]["scheduler"] = self.dictMCVal[scheduler_key_name]
    # Info
    info_key_name = observer_eficas_name + "Info"
    if info_key_name in self.dictMCVal.keys():
      observers[observer]["info"] = self.dictMCVal[info_key_name]
