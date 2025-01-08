# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2025 EDF R&D
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D
# Author: Luis Corona Mesa-Molles, luis.corona-mesa-molles@edf.fr, EDF R&D

__all__ = ["Calibration", "name", "version", "year"]

# ==============================================================================

name     = "Modelica and Dymola Calibration Tools"
version  = "1.0.9.14.0"  # "x.x"+"adao version"
year     = "2021"

# ==============================================================================
# Default configuration
# ---------------------
import os, sys, io, shutil, time, logging, subprocess, copy, csv  # noqa: E402
import tempfile, warnings, numpy, scipy, pandas  # noqa: E402
from datetime import datetime  # noqa: E402

try:
    import adao
    from adao import adaoBuilder
    from daCore.Interfaces import ImportFromFile, ImportScalarLinesFromFile
except ImportError:
    raise ImportError("ADAO module not found, please install it first.")

try:
    from buildingspy.io.outputfile import Reader
except ImportError:
    raise ImportError("buildingspy module not found, please install it first.")

try:
    from pst4mod.modelica_libraries.automatic_simulation import Automatic_Simulation
    from pst4mod.modelica_libraries.around_simulation import Around_Simulation
    from pst4mod.modelica_libraries import write_in_dsin
    from pst4mod.modelica_libraries.change_working_point import Dict_Var_To_Fix
    from pst4mod.modelica_libraries.change_working_point import Working_Point_Modification
except ImportError:
    raise ImportError("modelica_libraries module not found, please install it first.")

try:
    from fmpy import simulate_fmu
    from fmpy.fmi1 import FMICallException
except ImportError:
    __msg = "fmpy library not found, it will not be possible for you to simulate Functional Mock-up Units (FMUs) as models. Add it to Python installation it if necessary."
    warnings.warn(__msg, ImportWarning, stacklevel=50)
except Exception:
    pass

_configuration = {
    "DirectoryModels"   : "Models",
    "DirectoryMeasures" : "Measures",
    "DirectoryMethods"  : "Methods",
    "DirectoryResults"  : "Results",
    "Launcher"          : "configuration.py",
}

