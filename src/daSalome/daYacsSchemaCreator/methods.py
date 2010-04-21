#-*-coding:iso-8859-1-*-
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
import pilot
import loader
import SALOMERuntime
import os

from daYacsSchemaCreator.infos_daComposant import *

def create_yacs_proc(study_config):

  logging.debug("[create_yacs_proc]")

  # Init part
  SALOMERuntime.RuntimeSALOME_setRuntime()
  l = loader.YACSLoader()
  l.registerProcCataLoader()
  runtime = pilot.getRuntime()
  try:
    catalogAd = runtime.loadCatalog("proc", os.environ["DATASSIM_ROOT_DIR"] + "share/salome/resources/datassim/DATASSIMSchemaCatalog.xml")
  except:
    logging.fatal("Exception in loading DataAssim YACS catalog")
    traceback.print_exc()
    sys.exit(1)

  # Starting creating proc
  proc = runtime.createProc("proc")
  proc.setTypeCode("pyobj", runtime.getTypeCode("pyobj"))
  t_pyobj  = proc.getTypeCode("pyobj")
  t_string = proc.getTypeCode("string")

  # Step 0: create AssimilationStudyObject
  factory_CAS_node = catalogAd._nodeMap["CreateAssimilationStudy"]
  CAS_node = factory_CAS_node.cloneNode("CreateAssimilationStudy")
  CAS_node.getInputPort("Name").edInitPy(study_config["Name"])
  CAS_node.getInputPort("Algorithm").edInitPy(study_config["Algorithm"])
  proc.edAddChild(CAS_node)

  # Step 1: get input data from user configuration

  for key in study_config.keys():
    if key in AssimData:
      data_config = study_config[key]

      key_type = key + "Type"

      if data_config["Type"] == "Vector" and data_config["From"] == "string":
        # Create node
        factory_back_node = catalogAd._nodeMap["CreateNumpyVectorFromString"]
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("vector_in_string").edInitPy(data_config["Data"])
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        proc.edAddDFLink(back_node.getOutputPort("vector"), CAS_node.getInputPort(key))
        proc.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))

      if data_config["Type"] == "Matrix" and data_config["From"] == "string":
        # Create node
        factory_back_node = catalogAd._nodeMap["CreateNumpyMatrixFromString"]
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("matrix_in_string").edInitPy(data_config["Data"])
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        proc.edAddDFLink(back_node.getOutputPort("matrix"), CAS_node.getInputPort(key))
        proc.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))


  # Step 3: create optimizer loop

  # Step 4: create post-processing from user configuration

  return proc

def write_yacs_proc(proc, yacs_schema_filename):

  proc.saveSchema(yacs_schema_filename)

