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
    Normalized interface for ADAO scripting (generic API)
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["Aidsm"]

import os
import sys
#
from daCore.BasicObjects import State, Covariance, FullOperator, Operator
from daCore.BasicObjects import AlgorithmAndParameters, DataObserver
from daCore.BasicObjects import RegulationAndParameters, CaseLogger
from daCore import PlatformInfo
#
from daCore import ExtendedLogging ; ExtendedLogging.ExtendedLogging() # A importer en premier
import logging

# ==============================================================================
class Aidsm(object):
    """ ADAO Internal Data Structure Model """
    def __init__(self, name = "", addViewers=None):
        self.__name = str(name)
        self.__directory    = None
        self.__case = CaseLogger(self.__name, "case", addViewers)
        #
        self.__adaoObject   = {}
        self.__StoredInputs = {}
        self.__PostAnalysis = []
        #
        self.__Concepts = [
            "AlgorithmParameters",
            "Background",
            "CheckingPoint",
            "ControlInput",
            "Observation",
            "BackgroundError",
            "ObservationError",
            "EvolutionError",
            "ObservationOperator",
            "EvolutionModel",
            "ControlModel",
            "Name",
            "Directory",
            "Debug",
            "NoDebug",
            "RegulationParameters",
            "Observer",
            ]
        #
        for ename in self.__Concepts:
            self.__adaoObject[ename] = None
        for ename in ("ObservationOperator", "EvolutionModel", "ControlModel"):
            self.__adaoObject[ename] = {}
        for ename in ("Observer",):
            self.__adaoObject[ename]   = []
            self.__StoredInputs[ename] = []
        self.__StoredInputs["Name"] = self.__name
        self.__StoredInputs["Directory"] = self.__directory
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
            Checked              = False,
            ColMajor             = False,
            ColNames             = None,
            DataFile             = None,
            DiagonalSparseMatrix = None,
            ExtraArguments       = None,
            Info                 = None,
            InputFunctionAsMulti = False,
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
            Variable             = None,
            Vector               = None,
            VectorSerie          = None,
            ):
        "Interface unique de definition de variables d'entrees par argument"
        self.__case.register("set",dir(),locals(),None,True)
        try:
            if   Concept in ("Background", "CheckingPoint", "ControlInput", "Observation"):
                commande = getattr(self,"set"+Concept)
                commande(Vector, VectorSerie, Script, DataFile, ColNames, ColMajor, Stored, Scheduler, Checked )
            elif Concept in ("BackgroundError", "ObservationError", "EvolutionError"):
                commande = getattr(self,"set"+Concept)
                commande(Matrix, ScalarSparseMatrix, DiagonalSparseMatrix,
                         Script, Stored, ObjectMatrix, Checked )
            elif Concept == "AlgorithmParameters":
                self.setAlgorithmParameters( Algorithm, Parameters, Script )
            elif Concept == "RegulationParameters":
                self.setRegulationParameters( Algorithm, Parameters, Script )
            elif Concept == "Name":
                self.setName(String)
            elif Concept == "Directory":
                self.setDirectory(String)
            elif Concept == "Debug":
                self.setDebug()
            elif Concept == "NoDebug":
                self.setNoDebug()
            elif Concept == "Observer":
                self.setObserver( Variable, Template, String, Script, Info, ObjectFunction, Scheduler )
            elif Concept == "ObservationOperator":
                self.setObservationOperator(
                    Matrix, OneFunction, ThreeFunctions, AppliedInXb,
                    Parameters, Script, ExtraArguments,
                    Stored, AvoidRC, InputFunctionAsMulti, Checked )
            elif Concept in ("EvolutionModel", "ControlModel"):
                commande = getattr(self,"set"+Concept)
                commande(
                    Matrix, OneFunction, ThreeFunctions,
                    Parameters, Script, Scheduler, ExtraArguments,
                    Stored, AvoidRC, InputFunctionAsMulti, Checked )
            else:
                raise ValueError("the variable named '%s' is not allowed."%str(Concept))
        except Exception as e:
            if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError(("during settings, the following error occurs:\n"+\
                              "\n%s %s\n\nSee also the potential messages, "+\
                              "which can show the origin of the above error, "+\
                              "in the launching terminal.")%(str(e),msg))

    # -----------------------------------------------------------

    def setBackground(self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            DataFile       = None,
            ColNames       = None,
            ColMajor       = False,
            Stored         = False,
            Scheduler      = None,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "Background"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = self.__with_directory(Script),
            asDataFile         = DataFile,
            colNames           = ColNames,
            colMajor           = ColMajor,
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
            DataFile       = None,
            ColNames       = None,
            ColMajor       = False,
            Stored         = False,
            Scheduler      = None,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "CheckingPoint"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = self.__with_directory(Script),
            asDataFile         = DataFile,
            colNames           = ColNames,
            colMajor           = ColMajor,
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
            DataFile       = None,
            ColNames       = None,
            ColMajor       = False,
            Stored         = False,
            Scheduler      = None,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "ControlInput"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = self.__with_directory(Script),
            asDataFile         = DataFile,
            colNames           = ColNames,
            colMajor           = ColMajor,
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
            DataFile       = None,
            ColNames       = None,
            ColMajor       = False,
            Stored         = False,
            Scheduler      = None,
            Checked        = False):
        "Definition d'un concept de calcul"
        Concept = "Observation"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = State(
            name               = Concept,
            asVector           = Vector,
            asPersistentVector = VectorSerie,
            asScript           = self.__with_directory(Script),
            asDataFile         = DataFile,
            colNames           = ColNames,
            colMajor           = ColMajor,
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
            Script               = None,
            Stored               = False,
            ObjectMatrix         = None,
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
            asScript      = self.__with_directory(Script),
            toBeChecked   = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setObservationError(self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            Script               = None,
            Stored               = False,
            ObjectMatrix         = None,
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
            asScript      = self.__with_directory(Script),
            toBeChecked   = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setEvolutionError(self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            Script               = None,
            Stored               = False,
            ObjectMatrix         = None,
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
            asScript      = self.__with_directory(Script),
            toBeChecked   = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setObservationOperator(self,
            Matrix               = None,
            OneFunction          = None,
            ThreeFunctions       = None,
            AppliedInXb          = None,
            Parameters           = None,
            Script               = None,
            ExtraArguments       = None,
            Stored               = False,
            AvoidRC              = True,
            InputFunctionAsMulti = False,
            Checked              = False):
        "Definition d'un concept de calcul"
        Concept = "ObservationOperator"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = FullOperator(
            name             = Concept,
            asMatrix         = Matrix,
            asOneFunction    = OneFunction,
            asThreeFunctions = ThreeFunctions,
            asScript         = self.__with_directory(Script),
            asDict           = Parameters,
            appliedInX       = AppliedInXb,
            extraArguments   = ExtraArguments,
            avoidRC          = AvoidRC,
            inputAsMF        = InputFunctionAsMulti,
            scheduledBy      = None,
            toBeChecked      = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setEvolutionModel(self,
            Matrix               = None,
            OneFunction          = None,
            ThreeFunctions       = None,
            Parameters           = None,
            Script               = None,
            Scheduler            = None,
            ExtraArguments       = None,
            Stored               = False,
            AvoidRC              = True,
            InputFunctionAsMulti = False,
            Checked              = False):
        "Definition d'un concept de calcul"
        Concept = "EvolutionModel"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = FullOperator(
            name             = Concept,
            asMatrix         = Matrix,
            asOneFunction    = OneFunction,
            asThreeFunctions = ThreeFunctions,
            asScript         = self.__with_directory(Script),
            asDict           = Parameters,
            appliedInX       = None,
            extraArguments   = ExtraArguments,
            avoidRC          = AvoidRC,
            inputAsMF        = InputFunctionAsMulti,
            scheduledBy      = Scheduler,
            toBeChecked      = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setControlModel(self,
            Matrix               = None,
            OneFunction          = None,
            ThreeFunctions       = None,
            Parameters           = None,
            Script               = None,
            Scheduler            = None,
            ExtraArguments       = None,
            Stored               = False,
            AvoidRC              = True,
            InputFunctionAsMulti = False,
            Checked              = False):
        "Definition d'un concept de calcul"
        Concept = "ControlModel"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = FullOperator(
            name             = Concept,
            asMatrix         = Matrix,
            asOneFunction    = OneFunction,
            asThreeFunctions = ThreeFunctions,
            asScript         = self.__with_directory(Script),
            asDict           = Parameters,
            appliedInX       = None,
            extraArguments   = ExtraArguments,
            avoidRC          = AvoidRC,
            inputAsMF        = InputFunctionAsMulti,
            scheduledBy      = Scheduler,
            toBeChecked      = Checked,
            )
        if Stored:
            self.__StoredInputs[Concept] = self.__adaoObject[Concept].getO()
        return 0

    def setName(self, String=None):
        "Definition d'un concept de calcul"
        self.__case.register("setName",dir(),locals())
        if String is not None:
            self.__name = str(String)
        else:
            self.__name = None
        self.__StoredInputs["Name"] = self.__name

    def setDirectory(self, String=None):
        "Definition d'un concept de calcul"
        self.__case.register("setDirectory",dir(),locals())
        if os.path.isdir(os.path.abspath(str(String))):
            self.__directory = os.path.abspath(str(String))
        else:
            self.__directory = None
        self.__StoredInputs["Directory"] = self.__directory

    def setDebug(self, __level = 10):
        "NOTSET=0 < DEBUG=10 < INFO=20 < WARNING=30 < ERROR=40 < CRITICAL=50"
        self.__case.register("setDebug",dir(),locals())
        log = logging.getLogger()
        log.setLevel( __level )
        self.__StoredInputs["Debug"]   = __level
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
            asScript      = self.__with_directory(Script),
            )
        return 0

    def updateAlgorithmParameters(self,
            Parameters = None,
            Script     = None):
        "Mise a jour d'un concept de calcul"
        if "AlgorithmParameters" not in self.__adaoObject or self.__adaoObject["AlgorithmParameters"] is None:
            raise ValueError("\n\nNo algorithm registred, set one before updating parameters or executing\n")
        self.__adaoObject["AlgorithmParameters"].updateParameters(
            asDict        = Parameters,
            asScript      = self.__with_directory(Script),
            )
        return 0

    def setRegulationParameters(self,
            Algorithm  = None,
            Parameters = None,
            Script     = None):
        "Definition d'un concept de calcul"
        Concept = "RegulationParameters"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept] = RegulationAndParameters(
            name          = Concept,
            asAlgorithm   = Algorithm,
            asDict        = Parameters,
            asScript      = self.__with_directory(Script),
            )
        return 0

    def setObserver(self,
            Variable       = None,
            Template       = None,
            String         = None,
            Script         = None,
            Info           = None,
            ObjectFunction = None,
            Scheduler      = None):
        "Definition d'un concept de calcul"
        Concept = "Observer"
        self.__case.register("set"+Concept, dir(), locals())
        self.__adaoObject[Concept].append( DataObserver(
            name        = Concept,
            onVariable  = Variable,
            asTemplate  = Template,
            asString    = String,
            asScript    = self.__with_directory(Script),
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
        "Permet de retirer un observer à une ou des variable nommée"
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

    def get(self, Concept=None, noDetails=True ):
        "Recuperation d'une sortie du calcul"
        if Concept is not None:
            try:
                self.__case.register("get", dir(), locals(), Concept) # Break pickle in Python 2
            except Exception:
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
            elif Concept == "AlgorithmRequiredInputs" and self.__adaoObject["AlgorithmParameters"] is not None:
                return self.__adaoObject["AlgorithmParameters"].getAlgorithmInputArguments()
                #
            elif Concept == "AlgorithmAttributes" and self.__adaoObject["AlgorithmParameters"] is not None:
                return self.__adaoObject["AlgorithmParameters"].getAlgorithmAttributes()
                #
            else:
                raise ValueError("The requested key \"%s\" does not exists as an input or a stored variable."%Concept)
        else:
            allvariables = {}
            allvariables.update( {"AlgorithmParameters":self.__adaoObject["AlgorithmParameters"].get()} )
            # allvariables.update( self.__adaoObject["AlgorithmParameters"].get() )
            allvariables.update( self.__StoredInputs )
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
            trypath = os.path.join(directory,"daAlgorithms")
            if os.path.isdir(trypath):
                for fname in os.listdir(trypath):
                    if os.path.isfile(os.path.join(trypath,fname)):
                        root, ext = os.path.splitext(fname)
                        if ext != ".py": continue
                        fc = open(os.path.join(trypath,fname)).read()
                        iselal = bool("class ElementaryAlgorithm" in fc)
                        if iselal and ext == '.py' and root != '__init__':
                            files.append(root)
        files.sort()
        return files

    def get_algorithms_main_path(self):
        """
        Renvoie le chemin pour le répertoire principal contenant les algorithmes
        """
        return self.__parent

    def add_algorithms_path(self, Path=None):
        """
        Ajoute au chemin de recherche des algorithmes un répertoire dans lequel
        se trouve un sous-répertoire "daAlgorithms"
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

    # -----------------------------------------------------------

    def execute(self, Executor=None, SaveCaseInFile=None, nextStep=False):
        "Lancement du calcul"
        self.__case.register("execute",dir(),locals(),None,True)
        self.updateAlgorithmParameters(Parameters={"nextStep":bool(nextStep)})
        if not nextStep: Operator.CM.clearCache()
        try:
            if   Executor == "YACS": self.__executeYACSScheme( SaveCaseInFile )
            else:                    self.__executePythonScheme( SaveCaseInFile )
        except Exception as e:
            if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError(("during execution, the following error occurs:\n"+\
                             "\n%s %s\n\nSee also the potential messages, "+\
                             "which can show the origin of the above error, "+\
                             "in the launching terminal.\n")%(str(e),msg))
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
        self.dump( FileName, "YACS")
        self.__adaoObject["AlgorithmParameters"].executeYACSScheme( FileName )
        return 0

    # -----------------------------------------------------------

    def dump(self, FileName=None, Formater="TUI"):
        "Restitution normalisée des commandes"
        __Upa = "\n".join(self.__PostAnalysis)
        return self.__case.dump(FileName, Formater, __Upa)

    def load(self, FileName=None, Content=None, Object=None, Formater="TUI"):
        "Chargement normalisé des commandes"
        __commands = self.__case.load(FileName, Content, Object, Formater)
        from numpy import array, matrix
        for __command in __commands:
            if __command.find("set")>-1 and __command.find("set_")<0:
                exec("self."+__command)
            else:
                self.__PostAnalysis.append(__command)
        return self

    def convert(self,
        FileNameFrom=None, ContentFrom=None, ObjectFrom=None, FormaterFrom="TUI",
        FileNameTo=None, FormaterTo="TUI",
        ):
        "Conversion normalisée des commandes"
        return self.load(
            FileName=FileNameFrom, Content=ContentFrom, Object=ObjectFrom, Formater=FormaterFrom
            ).dump(
            FileName=FileNameTo, Formater=FormaterTo
            )

    def clear(self):
        "Effacement du contenu du cas en cours"
        self.__init__(self.__name)

    # -----------------------------------------------------------

    def __with_directory(self, __filename=None):
        if os.path.exists(str(__filename)):
            __fullpath = __filename
        elif os.path.exists(os.path.join(str(self.__directory), str(__filename))):
            __fullpath = os.path.join(self.__directory, str(__filename))
        else:
            __fullpath = __filename
        return __fullpath

    def __dir__(self):
        "Clarifie la visibilité des méthodes"
        return ['set', 'get', 'execute', 'dump', 'load', '__doc__', '__init__', '__module__']

    def prepare_to_pickle(self):
        "Retire les variables non pickelisables, avec recopie efficace"
        if self.__adaoObject['AlgorithmParameters'] is not None:
            for k in self.__adaoObject['AlgorithmParameters'].keys():
                if k == "Algorithm": continue
                if k in self.__StoredInputs:
                    raise ValueError("The key \"%s\" to be transfered for pickling will overwrite an existing one."%(k,))
                if self.__adaoObject['AlgorithmParameters'].hasObserver( k ):
                    self.__adaoObject['AlgorithmParameters'].removeObserver( k, "", True )
                self.__StoredInputs[k] = self.__adaoObject['AlgorithmParameters'].pop(k, None)
        if sys.version_info[0] == 2:
            del self.__adaoObject # Because it breaks pickle in Python 2. Not required for Python 3
            del self.__case       # Because it breaks pickle in Python 2. Not required for Python 3
        if sys.version_info.major < 3:
            return 0
        else:
            return self.__StoredInputs

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
