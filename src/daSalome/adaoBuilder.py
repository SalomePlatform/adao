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
__all__ = ["NewPy"]

from daCore import AssimilationStudy

class NewPy(object):
    """
    Creation TUI d'un cas ADAO sans lien avec YACS
    """
    def __init__(self, name = ""):
        self.__adaoStudy = AssimilationStudy.AssimilationStudy( name )
        self.__dumper = _DumpLogger(name)

    def set(
            self,
            Concept              = None,
            Algorithm            = None,
            DiagonalSparseMatrix = None,
            DirectFunction       = None,
            Info                 = None,
            Matrix               = None,
            Variable             = None,
            Parameters           = None,
            ScalarSparseMatrix   = None,
            String               = None,
            Stored               = False,
            Template             = None,
            ThreeFunctions       = None,
            Vector               = None,
            VectorSerie          = None):
        "Interface unique de définition de variables d'entrées par argument"
        self.__dumper.register("set",dir(),locals(),None,True)
        try:
            if   Concept == "AlgorithmParameters":
                self.setAlgorithmParameters(Algorithm,Parameters)
            elif Concept == "Background":
                self.setBackground(Vector,VectorSerie,Stored)
            elif Concept == "Observation":
                self.setObservation(Vector,VectorSerie,Stored)
            elif Concept == "BackgroundError":
                self.setBackgroundError(Matrix,ScalarSparseMatrix,
                                        DiagonalSparseMatrix,Stored)
            elif Concept == "ObservationError":
                self.setObservationError(Matrix,ScalarSparseMatrix,
                                         DiagonalSparseMatrix,Stored)
            elif Concept == "ObservationOperator":
                self.setObservationOperator(Matrix,DirectFunction,
                                            ThreeFunctions,Parameters,Stored)
            elif Concept == "Observer":
                self.setObserver(Variable,Template,String,Info)
            else:
                raise ValueError("the variable named '%s' is not allowed."%str(Concept))
        except Exception as e:
            if type(e) == type(SyntaxError()): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError("during settings, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal."%(str(e),msg))

    def setAlgorithmParameters(
            self,
            Algorithm  = None,
            Parameters = None):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setAlgorithmParameters", dir(), locals())
        self.__adaoStudy.setAlgorithm( choice = Algorithm )
        self.__adaoStudy.setAlgorithmParameters( asDico = Parameters )

    def setBackground(
            self,
            Vector         = None,
            VectorSerie    = None,
            # Script = None, # Nom du script contenant une variable Vector/VectorSerie
            Stored         = False):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setBackground", dir(), locals())
        __Vector, __PersistentVector = Vector, VectorSerie
        #
        self.__adaoStudy.setBackground(
            asVector           = __Vector,
            asPersistentVector = __PersistentVector,
            toBeStored         = Stored,
            )

    def setObservation(
            self,
            Vector         = None,
            VectorSerie    = None,
            # Script = None, # Nom du script contenant une variable nommée
            Stored         = False):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setObservation", dir(), locals())
        __Vector, __PersistentVector = Vector, VectorSerie
        #
        self.__adaoStudy.setObservation(
            asVector           = __Vector,
            asPersistentVector = __PersistentVector,
            toBeStored         = Stored,
            )

    def setBackgroundError(
            self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            # Script       = None, # Nom du script contenant une variable nommée
            Stored               = False):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setBackgroundError", dir(), locals())
        __Covariance, __Scalar, __Vector = Matrix, ScalarSparseMatrix, DiagonalSparseMatrix
        #
        self.__adaoStudy.setBackgroundError(
            asCovariance  = __Covariance,
            asEyeByScalar = __Scalar,
            asEyeByVector = __Vector,
            toBeStored    = Stored,
            )

    def setObservationError(
            self,
            Matrix               = None,
            ScalarSparseMatrix   = None,
            DiagonalSparseMatrix = None,
            # Script       = None, # Nom du script contenant une variable nommée
            Stored               = False):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setObservationError", dir(), locals())
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
            DirectFunction = None,
            ThreeFunctions = None,
            Parameters     = None,
            # MatrixAsScript         = None, # Nom du script contenant une variable nommée
            # DirectFunctionAsScript = None, # Nom du script contenant une variable nommée
            # ThreeFunctionsAsScript = None, # Nom du script contenant une variable nommée
            Stored         = False):
        "Définition d'une entrée de calcul"
        self.__dumper.register("setObservationOperator", dir(), locals())
        __Parameters = {}
        if Parameters is not None and type(Parameters) == type({}):
            for par in ("useApproximatedDerivatives", "withCenteredDF", "withIncrement", "withmpEnabled", "withmpWorkers"):
                if Parameters.has_key(par):
                    __Parameters[par] = Parameters[par]
        __Matrix = Matrix
        if DirectFunction is not None:
            __Function = { "Direct":DirectFunction }
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

    def analyze(self):
        "Lancement du calcul"
        self.__dumper.register("analyze", dir(), locals())
        try:
            self.__adaoStudy.analyze()
        except Exception as e:
            if type(e) == type(SyntaxError()): msg = "at %s: %s"%(e.offset, e.text)
            else: msg = ""
            raise ValueError("during analyse, the following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal."%(str(e),msg))

    def get(self, Variable=None):
        "Récupération d'une sortie du calcul"
        self.__dumper.register("get",dir(),locals(),Variable)
        return self.__adaoStudy.get(Variable)

    def setObserver(
            self,
            Variable = None,
            Template = None,
            String   = None,
            Info     = None):
        "Définition d'un observateur du calcul"
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
        else:
            __FunctionText = ""
        __Function = _ObserverF(__FunctionText)
        #
        self.__adaoStudy.setDataObserver(
            VariableName   = __Variable,
            HookFunction   = __Function.getfunc(),
            HookParameters = __Info,
            )

    def dumpNormalizedCommands(self):
        "Récupération de la liste des commandes de création d'un cas"
        return self.__dumper.dump()

