# -*- coding: utf-8 -*-
print "import generator_adao"

from generator.generator_python import PythonGenerator
import traceback

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

  def gener(self,obj,format='brut',config=None):
    print "AdaoGenerator gener"
    self.text_comm = PythonGenerator.gener(self, obj, format, config)

    print "Dictionnaire"
    print self.dictMCVal

    try :
      self.text_da_status = False
      self.generate_da()
      self.text_da_status = True
    except:
      print "Case seems not be correct"
      traceback.print_exc()
      pass
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

  def generMCFACT(self,obj):

   if obj.parent.nom == "ALGORITHM":
     self.dictMCVal["ALGORITHM_NAME"] = obj.nom

   s=PythonGenerator.generMCFACT(self,obj)
   return s

  def generate_da(self):

    self.text_da += "#-*-coding:iso-8859-1-*- \n"
    self.text_da += "study_config = {} \n"
    self.text_da += "study_config[\"Name\"] = \"" + self.dictMCVal["__ASSIM_STUDY__STUDY_NAME"] + "\"\n"
    
    if self.dictMCVal["ALGORITHM_NAME"] != "ThreeDVAR":
      self.text_da += "study_config[\"Algorithm\"] = \"" + self.dictMCVal["ALGORITHM_NAME"] + "\"\n"
    else:
      self.text_da += "study_config[\"Algorithm\"] = \"3DVAR\"\n"


    self.add_data("Background")
    self.add_data("BackgroundError")
    self.add_data("Observation")
    self.add_data("ObservationError")
    self.add_data("ObservationOperator")

    # Optionnel
    self.add_analysis()

  def add_data(self, data_name):
    search_text = "__ASSIM_STUDY__ALGORITHM__" + self.dictMCVal["ALGORITHM_NAME"] + "__"
    back_search_text = search_text + data_name + "__"

    # Data is a Vector
    search_vector = back_search_text + "Vector"
    if search_vector + "__FROM" in self.dictMCVal:
      back_from = self.dictMCVal[search_vector + "__FROM"]

      search_string = search_vector + "__STRING_DATA__STRING"
      search_script = search_vector + "__SCRIPT_DATA__SCRIPT_FILE"

      # Vector is from a string
      if search_string in self.dictMCVal:
        back_data = self.dictMCVal[search_string]
      # Vector is from a script
      elif search_script in self.dictMCVal:
        back_data = self.dictMCVal[search_script]
      else:
        print "[generator adao] Error cannot found Vector data"

      self.text_da += data_name + "_config = {} \n"
      self.text_da += data_name + "_config[\"Type\"] = \"Vector\" \n"
      self.text_da += data_name + "_config[\"From\"] = \"" + back_from + "\" \n"
      self.text_da += data_name + "_config[\"Data\"] = \"" + back_data + "\" \n"
      self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"
      return 1

    # Data is a Matrix
    search_matrix = back_search_text + "Matrix"
    if search_matrix + "__FROM" in self.dictMCVal:
      back_from = self.dictMCVal[search_matrix + "__FROM"]

      search_string = search_matrix + "__STRING_DATA__STRING"
      search_script = search_matrix + "__SCRIPT_DATA__SCRIPT_FILE"

      # Matrix is from a string
      if search_string in self.dictMCVal:
        back_data = self.dictMCVal[search_string]
      # Matrix is from a script
      elif search_script in self.dictMCVal:
        back_data = self.dictMCVal[search_script]
      else:
        print "[generator adao] Error cannot found Matrix data"

      self.text_da += data_name + "_config = {} \n"
      self.text_da += data_name + "_config[\"Type\"] = \"Matrix\" \n"
      self.text_da += data_name + "_config[\"From\"] = \"" + back_from + "\" \n"
      self.text_da += data_name + "_config[\"Data\"] = \"" + back_data + "\" \n"
      self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"
      return 1

    # Data is a FunctionDict
    search_function = back_search_text + "Function"
    if search_function + "__FROM" in self.dictMCVal:
      back_from = self.dictMCVal[search_function + "__FROM"]
      back_data = self.dictMCVal[search_function + "__FUNCTIONDICT_DATA__FUNCTIONDICT_FILE"]

      self.text_da += "FunctionDict = {} \n"
      self.text_da += "FunctionDict[\"Function\"] = [\"Direct\", \"Tangent\", \"Adjoint\"] \n"
      self.text_da += "FunctionDict[\"Script\"] = {} \n"
      self.text_da += "FunctionDict[\"Script\"][\"Direct\"] = \"" + back_data + "\" \n"
      self.text_da += "FunctionDict[\"Script\"][\"Tangent\"] = \"" + back_data + "\" \n"
      self.text_da += "FunctionDict[\"Script\"][\"Adjoint\"] = \"" + back_data + "\" \n"
      self.text_da += data_name + "_config = {} \n"
      self.text_da += data_name + "_config[\"Type\"] = \"Function\" \n"
      self.text_da += data_name + "_config[\"From\"] = \"FunctionDict\" \n"
      self.text_da += data_name + "_config[\"Data\"] = FunctionDict \n"
      self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"
      return 1

  def add_analysis(self):
    search_text = "__ASSIM_STUDY__ALGORITHM__" + self.dictMCVal["ALGORITHM_NAME"] + "__Analysis__"
    try :
      ana_from = self.dictMCVal[search_text + "FROM"]

      if ana_from == "String":
        ana_data = self.dictMCVal[search_text + "STRING_DATA__STRING"]
        self.text_da += "Analysis_config = {} \n"
        self.text_da += "Analysis_config[\"From\"] = \"String\" \n"
        self.text_da += "Analysis_config[\"Data\"] = \"\"\"" + ana_data + "\"\"\" \n"
        self.text_da += "study_config[\"Analysis\"] = Analysis_config \n"
        pass
      if ana_from == "Script":
        ana_data = self.dictMCVal[search_text + "SCRIPT_DATA__SCRIPT_FILE"]
        self.text_da += "Analysis_config = {} \n"
        self.text_da += "Analysis_config[\"From\"] = \"Script\" \n"
        self.text_da += "Analysis_config[\"Data\"] = \"" + ana_data + "\" \n"
        self.text_da += "study_config[\"Analysis\"] = Analysis_config \n"
        pass
    except:
      pass

