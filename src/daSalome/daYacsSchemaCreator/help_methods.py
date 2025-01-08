#-*- coding: utf-8 -*-
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import sys
import os
import traceback
import logging

from daYacsSchemaCreator.infos_daComposant import *

def check_args(args):

  logging.debug("Arguments are :" + str(args))
  if len(args) != 2:
    raise ValueError("\n\n Bad number of arguments: you have to provide two arguments (%d given)\n" % (len(args)))

def check_study(study_config):

  logging.debug("[check_env] study_config : " + str(study_config))

  # Check study_config
  if not isinstance(study_config, dict):
    raise ValueError("\n\n Study configuration is not a dictionnary!\n")

  # Name
  if "Name" not in study_config:
    raise ValueError("\n\n Cannot find Name in the study configuration!\n")

  # Algorithm
  if "Algorithm" not in study_config:
    raise ValueError("\n\n Cannot find Algorithm in the study configuration!\n")
  else:
    if not (study_config["Algorithm"] in AssimAlgos or study_config["Algorithm"] in CheckAlgos):
      raise ValueError("\n\n Algorithm provided is unknow : " + str(study_config["Algorithm"]) +
                         "\n You can choose between : " + str(AssimAlgos)+" "+str(CheckAlgos) + "\n")

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
      raise ValueError("\n\n Study repertory should be an absolute path\n"+
                           " Repertory provided is %s\n" % repertory)

  # ExecuteInContainer
  if "ExecuteInContainer" not in study_config:
    study_config["ExecuteInContainer"] = "No"

  # Check if all the data is provided
  for key in AlgoDataRequirements[study_config["Algorithm"]]:
    if key not in study_config.keys():
      raise ValueError("\n\nCannot find " +  key + " in your study configuration !" +
                    "\n This key is mandatory into a study with " + study_config["Algorithm"] + " algorithm." +
                    "\n " + study_config["Algorithm"] + " requirements are " + str(AlgoDataRequirements[study_config["Algorithm"]]) + "\n")

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
      raise ValueError("\n\n UserPostAnalysis found but From is not defined \n in the analysis configuration!\n")
    else:
      if analysis_config["From"] not in AnalysisFromList:
        raise ValueError("\n\n Analysis From defined in the study configuration does not have a correct type : " + str(analysis_config["From"])
                         + "\n You can have: " + str(AnalysisFromList) + "\n")
    if "Data" not in analysis_config:
      raise ValueError("\n\nAnalysis found but Data is not defined in the analysis configuration!\n")

    if analysis_config["From"] == "Script":
      # Recherche d'un nom valide :
      checked_file_name = analysis_config["Data"]
      if not os.path.exists(checked_file_name):
        if check_repertory:
          if os.path.exists( os.path.join(repertory, analysis_config["Data"]) ):
            checked_file_name = os.path.join(repertory, analysis_config["Data"])
          if os.path.exists( os.path.join(repertory, os.path.basename(analysis_config["Data"])) ):
            checked_file_name = os.path.join(repertory, os.path.basename(analysis_config["Data"]))
        else:
          __i = 0
          while not os.path.exists(checked_file_name) and __i < len(sys.path):
            # Correction avec le sys.path si nécessaire
            checked_file_name = os.path.join(sys.path[__i], analysis_config["Data"])
            __i += 1
          __i = 0
          while not os.path.exists(checked_file_name) and __i < len(sys.path):
            # Correction avec le sys.path si nécessaire
            checked_file_name = os.path.join(sys.path[__i], os.path.basename(analysis_config["Data"]))
            __i += 1
      if not os.path.exists(checked_file_name):
        raise ValueError("\n\n The script file cannot be found for UserPostAnalysis,\n please check its availability.\n"+
                             " The given user file is:\n %s\n" % checked_file_name)

  # Check observers
  if "Observers" in study_config.keys():
    for obs_var in study_config["Observers"]:
      # Check du type
      if not isinstance(study_config["Observers"][obs_var], type({})):
        raise ValueError("\n\n An observer description has to be a Python dictionary\n"+
                             " Observer is %s\n" % obs_var)
      if "nodetype" not in study_config["Observers"][obs_var].keys():
        raise ValueError("\n\n An observer description must provide a nodetype\n"+
                             " Observer is %s\n" % obs_var)
      nodetype = study_config["Observers"][obs_var]["nodetype"]
      if not isinstance(study_config["Observers"][obs_var]["nodetype"], type("")):
        raise ValueError("\n\n An observer nodetype description must be a string\n"+
                             " Observer is %s\n" % obs_var)
      if nodetype != "String" and nodetype != "Script":
        raise ValueError("\n\n An observer nodetype must be equal to 'String' or 'Script'\n"+
                             " Observer is %s\n" % obs_var)
      if nodetype == "String":
        if "String" not in study_config["Observers"][obs_var].keys():
          raise ValueError("\n\n An observer with nodetype String must provide a String\n"+
                               " Observer is %s\n" % obs_var)
        if not isinstance(study_config["Observers"][obs_var]["String"], type("")):
          raise ValueError("\n\n An observer String description must be a string\n"+
                               " Observer is %s\n" % obs_var)
      if nodetype == "Script":
        if "Script" not in study_config["Observers"][obs_var].keys():
          raise ValueError("\n\n An observer with nodetype Script provide a Script\n"+
                               " Observer is %s\n" % obs_var)
        if not isinstance(study_config["Observers"][obs_var]["Script"], type("")):
          raise ValueError("\n\n An observer Script description must be a string\n"+
                               " Observer is %s\n" % obs_var)
      if "scheduler" in study_config["Observers"][obs_var].keys():
        if not isinstance(study_config["Observers"][obs_var]["scheduler"], type("")):
          raise ValueError("\n\n An observer scheduler description must be a string\n"+
                              " Observer is %s\n" % obs_var)

