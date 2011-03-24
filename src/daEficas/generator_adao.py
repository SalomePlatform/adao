# -*- coding: utf-8 -*-
print "import generator_adao"

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
    self.logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
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
      print obj
      print obj.get_genealogie()
      clef=clef+"__"+i
    self.dictMCVal[clef]=obj.valeur

    s=PythonGenerator.generMCSIMP(self,obj)
    return s

  def generate_da(self):

    self.text_da += "#-*-coding:iso-8859-1-*- \n"
    self.text_da += "study_config = {} \n"

    # Extraction de Study_name
    self.text_da += "study_config[\"Name\"] = \"" + self.dictMCVal["__ASSIMILATION_STUDY__Study_name"] + "\"\n"
    # Extraction de Debug
    self.text_da += "study_config[\"Debug\"] = \"" + str(self.dictMCVal["__ASSIMILATION_STUDY__Debug"]) + "\"\n"
    # Extraction de Algorithm
    self.text_da += "study_config[\"Algorithm\"] = \"" + self.dictMCVal["__ASSIMILATION_STUDY__Algorithm"] + "\"\n"

    self.add_data("Background")
    self.add_data("BackgroundError")
    self.add_data("Observation")
    self.add_data("ObservationError")
    self.add_data("ObservationOperator")

    self.add_variables()
    # Parametres optionnels

    # Extraction du Study_repertory
    if "__ASSIMILATION_STUDY__Study_repertory" in self.dictMCVal.keys():
      self.text_da += "study_config[\"Repertory\"] = \"" + self.dictMCVal["__ASSIMILATION_STUDY__Study_repertory"] + "\"\n"
    # Extraction de AlgorithmParameters
    if "__ASSIMILATION_STUDY__AlgorithmParameters__INPUT_TYPE" in self.dictMCVal.keys():
      self.add_algorithm_parameters()
    # Extraction de UserPostAnalysis
    if "__ASSIMILATION_STUDY__UserPostAnalysis__FROM" in self.dictMCVal.keys():
      self.add_UserPostAnalysis()
    if "__ASSIMILATION_STUDY__UserDataInit__INIT_FILE" in self.dictMCVal.keys():
      self.add_init()

  def add_data(self, data_name):

    # Extraction des données
    search_text = "__ASSIMILATION_STUDY__" + data_name + "__"
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
      self.text_da += data_name + "_config = {} \n"
      self.text_da += data_name + "_config[\"Type\"] = \"" + data_type + "\" \n"
      self.text_da += data_name + "_config[\"From\"] = \"" + from_type + "\" \n"
      self.text_da += data_name + "_config[\"Data\"] = \"" + data      + "\" \n"
      self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"

    if from_type == "FunctionDict":
      self.text_da += data_name + "_FunctionDict = {} \n"
      self.text_da += data_name + "_FunctionDict[\"Function\"] = [\"Direct\", \"Tangent\", \"Adjoint\"] \n"
      self.text_da += data_name + "_FunctionDict[\"Script\"] = {} \n"
      self.text_da += data_name + "_FunctionDict[\"Script\"][\"Direct\"] = \""  + data + "\" \n"
      self.text_da += data_name + "_FunctionDict[\"Script\"][\"Tangent\"] = \"" + data + "\" \n"
      self.text_da += data_name + "_FunctionDict[\"Script\"][\"Adjoint\"] = \"" + data + "\" \n"
      self.text_da += data_name + "_config = {} \n"
      self.text_da += data_name + "_config[\"Type\"] = \"Function\" \n"
      self.text_da += data_name + "_config[\"From\"] = \"FunctionDict\" \n"
      self.text_da += data_name + "_config[\"Data\"] = " + data_name + "_FunctionDict \n"
      self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"

  def add_algorithm_parameters(self):

    data_name = "AlgorithmParameters"
    data_type = "Dict"
    from_type = "Script"
    data = self.dictMCVal["__ASSIMILATION_STUDY__AlgorithmParameters__Dict__data__SCRIPT_DATA__SCRIPT_FILE"]

    self.text_da += data_name + "_config = {} \n"
    self.text_da += data_name + "_config[\"Type\"] = \"" + data_type + "\" \n"
    self.text_da += data_name + "_config[\"From\"] = \"" + from_type + "\" \n"
    self.text_da += data_name + "_config[\"Data\"] = \"" + data + "\" \n"
    self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"

  def add_init(self):

      init_file_data = self.dictMCVal["__ASSIMILATION_STUDY__UserDataInit__INIT_FILE"]
      init_target_list = self.dictMCVal["__ASSIMILATION_STUDY__UserDataInit__TARGET_LIST"]

      self.text_da += "Init_config = {} \n"
      self.text_da += "Init_config[\"Type\"] = \"Dict\" \n"
      self.text_da += "Init_config[\"From\"] = \"Script\" \n"
      self.text_da += "Init_config[\"Data\"] = \"" + init_file_data + "\"\n"
      self.text_da += "Init_config[\"Target\"] = ["
      for target in init_target_list:
        self.text_da += "\"" + target + "\","
      self.text_da += "] \n"
      self.text_da += "study_config[\"UserDataInit\"] = Init_config \n"

  def add_UserPostAnalysis(self):

    from_type = self.dictMCVal["__ASSIMILATION_STUDY__UserPostAnalysis__FROM"]
    data = ""
    if from_type == "String":
      data = self.dictMCVal["__ASSIMILATION_STUDY__UserPostAnalysis__STRING_DATA__STRING"]
      self.text_da += "Analysis_config = {} \n"
      self.text_da += "Analysis_config[\"From\"] = \"String\" \n"
      self.text_da += "Analysis_config[\"Data\"] = \"\"\"" + data + "\"\"\" \n"
      self.text_da += "study_config[\"UserPostAnalysis\"] = Analysis_config \n"
    elif from_type == "Script":
      data = self.dictMCVal["__ASSIMILATION_STUDY__UserPostAnalysis__SCRIPT_DATA__SCRIPT_FILE"]
      self.text_da += "Analysis_config = {} \n"
      self.text_da += "Analysis_config[\"From\"] = \"Script\" \n"
      self.text_da += "Analysis_config[\"Data\"] = \"" + data + "\" \n"
      self.text_da += "study_config[\"UserPostAnalysis\"] = Analysis_config \n"
    else:
      raise Exception('From Type unknown', from_type)

  def add_variables(self):

    # Input variables
    if "__ASSIMILATION_STUDY__InputVariables__NAMES" in self.dictMCVal.keys():
      names = []
      sizes = []
      if isinstance(self.dictMCVal["__ASSIMILATION_STUDY__InputVariables__NAMES"], type("")):
        names.append(self.dictMCVal["__ASSIMILATION_STUDY__InputVariables__NAMES"])
      else:
        names = self.dictMCVal["__ASSIMILATION_STUDY__InputVariables__NAMES"]
      if isinstance(self.dictMCVal["__ASSIMILATION_STUDY__InputVariables__SIZES"], type(1)):
        sizes.append(self.dictMCVal["__ASSIMILATION_STUDY__InputVariables__SIZES"])
      else:
        sizes = self.dictMCVal["__ASSIMILATION_STUDY__InputVariables__SIZES"]

      self.text_da += "inputvariables_config = {} \n"
      for name, size in zip(names, sizes):
        self.text_da += "inputvariables_config[\"%s\"] = %s \n" % (name,size)
      self.text_da += "study_config[\"InputVariables\"] = inputvariables_config \n"
    else:
      self.text_da += "inputvariables_config = {} \n"
      self.text_da += "inputvariables_config[\"adao_default\"] = -1 \n"
      self.text_da += "study_config[\"InputVariables\"] = inputvariables_config \n"

    # Output variables
    if "__ASSIMILATION_STUDY__OutputVariables__NAMES" in self.dictMCVal.keys():
      names = []
      sizes = []
      if isinstance(self.dictMCVal["__ASSIMILATION_STUDY__OutputVariables__NAMES"], type("")):
        names.append(self.dictMCVal["__ASSIMILATION_STUDY__OutputVariables__NAMES"])
      else:
        names = self.dictMCVal["__ASSIMILATION_STUDY__OutputVariables__NAMES"]
      if isinstance(self.dictMCVal["__ASSIMILATION_STUDY__OutputVariables__SIZES"], type(1)):
        sizes.append(self.dictMCVal["__ASSIMILATION_STUDY__OutputVariables__SIZES"])
      else:
        sizes = self.dictMCVal["__ASSIMILATION_STUDY__OutputVariables__SIZES"]

      self.text_da += "outputvariables_config = {} \n"
      for name, size in zip(names, sizes):
        self.text_da += "outputvariables_config[\"%s\"] = %s \n" % (name,size)
      self.text_da += "study_config[\"OutputVariables\"] = outputvariables_config \n"
    else:
      self.text_da += "outputvariables_config = {} \n"
      self.text_da += "outputvariables_config[\"adao_default\"] = -1 \n"
      self.text_da += "study_config[\"OutputVariables\"] = outputvariables_config \n"
