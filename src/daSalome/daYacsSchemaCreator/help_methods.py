#-*- coding: utf-8 -*-
# Copyright (C) 2010-2012 EDF R&D
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

import sys
import os
import traceback
import logging

from daYacsSchemaCreator.infos_daComposant import *

def check_args(args):

  logging.debug("Arguments are :" + str(args))
  if len(args) != 2:
    logging.fatal("Bad number of arguments: you have to provide two arguments (%d given)" % (len(args)))
    sys.exit(1)

def check_study(study_config):

  logging.debug("[check_env] study_config : " + str(study_config))

  # Check study_config
  if not isinstance(study_config, dict):
    logging.fatal("Study configuration is not a dictionnary")
    sys.exit(1)

  # Name
  if "Name" not in study_config:
    logging.fatal("Cannot found Name in the study configuration")
    sys.exit(1)

  # Algorithm
  if "Algorithm" not in study_config:
    logging.fatal("Cannot found Algorithm in the study configuration")
    sys.exit(1)
  else:
    if not (study_config["Algorithm"] in AssimAlgos or study_config["Algorithm"] in CheckAlgos):
      logging.fatal("Algorithm provided is unknow : " + str(study_config["Algorithm"]) +
                    "\n You can choose between : " + str(AssimAlgos)+" "+str(CheckAlgos))
      sys.exit(1)

  # Debug
  if "Debug" not in study_config:
    study_config["Debug"] = "0"

  # Repertory
  check_repertory = False
  repertory = ""
  if "Repertory" in study_config.keys():
    repertory = study_config["Repertory"]
    check_repertory = True
    if not os.path.isabs(repertory):
      logging.fatal("Study repertory should be an absolute path")
      logging.fatal("Repertory provided is %s" % repertory)
      sys.exit(1)

  # Check if all the data is provided
  for key in AlgoDataRequirements[study_config["Algorithm"]]:
    if key not in study_config.keys():
      logging.fatal("Cannot found " +  key + " in your study configuration !" +
                    "\n This key is mandatory into a study with " + study_config["Algorithm"] + " algorithm." +
                    "\n " + study_config["Algorithm"] + " requirements are " + str(AlgoDataRequirements[study_config["Algorithm"]]))
      sys.exit(1)

  # Data
  for key in study_config.keys():
    if key in AssimData:
      check_data(key, study_config[key], check_repertory, repertory)

  # UserDataInit
  if "UserDataInit" in study_config.keys():
    check_data("UserDataInit", study_config["UserDataInit"], check_repertory, repertory)

  # Variables
  check_variables("InputVariables", study_config)
  check_variables("OutputVariables", study_config)

  # Analyse
  if "UserPostAnalysis" in study_config.keys():
    analysis_config = study_config["UserPostAnalysis"]
    if "From" not in analysis_config:
      logging.fatal("UserPostAnalysis found but From is not defined in the analysis configuration !")
      sys.exit(1)
    else:
      if analysis_config["From"] not in AnalysisFromList:
        logging.fatal("Analysis From defined in the study configuration does not have a correct type : " + str(analysis_config["From"])
                      + "\n You can have : " + str(AnalysisFromList))
        sys.exit(1)
    if "Data" not in analysis_config:
      logging.fatal("Analysis found but Data is not defined in the analysis configuration !")
      sys.exit(1)

    if analysis_config["From"] == "Script":
      check_file_name = ""
      if check_repertory:
        check_file_name = os.path.join(repertory, os.path.basename(analysis_config["Data"]))
      else:
        check_file_name = analysis_config["Data"]
      if not os.path.exists(check_file_name):
        logging.fatal("A script file cannot be found")
        logging.fatal("File is %s" % check_file_name)
        sys.exit(1)

  # Check observers
  if "Observers" in study_config.keys():
    for obs_var in study_config["Observers"]:
      # Check du type
      if not isinstance(study_config["Observers"][obs_var], type({})):
        logging.fatal("An observer description has to be a Python dictionary")
        logging.fatal("Observer is %s" % obs_var)
        sys.exit(1)
      if "nodetype" not in study_config["Observers"][obs_var].keys():
        logging.fatal("An observer description must provide a nodetype")
        logging.fatal("Observer is %s" % obs_var)
        sys.exit(1)
      nodetype = study_config["Observers"][obs_var]["nodetype"]
      if not isinstance(study_config["Observers"][obs_var]["nodetype"], type("")):
        logging.fatal("An observer nodetype description must be a string")
        logging.fatal("Observer is %s" % obs_var)
        sys.exit(1)
      if nodetype != "String" and nodetype != "Script":
        logging.fatal("An observer nodetype must be equal to 'String' or 'Script'")
        logging.fatal("Observer is %s" % obs_var)
        sys.exit(1)
      if nodetype == "String":
        if "String" not in study_config["Observers"][obs_var].keys():
          logging.fatal("An observer with nodetype String must provide a String")
          logging.fatal("Observer is %s" % obs_var)
          sys.exit(1)
        if not isinstance(study_config["Observers"][obs_var]["String"], type("")):
          logging.fatal("An observer String description must be a string")
          logging.fatal("Observer is %s" % obs_var)
          sys.exit(1)
      if nodetype == "Script":
        if "Script" not in study_config["Observers"][obs_var].keys():
          logging.fatal("An observer with nodetype Script provide a Script")
          logging.fatal("Observer is %s" % obs_var)
          sys.exit(1)
        if not isinstance(study_config["Observers"][obs_var]["Script"], type("")):
          logging.fatal("An observer Script description must be a string")
          logging.fatal("Observer is %s" % obs_var)
          sys.exit(1)
      if "scheduler" in study_config["Observers"][obs_var].keys():
        if not isinstance(study_config["Observers"][obs_var]["scheduler"], type("")):
          logging.fatal("An observer scheduler description must be a string")
          logging.fatal("Observer is %s" % obs_var)
          sys.exit(1)

