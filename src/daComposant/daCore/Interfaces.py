# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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

"""
    Définit les outils d'interfaces normalisées de cas.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os
import sys
import numpy
import mimetypes
import logging
import copy
from daCore import Persistence
from daCore import PlatformInfo
from daCore import Templates

# ==============================================================================
class GenericCaseViewer(object):
    """
    Gestion des commandes de creation d'une vue de cas
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        self._name         = str(__name)
        self._objname      = str(__objname)
        self._lineSerie    = []
        self._switchoff    = False
        self._numobservers = 2
        self._content      = __content
        self._object       = __object
        self._missing = """raise ValueError("This case requires beforehand to import or define the variable named <%s>. When corrected, remove this command, correct and uncomment the following one.")\n# """
    def _append(self, *args):
        "Transformation de commande individuelle en enregistrement"
        raise NotImplementedError()
    def _extract(self, *args):
        "Transformation d'enregistrement en commande individuelle"
        raise NotImplementedError()
    def _finalize(self, __upa=None):
        "Enregistrement du final"
        if __upa is not None and len(__upa)>0:
            self._lineSerie.append("%s.execute()"%(self._objname,))
            self._lineSerie.append(__upa)
    def _addLine(self, line=""):
        "Ajoute un enregistrement individuel"
        self._lineSerie.append(line)
    def _get_objname(self):
        return self._objname
    def dump(self, __filename=None, __upa=None):
        "Restitution normalisée des commandes"
        self._finalize(__upa)
        __text = "\n".join(self._lineSerie)
        __text +="\n"
        if __filename is not None:
            __file = os.path.abspath(__filename)
            __fid = open(__file,"w")
            __fid.write(__text)
            __fid.close()
        return __text
    def load(self, __filename=None, __content=None, __object=None):
        "Chargement normalisé des commandes"
        if __filename is not None and os.path.exists(__filename):
            self._content = open(__filename, 'r').read()
        elif __content is not None and type(__content) is str:
            self._content = __content
        elif __object is not None and type(__object) is dict:
            self._object = copy.deepcopy(__object)
        else:
            pass # use "self._content" from initialization
        __commands = self._extract(self._content, self._object)
        return __commands