# ==============================================================================
class Calibration(object):
    "ADAO case based parameters inverse estimation tools"
    def __init__(self, Name = "Calibration case", SaveStdoutIn = None, Verbose = False):
        """
        Name           : name as a string
        SaveAllStdoutIn: filename to be used for stdout stream
        Verbose        : verbose output
        """
        self.__name     = str(Name)
        self.__measures = {}
        self.__model    = {}
        self.__link     = {}
        self.__method   = {}
        self.__result   = {}
        self._setConfigurationDefaults()
        self.__verbose  = bool(Verbose)
        self.__stdoutid = sys.stdout
        if SaveStdoutIn is not None:
            sys.stdout = open(SaveStdoutIn, "w")
        if self.__verbose:
            __msg = "[VERBOSE] %s"%self.__name
            print("")
            print("  %s"%__msg)
            print("  %s"%("-" * len(__msg),))
            print("")
            VersionsLogicielles()

    def _setConfigurationDefaults(self, Configuration = None):
        """
        Impose case directory and files structure configuration defaults based
        on argument dictionary
        """
        if Configuration is None or type(Configuration) is not dict:
            Configuration = _configuration
        for __k, __v in Configuration.items():
            setattr(self, __k, __v)

    def _setModelTmpDir(self, __model_name = "dsin.txt", __model_format = "DYMOSIM", __model_dest = "dsin.txt", __before_tmp = None, __suffix=None):
        if __model_name is None:
            raise ValueError('Model file or directory has to be set and can not be None')
        elif os.path.isfile(__model_name):
            __model_nam = os.path.basename(__model_name)
            __model_dir = os.path.abspath(os.path.dirname(__model_name))
            __model_dst = __model_dest
        elif os.path.isdir(__model_name):
            __model_nam = "dsin.txt"
            __model_dir = os.path.abspath(__model_name)
            __model_dst = __model_dest
        else:
            raise ValueError('Model file or directory not found using %s'%str(__model_name))
        #
        if __before_tmp is not None:  # Mettre "../.." si nécessaire
            __mtmp = os.path.join(__model_dir, __before_tmp, "tmp")
        else:
            __mtmp = os.path.join(__model_dir, "tmp")
        if not os.path.exists(__mtmp):
            os.mkdir(__mtmp)
        __prefix = time.strftime('%Y%m%d_%Hh%Mm%Ss_tmp_', time.localtime())
        if __suffix is not None:
            __prefix = __prefix + __suffix + "_"
        __ltmp = tempfile.mkdtemp( prefix=__prefix, dir=__mtmp )
        #
        for sim, pmf, dst in (
            (__model_nam, __model_format, __model_dst),
            ("dymosim.exe", "DYMOSIM", "dymosim.exe"),
            ("pythonsim.exe", "PYSIM", "pythonsim.exe"),
            ):
            # Recherche un fichier de données ou un simulateur dans cet ordre

            if os.path.isfile(os.path.join(__model_dir, sim)) and (pmf.upper() in [__model_format, "GUESS"]):
                shutil.copy(
                    os.path.join(__model_dir, sim),
                    os.path.join(__ltmp, dst)
                )

                # _secure_copy_textfile(
                #         os.path.join(__model_dir, sim),
                #         os.path.join(__ltmp, dst)
                #         )

                break
        return __ltmp

    def _setModelTmpDir_simple(self, __model_name="dsin.txt", __model_format="DYMOSIM", __model_dest = "dsin.txt"):
        if __model_name is None:
            raise ValueError('Model file or directory has to be set and can not be None')
        elif os.path.isfile(__model_name):
            if __model_format == "OPENMODELICA": #same structure as in  the directory case
                __model_dir = os.path.abspath(os.path.dirname(__model_name))

                __model_nam_1 = os.path.basename(__model_name)
                __model_nam_2 = __model_nam_1[:-9]+'.exe'
                __model_nam = [__model_nam_1, __model_nam_2] #the first found model is kept

                __model_nam_3 = __model_nam_1[:-9]+'_info.json' #check if this file exists as well
                if os.path.exists(os.path.join(__model_dir,__model_nam_3)):
                    __model_nam.append(__model_nam_3)                      #get the three files necessar for simulation
                __model_nam_4 = __model_nam_1[:-9]+'_JacA.bin' #check if this file exists as well
                if os.path.exists(os.path.join(__model_dir,__model_nam_4)):
                    __model_nam.append(__model_nam_4)
                __model_dst = __model_nam #the same file name is kept

            else: #cas classique
                __model_nam = os.path.basename(__model_name)
                __model_dir = os.path.abspath(os.path.dirname(__model_name))
                __model_dst = os.path.basename(__model_dest)
        elif os.path.isdir(__model_name):
            if __model_format == "DYMOSIM":
                __model_nam = "dsin.txt"
                __model_dir = os.path.abspath(__model_name)
                __model_dst = os.path.basename(__model_dest)

            elif __model_format == "FMI" or __model_format == "FMU":
                __model_dir = os.path.abspath(__model_name)
                __model_nam = [files for files in os.listdir(__model_dir) if files[-4:] =='.fmu'][0] #the first found model is kept
                __model_dst = __model_nam #the same file name is kept

            elif __model_format == "OPENMODELICA":
                __model_dir = os.path.abspath(__model_name)
                __model_nam_1 = [files for files in os.listdir(__model_dir) if files[-4:] =='.xml'][0] #the first found model is kept, .xml extension is considered
                __model_nam_2 = __model_nam_1[:-9]+'.exe'
                __model_nam = [__model_nam_1, __model_nam_2] #the first found model is kept

                __model_nam_3 = __model_nam_1[:-9]+'_info.json' #check if this file exists as well
                if os.path.exists(os.path.join(__model_dir,__model_nam_3)):
                    __model_nam.append(__model_nam_3)                      #get the three files necessar for simulation
                __model_nam_4 = __model_nam_1[:-9]+'_JacA.bin' #check if this file exists as well
                if os.path.exists(os.path.join(__model_dir,__model_nam_4)):
                    __model_nam.append(__model_nam_4)
                __model_dst = __model_nam #the same file name is kept

            else :
                raise ValueError('If the model is not provided in DYMOSIM, OpenModelica or FMI format, the name of the model must refer to a file name (in a relative way with respect to the configuration file)')
        else:
            raise ValueError('Model file or directory not found using %s'%str(__model_name))
        #
        __mtmp = os.path.join(__model_dir, "tmp")
        if not os.path.exists(__mtmp):
            os.mkdir(__mtmp)
        __ltmp = __mtmp
        #
        if type(__model_nam) == list: #it means that it is an OpenModelica model
            for sim_element in __model_nam:
                shutil.copy(
                    os.path.join(__model_dir, sim_element),
                    os.path.join(__ltmp, sim_element) #the same name is kept for the files
                    )
        else:
            for sim, pmf, dst in (
                (__model_nam,__model_format,__model_dst),
                ("dsin.txt","DYMOSIM","dsin.txt"),
                ("pythonsim.exe","PYSIM","pythonsim.exe"),
                ):
                # Recherche un fichier de données ou un simulateur dans cet ordre
                if os.path.isfile(os.path.join(__model_dir, sim)) and (pmf.upper() in [__model_format, "GUESS"]):

                    shutil.copy(
                        os.path.join(__model_dir, sim),
                        os.path.join(__ltmp, dst)
                        )
                    # _secure_copy_textfile(
                    #         os.path.join(__model_dir, sim),
                    #         os.path.join(__ltmp, dst)
                    #         )

                    break
        return __ltmp

    def _get_Name_ModelTmpDir_simple(self, __model_name="dsin.txt"):
        if __model_name is None:
            raise ValueError('Model file or directory has to be set and can not be None')
        elif os.path.isfile(__model_name):
            __model_dir = os.path.abspath(os.path.dirname(__model_name))
        elif os.path.isdir(__model_name):
            __model_dir = os.path.abspath(__model_name)
        else:
            raise ValueError('Model file or directory not found using %s'%str(__model_name))
        #
        __mtmp = os.path.join(__model_dir, "tmp")
        __ltmp = __mtmp
        return __ltmp

    def _setModelTmpDir_REF_CALCULATION(self, __model_name="dsin.txt", __model_format="DYMOSIM", __suffix=None, __model_dest = "dsin.txt"):
        if __model_name is None:
            raise ValueError('Model file or directory has to be set and can not be None')
        elif os.path.isfile(__model_name):
            __model_dir = os.path.abspath(os.path.dirname(__model_name))
            __model_nam = os.path.basename(__model_name)
        elif os.path.isdir(__model_name):
            __model_dir = os.path.abspath(__model_name)
            __model_nam = "dsin.txt"
        else:
            raise ValueError('Model file or directory not found using %s'%str(__model_name))
        if __suffix is None:
            raise ValueError('Observation files must be named')
        #
        __mtmp = os.path.join(__model_dir, "tmp")
        if not os.path.exists(__mtmp):
            os.mkdir(__mtmp)
        for sim, pmf in ((__model_nam,__model_format), ("dymosim.exe","DYMOSIM"), ("pythonsim.exe","PYSIM")):
            # Recherche un simulateur dans cet ordre
            if os.path.isfile(os.path.join(__model_dir, sim)) and (pmf.upper() in [__model_format, "GUESS"]):
                __pref = time.strftime('%Y%m%d_%Hh%Mm%Ss_REF_CALCULATION_',time.localtime())
                if __suffix is not None:
                    __pref = __pref+__suffix+"_"
                __ltmp = tempfile.mkdtemp( prefix=__pref, dir=__mtmp )
                shutil.copy(
                    os.path.join(__model_dir, sim),
                    os.path.join(__ltmp, __model_dest)
                    )
                # _secure_copy_textfile(
                #         os.path.join(__model_dir, sim),
                #         os.path.join(__ltmp, __model_dest)
                #         )

                __ok = True
                break
            else:
                __ok = False
        if not __ok:
            raise ValueError("Model simulator not found using \"%s\" path and \"%s\" format"%(__model_name,__model_format))
        return __ltmp

    def describeMeasures(self, SourceName, Variables, Format="Guess"):
        "To store description of measures"
        self.__measures["SourceName"] = str(SourceName) # File or data name
        self.__measures["Variables"]  = tuple(Variables) # Name of variables
        self.__measures["Format"]     = str(Format) # File or data format
        if self.__verbose: print("  [VERBOSE] Measures described")
        return self.__measures

    def describeMultiMeasures(self, SourceNames, Variables, Format="Guess"):
        "To store description of measures"
        self.__measures["SourceName"] = tuple(SourceNames) # List of file or data name
        self.__measures["Variables"]  = tuple(Variables) # Name of variables
        self.__measures["Format"]     = str(Format) # File or data format
        if self.__verbose: print("  [VERBOSE] Measures described")
        return self.__measures

    def describeModel(self, SourceName, VariablesToCalibrate, OutputVariables, Format="Guess"):
        "To store description of model"
        self.__model["SourceName"]           = str(SourceName) # Model command file
        self.__model["VariablesToCalibrate"] = tuple(VariablesToCalibrate) # Name of variables
        self.__model["OutputVariables"]      = tuple(OutputVariables) # Name of variables
        self.__model["Format"]               = str(Format) # File or model format
        if os.path.isfile(SourceName):
            self.__model["Verbose_printing_name"] = os.path.basename(SourceName)
        elif os.path.isdir(SourceName):
            if self.__model["Format"] == "DYMOSIM":
                self.__model["Verbose_printing_name"] = "dsin.txt + dymosim.exe in " + os.path.basename(SourceName)
            elif self.__model["Format"] == "FMI" or self.__model["Format"] == "FMU":
                self.__model["Verbose_printing_name"] = [files for files in os.listdir(os.path.abspath(SourceName)) if files[-4:] =='.fmu'][0]
            elif self.__model["Format"] == "OPENMODELICA":
                xml_file_name = [files for files in os.listdir(os.path.abspath(SourceName)) if files[-4:] =='.xml'][0]
                exe_file_name = xml_file_name[:-9] + '.exe'
                json_file_name = xml_file_name[:-9] + '_info.json'
                if os.path.exists(os.path.join(os.path.abspath(SourceName),json_file_name)):
                    self.__model["Verbose_printing_name"] = xml_file_name + ' ' + exe_file_name + ' ' + json_file_name
                else:
                    self.__model["Verbose_printing_name"] = xml_file_name + ' ' + exe_file_name + ' '
            else:
                print("  [VERBOSE] Model described: ", "/!\\ Unknown ModelFormat /!\\ ")
                exit()
        if self.__verbose: print("  [VERBOSE] Model described: ", self.__model["Verbose_printing_name"] )
        return self.__model

    def describeLink(self, MeasuresNames, ModelName, LinkName, LinkVariable, Format="Guess"):
        "To store description of link between measures and model input data"
        self.__link["SourceName"]    = str(LinkName) # File or link name
        self.__link["MeasuresNames"] = tuple(MeasuresNames) # List of file or name
        self.__link["ModelName"]     = tuple(ModelName) # File or model name
        self.__link["Variable"]      = str(LinkVariable) # Name of variable names column
        self.__link["Format"]        = str(Format) # File or model format
        if self.__verbose: print("  [VERBOSE] Link between model and multiple measures described")
        return self.__link

    def describeMethod(self, SourceName, MethodFormat="PY", BackgroundName=None, BackgroundFormat="Guess"):
        "To store description of calibration method"
        self.__method["SourceName"]       = str(SourceName) # File or method name
        self.__method["Format"]           = str(MethodFormat) # File or model format
        self.__method["BackgroundName"]   = str(BackgroundName) # File or background name
        self.__method["BackgroundFormat"] = str(BackgroundFormat) # File or model format
        if self.__verbose: print("  [VERBOSE] Optimization method settings described")
        return self.__method

    def describeResult(self, ResultName, Level=None, Format="TXT"):
        "To store description of results"
        self.__result["SourceName"] = str(ResultName) # File or method name
        self.__result["Level"]      = str(Level) # Level = "Final", "IntermediaryFinal"
        self.__result["Format"]     = str(Format) # File or model format
        if self.__verbose: print("  [VERBOSE] Results settings described")
        return self.__result

    def calibrate(self,
            ModelName            = None, # Model command file
            ModelFormat          = "Guess",
            DataName             = None, # Measures
            DataFormat           = "Guess",
            BackgroundName       = None, # Background
            BackgroundFormat     = "Guess",
            MethodName           = None, # Assimilation
            MethodFormat         = "Guess",
            VariablesToCalibrate = None,
            OutputVariables      = None,
            ResultName           = "results.txt", # Results
            ResultFormat         = "Guess",
            ResultLevel          = None,
            Verbose              = False,
            ):
        """
        General method to set and realize a calibration (optimal estimation
        task) of model parameters using measures data.
        """
        if Verbose:
            self.__verbose = True
            print("  [VERBOSE] Verbose mode activated")
        else:
            self.__verbose = False
        if DataName is not None:
            # On force l'utilisateur à nommer dans son fichier de mesures
            # les variables avec le même nom que des sorties dans le modèle
            self.describeMeasures(DataName, OutputVariables, DataFormat)
        if ModelName is not None:
            self.describeModel(ModelName, VariablesToCalibrate, OutputVariables, ModelFormat)
        if MethodName is not None:
            self.describeMethod(MethodName, MethodFormat, BackgroundName, BackgroundFormat)
        if ResultName is not None:
            self.describeResult(ResultName, ResultLevel, ResultFormat)
        #
        ONames, Observations = _readMeasures(
            self.__measures["SourceName"],
            self.__measures["Variables"],
            self.__measures["Format"],
            )
        Algo, Params, CovB, CovR = _readMethod(
            self.__method["SourceName"],
            self.__method["Format"],
            )
        __bgfile = None
        if self.__method["BackgroundFormat"] == "DSIN":  __bgfile = self.__model["SourceName"]
        if self.__method["BackgroundFormat"] == "ADAO":  __bgfile = self.__method["SourceName"]
        if self.__method["BackgroundFormat"] == "USER":  __bgfile = self.__method["BackgroundName"]
        if self.__method["BackgroundFormat"] == "Guess":
            if self.__method["BackgroundName"] is not None: __bgfile = self.__method["BackgroundName"]
            if self.__method["SourceName"] is not None:     __bgfile = self.__method["SourceName"]
            if self.__model["SourceName"] is not None:      __bgfile = self.__model["SourceName"]
        BNames, Background, Bounds = _readBackground(
            __bgfile,
            self.__model["VariablesToCalibrate"],
            self.__method["BackgroundFormat"],
            )
        if "Bounds" not in Params: # On force la priorité aux bornes utilisateur
            Params["Bounds"] = Bounds
        if self.__verbose:
            print("  [VERBOSE] Measures read")
            print("  [VERBOSE] Optimization information read")
            if "MaximumNumberOfSteps" in Params:
                print("  [VERBOSE] Maximum possible number of iteration:",Params['MaximumNumberOfSteps'])
            print("  [VERBOSE] Background read:",Background)
            __v = Params['Bounds']
            if isinstance(__v, (numpy.ndarray, numpy.matrix, list, tuple)):
                __v = numpy.array(__v).astype('float')
                __v = numpy.where(numpy.isnan(__v), None, __v)
                __v = __v.tolist()
            print("  [VERBOSE] Bounds read:",__v)
        #
        if "DifferentialIncrement" not in Params:
            Params["DifferentialIncrement"] = 0.001
        if "StoreSupplementaryCalculations" not in Params:
            Params["StoreSupplementaryCalculations"] = ["SimulatedObservationAtOptimum",]
        if "StoreSupplementaryCalculations" in Params and \
            "SimulatedObservationAtOptimum" not in Params["StoreSupplementaryCalculations"]:
            Params["StoreSupplementaryCalculations"].append("SimulatedObservationAtOptimum")
        if self.__verbose and "StoreSupplementaryCalculations" in Params and \
            "CurrentOptimum" not in Params["StoreSupplementaryCalculations"]:
            Params["StoreSupplementaryCalculations"].append("CurrentOptimum")
        if self.__verbose and "StoreSupplementaryCalculations" in Params and \
            "CostFunctionJAtCurrentOptimum" not in Params["StoreSupplementaryCalculations"]:
            Params["StoreSupplementaryCalculations"].append("CostFunctionJAtCurrentOptimum")
        #
        def exedymosim( x_values_matrix ):
            "Appel du modèle et restitution des résultats"
            from buildingspy.io.outputfile import Reader
            from pst4mod.modelica_libraries.automatic_simulation import Automatic_Simulation
            #
            # x_values = list(numpy.ravel(x_values_matrix) * Background)
            x_values = list(numpy.ravel(x_values_matrix))
            dict_inputs=dict(zip(VariablesToCalibrate,x_values))
            # if Verbose: print("  Simulation for %s"%numpy.ravel(x_values))
            #
            simudir = self._setModelTmpDir(ModelName, ModelFormat)
            auto_simul = Automatic_Simulation(
                simu_dir=simudir,
                dict_inputs=dict_inputs,
                logfile=True,
                timeout=60,
                without_modelicares=True) #linux=true is removed
            auto_simul.single_simulation()
            reader = Reader(os.path.join(simudir,'dsres.mat'),'dymola')
            y_values = [reader.values(y_name)[1][-1] for y_name in OutputVariables]
            y_values_matrix = numpy.asarray(y_values)
            if not Verbose:
                shutil.rmtree(simudir, ignore_errors=True)
            return y_values_matrix
        #
        def exepython( x_values_matrix ):
            "Appel du modèle et restitution des résultats"
            # x_values = list(numpy.ravel(x_values_matrix))
            # dict_inputs=dict(zip(VariablesToCalibrate,x_values))
            #
            simudir = self._setModelTmpDir(ModelName, ModelFormat)
            auto_simul = Python_Simulation(
                simu_dir=simudir,
                val_inputs=x_values_matrix,
                logfile=True,
                timeout=60,
                verbose=self.__verbose)
            y_values_matrix = auto_simul.single_simulation()
            if not Verbose:
                shutil.rmtree(simudir, ignore_errors=True)
            return y_values_matrix
        #
        if self.__model["Format"].upper() in ["DYMOSIM", "GUESS"]:
            simulateur = exedymosim
        elif self.__model["Format"].upper() == "PYSIM":
            simulateur = exepython
        else:
            raise ValueError("Unknown model format \"%s\""%self.__model["Format"].upper())
        #
        __adaocase = adaoBuilder.New()
        __adaocase.set( 'AlgorithmParameters',  Algorithm=Algo, Parameters=Params )
        __adaocase.set( 'Background',           Vector=Background)
        __adaocase.set( 'Observation',          Vector=Observations )
        if type(CovB) is float:
            __adaocase.set( 'BackgroundError',  ScalarSparseMatrix=CovB )
        else:
            __adaocase.set( 'BackgroundError',  Matrix=CovB )
        if type(CovR) is float:
            __adaocase.set( 'ObservationError', ScalarSparseMatrix=CovR )
        else:
            __adaocase.set( 'ObservationError', Matrix=CovR )
        __adaocase.set( 'ObservationOperator',  OneFunction=simulateur, Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]} )
        if self.__verbose:
            __adaocase.set( 'Observer', Variable="CostFunctionJAtCurrentOptimum", String="print('\\n  -----------------------------------\\n  [VERBOSE] Current iteration: %i'%(len(var),))" )
            __adaocase.set( 'Observer', Variable="CostFunctionJAtCurrentOptimum", Template="ValuePrinter", Info="\n  [VERBOSE] Current best cost value:" )
            __adaocase.set( 'Observer', Variable="CurrentOptimum",                Template="ValuePrinter", Info="\n  [VERBOSE] Current optimal state..:" )
        __adaocase.execute()
        #
        __resultats = dict(
            InitialParameters = numpy.asarray(Background),
            OptimalParameters = __adaocase.get("Analysis")[-1], # * Background,
            OptimalSimulation = __adaocase.get("SimulatedObservationAtOptimum")[-1],
            Measures          = Observations,
            NamesOfParameters = BNames,
            NamesOfMeasures   = ONames,
            )
        if self.__verbose: print("")
        del __adaocase
        #
        _saveResults(
            __resultats,
            self.__result["SourceName"],
            self.__result["Level"],
            self.__result["Format"],
            self.__verbose,
            )
        #
        return __resultats



    def calibrateMultiObs(self,
            ModelName            = None, # Model command file
            ModelFormat          = "Guess",
            DataNames            = None, # Multiple measures
            DataFormat           = "Guess",
            LinkName             = None, # CL with data names
            LinkVariable         = "Variable", # Name of variable names column
            LinkFormat           = "Guess",
            BackgroundName       = None, # Background
            BackgroundFormat     = "Guess",
            MethodName           = None, # Assimilation
            MethodFormat         = "Guess",
            VariablesToCalibrate = None,
            OutputVariables      = None,
            ResultName           = "results.txt", # Results
            ResultFormat         = "Guess",
            ResultLevel          = None,
            Verbose              = False,
            IntermediateInformation = False,
            ComplexModel         = False,
            FMUInput             = None,
            NeedInitVariables         = False,
            KeepCalculationFolders = False,
            Linux = False,
            CreateOptimaldsin = False,
            InitialSimulation = False,
            VerifyFunction = False,
            GlobalSensitivityCheck = False,
            ParamSensitivityCheck = False,
            CreateCSVoutputResults = False,
            AdaptObservationError = False,
            ResultsSummary = False,
            AdvancedDebugModel = False,
            TimeoutModelExecution = 300,
            ModelStabilityCheck = False,
            ModelStabilityCheckingPoints = 10
            ):
        """
        General method to set and realize a calibration (optimal estimation
        task) of model parameters using multiple measures data, with an
        explicit link between measures and data for the model.
        """
        if Verbose:
            self.__verbose = True
            print("  [VERBOSE] Verbose mode activated")
        if IntermediateInformation:
            if self.__verbose:
                self.__IntermediateInformation = True
                print("  [VERBOSE] IntermediateInformation provided")
            else:
                self.__IntermediateInformation = False
                print("  [VERBOSE] IntermediateInformation requires Verbose mode activated")
        else:
            self.__IntermediateInformation = False

        if TimeoutModelExecution < 0:
            raise ValueError("TimeoutModelExecution must be positive")

        if DataNames is not None:
            # On force l'utilisateur à nommer dans son fichier de mesures
            # les variables avec le même nom que des sorties dans le modèle
            self.describeMultiMeasures(DataNames, OutputVariables, DataFormat)
        #
        if self.__verbose:
            print("  [VERBOSE] Timeoout for model execution is:", TimeoutModelExecution, "seconds")
        #
        if ModelFormat is not None: #included sot that the model format is allways in upper format
            ModelFormat = ModelFormat.upper()
            if ModelFormat == "DYMOLA": #to handle situations in which name Dymola is indicated
                ModelFormat = "DYMOSIM"
        if ModelName is not None:
            self.describeModel(ModelName, VariablesToCalibrate, OutputVariables, ModelFormat)
        if LinkName is not None:
            # On force l'utilisateur à utiliser les fichiers de mesures requis
            # et non pas tous ceux présents dans le Link
            self.describeLink(DataNames, ModelName, LinkName, LinkVariable, LinkFormat)
        if MethodName is not None:
            self.describeMethod(MethodName, MethodFormat, BackgroundName, BackgroundFormat)
        if ResultName is not None:
            self.describeResult(ResultName, ResultLevel, ResultFormat)
        #
        #handling of the new option for complex models while keeping the previous key word in the code
        if ComplexModel:
            print(" The option ComplexModel  is deprecated and has to be replaced by NeedInitVariables. Please update your code.")
            NeedInitVariables = ComplexModel
        ComplexModel = NeedInitVariables
       #

        ONames, Observations = _readMultiMeasures(
            self.__measures["SourceName"],
            self.__measures["Variables"],
            self.__measures["Format"],
            )


        Algo, Params, CovB, CovR = _readMethod(
            self.__method["SourceName"],
            self.__method["Format"],
            )
        __bgfile = None
        if self.__method["BackgroundFormat"] == "DSIN":  __bgfile = self.__model["SourceName"]
        if self.__method["BackgroundFormat"] == "ADAO":  __bgfile = self.__method["SourceName"]
        if self.__method["BackgroundFormat"] == "USER":  __bgfile = self.__method["BackgroundName"]
        if self.__method["BackgroundFormat"] == "Guess":
            if self.__method["BackgroundName"] is not None: __bgfile = self.__method["BackgroundName"]
            if self.__method["SourceName"] is not None:     __bgfile = self.__method["SourceName"]
            if self.__model["SourceName"] is not None:      __bgfile = self.__model["SourceName"]
        BNames, Background, Bounds = _readBackground(
            __bgfile,
            self.__model["VariablesToCalibrate"],
            self.__method["BackgroundFormat"],
            )
        if "Bounds" not in Params: # On force la priorité aux bornes utilisateur
            Params["Bounds"] = Bounds
        LNames, LColumns, LVariablesToChange = _readLink(
            self.__link["SourceName"],
            self.__link["MeasuresNames"],
            self.__link["Variable"],
            self.__link["Format"],
            )
        if self.__verbose:
            print("  [VERBOSE] Measures read")
            print("  [VERBOSE] Links read")
            print("  [VERBOSE] Optimization information read")
            print("  [VERBOSE] Background read:",Background)
            __v = Params['Bounds']
            if isinstance(__v, (numpy.ndarray, numpy.matrix, list, tuple)):
                __v = numpy.array(__v).astype('float')
                __v = numpy.where(numpy.isnan(__v), None, __v)
                __v = __v.tolist()
            print("  [VERBOSE] Bounds read:",__v)
        #
        if "DifferentialIncrement" not in Params:
            Params["DifferentialIncrement"] = 0.001
        if "EnableMultiProcessing" not in Params:
            Params["EnableMultiProcessing"] = 0
        if "NumberOfProcesses" not in Params:
            Params["NumberOfProcesses"] = 0
        if "StoreSupplementaryCalculations" not in Params:
            Params["StoreSupplementaryCalculations"] = ["SimulatedObservationAtOptimum",]
        if "StoreSupplementaryCalculations" in Params and \
            "SimulatedObservationAtOptimum" not in Params["StoreSupplementaryCalculations"]:
            Params["StoreSupplementaryCalculations"].append("SimulatedObservationAtOptimum")
        if self.__verbose and "StoreSupplementaryCalculations" in Params and \
            "CurrentOptimum" not in Params["StoreSupplementaryCalculations"]:
            Params["StoreSupplementaryCalculations"].append("CurrentOptimum")
        if self.__verbose and "StoreSupplementaryCalculations" in Params and \
            "CostFunctionJAtCurrentOptimum" not in Params["StoreSupplementaryCalculations"]:
            Params["StoreSupplementaryCalculations"].append("CostFunctionJAtCurrentOptimum")

        dict_dsin_path_ref ={} #creation of the dict_dsin_ref (for storing the path of the dsfinal file for each dataset
        #

        VariablesToCalibrate = list(BNames)

        def exedymosimMultiobs_REF_CALCULATION( x_values_matrix, dict_dsin_paths = dict_dsin_path_ref): #2ème argument à ne pas modifier
            "Appel du modèle et restitution des résultats"

            x_values = list(numpy.ravel(x_values_matrix))
            x_inputs = dict(zip(VariablesToCalibrate,x_values))
            dict_inputs_for_CWP = {}