def check_variables(name, study_config):

  if name not in study_config.keys():
    logging.fatal("%s not found in your study configuration!" % name)
    sys.exit(1)

  variable_config = study_config[name]
  if "Order" not in variable_config.keys():
    logging.fatal("Order not found in the %s configuration!" % name)
    sys.exit(1)

  list_of_variables = variable_config["Order"]
  if not isinstance(list_of_variables, type([])):
    logging.fatal("Order sould be a list in the %s configuration!" % name)
    sys.exit(1)
  if len(list_of_variables) < 1:
    logging.fatal("Order should contain one or more names in the %s configuration!" % name)
    sys.exit(1)

  for var in list_of_variables:
    if var not in variable_config.keys():
      logging.fatal("Variable %s not found in the %s configuration!" % name)
      sys.exit(1)
    value = variable_config[var]
    try:
      value = int(value)
    except:
      loggind.fatal("Variable %s value cannot be converted in an integer in the %s configuration!" % name)
      sys.exit(1)

def check_data(data_name, data_config, repertory_check=False, repertory=""):

  logging.debug("[check_data] " + data_name)
  data_name_data = "Data"
  data_name_type = "Type"
  data_name_from = "From"

  if data_name_data not in data_config:
    logging.fatal(data_name +" found but " + data_name_data +" is not defined in the study configuration !")
    sys.exit(1)

  if data_name_type not in data_config:
    logging.fatal(data_name +" found but " + data_name_type  +" is not defined in the study configuration !")
    sys.exit(1)
  else:
    if data_config[data_name_type] not in AssimType[data_name]:
      logging.fatal(data_name_type + " of " + data_name + " defined in the study configuration does not have a correct type : " + str(data_config[data_name_type]) 
                    + "\n You can have : " + str(AssimType[data_name]))
      sys.exit(1)
  if data_name_from not in data_config:
    logging.fatal(data_name + " found but " + data_name_from + " is not defined in the study configuration !")
    sys.exit(1)
  else:
    if data_config[data_name_from] not in FromNumpyList[data_config[data_name_type]]:
      logging.fatal(data_name_from + " of " + data_name + " defined in the study configuration does not have a correct value : " + str(data_config[data_name_from]) 
                    + "\n You can have : " + str(FromNumpyList[data_config[data_name_type]]))
      sys.exit(1)

  # Check des fichiers
  from_type = data_config["From"]
  if from_type == "Script":
    check_file_name = ""
    if repertory_check:
      check_file_name = os.path.join(repertory, os.path.basename(data_config["Data"]))
    else:
      check_file_name = data_config["Data"]
    if not os.path.exists(check_file_name):
      logging.fatal("A script file cannot be found")
      logging.fatal("File is %s" % check_file_name)
      sys.exit(1)
  elif from_type == "FunctionDict":
    FunctionDict = data_config["Data"]
    for FunctionName in FunctionDict["Function"]:
      check_file_name = ""
      if repertory_check:
        check_file_name = os.path.join(repertory, os.path.basename(FunctionDict["Script"][FunctionName]))
      else:
        check_file_name = FunctionDict["Script"][FunctionName]
      if not os.path.exists(check_file_name):
        logging.fatal("A script file cannot be found")
        logging.fatal("File is %s" % check_file_name)
        sys.exit(1)
