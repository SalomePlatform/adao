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
    catalogAd = runtime.loadCatalog("proc", os.environ["ADAO_ROOT_DIR"] + "/share/salome/resources/adao/ADAOSchemaCatalog.xml")
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

  # Step 0.5: Find if there is a user init node
  init_config = {}
  init_config["Target"] = []
  if "Init" in study_config.keys():
    init_config = study_config["Init"]
    factory_init_node = catalogAd._nodeMap["InitUserDataFromScript"]
    init_node = factory_init_node.cloneNode("InitUserData")
    init_node.getInputPort("script").edInitPy(init_config["Data"])
    proc.edAddChild(init_node)

  # Step 1: get input data from user configuration

  for key in study_config.keys():
    if key in AssimData:
      data_config = study_config[key]

      key_type = key + "Type"

      if data_config["Type"] == "Dict" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd._nodeMap["CreateDictFromScript"]
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.edAddOutputPort(key, t_pyobj)
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        proc.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Vector" and data_config["From"] == "String":
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
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Vector" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd._nodeMap["CreateNumpyVectorFromScript"]
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.edAddOutputPort(key, t_pyobj)
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        proc.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        proc.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Matrix" and data_config["From"] == "String":
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
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Matrix" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd._nodeMap["CreateNumpyMatrixFromScript"]
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.edAddOutputPort(key, t_pyobj)
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        proc.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        proc.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Function" and data_config["From"] == "Dict" and key == "ObservationOperator":
         FunctionDict = data_config["Data"]
         for FunctionName in FunctionDict["Function"]:
           port_name = "ObservationOperator" + FunctionName
           CAS_node.edAddInputPort(port_name, t_string)
           CAS_node.getInputPort(port_name).edInitPy(FunctionDict["Script"][FunctionName])

  # Step 3: create compute bloc
  compute_bloc = runtime.createBloc("compute_bloc")
  proc.edAddChild(compute_bloc)
  proc.edAddCFLink(CAS_node, compute_bloc)

  if AlgoType[study_config["Algorithm"]] == "Direct":
    # We don't need to use an optimizer loop
    factory_execute_node = catalogAd._nodeMap["SimpleExecuteDirectAlgorithm"]
    execute_node = factory_execute_node.cloneNode("Execute" + study_config["Algorithm"])
    compute_bloc.edAddChild(execute_node)
    proc.edAddDFLink(CAS_node.getOutputPort("Study"), execute_node.getInputPort("Study"))

  if AlgoType[study_config["Algorithm"]] == "Optim":
    # We use an optimizer loop
    name = "Execute" + study_config["Algorithm"]
    algLib = "daYacsIntegration.py"
    factoryName = "AssimilationAlgorithm_asynch"
    optimizer_node = runtime.createOptimizerLoop(name, algLib, factoryName, "")
    compute_bloc.edAddChild(optimizer_node)
    proc.edAddDFLink(CAS_node.getOutputPort("Study"), optimizer_node.edGetAlgoInitPort())

    # Check if we have a python script for OptimizerLoopNode
    data_config = study_config["ObservationOperator"]
    if data_config["Type"] == "Function" and data_config["From"] == "Dict":
      # Get script
      FunctionDict = data_config["Data"]
      script_filename = ""
      for FunctionName in FunctionDict["Function"]:
        # We currently support only one file
        script_filename = FunctionDict["Script"][FunctionName]
        break

      # We create a new pyscript node
      opt_script_node = runtime.createScriptNode("", "FunctionNode")
      if not os.path.exists(script_filename):
        logging.fatal("Function script source file does not exists ! :" + script_filename)
        sys.exit(1)
      try:
        script_str= open(script_filename, 'r')
      except:
        logging.fatal("Exception in opening function script file : " + script_filename)
        traceback.print_exc()
        sys.exit(1)
      opt_script_node.setScript(script_str.read())
      opt_script_node.edAddInputPort("computation", t_pyobj)
      opt_script_node.edAddOutputPort("result", t_pyobj)

      # Add it
      computation_bloc = runtime.createBloc("computation_bloc")
      optimizer_node.edSetNode(computation_bloc)
      computation_bloc.edAddChild(opt_script_node)

      # We connect Optimizer with the script
      proc.edAddDFLink(optimizer_node.edGetSamplePort(), opt_script_node.getInputPort("computation"))
      proc.edAddDFLink(opt_script_node.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

      # Connect node with InitUserData
      if "ObservationOperator" in init_config["Target"]:
        opt_script_node.edAddInputPort("init_data", t_pyobj)
        proc.edAddDFLink(init_node.getOutputPort("init_data"), opt_script_node.getInputPort("init_data"))

    else:
      factory_opt_script_node = catalogAd._nodeMap["FakeOptimizerLoopNode"]
      opt_script_node = factory_opt_script_node.cloneNode("FakeFunctionNode")

      # Add it
      computation_bloc = runtime.createBloc("computation_bloc")
      optimizer_node.edSetNode(computation_bloc)
      computation_bloc.edAddChild(opt_script_node)

      # We connect Optimizer with the script
      proc.edAddDFLink(optimizer_node.edGetSamplePort(), opt_script_node.getInputPort("computation"))
      proc.edAddDFLink(opt_script_node.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

  # Step 4: create post-processing from user configuration
  if "Analysis" in study_config.keys():
    analysis_config = study_config["Analysis"]
    if analysis_config["From"] == "String":
      factory_analysis_node = catalogAd._nodeMap["SimpleUserAnalysis"]
      analysis_node = factory_analysis_node.cloneNode("User Analysis")
      default_script = analysis_node.getScript()
      final_script = default_script + analysis_config["Data"]
      analysis_node.setScript(final_script)
      proc.edAddChild(analysis_node)
      proc.edAddCFLink(compute_bloc, analysis_node)
      if AlgoType[study_config["Algorithm"]] == "Optim":
        proc.edAddDFLink(optimizer_node.edGetAlgoResultPort(), analysis_node.getInputPort("Study"))
      else:
        proc.edAddDFLink(execute_node.getOutputPort("Study"), analysis_node.getInputPort("Study"))

      # Connect node with InitUserData
      if "Analysis" in init_config["Target"]:
        analysis_node.edAddInputPort("init_data", t_pyobj)
        proc.edAddDFLink(init_node.getOutputPort("init_data"), analysis_node.getInputPort("init_data"))

    elif analysis_config["From"] == "File":
      factory_analysis_node = catalogAd._nodeMap["SimpleUserAnalysis"]
      analysis_node = factory_analysis_node.cloneNode("User Analysis")
      default_script = analysis_node.getScript()
      if not os.path.exists(analysis_config["Data"]):
        logging.fatal("Analysis source file does not exists ! :" + str(analysis_config["Data"]))
        sys.exit(1)
      try:
        analysis_file = open(analysis_config["Data"], 'r')
      except:
        logging.fatal("Exception in opening analysis file : " + str(analysis_config["Data"]))
        traceback.print_exc()
        sys.exit(1)
      file_text = analysis_file.read()
      final_script = default_script + file_text
      analysis_node.setScript(final_script)
      proc.edAddChild(analysis_node)
      proc.edAddCFLink(compute_bloc, analysis_node)
      if AlgoType[study_config["Algorithm"]] == "Optim":
        proc.edAddDFLink(optimizer_node.edGetAlgoResultPort(), analysis_node.getInputPort("Study"))
      else:
        proc.edAddDFLink(execute_node.getOutputPort("Study"), analysis_node.getInputPort("Study"))
      # Connect node with InitUserData
      if "Analysis" in init_config["Target"]:
        analysis_node.edAddInputPort("init_data", t_pyobj)
        proc.edAddDFLink(init_node.getOutputPort("init_data"), analysis_node.getInputPort("init_data"))

      pass

  return proc

def write_yacs_proc(proc, yacs_schema_filename):

  proc.saveSchema(yacs_schema_filename)