#            multi_y_values_matrix = []
            for etat in range(len(LNames)):
                simudir = self._setModelTmpDir_REF_CALCULATION(ModelName, ModelFormat, LNames[etat])

                try: #to handle situations in which there is only one CL (boundary conditions) file
                    var_int = numpy.ravel(LColumns[:,etat])
                except Exception:
                    var_int = numpy.ravel(LColumns)
                dict_inputs = dict(zip(LVariablesToChange, var_int))

                dict_inputs.update( x_inputs )

                auto_simul = Automatic_Simulation(
                    simu_dir=simudir,
                    dymosim_path = os.path.join(simudir, os.pardir, os.pardir) ,
                    dsres_path = os.path.join(simudir, str("dsres" +LNames[etat]+ ".mat")),
                    dict_inputs=dict_inputs,
                    logfile=True,
                    timeout=TimeoutModelExecution,
                    without_modelicares=True,
                    linux = Linux)
                auto_simul.single_simulation()



                if AdvancedDebugModel:
                    dslog_file = os.path.join(simudir, 'dslog.txt')
                    debug_model_file = os.path.join(simudir, os.pardir, 'log_debug_model.txt')
                    try:
                        shutil.copy(dslog_file,debug_model_file)
                    except Exception:
                        pass

                if auto_simul.success_code == 2 :
                    raise ValueError("The simulation falis after initialization, please check the log file and your model in order to be sure that the whole simulation can be performed (specially for dynamic models)")

                if auto_simul.success_code == 3 :
                    raise ValueError("The simulation did not reach the final time, probably due to a lack of time, please increase the time for model execution by modifying the TimeoutModelExecution value in configuration.py")

                if auto_simul.success_code == 0:

                    path_around_simu_no_CWP = os.path.join(simudir, os.pardir, os.pardir)
                    around_simu_no_CWP = Around_Simulation(dymola_version='2012',
                                      curdir=path_around_simu_no_CWP,
                                      source_list_iter_var = 'from_dymtranslog',
                                      copy_from_dym_trans_log= os.path.join(path_around_simu_no_CWP,'ini.txt'),
                                      mat = os.path.join(simudir, str("dsres" +LNames[etat]+ ".mat")),
                                      iter_var_values_options={'source':'from_mat', 'moment':'initial'},
                                      verbose = False)
                    around_simu_no_CWP.set_list_iter_var()
                    around_simu_no_CWP.set_dict_iter_var()

                    writer_no_CWP = write_in_dsin.Write_in_dsin(dict_inputs =around_simu_no_CWP.dict_iter_var,filedir=simudir,dsin_name='dsin.txt',old_file_name='old_dsin.txt',new_file_name=str("dsin_updated_" +LNames[etat]+ ".txt"))
                    writer_no_CWP.write_in_dsin
                    writer_no_CWP.write_in_dsin()

                    dict_dsin_paths[LNames[etat]] = os.path.join(simudir,str("dsin_updated_" +LNames[etat]+ ".txt"))

                else:
                    from pst4mod.modelica_libraries.change_working_point import Dict_Var_To_Fix
                    from pst4mod.modelica_libraries.change_working_point import Working_Point_Modification

                    path_around_simu = os.path.join(simudir,os.path.pardir,os.path.pardir)

                    if not(os.path.exists(os.path.join(path_around_simu, str("ref" + ".mat")))):
                                        auto_simul_ref = Automatic_Simulation(
                                                                        simu_dir=path_around_simu,
                                                                        dymosim_path = os.path.join(simudir, os.pardir, os.pardir) ,
                                                                        dict_inputs={},
                                                                        logfile=True,
                                                                        dsres_path = os.path.join(path_around_simu, str("ref" + ".mat")),
                                                                        timeout=TimeoutModelExecution,
                                                                        without_modelicares=True,
                                                                        linux = Linux)
                                        auto_simul_ref.single_simulation()

                                        if not(auto_simul_ref.success_code == 0):
                                            raise ValueError("A working dsin.txt file must be provided, provide a dsin.txt that makes it possible for the initial simulation to converge")

                                        temporary_files_to_remove = [os.path.join(path_around_simu,'dsfinal.txt'),
                                                                     os.path.join(path_around_simu,'dsin_old.txt'),
                                                                     os.path.join(path_around_simu,'dslog.txt'),
                                                                     os.path.join(path_around_simu,'status'),
                                                                     os.path.join(path_around_simu,'success')
                                                                     ]
                                        for path_to_remove in temporary_files_to_remove:
                                            if os.path.exists(path_to_remove):
                                                os.remove(path_to_remove)

                    around_simu = Around_Simulation(dymola_version='2012',
                                      curdir=path_around_simu,
                                      source_list_iter_var = 'from_dymtranslog',
                                      copy_from_dym_trans_log= os.path.join(path_around_simu,'ini.txt'),
                                      mat = os.path.join(path_around_simu, str("ref" + ".mat")),
                                      iter_var_values_options={'source':'from_mat'},
                                      verbose = False)
                    around_simu.set_list_iter_var()
                    around_simu.set_dict_iter_var()

                    reader_CWP = Reader(os.path.join(path_around_simu, str("ref" + ".mat")),'dymola')
                    x_values_intemediary = [reader_CWP.values(x_name)[1][-1] for x_name in VariablesToCalibrate]
                    x_values_from_ref_calculation = numpy.asarray(x_values_intemediary)
                    x_inputs_from_ref_calculation = dict(zip(VariablesToCalibrate,x_values_from_ref_calculation))

                    cl_values_intemediary = [reader_CWP.values(cl_name)[1][-1] for cl_name in LVariablesToChange]
                    cl_values_from_ref_calculation = numpy.asarray(cl_values_intemediary)
                    cl_inputs_from_ref_calculation = dict(zip(LVariablesToChange,cl_values_from_ref_calculation))


                    for var_calib in x_inputs_from_ref_calculation.keys():
                        dict_inputs_for_CWP[var_calib] = (x_inputs_from_ref_calculation[var_calib], x_inputs[var_calib])

                    try: #to handle situations in which there is only one CL (boundary conditions) file
                        var_int = numpy.ravel(LColumns[:,etat])
                    except Exception:
                        var_int = numpy.ravel(LColumns)

                    dict_inputs = dict(zip(LVariablesToChange, var_int))

                    for var_cl in cl_inputs_from_ref_calculation.keys():
                        dict_inputs_for_CWP[var_cl] = (cl_inputs_from_ref_calculation[var_cl], dict_inputs[var_cl])

                    dict_var_to_fix2 = Dict_Var_To_Fix(option='automatic',
                                          dict_auto_var_to_fix=dict_inputs_for_CWP)

                    dict_var_to_fix2.set_dict_var_to_fix()

                    if Verbose:
                        LOG_FILENAME = os.path.join(simudir,'change_working_point.log')
                        for handler in logging.root.handlers[:]:
                            logging.root.removeHandler(handler)
                        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode='w')

                    working_point_modif = Working_Point_Modification(main_dir = simudir,
                                 simu_material_dir = simudir,
                                 dymosim_path = os.path.join(simudir, os.pardir, os.pardir),
                                 simu_dir = 'SIMUS',
                                 store_res_dir = 'RES',
                                 dict_var_to_fix = dict_var_to_fix2.dict_var_to_fix,
                                 around_simulation0 = around_simu,
                                 var_to_follow_path= os.path.join(simudir,'var_to_follow.csv'),
                                 gen_scripts_ini= False,
                                 nit_max= 1000000000000000,
                                 min_step_val = 0.00000000000005,
                                 timeout = TimeoutModelExecution,
                                 linux = Linux)

                    working_point_modif.create_working_directory()
                    working_point_modif.working_point_modification(skip_reference_simulation=True)

                    if AdvancedDebugModel:
                        dslog_file = os.path.join(simudir, 'SIMUS', 'dslog.txt')
                        debug_model_file = os.path.join(simudir, os.pardir, 'log_debug_model.txt')
                        try:
                            shutil.copy(dslog_file,debug_model_file)
                        except Exception:
                            pass

                    if not(os.path.exists(os.path.join(simudir, 'RES','1.0.mat'))):
                        raise ValueError(str("Simulation with Background values does not converge automatically, try to give a dsin.txt file that makes it possible to run a simulation with boundary conditions of " + LNames[etat]))

                    shutil.copy(
                        os.path.join(simudir, 'RES','1.0.mat'),
                        os.path.join(simudir, str("dsres" +LNames[etat]+ ".mat"))
                        )

                    path_around_simu_after_CWP = os.path.join(simudir,os.path.pardir,os.path.pardir)
                    around_simu_after_CWP = Around_Simulation(dymola_version='2012',
                                      curdir=path_around_simu_after_CWP,
                                      source_list_iter_var = 'from_dymtranslog',
                                      copy_from_dym_trans_log= os.path.join(path_around_simu_after_CWP,'ini.txt'),
                                      mat = os.path.join(simudir, 'RES','1.0.mat'),  #Le fichier .mat qui vient d'être créé et pour lequel on atteint les valeurs cibles de la variable
                                      iter_var_values_options={'source':'from_mat', 'moment':'initial'},
                                      verbose = False)
                    around_simu_after_CWP.set_list_iter_var()
                    around_simu_after_CWP.set_dict_iter_var()

                    writer_after_CWP = write_in_dsin.Write_in_dsin(dict_inputs =around_simu_after_CWP.dict_iter_var,filedir=os.path.join(simudir, 'SIMUS'),dsin_name='dsin.txt',old_file_name='old_dsin.txt',new_file_name='dsin_updated.txt')
                    writer_after_CWP.write_in_dsin
                    writer_after_CWP.write_in_dsin()

                    shutil.copy(
                        os.path.join(simudir, 'SIMUS','dsin_updated.txt'),
                        os.path.join(simudir, str("dsin_updated_" +LNames[etat]+ ".txt"))
                        )
                    dict_dsin_paths[LNames[etat]] = os.path.join(simudir,str("dsin_updated_" +LNames[etat]+ ".txt"))

                os.rename(
                os.path.join(os.path.dirname(dict_dsin_paths[LNames[etat]]), str("dsres" +LNames[etat]+ ".mat")),
                os.path.join(os.path.dirname(dict_dsin_paths[LNames[etat]]), str("REF_for_CWP" + ".mat"))
                        )

            return



        def preparation_exedymosimMultiobs_simple():
            from pst4mod.modelica_libraries import write_in_dsin

            for etat in range(len(LNames)):
                simudir = self._setModelTmpDir_simple(ModelName, ModelFormat, str("dsin_" +LNames[etat]+ ".txt"))
                #
                try: #to handle situations in which there is only one CL (boundary conditions) file
                    var_int = numpy.ravel(LColumns[:,etat])
                except Exception:
                    var_int = numpy.ravel(LColumns)
                dict_inputs = dict(zip(LVariablesToChange, var_int))
                writer_no_CWP = write_in_dsin.Write_in_dsin(dict_inputs = dict_inputs, filedir=simudir, dsin_name=str("dsin_" +LNames[etat]+ ".txt"), old_file_name='old_dsin.txt',new_file_name = str("dsin_" +LNames[etat]+ ".txt"))
                writer_no_CWP.write_in_dsin
                writer_no_CWP.write_in_dsin()
            return

        def preparation_exefmu_om_Multiobs():
            self._setModelTmpDir_simple(ModelName, ModelFormat, ModelName)

        def exepythonMultiobs( x_values_matrix ):
            "Appel du modèle et restitution des résultats"
            #
            x_values = list(numpy.ravel(x_values_matrix))
            x_inputs = dict(zip(VariablesToCalibrate,x_values))
            #
            multi_y_values_matrix = []
            for etat in range(len(LNames)):
                simudir = self._setModelTmpDir(ModelName, ModelFormat)
                #
                dict_inputs = dict(zip(LVariablesToChange, numpy.ravel(LColumns[:,etat])))
                dict_inputs.update( x_inputs )
                #
                auto_simul = Python_Simulation(
                    simu_dir=simudir,
                    val_inputs=x_values_matrix,
                    logfile=True,
                    timeout=TimeoutModelExecution,
                    verbose=self.__verbose)
                y_values_matrix = auto_simul.single_simulation()
                multi_y_values_matrix.append( y_values_matrix )
            if not Verbose:
                shutil.rmtree(simudir, ignore_errors=True)
            y_values_matrix = numpy.ravel(numpy.array(multi_y_values_matrix))
            return y_values_matrix
        #


        #Test for output variables - not repetition  - This test must be before the redefinition of OutputVariables
        OutputVariables_set = set(OutputVariables)
        if len(OutputVariables) != len(OutputVariables_set):
            diff_number_values = len(OutputVariables) - len(OutputVariables_set)
            raise ValueError("There are " + str(diff_number_values) + " repeated output variables in the definition of OutputVariables, please remove repeated names.")

        #Handle several times same obs -START
        OutputVariables_new_tmp = []

        whole_obs_in_fileobs = readObsnamesfile(self.__measures["SourceName"])

        for outputname in OutputVariables:
            if outputname not in whole_obs_in_fileobs:
                print("  [VERBOSE] /!\\ ", outputname," is not defined in the measurements file")
        for obsname in whole_obs_in_fileobs:
            if obsname in OutputVariables:
                OutputVariables_new_tmp.append(obsname)

        OutputVariables_new = []
        for obs_name in OutputVariables: #to get the same order as for measures
            count_obs_name = OutputVariables_new_tmp.count(obs_name)
            for i in range(count_obs_name):
                OutputVariables_new.append(obs_name)
        OutputVariables = OutputVariables_new

        ONames = OutputVariables
        #Handle several times same obs - END


        ODates,OHours = readMultiDatesHours(self.__measures["SourceName"])

        List_Multideltatime =[]

        for etat in range(len(ODates)):
            time_initial = datetime.strptime(ODates[etat][0]+ ' ' + OHours[etat][0], '%d/%m/%Y %H:%M:%S')
            list_deltatime = []

            if len(ODates[etat])>1:
                list_deltatime.append(0)
                for index_tmp in range(len(ODates[etat])-1): #the first date is considered as reference
                    time_index_tmp = datetime.strptime(ODates[etat][index_tmp+1] + ' ' + OHours[etat][index_tmp+1], '%d/%m/%Y %H:%M:%S')
                    list_deltatime.append((time_index_tmp-time_initial).total_seconds())

                    if (time_index_tmp-time_initial).total_seconds() < 0:
                         raise ValueError('The initial date is not chronological for state %s'%str(etat))

            List_Multideltatime.append(list_deltatime)


        #Bricolage Debut
        Observations_new =[]
        number_observations_by_cl = [] #to be used in the test function, number of measurements by boundary condition (i.e. number of lines in the measurements file)

        for etat in range(len(ODates)): #correspond au nombre de conditions aux limites
            Obs_etat = Observations[etat].tolist()
            list_obs_etat = []
            for obs in range(len(list(ONames))):
                if len(ODates[etat])==1: #cas classique, statique
                    list_obs_etat = Obs_etat
                    if not(isinstance(list_obs_etat, list)):
                        list_obs_etat = [list_obs_etat]

                else:
                    for time_etat in range(len(Obs_etat)):
                        if not(isinstance(Obs_etat[time_etat], list)): #une seule grandeur observée
                            list_obs_etat.append(Obs_etat[time_etat])
                        else:
                            list_obs_etat.append(Obs_etat[time_etat][obs])

            #EXTRA for verify tests - START
            if len(ODates[etat])==1:
                number_observations_by_cl.append(1) #in this case only one line in the measurements file, this is just to be used as input of the test functions
            else:
                number_observations_by_cl.append(len(Obs_etat)) #we get the number of lines of the measurements file, this is just to be used as input of the test functions
            #EXTRA for verify tests - END

            Observations_new = Observations_new + list_obs_etat
        Observations = Observations_new
        #Bricolage Fin




        def prev_adao_version_TOP_LEVEL_exedymosimMultiobs( x_values_matrix):
            y_values_matrix = TOP_LEVEL_exedymosimMultiobs( x_values_matrix=x_values_matrix, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables, LNames = LNames, ModelFormat = ModelFormat, KeepCalculationFolders = KeepCalculationFolders, Verbose = Verbose, dict_dsin_paths = dict_dsin_path_ref, Linux = Linux, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
            return y_values_matrix

        def prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(x_values_matrix):
            y_values_matrix = TOPLEVEL_exedymosimMultiobs_simple(x_values_matrix = x_values_matrix, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables, LNames = LNames, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName), KeepCalculationFolders = KeepCalculationFolders, Linux = Linux, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
            return y_values_matrix

        if self.__model["Format"].upper() in ["DYMOSIM", "GUESS"]:

            if adao.version[:5] < '9.7.0' and adao.version[5]=='.': #to handle differences in the way directoperator is mangaged after modifications brought to direct operator
                if ComplexModel:
                    simulateur = prev_adao_version_TOP_LEVEL_exedymosimMultiobs
                    exedymosimMultiobs_REF_CALCULATION(Background)
                else:
                    simulateur = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple
                    preparation_exedymosimMultiobs_simple()

            else:
                if ComplexModel:
                    simulateur = TOP_LEVEL_exedymosimMultiobs #to handle parallel computing
                    exedymosimMultiobs_REF_CALCULATION(Background)
                else:
                    simulateur = TOPLEVEL_exedymosimMultiobs_simple #to handle parallel computing
                    preparation_exedymosimMultiobs_simple()

        elif self.__model["Format"].upper() == "PYSIM":
            simulateur = exepythonMultiobs
        elif self.__model["Format"].upper() == "FMI" or self.__model["Format"].upper() == "FMU":
            simulateur = TOP_LEVEL_exefmuMultiobs
            preparation_exefmu_om_Multiobs()
        elif self.__model["Format"].upper() == "OPENMODELICA":
            preparation_exefmu_om_Multiobs()
            simulateur = TOP_LEVEL_exeOpenModelicaMultiobs

        else:
            raise ValueError("Unknown model format \"%s\""%self.__model["Format"].upper())

        def verify_function(x_values, model_format):


            simulation_results_all = []
            list_simulation_time = []
            for i in list(range(3)): #we consider only three iterations
                start_time_verify = time.time()
                if model_format in ["DYMOSIM"]:
                    if ComplexModel:
                        simulation_results = prev_adao_version_TOP_LEVEL_exedymosimMultiobs(x_values)
                    else:
                        simulation_results = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(x_values)
                elif model_format in ["FMI","FMU"]:
                    simulation_results = TOP_LEVEL_exefmuMultiobs(x_values, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution, FMUInput = FMUInput)
                elif model_format in ["OPENMODELICA"]:
                    simulation_results = TOP_LEVEL_exeOpenModelicaMultiobs(x_values, KeepCalculationFolders = KeepCalculationFolders, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, Linux = Linux, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
                else:
                    raise NotImplementedError("Not yet implemented for current model format: ", model_format)
                end_time_verify = time.time()

                list_simulation_time.append(round(end_time_verify - start_time_verify,3))
                simulation_results_all.append(simulation_results)


            elapsed_time = round(sum(list_simulation_time)/len(list_simulation_time),3)
                #not necessary, already in good format
            # numpy.set_printoptions(precision=2,linewidth=5000, threshold = 10000)
            # reshaped_simulation_results_all = numpy.array(simulation_results_all).reshape((len(OutputVariables),-1)).transpose()

            # numpy.set_printoptions(precision=2,linewidth=5000)

            list_check_output = []
            list_false_output = []
            simulation_results_all_one_boundary_condition =[]

            for simulation_output in simulation_results_all: #iteration over the three simulations performed
                # THIS DOES NOT WORK IF OBSERVATIONS FILES ARE OF DIFFERENT SIZE# simultation_ouput_reshaped = simulation_output.reshape((len(LNames),-1))[0]    #consideration of only one set of boundary conditions (otherwise outputs could be modified by boundary condition modifications)
                total_number_measurements_first_simulation = number_observations_by_cl[0]*len(OutputVariables)
                first_simulation_results = simulation_output[:total_number_measurements_first_simulation]
                simulation_results_all_one_boundary_condition.append(first_simulation_results)

            for index_line_time_simulation in range(len(simulation_results_all_one_boundary_condition[0].reshape(len(OutputVariables),-1).transpose())): #iteration over each time results individually
                for i in range(len(OutputVariables)):
                    if (simulation_results_all_one_boundary_condition[0].reshape(len(OutputVariables),-1).transpose()[index_line_time_simulation][i] == simulation_results_all_one_boundary_condition[1].reshape(len(OutputVariables),-1).transpose()[index_line_time_simulation][i]) & (simulation_results_all_one_boundary_condition[0].reshape(len(OutputVariables),-1).transpose()[index_line_time_simulation][i] == simulation_results_all_one_boundary_condition[2].reshape(len(OutputVariables),-1).transpose()[index_line_time_simulation][i]):
                        list_check_output.append("True")

                    else:
                        list_check_output.append("False")
                        if OutputVariables[i] in list_false_output: #problematic variable already included
                            pass
                        else:
                                list_false_output.append(OutputVariables[i])

            if "False" in list_check_output:
                verify_function_result = "False"
            else:
                verify_function_result = "True"
            return verify_function_result, list_false_output, elapsed_time

        def verify_function_sensitivity(x_values, increment, model_format):

            if model_format in ["DYMOSIM"]:
                if ComplexModel:
                    simulation_results = prev_adao_version_TOP_LEVEL_exedymosimMultiobs(x_values)
                else:
                    simulation_results = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(x_values)
            elif model_format in ["FMI","FMU"]:
                simulation_results = TOP_LEVEL_exefmuMultiobs(x_values, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution, FMUInput = FMUInput)
            elif model_format in ["OPENMODELICA"]:
                simulation_results = TOP_LEVEL_exeOpenModelicaMultiobs(x_values, KeepCalculationFolders = KeepCalculationFolders, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, Linux = Linux, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
            else:
                raise NotImplementedError("Not yet implemented for current model format: ", model_format)


            x_values_modif = [x*(1+increment) for x in x_values]

            if model_format in ["DYMOSIM"]:
                if ComplexModel:
                    simulation_results_modif = prev_adao_version_TOP_LEVEL_exedymosimMultiobs(x_values_modif)
                else:
                    simulation_results_modif = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(x_values_modif)
            elif model_format in ["FMI","FMU"]:
                simulation_results_modif = TOP_LEVEL_exefmuMultiobs(x_values_modif, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution, FMUInput = FMUInput)
            elif model_format in ["OPENMODELICA"]:
                simulation_results_modif = TOP_LEVEL_exeOpenModelicaMultiobs(x_values_modif, KeepCalculationFolders = KeepCalculationFolders, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, Linux = Linux, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
            else:
                raise NotImplementedError("Not yet implemented for current model format: ", model_format)

            list_check_output = ["False" for i in OutputVariables] #everything initialized as not good and then if something changes (at least one point), then it is OK
            list_not_modified_variables =[]

            total_number_measurements_first_simulation = number_observations_by_cl[0]*len(OutputVariables)

            # THIS DOES NOT WORK IF OBSERVATIONS FILES ARE OF DIFFERENT SIZE# simulation_results_one_boundary_condition = simulation_results.reshape((len(LNames),-1))[0]
            # THIS DOES NOT WORK IF OBSERVATIONS FILES ARE OF DIFFERENT SIZE# simulation_results_modif_one_boundary_condition = simulation_results_modif.reshape((len(LNames),-1))[0]
            simulation_results_one_boundary_condition = simulation_results[:total_number_measurements_first_simulation]
            simulation_results_modif_one_boundary_condition = simulation_results_modif[:total_number_measurements_first_simulation]

            for index_line_time_simulation in range(len(simulation_results_one_boundary_condition.reshape(len(OutputVariables),-1).transpose())):

                for i in range(len(OutputVariables)):
                    if simulation_results_one_boundary_condition.reshape(len(OutputVariables),-1).transpose()[index_line_time_simulation][i] != simulation_results_modif_one_boundary_condition.reshape(len(OutputVariables),-1).transpose()[index_line_time_simulation][i] :
                        list_check_output[i] = "True"


            for i in range(len(OutputVariables)):
                if list_check_output[i] == "False": #it means the variable has not changed
                    list_not_modified_variables.append(OutputVariables[i])

            if "False" in list_check_output:
                verify_function_sensitivity_result = "False"
            else:
                verify_function_sensitivity_result = "True"

            return verify_function_sensitivity_result, list_not_modified_variables

        def verify_function_sensitivity_parameter(x_values, increment, model_format):

            if model_format in ["DYMOSIM"]:
                if ComplexModel:
                    simulation_results_ref = prev_adao_version_TOP_LEVEL_exedymosimMultiobs(x_values)
                else:
                    simulation_results_ref = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(x_values)
            elif model_format in ["FMI","FMU"]:
                simulation_results_ref = TOP_LEVEL_exefmuMultiobs(x_values, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution, FMUInput = FMUInput)
            elif model_format in ["OPENMODELICA"]:
                simulation_results_ref = TOP_LEVEL_exeOpenModelicaMultiobs(x_values, KeepCalculationFolders = KeepCalculationFolders, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, Linux = Linux, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
            else:
                raise NotImplementedError("Not yet implemented for current model format: ", model_format)

            list_param_with_no_impact = []
            Check_params_impact = "True"

            x_values_modif = [x*(1+increment) for x in x_values]


            for param_index in range(len(x_values)):   #the goal is to modify each param individually and check if it is possible to observe variations
                x_values_param = list(x_values) #avoid memory surprises
                x_values_param[param_index] = x_values_modif[param_index]
                if model_format in ["DYMOSIM"]:
                    if ComplexModel:
                        simulation_results_param = prev_adao_version_TOP_LEVEL_exedymosimMultiobs(x_values_param)
                    else:
                        simulation_results_param = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(x_values_param)
                elif model_format in ["FMI","FMU"]:
                    simulation_results_param = TOP_LEVEL_exefmuMultiobs(x_values_param, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution, FMUInput = FMUInput)
                elif model_format in ["OPENMODELICA"]:
                    simulation_results_param = TOP_LEVEL_exeOpenModelicaMultiobs(x_values_param, KeepCalculationFolders = KeepCalculationFolders, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, Linux = Linux, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
                else:
                    raise NotImplementedError("Not yet implemented for current model format: ", model_format)

                if numpy.array_equal(simulation_results_param,simulation_results_ref): #there is not impact on the whole simulation
                    list_param_with_no_impact.append(VariablesToCalibrate[param_index])
                    Check_params_impact = "False"

            return Check_params_impact, list_param_with_no_impact


        def check_model_stability(x_values_names, background_values, bounds, number_of_tests, model_format):

            dict_check_model_stability = {}
            for index_x in range(len(x_values_names)):
                x_bg_tested = x_values_names[index_x]

                print("  [VERBOSE] Model stability check is being performed for the following variable to be calibrated: ", x_bg_tested)

                if bounds[index_x][0] == None or bounds[index_x][0] == "None":
                    bounds_inf_x_bg_tested = background_values[index_x] - abs(background_values[index_x]*100)
                else:
                    bounds_inf_x_bg_tested = bounds[index_x][0]

                if bounds[index_x][1] == None or bounds[index_x][1] == "None":
                    bounds_sup_x_bg_tested = background_values[index_x] + abs(background_values[index_x]*100)
                else:
                    bounds_sup_x_bg_tested = bounds[index_x][1]

                #avoid problems with values to be tested hen the bounds are strictly equal to 0
                if bounds_inf_x_bg_tested == 0: #which means that bounds_sup_x_bg_tested > 0
                    bounds_inf_x_bg_tested = min(1e-9,bounds_sup_x_bg_tested*1e-9)
                if bounds_sup_x_bg_tested == 0: #which means that bounds_inf_x_bg_tested < 0
                    bounds_sup_x_bg_tested = max(-1e-9,bounds_inf_x_bg_tested*1e-9)

                list_x_bg_tested = []

                if bounds_inf_x_bg_tested < 0:
                    if bounds_sup_x_bg_tested<0:
                        list_x_bg_tested = list(numpy.geomspace(bounds_inf_x_bg_tested,bounds_sup_x_bg_tested,int(number_of_tests)))
                    else:
                        list_x_bg_tested = list(numpy.geomspace(bounds_inf_x_bg_tested,bounds_inf_x_bg_tested*1e-4,int(number_of_tests/2)))
                        list_x_bg_tested = list_x_bg_tested + list((numpy.geomspace(bounds_sup_x_bg_tested*1e-4,bounds_sup_x_bg_tested,int(number_of_tests/2))))
                else: #both bounds are >0
                    list_x_bg_tested = list(numpy.geomspace(bounds_inf_x_bg_tested,bounds_sup_x_bg_tested,int(number_of_tests)))

                #for a linear partition, we consider a log repartition better
                # for index_partition in range(number_of_tests):
                #     list_x_bg_tested.append(bounds_inf_x_bg_tested + index_partition*(bounds_sup_x_bg_tested-bounds_inf_x_bg_tested)/(number_of_tests-1))

                list_failed_model_evaluation = []
                for x_value_bg_tested in list_x_bg_tested:

                    x_whole_values_with_bg = copy.deepcopy(background_values) #avoid modifiction of backgroundvalues
                    x_whole_values_with_bg[index_x] = x_value_bg_tested
                    try:
                        if model_format in ["DYMOSIM"]:
                            if ComplexModel:
                                simulation_results = prev_adao_version_TOP_LEVEL_exedymosimMultiobs(x_whole_values_with_bg)
                            else:
                                simulation_results = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(x_whole_values_with_bg)
                        elif model_format in ["FMI","FMU"]:
                            simulation_results = TOP_LEVEL_exefmuMultiobs(x_whole_values_with_bg, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution, FMUInput = FMUInput)
                        elif model_format in ["OPENMODELICA"]:
                            simulation_results = TOP_LEVEL_exeOpenModelicaMultiobs(x_whole_values_with_bg, KeepCalculationFolders = KeepCalculationFolders, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, Linux = Linux, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)
                        else:
                            raise NotImplementedError("Not yet implemented for current model format: ", model_format)
                    except Exception:
                        list_failed_model_evaluation.append(x_value_bg_tested)

                dict_check_model_stability[x_bg_tested] = list_failed_model_evaluation
            return dict_check_model_stability

        if VerifyFunction:
            check_function, list_not_same_model_outputs, elapsed_time_for_simu = verify_function(x_values = Background, model_format = self.__model["Format"].upper())
            if check_function == "True":
                print("  [VERBOSE] Results of function checking: ", "OK for all model outputs, ","simulation time (including all boundary conditions) is ",elapsed_time_for_simu, " seconds" )
            else:
                print("  [VERBOSE] Results of function checking: ", "NOT OK for all model outputs")
                print("  [VERBOSE] The following model outputs are not the same when repeating a simulation: ", list_not_same_model_outputs )

        if GlobalSensitivityCheck:
            check_sensitivity, list_same_model_outputs = verify_function_sensitivity(x_values = Background, increment = Params["DifferentialIncrement"], model_format = self.__model["Format"].upper())
            if VerifyFunction == False:
                print("  [VERBOSE] /!\\ Activate VerifyFunction option and check that the result of the check is OK to get reliable results from GlobalSensitivityCheck option")
            if check_sensitivity == "True":
                print("  [VERBOSE] Results of function global sensitivity analysis: ", "All model outputs vary when background values are modified")
            else:
                print("  [VERBOSE] Results of function global sensitivity analysis: ", "Some model outputs DO NOT vary when background values are modified")
                print("  [VERBOSE] The following model outputs DO NOT vary when background values are modified: ", list_same_model_outputs )

        if ParamSensitivityCheck:
            check_function, list_params_without_impact = verify_function_sensitivity_parameter(x_values = Background, increment = Params["DifferentialIncrement"], model_format = self.__model["Format"].upper())
            if VerifyFunction == False:
                print("  [VERBOSE] /!\\ Activate VerifyFunction option and check that the result of the check is OK to get reliable results from ParamSensitivityCheck option")
            if check_function == "True":
                print("  [VERBOSE] Results of parameter sensitivity checking: ", "OK, all parameters have an impact on model outputs")
            else:
                print("  [VERBOSE] Results of parameter sensitivity checking: ", "NOT OK, some parameters do not have an impact on model outputs")
                print("  [VERBOSE] The following parameters do not have an impact on model outputs: ", list_params_without_impact )

        if ModelStabilityCheck:
            print("  [VERBOSE] Model stability check is being performed, this check might take several minutes depending on the model and number of variables to calibrate (you can reduce the value of ModelStabilityCheckingPoints option to reduce checking time, by default its value is 10)")
            check_stability = check_model_stability(x_values_names = VariablesToCalibrate, background_values = Background, bounds = Params['Bounds'], number_of_tests = ModelStabilityCheckingPoints, model_format = self.__model["Format"].upper())
            if check_stability == dict(zip(VariablesToCalibrate,[list() for i in VariablesToCalibrate])):
                print("  [VERBOSE] Results of Model stability check: ", "The model simulates correctly when modifying individually the values of the variables to calibrate within the range in which their optimal value should be found")
            else:
                print("  [VERBOSE] Results of Model stability check: ", "The model FAILS to converge with the following values of variables to calibrate", check_stability)
                print("  [VERBOSE] The data assimilation procedure might not succeed if the model fails to converge, please revise the model and/or the range in which the optimal value of the variables to calibrate should be found")

        #

        __adaocase = adaoBuilder.New()
        __adaocase.set( 'AlgorithmParameters',  Algorithm=Algo, Parameters=Params )
        __adaocase.set( 'Background',           Vector=Background)
        __adaocase.set( 'Observation',          Vector=Observations )
        if type(CovB) is float:
            __adaocase.set( 'BackgroundError',  ScalarSparseMatrix=CovB )
        else:
            __adaocase.set( 'BackgroundError',  Matrix=CovB )

        if AdaptObservationError:
            Square_Observations = [x*x for x  in Observations]

            # if (type(CovR) is float and CovR!= 1.0 ):# by default we still consider the square, better not to modify it
            if type(CovR) is float:
                ObsError = CovR*numpy.diag(Square_Observations)
                __adaocase.set( 'ObservationError', Matrix = ObsError )
            else:
                ObsError = 1e-15*numpy.diag(Square_Observations) #arbitary low value to eventually handle pressures in Pa
                __adaocase.set( 'ObservationError', Matrix = ObsError )
            print("  [VERBOSE] AdaptObservationError was set to True, the following ObservationError matrix has been considered: ")
            print(ObsError)
        else: #classical situation
            if type(CovR) is float:
                __adaocase.set( 'ObservationError', ScalarSparseMatrix=CovR )
            else:
                __adaocase.set( 'ObservationError', Matrix=CovR )

        if Params["EnableMultiProcessing"]==1 :
            ParallelComputationGradient = True
        else:
            ParallelComputationGradient = False


        if self.__model["Format"].upper() in ["DYMOSIM"]:
            if ParallelComputationGradient:

                if adao.version[:5] < '9.7.0' and adao.version[5]=='.':
                    raise ValueError("ADAO version must be at least 9.7.0 to support parallel computation of the gradient, current version is %s"%str(adao.version[:5]))

                if ComplexModel:
                      __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                               Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"], "EnableMultiProcessing":Params["EnableMultiProcessing"], "NumberOfProcesses" : Params["NumberOfProcesses"]},
                               ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'ModelFormat': ModelFormat, 'KeepCalculationFolders': KeepCalculationFolders, 'Verbose' : Verbose, 'dict_dsin_paths' : dict_dsin_path_ref, 'Linux': Linux, 'List_Multideltatime' : List_Multideltatime, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution   },
                               )
                else:
                    __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                               Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"], "EnableMultiProcessing":Params["EnableMultiProcessing"], "NumberOfProcesses" : Params["NumberOfProcesses"]},
                               ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'ref_simudir': self._get_Name_ModelTmpDir_simple(ModelName), 'KeepCalculationFolders': KeepCalculationFolders, 'Linux': Linux, 'List_Multideltatime' : List_Multideltatime, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution  },
                               )

            else:
                if adao.version[:5] < '9.7.0' and adao.version[5]=='.':
                    __adaocase.set( 'ObservationOperator',  OneFunction=simulateur, Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]})

                else:
                    if ComplexModel:
                          __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                                   Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]},
                                   ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'ModelFormat': ModelFormat, 'KeepCalculationFolders': KeepCalculationFolders, 'Verbose' : Verbose, 'dict_dsin_paths' : dict_dsin_path_ref, 'Linux': Linux, 'List_Multideltatime' : List_Multideltatime, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution  },
                                   )
                    else:
                        __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                                   Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]},
                                   ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'ref_simudir': self._get_Name_ModelTmpDir_simple(ModelName), 'KeepCalculationFolders': KeepCalculationFolders, 'Linux': Linux, 'List_Multideltatime' : List_Multideltatime, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution  })

        elif self.__model["Format"].upper() in ["OPENMODELICA"]: #OPENMODELICA (different from FMI since there are different keywords for the function: Linux and KeepCalculationFolders)

            if ComplexModel:
                print("ComplexModel option is only valid for DYMOSIM format (it has no effect for the current calculation)")

            if ParallelComputationGradient:
                if adao.version[:5] < '9.7.0' and adao.version[5]=='.':
                    raise ValueError("ADAO version must be at least 9.7.0 to support parallel computation of the gradient, current version is %s"%str(adao.version[:5]))
                else:
                    __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                               Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]},
                               ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'LColumns':LColumns, 'LVariablesToChange':LVariablesToChange, 'ref_simudir': self._get_Name_ModelTmpDir_simple(ModelName), 'ModelName': ModelName, 'List_Multideltatime' : List_Multideltatime, 'Linux': Linux, 'KeepCalculationFolders': KeepCalculationFolders, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution})

            else:
                if adao.version[:5] < '9.7.0' and adao.version[5]=='.':
                    raise ValueError("ADAO version must be at least 9.7.0 to support other formats than DYMOSIM")
                else:
                    __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                               Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]},
                               ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'LColumns':LColumns, 'LVariablesToChange':LVariablesToChange, 'ref_simudir': self._get_Name_ModelTmpDir_simple(ModelName), 'ModelName': ModelName, 'List_Multideltatime' : List_Multideltatime, 'Linux': Linux, 'KeepCalculationFolders': KeepCalculationFolders, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution})

        else: #FMI or GUESS format

            if ComplexModel:
                print("ComplexModel option is only valid for DYMOSIM format (it has no effect for the current calculation)")

            if ParallelComputationGradient:
                if adao.version[:5] < '9.7.0' and adao.version[5]=='.':
                    raise ValueError("ADAO version must be at least 9.7.0 to support parallel computation of the gradient, current version is %s"%str(adao.version[:5]))
                else:
                    __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                               Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]},
                               ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'LColumns':LColumns, 'LVariablesToChange':LVariablesToChange, 'ref_simudir': self._get_Name_ModelTmpDir_simple(ModelName), 'ModelName': ModelName, 'List_Multideltatime' : List_Multideltatime, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution, 'FMUInput':FMUInput})

            else:
                if adao.version[:5] < '9.7.0' and adao.version[5]=='.':
                    raise ValueError("ADAO version must be at least 9.7.0 to support other formats than DYMOSIM")
                else:
                    __adaocase.set( 'ObservationOperator',  OneFunction=simulateur,
                               Parameters = {"DifferentialIncrement":Params["DifferentialIncrement"]},
                               ExtraArguments = {'VariablesToCalibrate':VariablesToCalibrate, 'OutputVariables' : OutputVariables, 'LNames': LNames, 'LColumns':LColumns, 'LVariablesToChange':LVariablesToChange, 'ref_simudir': self._get_Name_ModelTmpDir_simple(ModelName), 'ModelName': ModelName, 'List_Multideltatime' : List_Multideltatime, 'AdvancedDebugModel':AdvancedDebugModel, 'TimeoutModelExecution':TimeoutModelExecution, 'FMUInput':FMUInput})


        #
        if self.__verbose:
            __adaocase.set( 'Observer', Variable="CostFunctionJAtCurrentOptimum", String="print('\\n  -----------------------------------\\n  [VERBOSE] Current iteration number: %i'%len(var))" )
            __adaocase.set( 'Observer', Variable="CostFunctionJAtCurrentOptimum",  Template="ValuePrinter", Info="\n  [VERBOSE] Current optimal cost value.:" )
            __adaocase.set( 'Observer', Variable="CurrentOptimum",                 Template="ValuePrinter", Info="\n  [VERBOSE] Current optimal state......:" )        #

        if self.__IntermediateInformation:
            __adaocase.set( 'Observer', Variable="CostFunctionJ",  Template="ValuePrinter", Info="\n  [VERBOSE] Current cost value.:" )
            __adaocase.set( 'Observer', Variable="CurrentState",  Template="ValuePrinter", Info="\n  [VERBOSE] Current state......:" )

        __adaocase.execute()
        #

        if InitialSimulation: #the prev_adao_version_TOP_LEVEL_XXX is already defined with proper arguments (boundary conditions etc.)

            if self.__model["Format"].upper() in ["DYMOSIM"]:
                if ComplexModel:
                    initialsimulation_results = prev_adao_version_TOP_LEVEL_exedymosimMultiobs(Background)
                else:
                    initialsimulation_results = prev_adao_version_TOPLEVEL_exedymosimMultiobs_simple(Background)
            elif self.__model["Format"].upper() in ["FMI", "FMU"]:
                initialsimulation_results = TOP_LEVEL_exefmuMultiobs(Background, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution, FMUInput = FMUInput)

            elif self.__model["Format"].upper() in ["OPENMODELICA"]:
                initialsimulation_results = TOP_LEVEL_exeOpenModelicaMultiobs(Background, KeepCalculationFolders = KeepCalculationFolders, VariablesToCalibrate=VariablesToCalibrate, OutputVariables=OutputVariables,  LNames = LNames, LColumns = LColumns, LVariablesToChange=LVariablesToChange, ref_simudir = self._get_Name_ModelTmpDir_simple(ModelName),  ModelName = ModelName, List_Multideltatime = List_Multideltatime, Linux = Linux, AdvancedDebugModel = AdvancedDebugModel,  TimeoutModelExecution = TimeoutModelExecution )

            __resultats = dict(
                InitialParameters = numpy.asarray(Background),
                OptimalParameters = __adaocase.get("Analysis")[-1], # * Background,
                InitialSimulation = numpy.asarray(initialsimulation_results), #the simulation results are given for backgroung values, can be used to evaluate the overall performance of the calibration procedure
                OptimalSimulation = __adaocase.get("SimulatedObservationAtOptimum")[-1],
                Measures          = Observations,
                NamesOfParameters = BNames,
                NamesOfMeasures   = ONames,
                )
        else:
            __resultats = dict(
                InitialParameters = numpy.asarray(Background),
                OptimalParameters = __adaocase.get("Analysis")[-1], # * Background,
                OptimalSimulation = __adaocase.get("SimulatedObservationAtOptimum")[-1],
                Measures          = Observations,
                NamesOfParameters = BNames,
                NamesOfMeasures   = ONames,
                )

        if "APosterioriCovariance" in Params["StoreSupplementaryCalculations"]:
            __resultats["APosterioriCovariance"] = __adaocase.get("APosterioriCovariance")[-1]

        if ResultsSummary:
            if InitialSimulation:
                measures_input = __resultats ["Measures"]
                initial_simu = __resultats ["InitialSimulation"]
                optimal_simu = __resultats ["OptimalSimulation"]

                diff_measures_initial_rmse = numpy.array([(measures_input[i]-initial_simu[i])**2 for i in range(len(measures_input))])
                diff_measures_initial_reldiff = numpy.array([abs((measures_input[i]-initial_simu[i])/measures_input[i]) for i in range(len(measures_input)) if measures_input[i] !=0])

                diff_measures_optimal_rmse = numpy.array([(measures_input[i]-optimal_simu[i])**2 for i in range(len(measures_input))])
                diff_measures_optimal_reldiff = numpy.array([abs((measures_input[i]-optimal_simu[i])/measures_input[i]) for i in range(len(measures_input)) if measures_input[i] !=0])

                diff_measures_initial_rmse_res = str(numpy.format_float_scientific(numpy.sqrt(diff_measures_initial_rmse.mean()), precision = 3))
                diff_measures_initial_reldiff_res = str(numpy.round(diff_measures_initial_reldiff.mean()*100,decimals =2))

                diff_measures_optimal_rmse_res = str(numpy.format_float_scientific(numpy.sqrt(diff_measures_optimal_rmse.mean()), precision = 3))
                diff_measures_optimal_reldiff_res = str(numpy.round(diff_measures_optimal_reldiff.mean()*100,decimals =2))

                __resultats["ResultsSummary_RMSE"] = ["Average_RMSE_INITIAL = " + diff_measures_initial_rmse_res, "Average_RMSE_OPTIMAL = " + diff_measures_optimal_rmse_res ]
                __resultats["ResultsSummary_RelativeDifference"] = ["Average_RelativeDifference_INITIAL = " +  diff_measures_initial_reldiff_res + "%", "Average_RelativeDifference_OPTIMAL = " + diff_measures_optimal_reldiff_res + "%" ]
            else:
                measures_input = __resultats ["Measures"]
                optimal_simu = __resultats ["OptimalSimulation"]

                diff_measures_optimal_rmse = numpy.array([(measures_input[i]-optimal_simu[i])**2 for i in range(len(measures_input))])
                diff_measures_optimal_reldiff = numpy.array([abs((measures_input[i]-optimal_simu[i])/measures_input[i]) for i in range(len(measures_input)) if measures_input[i] !=0])


                diff_measures_optimal_rmse_res = str(numpy.format_float_scientific(numpy.sqrt(diff_measures_optimal_rmse.mean()), precision = 3))
                diff_measures_optimal_reldiff_res = str(numpy.round(diff_measures_optimal_reldiff.mean()*100,decimals =2))

                __resultats["ResultsSummary_RMSE"] = ["Average_RMSE_OPTIMAL = " + diff_measures_optimal_rmse_res ]
                __resultats["ResultsSummary_RelativeDifference"] = ["Average_RelativeDifference_OPTIMAL = " + diff_measures_optimal_reldiff_res + "%" ]

        #
        _saveResults(
            __resultats,
            self.__result["SourceName"],
            self.__result["Level"],
            self.__result["Format"],
            self.__verbose,
            )
        #

        if CreateOptimaldsin:
             if self.__model["Format"].upper() in ["DYMOSIM"]:
                 for etat in range(len(LNames)):
                     dict_optimal_params = dict(zip(VariablesToCalibrate, __adaocase.get("Analysis")[-1])) #dans la boucle, sinon il se vide à chaque fois que l'on fait itère
                     if not(ComplexModel):
                         dir_for_dsin_opti = os.path.abspath(os.path.join(self._get_Name_ModelTmpDir_simple(ModelName),os.pardir))
                         simu_dir_opti = os.path.abspath(self._get_Name_ModelTmpDir_simple(ModelName))

                         writer_opti = write_in_dsin.Write_in_dsin(dict_inputs =dict_optimal_params,filedir=simu_dir_opti,dsin_name=str("dsin_" +LNames[etat]+ ".txt"),old_file_name='dsin.txt',new_file_name= str("dsin_" +LNames[etat]+ "_optimal.txt"))
                         writer_opti.write_in_dsin

                         writer_opti.write_in_dsin()

                         try:
                             os.remove(os.path.join(dir_for_dsin_opti,str("dsin_" +LNames[etat]+ "_optimal.txt")))
                         except Exception:
                             pass

                         shutil.copyfile(
                                    os.path.join(simu_dir_opti, str("dsin_" +LNames[etat]+ "_optimal.txt")),
                                    os.path.join(dir_for_dsin_opti, str("dsin_" +LNames[etat]+ "_optimal.txt"))
                                    )

                         auto_simul_opti = Automatic_Simulation(
                                                     simu_dir=simu_dir_opti,
                                                     dsin_name= str("dsin_" +LNames[etat]+ "_optimal.txt"),
                                                     dymosim_path = os.path.join(simu_dir_opti, os.pardir) ,
                                                     dsres_path = str("dsres_" +LNames[etat]+ "_opti.mat"),
                                                     dict_inputs= {},
                                                     logfile=False,
                                                     timeout=TimeoutModelExecution,
                                                     without_modelicares=True,
                                                     linux=Linux
                                                     )
                         auto_simul_opti.single_simulation()

                         if not(auto_simul_opti.success_code == 0):
                             print("The dsin.txt with the optimal values does not converge directly, please update the value of iteration variables using Change_working_Point script (consider both calibrated paramaters and boundary conditions in the procedure)")
                     else:
                         try: #to handle situations in which there is only one CL (boundary conditions) file
                             var_int = numpy.ravel(LColumns[:,etat])
                         except Exception:
                             var_int = numpy.ravel(LColumns)
                         dict_inputs_boundary_conditions_optimal_params = dict(zip(LVariablesToChange, var_int))
                         dict_inputs_boundary_conditions_optimal_params.update(dict_optimal_params)

                         try:
                             os.remove(os.path.join(dir_for_dsin_opti,str("dsin_" +LNames[etat]+ "_optimal.txt")))
                         except Exception:
                             pass
                         dir_for_dsin_opti = os.path.abspath(os.path.join(self._get_Name_ModelTmpDir_simple(ModelName),os.pardir))
                         shutil.copyfile(
                                    os.path.join(dir_for_dsin_opti, str("dsin.txt")),
                                    os.path.join(dir_for_dsin_opti, str("dsin_" +LNames[etat]+ "_optimal.txt"))
                                    )
                         writer_opti = write_in_dsin.Write_in_dsin(dict_inputs =dict_inputs_boundary_conditions_optimal_params,filedir=dir_for_dsin_opti,dsin_name=str("dsin_" +LNames[etat]+ "_optimal.txt"),old_file_name=str("dsin_" +LNames[etat]+ "_old.txt"),new_file_name= str("dsin_" +LNames[etat]+ "_optimal.txt"))
                         writer_opti.write_in_dsin
                         writer_opti.write_in_dsin()
                         os.remove(os.path.join(dir_for_dsin_opti,str("dsin_" +LNames[etat]+ "_old.txt")))
                         print("The dsin.txt with the optimal values has not been tested, updating the values of iteration variables might be necessary: this can be done by using Change_working_Point script (consider both calibrated paramaters and boundary conditions in the procedure)")

             else: #FMI, OM or GUESS format
                 print("CreateOptimaldsin option is only valid for DYMOSIM format (it has no effect for the current calculation)")

        if self.__verbose: print("")
        del __adaocase

        if not(KeepCalculationFolders):
            shutil.rmtree(self._get_Name_ModelTmpDir_simple(ModelName), ignore_errors=True)

        if CreateCSVoutputResults:
            print("Creation of CSV output results")


            optimal_results = __resultats["OptimalSimulation"]
            for obs_file_index in range(len(self.__measures["SourceName"])):
                obs_filename = self.__measures["SourceName"][obs_file_index] #for the name of the outputresult

                time_measures_number = len(OHours[obs_file_index]) #get the number of lines in the obs file
                total_measures_number_per_cl = time_measures_number*len(__resultats["NamesOfMeasures"]) #size of the list to be removed from the whole results file
                optimal_results_cl = optimal_results[:total_measures_number_per_cl] # output results for the current cl
                optimal_results = optimal_results[total_measures_number_per_cl:] # update of the whole results file (we remove te results already treated)

                optimal_results_cl_to_csv = optimal_results_cl.reshape((len(__resultats["NamesOfMeasures"]),-1)).transpose() #reshape to get one line per timedate
                df_optimal_results_cl_to_csv = pandas.DataFrame(optimal_results_cl_to_csv, columns = __resultats["NamesOfMeasures"]) #creation of the df with the names of measures
                df_optimal_results_cl_to_csv.insert(0,"Hour", OHours[obs_file_index]) #add Hour column
                df_optimal_results_cl_to_csv.insert(0,"Date", ODates[obs_file_index]) # add Date column

                optimal_file_results_name_cl_tmp = "Optimal_simulation_tmp.csv"
                df_optimal_results_cl_to_csv.to_csv(optimal_file_results_name_cl_tmp, sep = ";", index = False)

                optimal_file_results_name_cl = "Optimal_simulation_"+obs_filename
                with open(optimal_file_results_name_cl_tmp, 'r') as infile:
                    readie=csv.reader(infile, delimiter=';')
                    with open(optimal_file_results_name_cl, 'wt', newline='') as output:
                        outwriter=csv.writer(output, delimiter=';')
                        outwriter.writerow(["#"])
                        for row in readie:
                             outwriter.writerow(row)
                try:
                    os.remove(optimal_file_results_name_cl_tmp)
                except Exception:
                    pass

            if InitialSimulation: #If initial simulation is required as well, the Initial results files are given as well
                initial_results = __resultats["InitialSimulation"]
                for obs_file_index in range(len(self.__measures["SourceName"])):
                    obs_filename = self.__measures["SourceName"][obs_file_index] #for the name of the outputresult

                    time_measures_number = len(OHours[obs_file_index]) #get the number of lines in the obs file
                    total_measures_number_per_cl = time_measures_number*len(__resultats["NamesOfMeasures"]) #size of the list to be removed from the whole results file
                    initial_results_cl = initial_results[:total_measures_number_per_cl] # output results for the current cl
                    initial_results = initial_results[total_measures_number_per_cl:] # update of the whole results file (we remove te results already treated)

                    initial_results_cl_to_csv = initial_results_cl.reshape((len(__resultats["NamesOfMeasures"]),-1)).transpose() #reshape to get one line per timedate
                    df_initial_results_cl_to_csv = pandas.DataFrame(initial_results_cl_to_csv, columns = __resultats["NamesOfMeasures"]) #creation of the df with the names of measures
                    df_initial_results_cl_to_csv.insert(0,"Hour", OHours[obs_file_index]) #add Hour column
                    df_initial_results_cl_to_csv.insert(0,"Date", ODates[obs_file_index]) # add Date column

                    initial_file_results_name_cl_tmp = "Initial_simulation_tmp.csv"
                    df_initial_results_cl_to_csv.to_csv(initial_file_results_name_cl_tmp, sep = ";", index = False)

                    initial_file_results_name_cl = "Initial_simulation_"+obs_filename
                    with open(initial_file_results_name_cl_tmp, 'r') as infile:
                        readie=csv.reader(infile, delimiter=';')
                        with open(initial_file_results_name_cl, 'wt', newline='') as output:
                            outwriter=csv.writer(output, delimiter=';')
                            outwriter.writerow(["#"])
                            for row in readie:
                                 outwriter.writerow(row)
                    try:
                        os.remove(initial_file_results_name_cl_tmp)
                    except Exception:
                        pass

        return __resultats


        def verify_gradient(self):
            raise NotImplementedError("Not yet implemented")

