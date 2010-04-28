# -*- coding: utf-8 -*-
print "import generator_datassim"

from generator.generator_python import PythonGenerator

def entryPoint():
   """
      Retourne les informations necessaires pour le chargeur de plugins

      Ces informations sont retournees dans un dictionnaire
   """
   return {
        # Le nom du plugin
          'name' : 'datassim',
        # La factory pour creer une instance du plugin
          'factory' : DatassimGenerator,
          }

class DatassimGenerator(PythonGenerator):

  def __init__(self,cr=None):
    PythonGenerator.__init__(self, cr)
    self.dictMCVal={}
    self.text_comm = ""
    self.text_da = ""
    self.text_da_status = False

  def gener(self,obj,format='brut',config=None):
    print "DatassimGenerator gener"
    self.text_comm = PythonGenerator.gener(self, obj, format, config)

    print "Dictionnaire"
    print self.dictMCVal
    
    try :
      self.text_da_status = False
      self.generate_da()
      self.text_da_status = True
    except:
      print "Case seems not be correct"
      pass
    return self.text_comm

  def writeDefault(self, fn):
    if self.text_da_status:
      print "write datassim python command file"
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
    self.text_da += "study_config[\"Algorithm\"] = \"" + self.dictMCVal["ALGORITHM_NAME"] + "\"\n"


    self.add_data("Background")
    self.add_data("BackgroundError")
    self.add_data("Observation")
    self.add_data("ObservationError")
    self.add_data("ObservationOperator")
    self.add_analysis()

  def add_data(self, data_name):
    search_text = "__ASSIM_STUDY__ALGORITHM__" + self.dictMCVal["ALGORITHM_NAME"] + "__"
    back_search_text = search_text + data_name + "__"
    try :
      back_from = self.dictMCVal[back_search_text + "VECTOR__FROM"]
      back_data = self.dictMCVal[back_search_text + "VECTOR__DATA"]

      self.text_da += data_name + "_config = {} \n"
      self.text_da += data_name + "_config[\"Type\"] = \"Vector\" \n"
      self.text_da += data_name + "_config[\"From\"] = \"" + back_from + "\" \n"
      self.text_da += data_name + "_config[\"Data\"] = \"" + back_data + "\" \n"
      self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"
    except:
      pass
    try :
      back_from = self.dictMCVal[back_search_text + "MATRIX__FROM"]
      back_data = self.dictMCVal[back_search_text + "MATRIX__DATA"]

      self.text_da += data_name + "_config = {} \n"
      self.text_da += data_name + "_config[\"Type\"] = \"Matrix\" \n"
      self.text_da += data_name + "_config[\"From\"] = \"" + back_from + "\" \n"
      self.text_da += data_name + "_config[\"Data\"] = \"" + back_data + "\" \n"
      self.text_da += "study_config[\"" + data_name + "\"] = " + data_name + "_config \n"
    except:
      pass

  def add_analysis(self):
    search_text = "__ASSIM_STUDY__ALGORITHM__" + self.dictMCVal["ALGORITHM_NAME"] + "__Analysis__"
    try :
      ana_from = self.dictMCVal[search_text + "FROM"]
      print ana_from
      if ana_from == "String":
        ana_data = self.dictMCVal[search_text + "STRING_DATA__STRING"]
        self.text_da += "Analysis_config = {} \n"
        self.text_da += "Analysis_config[\"From\"] = \"String\" \n"
        self.text_da += "Analysis_config[\"Data\"] = \"\"\"" + ana_data + "\"\"\" \n"
        self.text_da += "study_config[\"Analysis\"] = Analysis_config \n"
        pass
      if ana_from == "File":
        ana_data = self.dictMCVal[search_text + "FILE_DATA__FILE"]
        self.text_da += "Analysis_config = {} \n"
        self.text_da += "Analysis_config[\"From\"] = \"File\" \n"
        self.text_da += "Analysis_config[\"Data\"] = \"" + ana_data + "\" \n"
        self.text_da += "study_config[\"Analysis\"] = Analysis_config \n"
        pass
    except:
      pass