#     def __dir__(self):
#         # return set(self.__dict__.keys() + dir(self.__class__))
#         return [
#             'AlgorithmParameters',
#             'Background',
#             'BackgroundError',
#             'ControlInput',
#             'ControlModel',
#             'Controls',
#             'Debug',
#             'EvolutionError',
#             'EvolutionModel',
#             'InputVariables',
#             'Observation',
#             'ObservationError',
#             'ObservationOperator',
#             'Observers',
#             'OutputVariables',
#             'StudyName',
#             'StudyRepertory',
#             'UserDataInit',
#             'UserPostAnalysis',
#             '__doc__',
#             '__init__',
#             '__module__',
#             'analyze',
#             'get',
#             'prepare_to_pickle',
#             'saveAsEFICASFile',
#             ]
#
#     def UserPostAnalysis(self):
#         raise NotImplementedError()
#
#     def Controls(self):
#         raise NotImplementedError()
#
#     def StudyName(self):
#         raise NotImplementedError()
#
#     def StudyRepertory(self):
#         raise NotImplementedError()
#
#     def Debug(self):
#         raise NotImplementedError()
#
#     def EvolutionModel(self):
#         raise NotImplementedError()
#
#     def EvolutionError(self):
#         raise NotImplementedError()
#
#     def ControlModel(self):
#         raise NotImplementedError()
#
#     def ControlInput(self):
#         raise NotImplementedError()
#
#     def UserDataInit(self):
#         raise NotImplementedError()
#
#     def InputVariables(self):
#         raise NotImplementedError()
#
#     def OutputVariables(self):
#         raise NotImplementedError()
#
#     def prepare_to_pickle(self):
#         raise NotImplementedError()
#
#     def saveAsEFICASFile(self):
#         raise NotImplementedError()
#
# class NewFromYacsTemplate():
#     """
#     Creation TUI d'un cas ADAO à l'aide d'un cas YACS pré-existant
#     """
#     def __init__(self, salome_Study = None, name = ""):
#         raise NotImplementedError(NewFromYacsTemplate.__doc__)
#
# class NewYacs():
#     """
#     Creation TUI d'un cas ADAO de type YACS
#     """
#     def __init__(self, salome_Study = None, name = ""):
#         raise NotImplementedError(NewYacs.__doc__)

class _DumpLogger(object):
    """
    Conservation des commandes de création d'un cas
    """
    def __init__(self,__name="",__objname="case"):
        self.__logSerie = []
        # self.__logSerie.append("#-*-coding:iso-8859-1-*-\n#")
        # self.__logSerie.append("# Copyright (C) 2008-2015 EDF R&D\n#")
        self.__logSerie.append("#\n# Python script for ADAO\n#")
        self.__logSerie.append("from numpy import *")
        self.__logSerie.append("import adaoBuilder")
        self.__logSerie.append("%s = adaoBuilder.NewPy('%s')"%(__objname,__name))
        self.__switchoff = False
    def register(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Enregistrement d'une commande individuelle"
        if __command is not None and __keys is not None and __local is not None and not self.__switchoff:
            __text  = ""
            if __pre is not None:
                __text += "%s = "%__pre
            __text += "case.%s( "%str(__command)
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
    def dump(self,filename=None):
        "Restitution de la liste des commandes de création d'un cas"
        if filename is None:
            return "\n".join(self.__logSerie)
        else:
            fid = open(filename,"w")
            fid.writelines(self.__logSerie)
            fid.close()

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

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
