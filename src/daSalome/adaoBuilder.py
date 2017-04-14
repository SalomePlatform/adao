#-*-coding:iso-8859-1-*-
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
    Normalized interface for ADAO scripting (full version API)
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["New"]

import os
from daCore.AssimilationStudy import AssimilationStudy as _AssimilationStudy
from daCore.Templates import ObserverTemplates as _ObserverTemplates
from daCore.BasicObjects import ImportFromScript as _ImportFromScript
from daCore.BasicObjects import ObserverF as _ObserverF

# ==============================================================================
class New(object):
    """
    Creation TUI d'un cas ADAO
    """
    def __init__(self, name = ""):
        self.__adaoStudy = _AssimilationStudy(name)
        self.__case = _CaseLogger(name)

    # -----------------------------------------------------------

    def set(
            self,
            Concept              = None,
            Algorithm            = None,
            DiagonalSparseMatrix = None,
            Info                 = None,
            Matrix               = None,
            OneFunction          = None,
            Parameters           = None,
            ScalarSparseMatrix   = None,
            Script               = None,
            Stored               = False,
            String               = None,
            Template             = None,
            ThreeFunctions       = None,
            AppliedInXb          = None,
            Variable             = None,
            Vector               = None,
            VectorSerie          = None):
        "Interface unique de definition de variables d'entrees par argument"
        self.__case.register("set",dir(),locals(),None,True)
        try:
            if   Concept == "Background":
                self.setBackground(Vector,VectorSerie,Script,Stored)
            elif Concept == "BackgroundError":
                self.setBackgroundError(Matrix,ScalarSparseMatrix,
                                        DiagonalSparseMatrix,Script,Stored)
            elif Concept == "CheckingPoint":
                self.setCheckingPoint(Vector,VectorSerie,Script,Stored)
            elif Concept == "ControlModel":
                self.setControlModel(Matrix,OneFunction,ThreeFunctions,
                                     Parameters,Script,Stored)
            elif Concept == "ControlInput":
                self.setControlInput(Vector,VectorSerie,Script,Stored)
            elif Concept == "EvolutionError":
                self.setEvolutionError(Matrix,ScalarSparseMatrix,
                                       DiagonalSparseMatrix,Script,Stored)
            elif Concept == "EvolutionModel":
                self.setEvolutionModel(Matrix,OneFunction,ThreeFunctions,
                                       Parameters,Script,Stored)
            elif Concept == "Observation":
                self.setObservation(Vector,VectorSerie,Script,Stored)
            elif Concept == "ObservationError":
                self.setObservationError(Matrix,ScalarSparseMatrix,
                                         DiagonalSparseMatrix,Script,Stored)
            elif Concept == "ObservationOperator":
                self.setObservationOperator(Matrix,OneFunction,ThreeFunctions,
                                            AppliedInXb, Parameters,Script,Stored)
            elif Concept == "AlgorithmParameters":
                self.setAlgorithmParameters(Algorithm,Parameters,Script)
            elif Concept == "Debug":
                self.setDebug()
            elif Concept == "NoDebug":
                self.setNoDebug()
            elif Concept == "Observer":
                self.setObserver(Variable,Template,String,Script,Info)
            else:
                raise ValueError("the variable named '%s' is not allowed."%str(Concept))
        except Exception as e:
            if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError("during settings, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal."%(str(e),msg))

    # -----------------------------------------------------------

    def setBackground(
            self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Stored         = False):
        "Definition d'une entree de calcul"
        self.__case.register("setBackground", dir(), locals())
        if Script is not None:
            __Vector, __PersistentVector = None, None
            if VectorSerie:
                __PersistentVector = _ImportFromScript(Script).getvalue( "Background" )
            else:
                __Vector = _ImportFromScript(Script).getvalue( "Background" )
        else:
            __Vector, __PersistentVector = Vector, VectorSerie
        #
        self.__adaoStudy.setBackground(
            asVector           = __Vector,
            asPersistentVector = __PersistentVector,
            toBeStored         = Stored,
            )

    def setBackgroundError(
            self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            Script               = None,
            Stored               = False):
        "Definition d'une entree de calcul"
        self.__case.register("setBackgroundError", dir(), locals())
        if Script is not None:
            __Covariance, __Scalar, __Vector = None, None, None
            if ScalarSparseMatrix:
                __Scalar = _ImportFromScript(Script).getvalue( "BackgroundError" )
            elif DiagonalSparseMatrix:
                __Vector = _ImportFromScript(Script).getvalue( "BackgroundError" )
            else:
                __Covariance = _ImportFromScript(Script).getvalue( "BackgroundError" )
        else:
            __Covariance, __Scalar, __Vector = Matrix, ScalarSparseMatrix, DiagonalSparseMatrix
        #
        self.__adaoStudy.setBackgroundError(
            asCovariance  = __Covariance,
            asEyeByScalar = __Scalar,
            asEyeByVector = __Vector,
            toBeStored    = Stored,
            )

    def setCheckingPoint(
            self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Stored         = False):
        "Definition d'une entree de verification"
        self.__case.register("setCheckingPoint", dir(), locals())
        if Script is not None:
            __Vector, __PersistentVector = None, None
            if VectorSerie:
                __PersistentVector = _ImportFromScript(Script).getvalue( "CheckingPoint" )
            else:
                __Vector = _ImportFromScript(Script).getvalue( "CheckingPoint" )
        else:
            __Vector, __PersistentVector = Vector, VectorSerie
        #
        self.__adaoStudy.setBackground(
            asVector           = __Vector,
            asPersistentVector = __PersistentVector,
            toBeStored         = Stored,
            )

    def setControlModel(
            self,
            Matrix         = None,
            OneFunction    = None,
            ThreeFunctions = None,
            Parameters     = None,
            Script         = None,
            Stored         = False):
        "Definition d'une entree de calcul"
        self.__case.register("setControlModel", dir(), locals())
        __Parameters = {}
        if (Parameters is not None) and isinstance(Parameters, dict):
            if "DifferentialIncrement" in Parameters:
                __Parameters["withIncrement"] = Parameters["DifferentialIncrement"]
            if "CenteredFiniteDifference" in Parameters:
                __Parameters["withCenteredDF"] = Parameters["CenteredFiniteDifference"]
        if Script is not None:
            __Matrix, __Function = None, None
            if Matrix:
                __Matrix = _ImportFromScript(Script).getvalue( "ObservationOperator" )
            elif OneFunction:
                __Function = { "Direct":_ImportFromScript(Script).getvalue( "DirectOperator" ) }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif ThreeFunctions:
                __Function = {
                    "Direct" :_ImportFromScript(Script).getvalue( "DirectOperator" ),
                    "Tangent":_ImportFromScript(Script).getvalue( "TangentOperator" ),
                    "Adjoint":_ImportFromScript(Script).getvalue( "AdjointOperator" ),
                    }
                __Function.update(__Parameters)
        else:
            __Matrix = Matrix
            if OneFunction is not None:
                __Function = { "Direct":OneFunction }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif ThreeFunctions is not None:
                if (not isinstance(ThreeFunctions, dict)) or \
                   "Direct"  not in ThreeFunctions or \
                   "Tangent" not in ThreeFunctions or \
                   "Adjoint" not in ThreeFunctions:
                    raise ValueError("ThreeFunctions has to be a dictionnary and to have the 3 keys Direct, Tangent, Adjoint")
                __Function = ThreeFunctions
                __Function.update(__Parameters)
            else:
                __Function = None
        #
        self.__adaoStudy.setControlModel(
            asFunction = __Function,
            asMatrix   = __Matrix,
            toBeStored = Stored,
            )

    def setControlInput(
            self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Stored         = False):
        "Definition d'une entree de calcul"
        self.__case.register("setControlInput", dir(), locals())
        if Script is not None:
            __Vector, __PersistentVector = None, None
            if VectorSerie:
                __PersistentVector = _ImportFromScript(Script).getvalue( "ControlInput" )
            else:
                __Vector = _ImportFromScript(Script).getvalue( "ControlInput" )
        else:
            __Vector, __PersistentVector = Vector, VectorSerie
        #
        self.__adaoStudy.setControlInput(
            asVector           = __Vector,
            asPersistentVector = __PersistentVector,
            toBeStored         = Stored,
            )

    def setEvolutionError(
            self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            Script               = None,
            Stored               = False):
        "Definition d'une entree de calcul"
        self.__case.register("setEvolutionError", dir(), locals())
        if Script is not None:
            __Covariance, __Scalar, __Vector = None, None, None
            if ScalarSparseMatrix:
                __Scalar = _ImportFromScript(Script).getvalue( "EvolutionError" )
            elif DiagonalSparseMatrix:
                __Vector = _ImportFromScript(Script).getvalue( "EvolutionError" )
            else:
                __Covariance = _ImportFromScript(Script).getvalue( "EvolutionError" )
        else:
            __Covariance, __Scalar, __Vector = Matrix, ScalarSparseMatrix, DiagonalSparseMatrix
        #
        self.__adaoStudy.setEvolutionError(
            asCovariance  = __Covariance,
            asEyeByScalar = __Scalar,
            asEyeByVector = __Vector,
            toBeStored    = Stored,
            )

    def setEvolutionModel(
            self,
            Matrix         = None,
            OneFunction    = None,
            ThreeFunctions = None,
            Parameters     = None,
            Script         = None,
            Stored         = False):
        "Definition d'une entree de calcul"
        self.__case.register("setEvolutionModel", dir(), locals())
        __Parameters = {}
        if (Parameters is not None) and isinstance(Parameters, dict):
            if "DifferentialIncrement" in Parameters:
                __Parameters["withIncrement"] = Parameters["DifferentialIncrement"]
            if "CenteredFiniteDifference" in Parameters:
                __Parameters["withCenteredDF"] = Parameters["CenteredFiniteDifference"]
            if "EnableMultiProcessing" in Parameters:
                __Parameters["withmpEnabled"] = Parameters["EnableMultiProcessing"]
            if "NumberOfProcesses" in Parameters:
                __Parameters["withmpWorkers"] = Parameters["NumberOfProcesses"]
        if Script is not None:
            __Matrix, __Function = None, None
            if Matrix:
                __Matrix = _ImportFromScript(Script).getvalue( "ObservationOperator" )
            elif OneFunction:
                __Function = { "Direct":_ImportFromScript(Script).getvalue( "DirectOperator" ) }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif ThreeFunctions:
                __Function = {
                    "Direct" :_ImportFromScript(Script).getvalue( "DirectOperator" ),
                    "Tangent":_ImportFromScript(Script).getvalue( "TangentOperator" ),
                    "Adjoint":_ImportFromScript(Script).getvalue( "AdjointOperator" ),
                    }
                __Function.update(__Parameters)
        else:
            __Matrix = Matrix
            if OneFunction is not None:
                __Function = { "Direct":OneFunction }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif ThreeFunctions is not None:
                if (not isinstance(ThreeFunctions, dict)) or \
                   "Direct"  not in ThreeFunctions or \
                   "Tangent" not in ThreeFunctions or \
                   "Adjoint" not in ThreeFunctions:
                    raise ValueError("ThreeFunctions has to be a dictionnary and to have the 3 keys Direct, Tangent, Adjoint")
                __Function = ThreeFunctions
                __Function.update(__Parameters)
            else:
                __Function = None
        #
        self.__adaoStudy.setEvolutionModel(
            asFunction = __Function,
            asMatrix   = __Matrix,
            toBeStored = Stored,
            )

    def setObservation(
            self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Stored         = False):
        "Definition d'une entree de calcul"
        self.__case.register("setObservation", dir(), locals())
        if Script is not None:
            __Vector, __PersistentVector = None, None
            if VectorSerie:
                __PersistentVector = _ImportFromScript(Script).getvalue( "Observation" )
            else:
                __Vector = _ImportFromScript(Script).getvalue( "Observation" )
        else:
            __Vector, __PersistentVector = Vector, VectorSerie
        #
        self.__adaoStudy.setObservation(
            asVector           = __Vector,
            asPersistentVector = __PersistentVector,
            toBeStored         = Stored,
            )

    def setObservationError(
            self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            Script               = None,
            Stored               = False):
        "Definition d'une entree de calcul"
        self.__case.register("setObservationError", dir(), locals())
        if Script is not None:
            __Covariance, __Scalar, __Vector = None, None, None
            if ScalarSparseMatrix:
                __Scalar = _ImportFromScript(Script).getvalue( "ObservationError" )
            elif DiagonalSparseMatrix:
                __Vector = _ImportFromScript(Script).getvalue( "ObservationError" )
            else:
                __Covariance = _ImportFromScript(Script).getvalue( "ObservationError" )
        else:
            __Covariance, __Scalar, __Vector = Matrix, ScalarSparseMatrix, DiagonalSparseMatrix
        #
        self.__adaoStudy.setObservationError(
            asCovariance  = __Covariance,
            asEyeByScalar = __Scalar,
            asEyeByVector = __Vector,
            toBeStored    = Stored,
            )

    def setObservationOperator(
            self,
            Matrix         = None,
            OneFunction    = None,
            ThreeFunctions = None,
            AppliedInXb    = None,
            Parameters     = None,
            Script         = None,
            Stored         = False):
        "Definition d'une entree de calcul"
        self.__case.register("setObservationOperator", dir(), locals())
        __Parameters = {}
        if (Parameters is not None) and isinstance(Parameters, dict):
            if "DifferentialIncrement" in Parameters:
                __Parameters["withIncrement"] = Parameters["DifferentialIncrement"]
            if "CenteredFiniteDifference" in Parameters:
                __Parameters["withCenteredDF"] = Parameters["CenteredFiniteDifference"]
            if "EnableMultiProcessing" in Parameters:
                __Parameters["EnableMultiProcessing"] = Parameters["EnableMultiProcessing"]
                __Parameters["withmpEnabled"]         = Parameters["EnableMultiProcessing"]
            if "NumberOfProcesses" in Parameters:
                __Parameters["NumberOfProcesses"] = Parameters["NumberOfProcesses"]
                __Parameters["withmpWorkers"]     = Parameters["NumberOfProcesses"]
        if Script is not None:
            __Matrix, __Function = None, None
            if Matrix:
                __Matrix = _ImportFromScript(Script).getvalue( "ObservationOperator" )
            elif OneFunction:
                __Function = { "Direct":_ImportFromScript(Script).getvalue( "DirectOperator" ) }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif ThreeFunctions:
                __Function = {
                    "Direct" :_ImportFromScript(Script).getvalue( "DirectOperator" ),
                    "Tangent":_ImportFromScript(Script).getvalue( "TangentOperator" ),
                    "Adjoint":_ImportFromScript(Script).getvalue( "AdjointOperator" ),
                    }
                __Function.update(__Parameters)
        else:
            __Matrix = Matrix
            if OneFunction is not None:
                __Function = { "Direct":OneFunction }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif ThreeFunctions is not None:
                if (not isinstance(ThreeFunctions, dict)) or \
                   "Direct"  not in ThreeFunctions or \
                   "Tangent" not in ThreeFunctions or \
                   "Adjoint" not in ThreeFunctions:
                    raise ValueError("ThreeFunctions has to be a dictionnary and to have the 3 keys Direct, Tangent, Adjoint")
                __Function = ThreeFunctions
                __Function.update(__Parameters)
            else:
                __Function = None
        if AppliedInXb is not None:
            __appliedToX = {"HXb":AppliedInXb}
        else:
            __appliedToX = None
        #
        self.__adaoStudy.setObservationOperator(
            asFunction = __Function,
            asMatrix   = __Matrix,
            appliedToX = __appliedToX,
            toBeStored = Stored,
            )

    # -----------------------------------------------------------

    def setAlgorithmParameters(
            self,
            Algorithm  = None,
            Parameters = None,
            Script     = None):
        "Definition d'un parametrage du calcul"
        self.__case.register("setAlgorithmParameters", dir(), locals())
        if Script is not None:
            __Algorithm  = _ImportFromScript(Script).getvalue( "Algorithm" )
            __Parameters = _ImportFromScript(Script).getvalue( "AlgorithmParameters", "Parameters" )
        else:
            __Algorithm  = Algorithm
            __Parameters = Parameters
        self.__adaoStudy.setAlgorithm( choice = __Algorithm )
        self.__adaoStudy.setAlgorithmParameters( asDico = __Parameters )

    def setDebug(self):
        "Definition d'un parametrage du calcul"
        self.__case.register("setDebug",dir(),locals())
        return self.__adaoStudy.setDebug()

    def setNoDebug(self):
        "Definition d'un parametrage du calcul"
        self.__case.register("setNoDebug",dir(),locals())
        return self.__adaoStudy.unsetDebug()

    def setObserver(
            self,
            Variable = None,
            Template = None,
            String   = None,
            Script   = None,
            Info     = None):
        "Definition d'un parametrage du calcul"
        self.__case.register("setObserver", dir(), locals())
        if Variable is None:
            raise ValueError("setting an observer has to be done over a variable name, not over None.")
        else:
            __Variable = str(Variable)
            if Info is None:
                __Info = str(Variable)
            else:
                __Info = str(Info)
        #
        if String is not None:
            __FunctionText = String
        elif (Template is not None) and (Template in _ObserverTemplates):
            __FunctionText = _ObserverTemplates[Template]
        elif Script is not None:
            __FunctionText = _ImportFromScript(Script).getstring()
        else:
            __FunctionText = ""
        __Function = _ObserverF(__FunctionText)
        #
        self.__adaoStudy.setDataObserver(
            VariableName   = __Variable,
            HookFunction   = __Function.getfunc(),
            HookParameters = __Info,
            )

    # -----------------------------------------------------------

    def executePythonScheme(self):
        "Lancement du calcul"
        self.__case.register("executePythonScheme", dir(), locals())
        try:
            self.__adaoStudy.analyze()
        except Exception as e:
            if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError("during execution, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal."%(str(e),msg))

    execute = executePythonScheme

    def executeYACSScheme(self, File=None):
        "Lancement du calcul"
        self.__case.register("executeYACSScheme", dir(), locals())
        raise NotImplementedError()

    # -----------------------------------------------------------

    def get(self, Concept=None):
        "Recuperation d'une sortie du calcul"
        self.__case.register("get",dir(),locals(),Concept)
        return self.__adaoStudy.get(Concept)

    def dumpNormalizedCommands(self, filename=None):
        "Recuperation de la liste des commandes du cas TUI"
        return self.__case.dump(filename, "TUI")

    def __dir__(self):
        return ['set', 'get', 'execute', '__doc__', '__init__', '__module__']

