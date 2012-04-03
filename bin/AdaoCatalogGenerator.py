#-*- coding:utf-8 -*-
#  Copyright (C) 2008-2011  EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public
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
# --
# Author : André RIBES (EDF R&D)
# --

import logging
import traceback
import sys
import string
import StringIO

logging.basicConfig(level=logging.INFO)

#----------- Templates Part ---------------#
begin_catalog_file = """
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# generated by AdaoCatalogGenerator at ${date}
# --------------------------------------------------------

import Accas
from Accas import *

JdC = JDC_CATA (code = 'ADAO',
                execmodul = None,
                regles = ( AU_MOINS_UN ('ASSIMILATION_STUDY'), AU_PLUS_UN ('ASSIMILATION_STUDY')),
               )
"""

data_method = """
def F_${data_name}(statut) : return FACT(statut = statut,
                                         FROM = SIMP(statut = "o", typ = "TXM", into=(${data_into}), defaut=${data_default}),
                                         SCRIPT_DATA = BLOC ( condition = " FROM in ( 'Script', ) ",

                                                      SCRIPT_FILE = SIMP(statut = "o", typ = "FichierNoAbs", validators=(OnlyStr())),
                                                     ),
                                         STRING_DATA = BLOC ( condition = " FROM in ( 'String', ) ",

                                                      STRING = SIMP(statut = "o", typ = "TXM"),
                                                     ),
                                         FUNCTIONDICT_DATA = BLOC ( condition = " FROM in ( 'FunctionDict', ) ",

                                                      FUNCTIONDICT_FILE = SIMP(statut = "o", typ = "FichierNoAbs", validators=(OnlyStr())),
                                                     ),
                                    )
"""

init_method = """
def F_InitChoice() : return  ("Background",
                              "BackgroundError",
                              "Observation",
                              "ObservationError",
                              "ObservationOperator",
                              "AlgorithmParameters",
                              "UserPostAnalysis",
                             )

def F_Init(statut) : return FACT(statut = statut,
                                 INIT_FILE = SIMP(statut = "o", typ = "FichierNoAbs", validators=(OnlyStr())),
                                 TARGET_LIST = SIMP(statut = "o", typ = "TXM", min=1, max="**", into=F_InitChoice(),  validators=(VerifExiste(2))),
                                )
"""

assim_data_method = """
def F_${assim_name}(statut) : return FACT(statut=statut,
                                          INPUT_TYPE = SIMP(statut="o", typ = "TXM", into=(${choices}), defaut=${default_choice}),
${decl_choices}
                                                )
"""

assim_data_choice = """
                                                 ${choice_name} = BLOC ( condition = " INPUT_TYPE in ( '${choice_name}', ) ",
                                                 data = F_${choice_name}("o"),
                                                 ),
"""

observers_choice = """
                                       ${var_name} = BLOC (condition=" '${var_name}' in set(SELECTION) ",
                                                  ${var_name}_data = FACT(statut = "o",
                                                             Scheduler = SIMP(statut = "f", typ = "TXM"),
                                                             Info      = SIMP(statut = "f", typ = "TXM"),
                                                             NodeType  = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "", into=("String", "Script")),
                                                             PythonScript = BLOC (condition = " NodeType == 'String' ",
                                                                                  Value = SIMP(statut = "o", typ = "TXM")
                                                                                 ),
                                                             UserFile = BLOC (condition = " NodeType == 'Script' ",
                                                                              Value = SIMP(statut = "o", typ = "FichierNoAbs", validators=(OnlyStr()))
                                                                             )
                                                                      ),
                                                          ),
"""

observers_method = """
def F_Observers(statut) : return FACT(statut=statut,
                                      SELECTION = SIMP(statut="o", defaut=[], typ="TXM", min=0, max="**", validators=NoRepeat(), into=(${choices})),
${decl_choices}
                                     )
"""

assim_study = """

def F_variables(statut) : return FACT(statut=statut,
                                      regles = ( MEME_NOMBRE ('NAMES', 'SIZES')),
                                      NAMES = SIMP(statut="o", typ="TXM", max="**", validators=NoRepeat()),
                                      SIZES = SIMP(statut="o", typ="I", val_min=1, max="**")
                                      )

ASSIMILATION_STUDY = PROC(nom="ASSIMILATION_STUDY",
                          op=None,
                          repetable           = "n",
                          Study_name          = SIMP(statut="o", typ = "TXM"),
                          Study_repertory     = SIMP(statut="f", typ = "TXM"),
                          Debug               = SIMP(statut="o", typ = "I", into=(0, 1), defaut=0),
                          Algorithm           = SIMP(statut="o", typ = "TXM", into=(${algos_names})),
                          Background          = F_Background("o"),
                          BackgroundError     = F_BackgroundError("o"),
                          Observation         = F_Observation("o"),
                          ObservationError    = F_ObservationError("o"),
                          ObservationOperator = F_ObservationOperator("o"),
                          AlgorithmParameters = F_AlgorithmParameters("f"),
                          UserDataInit        = F_Init("f"),
                          UserPostAnalysis    = F_UserPostAnalysis("f"),
                          InputVariables      = F_variables("f"),
                          OutputVariables     = F_variables("f"),
                          Observers           = F_Observers("f")
                         )
"""