# ==============================================================================
def _readLink(__filename=None, __colnames=None, __indexname="Variable", __format="Guess"):
    """
    Read file of link between model and measures

    Arguments:
        - File name
        - Names of the columns to read, known by their variable header
        - Name of the column containing the variables to adapt
        - Format of the data (CSV, TSV... or can be guessed)
    """
    #
    if __colnames is None:
        raise
    if __indexname is None: __indexname="Variable"

    try: #Solution provisoire pou gérer les cas sans CL précisées par l'utilisateur
        with ImportFromFile(__filename, __colnames, __indexname, __format, False) as reading:
            colnames, columns, indexname, variablestochange = reading.getvalue()
    except Exception:
        colnames =__colnames
        columns =[]
        variablestochange =[]
        print("/!\\ Boundary conditions indicated in ", __filename, " are not considered for calculation. Indicate at least two boundary conditions so that they are considered. /!\\ ")
    #
    variablestochange = tuple([v.strip() for v in variablestochange])
    return (colnames, columns, variablestochange)

# ==============================================================================
def _readMultiMeasures(__filenames=None, __colnames=None, __format="Guess"):
    """
    Read files of measures, using only some named variables by columns

    Arguments:
        - File name
        - Names of the columns to read, known by their variable header
        - Format of the data (CSV, TSV... or can be guessed)
    """
    #
    MultiMeasures = []
    for __filename in __filenames:
        colnames, columns = _readMeasures(__filename, __colnames, __format)
        MultiMeasures.append( columns )
    #
    return (colnames, MultiMeasures)

