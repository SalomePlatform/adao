# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

from generator.generator_python import PythonGenerator
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

  def gener(self,obj,format='brut',config=None,appliEficas=None):
    self.logger.debug("method gener called")
    self.text_comm = PythonGenerator.gener(self, obj, format, config, appliEficas)
    for key, value in self.dictMCVal.items():
      self.logger.debug("dictMCVAl %s %s" % (key,value))

    try :
      self.text_da_status = False
      self.generate_da()
      self.text_da_status = True
    except:
      self.logger.debug("EFICAS case is not valid, python command file for YACS schema generation cannot be created")
      self.logger.debug(self.text_da)
      self.dictMCVal = {}
      # import traceback ; traceback.print_exc()
    return self.text_comm

  def writeDefault(self, fn):
    if self.text_da_status:
      self.logger.debug("write adao python command file")
      filename = fn[:fn.rfind(".")] + '.py'
      #~ f = open( str(filename), 'wb')
      f = open( str(filename), 'w')
      f.write( self.text_da )
      f.close()

  def generMCSIMP(self,obj) :
    """
    Convertit un objet MCSIMP en texte python
    """
    clef=""
    for i in obj.getGenealogie() :
      clef=clef+"__"+i
    self.dictMCVal[clef]=obj.valeur

    s=PythonGenerator.generMCSIMP(self,obj)
    return s

  def generate_da(self):

    self.text_da += "#-*- coding: utf-8 -*-\n"
    self.text_da += "study_config = {}\n"

    # Extraction de Study_type
    if "__CHECKING_STUDY__StudyName" in self.dictMCVal.keys():
      self.type_of_study = "CHECKING_STUDY"
      self.text_da += "study_config['StudyType'] = '\"CHECKING_STUDY\"'\n"
    elif "__OPTIMIZATION_STUDY__StudyName" in self.dictMCVal.keys():
      self.type_of_study = "OPTIMIZATION_STUDY"
      self.text_da += "study_config['StudyType'] = '\"ASSIMILATION_STUDY\"'\n"
    elif "__REDUCTION_STUDY__StudyName" in self.dictMCVal.keys():
      self.type_of_study = "REDUCTION_STUDY"
      self.text_da += "study_config['StudyType'] = '\"ASSIMILATION_STUDY\"'\n"
    else:
      self.type_of_study = "ASSIMILATION_STUDY"
      self.text_da += "study_config['StudyType'] = '\"ASSIMILATION_STUDY\"'\n"

    # Extraction de StudyName
    self.text_da += "study_config['Name'] = '" + self.dictMCVal["__"+self.type_of_study+"__StudyName"] + "'\n"
    # Extraction de Debug
    if "__"+self.type_of_study+"__Debug" in self.dictMCVal.keys():
      self.text_da += "study_config['Debug'] = '" + str(self.dictMCVal["__"+self.type_of_study+"__Debug"]) + "'\n"
    else:
      self.text_da += "study_config['Debug'] = '0'\n"

    # Extraction de Algorithm et de ses parametres
    if "__"+self.type_of_study+"__AlgorithmParameters__Algorithm" in self.dictMCVal.keys():
      self.text_da += "study_config['Algorithm'] = '" + self.dictMCVal["__"+self.type_of_study+"__AlgorithmParameters__Algorithm"] + "'\n"
      self.add_AlgorithmParameters()
    elif "__"+self.type_of_study+"__Algorithm" in self.dictMCVal.keys():
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
    if "__"+self.type_of_study+"__ObservationOperator__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("ObservationOperator")
    if "__"+self.type_of_study+"__EvolutionModel__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("EvolutionModel")
    if "__"+self.type_of_study+"__EvolutionError__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("EvolutionError")
    if "__"+self.type_of_study+"__ControlInput__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_data("ControlInput")

    self.add_variables()
    # Parametres optionnels

    # Extraction du StudyRepertory
    if "__"+self.type_of_study+"__StudyRepertory" in self.dictMCVal.keys():
      self.text_da += "study_config['Repertory'] = '" + self.dictMCVal["__"+self.type_of_study+"__StudyRepertory"] + "'\n"

    # Extraction du ExecuteInContainer
    if "__"+self.type_of_study+"__ExecuteInContainer" in self.dictMCVal.keys():
      self.text_da += "study_config['ExecuteInContainer'] = '" + str(self.dictMCVal["__"+self.type_of_study+"__ExecuteInContainer"]) + "'\n"
    else:
      self.text_da += "study_config['ExecuteInContainer'] = 'No'\n"

    # Extraction de UserPostAnalysis
    if "__"+self.type_of_study+"__UserPostAnalysis__FROM" in self.dictMCVal.keys():
      self.add_UserPostAnalysis()
    if "__"+self.type_of_study+"__UserDataInit__INIT_FILE" in self.dictMCVal.keys():
      self.add_init()
    if "__"+self.type_of_study+"__Observers__SELECTION" in self.dictMCVal.keys():
      self.add_observers()

  def add_data(self, data_name):

    # Extraction des donnees
    search_text = "__"+self.type_of_study+"__" + data_name + "__"
    data_type = self.dictMCVal[search_text + "INPUT_TYPE"]
    search_type = search_text + data_type + "__data__"
    from_type = self.dictMCVal[search_type + "FROM"]
    data = ""
    if from_type == "String":
      data = self.dictMCVal[search_type + "STRING_DATA__STRING"]
    elif from_type == "Script":
      data = self.dictMCVal[search_type + "SCRIPT_DATA__SCRIPT_FILE"]
    elif from_type == "DataFile":
      data = self.dictMCVal[search_type + "DATA_DATA__DATA_FILE"]
    elif from_type == "ScriptWithSwitch":
      data = self.dictMCVal[search_type + "SCRIPTWITHSWITCH_DATA__SCRIPTWITHSWITCH_FILE"]
    elif from_type == "ScriptWithFunctions":
      data = self.dictMCVal[search_type + "SCRIPTWITHFUNCTIONS_DATA__SCRIPTWITHFUNCTIONS_FILE"]
    elif from_type == "ScriptWithOneFunction":
      data = self.dictMCVal[search_type + "SCRIPTWITHONEFUNCTION_DATA__SCRIPTWITHONEFUNCTION_FILE"]
    elif from_type == "FunctionDict":
      data = self.dictMCVal[search_type + "FUNCTIONDICT_DATA__FUNCTIONDICT_FILE"]
    else:
      raise Exception('From Type unknown', from_type)

    if from_type == "String" or from_type == "Script" or from_type == "DataFile":
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = '" + data_type + "'\n"
      self.text_da += data_name + "_config['From'] = '" + from_type + "'\n"
      self.text_da += data_name + "_config['Data'] = '" + data      + "'\n"
      if search_text+"Stored" in self.dictMCVal.keys():
        self.text_da += data_name + "_config['Stored'] = '" +  str(self.dictMCVal[search_text+"Stored"])  + "'\n"
      if search_type+"DATA_DATA__ColMajor" in self.dictMCVal.keys():
        self.text_da += data_name + "_config['ColMajor'] = '" +  str(self.dictMCVal[search_type+"DATA_DATA__ColMajor"])  + "'\n"
      self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"

    if from_type == "ScriptWithSwitch":
      self.text_da += data_name + "_ScriptWithSwitch = {}\n"
      self.text_da += data_name + "_ScriptWithSwitch['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"
      self.text_da += data_name + "_ScriptWithSwitch['Script'] = {}\n"
      self.text_da += data_name + "_ScriptWithSwitch['Script']['Direct'] = '"  + data + "'\n"
      self.text_da += data_name + "_ScriptWithSwitch['Script']['Tangent'] = '" + data + "'\n"
      self.text_da += data_name + "_ScriptWithSwitch['Script']['Adjoint'] = '" + data + "'\n"
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = 'Function'\n"
      self.text_da += data_name + "_config['From'] = 'ScriptWithSwitch'\n"
      self.text_da += data_name + "_config['Data'] = " + data_name + "_ScriptWithSwitch\n"
      self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"

    if from_type == "ScriptWithFunctions":
      self.text_da += data_name + "_ScriptWithFunctions = {}\n"
      self.text_da += data_name + "_ScriptWithFunctions['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"
      self.text_da += data_name + "_ScriptWithFunctions['Script'] = {}\n"
      self.text_da += data_name + "_ScriptWithFunctions['Script']['Direct'] = '"  + data + "'\n"
      self.text_da += data_name + "_ScriptWithFunctions['Script']['Tangent'] = '" + data + "'\n"
      self.text_da += data_name + "_ScriptWithFunctions['Script']['Adjoint'] = '" + data + "'\n"
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = 'Function'\n"
      self.text_da += data_name + "_config['From'] = 'ScriptWithFunctions'\n"
      self.text_da += data_name + "_config['Data'] = " + data_name + "_ScriptWithFunctions\n"
      self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"

    if from_type == "ScriptWithOneFunction":
      self.text_da += data_name + "_ScriptWithOneFunction = {}\n"
      self.text_da += data_name + "_ScriptWithOneFunction['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"
      self.text_da += data_name + "_ScriptWithOneFunction['Script'] = {}\n"
      self.text_da += data_name + "_ScriptWithOneFunction['Script']['Direct'] = '"  + data + "'\n"
      self.text_da += data_name + "_ScriptWithOneFunction['Script']['Tangent'] = '" + data + "'\n"
      self.text_da += data_name + "_ScriptWithOneFunction['Script']['Adjoint'] = '" + data + "'\n"
      self.text_da += data_name + "_ScriptWithOneFunction['DifferentialIncrement'] = " + str(float(self.dictMCVal[search_type + "SCRIPTWITHONEFUNCTION_DATA__DifferentialIncrement"])) + "\n"
      self.text_da += data_name + "_ScriptWithOneFunction['CenteredFiniteDifference'] = " + str(self.dictMCVal[search_type + "SCRIPTWITHONEFUNCTION_DATA__CenteredFiniteDifference"]) + "\n"
      if search_type + "SCRIPTWITHONEFUNCTION_DATA__EnableMultiProcessing" in self.dictMCVal.keys():
        self.text_da += data_name + "_ScriptWithOneFunction['EnableWiseParallelism'] = " + str(self.dictMCVal[search_type + "SCRIPTWITHONEFUNCTION_DATA__EnableMultiProcessing"]) + "\n"
      if search_type + "SCRIPTWITHONEFUNCTION_DATA__EnableWiseParallelism" in self.dictMCVal.keys():
        self.text_da += data_name + "_ScriptWithOneFunction['EnableWiseParallelism'] = " + str(self.dictMCVal[search_type + "SCRIPTWITHONEFUNCTION_DATA__EnableWiseParallelism"]) + "\n"
      if search_type + "SCRIPTWITHONEFUNCTION_DATA__NumberOfProcesses" in self.dictMCVal.keys():
        self.text_da += data_name + "_ScriptWithOneFunction['NumberOfProcesses'] = " + str(self.dictMCVal[search_type + "SCRIPTWITHONEFUNCTION_DATA__NumberOfProcesses"]) + "\n"
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = 'Function'\n"
      self.text_da += data_name + "_config['From'] = 'ScriptWithOneFunction'\n"
      self.text_da += data_name + "_config['Data'] = " + data_name + "_ScriptWithOneFunction\n"
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

  def add_init(self):

      init_file_data = self.dictMCVal["__"+self.type_of_study+"__UserDataInit__INIT_FILE"]
      init_target_list = self.dictMCVal["__"+self.type_of_study+"__UserDataInit__TARGET_LIST"]

      self.text_da += "Init_config = {}\n"
      self.text_da += "Init_config['Type'] = 'Dict'\n"
      self.text_da += "Init_config['From'] = 'Script'\n"
      self.text_da += "Init_config['Data'] = '" + init_file_data + "'\n"
      self.text_da += "Init_config['Target'] = ["
      if isinstance(init_target_list, "str"):
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
    elif from_type == "Template":
      tmpl = self.dictMCVal["__"+self.type_of_study+"__UserPostAnalysis__TEMPLATE_DATA__Template"]
      data = self.dictMCVal["__"+self.type_of_study+"__UserPostAnalysis__TEMPLATE_DATA__%s__ValueTemplate"%tmpl]
      self.text_da += "Analysis_config = {}\n"
      self.text_da += "Analysis_config['From'] = 'String'\n"
      self.text_da += "Analysis_config['Data'] = \"\"\"" + data + "\"\"\"\n"
      self.text_da += "study_config['UserPostAnalysis'] = Analysis_config\n"
    else:
      raise Exception('From Type unknown', from_type)

  def add_AlgorithmParameters(self):

    data_name = "AlgorithmParameters"
    data_type = "Dict"
    #
    if "__"+self.type_of_study+"__AlgorithmParameters__Parameters" in self.dictMCVal:
        para_type = self.dictMCVal["__"+self.type_of_study+"__AlgorithmParameters__Parameters"]
    else:
        para_type = "Defaults"
    #
    if para_type == "Defaults":
        from_type = para_type
    elif para_type == "Dict":
        from_type = self.dictMCVal["__"+self.type_of_study+"__AlgorithmParameters__Dict__data__FROM"]
    else:
        return

    if from_type == "Script":
      data = self.dictMCVal["__"+self.type_of_study+"__AlgorithmParameters__Dict__data__SCRIPT_DATA__SCRIPT_FILE"]
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = '" + data_type + "'\n"
      self.text_da += data_name + "_config['From'] = '" + from_type + "'\n"
      self.text_da += data_name + "_config['Data'] = '" + data + "'\n"
      self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"
    elif from_type == "String":
      data = self.dictMCVal["__"+self.type_of_study+"__AlgorithmParameters__Dict__data__STRING_DATA__STRING"]
      self.text_da += data_name + "_config = {}\n"
      self.text_da += data_name + "_config['Type'] = '" + data_type + "'\n"
      self.text_da += data_name + "_config['From'] = '" + from_type + "'\n"
      self.text_da += data_name + "_config['Data'] = '" + data + "'\n"
      self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"
    elif from_type == "Defaults":
      base = "__"+self.type_of_study+"__AlgorithmParameters__Parameters"
      keys = [k for k in self.dictMCVal.keys() if base in k]
      if base in keys: keys.remove(base)
      keys = [k.replace(base,'') for k in keys]
      data  = '{'
      for k in keys:
        key = k.split('__')[-1]
        val = self.dictMCVal[base+k]
        # print key," = ",val,"    ",type(val)
        if isinstance(val, str) and key == "SetSeed":
            data += '"%s":%s,'%(key,int(val))
        elif isinstance(val, str) and not (val.count('[')>=2 or val.count('(')>=2):
            data += '"%s":"%s",'%(key,val)
        else:
            data += '"%s":%s,'%(key,val)
      data = data.replace("'",'"')
      data += '}'
      if data != '{}':
          self.text_da += data_name + "_config = {}\n"
          self.text_da += data_name + "_config['Type'] = '" + data_type + "'\n"
          self.text_da += data_name + "_config['From'] = 'String'\n"
          self.text_da += data_name + "_config['Data'] = '" + data + "'\n"
          self.text_da += "study_config['" + data_name + "'] = " + data_name + "_config\n"

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
    number = 2
    self.text_da += "observers = {}\n"
    for observer in observers.keys():
      number += 1
      self.text_da += "observers[\"" + observer + "\"] = {}\n"
      self.text_da += "observers[\"" + observer + "\"][\"number\"] = " + str(number) + "\n"
      self.text_da += "observers[\"" + observer + "\"][\"nodetype\"] = \"" + observers[observer]["nodetype"] + "\"\n"
      if observers[observer]["nodetype"] == "String":
        self.text_da += "observers[\"" + observer + "\"][\"String\"] = \"\"\"" + observers[observer]["script"] + "\"\"\"\n"
      elif observers[observer]["nodetype"] == "Template":
        self.text_da += "observers[\"" + observer + "\"][\"String\"] = \"\"\"" + observers[observer]["script"] + "\"\"\"\n"
        self.text_da += "observers[\"" + observer + "\"][\"Template\"] = \"\"\"" + observers[observer]["template"] + "\"\"\"\n"
      else:
        self.text_da += "observers[\"" + observer + "\"][\"Script\"] = \"" + observers[observer]["file"] + "\"\n"
      if "scheduler" in observers[observer].keys():
        self.text_da += "observers[\"" + observer + "\"][\"scheduler\"] = \"\"\"" + observers[observer]["scheduler"] + "\"\"\"\n"
      if "info" in observers[observer].keys():
        self.text_da += "observers[\"" + observer + "\"][\"info\"] = \"\"\"" + observers[observer]["info"] + "\"\"\"\n"
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
    elif observers[observer]["nodetype"] == "Template":
      observers[observer]["nodetype"] = "String"
      observer_template_key = observer_eficas_name + "ObserverTemplate__"
      observers[observer]["template"] = self.dictMCVal[observer_template_key + "Template"]
      observers[observer]["script"]   = self.dictMCVal[observer_template_key + observers[observer]["template"] + "__ValueTemplate"]
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
