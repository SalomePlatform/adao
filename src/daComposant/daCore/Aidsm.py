# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2017 EDF R&D
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
    Normalized interface for ADAO scripting (generic API)
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["Aidsm"]

import os, sys
from daCore import ExtendedLogging ; ExtendedLogging.ExtendedLogging() # A importer en premier
import logging
import numpy
#
from daCore.BasicObjects import State, Covariance, FullOperator, Operator
from daCore.BasicObjects import AlgorithmAndParameters, DataObserver
from daCore.BasicObjects import DiagnosticAndParameters, ImportFromScript
from daCore.BasicObjects import CaseLogger, GenericCaseViewer
from daCore.Templates    import ObserverTemplates
from daCore import Persistence
from daCore import PlatformInfo

# ==============================================================================
class DICViewer(GenericCaseViewer):
    """
    Etablissement des commandes de creation d'un cas DIC
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content)
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
        if __command in (None, 'execute', 'executePythonScheme', 'executeYACSScheme', 'get'):
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
            if __local['Template'] is not None:
                __text += "observers['%s']['nodetype'] = '%s'\n"%(__obs, 'String')
                __text += "observers['%s']['String'] = \"\"\"%s\"\"\"\n"%(__obs, ObserverTemplates[__local['Template']])
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
                    if __k is 'Parameters': __k = "Dict"
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
    def _finalize(self):
        self.__loadVariablesByScript()
        self._addLine("#")
        self._addLine("Analysis_config = {}")
        self._addLine("Analysis_config['From'] = 'String'")
        self._addLine("Analysis_config['Data'] = \"\"\"import numpy")
        self._addLine("xa=numpy.ravel(ADD.get('Analysis')[-1])")
        self._addLine("print 'Analysis:',xa\"\"\"")
        self._addLine("study_config['UserPostAnalysis'] = Analysis_config")
    def __loadVariablesByScript(self):
        exec("\n".join(self._lineSerie))
        if "Algorithm" in study_config and len(study_config['Algorithm'])>0:
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

class XMLViewer(GenericCaseViewer):
    """
    Etablissement des commandes de creation d'un cas XML
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content)
        raise NotImplementedError()

