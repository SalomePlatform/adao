#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2015 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
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
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

"""
    Interface de scripting pour une étude ADAO
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["New"]

import os
from daCore import AssimilationStudy

class New(object):
    """
    Creation TUI d'un cas ADAO
    """
    def __init__(self, name = ""):
        self.__adaoStudy = AssimilationStudy.AssimilationStudy(name)
        self.__dumper = _DumpLogger(name)

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
            Variable             = None,
            Vector               = None,
            VectorSerie          = None
            ):
        "Interface unique de définition de variables d'entrées par argument"
        self.__dumper.register("set",dir(),locals(),None,True)
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
                                            Parameters,Script,Stored)
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
            if type(e) == type(SyntaxError()): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError("during settings, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal."%(str(e),msg))

    # -----------------------------------------------------------

    def setBackground(
            self,
            Vector         = None,
            VectorSerie    = None,
            Script         = None,
            Stored         = False):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setBackground", dir(), locals())
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
        "Définition d'une entrée de calcul"
        self.__dumper.register("setBackgroundError", dir(), locals())
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
        "Définition d'une entrée de vérification"
        self.__dumper.register("setCheckingPoint", dir(), locals())
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
        "Définition d'une entrée de calcul"
        self.__dumper.register("setControlModel", dir(), locals())
        __Parameters = {}
        if Parameters is not None and type(Parameters) == type({}):
            if Parameters.has_key("DifferentialIncrement"):
                __Parameters["withIncrement"] = Parameters["DifferentialIncrement"]
            if Parameters.has_key("CenteredFiniteDifference"):
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
                if (type(ThreeFunctions) is not type({})) or \
                    not ThreeFunctions.has_key("Direct") or \
                    not ThreeFunctions.has_key("Tangent") or \
                    not ThreeFunctions.has_key("Adjoint"):
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
        "Définition d'une entrée de calcul"
        self.__dumper.register("setControlInput", dir(), locals())
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
        "Définition d'une entrée de calcul"
        self.__dumper.register("setEvolutionError", dir(), locals())
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
        "Définition d'une entrée de calcul"
        self.__dumper.register("setEvolutionModel", dir(), locals())
        __Parameters = {}
        if Parameters is not None and type(Parameters) == type({}):
            if Parameters.has_key("DifferentialIncrement"):
                __Parameters["withIncrement"] = Parameters["DifferentialIncrement"]
            if Parameters.has_key("CenteredFiniteDifference"):
                __Parameters["withCenteredDF"] = Parameters["CenteredFiniteDifference"]
            if Parameters.has_key("EnableMultiProcessing"):
                __Parameters["withmpEnabled"] = Parameters["EnableMultiProcessing"]
            if Parameters.has_key("NumberOfProcesses"):
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
                if (type(ThreeFunctions) is not type({})) or \
                    not ThreeFunctions.has_key("Direct") or \
                    not ThreeFunctions.has_key("Tangent") or \
                    not ThreeFunctions.has_key("Adjoint"):
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
        "Définition d'une entrée de calcul"
        self.__dumper.register("setObservation", dir(), locals())
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
        "Définition d'une entrée de calcul"
        self.__dumper.register("setObservationError", dir(), locals())
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
            Parameters     = None,
            Script         = None,
            Stored         = False):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setObservationOperator", dir(), locals())
        __Parameters = {}
        if Parameters is not None and type(Parameters) == type({}):
            if Parameters.has_key("DifferentialIncrement"):
                __Parameters["withIncrement"] = Parameters["DifferentialIncrement"]
            if Parameters.has_key("CenteredFiniteDifference"):
                __Parameters["withCenteredDF"] = Parameters["CenteredFiniteDifference"]
            if Parameters.has_key("EnableMultiProcessing"):
                __Parameters["withmpEnabled"] = Parameters["EnableMultiProcessing"]
            if Parameters.has_key("NumberOfProcesses"):
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
                if (type(ThreeFunctions) is not type({})) or \
                    not ThreeFunctions.has_key("Direct") or \
                    not ThreeFunctions.has_key("Tangent") or \
                    not ThreeFunctions.has_key("Adjoint"):
                    raise ValueError("ThreeFunctions has to be a dictionnary and to have the 3 keys Direct, Tangent, Adjoint") 
                __Function = ThreeFunctions
                __Function.update(__Parameters)
            else:
                __Function = None
        #
        self.__adaoStudy.setObservationOperator(
            asFunction = __Function,
            asMatrix   = __Matrix,
            toBeStored = Stored,
            )

    # -----------------------------------------------------------

    def setAlgorithmParameters(
            self,
            Algorithm  = None,
            Parameters = None,
            Script     = None):
        "Définition d'un paramétrage du calcul"
        self.__dumper.register("setAlgorithmParameters", dir(), locals())
        if Script is not None:
            __Algorithm  = _ImportFromScript(Script).getvalue( "Algorithm" )
            __Parameters = _ImportFromScript(Script).getvalue( "AlgorithmParameters", "Parameters" )
        else:
            __Algorithm  = Algorithm
            __Parameters = Parameters
        self.__adaoStudy.setAlgorithm( choice = __Algorithm )
        self.__adaoStudy.setAlgorithmParameters( asDico = __Parameters )

    def setDebug(self):
        "Définition d'un paramétrage du calcul"
        self.__dumper.register("setDebug",dir(),locals())
        return self.__adaoStudy.setDebug()

    def setNoDebug(self):
        "Définition d'un paramétrage du calcul"
        self.__dumper.register("setNoDebug",dir(),locals())
        return self.__adaoStudy.unsetDebug()

    def setObserver(
            self,
            Variable = None,
            Template = None,
            String   = None,
            Script   = None,
            Info     = None):
        "Définition d'un paramétrage du calcul"
        self.__dumper.register("setObserver", dir(), locals())
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
        elif Template is not None:
            if Template == "ValuePrinter":
                __FunctionText = "print info,var[-1]"
            if Template == "ValueSeriePrinter":
                __FunctionText = "print info,var[:]"
            if Template == "ValueSaver":
                __FunctionText = r"import numpy,re\nv=numpy.array((var[-1]))\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\s','_',f)\nprint 'Value saved in \"%s\"'%f\nnumpy.savetxt(f,v)"
            if Template == "ValueSerieSaver":
                __FunctionText = r"import numpy,re\nv=numpy.array((var[:])) \nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\s','_',f)\nprint 'Value saved in \"%s\"'%f\nnumpy.savetxt(f,v)"
            if Template == "ValuePrinterAndSaver":
                __FunctionText = r"import numpy,re\nv=numpy.array((var[-1]))\nprint info,v\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\s','_',f)\nprint 'Value saved in \"%s\"'%f\nnumpy.savetxt(f,v)"
            if Template == "ValueSeriePrinterAndSaver":
                __FunctionText = r"import numpy,re\nv=numpy.array((var[:])) \nprint info,v\nglobal istep\ntry:\n    istep += 1\nexcept:\n    istep = 0\nf='/tmp/value_%s_%05i.txt'%(info,istep)\nf=re.sub('\s','_',f)\nprint 'Value saved in \"%s\"'%f\nnumpy.savetxt(f,v)"
            if Template == "ValueGnuPlotter":
                __FunctionText = r"import Gnuplot\nglobal ifig,gp\ntry:\n    ifig += 1\n    gp('set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp('set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( var[-1], with_='lines lw 2' ) )"
            if Template == "ValueSerieGnuPlotter":
                __FunctionText = r"import Gnuplot\nglobal ifig,gp\ntry:\n    ifig += 1\n    gp('set style data lines')\nexcept:\n    ifig = 0\n    gp = Gnuplot.Gnuplot(persist=1)\n    gp('set style data lines')\ngp('set title  \"%s (Figure %i)\"'%(info,ifig))\ngp.plot( Gnuplot.Data( var[:], with_='lines lw 2' ) )"
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
        self.__dumper.register("executePythonScheme", dir(), locals())
        try:
            self.__adaoStudy.analyze()
        except Exception as e:
            if type(e) == type(SyntaxError()): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError("during execution, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal."%(str(e),msg))

    execute = executePythonScheme

    def executeYACSScheme(self, File=None):
        "Lancement du calcul"
        self.__dumper.register("executeYACSScheme", dir(), locals())
        raise NotImplementedError()

    # -----------------------------------------------------------

    def get(self, Concept=None):
        "Récupération d'une sortie du calcul"
        self.__dumper.register("get",dir(),locals(),Concept)
        return self.__adaoStudy.get(Concept)

    def dumpNormalizedCommands(self, filename=None):
        "Récupération de la liste des commandes du cas"
        return self.__dumper.dump(filename)

    def __dir__(self):
        return ['set', 'get', 'execute', '__doc__', '__init__', '__module__']

class _DumpLogger(object):
    """
    Conservation des commandes de création d'un cas
    """
    def __init__(self, __name="", __objname="case"):
        self.__name     = str(__name)
        self.__objname  = str(__objname)
        self.__logSerie = []
        self.__switchoff = False
        self.__logSerie.append("#\n# Python script for ADAO TUI\n#")
        self.__logSerie.append("from numpy import array, matrix")
        self.__logSerie.append("import adaoBuilder")
        self.__logSerie.append("%s = adaoBuilder.New('%s')"%(self.__objname, self.__name))
    def register(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Enregistrement d'une commande individuelle"
        if __command is not None and __keys is not None and __local is not None and not self.__switchoff:
            __text  = ""
            if __pre is not None:
                __text += "%s = "%__pre
            __text += "%s.%s( "%(self.__objname,str(__command))
            __keys.remove("self")
            for k in __keys:
                __v = __local[k]
                if __v is None: continue
                __text += "%s=%s, "%(k,repr(__v))
            __text += ")"
            self.__logSerie.append(__text)
            if __switchoff:
                self.__switchoff = True
        if not __switchoff:
            self.__switchoff = False
    def dump(self, __filename=None):
        "Restitution de la liste des commandes de création d'un cas"
        __text = "\n".join(self.__logSerie)
        if __filename is not None:
            fid = open(__filename,"w")
            fid.write(__text)
            fid.close()
        return __text

class _ObserverF(object):
    """
    Création d'une fonction d'observateur à partir de son texte
    """
    def __init__(self, corps=""):
        self.__corps = corps
    def func(self,var,info):
        "Fonction d'observation"
        exec(self.__corps)
    def getfunc(self):
        "Restitution du pointeur de fonction dans l'objet"
        return self.func

class _ImportFromScript(object):
    """
    Obtention d'une variable nommée depuis un fichier script importé
    """
    def __init__(self, __filename=None):
        "Verifie l'existence et importe le script"
        __filename = __filename.rstrip(".py")
        if __filename is None:
            raise ValueError("The name of the file containing the variable to be imported has to be specified.")
        if not os.path.isfile(str(__filename)+".py"):
            raise ValueError("The file containing the variable to be imported doesn't seem to exist. The given file name is:\n  \"%s\""%__filename)
        self.__scriptfile = __import__(__filename, globals(), locals(), [])
        self.__scriptstring = open(__filename+".py",'r').read()
    def getvalue(self, __varname=None, __synonym=None ):
        "Renvoie la variable demandee"
        if __varname is None:
            raise ValueError("The name of the variable to be imported has to be specified.")
        if not hasattr(self.__scriptfile, __varname):
            if __synonym is None:
                raise ValueError("The imported script file doesn't contain the specified variable \"%s\"."%__varname)
            elif not hasattr(self.__scriptfile, __synonym):
                raise ValueError("The imported script file doesn't contain the specified variable \"%s\"."%__synonym)
            else:
                return getattr(self.__scriptfile, __synonym)
        else:
            return getattr(self.__scriptfile, __varname)
    def getstring(self):
        return self.__scriptstring

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
