#-*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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
# Author: Andre Ribes, andre.ribes@edf.fr, EDF R&D

import sys
import traceback
import logging
import pilot
import loader
import SALOMERuntime
import os

from daYacsSchemaCreator.infos_daComposant import *

def _Internal_Add_dir_script_ports(node, sf, ed, br, t_type):
  # On conserve le pointeur de "node" et "t_type"
  __scriptfile = str( sf )
  __exist_dir  = bool( ed )
  __base_dir   = str( br )
  __full_name  = os.path.join(__base_dir, os.path.basename(__scriptfile))
  if os.path.exists(__full_name):
    node.getInputPort("script").edInitPy(__full_name)
  else:
    node.getInputPort("script").edInitPy(__scriptfile)
  if __exist_dir:
    node.edAddInputPort("studydir", t_type)
    node.getInputPort("studydir").edInitPy(__base_dir)

def create_yacs_proc(study_config):

  logging.debug("[create_yacs_proc]")

  # Init part
  SALOMERuntime.RuntimeSALOME_setRuntime()
  l = loader.YACSLoader()
  l.registerProcCataLoader()
  runtime = pilot.getRuntime()
  try:
    catalogAd = runtime.loadCatalog("proc", os.environ["ADAO_ENGINE_ROOT_DIR"] + "/share/resources/adao/ADAOSchemaCatalog.xml")
    runtime.addCatalog(catalogAd)
  except:
    raise ValueError("Exception in loading ADAO YACS Schema catalog")

  # Starting creating proc
  proc = runtime.createProc("proc")
  proc.setTypeCode("pyobj", runtime.getTypeCode("pyobj"))
  proc.setTypeCode("SALOME_TYPES/ParametricInput", catalogAd._typeMap["SALOME_TYPES/ParametricInput"])
  proc.setTypeCode("SALOME_TYPES/ParametricOutput", catalogAd._typeMap["SALOME_TYPES/ParametricOutput"])
  t_pyobj  = proc.getTypeCode("pyobj")
  t_string = proc.getTypeCode("string")
  t_bool = proc.getTypeCode("bool")
  t_param_input  = proc.getTypeCode("SALOME_TYPES/ParametricInput")
  t_param_output = proc.getTypeCode("SALOME_TYPES/ParametricOutput")
  if "Repertory" in list(study_config.keys()):
    base_repertory = study_config["Repertory"]
    repertory      = True
  else:
    base_repertory = ""
    repertory = False
  if "ExecuteInContainer" in list(study_config.keys()):
    if study_config["ExecuteInContainer"] == "Mono":
      ExecuteInContainer = True
      ExecuteInModeMulti = False
    elif study_config["ExecuteInContainer"] == "Multi":
      ExecuteInContainer = True
      ExecuteInModeMulti = True
    else: # cas "No"
      ExecuteInContainer = False
      ExecuteInModeMulti = False
  else:
    ExecuteInContainer = False
    ExecuteInModeMulti = False
  if ExecuteInContainer and bool(UseSeparateContainer):
    mycontainer = proc.createContainer("AdaoContainer")
    if ExecuteInModeMulti:
      # type : multi pour creer un nouveau container pour chaque noeud
      # type : mono pour réutiliser le même container (defaut)
      mycontainer.setProperty("type","multi")

  # Create ADAO case bloc
  ADAO_Case = runtime.createBloc("ADAO_Case_Bloc")
  proc.edAddChild(ADAO_Case)

  # Step 0: create AssimilationStudyObject
  factory_CAS_node = catalogAd.getNodeFromNodeMap("CreateAssimilationStudy")
  CAS_node = factory_CAS_node.cloneNode("CreateAssimilationStudy")
  CAS_node.getInputPort("Name").edInitPy(study_config["Name"])
  CAS_node.getInputPort("Algorithm").edInitPy(study_config["Algorithm"])
  if "Debug" in study_config and study_config["Debug"] == "1":
    CAS_node.getInputPort("Debug").edInitPy(True)
  else:
    CAS_node.getInputPort("Debug").edInitPy(False)

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

  ADAO_Case.edAddChild(CAS_node)
  if ExecuteInContainer and bool(UseSeparateContainer):
    CAS_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
    CAS_node.setContainer(mycontainer)

  # Adding an observer init node if an user defines some
  factory_init_observers_node = catalogAd.getNodeFromNodeMap("SetObserversNode")
  init_observers_node = factory_init_observers_node.cloneNode("SetObservers")
  if "Observers" in list(study_config.keys()):
    node_script = init_observers_node.getScript()
    node_script += "has_observers = True\n"
    node_script += "observers = " + str(study_config["Observers"]) + "\n"
    init_observers_node.setScript(node_script)
    ADAO_Case.edAddChild(init_observers_node)
    ADAO_Case.edAddDFLink(init_observers_node.getOutputPort("has_observers"), CAS_node.getInputPort("has_observers"))
    ADAO_Case.edAddDFLink(init_observers_node.getOutputPort("observers"), CAS_node.getInputPort("observers"))
  else:
    node_script = init_observers_node.getScript()
    node_script += "has_observers = False\n"
    node_script += "observers = \"\"\n"
    init_observers_node.setScript(node_script)
    ADAO_Case.edAddChild(init_observers_node)
    ADAO_Case.edAddDFLink(init_observers_node.getOutputPort("has_observers"), CAS_node.getInputPort("has_observers"))
    ADAO_Case.edAddDFLink(init_observers_node.getOutputPort("observers"), CAS_node.getInputPort("observers"))
  if ExecuteInContainer and bool(UseSeparateContainer):
    init_observers_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
    init_observers_node.setContainer(mycontainer)

  # Step 0.5: Find if there is a user init node
  init_config = {}
  init_config["Target"] = []
  if "UserDataInit" in list(study_config.keys()):
    init_config = study_config["UserDataInit"]
    factory_init_node = catalogAd.getNodeFromNodeMap("UserDataInitFromScript")
    init_node = factory_init_node.cloneNode("UserDataInit")
    _Internal_Add_dir_script_ports( init_node, init_config["Data"], repertory, base_repertory, t_string)
    init_node_script = init_node.getScript()
    init_node_script += "# Import script and get data\n__import__(module_name)\nuser_script_module = sys.modules[module_name]\n\n"
    init_node_script += "init_data = user_script_module.init_data\n"
    init_node.setScript(init_node_script)
    ADAO_Case.edAddChild(init_node)
    if ExecuteInContainer and bool(UseSeparateContainer):
      init_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
      init_node.setContainer(mycontainer)

  # Step 1: get input data from user configuration

  st_keys = sorted(list(study_config.keys()))
  for key in st_keys:
    ad_keys = sorted(AssimData)
    if key in ad_keys:
      data_config = study_config[key]

      key_type = key + "Type"
      key_stored = key + "Stored"

      if data_config["Type"] == "Dict" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateDictFromScript")
        back_node = factory_back_node.cloneNode("Get" + key)
        _Internal_Add_dir_script_ports( back_node, data_config["Data"], repertory, base_repertory, t_string)
        back_node.edAddOutputPort(key, t_pyobj)
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node_script += "# Import script and get data\n__import__(module_name)\nuser_script_module = sys.modules[module_name]\n\n"
        if key == "AlgorithmParameters":
            back_node_script += "if hasattr(user_script_module,'" + key + "'):\n  "
            back_node_script += key + " = user_script_module." + key + "\n"
            skey = "Parameters"
            back_node_script += "elif hasattr(user_script_module,'" + skey + "'):\n  "
            back_node_script += key + " = user_script_module." + skey + "\n"
        else:
            back_node_script += key + " = user_script_module." + key + "\n"
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        ADAO_Case.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))

      if data_config["Type"] == "Dict" and data_config["From"] == "String":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateDictFromString")
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("dict_in_string").edInitPy(data_config["Data"])
        back_node.edAddOutputPort(key, t_pyobj)
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node_script += key + " = dict(dico)\n"
        back_node_script += "logging.debug(\"Dict is %ss\"%s%s)"%("%","%",key)
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        ADAO_Case.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))

      if data_config["Type"] == "Vector" and data_config["From"] == "String":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorFromString")
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("vector_in_string").edInitPy(data_config["Data"])
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort("vector"), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] == "Vector" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorFromScript")
        back_node = factory_back_node.cloneNode("Get" + key)
        _Internal_Add_dir_script_ports( back_node, data_config["Data"], repertory, base_repertory, t_string)
        back_node.edAddOutputPort(key, t_pyobj)
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node_script += "# Import script and get data\n__import__(module_name)\nuser_script_module = sys.modules[module_name]\n\n"
        back_node_script += key + " = user_script_module." + key + "\n"
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] == "Vector" and data_config["From"] == "DataFile":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorFromDataFile")
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.getInputPort("columns").edInitPy((key,)) # On impose le concept, et le schéma YACS est ammendable
        if "ColMajor" in data_config:
            colmajor = bool(data_config["ColMajor"])
        else:
            colmajor = False
        back_node.getInputPort("colmajor").edInitPy(colmajor) # On impose le concept, et le schéma YACS est ammendable
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort("vector"), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] == "VectorSerie" and data_config["From"] == "String":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorSerieFromString")
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("vector_in_string").edInitPy(data_config["Data"])
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n" + back_node_script
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort("vector"), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] == "VectorSerie" and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorSerieFromScript")
        back_node = factory_back_node.cloneNode("Get" + key)
        _Internal_Add_dir_script_ports( back_node, data_config["Data"], repertory, base_repertory, t_string)
        back_node.edAddOutputPort(key, t_pyobj)
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node_script += "# Import script and get data\n__import__(module_name)\nuser_script_module = sys.modules[module_name]\n\n"
        back_node_script += key + " = user_script_module." + key + "\n"
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] == "VectorSerie" and data_config["From"] == "DataFile":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpyVectorSerieFromDataFile")
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("script").edInitPy(data_config["Data"])
        back_node.getInputPort("columns").edInitPy(()) # On impose aucun nom et le schéma YACS est ammendable
        if "ColMajor" in data_config:
            colmajor = bool(data_config["ColMajor"])
        else:
            colmajor = False
        back_node.getInputPort("colmajor").edInitPy(colmajor) # On impose le concept, et le schéma YACS est ammendable
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort("vector"), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] in ("Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix") and data_config["From"] == "String":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpy%sFromString"%(data_config["Type"],))
        back_node = factory_back_node.cloneNode("Get" + key)
        back_node.getInputPort("matrix_in_string").edInitPy(data_config["Data"])
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort("matrix"), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] in ("Matrix", "ScalarSparseMatrix", "DiagonalSparseMatrix") and data_config["From"] == "Script":
        # Create node
        factory_back_node = catalogAd.getNodeFromNodeMap("CreateNumpy%sFromScript"%(data_config["Type"],))
        back_node = factory_back_node.cloneNode("Get" + key)
        _Internal_Add_dir_script_ports( back_node, data_config["Data"], repertory, base_repertory, t_string)
        back_node.edAddOutputPort(key, t_pyobj)
        ADAO_Case.edAddChild(back_node)
        if ExecuteInContainer and bool(UseSeparateContainer):
          back_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
          back_node.setContainer(mycontainer)
        # Set content of the node
        back_node_script = back_node.getScript()
        if "Stored" in data_config:
            back_node_script += "stored = " + str(data_config["Stored"]) + "\n"
        else:
            back_node_script += "stored = 0\n"
        if key in init_config["Target"]:
          # Connect node with InitUserData
          back_node_script += "__builtins__[\"init_data\"] = init_data\n"
          back_node.edAddInputPort("init_data", t_pyobj)
          ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), back_node.getInputPort("init_data"))
        back_node_script += "# Import script and get data\n__import__(module_name)\nuser_script_module = sys.modules[module_name]\n\n"
        back_node_script += key + " = user_script_module." + key + "\n"
        back_node.setScript(back_node_script)
        # Connect node with CreateAssimilationStudy
        CAS_node.edAddInputPort(key, t_pyobj)
        CAS_node.edAddInputPort(key_type, t_string)
        CAS_node.edAddInputPort(key_stored, t_bool)
        ADAO_Case.edAddDFLink(back_node.getOutputPort(key), CAS_node.getInputPort(key))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("type"), CAS_node.getInputPort(key_type))
        ADAO_Case.edAddDFLink(back_node.getOutputPort("stored"), CAS_node.getInputPort(key_stored))

      if data_config["Type"] == "Function" and (key == "ObservationOperator" or key == "EvolutionModel"):
         TheData = data_config["Data"]
         for FunctionName in TheData["Function"]:
           port_name = key + FunctionName
           CAS_node.edAddInputPort(port_name, t_string)
           if os.path.exists(os.path.join(base_repertory, os.path.basename(TheData["Script"][FunctionName]))):
             CAS_node.getInputPort(port_name).edInitPy(os.path.join(base_repertory, os.path.basename(TheData["Script"][FunctionName])))
           else:
             CAS_node.getInputPort(port_name).edInitPy(TheData["Script"][FunctionName])
           try:
             CAS_node.edAddInputPort("studydir", t_string)
             CAS_node.getInputPort("studydir").edInitPy(base_repertory)
           except: pass

  # Step 3: create compute bloc
  compute_bloc = runtime.createBloc("compute_bloc")
  ADAO_Case.edAddChild(compute_bloc)
  ADAO_Case.edAddCFLink(CAS_node, compute_bloc)
  # We use an optimizer loop
  name = "Execute" + study_config["Algorithm"]
  if sys.version_info.major < 3:
    algLib = "daYacsIntegration.py"
  else:
    algLib = "adao.py"
  factoryName = "AssimilationAlgorithm_asynch"
  #~ optimizer_node = runtime.createOptimizerLoop(name, algLib, factoryName, "")
  optimizer_node = runtime.createOptimizerLoop(name, algLib, factoryName, True)
  compute_bloc.edAddChild(optimizer_node)
  ADAO_Case.edAddDFLink(CAS_node.getOutputPort("Study"), optimizer_node.edGetAlgoInitPort())

  # Check if we have a python script for OptimizerLoopNode
  data_config = study_config["ObservationOperator"]
  opt_script_nodeOO = None
  if data_config["Type"] == "Function" and (data_config["From"] == "ScriptWithSwitch" or data_config["From"] == "FunctionDict"):
    # Get script
    TheData = data_config["Data"]
    script_filename = ""
    for FunctionName in TheData["Function"]:
      # We currently support only one file
      script_filename = TheData["Script"][FunctionName]
      break
    # We create a new pyscript node
    opt_script_nodeOO = runtime.createScriptNode("", "FunctionNodeOO")
    if repertory and os.path.exists(os.path.join(base_repertory, os.path.basename(script_filename))):
      script_filename = os.path.join(base_repertory, os.path.basename(script_filename))
    try:
      script_str= open(script_filename, 'r')
    except:
      raise ValueError("Exception in opening function script file: " + script_filename)
    node_script  = "#-*- coding: utf-8 -*-\n"
    node_script += "import sys, os \n"
    node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
    node_script += "filename = \"" + os.path.basename(script_filename) + "\"\n"
    node_script += "if sys.path.count(filepath)==0 or (sys.path.count(filepath)>0 and sys.path.index(filepath)>0):\n"
    node_script += "  sys.path.insert(0,filepath)\n"
    node_script += script_str.read()
    opt_script_nodeOO.setScript(node_script)
    opt_script_nodeOO.edAddInputPort("computation", t_param_input)
    opt_script_nodeOO.edAddOutputPort("result", t_param_output)

  elif data_config["Type"] == "Function" and data_config["From"] == "ScriptWithFunctions":
    # Get script
    ScriptWithFunctions = data_config["Data"]
    script_filename = ""
    for FunctionName in ScriptWithFunctions["Function"]:
      # We currently support only one file
      script_filename = ScriptWithFunctions["Script"][FunctionName]
      break

    # We create a new pyscript node
    opt_script_nodeOO = runtime.createScriptNode("", "FunctionNodeOO")
    if repertory and os.path.exists(os.path.join(base_repertory, os.path.basename(script_filename))):
      script_filename = os.path.join(base_repertory, os.path.basename(script_filename))
    try:
      script_str= open(script_filename, 'r')
    except:
      raise ValueError("Exception in opening function script file: " + script_filename)
    node_script  = "#-*- coding: utf-8 -*-\n"
    node_script += "import sys, os, numpy, logging, pickle, codecs\n"
    node_script += "def loads( data ):\n"
    node_script += "  return pickle.loads(codecs.decode(data.encode(), 'base64'))\n"
    node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
    node_script += "filename = \"" + os.path.basename(script_filename) + "\"\n"
    node_script += "if sys.path.count(filepath)==0 or (sys.path.count(filepath)>0 and sys.path.index(filepath)>0):\n"
    node_script += "  sys.path.insert(0,filepath)\n"
    node_script += """# ==============================================\n"""
    node_script += script_str.read()
    node_script += """# ==============================================\n"""
    node_script += """__method = None\n"""
    node_script += """for param in computation["specificParameters"]:\n"""
    node_script += """  if param["name"] == "method": __method = loads(param["value"])\n"""
    node_script += """if __method not in ["Direct", "Tangent", "Adjoint"]:\n"""
    node_script += """  raise ValueError("ComputationFunctionNode: no valid computation method is given, it has to be Direct, Tangent or Adjoint (\'%s\' given)."%__method)\n"""
    node_script += """logging.debug("ComputationFunctionNode: Found method is \'%s\'"%__method)\n"""
    node_script += """#\n"""
    node_script += """#\n"""
    node_script += """__data = []\n"""
    node_script += """if __method == "Direct":\n"""
    node_script += """  try:\n"""
    node_script += """      DirectOperator\n"""
    node_script += """  except NameError:\n"""
    node_script += """      raise ValueError("ComputationFunctionNode: DirectOperator not found in the imported user script file")\n"""
    node_script += """  logging.debug("ComputationFunctionNode: Direct computation")\n"""
    node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
    node_script += """  __data = DirectOperator(numpy.matrix( __Xcurrent ).T)\n"""
    node_script += """#\n"""
    node_script += """if __method == "Tangent":\n"""
    node_script += """  try:\n"""
    node_script += """    TangentOperator\n"""
    node_script += """  except NameError:\n"""
    node_script += """    raise ValueError("ComputationFunctionNode:  TangentOperator not found in the imported user script file")\n"""
    node_script += """  logging.debug("ComputationFunctionNode: Tangent computation")\n"""
    node_script += """  __Xcurrent  = computation["inputValues"][0][0][0]\n"""
    node_script += """  __dXcurrent = computation["inputValues"][0][0][1]\n"""
    node_script += """  __data = TangentOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __dXcurrent ).T))\n"""
    node_script += """#\n"""
    node_script += """if __method == "Adjoint":\n"""
    node_script += """  try:\n"""
    node_script += """    AdjointOperator\n"""
    node_script += """  except NameError:\n"""
    node_script += """    raise ValueError("ComputationFunctionNode: AdjointOperator not found in the imported user script file")\n"""
    node_script += """  logging.debug("ComputationFunctionNode: Adjoint computation")\n"""
    node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
    node_script += """  __Ycurrent = computation["inputValues"][0][0][1]\n"""
    node_script += """  __data = AdjointOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __Ycurrent ).T))\n"""
    node_script += """#\n"""
    node_script += """logging.debug("ComputationFunctionNode: Formatting the output")\n"""
    node_script += """__it = 1.*numpy.ravel(__data)\n"""
    node_script += """outputValues = [[[[]]]]\n"""
    node_script += """outputValues[0][0][0] = list(__it)\n"""
    node_script += """#\n"""
    node_script += """result = {}\n"""
    node_script += """result["outputValues"]        = outputValues\n"""
    node_script += """result["specificOutputInfos"] = []\n"""
    node_script += """result["returnCode"]          = 0\n"""
    node_script += """result["errorMessage"]        = ""\n"""
    node_script += """# ==============================================\n"""
    #
    opt_script_nodeOO.setScript(node_script)
    opt_script_nodeOO.edAddInputPort("computation", t_param_input)
    opt_script_nodeOO.edAddOutputPort("result", t_param_output)

  elif data_config["Type"] == "Function" and data_config["From"] == "ScriptWithOneFunction":
    # Get script
    ScriptWithOneFunction = data_config["Data"]
    script_filename = ""
    for FunctionName in ScriptWithOneFunction["Function"]:
      # We currently support only one file
      script_filename = ScriptWithOneFunction["Script"][FunctionName]
      break

    # We create a new pyscript node
    opt_script_nodeOO = runtime.createScriptNode("", "FunctionNodeOO")
    if repertory and os.path.exists(os.path.join(base_repertory, os.path.basename(script_filename))):
      script_filename = os.path.join(base_repertory, os.path.basename(script_filename))
    try:
      script_str= open(script_filename, 'r')
    except:
      raise ValueError("Exception in opening function script file: " + script_filename)
    node_script  = "#-*- coding: utf-8 -*-\n"
    node_script += "import sys, os, numpy, logging, pickle, codecs\n"
    node_script += "def loads( data ):\n"
    node_script += "  return pickle.loads(codecs.decode(data.encode(), 'base64'))\n"
    node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
    node_script += "filename = \"" + os.path.basename(script_filename) + "\"\n"
    node_script += "if sys.path.count(filepath)==0 or (sys.path.count(filepath)>0 and sys.path.index(filepath)>0):\n"
    node_script += "  sys.path.insert(0,filepath)\n"
    node_script += """# ==============================================\n"""
    node_script += script_str.read()
    node_script += """# ==============================================\n"""
    node_script += """__method = None\n"""
    node_script += """for param in computation["specificParameters"]:\n"""
    node_script += """  if param["name"] == "method": __method = loads(param["value"])\n"""
    node_script += """if __method not in ["Direct", "Tangent", "Adjoint"]:\n"""
    node_script += """  raise ValueError("ComputationFunctionNode: no valid computation method is given, it has to be Direct, Tangent or Adjoint (\'%s\' given)."%__method)\n"""
    node_script += """logging.debug("ComputationFunctionNode: Found method is \'%s\'"%__method)\n"""
    node_script += """#\n"""
    node_script += """try:\n"""
    node_script += """    DirectOperator\n"""
    node_script += """except NameError:\n"""
    node_script += """    raise ValueError("ComputationFunctionNode: DirectOperator not found in the imported user script file")\n"""
    if sys.version_info.major < 3:
        node_script += """from daCore import NumericObjects\n"""
    else:
        node_script += """from adao.daCore import NumericObjects\n"""
    node_script += """FDA = NumericObjects.FDApproximation(\n"""
    node_script += """    Function   = DirectOperator,\n"""
    node_script += """    increment  = %s,\n"""%str(ScriptWithOneFunction['DifferentialIncrement'])
    node_script += """    centeredDF = %s,\n"""%str(ScriptWithOneFunction['CenteredFiniteDifference'])
    if 'EnableMultiProcessing' in list(ScriptWithOneFunction.keys()):
        node_script += """    mpEnabled  = %s,\n"""%str(ScriptWithOneFunction['EnableMultiProcessing'])
    if 'NumberOfProcesses' in list(ScriptWithOneFunction.keys()):
        node_script += """    mpWorkers  = %s,\n"""%str(ScriptWithOneFunction['NumberOfProcesses'])
    node_script += """    )\n"""
    node_script += """#\n"""
    node_script += """__data = []\n"""
    node_script += """if __method == "Direct":\n"""
    node_script += """  logging.debug("ComputationFunctionNode: Direct computation")\n"""
    node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
    node_script += """  __data = FDA.DirectOperator(numpy.matrix( __Xcurrent ).T)\n"""
    node_script += """#\n"""
    node_script += """if __method == "Tangent":\n"""
    node_script += """  logging.debug("ComputationFunctionNode: Tangent computation")\n"""
    node_script += """  __Xcurrent  = computation["inputValues"][0][0][0]\n"""
    node_script += """  __dXcurrent = computation["inputValues"][0][0][1]\n"""
    node_script += """  __data = FDA.TangentOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __dXcurrent ).T))\n"""
    node_script += """#\n"""
    node_script += """if __method == "Adjoint":\n"""
    node_script += """  logging.debug("ComputationFunctionNode: Adjoint computation")\n"""
    node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
    node_script += """  __Ycurrent = computation["inputValues"][0][0][1]\n"""
    node_script += """  __data = FDA.AdjointOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __Ycurrent ).T))\n"""
    node_script += """#\n"""
    node_script += """logging.debug("ComputationFunctionNode: Formatting the output")\n"""
    node_script += """__it = 1.*numpy.ravel(__data)\n"""
    node_script += """outputValues = [[[[]]]]\n"""
    node_script += """outputValues[0][0][0] = list(__it)\n"""
    node_script += """#\n"""
    node_script += """result = {}\n"""
    node_script += """result["outputValues"]        = outputValues\n"""
    node_script += """result["specificOutputInfos"] = []\n"""
    node_script += """result["returnCode"]          = 0\n"""
    node_script += """result["errorMessage"]        = ""\n"""
    node_script += """# ==============================================\n"""
    #
    opt_script_nodeOO.setScript(node_script)
    opt_script_nodeOO.edAddInputPort("computation", t_param_input)
    opt_script_nodeOO.edAddOutputPort("result", t_param_output)

  else:
    factory_opt_script_node = catalogAd.getNodeFromNodeMap("FakeOptimizerLoopNode")
    opt_script_nodeOO = factory_opt_script_node.cloneNode("FakeFunctionNode")
  #
  if ExecuteInContainer and bool(UseSeparateContainer):
    opt_script_nodeOO.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
    opt_script_nodeOO.setContainer(mycontainer)

  # Check if we have a python script for OptimizerLoopNode
  if "EvolutionModel" in list(study_config.keys()):
    data_config = study_config["EvolutionModel"]
    opt_script_nodeEM = None
    if data_config["Type"] == "Function" and (data_config["From"] == "ScriptWithSwitch" or data_config["From"] == "FunctionDict"):
      # Get script
      TheData = data_config["Data"]
      script_filename = ""
      for FunctionName in TheData["Function"]:
        # We currently support only one file
        script_filename = TheData["Script"][FunctionName]
        break
      # We create a new pyscript node
      opt_script_nodeEM = runtime.createScriptNode("", "FunctionNodeEM")
      if repertory and os.path.exists(os.path.join(base_repertory, os.path.basename(script_filename))):
        script_filename = os.path.join(base_repertory, os.path.basename(script_filename))
      try:
        script_str= open(script_filename, 'r')
      except:
        raise ValueError("Exception in opening function script file: " + script_filename)
      node_script  = "#-*- coding: utf-8 -*-\n"
      node_script += "import sys, os \n"
      node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
      node_script += "filename = \"" + os.path.basename(script_filename) + "\"\n"
      node_script += "if sys.path.count(filepath)==0 or (sys.path.count(filepath)>0 and sys.path.index(filepath)>0):\n"
      node_script += "  sys.path.insert(0,filepath)\n"
      node_script += script_str.read()
      opt_script_nodeEM.setScript(node_script)
      opt_script_nodeEM.edAddInputPort("computation", t_param_input)
      opt_script_nodeEM.edAddOutputPort("result", t_param_output)

    elif data_config["Type"] == "Function" and data_config["From"] == "ScriptWithFunctions":
      # Get script
      ScriptWithFunctions = data_config["Data"]
      script_filename = ""
      for FunctionName in ScriptWithFunctions["Function"]:
        # We currently support only one file
        script_filename = ScriptWithFunctions["Script"][FunctionName]
        break
      # We create a new pyscript node
      opt_script_nodeEM = runtime.createScriptNode("", "FunctionNodeEM")
      if repertory and os.path.exists(os.path.join(base_repertory, os.path.basename(script_filename))):
        script_filename = os.path.join(base_repertory, os.path.basename(script_filename))
      try:
        script_str= open(script_filename, 'r')
      except:
        raise ValueError("Exception in opening function script file: " + script_filename)
      node_script  = "#-*- coding: utf-8 -*-\n"
      node_script += "import sys, os, numpy, logging, pickle, codecs\n"
      node_script += "def loads( data ):\n"
      node_script += "  return pickle.loads(codecs.decode(data.encode(), 'base64'))\n"
      node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
      node_script += "filename = \"" + os.path.basename(script_filename) + "\"\n"
      node_script += "if sys.path.count(filepath)==0 or (sys.path.count(filepath)>0 and sys.path.index(filepath)>0):\n"
      node_script += "  sys.path.insert(0,filepath)\n"
      node_script += script_str.read()
      node_script += """# ==============================================\n"""
      node_script += """__method = None\n"""
      node_script += """for param in computation["specificParameters"]:\n"""
      node_script += """  if param["name"] == "method": __method = loads(param["value"])\n"""
      node_script += """if __method not in ["Direct", "Tangent", "Adjoint"]:\n"""
      node_script += """  raise ValueError("ComputationFunctionNode: no valid computation method is given, it has to be Direct, Tangent or Adjoint (\'%s\' given)."%__method)\n"""
      node_script += """logging.debug("ComputationFunctionNode: Found method is \'%s\'"%__method)\n"""
      node_script += """#\n"""
      node_script += """#\n"""
      node_script += """__data = []\n"""
      node_script += """if __method == "Direct":\n"""
      node_script += """  try:\n"""
      node_script += """    DirectOperator\n"""
      node_script += """  except NameError:\n"""
      node_script += """    raise ValueError("ComputationFunctionNode: mandatory DirectOperator not found in the imported user script file")\n"""
      node_script += """  logging.debug("ComputationFunctionNode: Direct computation")\n"""
      node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
      node_script += """  if len(computation["inputValues"][0][0]) == 2:\n"""
      node_script += """    __Ucurrent = computation["inputValues"][0][0][1]\n"""
      node_script += """    __data = DirectOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __Ucurrent ).T))\n"""
      node_script += """  else:\n"""
      node_script += """    __data = DirectOperator(numpy.matrix( __Xcurrent ).T)\n"""
      node_script += """#\n"""
      node_script += """if __method == "Tangent":\n"""
      node_script += """  try:\n"""
      node_script += """    TangentOperator\n"""
      node_script += """  except NameError:\n"""
      node_script += """    raise ValueError("ComputationFunctionNode: mandatory TangentOperator not found in the imported user script file")\n"""
      node_script += """  logging.debug("ComputationFunctionNode: Tangent computation")\n"""
      node_script += """  __Xcurrent  = computation["inputValues"][0][0][0]\n"""
      node_script += """  __dXcurrent = computation["inputValues"][0][0][1]\n"""
      node_script += """  __data = TangentOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __dXcurrent ).T))\n"""
      node_script += """#\n"""
      node_script += """if __method == "Adjoint":\n"""
      node_script += """  try:\n"""
      node_script += """    AdjointOperator\n"""
      node_script += """  except NameError:\n"""
      node_script += """    raise ValueError("ComputationFunctionNode: mandatory AdjointOperator not found in the imported user script file")\n"""
      node_script += """  logging.debug("ComputationFunctionNode: Adjoint computation")\n"""
      node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
      node_script += """  __Ycurrent = computation["inputValues"][0][0][1]\n"""
      node_script += """  __data = AdjointOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __Ycurrent ).T))\n"""
      node_script += """#\n"""
      node_script += """logging.debug("ComputationFunctionNode: Formatting the output")\n"""
      node_script += """__it = 1.*numpy.ravel(__data)\n"""
      node_script += """outputValues = [[[[]]]]\n"""
      node_script += """outputValues[0][0][0] = list(__it)\n"""
      node_script += """#\n"""
      node_script += """result = {}\n"""
      node_script += """result["outputValues"]        = outputValues\n"""
      node_script += """result["specificOutputInfos"] = []\n"""
      node_script += """result["returnCode"]          = 0\n"""
      node_script += """result["errorMessage"]        = ""\n"""
      node_script += """# ==============================================\n"""
      #
      opt_script_nodeEM.setScript(node_script)
      opt_script_nodeEM.edAddInputPort("computation", t_param_input)
      opt_script_nodeEM.edAddOutputPort("result", t_param_output)

    elif data_config["Type"] == "Function" and data_config["From"] == "ScriptWithOneFunction":
      # Get script
      ScriptWithOneFunction = data_config["Data"]
      script_filename = ""
      for FunctionName in ScriptWithOneFunction["Function"]:
        # We currently support only one file
        script_filename = ScriptWithOneFunction["Script"][FunctionName]
        break
      # We create a new pyscript node
      opt_script_nodeEM = runtime.createScriptNode("", "FunctionNodeEM")
      if repertory and os.path.exists(os.path.join(base_repertory, os.path.basename(script_filename))):
        script_filename = os.path.join(base_repertory, os.path.basename(script_filename))
      try:
        script_str= open(script_filename, 'r')
      except:
        raise ValueError("Exception in opening function script file: " + script_filename)
      node_script  = "#-*- coding: utf-8 -*-\n"
      node_script += "import sys, os, numpy, logging, pickle, codecs\n"
      node_script += "def loads( data ):\n"
      node_script += "  return pickle.loads(codecs.decode(data.encode(), 'base64'))\n"
      node_script += "filepath = \"" + os.path.dirname(script_filename) + "\"\n"
      node_script += "filename = \"" + os.path.basename(script_filename) + "\"\n"
      node_script += "if sys.path.count(filepath)==0 or (sys.path.count(filepath)>0 and sys.path.index(filepath)>0):\n"
      node_script += "  sys.path.insert(0,filepath)\n"
      node_script += script_str.read()
      node_script += """# ==============================================\n"""
      node_script += """__method = None\n"""
      node_script += """for param in computation["specificParameters"]:\n"""
      node_script += """  if param["name"] == "method": __method = loads(param["value"])\n"""
      node_script += """if __method not in ["Direct", "Tangent", "Adjoint"]:\n"""
      node_script += """  raise ValueError("ComputationFunctionNode: no valid computation method is given, it has to be Direct, Tangent or Adjoint (\'%s\' given)."%__method)\n"""
      node_script += """logging.debug("ComputationFunctionNode: Found method is \'%s\'"%__method)\n"""
      node_script += """#\n"""
      node_script += """try:\n"""
      node_script += """    DirectOperator\n"""
      node_script += """except NameError:\n"""
      node_script += """    raise ValueError("ComputationFunctionNode: DirectOperator not found in the imported user script file")\n"""
      if sys.version_info.major < 3:
          node_script += """from daCore import NumericObjects\n"""
      else:
          node_script += """from adao.daCore import NumericObjects\n"""
      node_script += """FDA = NumericObjects.FDApproximation(\n"""
      node_script += """    Function   = DirectOperator,\n"""
      node_script += """    increment  = %s,\n"""%str(ScriptWithOneFunction['DifferentialIncrement'])
      node_script += """    centeredDF = %s,\n"""%str(ScriptWithOneFunction['CenteredFiniteDifference'])
      if 'EnableMultiProcessing' in list(ScriptWithOneFunction.keys()):
          node_script += """    mpEnabled  = %s,\n"""%str(ScriptWithOneFunction['EnableMultiProcessing'])
      if 'NumberOfProcesses' in list(ScriptWithOneFunction.keys()):
          node_script += """    mpWorkers  = %s,\n"""%str(ScriptWithOneFunction['NumberOfProcesses'])
      node_script += """    )\n"""
      node_script += """#\n"""
      node_script += """__data = []\n"""
      node_script += """if __method == "Direct":\n"""
      node_script += """  logging.debug("ComputationFunctionNode: Direct computation")\n"""
      node_script += """  if len(computation["inputValues"][0][0]) == 2:\n"""
      node_script += """    raise ValueError("ComputationFunctionNode: you have to build explicitly the controled evolution model and its tangent and adjoint operators, instead of using approximate derivative.")"""
      node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
      node_script += """  __data = FDA.DirectOperator(numpy.matrix( __Xcurrent ).T)\n"""
      node_script += """#\n"""
      node_script += """if __method == "Tangent":\n"""
      node_script += """  logging.debug("ComputationFunctionNode: Tangent computation")\n"""
      node_script += """  __Xcurrent  = computation["inputValues"][0][0][0]\n"""
      node_script += """  __dXcurrent = computation["inputValues"][0][0][1]\n"""
      node_script += """  __data = FDA.TangentOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __dXcurrent ).T))\n"""
      node_script += """#\n"""
      node_script += """if __method == "Adjoint":\n"""
      node_script += """  logging.debug("ComputationFunctionNode: Adjoint computation")\n"""
      node_script += """  __Xcurrent = computation["inputValues"][0][0][0]\n"""
      node_script += """  __Ycurrent = computation["inputValues"][0][0][1]\n"""
      node_script += """  __data = FDA.AdjointOperator((numpy.matrix( __Xcurrent ).T, numpy.matrix( __Ycurrent ).T))\n"""
      node_script += """#\n"""
      node_script += """logging.debug("ComputationFunctionNode: Formatting the output")\n"""
      node_script += """__it = 1.*numpy.ravel(__data)\n"""
      node_script += """outputValues = [[[[]]]]\n"""
      node_script += """outputValues[0][0][0] = list(__it)\n"""
      node_script += """#\n"""
      node_script += """result = {}\n"""
      node_script += """result["outputValues"]        = outputValues\n"""
      node_script += """result["specificOutputInfos"] = []\n"""
      node_script += """result["returnCode"]          = 0\n"""
      node_script += """result["errorMessage"]        = ""\n"""
      node_script += """# ==============================================\n"""
      #
      opt_script_nodeEM.setScript(node_script)
      opt_script_nodeEM.edAddInputPort("computation", t_param_input)
      opt_script_nodeEM.edAddOutputPort("result", t_param_output)

    else:
      factory_opt_script_node = catalogAd.getNodeFromNodeMap("FakeOptimizerLoopNode")
      opt_script_nodeEM = factory_opt_script_node.cloneNode("FakeFunctionNode")
    #
    if ExecuteInContainer and bool(UseSeparateContainer):
      opt_script_nodeEM.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
      opt_script_nodeEM.setContainer(mycontainer)

  # Add computation bloc
  if "Observers" in list(study_config.keys()):
    execution_bloc = runtime.createBloc("Execution Bloc")
    optimizer_node.edSetNode(execution_bloc)

    # Add a node that permits to configure the switch
    factory_read_for_switch_node = catalogAd.getNodeFromNodeMap("ReadForSwitchNode")
    read_for_switch_node = factory_read_for_switch_node.cloneNode("ReadForSwitch")
    if ExecuteInContainer and bool(UseSeparateContainer):
      read_for_switch_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
      read_for_switch_node.setContainer(mycontainer)
    execution_bloc.edAddChild(read_for_switch_node)
    ADAO_Case.edAddDFLink(optimizer_node.edGetSamplePort(), read_for_switch_node.getInputPort("data"))

    # Add a switch
    switch_node = runtime.createSwitch("Execution Switch")
    execution_bloc.edAddChild(switch_node)
    # Connect switch
    ADAO_Case.edAddDFLink(read_for_switch_node.getOutputPort("switch_value"), switch_node.edGetConditionPort())

    # First case: computation bloc
    computation_blocOO = runtime.createBloc("computation_blocOO")
    computation_blocOO.edAddChild(opt_script_nodeOO)
    switch_node.edSetNode(1, computation_blocOO)

    # We connect with the script
    ADAO_Case.edAddDFLink(read_for_switch_node.getOutputPort("data"), opt_script_nodeOO.getInputPort("computation"))
    ADAO_Case.edAddDFLink(opt_script_nodeOO.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

    # Second case: evolution bloc
    if "EvolutionModel" in list(study_config.keys()):
      computation_blocEM = runtime.createBloc("computation_blocEM")
      computation_blocEM.edAddChild(opt_script_nodeEM)
      switch_node.edSetNode(2, computation_blocEM)

      # We connect with the script
      ADAO_Case.edAddDFLink(read_for_switch_node.getOutputPort("data"), opt_script_nodeEM.getInputPort("computation"))
      ADAO_Case.edAddDFLink(opt_script_nodeEM.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

    # For each observer add a new bloc in the switch
    observer_config = study_config["Observers"]
    for observer_name in observer_config:
      observer_cfg = observer_config[observer_name]
      observer_bloc = runtime.createBloc("Observer %s" % observer_name)
      switch_node.edSetNode(observer_cfg["number"], observer_bloc)

      factory_extract_data_node = catalogAd.getNodeFromNodeMap("ExtractDataNode")
      extract_data_node = factory_extract_data_node.cloneNode("ExtractData")
      if ExecuteInContainer and bool(UseSeparateContainer):
        extract_data_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
        extract_data_node.setContainer(mycontainer)
      observer_bloc.edAddChild(extract_data_node)
      ADAO_Case.edAddDFLink(read_for_switch_node.getOutputPort("data"), extract_data_node.getInputPort("data"))

      observation_node = None
      if observer_cfg["nodetype"] == "String":
        factory_observation_node = catalogAd.getNodeFromNodeMap("ObservationNodeString")
        observation_node = factory_observation_node.cloneNode("Observation")
        node_script = observation_node.getScript()
        node_script += observer_cfg["String"]
        observation_node.setScript(node_script)
      else:
        factory_observation_node = catalogAd.getNodeFromNodeMap("ObservationNodeFile")
        observation_node = factory_observation_node.cloneNode("Observation")
        _Internal_Add_dir_script_ports( observation_node, observer_cfg["Script"], repertory, base_repertory, t_string)
      if ExecuteInContainer and bool(UseSeparateContainer):
        observation_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
        observation_node.setContainer(mycontainer)
      observer_bloc.edAddChild(observation_node)
      ADAO_Case.edAddDFLink(extract_data_node.getOutputPort("var"), observation_node.getInputPort("var"))
      ADAO_Case.edAddDFLink(extract_data_node.getOutputPort("info"), observation_node.getInputPort("info"))

      factory_end_observation_node = catalogAd.getNodeFromNodeMap("EndObservationNode")
      end_observation_node = factory_end_observation_node.cloneNode("EndObservation")
      if ExecuteInContainer and bool(UseSeparateContainer):
        end_observation_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
        end_observation_node.setContainer(mycontainer)
      observer_bloc.edAddChild(end_observation_node)
      ADAO_Case.edAddCFLink(observation_node, end_observation_node)
      ADAO_Case.edAddDFLink(end_observation_node.getOutputPort("output"), optimizer_node.edGetPortForOutPool())

  elif "EvolutionModel" in list(study_config.keys()):
    execution_bloc = runtime.createBloc("Execution Bloc")
    optimizer_node.edSetNode(execution_bloc)

    # Add a node that permits to configure the switch
    factory_read_for_switch_node = catalogAd.getNodeFromNodeMap("ReadForSwitchNode")
    read_for_switch_node = factory_read_for_switch_node.cloneNode("ReadForSwitch")
    if ExecuteInContainer and bool(UseSeparateContainer):
      read_for_switch_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
      read_for_switch_node.setContainer(mycontainer)
    execution_bloc.edAddChild(read_for_switch_node)
    ADAO_Case.edAddDFLink(optimizer_node.edGetSamplePort(), read_for_switch_node.getInputPort("data"))

    # Add a switch
    switch_node = runtime.createSwitch("Execution Switch")
    execution_bloc.edAddChild(switch_node)
    # Connect switch
    ADAO_Case.edAddDFLink(read_for_switch_node.getOutputPort("switch_value"), switch_node.edGetConditionPort())

    # First case: computation bloc
    computation_blocOO = runtime.createBloc("computation_blocOO")
    computation_blocOO.edAddChild(opt_script_nodeOO)
    switch_node.edSetNode(1, computation_blocOO)

    # We connect with the script
    ADAO_Case.edAddDFLink(read_for_switch_node.getOutputPort("data"), opt_script_nodeOO.getInputPort("computation"))
    ADAO_Case.edAddDFLink(opt_script_nodeOO.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

    # Second case: evolution bloc
    computation_blocEM = runtime.createBloc("computation_blocEM")
    computation_blocEM.edAddChild(opt_script_nodeEM)
    switch_node.edSetNode(2, computation_blocEM)

    # We connect with the script
    ADAO_Case.edAddDFLink(read_for_switch_node.getOutputPort("data"), opt_script_nodeEM.getInputPort("computation"))
    ADAO_Case.edAddDFLink(opt_script_nodeEM.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

  else:
    computation_blocOO = runtime.createBloc("computation_blocOO")
    optimizer_node.edSetNode(computation_blocOO)
    computation_blocOO.edAddChild(opt_script_nodeOO)

    # We connect Optimizer with the script
    ADAO_Case.edAddDFLink(optimizer_node.edGetSamplePort(), opt_script_nodeOO.getInputPort("computation"))
    ADAO_Case.edAddDFLink(opt_script_nodeOO.getOutputPort("result"), optimizer_node.edGetPortForOutPool())

  # Connect node with InitUserData
  if "ObservationOperator" in init_config["Target"]:
    opt_node_script = opt_script_nodeOO.getScript()
    opt_node_script = "__builtins__[\"init_data\"] = init_data\n" + opt_node_script
    opt_script_nodeOO.setScript(opt_node_script)
    opt_script_nodeOO.edAddInputPort("init_data", t_pyobj)
    ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), opt_script_nodeOO.getInputPort("init_data"))

  # Step 4: create post-processing from user configuration
  if "UserPostAnalysis" in list(study_config.keys()):
    analysis_config = study_config["UserPostAnalysis"]
    if analysis_config["From"] == "String":
      factory_analysis_node = catalogAd.getNodeFromNodeMap("SimpleUserAnalysis")
      analysis_node = factory_analysis_node.cloneNode("UsePostAnalysis")
      if ExecuteInContainer and bool(UseSeparateContainer):
        analysis_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
        analysis_node.setContainer(mycontainer)
      default_script = analysis_node.getScript()
      final_script = default_script + analysis_config["Data"]
      analysis_node.setScript(final_script)
      ADAO_Case.edAddChild(analysis_node)
      ADAO_Case.edAddCFLink(compute_bloc, analysis_node)
      if AlgoType[study_config["Algorithm"]] == "Optim":
        ADAO_Case.edAddDFLink(optimizer_node.edGetAlgoResultPort(), analysis_node.getInputPort("Study"))
      else:
        ADAO_Case.edAddDFLink(execute_node.getOutputPort("Study"), analysis_node.getInputPort("Study"))

      # Connect node with InitUserData
      if "UserPostAnalysis" in init_config["Target"]:
        node_script = analysis_node.getScript()
        node_script = "__builtins__[\"init_data\"] = init_data\n" + node_script
        analysis_node.setScript(node_script)
        analysis_node.edAddInputPort("init_data", t_pyobj)
        ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), analysis_node.getInputPort("init_data"))

    elif analysis_config["From"] == "Script":
      factory_analysis_node = catalogAd.getNodeFromNodeMap("SimpleUserAnalysis")
      analysis_node = factory_analysis_node.cloneNode("UserPostAnalysis")
      if ExecuteInContainer and bool(UseSeparateContainer):
        analysis_node.setExecutionMode(SALOMERuntime.PythonNode.REMOTE_STR)
        analysis_node.setContainer(mycontainer)
      default_script = analysis_node.getScript()
      analysis_file_name = analysis_config["Data"]
      if repertory and os.path.exists(os.path.join(base_repertory, os.path.basename(analysis_file_name))):
        analysis_file_name = os.path.join(base_repertory, os.path.basename(analysis_file_name))
      try:
        analysis_file = open(analysis_file_name, 'r')
      except:
        raise ValueError("Exception in opening analysis file: " + str(analysis_config["Data"]))
      node_script  = "#-*- coding: utf-8 -*-\n"
      node_script += "import sys, os \n"
      node_script += "filepath = \"" + os.path.dirname(analysis_file_name) + "\"\n"
      node_script += "filename = \"" + os.path.basename(analysis_file_name) + "\"\n"
      node_script += "if sys.path.count(filepath)==0 or (sys.path.count(filepath)>0 and sys.path.index(filepath)>0):\n"
      node_script += "  sys.path.insert(0,filepath)\n"
      node_script += default_script
      node_script += analysis_file.read()
      analysis_node.setScript(node_script)
      ADAO_Case.edAddChild(analysis_node)
      ADAO_Case.edAddCFLink(compute_bloc, analysis_node)
      if AlgoType[study_config["Algorithm"]] == "Optim":
        ADAO_Case.edAddDFLink(optimizer_node.edGetAlgoResultPort(), analysis_node.getInputPort("Study"))
      else:
        ADAO_Case.edAddDFLink(execute_node.getOutputPort("Study"), analysis_node.getInputPort("Study"))
      # Connect node with InitUserData
      if "UserPostAnalysis" in init_config["Target"]:
        node_script = analysis_node.getScript()
        node_script = "__builtins__[\"init_data\"] = init_data\n" + node_script
        analysis_node.setScript(node_script)
        analysis_node.edAddInputPort("init_data", t_pyobj)
        ADAO_Case.edAddDFLink(init_node.getOutputPort("init_data"), analysis_node.getInputPort("init_data"))

      pass

  return proc

def write_yacs_proc(proc, yacs_schema_filename):

  proc.saveSchema(yacs_schema_filename)

