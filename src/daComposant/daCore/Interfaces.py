# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2018 EDF R&D
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
import logging
import copy
import numpy
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
        self._addLine("import adaoBuilder")
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
                if   k == "Checked" and not __v: continue
                if   k == "Stored"  and not __v: continue
                if   k == "AvoidRC" and __v: continue
                if   k == "noDetails": continue
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

class _EPDViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas EPD (Eficas Python Dictionnary/Cas<-EPD)
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        self._observerIndex = 0
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Python script using ADAO EPD\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("#")
        self._addLine("%s = {}"%__objname)
        if self._content is not None:
            for command in self._content:
                self._append(*command)
    def _extract(self, __multilines=None, __object=None):
        "Transformation un enregistrement en une commande individuelle"
        if __multilines is not None:
            __multilines = __multilines.replace("\r\n","\n")
            exec(__multilines)
            self._objdata = None
            __getlocals = locals()
            for k in __getlocals:
                try:
                    if type(__getlocals[k]) is dict:
                        if 'ASSIMILATION_STUDY' in __getlocals[k]:
                            self._objname = k
                            self._objdata = __getlocals[k]['ASSIMILATION_STUDY']
                        if 'CHECKING_STUDY' in __getlocals[k]:
                            self._objname = k
                            self._objdata = __getlocals[k]['CHECKING_STUDY']
                except:
                    continue
        elif __multilines is None and __object is not None and type(__object) is dict:
            self._objname = "case"
            self._objdata = None
            if 'ASSIMILATION_STUDY' in __object:
                self._objdata = __object['ASSIMILATION_STUDY']
            if 'CHECKING_STUDY' in __object:
                self._objdata = __object['CHECKING_STUDY']
        else:
            self._objdata = None
        #
        if self._objdata is None or not(type(self._objdata) is dict) or not('AlgorithmParameters' in self._objdata):
            raise ValueError("Impossible to load given content as an ADAO EPD one (no dictionnary or no 'AlgorithmParameters' key found).")
        # ----------------------------------------------------------------------
        logging.debug("EPD Extracting commands of '%s' object..."%(self._objname,))
        __commands = []
        __UserPostAnalysis = ""
        for k,r in self._objdata.items():
            __command = k
            logging.debug("EPD Extracted command: %s:%s"%(k, r))
            if   __command == "StudyName" and len(str(r))>0:
                __commands.append( "set( Concept='Name', String='%s')"%(str(r),) )
            elif   __command == "StudyRepertory":
                __commands.append( "set( Concept='Directory', String='%s')"%(str(r),) )
            #
            elif __command == "UserPostAnalysis" and type(r) is dict:
                if 'STRING_DATA' in r:
                    __UserPostAnalysis = r['STRING_DATA']['STRING']
                elif 'SCRIPT_DATA' in r and os.path.exists(r['SCRIPT_DATA']['SCRIPT_FILE']):
                    __UserPostAnalysis = open(r['SCRIPT_DATA']['SCRIPT_FILE'],'r').read()
                elif 'TEMPLATE_DATA' in r:
                    # AnalysisPrinter...
                    __itempl = r['TEMPLATE_DATA']['Template']
                    __UserPostAnalysis = r['TEMPLATE_DATA'][__itempl]['ValueTemplate']
                else:
                    __UserPostAnalysis = ""
                __UserPostAnalysis = __UserPostAnalysis.replace("ADD",self._objname)
            #
            elif __command == "AlgorithmParameters" and type(r) is dict and 'Algorithm' in r:
                if 'Parameters%s'%(r['Algorithm'],) in r and r['Parameters'] == 'Defaults':
                    __Dict = r['Parameters%s'%(r['Algorithm'],)]
                    if 'SetSeed' in __Dict:__Dict['SetSeed'] = int(__Dict['SetSeed'])
                    if 'BoxBounds' in __Dict and type(__Dict['BoxBounds']) is str:
                        __Dict['BoxBounds'] = eval(__Dict['BoxBounds'])
                    __parameters = ', Parameters=%s'%(repr(__Dict),)
                elif 'Dict' in r and r['Parameters'] == 'Dict':
                    __from = r['Dict']['data']
                    if 'STRING_DATA' in __from:
                        __parameters = ", Parameters=%s"%(repr(eval(__from['STRING_DATA']['STRING'])),)
                    elif 'SCRIPT_DATA' in __from and os.path.exists(__from['SCRIPT_DATA']['SCRIPT_FILE']):
                        __parameters = ", Script='%s'"%(__from['SCRIPT_DATA']['SCRIPT_FILE'],)
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
                    __idata = r[sk]['%s_data'%sk]
                    if __idata['NodeType'] == 'Template' and 'Template' in __idata['ObserverTemplate']:
                        __template =__idata['ObserverTemplate']['Template']
                        __commands.append( "set( Concept='Observer', Variable='%s', Template='%s' )"%(sk,__template) )
                    if __idata['NodeType'] == 'String' and 'Value' in __idata:
                        __value =__idata['Value']
                        __commands.append( "set( Concept='Observer', Variable='%s', String='%s' )"%(sk,__value) )
            #
            # Background, ObservationError, ObservationOperator...
            elif type(r) is dict:
                __argumentsList = []
                if 'Stored' in r and bool(r['Stored']):
                    __argumentsList.append(['Stored',True])
                if 'INPUT_TYPE' in r and r['INPUT_TYPE'] in r:
                    # Vector, Matrix, ScalarSparseMatrix, DiagonalSparseMatrix, Function
                    __itype = r['INPUT_TYPE']
                    __idata = r[__itype]['data']
                    if 'FROM' in __idata and __idata['FROM'].upper()+'_DATA' in __idata:
                        # String, Script, Template, ScriptWithOneFunction, ScriptWithFunctions
                        __ifrom = __idata['FROM']
                        if __ifrom == 'String' or __ifrom == 'Template':
                            __argumentsList.append([__itype,__idata['STRING_DATA']['STRING']])
                        if __ifrom == 'Script':
                            __argumentsList.append([__itype,True])
                            __argumentsList.append(['Script',__idata['SCRIPT_DATA']['SCRIPT_FILE']])
                        if __ifrom == 'ScriptWithOneFunction':
                            __argumentsList.append(['OneFunction',True])
                            __argumentsList.append(['Script',__idata['SCRIPTWITHONEFUNCTION_DATA'].pop('SCRIPTWITHONEFUNCTION_FILE')])
                            if len(__idata['SCRIPTWITHONEFUNCTION_DATA'])>0:
                                __argumentsList.append(['Parameters',__idata['SCRIPTWITHONEFUNCTION_DATA']])
                        if __ifrom == 'ScriptWithFunctions':
                            __argumentsList.append(['ThreeFunctions',True])
                            __argumentsList.append(['Script',__idata['SCRIPTWITHFUNCTIONS_DATA'].pop('SCRIPTWITHFUNCTIONS_FILE')])
                            if len(__idata['SCRIPTWITHFUNCTIONS_DATA'])>0:
                                __argumentsList.append(['Parameters',__idata['SCRIPTWITHFUNCTIONS_DATA']])
                __arguments = ["%s = %s"%(k,repr(v)) for k,v in __argumentsList]
                __commands.append( "set( Concept='%s', %s )"%(__command, ", ".join(__arguments)))
        #
        # ----------------------------------------------------------------------
        __commands.sort() # Pour commencer par 'AlgorithmParameters'
        __commands.append(__UserPostAnalysis)
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
                if 'Parameters' in r and r['Parameters'] == 'Defaults':
                    __Dict = copy.deepcopy(r)
                    __Dict.pop('Algorithm')
                    if 'SetSeed' in __Dict:__Dict['SetSeed'] = int(__Dict['SetSeed'])
                    if 'BoxBounds' in __Dict and type(__Dict['BoxBounds']) is str:
                        __Dict['BoxBounds'] = eval(__Dict['BoxBounds'])
                    __parameters = ', Parameters=%s'%(repr(__Dict),)
                elif 'data' in r and r['Parameters'] == 'Dict':
                    __from = r['data']
                    if 'STRING' in __from:
                        __parameters = ", Parameters=%s"%(repr(eval(__from['STRING'])),)
                    elif 'SCRIPT_FILE' in __from and os.path.exists(__from['SCRIPT_FILE']):
                        __parameters = ", Script='%s'"%(__from['SCRIPT_FILE'],)
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
                        # String, Script, Template, ScriptWithOneFunction, ScriptWithFunctions
                        __ifrom = __idata['FROM']
                        if __ifrom == 'String' or __ifrom == 'Template':
                            __argumentsList.append([__itype,__idata['STRING']])
                        if __ifrom == 'Script':
                            __argumentsList.append([__itype,True])
                            __argumentsList.append(['Script',__idata['SCRIPT_FILE']])
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

