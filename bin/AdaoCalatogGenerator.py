#-*- coding:utf-8 -*-
#  Copyright (C) 2008-2009  EDF R&D
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

logging.basicConfig(level=logging.DEBUG)

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
                regles = ( AU_MOINS_UN ('ASSIM_STUDY')),
               )
"""

String_data_bloc = """
                                     STRING_DATA = BLOC ( condition = " FROM in ( 'String', ) ",

                                                  STRING = SIMP(statut = "o", typ = "TXM"),
                                                 ),
"""

Script_data_bloc = """
                                     SCRIPT_DATA = BLOC ( condition = " FROM in ( 'Script', ) ",

                                                  SCRIPT_FILE = SIMP(statut = "o", typ = "Fichier"),
                                                 ),
"""

Dict_data_bloc = """
                                     DICT_DATA = BLOC ( condition = " FROM in ( 'Script', ) ",

                                                  SCRIPT_FILE = SIMP(statut = "o", typ = "Fichier"),
                                                 ),
"""

# Pour l'instant on ne gère qu'un seul script pour toutes les functions
FunctionDict_data_bloc = """
                                     FUNCTIONDICT_DATA = BLOC ( condition = " FROM in ( 'FunctionDict', ) ",

                                                  FUNCTIONDICT_FILE = SIMP(statut = "o", typ = "Fichier"),
                                                 ),
"""

data_method = """
def F_${data_name}(statut) : return FACT(statut = statut,
                                         FROM = SIMP(statut = "o", typ = "TXM", into=(${data_into})),
${data_bloc}
                                    )
"""

init_method = """
def F_InitChoice() : return  ("Background",
                              "BackgroundError",
                              "Observation",
                              "ObservationError",
                              "ObservationOperator",
                              "AlgorithmParameters",
                              "Analysis",
                             )
def F_Init(statut) : return FACT(statut = statut,
                                 INIT_FILE = SIMP(statut = "o", typ = "Fichier"),
                                 TARGET_LIST = SIMP(statut = "o", typ = "TXM", min=1, max="**", into=F_InitChoice(),  validators=(VerifExiste(2))),
                                )
"""
assim_data_method = """
def F_${assim_name}(statut) : return FACT(statut=statut,
                                          regles = ( UN_PARMI (${choices})),
${decl_choices}
                                                )
"""

assim_data_choice = """
                                                 ${choice_name} = F_${choice_name}("f"),
"""

assim_opt_choice = """
                                                 ${choice_name} = F_${choice_name}("f"),
"""

assim_algo = """
                                     ${name} = FACT(regles = ( ENSEMBLE ("Background", "BackgroundError", 
                                                                      "Observation", "ObservationError",
                                                                      "ObservationOperator")),
                                                 Background = F_Background("o"),
                                                 BackgroundError = F_BackgroundError("o"),
                                                 Observation = F_Observation("o"),
                                                 ObservationError = F_ObservationError("o"),
                                                 ObservationOperator = F_ObservationOperator("o"),
                                                 AlgorithmParameters = F_AlgorithmParameters("f"),
                                                 Init = F_Init("f"),
${decl_opts}
                                                ),
"""
assim_study = """
ASSIM_STUDY = PROC(nom="ASSIM_STUDY",
                   op=None,
                   repetable = "n",
                   STUDY_NAME = SIMP(statut="o", typ = "TXM"),
                   ALGORITHM  = FACT(statut='o',
                                     regles = ( UN_PARMI (${algos}),),
${decl_algos}
                                    ),
                  )
"""

begin_catalog_file = string.Template(begin_catalog_file)
data_method = string.Template(data_method)
assim_data_method = string.Template(assim_data_method)
assim_data_choice = string.Template(assim_data_choice)
assim_opt_choice = string.Template(assim_opt_choice)
assim_algo = string.Template(assim_algo)
assim_study = string.Template(assim_study)

#----------- End of Templates Part ---------------#



#----------- Begin generation script -----------#
print "-- Starting AdaoCalatogGenerator.py --"

try:
  import daEficas
  import daYacsSchemaCreator
  import daCore.AssimilationStudy
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

# Step 1: Check basic data input types
import daYacsSchemaCreator.infos_daComposant as infos
for basic_type in infos.BasicDataInputs:
  logging.debug('A basic data input type is found: ' + basic_type)
  if basic_type + '_data_bloc' not in locals().keys():
    logging.fatal("Basic data input type not found: " + basic_type)
    sys.exit(1)

# Step 2: Add data input dict
for data_input_name in infos.DataTypeDict.keys():
  logging.debug('A data input is found: ' + data_input_name)
  data_name = data_input_name
  data_into = ""
  data_bloc = ""

  for basic_type in infos.DataTypeDict[data_input_name]:
    data_into += "\"" + basic_type + "\", "
    data_bloc += locals()[basic_type + '_data_bloc'] + "\n"

  mem_file.write(data_method.substitute(data_name = data_name,
                                        data_into = data_into,
                                        data_bloc = data_bloc))

# Step 3: Add assimilation algorithm data input
for assim_data_input_name in infos.AssimDataDict.keys():
  logging.debug("An assimilation algorithm data input is found: " + assim_data_input_name)
  assim_name = assim_data_input_name
  choices = ""
  decl_choices = ""
  decl_opts = ""
  for choice in infos.AssimDataDict[assim_data_input_name]:
    choices += "\"" + choice + "\", "
    decl_choices += assim_data_choice.substitute(choice_name = choice)

  mem_file.write(assim_data_method.substitute(assim_name = assim_name,
                                              choices = choices,
                                              decl_choices = decl_choices))

# Step 4: Add optional nodes
opt_names = []
for opt_name in infos.OptDict.keys():
  logging.debug("An optional node is found: " + opt_name)
  data_name = opt_name
  data_into = ""
  data_bloc = ""

  for choice in infos.OptDict[opt_name]:
    data_into += "\"" + choice + "\", "
    data_bloc += locals()[choice + '_data_bloc'] + "\n"

  mem_file.write(data_method.substitute(data_name = data_name,
                                        data_into = data_into,
                                        data_bloc = data_bloc))

  opt_names.append(opt_name)

# Step 5: Add init node
mem_file.write(init_method)

# Final step: Add algorithm and assim_study
algos = ""
decl_algos = ""
decl_opts = ""
for opt_name in opt_names:
  decl_opts += assim_opt_choice.substitute(choice_name = opt_name)

assim_study_object = daCore.AssimilationStudy.AssimilationStudy()
algos_list = assim_study_object.get_available_algorithms()
for algo_name in algos_list:
  logging.debug("An assimilation algorithm is found: " + algo_name)
  if algo_name == "3DVAR":
    algo_name = "ThreeDVAR"
  algos += "\"" + algo_name + "\", "
  decl_algos += assim_algo.substitute(name = algo_name, decl_opts=decl_opts) + "\n"

mem_file.write(assim_study.substitute(algos=algos,
                                      decl_algos=decl_algos))
# Write file
final_file = open(catalog_path + "/" + catalog_name, "wr")
final_file.write(mem_file.getvalue())
mem_file.close()
final_file.close()