def check_variables(name, study_config):

  if name not in study_config.keys():
    raise ValueError("\n\n %s not found in your study configuration!\n" % name)

  variable_config = study_config[name]
  if "Order" not in variable_config.keys():
    raise ValueError("\n\n Order not found in the %s configuration!\n" % name)

  list_of_variables = variable_config["Order"]
  if not isinstance(list_of_variables, type([])):
    raise ValueError("\n\n Order sould be a list in the %s configuration!\n" % name)
  if len(list_of_variables) < 1:
    raise ValueError("\n\nOrder should contain one or more names in the %s configuration!\n" % name)

  for var in list_of_variables:
    if var not in variable_config.keys():
      raise ValueError("\n\n Variable %s not found in the %s configuration!\n" % name)
    value = variable_config[var]
    try:
      value = int(value)
    except:
      raise ValueError("\n\n Variable %s value cannot be converted in an integer \n in the %s configuration!\n" % name)

def check_data(data_name, data_config, check_repertory=False, repertory=""):

  logging.debug("[check_data] " + data_name)
  data_name_data = "Data"
  data_name_type = "Type"
  data_name_from = "From"

  if data_name_data not in data_config:
    raise ValueError("\n\n" + data_name +" found but " + data_name_data +" is not defined in the study configuration !\n")

  if data_name_type not in data_config:
    raise ValueError("\n\n" + data_name +" found but " + data_name_type  +" is not defined in the study configuration !\n")
  else:
    if data_config[data_name_type] not in AssimType[data_name]:
      raise ValueError("\n\n" + data_name_type + " of " + data_name + " defined in the study configuration does not have a correct type : " + str(data_config[data_name_type])
                    + "\n You can have : " + str(AssimType[data_name]) + "\n")
  if data_name_from not in data_config:
    raise ValueError("\n\n" + data_name + " found but " + data_name_from + " is not defined in the study configuration !\n")
  else:
    if data_config[data_name_from] not in FromNumpyList[data_config[data_name_type]]:
      raise ValueError("\n\n" + data_name_from + " of " + data_name + " defined in the study configuration does not have a correct value : " + str(data_config[data_name_from])
                    + "\n You can have : " + str(FromNumpyList[data_config[data_name_type]]) + "\n")

  # Check des fichiers
  from_type = data_config["From"]
  if from_type == "Script":
    # Recherche d'un nom valide :
    checked_file_name = data_config["Data"]
    if not os.path.exists(checked_file_name):
      if check_repertory:
        if os.path.exists( os.path.join(repertory, data_config["Data"]) ):
          checked_file_name = os.path.join(repertory, data_config["Data"])
        if os.path.exists( os.path.join(repertory, os.path.basename(data_config["Data"])) ):
          checked_file_name = os.path.join(repertory, os.path.basename(data_config["Data"]))
      else:
        # Correction avec le sys.path si nécessaire
        __i = 0
        while not os.path.exists(checked_file_name) and __i < len(sys.path):
          checked_file_name = os.path.join(sys.path[__i], data_config["Data"])
          __i += 1
        __i = 0
        while not os.path.exists(checked_file_name) and __i < len(sys.path):
          checked_file_name = os.path.join(sys.path[__i], os.path.basename(data_config["Data"]))
          __i += 1
    if not os.path.exists(checked_file_name):
      raise ValueError("\n\n The script file cannot be found for the \"%s\" keyword,\n please check its availability.\n The given user file is:\n %s\n"%(from_type,data_config["Data"]))
    #
  elif (from_type == "FunctionDict" or from_type == "ScriptWithSwitch" or from_type == "ScriptWithFunctions" or from_type == "ScriptWithOneFunction"):
    TheData = data_config["Data"]
    for FunctionName in TheData["Function"]:
      # Recherche d'un nom valide :
      checked_file_name = TheData["Script"][FunctionName]
      if not os.path.exists(checked_file_name):
        if check_repertory:
          if os.path.exists( os.path.join(repertory, TheData["Script"][FunctionName]) ):
            checked_file_name = os.path.join(repertory, TheData["Script"][FunctionName])
          if os.path.exists( os.path.join(repertory, os.path.basename(TheData["Script"][FunctionName])) ):
            checked_file_name = os.path.join(repertory, os.path.basename(TheData["Script"][FunctionName]))
        else:
          # Correction avec le sys.path si nécessaire
          __i = 0
          while not os.path.exists(checked_file_name) and __i < len(sys.path):
            checked_file_name = os.path.join(sys.path[__i], TheData["Script"][FunctionName])
            __i += 1
          __i = 0
          while not os.path.exists(checked_file_name) and __i < len(sys.path):
            checked_file_name = os.path.join(sys.path[__i], os.path.basename(TheData["Script"][FunctionName]))
            __i += 1
      if not os.path.exists(checked_file_name):
        raise ValueError("\n\n The script file cannot be found for the \"%s\" keyword, please \n check its availability. The given user file is:\n %s\n"%(from_type,checked_file_name))