class _DCTViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas DCT (Cas<->DCT)
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        self._observerIndex = 0
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Python script using ADAO DCT\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("#")
        self._addLine("%s = {}"%__objname)
        if self._content is not None:
            for command in self._content:
                self._append(*command)
    def _append(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Transformation d'une commande individuelle en un enregistrement"
        if __command is not None and __keys is not None and __local is not None:
            __text  = ""
            if "execute" in __command: return
            if "self" in __keys: __keys.remove("self")
            if __command in ("set","get") and "Concept" in __keys:
                __key = __local["Concept"]
                __keys.remove("Concept")
            else:
                __key = __command.replace("set","").replace("get","")
            if "Observer" in __key and 'Variable' in __keys:
                self._observerIndex += 1
                __key += "_%i"%self._observerIndex
            __text += "%s['%s'] = {"%(self._objname,str(__key))
            for k in __keys:
                __v = __local[k]
                if __v is None: continue
                if   k == "Checked" and not __v: continue
                if   k == "Stored"  and not __v: continue
                if   k == "AvoidRC" and __v: continue
                if   k == "noDetails": continue
                if isinstance(__v,Persistence.Persistence): __v = __v.values()
                if callable(__v): __text = self._missing%__v.__name__+__text
                if isinstance(__v,dict):
                    for val in __v.values():
                        if callable(val): __text = self._missing%val.__name__+__text
                numpy.set_printoptions(precision=15,threshold=1000000,linewidth=1000*15)
                __text += "'%s':%s, "%(k,repr(__v))
                numpy.set_printoptions(precision=8,threshold=1000,linewidth=75)
            __text.rstrip(", ").rstrip()
            __text += "}"
            if __text[-2:] == "{}": return # Supprime les *Debug et les variables
            self._addLine(__text)
    def _extract(self, __multilines="", __object=None):
        "Transformation un enregistrement en une commande individuelle"
        __multilines = __multilines.replace("\r\n","\n")
        exec(__multilines)
        self._objdata = None
        __getlocals = locals()
        for k in __getlocals:
            try:
                if 'AlgorithmParameters' in __getlocals[k] and type(__getlocals[k]) is dict:
                    self._objname = k
                    self._objdata = __getlocals[k]
            except:
                continue
        if self._objdata is None:
            raise ValueError("Impossible to load given content as an ADAO DCT one (no 'AlgorithmParameters' key found).")
        # ----------------------------------------------------------------------
        logging.debug("DCT Extracting commands of '%s' object..."%(self._objname,))
        __commands = []
        for k in self._objdata:
            if 'Observer_' in k:
                __command = k.split('_',1)[0]
            else:
                __command = k
            __arguments = ["%s = %s"%(k,repr(v)) for k,v in self._objdata[k].items()]
            __commands.append( "set( Concept='%s', %s )"%(__command, ", ".join(__arguments)))
        __commands.sort() # Pour commencer par 'AlgorithmParameters'
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
            if 'self' in __local: __local.pop('self')
            __to_be_removed = []
            for __k,__v in __local.items():
                if __v is None: __to_be_removed.append(__k)
            for __k in __to_be_removed:
                __local.pop(__k)
            for __k,__v in __local.items():
                if __k == "Concept": continue
                if __k in ['ScalarSparseMatrix','DiagonalSparseMatrix','Matrix','OneFunction','ThreeFunctions'] and 'Script' in __local: continue
                if __k == 'Algorithm':
                    __text += "study_config['Algorithm'] = %s\n"%(repr(__v))
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
                elif __k in ('Stored', 'Checked'):
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
        self._addLine("print 'Analysis:',xa\"\"\"")
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

class _XMLViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas XML
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        raise NotImplementedError()

class _YACSViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas YACS (Cas->SCD->YACS)
    """
    def __init__(self, __name="", __objname="case", __content=None, __object=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content, __object)
        self.__internalSCD = _SCDViewer(__name, __objname, __content, __object)
        self._append       = self.__internalSCD._append
    def dump(self, __filename=None, __convertSCDinMemory=True):
        "Restitution normalisée des commandes"
        self.__internalSCD._finalize()
        # -----
        if __filename is None:
            raise ValueError("A file name has to be given for YACS XML output.")
        # -----
        if not PlatformInfo.has_salome or \
            not PlatformInfo.has_adao:
            raise ImportError(
                "Unable to get SALOME or ADAO environnement variables for YACS conversion.\n"+\
                "Please load the right environnement before trying to use it.")
        elif __convertSCDinMemory:
            __file    = os.path.abspath(__filename)
            __SCDdump = self.__internalSCD.dump()
            if os.path.isfile(__file) or os.path.islink(__file):
                os.remove(__file)
            from daYacsSchemaCreator.run import create_schema_from_content
            create_schema_from_content(__SCDdump, __file)
        else:
            __file    = os.path.abspath(__filename)
            __SCDfile = __file[:__file.rfind(".")] + '_SCD.py'
            __SCDdump = self.__internalSCD.dump(__SCDfile)
            if os.path.isfile(__file) or os.path.islink(__file):
                os.remove(__file)
            __converterExe = os.path.join(os.environ["ADAO_ROOT_DIR"], "bin/salome", "AdaoYacsSchemaCreator.py")
            __args = ["python", __converterExe, __SCDfile, __file]
            import subprocess
            __p = subprocess.Popen(__args)
            (__stdoutdata, __stderrdata) = __p.communicate()
            __p.terminate()
            os.remove(__SCDfile)
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

class ImportFromScript(object):
    """
    Obtention d'une variable nommee depuis un fichier script importe
    """
    def __init__(self, __filename=None):
        "Verifie l'existence et importe le script"
        if __filename is None:
            raise ValueError("The name of the file, containing the variable to be read, has to be specified.")
        if not os.path.isfile(__filename):
            raise ValueError("The file containing the variable to be imported doesn't seem to exist. Please check the file. The given file name is:\n  \"%s\""%__filename)
        if os.path.dirname(__filename) != '':
            sys.path.insert(0, os.path.dirname(__filename))
            __basename = os.path.basename(__filename).rstrip(".py")
        else:
            __basename = __filename.rstrip(".py")
        self.__basename = __basename
        self.__scriptfile = __import__(__basename, globals(), locals(), [])
        self.__scriptstring = open(__filename,'r').read()
    def getvalue(self, __varname=None, __synonym=None ):
        "Renvoie la variable demandee"
        if __varname is None:
            raise ValueError("The name of the variable to be read has to be specified. Please check the content of the file and the syntax.")
        if not hasattr(self.__scriptfile, __varname):
            if __synonym is None:
                raise ValueError("The imported script file \"%s\" doesn't contain the mandatory variable \"%s\" to be read. Please check the content of the file and the syntax."%(str(self.__basename)+".py",__varname))
            elif not hasattr(self.__scriptfile, __synonym):
                raise ValueError("The imported script file \"%s\" doesn't contain the mandatory variable \"%s\" to be read. Please check the content of the file and the syntax."%(str(self.__basename)+".py",__synonym))
            else:
                return getattr(self.__scriptfile, __synonym)
        else:
            return getattr(self.__scriptfile, __varname)
    def getstring(self):
        "Renvoie le script complet"
        return self.__scriptstring

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')