# ==============================================================================
class _CaseLogger(object):
    """
    Conservation des commandes de creation d'un cas
    """
    def __init__(self, __name="", __objname="case"):
        self.__name     = str(__name)
        self.__objname  = str(__objname)
        self.__logSerie = []
        self.__switchoff = False
    def register(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Enregistrement d'une commande individuelle"
        if __command is not None and __keys is not None and __local is not None and not self.__switchoff:
            if "self" in __keys: __keys.remove("self")
            self.__logSerie.append( (str(__command), __keys, __local, __pre, __switchoff) )
            if __switchoff:
                self.__switchoff = True
        if not __switchoff:
            self.__switchoff = False
    def dump(self, __filename=None, __format="TUI"):
        if __format == "TUI":
            self.__dumper = _TUIViewer(self.__name, self.__objname, self.__logSerie)
            __text = self.__dumper.dump(__filename)
        else:
            raise ValueError("Dumping as \"%s\" is not available"%__format)
        return __text

# ==============================================================================
class _GenericViewer(object):
    """
    Etablissement des commandes de creation d'une vue
    """
    def __init__(self, __name="", __objname="case", __content=None):
        self._name     = str(__name)
        self._objname  = str(__objname)
        self._lineSerie = []
        self._switchoff = False
        self._numobservers = 1
    def _addLine(self, line=""):
        self._lineSerie.append(line)
    def _append(self):
        "Enregistrement d'une commande individuelle"
        raise NotImplementedError()
    def dump(self, __filename=None):
        "Restitution de la liste des commandes de creation d'un cas"
        raise NotImplementedError()

class _TUIViewer(_GenericViewer):
    """
    Etablissement des commandes de creation d'un cas TUI
    """
    def __init__(self, __name="", __objname="case", __content=None):
        _GenericViewer.__init__(self, __name, __objname, __content)
        self._addLine("#\n# Python script for ADAO TUI\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("import adaoBuilder")
        self._addLine("%s = adaoBuilder.New('%s')"%(self._objname, self._name))
        if __content is not None:
            for command in __content:
                self._append(*command)
    def _append(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        if __command is not None and __keys is not None and __local is not None and not self._switchoff:
            __text  = ""
            if __pre is not None:
                __text += "%s = "%__pre
            __text += "%s.%s( "%(self._objname,str(__command))
            if "self" in __keys: __keys.remove("self")
            for k in __keys:
                __v = __local[k]
                if __v is None: continue
                __text += "%s=%s, "%(k,repr(__v))
            __text += ")"
            self._addLine(__text)
            if __switchoff:
                self._switchoff = True
        if not __switchoff:
            self._switchoff = False
    def dump(self, __filename=None):
        __text = "\n".join(self._lineSerie)
        if __filename is not None:
            fid = open(__filename,"w")
            fid.write(__text)
            fid.close()
        return __text

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')