# ==============================================================================
def _readMeasures(__filename=None, __colnames=None, __format="Guess"):
    """
    Read files of measures, using only some named variables by columns

    Arguments:
        - File name
        - Names of the columns to read, known by their variable header
        - Format of the data (CSV, TSV... or can be guessed)
    """
    #
    with ImportFromFile(__filename, __colnames, None, __format) as reading:
        colnames, columns, indexname, index = reading.getvalue()
    #
    return (colnames, columns)

# ==============================================================================
def _readBackground(__filename="dsin.txt", __varnames=None, __backgroundformat="Guess"):
    """
    Read background in model definition. The priority is "USER", then "ADAO",
    then "DSIN", and the default one correspond to "DSIN".

    Arguments:
        - File name
        - Names of the variables to be found in the model data
        - Format of the data (can be guessed)
    """
    __format = None
    if __backgroundformat.upper() in ["GUESS", "DSIN"]:
        __format = "DSIN"
        if __filename is not None and os.path.isfile(__filename):
            __model_dir = os.path.dirname(__filename)
            __model_fil = os.path.basename(__filename)
        elif  __filename is not None and os.path.isdir(__filename) and os.path.isfile(os.path.join(__filename, "dsin.txt")):
            __model_dir = os.path.abspath(__filename)
            __model_fil = "dsin.txt"
        else:
            raise ValueError('No such file or directory: %s'%str(__filename))
        __bgfile = os.path.abspath(os.path.join(__model_dir, __model_fil))
        if (len(__bgfile)<7) and (__bgfile[-8:].lower() != "dsin.txt" ):
            raise ValueError("Model definition file \"dsin.txt\" can not be found.")
        if __varnames is None:
            raise ValueError("Model variables to be read has to be given")
    if __backgroundformat.upper() == "ADAO":
        __format = "ADAO"
        if __filename is None or not os.path.isfile(__filename):
            raise ValueError('No such file or directory: %s'%str(__filename))
        __bgfile = os.path.abspath(__filename)
        if not( len(__bgfile)>4 ):
            raise ValueError("User file name \"%s\" is too short and seems not to be valid."%__bgfile)
    if __backgroundformat.upper() == "USER":
        __format = "USER"
        if __filename is None or not os.path.isfile(__filename):
            raise ValueError('No such file or directory: %s'%str(__filename))
        __bgfile = os.path.abspath(__filename)
        if not( len(__bgfile)>5 ):
            raise ValueError("User file name \"%s\" is too short and seems not to be valid."%__bgfile)
    if __format not in ["DSIN", "ADAO", "USER"]:
        raise ValueError("Background initial values asked format \"%s\" is not valid."%__format)
    #
    #---------------------------------------------
    if __format == "DSIN":
        if __varnames is None:
            raise ValueError("Names of variables to read has to be given")
        #
        __names, __background, __bounds = [], [], []
        with open(__bgfile, 'r') as fid:
            __content = fid.readlines()
            for v in tuple(__varnames):
                if _verify_existence_of_variable_in_dsin(v, __content):
                    __value = _read_existing_variable_in_dsin(v, __content)
                    __names.append(v)
                    __background.append(__value[0])
                    __bounds.append(__value[1:3])
                    # print "%s = "%v, __value
        __names = tuple(__names)
        __background = numpy.ravel(__background)
        __bounds = tuple(__bounds)
    #---------------------------------------------
    elif __format.upper() == "ADAO":
        with open(__bgfile, 'r') as fid:
            exec(fid.read())
        #
        __background = locals().get("Background", None)
        if __background is None:
            raise ValueError("Background is not defined")
        else:
            __background = numpy.ravel(__background)
        __Params     = locals().get("Parameters", {})
        if "Bounds" not in __Params:
            raise ValueError("Bounds can not be find in file \"%s\""%str(__filename))
        else:
            __bounds = tuple(__Params["Bounds"])
            if len(__bounds) != len(__background):
                raise ValueError("Initial background length does not match bounds number")
        #
        if __varnames is None:
            __names = ()
        else:
            __names = tuple(__varnames)
            if len(__names) != len(__background):
                raise ValueError("Initial background length does not match names number")
    #---------------------------------------------
    elif __format.upper() == "USER":
        __names, __background, __bounds = ImportScalarLinesFromFile(__bgfile).getvalue(__varnames)
    #---------------------------------------------
    for i,b in enumerate(__bounds) :
        if b[0] is not None and b[1] is not None and not (b[0] < b[1]) :
            raise ValueError(f'Inconsistent boundaries values for "{__names[i]}": {b[0]} not < {b[1]}')

    return (__names, __background, __bounds)

