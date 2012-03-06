#-*- coding: utf-8 -*-
# Copyright (C) 2010-2011 EDF R&D
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
    runtime.addCatalog(catalogAd)
  except:
    logging.fatal("Exception in loading DataAssim YACS catalog")
    traceback.print_exc()
    sys.exit(1)

  # Starting creating proc
  proc = runtime.createProc("proc")
  proc.setTypeCode("pyobj", runtime.getTypeCode("pyobj"))
  proc.setTypeCode("SALOME_TYPES/ParametricInput", catalogAd._typeMap["SALOME_TYPES/ParametricInput"])
  proc.setTypeCode("SALOME_TYPES/ParametricOutput", catalogAd._typeMap["SALOME_TYPES/ParametricOutput"])
  t_pyobj  = proc.getTypeCode("pyobj")
  t_string = proc.getTypeCode("string")
  t_param_input  = proc.getTypeCode("SALOME_TYPES/ParametricInput")
  t_param_output = proc.getTypeCode("SALOME_TYPES/ParametricOutput")
  repertory = False
  base_repertory = ""
  if "Repertory" in study_config.keys():
    base_repertory = study_config["Repertory"]
    repertory = True

  # Step 0: create AssimilationStudyObject
  factory_CAS_node = catalogAd.getNodeFromNodeMap("CreateAssimilationStudy")
  CAS_node = factory_CAS_node.cloneNode("CreateAssimilationStudy")
  CAS_node.getInputPort("Name").edInitPy(study_config["Name"])
  CAS_node.getInputPort("Algorithm").edInitPy(study_config["Algorithm"])
  if study_config["Debug"] == "0":
    CAS_node.getInputPort("Debug").edInitPy(False)
  else:
    CAS_node.getInputPort("Debug").edInitPy(True)

  # Ajout des Variables
  InputVariablesNames = []
  InputVariablesSizes = []
  for var in study_config["InputVariables"]["Order"]:
    InputVariablesNames.append(var)
    InputVariablesSizes.append(int(study_config["InputVariables"][var]))
  CAS_node.getInputPort("InputVariablesNames").edInitPy(InputVariablesNames)
  CAS_node.getInputPort("InputVariablesSizes").edInitPy(InputVariablesSizes)
  OutputVariablesNames = []
  OutputVariablesSizes = []
  for var in study_config["OutputVariables"]["Order"]:
    OutputVariablesNames.append(var)
    OutputVariablesSizes.append(int(study_config["OutputVariables"][var]))
  CAS_node.getInputPort("OutputVariablesNames").edInitPy(OutputVariablesNames)
  CAS_node.getInputPort("OutputVariablesSizes").edInitPy(OutputVariablesSizes)

  proc.edAddChild(CAS_node)

  # Step 0.5: Find if there is a user init node
  init_config = {}
  init_config["Target"] = []
  if "UserDataInit" in study_config.keys():
    init_config = study_config["UserDataInit"]
    factory_init_node = catalogAd.getNodeFromNodeMap("UserDataInitFromScript")
    init_node = factory_init_node.cloneNode("UserDataInit")
    if repertory:
      init_node.getInputPort("script").edInitPy(os.path.join(base_repertory, os.path.basename(init_config["Data"])))
    else:
      init_node.getInputPort("script").edInitPy(init_config["Data"])
    init_node_script = init_node.getScript()
    init_node_script += "init_data = user_script_module.init_data\n"
    init_node.setScript(init_node_script)
    proc.edAddChild(init_node)

  # Step 1: get input data from user configuration

  for key in study_config.keys():
    if key in AssimData:
      data_config = study_config[key]

      key_type = key + "Type"

      if data_config["Type"] == "Dict" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateDictFromScript")
        back_node = factory_back_node.cloneNode("Get" + key)
        if repertory:
          back_node.getInputPort("script").edInitPy(os.path.join(base_repertory, os.path.basename(data_config["Data"])))
        else:
          back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.edAddOutputPort(key, t_pyobj)
        back_node_script = back_node.getScript()
        back_node_script += key + " = user_script_module." + key + "\n"
        back_node.setScript(back_node_script)
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        proc.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node_script = back_node.getScript()
          back_node_script = "__builtins__[\"init_data\"] = init_data\n" + back_node_script
          back_node.setScript(back_node_script)
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Vector" and data_config["From"] == "String":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorFromString")
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
          back_node_script = back_node.getScript()
          back_node_script = "__builtins__[\"init_data\"] = init_data\n" + back_node_script
          back_node.setScript(back_node_script)
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Vector" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorFromScript")
        back_node = factory_back_node.cloneNode("Get" + key)
        if repertory:
          back_node.getInputPort("script").edInitPy(os.path.join(base_repertory, os.path.basename(data_config["Data"])))
        else:
          back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.edAddOutputPort(key, t_pyobj)
        back_node_script = back_node.getScript()
        back_node_script += key + " = user_script_module." + key + "\n"
        back_node.setScript(back_node_script)
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        proc.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        proc.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node_script = back_node.getScript()
          back_node_script = "__builtins__[\"init_data\"] = init_data\n" + back_node_script
          back_node.setScript(back_node_script)
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Matrix" and data_config["From"] == "String":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyMatrixFromString")
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
          back_node_script = back_node.getScript()
          back_node_script = "__builtins__[\"init_data\"] = init_data\n" + back_node_script
          back_node.setScript(back_node_script)
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Matrix" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyMatrixFromScript")
        back_node = factory_back_node.cloneNode("Get" + key)
        if repertory:
          back_node.getInputPort("script").edInitPy(os.path.join(base_repertory, os.path.basename(data_config["Data"])))
        else:
          back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.edAddOutputPort(key, t_pyobj)
        back_node_script = back_node.getScript()
        back_node_script += key + " = user_script_module." + key + "\n"
        back_node.setScript(back_node_script)
        proc.edAddChild(back_node)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        proc.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        proc.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        # Connect node with InitUserData
        if key in init_config["Target"]:
          back_node_script = back_node.getScript()
          back_node_script = "__builtins__[\"init_data\"] = init_data\n" + back_node_script
          back_node.setScript(back_node_script)
          back_node.edAddInputPort("init_data", t_pyobj)
          proc.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))

      if data_config["Type"] == "Function" and data_config["From"] == "FunctionDict" and key == "ObservationOperator":
         FunctionDict = data_config["Data"]
         for FunctionName in FunctionDict["Function"]:
           port_name = "ObservationOperator" + FunctionName
           CAS_node.edAddInputPort(port_name, t_string)
           if repertory:
             CAS_node.getInputPort(port_name).edInitPy(os.path.join(base_repertory, os.path.basename(FunctionDict["Script"][FunctionName])))
           else:
             CAS_node.getInputPort(port_name).edInitPy(FunctionDict["Script"][FunctionName])

  # Step 3: create compute bloc
  compute_bloc = runtime.createBloc("compute_bloc")
  proc.edAddChild(compute_bloc)
  proc.edAddCFLink(CAS_node, compute_bloc)
  # We use an optimizer loop
  name = "Execute" + study_config["Algorithm"]
  algLib = "daYacsIntegration.py"
  factoryName = "AssimilationAlgorithm_asynch"
  optimizer_node = runtime.createOptimizerLoop(name, algLib, factoryName, "")
  compute_bloc.edAddChild(optimizer_node)
  proc.edAddDFLink(CAS_node.getOutputPort("Study"), optimizer_node.edGetAlgoInitPort())
  # Check if we have a python script for OptimizerLoopNode
  data_config = study_config["ObservationOperator"]
  opt_script_node = None
  if data_config["Type"] == "Function" and data_config["From"] == "FunctionDict":
    # Get script
    FunctionDict = data_config["Data"]
    script_filename = ""
    for FunctionName in FunctionDict["Function"]:
      # We currently support only one file
      script_filename = FunctionDict["Script"][FunctionName]
      break

    # We create a new pyscript node
    opt_script_node = runtime.createScriptNode("", "FunctionNode")
    if repertory:
      script_filename = os.path.join(base_repertory, os.path.basename(script_filename))
    try:
      script_str= open(script_filename, 'r')
    except:
      logging.fatal("Exception in opening function script file : " + script_filename)
      traceback.print_exc()
      sys.exit(1)
    node_script  = "#-*-coding:iso-8859-1-*-\n"
    node_script += "import sys, os \n"
    if base_repertory != "":
      node_script += "filepath = \"" + base_repertory + "\"\n"
    else:
      node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
    node_script += "sys.path.insert(0,os.path.dirname(filepath))\n"
    node_script += script_str.read()
    opt_script_node.setScript(node_script)
    opt_script_node.edAddInputPort("computation", t_param_input)
    opt_script_node.edAddOutputPort("result", t_param_output)
  else:
    factory_opt_script_node = catalogAd.getNodeFromNodeMap("FakeOptimizerLoopNode")
    opt_script_node = factory_opt_script_node.cloneNode("FakeFunctionNode")

  # Add computation bloc
  if "Observers" in study_config.keys():
    execution_bloc = runtime.createBloc("Execution Bloc")
    optimizer_node.edSetNode(execution_bloc)

    # Add a node that permits to configure the switch
    factory_read_for_switch_node = catalogAd.getNodeFromNodeMap("ReadForSwitchNode")
    read_for_switch_node = factory_read_for_switch_node.cloneNode("ReadForSwitch")
    execution_bloc.edAddChild(read_for_switch_node)
    proc.edAddDFLink(optimizer_node.edGetSamplePort(), read_for_switch_node.getInputPort("data"))

    # Add a switch
    switch_node = runtime.createSwitch("Execution Switch")
    execution_bloc.edAddChild(switch_node)
    # Connect switch
    proc.edAddDFLink(read_for_switch_node.getOutputPort("switch_value"), switch_node.edGetConditionPort())

    # First case: always computation bloc
    computation_bloc = runtime.createBloc("computation_bloc")
    computation_bloc.edAddChild(opt_script_node)
    switch_node.edSetNode(1, computation_bloc)

    # We connect Optimizer with the script
    proc.edAddDFLink(read_for_switch_node.getOutputPort("data"), opt_script_node.getInputPort("computation"))
    proc.edAddDFLink(opt_script_node.getOutputPort("result"), optimizer_node.edGetPortForOutPool())


    # For each observer add a new bloc in the switch
    observer_config = study_config["Observers"]
    for observer_name in observer_config:
      observer_cfg = observer_config[observer_name]
      observer_bloc = runtime.createBloc("Observer %s" % observer_name)
      switch_node.edSetNode(observer_cfg["number"], observer_bloc)

      factory_extract_data_node = catalogAd.getNodeFromNodeMap("ExtractDataNode")
      extract_data_node = factory_extract_data_node.cloneNode("ExtractData")
      observer_bloc.edAddChild(extract_data_node)
      proc.edAddDFLink(read_for_switch_node.getOutputPort("data"), extract_data_node.getInputPort("data"))

      observation_node = None
      if observer_cfg["nodetype"] == "pyscript":
        factory_observation_node = catalogAd.getNodeFromNodeMap("ObservationNodeString")
        observation_node = factory_observation_node.cloneNode("Observation")
        node_script = observation_node.getScript()
        node_script += observer_cfg["pyscript"]
        observation_node.setScript(node_script)
      else:
        factory_observation_node = catalogAd.getNodeFromNodeMap("ObservationNodeFile")
        observation_node = factory_observation_node.cloneNode("Observation")
        if repertory:
          observation_node.getInputPort("script").edInitPy(os.path.join(base_repertory, os.path.basename(observer_cfg["userfile"])))
        else:
          observation_node.getInputPort("script").edInitPy(observer_cfg["userfile"])
      observer_bloc.edAddChild(observation_node)
      proc.edAddDFLink(extract_data_node.getOutputPort("var"), observation_node.getInputPort("var"))
      proc.edAddDFLink(extract_data_node.getOutputPort("info"), observation_node.getInputPort("info"))

      factory_end_observation_node = catalogAd.getNodeFromNodeMap("EndObservationNode")
      end_observation_node = factory_end_observation_node.cloneNode("EndObservation")
      observer_bloc.edAddChild(end_observation_node)
      proc.edAddCFLink(observation_node, end_observation_node)
      proc.edAddDFLink(end_observation_node.getOutputPort("output"), optimizer_node.edGetPortForOutPool())
  else:
    computation_bloc = runtime.createBloc("computation_bloc")
    optimizer_node.edSetNode(computation_bloc)
    computation_bloc.edAddChild(opt_script_node)

    # We connect Optimizer with the script
    proc.edAddDFLink(optimizer_node.edGetSamplePort(), opt_script_node.getInputPort("computation"))
    proc.edAddDFLink(opt_script_node.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

  # Connect node with InitUserData
  if "ObservationOperator" in init_config["Target"]:
    opt_node_script = opt_script_node.getScript()
    opt_node_script = "__builtins__[\"init_data\"] = init_data\n" + opt_node_script
    opt_script_node.setScript(opt_node_script)
    opt_script_node.edAddInputPort("init_data", t_pyobj)
    proc.edAddDFLink(init_node.getOutputPort("init_data"), opt_script_node.getInputPort("init_data"))

  # Step 4: create post-processing from user configuration
  if "UserPostAnalysis" in study_config.keys():
    analysis_config = study_config["UserPostAnalysis"]
    if analysis_config["From"] == "String":
      factory_analysis_node = catalogAd.getNodeFromNodeMap("SimpleUserAnalysis")
      analysis_node = factory_analysis_node.cloneNode("UsePostAnalysis")
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
      if "UserPostAnalysis" in init_config["Target"]:
        node_script = analysis_node.getScript()
        node_script = "__builtins__[\"init_data\"] = init_data\n" + node_script
        analysis_node.setScript(opt_node_script)
        analysis_node.edAddInputPort("init_data", t_pyobj)
        proc.edAddDFLink(init_node.getOutputPort("init_data"), analysis_node.getInputPort("init_data"))

    elif analysis_config["From"] == "Script":
      factory_analysis_node = catalogAd.getNodeFromNodeMap("SimpleUserAnalysis")
      analysis_node = factory_analysis_node.cloneNode("UserPostAnalysis")
      default_script = analysis_node.getScript()
      analysis_file_name = analysis_config["Data"]
      if repertory:
        analysis_file_name = os.path.join(base_repertory, os.path.basename(analysis_file_name))
      try:
        analysis_file = open(analysis_file_name, 'r')
      except:
        logging.fatal("Exception in opening analysis file : " + str(analysis_config["Data"]))
        traceback.print_exc()
        sys.exit(1)
      node_script  = "#-*-coding:iso-8859-1-*-\n"
      node_script += "import sys, os \n"
      if base_repertory != "":
        node_script += "filepath = \"" + base_repertory + "\"\n"
      else:
        node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
      node_script += "sys.path.insert(0,os.path.dirname(filepath))\n"
      node_script += default_script
      node_script += analysis_file.read()
      analysis_node.setScript(node_script)
      proc.edAddChild(analysis_node)
      proc.edAddCFLink(compute_bloc, analysis_node)
      if AlgoType[study_config["Algorithm"]] == "Optim":
        proc.edAddDFLink(optimizer_node.edGetAlgoResultPort(), analysis_node.getInputPort("Study"))
      else:
        proc.edAddDFLink(execute_node.getOutputPort("Study"), analysis_node.getInputPort("Study"))
      # Connect node with InitUserData
      if "UserPostAnalysis" in init_config["Target"]:
        node_script = analysis_node.getScript()
        node_script = "__builtins__[\"init_data\"] = init_data\n" + node_script
        analysis_node.setScript(opt_node_script)
        analysis_node.edAddInputPort("init_data", t_pyobj)
        proc.edAddDFLink(init_node.getOutputPort("init_data"), analysis_node.getInputPort("init_data"))

      pass

  return proc

def write_yacs_proc(proc, yacs_schema_filename):

  proc.saveSchema(yacs_schema_filename)