begin_catalog_file = string.Template(begin_catalog_file)
data_method = string.Template(data_method)
assim_data_method = string.Template(assim_data_method)
assim_data_choice = string.Template(assim_data_choice)
assim_study = string.Template(assim_study)
observers_method = string.Template(observers_method)
observers_choice = string.Template(observers_choice)

#----------- End of Templates Part ---------------#



#----------- Begin generation script -----------#
print "-- Starting AdaoCalatogGenerator.py --"

try:
  import daEficas
  import daYacsSchemaCreator
  import daCore.AssimilationStudy
  import daYacsSchemaCreator.infos_daComposant as infos
except:
  logging.fatal("Import of ADAO python modules failed !" +
                "\n add ADAO python installation directory in your PYTHONPATH")
  traceback.print_exc()
  sys.exit(1)

def check_args(args):
  logging.debug("Arguments are :" + str(args))
  if len(args) != 2:
    logging.fatal("Bad number of arguments: you have to provide two arguments (%d given)" % (len(args)))
    sys.exit(1)

# Parse arguments
from optparse import OptionParser
usage = "usage: %prog [options] catalog_path catalog_name"
version="%prog 0.1"
my_parser = OptionParser(usage=usage, version=version)
(options, args) = my_parser.parse_args()
check_args(args)

catalog_path =  args[0]
catalog_name =  args[1]

# Generates into a string
mem_file = StringIO.StringIO()

# Start file
from time import strftime
mem_file.write(begin_catalog_file.substitute(date=strftime("%Y-%m-%d %H:%M:%S")))

# Step 1: A partir des infos, on crée les fonctions qui vont permettre
# d'entrer les données utilisateur
for data_input_name in infos.DataTypeDict.keys():
  logging.debug('A data input Type is found: ' + data_input_name)
  data_name = data_input_name
  data_into = ""
  data_default = ""

  # On récupère les différentes façon d'entrer les données
  for basic_type in infos.DataTypeDict[data_input_name]:
    data_into += "\"" + basic_type + "\", "

  # On choisit le défault
  data_default = "\"" + infos.DataTypeDefaultDict[data_input_name] + "\""

  mem_file.write(data_method.substitute(data_name    = data_name,
                                        data_into    = data_into,
                                        data_default = data_default))

# Step 2: On crée les fonctions qui permettent de rentrer les données des algorithmes
for assim_data_input_name in infos.AssimDataDict.keys():
  logging.debug("An assimilation algorithm data input is found: " + assim_data_input_name)
  assim_name = assim_data_input_name
  choices = ""
  default_choice = ""
  decl_choices = ""
  decl_opts = ""
  for choice in infos.AssimDataDict[assim_data_input_name]:
    choices += "\"" + choice + "\", "
    decl_choices += assim_data_choice.substitute(choice_name = choice)
  default_choice = "\"" + infos.AssimDataDefaultDict[assim_data_input_name] + "\""

  mem_file.write(assim_data_method.substitute(assim_name = assim_name,
                                              choices = choices,
                                              decl_choices = decl_choices,
                                              default_choice=default_choice))

# Step 3: On ajoute les fonctions représentant les options possibles
for opt_name in infos.OptDict.keys():
  logging.debug("An optional node is found: " + opt_name)
  data_name = opt_name
  data_into = ""
  data_default = ""

  for choice in infos.OptDict[opt_name]:
    data_into += "\"" + choice + "\", "
  data_default = "\"" + infos.OptDefaultDict[opt_name] + "\""

  mem_file.write(data_method.substitute(data_name = data_name,
                                        data_into = data_into,
                                        data_default = data_default))

# Step 4: On ajoute la méthode optionnelle init
# TODO uniformiser avec le step 3
mem_file.write(init_method)

# Step 5: Add observers
decl_choices = ""
for obs_var in infos.ObserversList:
  decl_choices += observers_choice.substitute(var_name=obs_var)
mem_file.write(observers_method.substitute(choices = infos.ObserversList,
                                           decl_choices = decl_choices))

# Final step: Add algorithm and assim_study
algos_names = ""
decl_algos = ""

assim_study_object = daCore.AssimilationStudy.AssimilationStudy()
algos_list = assim_study_object.get_available_algorithms()
for algo_name in algos_list:
  logging.debug("An assimilation algorithm is found: " + algo_name)
  algos_names += "\"" + algo_name + "\", "

mem_file.write(assim_study.substitute(algos_names=algos_names,
                                      decl_algos=decl_algos))
# Write file
final_file = open(catalog_path + "/" + catalog_name, "wr")
final_file.write(mem_file.getvalue())
mem_file.close()
final_file.close()