def _verify_existence_of_variable_in_dsin(__variable, __content, __number = 2):
    "Verify if the variable exist in the model file content"
    if "".join(__content).count(__variable) >= __number:
        return True
    else:
        return False

def _read_existing_variable_in_dsin(__variable, __content):
    "Return the value of the real variable"
    __previousline, __currentline = "", ""
    internalOrder = 0
    initialValuePart = False
    for line in __content:
        if not initialValuePart and "initialValue" not in line: continue
        if not initialValuePart and "initialValue" in line: initialValuePart = True
        __previousline = __currentline
        __currentline  = line
        if __variable in __currentline and "#" in __currentline and "#" not in __previousline:
            # Informations ecrites sur deux lignes successives
            vini, value, vmin, vmax = __previousline.split()
            # vcat, vtype, diez, vnam = __currentline.split()
            value = float(value)
            if float(vmin) >= float(vmax):
                vmin, vmax = None, None
            else:
                vmin, vmax = float(vmin), float(vmax)
            return (value, vmin, vmax)
        elif __variable in __currentline and "#" in __currentline and "#" in __previousline:
            # Informations ecrites sur une seule ligne
            vini, value, vmin, vmax, reste = __previousline.split(maxsplit=5)
            value = float(value)
            if float(vmin) >= float(vmax):
                vmin, vmax = None, None
            else:
                vmin, vmax = float(vmin), float(vmax)
            return (value, vmin, vmax)
    #
    raise ValueError("Value of variable %s not found in the file content"%__variable)

# ==============================================================================
def _readMethod(__filename="parameters.py", __format="ADAO"):
    """
    Read data assimilation method parameters

    Arguments:
        - File name
        - Format of the data (can be guessed)
    """
    if not os.path.isfile(__filename):
        raise ValueError('No such file or directory: %s'%str(__filename))
    #
    #---------------------------------------------
    if __format.upper() in ["GUESS", "ADAO"]:
        with open(__filename, 'r') as fid:
            exec(fid.read())
        __Algo   = locals().get("Algorithm", "3DVAR")
        __Params = locals().get("Parameters", {})
        __CovB   = locals().get("BackgroundError", 1.)
        __CovR   = locals().get("ObservationError", 1.)
        # __Xb     = locals().get("Background", __background)
        # if not isinstance(__Params, dict): __Params = {"Bounds":__bounds}
        # if "Bounds" not in __Params:       __Params["Bounds"] = __bounds
    #---------------------------------------------
    else:
        __Algo, __Params, __CovB, __CovR = "3DVAR", {}, 1., 1.
    #---------------------------------------------
    # if __Xb is None:
    #     raise ValueError("Background is not defined")
    # else:
    #     __Xb = numpy.ravel(__Xb)
    #
    return (__Algo, __Params, __CovB, __CovR)

