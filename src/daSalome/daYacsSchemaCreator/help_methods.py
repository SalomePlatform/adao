#-*- coding: utf-8 -*-
#  Copyright (C) 2010 EDF R&D
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

import sys
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
    if study_config["Algorithm"] not in AssimAlgos:
      logging.fatal("Algorithm provided is unknow : " + str(study_config["Algorithm"]) +
                    "\n You can choose between : " + str(AssimAlgos))
      sys.exit(1)

  # Debug
  if "Debug" not in study_config:
    study_config["Debug"] = "0"

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
      check_data(key, study_config[key])

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


def check_data(data_name, data_config):

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
      logging.fatal(data_name_type + " defined in the study configuration does not have a correct type : " + str(data_config[data_name_type]) 
                    + "\n You can have : " + str(AssimType[data_name]))
      sys.exit(1)
  if data_name_from not in data_config:
    logging.fatal(data_name + " found but " + data_name_from + " is not defined in the study configuration !")
    sys.exit(1)
  else:
    if data_config[data_name_from] not in FromNumpyList[data_config[data_name_type]]:
      logging.fatal(data_name_from + " defined in the study configuration does not have a correct value : " + str(data_config[data_name_from]) 
                    + "\n You can have : " + str(FromNumpyList[data_config[data_name_type]]))
      sys.exit(1)