class _TUIViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas ADAO TUI (Cas<->TUI)
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Python script using ADAO TUI\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("from adao import adaoBuilder")
        self._addLine("%s = adaoBuilder.New('%s')"%(self._objname, self._name))
        if self._content is not None:
            for command in self._content:
                self._append(*command)
    def _append(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Transformation d'une commande individuelle en un enregistrement"
        if __command is not None and __keys is not None and __local is not None:
            __text  = ""
            if __pre is not None:
                __text += "%s = "%__pre
            __text += "%s.%s( "%(self._objname,str(__command))
            if "self" in __keys: __keys.remove("self")
            if __command not in ("set","get") and "Concept" in __keys: __keys.remove("Concept")
            for k in __keys:
                __v = __local[k]
                if __v is None: continue
                if   k == "Checked"              and not __v: continue
                if   k == "Stored"               and not __v: continue
                if   k == "ColMajor"             and not __v: continue
                if   k == "InputFunctionAsMulti" and not __v: continue
                if   k == "nextStep"             and not __v: continue
                if   k == "AvoidRC"              and     __v: continue
                if   k == "noDetails":                        continue
                if isinstance(__v,Persistence.Persistence): __v = __v.values()
                if callable(__v): __text = self._missing%__v.__name__+__text
                if isinstance(__v,dict):
                    for val in __v.values():
                        if callable(val): __text = self._missing%val.__name__+__text
                numpy.set_printoptions(precision=15,threshold=1000000,linewidth=1000*15)
                __text += "%s=%s, "%(k,repr(__v))
                numpy.set_printoptions(precision=8,threshold=1000,linewidth=75)
            __text.rstrip(", ")
            __text += ")"
            self._addLine(__text)
    def _extract(self, __multilines="", __object=None):
        "Transformation un enregistrement en une commande individuelle"
        __is_case = False
        __commands = []
        __multilines = __multilines.replace("\r\n","\n")
        for line in __multilines.split("\n"):
            if "adaoBuilder.New" in line and "=" in line:
                self._objname = line.split("=")[0].strip()
                __is_case = True
                logging.debug("TUI Extracting commands of '%s' object..."%(self._objname,))
            if not __is_case:
                continue
            else:
                if self._objname+".set" in line:
                    __commands.append( line.replace(self._objname+".","",1) )
                    logging.debug("TUI Extracted command: %s"%(__commands[-1],))
        return __commands

class _COMViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas COMM (Eficas Native Format/Cas<-COM)
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        self._observerIndex = 0
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Python script using ADAO COMM\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("#")
        self._addLine("%s = {}"%__objname)
        if self._content is not None:
            for command in self._content:
                self._append(*command)
    def _extract(self, __multilines=None, __object=None):
        "Transformation un enregistrement en une commande individuelle"
        if __multilines is not None:
            __multilines = __multilines.replace("ASSIMILATION_STUDY","dict")
            __multilines = __multilines.replace("CHECKING_STUDY",    "dict")
            __multilines = __multilines.replace("_F(",               "dict(")
            __multilines = __multilines.replace(",),);",             ",),)")
        __fulllines = ""
        for line in __multilines.split("\n"):
            if len(line) < 1: continue
            __fulllines += line + "\n"
        __multilines = __fulllines
        self._objname = "case"
        self._objdata = None
        exec("self._objdata = "+__multilines)
        #
        if self._objdata is None or not(type(self._objdata) is dict) or not('AlgorithmParameters' in self._objdata):
            raise ValueError("Impossible to load given content as an ADAO COMM one (no dictionnary or no 'AlgorithmParameters' key found).")
        # ----------------------------------------------------------------------
        logging.debug("COMM Extracting commands of '%s' object..."%(self._objname,))
        __commands = []
        __UserPostAnalysis = ""
        for k,r in self._objdata.items():
            __command = k
            logging.debug("COMM Extracted command: %s:%s"%(k, r))
            if   __command == "StudyName" and len(str(r))>0:
                __commands.append( "set( Concept='Name', String='%s')"%(str(r),) )
            elif   __command == "StudyRepertory":
                __commands.append( "set( Concept='Directory', String='%s')"%(str(r),) )
            #
            elif __command == "UserPostAnalysis" and type(r) is dict:
                if 'STRING' in r:
                    __UserPostAnalysis = r['STRING']
                elif 'SCRIPT_FILE' in r and os.path.exists(r['SCRIPT_FILE']):
                    __UserPostAnalysis = open(r['SCRIPT_FILE'],'r').read()
                elif 'Template' in r and 'ValueTemplate' in r:
                    # AnalysisPrinter...
                    __UserPostAnalysis = r['ValueTemplate']
                else:
                    __UserPostAnalysis = ""
                __UserPostAnalysis = __UserPostAnalysis.replace("ADD",self._objname)
            #
            elif __command == "AlgorithmParameters" and type(r) is dict and 'Algorithm' in r:
                if 'data' in r and r['Parameters'] == 'Dict':
                    __from = r['data']
                    if 'STRING' in __from:
                        __parameters = ", Parameters=%s"%(repr(eval(__from['STRING'])),)
                    elif 'SCRIPT_FILE' in __from and os.path.exists(__from['SCRIPT_FILE']):
                        __parameters = ", Script='%s'"%(__from['SCRIPT_FILE'],)
                else: # if 'Parameters' in r and r['Parameters'] == 'Defaults':
                    __Dict = copy.deepcopy(r)
                    __Dict.pop('Algorithm','')
                    __Dict.pop('Parameters','')
                    if 'SetSeed' in __Dict:__Dict['SetSeed'] = int(__Dict['SetSeed'])
                    if 'BoxBounds' in __Dict and type(__Dict['BoxBounds']) is str:
                        __Dict['BoxBounds'] = eval(__Dict['BoxBounds'])
                    if len(__Dict) > 0:
                        __parameters = ', Parameters=%s'%(repr(__Dict),)
                    else:
                        __parameters = ""
                __commands.append( "set( Concept='AlgorithmParameters', Algorithm='%s'%s )"%(r['Algorithm'],__parameters) )
            #
            elif __command == "Observers" and type(r) is dict and 'SELECTION' in r:
                if type(r['SELECTION']) is str:
                    __selection = (r['SELECTION'],)
                else:
                    __selection = tuple(r['SELECTION'])
                for sk in __selection:
                    __idata = r['%s_data'%sk]
                    if __idata['NodeType'] == 'Template' and 'Template' in __idata:
                        __template = __idata['Template']
                        if 'Info' in __idata:
                            __info = ", Info='%s'"%(__idata['Info'],)
                        else:
                            __info = ""
                        __commands.append( "set( Concept='Observer', Variable='%s', Template='%s'%s )"%(sk,__template,__info) )
                    if __idata['NodeType'] == 'String' and 'Value' in __idata:
                        __value =__idata['Value']
                        __commands.append( "set( Concept='Observer', Variable='%s', String='%s' )"%(sk,__value) )
            #
            # Background, ObservationError, ObservationOperator...
            elif type(r) is dict:
                __argumentsList = []
                if 'Stored' in r and bool(r['Stored']):
                    __argumentsList.append(['Stored',True])
                if 'INPUT_TYPE' in r and 'data' in r:
                    # Vector, Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Function
                    __itype = r['INPUT_TYPE']
                    __idata = r['data']
                    if 'FROM' in __idata:
                        # String, Script, DataFile, Template, ScriptWithOneFunction, ScriptWithFunctions
                        __ifrom = __idata['FROM']
                        __idata.pop('FROM','')
                        if __ifrom == 'String' or __ifrom == 'Template':
                            __argumentsList.append([__itype,__idata['STRING']])
                        if __ifrom == 'Script':
                            __argumentsList.append([__itype,True])
                            __argumentsList.append(['Script',__idata['SCRIPT_FILE']])
                        if __ifrom == 'DataFile':
                            __argumentsList.append([__itype,True])
                            __argumentsList.append(['DataFile',__idata['DATA_FILE']])
                        if __ifrom == 'ScriptWithOneFunction':
                            __argumentsList.append(['OneFunction',True])
                            __argumentsList.append(['Script',__idata.pop('SCRIPTWITHONEFUNCTION_FILE')])
                            if len(__idata)>0:
                                __argumentsList.append(['Parameters',__idata])
                        if __ifrom == 'ScriptWithFunctions':
                            __argumentsList.append(['ThreeFunctions',True])
                            __argumentsList.append(['Script',__idata.pop('SCRIPTWITHFUNCTIONS_FILE')])
                            if len(__idata)>0:
                                __argumentsList.append(['Parameters',__idata])
                __arguments = ["%s = %s"%(k,repr(v)) for k,v in __argumentsList]
                __commands.append( "set( Concept='%s', %s )"%(__command, ", ".join(__arguments)))
        #
        # ----------------------------------------------------------------------
        __commands.sort() # Pour commencer par 'AlgorithmParameters'
        __commands.append(__UserPostAnalysis)
        return __commands

class _SCDViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas SCD (Study Config Dictionary/Cas->SCD)
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Input for ADAO converter to YACS\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("#")
        self._addLine("study_config = {}")
        self._addLine("study_config['StudyType'] = 'ASSIMILATION_STUDY'")
        self._addLine("study_config['Name'] = '%s'"%self._name)
        self._addLine("observers = {}")
        self._addLine("study_config['Observers'] = observers")
        self._addLine("#")
        self._addLine("inputvariables_config = {}")
        self._addLine("inputvariables_config['Order'] =['adao_default']")
        self._addLine("inputvariables_config['adao_default'] = -1")
        self._addLine("study_config['InputVariables'] = inputvariables_config")
        self._addLine("#")
        self._addLine("outputvariables_config = {}")
        self._addLine("outputvariables_config['Order'] = ['adao_default']")
        self._addLine("outputvariables_config['adao_default'] = -1")
        self._addLine("study_config['OutputVariables'] = outputvariables_config")
        if __content is not None:
            for command in __content:
                self._append(*command)
    def _append(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Transformation d'une commande individuelle en un enregistrement"
        if __command == "set": __command = __local["Concept"]
        else:                  __command = __command.replace("set", "", 1)
        #
        __text  = None
        if __command in (None, 'execute', 'executePythonScheme', 'executeYACSScheme', 'get', 'Name'):
            return
        elif __command in ['Debug', 'setDebug']:
            __text  = "#\nstudy_config['Debug'] = '1'"
        elif __command in ['NoDebug', 'setNoDebug']:
            __text  = "#\nstudy_config['Debug'] = '0'"
        elif __command in ['Observer', 'setObserver']:
            __obs   = __local['Variable']
            self._numobservers += 1
            __text  = "#\n"
            __text += "observers['%s'] = {}\n"%__obs
            if __local['String'] is not None:
                __text += "observers['%s']['nodetype'] = '%s'\n"%(__obs, 'String')
                __text += "observers['%s']['String'] = \"\"\"%s\"\"\"\n"%(__obs, __local['String'])
            if __local['Script'] is not None:
                __text += "observers['%s']['nodetype'] = '%s'\n"%(__obs, 'Script')
                __text += "observers['%s']['Script'] = \"%s\"\n"%(__obs, __local['Script'])
            if __local['Template'] is not None and __local['Template'] in Templates.ObserverTemplates:
                __text += "observers['%s']['nodetype'] = '%s'\n"%(__obs, 'String')
                __text += "observers['%s']['String'] = \"\"\"%s\"\"\"\n"%(__obs, Templates.ObserverTemplates[__local['Template']])
            if __local['Info'] is not None:
                __text += "observers['%s']['info'] = \"\"\"%s\"\"\"\n"%(__obs, __local['Info'])
            else:
                __text += "observers['%s']['info'] = \"\"\"%s\"\"\"\n"%(__obs, __obs)
            __text += "observers['%s']['number'] = %s"%(__obs, self._numobservers)
        elif __local is not None: # __keys is not None and
            numpy.set_printoptions(precision=15,threshold=1000000,linewidth=1000*15)
            __text  = "#\n"
            __text += "%s_config = {}\n"%__command
            __local.pop('self','')
            __to_be_removed = []
            for __k,__v in __local.items():
                if __v is None: __to_be_removed.append(__k)
            for __k in __to_be_removed:
                __local.pop(__k)
            for __k,__v in __local.items():
                if __k == "Concept": continue
                if __k in ['ScalarSparseMatrix','DiagonalSparseMatrix','Matrix','OneFunction','ThreeFunctions'] and 'Script' in __local and __local['Script'] is not None: continue
                if __k in ['Vector','VectorSerie'] and 'DataFile' in __local and __local['DataFile'] is not None: continue
                if __k == 'Algorithm':
                    __text += "study_config['Algorithm'] = %s\n"%(repr(__v))
                elif __k == 'DataFile':
                    __k = 'Vector'
                    __f = 'DataFile'
                    __v = "'"+repr(__v)+"'"
                    for __lk in ['Vector','VectorSerie']:
                        if __lk in __local and __local[__lk]: __k = __lk
                    __text += "%s_config['Type'] = '%s'\n"%(__command,__k)
                    __text += "%s_config['From'] = '%s'\n"%(__command,__f)
                    __text += "%s_config['Data'] = %s\n"%(__command,__v)
                    __text = __text.replace("''","'")
                elif __k == 'Script':
                    __k = 'Vector'
                    __f = 'Script'
                    __v = "'"+repr(__v)+"'"
                    for __lk in ['ScalarSparseMatrix','DiagonalSparseMatrix','Matrix']:
                        if __lk in __local and __local[__lk]: __k = __lk
                    if __command == "AlgorithmParameters": __k = "Dict"
                    if 'OneFunction' in __local and __local['OneFunction']:
                        __text += "%s_ScriptWithOneFunction = {}\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['Script'] = {}\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['Script']['Direct'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithOneFunction['Script']['Tangent'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithOneFunction['Script']['Adjoint'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithOneFunction['DifferentialIncrement'] = 1e-06\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['CenteredFiniteDifference'] = 0\n"%(__command,)
                        __k = 'Function'
                        __f = 'ScriptWithOneFunction'
                        __v = '%s_ScriptWithOneFunction'%(__command,)
                    if 'ThreeFunctions' in __local and __local['ThreeFunctions']:
                        __text += "%s_ScriptWithFunctions = {}\n"%(__command,)
                        __text += "%s_ScriptWithFunctions['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"%(__command,)
                        __text += "%s_ScriptWithFunctions['Script'] = {}\n"%(__command,)
                        __text += "%s_ScriptWithFunctions['Script']['Direct'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithFunctions['Script']['Tangent'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithFunctions['Script']['Adjoint'] = %s\n"%(__command,__v)
                        __k = 'Function'
                        __f = 'ScriptWithFunctions'
                        __v = '%s_ScriptWithFunctions'%(__command,)
                    __text += "%s_config['Type'] = '%s'\n"%(__command,__k)
                    __text += "%s_config['From'] = '%s'\n"%(__command,__f)
                    __text += "%s_config['Data'] = %s\n"%(__command,__v)
                    __text = __text.replace("''","'")
                elif __k in ('Stored', 'Checked', 'ColMajor', 'InputFunctionAsMulti', 'nextStep'):
                    if bool(__v):
                        __text += "%s_config['%s'] = '%s'\n"%(__command,__k,int(bool(__v)))
                elif __k in ('AvoidRC', 'noDetails'):
                    if not bool(__v):
                        __text += "%s_config['%s'] = '%s'\n"%(__command,__k,int(bool(__v)))
                else:
                    if __k == 'Parameters': __k = "Dict"
                    if isinstance(__v,Persistence.Persistence): __v = __v.values()
                    if callable(__v): __text = self._missing%__v.__name__+__text
                    if isinstance(__v,dict):
                        for val in __v.values():
                            if callable(val): __text = self._missing%val.__name__+__text
                    __text += "%s_config['Type'] = '%s'\n"%(__command,__k)
                    __text += "%s_config['From'] = '%s'\n"%(__command,'String')
                    __text += "%s_config['Data'] = \"\"\"%s\"\"\"\n"%(__command,repr(__v))
            __text += "study_config['%s'] = %s_config"%(__command,__command)
            numpy.set_printoptions(precision=8,threshold=1000,linewidth=75)
            if __switchoff:
                self._switchoff = True
        if __text is not None: self._addLine(__text)
        if not __switchoff:
            self._switchoff = False
    def _finalize(self, *__args):
        self.__loadVariablesByScript()
        self._addLine("#")
        self._addLine("Analysis_config = {}")
        self._addLine("Analysis_config['From'] = 'String'")
        self._addLine("Analysis_config['Data'] = \"\"\"import numpy")
        self._addLine("xa=numpy.ravel(ADD.get('Analysis')[-1])")
        self._addLine("print('Analysis:',xa)\"\"\"")
        self._addLine("study_config['UserPostAnalysis'] = Analysis_config")
    def __loadVariablesByScript(self):
        __ExecVariables = {} # Necessaire pour recuperer la variable
        exec("\n".join(self._lineSerie), __ExecVariables)
        study_config = __ExecVariables['study_config']
        # Pour Python 3 : self.__hasAlgorithm = bool(study_config['Algorithm'])
        if 'Algorithm' in study_config:
            self.__hasAlgorithm = True
        else:
            self.__hasAlgorithm = False
        if not self.__hasAlgorithm and \
                "AlgorithmParameters" in study_config and \
                isinstance(study_config['AlgorithmParameters'], dict) and \
                "From" in study_config['AlgorithmParameters'] and \
                "Data" in study_config['AlgorithmParameters'] and \
                study_config['AlgorithmParameters']['From'] == 'Script':
            __asScript = study_config['AlgorithmParameters']['Data']
            __var = ImportFromScript(__asScript).getvalue( "Algorithm" )
            __text = "#\nstudy_config['Algorithm'] = '%s'"%(__var,)
            self._addLine(__text)
        if self.__hasAlgorithm and \
                "AlgorithmParameters" in study_config and \
                isinstance(study_config['AlgorithmParameters'], dict) and \
                "From" not in study_config['AlgorithmParameters'] and \
                "Data" not in study_config['AlgorithmParameters']:
            __text  = "#\n"
            __text += "AlgorithmParameters_config['Type'] = 'Dict'\n"
            __text += "AlgorithmParameters_config['From'] = 'String'\n"
            __text += "AlgorithmParameters_config['Data'] = '{}'\n"
            self._addLine(__text)
        del study_config

class _YACSViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas YACS (Cas->SCD->YACS)
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        self.__internalSCD = _SCDViewer(__name, __objname, __content, __object)
        self._append       = self.__internalSCD._append
    def dump(self, __filename=None, __upa=None):
        "Restitution normalisée des commandes"
        # -----
        if __filename is None:
            raise ValueError("A file name has to be given for YACS XML output.")
        else:
            __file    = os.path.abspath(__filename)
            if os.path.isfile(__file) or os.path.islink(__file):
                os.remove(__file)
        # -----
        if not PlatformInfo.has_salome or \
            not PlatformInfo.has_adao:
            raise ImportError(
                "Unable to get SALOME or ADAO environnement variables for YACS conversion.\n"+\
                "Please load the right environnement before trying to use it.")
        else:
            from daYacsSchemaCreator.run import create_schema_from_content
        # -----
        self.__internalSCD._finalize(__upa)
        __SCDdump = self.__internalSCD.dump()
        create_schema_from_content(__SCDdump, __file)
        # -----
        if not os.path.exists(__file):
            __msg  = "An error occured during the ADAO YACS Schema build for\n"
            __msg += "the target output file:\n"
            __msg += "  %s\n"%__file
            __msg += "See errors details in your launching terminal log.\n"
            raise ValueError(__msg)
        # -----
        __fid = open(__file,"r")
        __text = __fid.read()
        __fid.close()
        return __text

# ==============================================================================
class ImportFromScript(object):
    """
    Obtention d'une variable nommee depuis un fichier script importé
    """
    __slots__ = ("__basename", "__filenspace", "__filestring")
    def __init__(self, __filename=None):
        "Verifie l'existence et importe le script"
        if __filename is None:
            raise ValueError("The name of the file, containing the variable to be read, has to be specified.")
        if not os.path.isfile(__filename):
            raise ValueError("The file containing the variable to be imported doesn't seem to exist. Please check the file. The given file name is:\n  \"%s\""%str(__filename))
        if os.path.dirname(__filename) != '':
            sys.path.insert(0, os.path.dirname(__filename))
            __basename = os.path.basename(__filename).rstrip(".py")
        else:
            __basename = __filename.rstrip(".py")
        PlatformInfo.checkFileNameImportability( __basename+".py" )
        self.__basename = __basename
        self.__filenspace = __import__(__basename, globals(), locals(), [])
        self.__filestring = open(__filename,'r').read()
    def getvalue(self, __varname=None, __synonym=None ):
        "Renvoie la variable demandee par son nom ou son synonyme"
        if __varname is None:
            raise ValueError("The name of the variable to be read has to be specified. Please check the content of the file and the syntax.")
        if not hasattr(self.__filenspace, __varname):
            if __synonym is None:
                raise ValueError("The imported script file \"%s\" doesn't contain the mandatory variable \"%s\" to be read. Please check the content of the file and the syntax."%(str(self.__basename)+".py",__varname))
            elif not hasattr(self.__filenspace, __synonym):
                raise ValueError("The imported script file \"%s\" doesn't contain the mandatory variable \"%s\" to be read. Please check the content of the file and the syntax."%(str(self.__basename)+".py",__synonym))
            else:
                return getattr(self.__filenspace, __synonym)
        else:
            return getattr(self.__filenspace, __varname)
    def getstring(self):
        "Renvoie le script complet"
        return self.__filestring

# ==============================================================================
class ImportDetector(object):
    """
    Détection des caractéristiques de fichiers ou objets en entrée
    """
    __slots__ = (
        "__url", "__usr", "__root", "__end")
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
    #
    def __init__(self, __url, UserMime=""):
        if __url is None:
            raise ValueError("The name or url of the file object has to be specified.")
        if __url is bytes:
            self.__url = __url.decode()
        else:
            self.__url = str(__url)
        if UserMime is bytes:
            self.__usr = UserMime.decode().lower()
        else:
            self.__usr = str(UserMime).lower()
        (self.__root, self.__end) = os.path.splitext(self.__url)
        #
        mimetypes.add_type('application/numpy.npy', '.npy')
        mimetypes.add_type('application/numpy.npz', '.npz')
        mimetypes.add_type('application/dymola.sdf', '.sdf')
        if sys.platform.startswith("win"):
            mimetypes.add_type('text/plain', '.txt')
            mimetypes.add_type('text/csv', '.csv')
            mimetypes.add_type('text/tab-separated-values', '.tsv')
    #
    # File related tests
    # ------------------
    def is_local_file(self):
        if os.path.isfile(os.path.realpath(self.__url)):
            return True
        else:
            return False
    def is_not_local_file(self):
        if not os.path.isfile(os.path.realpath(self.__url)):
            return True
        else:
            return False
    def raise_error_if_not_local_file(self):
        if not os.path.isfile(os.path.realpath(self.__url)):
            raise ValueError("The name or the url of the file object doesn't seem to exist. The given name is:\n  \"%s\""%str(self.__url))
        else:
            return False
    #
    # Directory related tests
    # -----------------------
    def is_local_dir(self):
        if os.path.isdir(self.__url):
            return True
        else:
            return False
    def is_not_local_dir(self):
        if not os.path.isdir(self.__url):
            return True
        else:
            return False
    def raise_error_if_not_local_dir(self):
        if not os.path.isdir(self.__url):
            raise ValueError("The name or the url of the directory object doesn't seem to exist. The given name is:\n  \"%s\""%str(self.__url))
        else:
            return False
    #
    # Mime related functions
    # ------------------------
    def get_standard_mime(self):
        (__mtype, __encoding) = mimetypes.guess_type(self.__url, strict=False)
        return __mtype
    def get_user_mime(self):
        __fake = "fake."+self.__usr.lower()
        (__mtype, __encoding) = mimetypes.guess_type(__fake, strict=False)
        return __mtype
    def get_comprehensive_mime(self):
        if self.get_standard_mime() is not None:
            return self.get_standard_mime()
        elif self.get_user_mime() is not None:
            return self.get_user_mime()
        else:
            return None
    #
    # Name related functions
    # ----------------------
    def get_user_name(self):
        return self.__url
    def get_absolute_name(self):
        return os.path.abspath(os.path.realpath(self.__url))
    def get_extension(self):
        return self.__end

class ImportFromFile(object):
    """
    Obtention de variables disrétisées en 1D, définies par une ou des variables
    nommées, et sous la forme d'une série de points éventuellement indexés. La
    lecture d'un fichier au format spécifié (ou intuité) permet de charger ces
    fonctions depuis :
        - des fichiers textes en colonnes de type TXT, CSV, TSV...
        - des fichiers de données binaires NPY, NPZ, SDF...
    La lecture du fichier complet ne se fait que si nécessaire, pour assurer la
    performance tout en disposant de l'interprétation du contenu. Les fichiers
    textes doivent présenter en première ligne (hors commentaire ou ligne vide)
    les noms des variables de colonnes. Les commentaires commencent par un "#".
    """
    __slots__ = (
        "_filename", "_colnames", "_colindex", "_varsline", "_format",
        "_delimiter", "_skiprows", "__url", "__filestring", "__header",
        "__allowvoid", "__binaryformats", "__supportedformats")
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
    #
    def __init__(self, Filename=None, ColNames=None, ColIndex=None, Format="Guess", AllowVoidNameList=True):
        """
        Verifie l'existence et les informations de définition du fichier. Les
        noms de colonnes ou de variables sont ignorées si le format ne permet
        pas de les indiquer.
        Arguments :
            - Filename : nom du fichier
            - ColNames : noms de la ou des colonnes/variables à lire
            - ColIndex : nom unique de la colonne/variable servant d'index
            - Format : format du fichier et/ou des données inclues
            - AllowVoidNameList : permet, si la liste de noms est vide, de
              prendre par défaut toutes les colonnes
        """
        self.__binaryformats =(
            "application/numpy.npy",
            "application/numpy.npz",
            "application/dymola.sdf",
            )
        self.__url = ImportDetector( Filename, Format)
        self.__url.raise_error_if_not_local_file()
        self._filename = self.__url.get_absolute_name()
        PlatformInfo.checkFileNameConformity( self._filename )
        #
        self._format = self.__url.get_comprehensive_mime()
        #
        self.__header, self._varsline, self._skiprows = self.__getentete()
        #
        if self._format == "text/csv" or Format.upper() == "CSV":
            self._format = "text/csv"
            self.__filestring = "".join(self.__header)
            if self.__filestring.count(",") > 1:
                self._delimiter = ","
            elif self.__filestring.count(";") > 1:
                self._delimiter = ";"
            else:
                self._delimiter = None
        elif self._format == "text/tab-separated-values" or Format.upper() == "TSV":
            self._format = "text/tab-separated-values"
            self._delimiter = "\t"
        else:
            self._delimiter = None
        #
        if ColNames is not None: self._colnames = tuple(ColNames)
        else:                    self._colnames = None
        #
        if ColIndex is not None: self._colindex = str(ColIndex)
        else:                    self._colindex = None
        #
        self.__allowvoid = bool(AllowVoidNameList)

    def __getentete(self, __nblines = 3):
        "Lit l'entête du fichier pour trouver la définition des variables"
        # La première ligne non vide non commentée est toujours considérée
        # porter les labels de colonne, donc pas des valeurs
        __header, __varsline, __skiprows = [], "", 1
        if self._format in self.__binaryformats:
            pass
        else:
            with open(self._filename,'r') as fid:
                __line = fid.readline().strip()
                while "#" in __line or len(__line) < 1:
                    __header.append(__line)
                    __skiprows += 1
                    __line = fid.readline().strip()
                __varsline = __line
                for i in range(max(0,__nblines)):
                    __header.append(fid.readline())
        return (__header, __varsline, __skiprows)

    def __getindices(self, __colnames, __colindex, __delimiter=None ):
        "Indices de colonnes correspondants à l'index et aux variables"
        if __delimiter is None:
            __varserie = self._varsline.strip('#').strip().split()
        else:
            __varserie = self._varsline.strip('#').strip().split(str(__delimiter))
        #
        if __colnames is not None:
            __usecols = []
            __colnames = tuple(__colnames)
            for v in __colnames:
                for i, n in enumerate(__varserie):
                    if v == n: __usecols.append(i)
            __usecols = tuple(__usecols)
            if len(__usecols) == 0:
                if self.__allowvoid:
                    __usecols = None
                else:
                    raise ValueError("Can not found any column corresponding to the required names %s"%(__colnames,))
        else:
            __usecols = None
        #
        if __colindex is not None:
            __useindex = None
            __colindex = str(__colindex)
            for i, n in enumerate(__varserie):
                if __colindex == n: __useindex = i
        else:
            __useindex = None
        #
        return (__usecols, __useindex)

    def getsupported(self):
        self.__supportedformats = {}
        self.__supportedformats["text/plain"]                = True
        self.__supportedformats["text/csv"]                  = True
        self.__supportedformats["text/tab-separated-values"] = True
        self.__supportedformats["application/numpy.npy"]     = True
        self.__supportedformats["application/numpy.npz"]     = True
        self.__supportedformats["application/dymola.sdf"]    = PlatformInfo.has_sdf
        return self.__supportedformats

    def getvalue(self, ColNames=None, ColIndex=None ):
        "Renvoie la ou les variables demandees par la liste de leurs noms"
        # Uniquement si mise à jour
        if ColNames is not None: self._colnames = tuple(ColNames)
        if ColIndex is not None: self._colindex = str(ColIndex)
        #
        __index = None
        if self._format == "application/numpy.npy":
            __columns = numpy.load(self._filename)
        #
        elif self._format == "application/numpy.npz":
            __columns = None
            with numpy.load(self._filename) as __allcolumns:
                if self._colnames is None:
                    self._colnames = __allcolumns.files
                for nom in self._colnames: # Si une variable demandée n'existe pas
                    if nom not in __allcolumns.files:
                        self._colnames = tuple( __allcolumns.files )
                for nom in self._colnames:
                    if nom in __allcolumns.files:
                        if __columns is not None:
                            # Attention : toutes les variables doivent avoir la même taille
                            __columns = numpy.vstack((__columns, numpy.reshape(__allcolumns[nom], (1,-1))))
                        else:
                            # Première colonne
                            __columns = numpy.reshape(__allcolumns[nom], (1,-1))
                if self._colindex is not None and self._colindex in __allcolumns.files:
                    __index = numpy.array(numpy.reshape(__allcolumns[self._colindex], (1,-1)), dtype=bytes)
        elif self._format == "text/plain":
            __usecols, __useindex = self.__getindices(self._colnames, self._colindex)
            __columns = numpy.loadtxt(self._filename, usecols = __usecols, skiprows=self._skiprows)
            if __useindex is not None:
                __index = numpy.loadtxt(self._filename, dtype = bytes, usecols = (__useindex,), skiprows=self._skiprows)
            if __usecols is None: # Si une variable demandée n'existe pas
                self._colnames = None
        #
        elif self._format == "application/dymola.sdf" and PlatformInfo.has_sdf:
            import sdf
            __content = sdf.load(self._filename)
            __columns = None
            if self._colnames is None:
                self._colnames = [__content.datasets[i].name for i in range(len(__content.datasets))]
            for nom in self._colnames:
                if nom in __content:
                    if __columns is not None:
                        # Attention : toutes les variables doivent avoir la même taille
                        __columns = numpy.vstack((__columns, numpy.reshape(__content[nom].data, (1,-1))))
                    else:
                        # Première colonne
                        __columns = numpy.reshape(__content[nom].data, (1,-1))
            if self._colindex is not None and self._colindex in __content:
                __index = __content[self._colindex].data
        #
        elif self._format == "text/csv":
            __usecols, __useindex = self.__getindices(self._colnames, self._colindex, self._delimiter)
            __columns = numpy.loadtxt(self._filename, usecols = __usecols, delimiter = self._delimiter, skiprows=self._skiprows)
            if __useindex is not None:
                __index = numpy.loadtxt(self._filename, dtype = bytes, usecols = (__useindex,), delimiter = self._delimiter, skiprows=self._skiprows)
            if __usecols is None: # Si une variable demandée n'existe pas
                self._colnames = None
        #
        elif self._format == "text/tab-separated-values":
            __usecols, __useindex = self.__getindices(self._colnames, self._colindex, self._delimiter)
            __columns = numpy.loadtxt(self._filename, usecols = __usecols, delimiter = self._delimiter, skiprows=self._skiprows)
            if __useindex is not None:
                __index = numpy.loadtxt(self._filename, dtype = bytes, usecols = (__useindex,), delimiter = self._delimiter, skiprows=self._skiprows)
            if __usecols is None: # Si une variable demandée n'existe pas
                self._colnames = None
        else:
            raise ValueError("Unkown file format \"%s\" or no reader available"%self._format)
        if __columns is None: __columns = ()
        #
        def toString(value):
            try:
                return value.decode()
            except ValueError:
                return value
        if __index is not None:
            __index = tuple([toString(v) for v in __index])
        #
        return (self._colnames, __columns, self._colindex, __index)

    def getstring(self):
        "Renvoie le fichier texte complet"
        if self._format in self.__binaryformats:
            return ""
        else:
            with open(self._filename,'r') as fid:
                return fid.read()

    def getformat(self):
        return self._format

class ImportScalarLinesFromFile(ImportFromFile):
    """
    Importation de fichier contenant des variables scalaires nommées. Le
    fichier comporte soit 2, soit 4 colonnes, obligatoirement nommées "Name",
    "Value", "Minimum", "Maximum" si les noms sont précisés. Sur chaque ligne
    est indiqué le nom, la valeur, et éventuelement deux bornes min et max (ou
    None si nécessaire pour une borne).

    Seule la méthode "getvalue" est changée.
    """
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False
    #
    def __init__(self, Filename=None, ColNames=None, ColIndex=None, Format="Guess"):
        ImportFromFile.__init__(self, Filename, ColNames, ColIndex, Format)
        if self._format not in ["text/plain", "text/csv", "text/tab-separated-values"]:
            raise ValueError("Unkown file format \"%s\""%self._format)
    #
    def getvalue(self, VarNames = None, HeaderNames=()):
        "Renvoie la ou les variables demandees par la liste de leurs noms"
        if VarNames is not None: __varnames = tuple(VarNames)
        else:                    __varnames = None
        #
        if "Name" in self._varsline and "Value" in self._varsline and "Minimum" in self._varsline and "Maximum" in self._varsline:
            __ftype = "NamValMinMax"
            __dtypes   = {'names'  : ('Name', 'Value', 'Minimum', 'Maximum'),
                          'formats': ('S128', 'g', 'g', 'g')}
            __usecols  = (0, 1, 2, 3)
            def __replaceNoneN( s ):
                if s.strip() == b'None': return numpy.NINF
                else:                    return s
            def __replaceNoneP( s ):
                if s.strip() == b'None': return numpy.PINF
                else:                    return s
            __converters = {2: __replaceNoneN, 3: __replaceNoneP}
        elif "Name" in self._varsline and "Value" in self._varsline and ("Minimum" not in self._varsline or "Maximum" not in self._varsline):
            __ftype = "NamVal"
            __dtypes   = {'names'  : ('Name', 'Value'),
                          'formats': ('S128', 'g')}
            __converters = None
            __usecols  = (0, 1)
        elif len(HeaderNames)>0 and numpy.all([kw in self._varsline for kw in HeaderNames]):
            __ftype = "NamLotOfVals"
            __dtypes   = {'names'  : HeaderNames,
                          'formats': tuple(['S128',]+['g']*(len(HeaderNames)-1))}
            __usecols  = tuple(range(len(HeaderNames)))
            def __replaceNone( s ):
                if s.strip() == b'None': return numpy.NAN
                else:                    return s
            __converters = dict()
            for i in range(1,len(HeaderNames)):
                __converters[i] = __replaceNone
        else:
            raise ValueError("Can not find names of columns for initial values. Wrong first line is:\n            \"%s\""%__firstline)
        #
        if self._format == "text/plain":
            __content = numpy.loadtxt(self._filename, dtype = __dtypes, usecols = __usecols, skiprows = self._skiprows, converters = __converters)
        elif self._format in ["text/csv", "text/tab-separated-values"]:
            __content = numpy.loadtxt(self._filename, dtype = __dtypes, usecols = __usecols, skiprows = self._skiprows, converters = __converters, delimiter = self._delimiter)
        else:
            raise ValueError("Unkown file format \"%s\""%self._format)
        #
        __names, __thevalue, __bounds = [], [], []
        for sub in __content:
            if len(__usecols) == 4:
                na, va, mi, ma = sub
                if numpy.isneginf(mi): mi = None # Réattribue les variables None
                elif numpy.isnan(mi):  mi = None # Réattribue les variables None
                if numpy.isposinf(ma): ma = None # Réattribue les variables None
                elif numpy.isnan(ma):  ma = None # Réattribue les variables None
            elif len(__usecols) == 2 and __ftype == "NamVal":
                na, va = sub
                mi, ma = None, None
            else:
                nsub = list(sub)
                na = sub[0]
                for i, v in enumerate(nsub[1:]):
                    if numpy.isnan(v): nsub[i+1] = None
                va = nsub[1:]
                mi, ma = None, None
            na = na.decode()
            if (__varnames is None or na in __varnames) and (na not in __names):
                # Ne stocke que la premiere occurence d'une variable
                __names.append(na)
                __thevalue.append(va)
                __bounds.append((mi,ma))
        #
        __names      = tuple(__names)
        __thevalue = numpy.array(__thevalue)
        __bounds     = tuple(__bounds)
        #
        return (__names, __thevalue, __bounds)

# ==============================================================================
class EficasGUI(object):
    """
    Lancement autonome de l'interface EFICAS/ADAO
    """
    def __init__(self, __addpath = None):
        # Chemin pour l'installation (ordre important)
        self.__msg = ""
        self.__path_settings_ok = False
        #----------------
        if "EFICAS_ROOT" in os.environ:
            __EFICAS_ROOT = os.environ["EFICAS_ROOT"]
            __path_ok = True
        else:
            self.__msg += "\nKeyError:\n"+\
                "  the required environment variable EFICAS_ROOT is unknown.\n"+\
                "  You have either to be in SALOME environment, or to set\n"+\
                "  this variable in your environment to the right path \"<...>\"\n"+\
                "  to find an installed EFICAS application. For example:\n"+\
                "      EFICAS_ROOT=\"<...>\" command\n"
            __path_ok = False
        try:
            import adao
            __path_ok = True and __path_ok
        except ImportError:
            self.__msg += "\nImportError:\n"+\
                "  the required ADAO library can not be found to be imported.\n"+\
                "  You have either to be in ADAO environment, or to be in SALOME\n"+\
                "  environment, or to set manually in your Python 3 environment the\n"+\
                "  right path \"<...>\" to find an installed ADAO application. For\n"+\
                "  example:\n"+\
                "      PYTHONPATH=\"<...>:${PYTHONPATH}\" command\n"
            __path_ok = False
        try:
            import PyQt5
            __path_ok = True and __path_ok
        except ImportError:
            self.__msg += "\nImportError:\n"+\
                "  the required PyQt5 library can not be found to be imported.\n"+\
                "  You have either to have a raisonable up-to-date Python 3\n"+\
                "  installation (less than 5 years), or to be in SALOME environment.\n"
            __path_ok = False
        #----------------
        if not __path_ok:
            self.__msg += "\nWarning:\n"+\
                "  It seems you have some troubles with your installation.\n"+\
                "  Be aware that some other errors may exist, that are not\n"+\
                "  explained as above, like some incomplete or obsolete\n"+\
                "  Python 3, or incomplete module installation.\n"+\
                "  \n"+\
                "  Please correct the above error(s) before launching the\n"+\
                "  standalone EFICAS/ADAO interface.\n"
            logging.debug("Some of the ADAO/EFICAS/QT5 paths have not been found")
            self.__path_settings_ok = False
        else:
            logging.debug("All the ADAO/EFICAS/QT5 paths have been found")
            self.__path_settings_ok = True
        #----------------
        if self.__path_settings_ok:
            sys.path.insert(0,__EFICAS_ROOT)
            sys.path.insert(0,os.path.join(adao.adao_py_dir,"daEficas"))
            if __addpath is not None and os.path.exists(os.path.abspath(__addpath)):
                sys.path.insert(0,os.path.abspath(__addpath))
            logging.debug("All the paths have been correctly set up")
        else:
            print(self.__msg)
            logging.debug("Errors in path settings have been found")

    def gui(self):
        if self.__path_settings_ok:
            logging.debug("Launching standalone EFICAS/ADAO interface...")
            from daEficas import prefs
            from InterfaceQT4 import eficas_go
            eficas_go.lanceEficas(code=prefs.code)
        else:
            logging.debug("Can not launch standalone EFICAS/ADAO interface for path errors.")

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