# ==============================================================================
def _saveResults(__resultats, __filename=None, __level=None, __format="Guess", __verbose=False):
    """
    Save results relatively to the level required

    Arguments!
        - File name
        - Level of saving : final output only or intermediary with final output
        - Format of the data
    """
    if __filename is None:
        raise ValueError('A file to save results has to be named, please specify one')
    if __format.upper() == "GUESS":
        if __filename.split(".")[-1].lower() == "txt":
            __format = "TXT"
        elif __filename.split(".")[-1].lower() == "py":
            __format = "PY"
        else:
            raise ValueError("Can not guess the file format of \"%s\", please specify the good one"%__filename)
    else:
        __format     = str(__format).upper()
    if __format not in ["TXT", "PY"]:
        raise ValueError("Result file format \"%s\" is not valid."%__format)
    if __format == "PY" and os.path.splitext(__filename)[1] != ".py":
        __filename = os.path.splitext(__filename)[0] + ".py"
    #
    #---------------------------------------------
    if __format.upper() == "TXT":
        output = ["# Final results",]
        keys = list(__resultats.keys())
        keys.sort()
        for k in keys:
            __v = __resultats[k]
            if isinstance(__v, numpy.matrix):  # no1
                __v = __v.astype('float').tolist()
            elif isinstance(__v, numpy.ndarray):  # no2
                __v = tuple(__v.astype('float').tolist())
            else:
                __v = tuple(__v)
            output.append("%22s = %s"%(k,__v))
        output.append("")
        with open(__filename, 'w') as fid:
            fid.write( "\n".join(output) )
            fid.flush()
    #---------------------------------------------
    elif __format.upper() == "PY":
        output = ["# Final results",]
        keys = list(__resultats.keys())
        keys.sort()
        for k in keys:
            __v = __resultats[k]
            if isinstance(__v, numpy.matrix):  # no1
                __v = __v.astype('float').tolist()
            elif isinstance(__v, numpy.ndarray):  # no2
                __v = tuple(__v.astype('float').tolist())
            else:
                __v = tuple(__v)
            output.append("%s = %s"%(k,__v))
        output.append("")
        with open(__filename, 'w') as fid:
            fid.write( "\n".join(output) )
            fid.flush()
    #---------------------------------------------
    elif __format.upper() == "CSV":
        raise NotImplementedError("Not yet implemented")
    #---------------------------------------------
    elif __format.upper() == "DICT":
        raise NotImplementedError("Not yet implemented")
    #---------------------------------------------
    if __verbose: # Format TXT
        output = ["# Final results",]
        keys = list(__resultats.keys())
        keys.sort()
        for k in keys:
            __v = __resultats[k]
            if isinstance(__v, numpy.matrix):  # no1
                __v = __v.astype('float').tolist()
            elif isinstance(__v, numpy.ndarray):  # no2
                __v = tuple(__v.astype('float').tolist())
            else:
                __v = tuple(__v)
            output.append("%22s = %s"%(k,__v))
        output.append("")
        print( "\n".join(output) )
    #---------------------------------------------
    return True

def _secure_copy_textfile(__original_file, __destination_file):
    "Copy the file guranteeing that it is copied"


    shutil.copy(
                __original_file,
                __destination_file
                )
    shutil.copystat( # commande pour assurer que le fichier soit bien copié
        __original_file,
        __destination_file
        )
    os.path.getsize(__destination_file)# commande bis pour assurer que le fichier soit bien copié

    def file_len(fname):
        count = 0
        with open(fname) as f:
            for line in f:
                count += 1
        return count

    while file_len(__original_file)!= file_len(__destination_file):
        shutil.copy(
            __original_file,
            __destination_file
            )

# ==============================================================================
class Python_Simulation(object):
    def __init__(self, simu_dir=".", val_inputs=(), logfile=True, timeout=60, verbose=True):
        self.__simu_dir = os.path.abspath(simu_dir)
        self.__inputs = numpy.ravel(val_inputs)
        if verbose:
            print()
            print("  [VERBOSE] Input values %s"%self.__inputs)

    def single_simulation(self, __inputs = None):
        with open(os.path.join(self.__simu_dir,"pythonsim.exe"), 'r') as fid:
            exec(fid.read())
        __directoperator = locals().get("DirectOperator", None)
        if __inputs is None: __inputs = self.__inputs
        return __directoperator(__inputs)

# ==============================================================================
class VersionsLogicielles (object):
    "Modules version information"
    def __init__(self):
        print("  [VERBOSE] System configuration:")
        print("      - Python...:",sys.version.split()[0])
        print("      - Numpy....:",numpy.version.version)
        print("      - Scipy....:",scipy.version.version)
        print("      - ADAO.....:",adao.version)
        print("")

def TOP_LEVEL_exefmuMultiobs_ref( x_values_matrix , VariablesToCalibrate=None, OutputVariables=None, ref_simudir = None,  ModelName = None ):
    "Appel du modèle en format FMU et restitution des résultats"
    x_values = list(numpy.ravel(x_values_matrix))
    x_inputs=dict(zip(VariablesToCalibrate,x_values))

    fmuname = os.path.basename(ModelName) #in case ModelName is given as a path (works also if it is a file name)
    fmu = os.path.join(ref_simudir,fmuname)

    reader = simulate_fmu(fmu, output = OutputVariables, start_values = x_inputs)
    y_values = [reader[y_name][-1] for y_name in OutputVariables]
    y_values_matrix = numpy.asarray(y_values)

    return y_values_matrix

def TOP_LEVEL_exefmuMultiobs( x_values_matrix , VariablesToCalibrate=None, OutputVariables=None,  LNames = None, LColumns = None, LVariablesToChange=None, ref_simudir = None,  ModelName = None, List_Multideltatime = None, AdvancedDebugModel = None, TimeoutModelExecution = None, FMUInput = None):
    "Appel du modèle en format FMU et restitution des résultats"

    if VariablesToCalibrate is None:
        raise ValueError("VariablesToCalibrate")

    if OutputVariables is None:
        raise ValueError("OutputVariables")

    if LNames is None:
        raise ValueError("LNames")

    if LColumns is None:
        raise ValueError("LColumns")

    if LVariablesToChange is None:
        raise ValueError("LVariablesToChange")

    if ref_simudir is None:
        raise ValueError("ref_simudir")

    if List_Multideltatime is None:
        raise ValueError("Problem defining simulation output results")

    if AdvancedDebugModel is None:
        raise ValueError("AdvancedDebugModel")

    if TimeoutModelExecution is None:
        raise ValueError("TimeoutModelExecution")

    x_values = list(numpy.ravel(x_values_matrix))
    x_inputs=dict(zip(VariablesToCalibrate,x_values))

    if os.path.isfile(ModelName):
        fmuname = os.path.basename(ModelName)
    elif os.path.isdir(ModelName):
        fmuname = [files for files in os.listdir(os.path.abspath(ModelName)) if files[-4:] =='.fmu'][0]

    fmu = os.path.join(ref_simudir,fmuname)

    multi_y_values_matrix = []

    for etat in range(len(LNames)):
        y_values =[]

        try: #to handle situations in which there is only one CL (boundary conditions) file
            var_int = numpy.ravel(LColumns[:,etat])
        except Exception:
            var_int = numpy.ravel(LColumns)

        dict_inputs = dict(zip(LVariablesToChange, var_int))
        #
        dict_inputs.update(x_inputs)

        if FMUInput:
            fmu_inputs = FMUInput[LNames[etat]]
            timestep = fmu_inputs[1][0] - fmu_inputs[0][0]  # Assuming constant timestep
            if AdvancedDebugModel: print(f'The timestep for {LNames[etat]} is {timestep} seconds')
        else:
            fmu_inputs = None
            timestep = None

        try:
            stoptime_fmu = List_Multideltatime[etat][-1]

        except IndexError:
            stoptime_fmu = None


        if AdvancedDebugModel == True:
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            start_time_simulation_fmi = time.time()  # timeout manangement since fmpy does not raise an error for this, it just ends the simulations and continues

            try :
                reader = simulate_fmu(fmu, output = OutputVariables, start_values = dict_inputs, debug_logging = True, timeout = TimeoutModelExecution, input = fmu_inputs, stop_time= stoptime_fmu, output_interval= timestep)
            except FMICallException as e:
                output = new_stdout.getvalue()
                sys.stdout = old_stdout
                print('[ERROR] Failed simulation with the following input:\n',dict_inputs)
                raise e

            elapsed_time_simulation_fmi =  time.time() - start_time_simulation_fmi
            if elapsed_time_simulation_fmi > TimeoutModelExecution:
                raise TimeoutError("Timeout for simulation reached, please increase it in order to be able to simulate your model and/or check if your model is correct (use TimeoutModelExecution option in configuration.py file)")

            output = new_stdout.getvalue()
            sys.stdout = old_stdout

            dir_run=ref_simudir
            log_file=os.path.join(dir_run,
                                  'log_debug_model.txt')
            try: #try toremove the previous file
                os.remove(log_file)
            except Exception:
                pass

            f=open(log_file,'a')
            for line in output:
                f.write(line)

        else:
            start_time_simulation_fmi = time.time()

            try :
                reader = simulate_fmu(fmu, output = OutputVariables, start_values = dict_inputs, timeout = TimeoutModelExecution, input = fmu_inputs, stop_time= stoptime_fmu, output_interval= timestep)
            except FMICallException as e:
                print('[ERROR] Failed simulation with the following input:\n',dict_inputs)
                raise e

            elapsed_time_simulation_fmi =  time.time() - start_time_simulation_fmi
            if elapsed_time_simulation_fmi > TimeoutModelExecution:
                raise TimeoutError("Timeout for simulation reached, please increase it in order to be able to simulate your model and/or check if your model is correct (use TimeoutModelExecution option in configuration.py file)")

        y_whole = [reader[y_name] for y_name in OutputVariables]

        for y_ind in range(len(OutputVariables)):
            y_ind_whole_values = y_whole[y_ind]
            y_ind_whole_time = reader['time'] #standard output of fmu

            if len(List_Multideltatime[etat])>1:
                index_y_values = [find_nearest_index(y_ind_whole_time,time)[0] for time in List_Multideltatime[etat]]
            else:
                index_y_values = [-1] #we only take the last point if one measure point
            y_ind_values = [y_ind_whole_values[i] for i in index_y_values]
            y_values = y_values + y_ind_values

        y_values_matrix = y_values #pbs in results management
        multi_y_values_matrix = multi_y_values_matrix + y_values_matrix

    y_values_matrix_def = numpy.ravel(numpy.array(multi_y_values_matrix))
    return y_values_matrix_def

def TOP_LEVEL_exeOpenModelicaMultiobs( x_values_matrix , KeepCalculationFolders = None, VariablesToCalibrate=None, OutputVariables=None,  LNames = None, LColumns = None, LVariablesToChange=None, ref_simudir = None,  ModelName = None, List_Multideltatime = None, Linux = None, AdvancedDebugModel = None, TimeoutModelExecution = None):
    "Appel du modèle en format OpenModelica et restitution des résultats"

    if VariablesToCalibrate is None:
        raise ValueError("VariablesToCalibrate")

    if OutputVariables is None:
        raise ValueError("OutputVariables")

    if LNames is None:
        raise ValueError("LNames")

    if LColumns is None:
        raise ValueError("LColumns")

    if LVariablesToChange is None:
        raise ValueError("LVariablesToChange")

    if ref_simudir is None:
        raise ValueError("ref_simudir")

    if KeepCalculationFolders is None:
        raise ValueError("KeepCalculationFolders")

    if Linux is None:
        raise ValueError("Linux")

    if List_Multideltatime is None:
        raise ValueError("Problem defining simulation output results")

    if AdvancedDebugModel is None:
        raise ValueError("AdvancedDebugModel")

    if TimeoutModelExecution is None:
        raise ValueError("TimeoutModelExecution")

    x_values = list(numpy.ravel(x_values_matrix))
    x_inputs=dict(zip(VariablesToCalibrate,x_values))

    if os.path.isfile(ModelName):
        om_xml = os.path.basename(ModelName)
    elif os.path.isdir(ModelName):
        om_xml = [files for files in os.listdir(os.path.abspath(ModelName)) if files[-4:] =='.xml'][0]

    om_xml = os.path.abspath(os.path.join(ref_simudir,om_xml))

    multi_y_values_matrix = []

    for etat in range(len(LNames)):
        y_values =[]

        try: #to handle situations in which there is only one CL (boundary conditions) file
            var_int = numpy.ravel(LColumns[:,etat])
        except Exception:
            var_int = numpy.ravel(LColumns)

        dict_inputs = dict(zip(LVariablesToChange, var_int))
        #

        dict_inputs.update(x_inputs)


        results_dir = tempfile.mkdtemp( dir=os.path.dirname(om_xml) ) #to handle parallel computation

        results_file_name = os.path.join(results_dir,os.path.basename(om_xml)[:-9] + '_' + LNames[etat].replace('.','_') + ".mat")

        OM_execution = run_OM_model(om_xml, dict_inputs = dict_inputs, result_file_name = results_file_name , Linux = Linux, AdvancedDebugModel = AdvancedDebugModel, TimeoutModelExecution = TimeoutModelExecution)

        try:
            reader = Reader(results_file_name,'dymola') #dymola even if it is OpenModelica
        except Exception:
            raise ValueError("Simulation cannot be performed: reduce the number of parameters to calibrate and/or the range in which their optimal value should be found (or modify and simplify the model to make it easier to simulate)" )

        y_whole = [reader.values(y_name) for y_name in OutputVariables]

        for y_ind in range(len(OutputVariables)):
            y_ind_whole_values = y_whole[y_ind][1]
            y_ind_whole_time = y_whole[y_ind][0]

            if len(List_Multideltatime[etat])>1:
                index_y_values = [find_nearest_index(y_ind_whole_time,time)[0] for time in List_Multideltatime[etat]]
            else:
                index_y_values = [-1] #we only take the last point if one measure point

            y_ind_values = [y_ind_whole_values[i] for i in index_y_values]
            y_values = y_values + y_ind_values
#        y_values_matrix = numpy.asarray(y_values)
        y_values_matrix = y_values #pbs in results management
        multi_y_values_matrix = multi_y_values_matrix + y_values_matrix

        if not KeepCalculationFolders:
            shutil.rmtree(results_dir, ignore_errors=True)

    y_values_matrix_def = numpy.ravel(numpy.array(multi_y_values_matrix))

    return y_values_matrix_def