# ==============================================================================
class Aidsm(object):
    """ ADAO Internal Data Structure Model """
    def __init__(self, name = "", addViewers={"DIC":DICViewer}):
        self.__name = str(name)
        self.__case = CaseLogger(self.__name, "case", addViewers)
        #
        self.__adaoObject   = {}
        self.__StoredInputs = {}
        #
        self.__Concepts = [
            "AlgorithmParameters",
            "Background",
            "CheckingPoint",
            "ControlInput",
            "Observation",
            "Controls",
            "BackgroundError",
            "ObservationError",
            "EvolutionError",
            "ObservationOperator",
            "EvolutionModel",
            "ControlModel",
            "Debug",
            "NoDebug",
            "Observer",
            ]
        #
        for ename in self.__Concepts:
            self.__adaoObject[ename] = None
        for ename in ("ObservationOperator", "EvolutionModel", "ControlModel"):
            self.__adaoObject[ename] = {}
        for ename in ("Diagnostic", "Observer"):
            self.__adaoObject[ename]   = []
            self.__StoredInputs[ename] = []
        #
        # Récupère le chemin du répertoire parent et l'ajoute au path
        # (Cela complète l'action de la classe PathManagement dans PlatformInfo,
        # qui est activée dans Persistence)
        self.__parent = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        sys.path.insert(0, self.__parent)
        sys.path = PlatformInfo.uniq( sys.path ) # Conserve en unique exemplaire chaque chemin

    def set(self,
            Concept              = None, # Premier argument
            Algorithm            = None,
            AppliedInXb          = None,
            AvoidRC              = True,
            BaseType             = None,
            Checked              = False,
            Diagnostic           = None,
            DiagonalSparseMatrix = None,
            Identifier           = None,
            Info                 = None,
            Matrix               = None,
            ObjectFunction       = None,
            ObjectMatrix         = None,
            OneFunction          = None,
            Parameters           = None,
            ScalarSparseMatrix   = None,
            Scheduler            = None,
            Script               = None,
            Stored               = False,
            String               = None,
            Template             = None,
            ThreeFunctions       = None,
            Unit                 = None,
            Variable             = None,
            Vector               = None,
            VectorSerie          = None,
            ):
        "Interface unique de definition de variables d'entrees par argument"
        self.__case.register("set",dir(),locals(),None,True)
        try:
            if   Concept in ("Background", "CheckingPoint", "ControlInput", "Observation", "Controls"):
                commande = getattr(self,"set"+Concept)
                commande(Vector, VectorSerie, Script, Scheduler, Stored, Checked )
            elif Concept in ("BackgroundError", "ObservationError", "EvolutionError"):
                commande = getattr(self,"set"+Concept)
                commande(Matrix, ScalarSparseMatrix, DiagonalSparseMatrix,
                         ObjectMatrix, Script, Stored, Checked )
            elif Concept == "AlgorithmParameters":
                self.setAlgorithmParameters( Algorithm, Parameters, Script )
            elif Concept == "Debug":
                self.setDebug()
            elif Concept == "NoDebug":
                self.setNoDebug()
            elif Concept == "Observer":
                self.setObserver( Variable, Template, String, Script, ObjectFunction, Scheduler, Info )
            elif Concept == "Diagnostic":
                self.setDiagnostic( Diagnostic, Identifier, Parameters, Script, Unit, BaseType )
            elif Concept == "ObservationOperator":
                self.setObservationOperator(
                    Matrix, OneFunction, ThreeFunctions, AppliedInXb,
                    Parameters, Script, AvoidRC, Stored, Checked )
            elif Concept in ("EvolutionModel", "ControlModel"):
                commande = getattr(self,"set"+Concept)
                commande(
                    Matrix, OneFunction, ThreeFunctions,
                    Parameters, Script, Scheduler, AvoidRC, Stored, Checked )

            else:
                raise ValueError("the variable named '%s' is not allowed."%str(Concept))
        except Exception as e:
            if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError("during settings, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal."%(str(e),msg))

    # -----------------------------------------------------------

    def setBackground(self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Scheduler      = None,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "Background"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = Script,
            scheduledBy        = Scheduler,
            toBeChecked        = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setCheckingPoint(self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Scheduler      = None,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "CheckingPoint"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = Script,
            scheduledBy        = Scheduler,
            toBeChecked        = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setControlInput(self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Scheduler      = None,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "ControlInput"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = Script,
            scheduledBy        = Scheduler,
            toBeChecked        = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setObservation(self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Scheduler      = None,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "Observation"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = Script,
            scheduledBy        = Scheduler,
            toBeChecked        = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setControls(self,
            Vector         = (), # Valeur par defaut pour un vecteur vide
            VectorSerie    = None,
            Script         = None,
            Scheduler      = None,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "Controls"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = Script,
            scheduledBy        = Scheduler,
            toBeChecked        = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setBackgroundError(self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            ObjectMatrix         = None,
            Script               = None,
            Stored               = False,
            Checked              = False):
        "Definition d'un concept de calcul"
        Concept = "BackgroundError"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = Covariance(
            name          = Concept,
            asCovariance  = Matrix,
            asEyeByScalar = ScalarSparseMatrix,
            asEyeByVector = DiagonalSparseMatrix,
            asCovObject   = ObjectMatrix,
            asScript      = Script,
            toBeChecked   = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setObservationError(self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            ObjectMatrix         = None,
            Script               = None,
            Stored               = False,
            Checked              = False):
        "Definition d'un concept de calcul"
        Concept = "ObservationError"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = Covariance(
            name          = Concept,
            asCovariance  = Matrix,
            asEyeByScalar = ScalarSparseMatrix,
            asEyeByVector = DiagonalSparseMatrix,
            asCovObject   = ObjectMatrix,
            asScript      = Script,
            toBeChecked   = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setEvolutionError(self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            ObjectMatrix         = None,
            Script               = None,
            Stored               = False,
            Checked              = False):
        "Definition d'un concept de calcul"
        Concept = "EvolutionError"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = Covariance(
            name          = Concept,
            asCovariance  = Matrix,
            asEyeByScalar = ScalarSparseMatrix,
            asEyeByVector = DiagonalSparseMatrix,
            asCovObject   = ObjectMatrix,
            asScript      = Script,
            toBeChecked   = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setObservationOperator(self,
            Matrix         = None,
            OneFunction    = None,
            ThreeFunctions = None,
            AppliedInXb    = None,
            Parameters     = None,
            Script         = None,
            AvoidRC        = True,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "ObservationOperator"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = FullOperator(
            name             = Concept,
            asMatrix         = Matrix,
            asOneFunction    = OneFunction,
            asThreeFunctions = ThreeFunctions,
            asScript         = Script,
            asDict           = Parameters,
            appliedInX       = AppliedInXb,
            avoidRC          = AvoidRC,
            scheduledBy      = None,
            toBeChecked      = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setEvolutionModel(self,
            Matrix         = None,
            OneFunction    = None,
            ThreeFunctions = None,
            Parameters     = None,
            Script         = None,
            Scheduler      = None,
            AvoidRC        = True,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "EvolutionModel"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = FullOperator(
            name             = Concept,
            asMatrix         = Matrix,
            asOneFunction    = OneFunction,
            asThreeFunctions = ThreeFunctions,
            asScript         = Script,
            asDict           = Parameters,
            appliedInX       = None,
            avoidRC          = AvoidRC,
            scheduledBy      = Scheduler,
            toBeChecked      = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setControlModel(self,
            Matrix         = None,
            OneFunction    = None,
            ThreeFunctions = None,
            Parameters     = None,
            Script         = None,
            Scheduler      = None,
            AvoidRC        = True,
            Stored         = False,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "ControlModel"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = FullOperator(
            name             = Concept,
            asMatrix         = Matrix,
            asOneFunction    = OneFunction,
            asThreeFunctions = ThreeFunctions,
            asScript         = Script,
            asDict           = Parameters,
            appliedInX       = None,
            avoidRC          = AvoidRC,
            scheduledBy      = Scheduler,
            toBeChecked      = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setDebug(self, level = 10):
        "NOTSET=0 < DEBUG=10 < INFO=20 < WARNING=30 < ERROR=40 < CRITICAL=50"
        self.__case.register("setDebug",dir(),locals())
        log = logging.getLogger()
        log.setLevel( level )
        self.__StoredInputs["Debug"]   = level
        self.__StoredInputs["NoDebug"] = False
        return 0

    def setNoDebug(self):
        "NOTSET=0 < DEBUG=10 < INFO=20 < WARNING=30 < ERROR=40 < CRITICAL=50"
        self.__case.register("setNoDebug",dir(),locals())
        log = logging.getLogger()
        log.setLevel( logging.WARNING )
        self.__StoredInputs["Debug"]   = logging.WARNING
        self.__StoredInputs["NoDebug"] = True
        return 0

    def setAlgorithmParameters(self,
            Algorithm  = None,
            Parameters = None,
            Script     = None):
        "Definition d'un concept de calcul"
        Concept = "AlgorithmParameters"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = AlgorithmAndParameters(
            name          = Concept,
            asAlgorithm   = Algorithm,
            asDict        = Parameters,
            asScript      = Script,
            )
        return 0

    def updateAlgorithmParameters(self,
            Parameters = None,
            Script     = None):
        "Mise a jour d'un concept de calcul"
        if "AlgorithmParameters" not in self.__adaoObject:
            raise ValueError("No algorithm registred, ask for one before updating parameters")
        self.__adaoObject["AlgorithmParameters"].updateParameters(
            asDict        = Parameters,
            asScript      = Script,
            )
        return 0

    def setObserver(self,
            Variable       = None,
            Template       = None,
            String         = None,
            Script         = None,
            ObjectFunction = None,
            Scheduler      = None,
            Info           = None):
        "Definition d'un concept de calcul"
        Concept = "Observer"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept].append( DataObserver(
            name        = Concept,
            onVariable  = Variable,
            asTemplate  = Template,
            asString    = String,
            asScript    = Script,
            asObsObject = ObjectFunction,
            withInfo    = Info,
            scheduledBy = Scheduler,
            withAlgo    = self.__adaoObject["AlgorithmParameters"]
            ))
        return 0

    def removeObserver(self,
            Variable       = None,
            ObjectFunction = None,
            ):
        """
        Permet de retirer un observer à une ou des variable nommée.
        """
        if "AlgorithmParameters" not in self.__adaoObject:
            raise ValueError("No algorithm registred, ask for one before removing observers")
        #
        # Vérification du nom de variable et typage
        # -----------------------------------------
        if isinstance(Variable, str):
            VariableNames = (Variable,)
        elif isinstance(Variable, list):
            VariableNames = tuple(map( str, Variable ))
        else:
            raise ValueError("The observer requires a name or a list of names of variables.")
        #
        # Association interne de l'observer à la variable
        # -----------------------------------------------
        for ename in VariableNames:
            if ename not in self.__adaoObject["AlgorithmParameters"]:
                raise ValueError("An observer requires to be removed on a variable named %s which does not exist."%ename)
            else:
                return self.__adaoObject["AlgorithmParameters"].removeObserver( ename, ObjectFunction )

    # -----------------------------------------------------------

    def setDiagnostic(self,
            Diagnostic = None,
            Identifier = None,
            Parameters = None,
            Script     = None,
            Unit       = None,
            BaseType   = None):
        "Definition d'un concept de calcul"
        Concept = "Diagnostic"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept].append( DiagnosticAndParameters(
                 name               = Concept,
                 asDiagnostic       = Diagnostic,
                 asIdentifier       = Identifier,
                 asDict             = Parameters,
                 asScript           = Script,
                 asUnit             = Unit,
                 asBaseType         = BaseType,
                 asExistingDiags    = self.__StoredInputs[Concept],
                ))
        self.__StoredInputs[Concept].append(str(Identifier))
        return 0

    def get(self, Concept=None, noDetails=True ):
        "Recuperation d'une sortie du calcul"
        """
        Permet d'accéder aux informations stockées, diagnostics et résultats
        disponibles après l'exécution du calcul. Attention, quand un diagnostic
        porte le même nom qu'une variable stockée (paramètre ou résultat),
        c'est la variable stockée qui est renvoyée, et le diagnostic est
        inatteignable.
        """
        if Concept is not None:
            try:
                self.__case.register("get", dir(), locals(), Concept) # Break pickle in Python 2
            except:
                pass
            if Concept in self.__StoredInputs:
                return self.__StoredInputs[Concept]
                #
            elif self.__adaoObject["AlgorithmParameters"] is not None and Concept == "AlgorithmParameters":
                return self.__adaoObject["AlgorithmParameters"].get()
                #
            elif self.__adaoObject["AlgorithmParameters"] is not None and Concept in self.__adaoObject["AlgorithmParameters"]:
                return self.__adaoObject["AlgorithmParameters"].get( Concept )
                #
            elif Concept == "AlgorithmRequiredParameters" and self.__adaoObject["AlgorithmParameters"] is not None:
                return self.__adaoObject["AlgorithmParameters"].getAlgorithmRequiredParameters(noDetails)
                #
            elif Concept in self.__StoredInputs["Diagnostic"]:
                indice = self.__StoredInputs["Diagnostic"].index(Concept)
                return self.__adaoObject["Diagnostic"][indice].get()
                #
            else:
                raise ValueError("The requested key \"%s\" does not exists as an input, a diagnostic or a stored variable."%Concept)
        else:
            allvariables = {}
            allvariables.update( {"AlgorithmParameters":self.__adaoObject["AlgorithmParameters"].get()} )
            allvariables.update( self.__adaoObject["AlgorithmParameters"].get() )
            allvariables.update( self.__StoredInputs )
            allvariables.pop('Diagnostic', None)
            allvariables.pop('Observer', None)
            return allvariables

    # -----------------------------------------------------------

    def get_available_variables(self):
        """
        Renvoie les variables potentiellement utilisables pour l'étude,
        initialement stockées comme données d'entrées ou dans les algorithmes,
        identifiés par les chaînes de caractères. L'algorithme doit avoir été
        préalablement choisi sinon la méthode renvoie "None".
        """
        if len(list(self.__adaoObject["AlgorithmParameters"].keys())) == 0 and \
            len(list(self.__StoredInputs.keys())) == 0:
            return None
        else:
            variables = []
            if len(list(self.__adaoObject["AlgorithmParameters"].keys())) > 0:
                variables.extend(list(self.__adaoObject["AlgorithmParameters"].keys()))
            if len(list(self.__StoredInputs.keys())) > 0:
                variables.extend( list(self.__StoredInputs.keys()) )
            variables.remove('Diagnostic')
            variables.remove('Observer')
            variables.sort()
            return variables

    def get_available_algorithms(self):
        """
        Renvoie la liste des algorithmes potentiellement utilisables, identifiés
        par les chaînes de caractères.
        """
        files = []
        for directory in sys.path:
            if os.path.isdir(os.path.join(directory,"daAlgorithms")):
                for fname in os.listdir(os.path.join(directory,"daAlgorithms")):
                    root, ext = os.path.splitext(fname)
                    if ext == '.py' and root != '__init__':
                        files.append(root)
        files.sort()
        return files

    def get_available_diagnostics(self):
        """
        Renvoie la liste des diagnostics potentiellement utilisables, identifiés
        par les chaînes de caractères.
        """
        files = []
        for directory in sys.path:
            if os.path.isdir(os.path.join(directory,"daDiagnostics")):
                for fname in os.listdir(os.path.join(directory,"daDiagnostics")):
                    root, ext = os.path.splitext(fname)
                    if ext == '.py' and root != '__init__':
                        files.append(root)
        files.sort()
        return files

    # -----------------------------------------------------------

    def get_algorithms_main_path(self):
        """
        Renvoie le chemin pour le répertoire principal contenant les algorithmes
        dans un sous-répertoire "daAlgorithms"
        """
        return self.__parent

    def add_algorithms_path(self, Path=None):
        """
        Ajoute au chemin de recherche des algorithmes un répertoire dans lequel
        se trouve un sous-répertoire "daAlgorithms"

        Remarque : si le chemin a déjà été ajouté pour les diagnostics, il n'est
        pas indispensable de le rajouter ici.
        """
        if not os.path.isdir(Path):
            raise ValueError("The given "+Path+" argument must exist as a directory")
        if not os.path.isdir(os.path.join(Path,"daAlgorithms")):
            raise ValueError("The given \""+Path+"\" argument must contain a subdirectory named \"daAlgorithms\"")
        if not os.path.isfile(os.path.join(Path,"daAlgorithms","__init__.py")):
            raise ValueError("The given \""+Path+"/daAlgorithms\" path must contain a file named \"__init__.py\"")
        sys.path.insert(0, os.path.abspath(Path))
        sys.path = PlatformInfo.uniq( sys.path ) # Conserve en unique exemplaire chaque chemin
        return 0

    def get_diagnostics_main_path(self):
        """
        Renvoie le chemin pour le répertoire principal contenant les diagnostics
        dans un sous-répertoire "daDiagnostics"
        """
        return self.__parent

    def add_diagnostics_path(self, Path=None):
        """
        Ajoute au chemin de recherche des algorithmes un répertoire dans lequel
        se trouve un sous-répertoire "daDiagnostics"

        Remarque : si le chemin a déjà été ajouté pour les algorithmes, il n'est
        pas indispensable de le rajouter ici.
        """
        if not os.path.isdir(Path):
            raise ValueError("The given "+Path+" argument must exist as a directory")
        if not os.path.isdir(os.path.join(Path,"daDiagnostics")):
            raise ValueError("The given \""+Path+"\" argument must contain a subdirectory named \"daDiagnostics\"")
        if not os.path.isfile(os.path.join(Path,"daDiagnostics","__init__.py")):
            raise ValueError("The given \""+Path+"/daDiagnostics\" path must contain a file named \"__init__.py\"")
        sys.path.insert(0, os.path.abspath(Path))
        sys.path = PlatformInfo.uniq( sys.path ) # Conserve en unique exemplaire chaque chemin
        return 0

    # -----------------------------------------------------------

    def execute(self, Executor=None, SaveCaseInFile=None):
        "Lancement du calcul"
        self.__case.register("execute",dir(),locals(),None,True)
        Operator.CM.clearCache()
        #~ try:
        if   Executor == "YACS": self.__executeYACSScheme( SaveCaseInFile )
        else:                    self.__executePythonScheme( SaveCaseInFile )
        #~ except Exception as e:
            #~ if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
            #~ else: msg = ""
            #~ raise ValueError("during execution, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal.\n"%(str(e),msg))
        return 0

    def __executePythonScheme(self, FileName=None):
        "Lancement du calcul"
        self.__case.register("executePythonScheme", dir(), locals())
        if FileName is not None:
            self.dump( FileName, "TUI")
        self.__adaoObject["AlgorithmParameters"].executePythonScheme( self.__adaoObject )
        return 0

    def __executeYACSScheme(self, FileName=None):
        "Lancement du calcul"
        self.__case.register("executeYACSScheme", dir(), locals())
        if FileName is not None:
            self.dump( FileName, "DIC")
        self.__adaoObject["AlgorithmParameters"].executeYACSScheme( FileName )
        return 0

    # -----------------------------------------------------------

    def dump(self, FileName=None, Formater="TUI"):
        "Restitution normalisée des commandes"
        return self.__case.dump(FileName, Formater)

    def load(self, FileName=None, Formater="TUI"):
        "Chargement normalisé des commandes"
        __commands = self.__case.load(FileName, Formater)
        from numpy import array, matrix
        for __command in __commands:
            exec("self."+__command)
        return 0

    def clear(self):
        "Effacement du contenu du cas en cours"
        self.__init__(self.__name)

    # -----------------------------------------------------------

    def __dir__(self):
        "Clarifie la visibilité des méthodes"
        return ['set', 'get', 'execute', '__doc__', '__init__', '__module__']

    def prepare_to_pickle(self):
        "Retire les variables non pickelisables, avec recopie efficace"
        if self.__adaoObject['AlgorithmParameters'] is not None:
            for k in self.__adaoObject['AlgorithmParameters'].keys():
                if k == "Algorithm": continue
                if k in self.__StoredInputs:
                    raise ValueError("the key \"%s\s to be transfered for pickling will overwrite an existing one.")
                if self.__adaoObject['AlgorithmParameters'].hasObserver( k ):
                    self.__adaoObject['AlgorithmParameters'].removeObserver( k, "", True )
                self.__StoredInputs[k] = self.__adaoObject['AlgorithmParameters'].pop(k, None)
        del self.__adaoObject # Because it breaks pickle in Python 2
        del self.__case       # Because it breaks pickle in Python 2
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')