def TOPLEVEL_exedymosimMultiobs_simple( x_values_matrix , VariablesToCalibrate=None, OutputVariables=None, LNames = None, ref_simudir = None, KeepCalculationFolders = None, Linux = None, List_Multideltatime = None, AdvancedDebugModel = None, TimeoutModelExecution = None):
    "Appel du modèle en format DYMOSIM et restitution des résultats"


    if VariablesToCalibrate is None:
        raise ValueError("VariablesToCalibrate")

    if OutputVariables is None:
        raise ValueError("OutputVariables")

    if LNames is None:
        raise ValueError("LNames")

    if ref_simudir is None:
        raise ValueError("ref_simudir")

    if KeepCalculationFolders is None:
        raise ValueError("KeepCalculationFolders")

    if Linux is None:
        raise ValueError("Linux")

    if List_Multideltatime is None:
        raise ValueError("Problem defining simulation output results")

    if AdvancedDebugModel is None:
        raise ValueError("AdvancedDebugModel")

    if TimeoutModelExecution is None:
        raise ValueError("TimeoutModelExecution")
    #
    # x_values = list(numpy.ravel(x_values_matrix) * Background)
    x_values = list(numpy.ravel(x_values_matrix))
    x_inputs=dict(zip(VariablesToCalibrate,x_values))
    # if Verbose: print("  Simulation for %s"%numpy.ravel(x_values))
    #

    multi_y_values_matrix = []

    for etat in range(len(LNames)):
        y_values =[]

        simudir = tempfile.mkdtemp( dir=ref_simudir )
        #
        dict_inputs ={}
        dict_inputs.update( x_inputs )
        #
        shutil.copy(
            os.path.join(ref_simudir, str("dsin_" +LNames[etat]+ ".txt")),
            os.path.join(simudir, str("dsin_" +LNames[etat]+ ".txt"))
            )
        _secure_copy_textfile(
                        os.path.join(ref_simudir, str("dsin_" +LNames[etat]+ ".txt")),
                        os.path.join(simudir, str("dsin_" +LNames[etat]+ ".txt"))
                        )

        auto_simul = Automatic_Simulation(
                                        simu_dir = simudir,
                                        dymosim_path = os.path.join(ref_simudir,os.pardir) ,
                                        dsin_name = str("dsin_" +LNames[etat]+ ".txt"),
                                        dsres_path = os.path.join(simudir, str("dsres" +LNames[etat]+ ".mat")),
                                        dict_inputs = dict_inputs,
                                        logfile = True,
                                        timeout = TimeoutModelExecution,
                                        without_modelicares = True,
                                        linux=Linux,
                                        )
        auto_simul.single_simulation()

        if AdvancedDebugModel:
            dslog_file = os.path.join(simudir, 'dslog.txt')
            debug_model_file = os.path.join(ref_simudir,'log_debug_model.txt')
            try:
                shutil.copy(dslog_file,debug_model_file)
            except Exception:
                pass

        if auto_simul.success_code == 2 :
            raise ValueError("The simulation falis after initialization, please check the log file and your model in order to be sure that the whole simulation can be performed (specially for dynamic models)")

        if auto_simul.success_code == 3 :
            raise ValueError("The simulation did not reach the final time, probably due to a lack of time, please increase the time for model execution by modifying the TimeoutModelExecution value in configuration.py")

        if auto_simul.success_code == 0:
            pass #means that everything OK, we keep going
        else  :
            raise ValueError("The NeedInitVariables iteration should be set to True, convergence issues found for %s" % str(LNames[etat])) #means this value is 1--> not correct initialization

        reader = Reader(os.path.join(simudir, str("dsres" +LNames[etat]+ ".mat")),'dymola')

        y_whole = [reader.values(y_name) for y_name in OutputVariables]

        for y_ind in range(len(OutputVariables)):
            y_ind_whole_values = y_whole[y_ind][1]
            y_ind_whole_time = y_whole[y_ind][0]

            if len(List_Multideltatime[etat])>1:
                index_y_values = [find_nearest_index(y_ind_whole_time,time)[0] for time in List_Multideltatime[etat]]
            else:
                index_y_values = [-1] #we only take the last point if one measure point

            y_ind_values = [y_ind_whole_values[i] for i in index_y_values]
            y_values = y_values + y_ind_values
#        y_values_matrix = numpy.asarray(y_values)
        y_values_matrix = y_values #pbs in results management
        multi_y_values_matrix = multi_y_values_matrix + y_values_matrix

        if not KeepCalculationFolders:
            shutil.rmtree(simudir, ignore_errors=True)

    y_values_matrix_def = numpy.ravel(numpy.array(multi_y_values_matrix))
    return y_values_matrix_def

def TOP_LEVEL_exedymosimMultiobs( x_values_matrix , VariablesToCalibrate=None, OutputVariables=None, LNames = None, ModelFormat = None, KeepCalculationFolders = None, Verbose = None, dict_dsin_paths = None, Linux = None, List_Multideltatime = None, AdvancedDebugModel = None, TimeoutModelExecution = None): #2ème argument à ne pas modifier
    "Appel du modèle en format DYMOSIM et restitution des résultats"

    if VariablesToCalibrate is None:
        raise ValueError("VariablesToCalibrate")

    if OutputVariables is None:
        raise ValueError("OutputVariables")

    if LNames is None:
        raise ValueError("LNames")

    if ModelFormat is None:
        raise ValueError("ModelFormat")

    if KeepCalculationFolders is None:
        raise ValueError("KeepCalculationFolders")

    if Verbose is None:
        raise ValueError("Verbose")

    if dict_dsin_paths is None:
        raise ValueError("dict_dsin_paths")

    if Linux is None:
        raise ValueError("Linux")

    if List_Multideltatime is None:
        raise ValueError("Problem defining simulation output results")

    if AdvancedDebugModel is None:
        raise ValueError("AdvancedDebugModel")

    if TimeoutModelExecution is None:
        raise ValueError("TimeoutModelExecution")
#
    # x_values = list(numpy.ravel(x_values_matrix) * Background)
    x_values = list(numpy.ravel(x_values_matrix))
    x_inputs = dict(zip(VariablesToCalibrate,x_values))
    x_inputs_for_CWP = {}
    # if Verbose: print("  Simulation for %s"%numpy.ravel(x_values))

    multi_y_values_matrix = []



    for etat in range(len(LNames)):
        y_values =[]

        ref_simudir = Calibration._setModelTmpDir( None,dict_dsin_paths[LNames[etat]], ModelFormat,   'dsin.txt', os.path.join(os.path.pardir,os.path.pardir),  LNames[etat])
        simudir = ref_simudir
        dict_inputs={}
        dict_inputs.update(x_inputs)


        auto_simul = Automatic_Simulation(
            simu_dir=simudir,
            dymosim_path = os.path.join(simudir, os.pardir, os.pardir) ,
            dsres_path = os.path.join(simudir, str("dsres" +LNames[etat]+ ".mat")),
            dict_inputs=dict_inputs,
            logfile=True,
            timeout=TimeoutModelExecution,
            without_modelicares=True,
            linux=Linux
            )
        auto_simul.single_simulation()

        if AdvancedDebugModel:
            dslog_file = os.path.join(simudir, 'dslog.txt')
            debug_model_file = os.path.join(simudir, os.pardir, 'log_debug_model.txt')
            try:
                shutil.copy(dslog_file,debug_model_file)
            except Exception:
                pass

        if auto_simul.success_code == 2 :
            raise ValueError("The simulation falis after initialization, please check the log file and your model in order to be sure that the whole simulation can be performed (specially for dynamic models)")

        if auto_simul.success_code == 3 :
            raise ValueError("The simulation did not reach the final time, probably due to a lack of time, please increase the time for model execution by modifying the TimeoutModelExecution value in configuration.py")


        if auto_simul.success_code == 0:
            reader = Reader(os.path.join(simudir, str("dsres" +LNames[etat]+ ".mat")),'dymola')

        else:

            path_around_simu = os.path.join(simudir,os.path.pardir,os.path.pardir)
            around_simu = Around_Simulation(dymola_version='2012',
                              curdir=path_around_simu,
                              source_list_iter_var = 'from_dymtranslog',
                              copy_from_dym_trans_log= os.path.join(path_around_simu,'ini.txt'),
                              mat = os.path.join(os.path.dirname(dict_dsin_paths[LNames[etat]]), str("REF_for_CWP" + ".mat")),
                              iter_var_values_options={'source':'from_mat','moment':'initial'},
                              verbose = False)
            around_simu.set_list_iter_var()
            around_simu.set_dict_iter_var()

            reader_CWP = Reader(os.path.join(os.path.dirname(dict_dsin_paths[LNames[etat]]), str("REF_for_CWP" + ".mat")),'dymola')
            x_values_intemediary = [reader_CWP.values(x_name)[1][-1] for x_name in VariablesToCalibrate]
            x_values_from_last_calculation = numpy.asarray(x_values_intemediary)
            x_inputs_from_last_calculation = dict(zip(VariablesToCalibrate,x_values_from_last_calculation))


            for var_calib in x_inputs_from_last_calculation.keys():
                x_inputs_for_CWP[var_calib] = (x_inputs_from_last_calculation[var_calib], x_inputs[var_calib])

            dict_var_to_fix2 = Dict_Var_To_Fix(option='automatic',
                                  dict_auto_var_to_fix=x_inputs_for_CWP)

            dict_var_to_fix2.set_dict_var_to_fix()

            if Verbose:
                LOG_FILENAME = os.path.join(simudir,'change_working_point.log')
                for handler in logging.root.handlers[:]:
                    logging.root.removeHandler(handler)
                logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode='w')

            working_point_modif = Working_Point_Modification(main_dir = simudir,
                         simu_material_dir = simudir,
                         dymosim_path = os.path.join(simudir, os.pardir, os.pardir),
                         simu_dir = 'SIMUS',
                         store_res_dir = 'RES',
                         dict_var_to_fix = dict_var_to_fix2.dict_var_to_fix,
                         around_simulation0 = around_simu,
                         var_to_follow_path= os.path.join(simudir,'var_to_follow.csv'),
                         gen_scripts_ini= False,
                         nit_max= 1000000000000000,
                         min_step_val = 0.00000000000005,
                         timeout = TimeoutModelExecution,
                         linux=Linux)

            working_point_modif.create_working_directory()
            working_point_modif.working_point_modification(skip_reference_simulation=True)

            if AdvancedDebugModel:
                dslog_file = os.path.join(simudir,'SIMUS', 'dslog.txt')
                debug_model_file = os.path.join(simudir, os.pardir, 'log_debug_model.txt')
                try:
                    shutil.copy(dslog_file,debug_model_file)
                except Exception:
                    pass
            try:
                reader = Reader(os.path.join(simudir, 'RES','1.0.mat'),'dymola')
            except Exception:
                raise ValueError("Simulation cannot be performed: reduce the number of parameters to calibrate and/or the range in which their optimal value should be found (or modify and simplify the model to make it easier to simulate)" )


        y_whole = [reader.values(y_name) for y_name in OutputVariables]

        for y_ind in range(len(OutputVariables)):
            y_ind_whole_values = y_whole[y_ind][1]
            y_ind_whole_time = y_whole[y_ind][0]
            if len(List_Multideltatime[etat])>1:
                index_y_values = [find_nearest_index(y_ind_whole_time,time)[0] for time in List_Multideltatime[etat]]
            else:
                index_y_values = [-1] #we only take the last point if one measure point

            y_ind_values = [y_ind_whole_values[i] for i in index_y_values]
            y_values = y_values + y_ind_values
#        y_values_matrix = numpy.asarray(y_values)
        y_values_matrix = y_values #pbs in results management
        multi_y_values_matrix = multi_y_values_matrix + y_values_matrix

        if not KeepCalculationFolders:
            shutil.rmtree(simudir, ignore_errors=True)
    y_values_matrix_def = numpy.ravel(numpy.array(multi_y_values_matrix))
    return y_values_matrix_def

def run_OM_model(xml_file, #req arg, file path to _init.xml file
                 result_file_name = None, #file path for storing results
                 dict_inputs = None, #optionnal argument : for overriding paramters
                 Linux = False,
                 AdvancedDebugModel = None,
                 TimeoutModelExecution = None):

    Command=[] #initialize command with list of argument

    xml_file = os.path.abspath(xml_file)

    #set main command to be runned
    if Linux:
        OM_binary = xml_file.replace('_init.xml','') # not tested
    else: #WIndows
        OM_binary = xml_file.replace('_init.xml','.exe')
    Command.append(OM_binary)

    #Get base path for binaries and input


    inputPath='-inputPath='+os.path.dirname(xml_file)
    Command.append(inputPath)

    #Generate override command
    if dict_inputs !=None:
        Override='-override='
        for elt in dict_inputs.items():
            Override=Override+elt[0]+'='+str(elt[1])+','
        Override=Override.rstrip(',') #remove last ',' if any
        Command.append(Override)

    #Generate name of result file
    if result_file_name != None:
        result='-r='+result_file_name
        Command.append(result)
    else:
        result='-r='+OM_binary+'.mat' #by default result is stored next to _init and bin file
        Command.append(result)

    result='-w' #by default result is stored next to _init and bin file
    Command.append(result)

    result='-lv='+'LOG_STATS,LOG_NLS_V' #by default result is stored next to _init and bin file
    Command.append(result)

    inputPath='-outputPath='+os.path.dirname(xml_file)
    Command.append(inputPath)

   #launch calculation
    proc = subprocess.Popen(Command, #Command in the form of a text list
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    # for line in proc.stdout.readlines():
    #     print(line)

    if AdvancedDebugModel == True:
        dir_run=os.path.join(os.path.dirname(result_file_name),os.pardir)
        log_file=os.path.join(dir_run,
                              'log_debug_model.txt')

        try:
            os.remove(log_file)
        except Exception:
            pass
        try:
            f=open(log_file,'a')
            for line in proc.stdout.readlines():
                f.write(line)
            f.close()
            proc.communicate(timeout = TimeoutModelExecution)
        except subprocess.TimeoutExpired:
            raise ValueError("Timeout for simulation reached, please increase it in order to be able to simulate your model and/or check if your model is correct (use TimeoutModelExecution option in configuration.py file)")

    else:
        try:
            proc.communicate(timeout = TimeoutModelExecution)
        except Exception:
            raise ValueError("Timeout for simulation reached, please increase it in order to be able to simulate your model and/or check if your model is correct (use TimeoutModelExecution option in configuration.py file)")

    # proc.communicate()

    # r = proc.poll()
    # while r !=0:
    #     r = proc.poll()

    # if proc.returncode !=0:
    #     raise ValueError("Simulation not ended")


    # sys.stdout.flush()
    # sys.stderr.flush()

    # dir_run=os.path.dirname(result_file_name)
    # log_file=os.path.join(dir_run,
    #                       'log.txt')
    # try:
    #     proc.wait(timeout=50)

    #     f=open(log_file,'a')
    #     for line in proc.stdout.readlines():
    #         f.write(line)

    #     f.close()
    #     return_code=proc.returncode

    # except subprocess.TimeoutExpired:

    #     f=open(log_file,'a')
    #     for line in proc.stdout.readlines():
    #         f.write(line)

    #     f.write('Simulation stoppe because of TimeOut')
    #     f.close()

    #     return_code=2

    return #return_code

def readObsnamesfile(__filenames=None):
    "Provisionnel pour lire les noms des observations d'un fichier"
    for __filename in __filenames:
        try:
            df = pandas.read_csv(__filename, sep = ";", header =0) #so that repeated names are not modified
            obsnames_infile = df.loc[0, :].values.tolist()[2:]
        except Exception:
            df_tmp = pandas.read_csv(__filename, sep = ";", header =1)
            with open(__filename, 'r') as infile:
                readie=csv.reader(infile, delimiter=';')
                with open('tmp_obs_file.csv', 'wt', newline='') as output:
                    outwriter=csv.writer(output, delimiter=';')
                    list_row = ['#'] + df_tmp.columns
                    outwriter.writerow(list_row)
                    for row in readie:
                         outwriter.writerow(row)

            df = pandas.read_csv('tmp_obs_file.csv', sep = ";", header =0) #so that repeated names are not modified
            df = df.iloc[1: , :]
            obsnames_infile = df.iloc[0, :].values.tolist()[2:]

            try:
                os.remove('tmp_obs_file.csv')
            except Exception:
                pass
    return obsnames_infile

def readDatesHours(__filename=None):
    "Provisionnel pour lire les heures et les dates d'une simulation dynamique"
    df = pandas.read_csv(__filename, sep = ";", header =1)
    dates = numpy.array(df['Date'])
    hours = numpy.array(df['Hour'])
    return (dates,hours)

def readMultiDatesHours(__filenames=None):
    "Provisionnel pour lire les heures et les dates d'une simulation dynamique dans le cas multi-observations"
    Multidates =[]
    Multihours = []
    for __filename in __filenames:
        df = pandas.read_csv(__filename, sep = ";", header =1)
        dates = numpy.array(df[df.columns[0]])
        hours = numpy.array(df[df.columns[1]])
        Multidates.append( dates )
        Multihours.append( hours )
    return (Multidates,Multihours)

def find_nearest_index(array, value):
    "Trouver le point de la simulation qui se rapproche le plus aux observations"
    array = numpy.asarray(array)
    idx = (numpy.abs(array - value)).argmin()
    return [idx, array[idx]]
# ==============================================================================
if __name__ == "__main__":
    print('\n  AUTODIAGNOSTIC\n  ==============\n')
    print("  Module name..............: %s"%name)
    print("  Module version...........: %s"%version)
    print("  Module year..............: %s"%year)
    print("")
    print("  Configuration attributes.:")
    for __k, __v in _configuration.items():
        print("%26s : %s"%(__k,__v))
    print("")
