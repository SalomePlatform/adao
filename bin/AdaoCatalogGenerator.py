# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2019 EDF R&D
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
import traceback
import sys
import io
import os

import module_version

logging.basicConfig(level=logging.WARNING)

if sys.version_info.major > 2:
    def unicode(text, encoding='utf-8'): return text

print("-- Starting AdaoCalatogGenerator.py --")

try:
  import adao
  import daEficas
  import daYacsSchemaCreator
  import daCore.AssimilationStudy
  import daYacsSchemaCreator.infos_daComposant as infos
except:
  logging.fatal("Import of ADAO python modules failed !" +
                "\n add ADAO python installation directory in your PYTHONPATH")
  traceback.print_exc()
  sys.exit(1)

#----------- Templates Part ---------------#
begin_catalog_file = """# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2019 EDF R&D
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
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

# --------------------------------------------------------
# Generated by AdaoCatalogGenerator on {date}
# --------------------------------------------------------

import os, re
import Accas
from Accas import *

JdC = JDC_CATA (
    code = '%s',
    execmodul = None,
    regles = ( AU_MOINS_UN ('ASSIMILATION_STUDY','CHECKING_STUDY'), AU_PLUS_UN ('ASSIMILATION_STUDY','CHECKING_STUDY')),
    )
VERSION_CATALOGUE='%s'

def NoCheckInNS(filename):
    return 1
NoCheckInNS.info = u""
def DirectOperatorInNS(filename):
    if os.path.exists(filename):
        fc = open(filename, 'r').readlines()
        cr = re.compile("^def[\s]*DirectOperator[\s]*\(")
        for ln in fc:
            if cr.match(ln): return 1
        cr = re.compile("^DirectOperator[\s]*=")
        for ln in fc:
            if cr.match(ln): return 1
    return 0
DirectOperatorInNS.info = u"The Python file has to contain explicitly a \\"DirectOperator\\" function definition with only one vector as argument."
def TangentOperatorInNS(filename):
    if os.path.exists(filename):
        fc = open(filename, 'r').readlines()
        cr = re.compile("^def[\s]*TangentOperator[\s]*\(")
        for ln in fc:
            if cr.match(ln): return 1
        cr = re.compile("^TangentOperator[\s]*=")
        for ln in fc:
            if cr.match(ln): return 1
    return 0
TangentOperatorInNS.info = u"The Python file has to contain explicitly a \\"TangentOperator\\" function definition with only one pair of vectors as argument."
def AdjointOperatorInNS(filename):
    if os.path.exists(filename):
        fc = open(filename, 'r').readlines()
        cr = re.compile("^def[\s]*AdjointOperator[\s]*\(")
        for ln in fc:
            if cr.match(ln): return 1
        cr = re.compile("^AdjointOperator[\s]*=")
        for ln in fc:
            if cr.match(ln): return 1
    return 0
AdjointOperatorInNS.info = u"The Python file has to contain explicitly an \\"AdjointOperator\\" function definition with only one pair of vectors as argument."
def ColDataFileExtVal(filename):
    __readable = (".csv", ".tsv", ".txt", ".npy", ".npz")
    if os.path.exists(filename) and os.path.splitext(filename)[1] in __readable:
        return 1
    return 0
ColDataFileExtVal.info = u"The data file has to contain explicitly one or more number columns with separator, or one variable, that can fit in a unique continuous vector."
"""%(module_version.name,module_version.cata)

# Important : validators=[...] pour que les conditions soient traitees simultanement, en "ET", et pas en "OU" (choisi dans le cas du tuple a la place de la liste)
# validators=[OnlyStr(), FileExtVal('py'), FunctionVal(fv)]
data_method = """
def F_{data_name}(statut, fv=NoCheckInNS) : return FACT(
    statut = statut,
    FROM = SIMP(statut = "o", typ = "TXM", into=({data_into}), defaut={data_default}),
    SCRIPT_DATA = BLOC ( condition = " FROM in ( 'Script', ) ",
        SCRIPT_FILE = SIMP(statut = "o", typ = ("FichierNoAbs",'Python Files (*.py)',), validators=[OnlyStr(), FileExtVal('py'), FunctionVal(fv)], fr="En attente d'un nom de fichier script, avec ou sans le chemin complet pour le trouver, contenant si nécessaire la définition d'une variable interne de même nom que le concept parent", ang="Waiting for a script file name, with or without the full path to find it, containing if necessary the definition of an internal variable of the same name as the parent concept"),
        ),
    DATA_DATA = BLOC ( condition = " FROM in ( 'DataFile', ) ",
        DATA_FILE = SIMP(statut = "o", typ = ("FichierNoAbs",'CSV Text Files (*.csv);;TSV Text Files (*.tsv);;TXT Text Files (*.txt);;NPY Binary Numpy Files (*.npy);;NPZ Binary Numpy Files (*.npz);;All Files (*)", ',), validators=[OnlyStr(), FunctionVal(ColDataFileExtVal)], fr="En attente d'un nom de fichier de données, avec ou sans le chemin complet pour le trouver, contenant ou plusieurs colonnes pour définir un unique vecteur continu", ang="Waiting for a data file name, with or without the full path to find it, containing one or more columns to define a unique continuous vector"),
        ColMajor = SIMP(statut="f", typ = "I", into=(0, 1), defaut=0, fr="Variables en colonnes acquises ligne par ligne (0) ou colonne par colonne (1)", ang="Variables in columns acquired line by line (0) or column by column (1)"),
        ),
    STRING_DATA = BLOC ( condition = " FROM in ( 'String', ) ",
        STRING = SIMP(statut = "o", typ = "TXM",{ms_default} fr="En attente d'une chaine de caractères entre guillements. Pour construire un vecteur ou une matrice, ce doit être une suite de nombres, utilisant un espace ou une virgule pour séparer deux éléments et un point-virgule pour séparer deux lignes", ang="Waiting for a string in quotes. To build a vector or a matrix, it has to be a float serie, using a space or comma to separate two elements in a line, a semi-colon to separate rows"),
        ),
    SCRIPTWITHFUNCTIONS_DATA = BLOC ( condition = " FROM in ( 'ScriptWithFunctions', ) ",
        SCRIPTWITHFUNCTIONS_FILE = SIMP(statut = "o", typ = "FichierNoAbs", validators=[OnlyStr(), FileExtVal('py'), FunctionVal(DirectOperatorInNS), FunctionVal(TangentOperatorInNS), FunctionVal(AdjointOperatorInNS)], fr="En attente d'un nom de fichier script, avec ou sans le chemin complet pour le trouver, contenant en variables internes trois fonctions de calcul nommées DirectOperator, TangentOperator et AdjointOperator", ang="Waiting for a script file name, with or without the full path to find it, containing as internal variables three computation functions named DirectOperator, TangentOperator and AdjointOperator"),
        ),
    SCRIPTWITHONEFUNCTION_DATA = BLOC ( condition = " FROM in ( 'ScriptWithOneFunction', ) ",
        SCRIPTWITHONEFUNCTION_FILE = SIMP(statut = "o", typ = "FichierNoAbs", validators=[OnlyStr(), FileExtVal('py'), FunctionVal(DirectOperatorInNS)], fr="En attente d'un nom de fichier script, avec ou sans le chemin complet pour le trouver, contenant en variable interne une seule fonction de calcul nommée DirectOperator", ang="Waiting for a script file name, with or without the full path to find it, containing as internal variable only one function named DirectOperator"),
        DifferentialIncrement = SIMP(statut="o", typ = "R", val_min=0, val_max=1, defaut=0.01, fr="Incrément de la perturbation dX pour calculer la dérivée, construite en multipliant X par l'incrément en évitant les valeurs nulles", ang="Increment of dX perturbation to calculate the derivative, build multiplying X by the increment avoiding null values"),
        CenteredFiniteDifference = SIMP(statut="o", typ = "I", into=(0, 1), defaut=0, fr="Formulation centrée (1) ou décentrée (0) pour la méthode des différences finies", ang="Centered (1) or uncentered (0) formulation for the finite differences method"),
        EnableMultiProcessing = SIMP(statut="f", typ = "I", into=(0, 1), defaut=0, fr="Calculs élémentaires effectués en séquentiel (0) ou en parallèle (1) dans la méthode des différences finies", ang="Elementary calculations done sequentially (0) or in parallel (1) in the finite differences method"),
        NumberOfProcesses = SIMP(statut="f", typ = "I", val_min=0, defaut=0, fr="Nombre de processus parallèles, 0 pour un contrôle automatique", ang="Number of parallel processes, 0 for automatic control"),
        ),
    SCRIPTWITHSWITCH_DATA = BLOC ( condition = " FROM in ( 'ScriptWithSwitch', ) ",
        SCRIPTWITHSWITCH_FILE = SIMP(statut = "o", typ = "FichierNoAbs", validators=[OnlyStr(), FileExtVal('py')], fr="En attente d'un nom de fichier script, avec ou sans le chemin complet pour le trouver, contenant un switch pour les calculs direct, tangent et adjoint", ang="Waiting for a script file name, with or without the full path to find it, containing a switch for direct, tangent and adjoint computations"),
        ),
    TEMPLATE_DATA =  BLOC (condition = " FROM in ( 'Template', ) ",
        Template = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "AnalysisPrinter", into=("AnalysisPrinter", "AnalysisSaver", "AnalysisPrinterAndSaver")),
        AnalysisPrinter = BLOC (condition = " Template == 'AnalysisPrinter' ",
            ValueTemplate = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "import numpy\\nxa=numpy.ravel(ADD.get('Analysis')[-1])\\nprint('Analysis:',xa)" ),
            ),
        AnalysisSaver = BLOC (condition = " Template == 'AnalysisSaver' ",
            ValueTemplate = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "import numpy\\nxa=numpy.ravel(ADD.get('Analysis')[-1])\\nf='/tmp/analysis.txt'\\nprint('Analysis saved in \\"%s\\"'%f)\\nnumpy.savetxt(f,xa)" ),
            ),
        AnalysisPrinterAndSaver = BLOC (condition = " Template == 'AnalysisPrinterAndSaver' ",
            ValueTemplate = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "import numpy\\nxa=numpy.ravel(ADD.get('Analysis')[-1])\\nprint 'Analysis:',xa\\nf='/tmp/analysis.txt'\\nprint('Analysis saved in \\"%s\\"'%f)\\nnumpy.savetxt(f,xa)" ),
            ),
        ),
    )
"""

init_method = """
def F_InitChoice() : return  ("Background",
                              "BackgroundError",
                              "Observation",
                              "ObservationError",
                              "ObservationOperator",
                              "EvolutionModel",
                              "EvolutionError",
                              "AlgorithmParameters",
                              "UserPostAnalysis",
                             )

def F_Init(statut) : return FACT(statut = statut,
    INIT_FILE = SIMP(statut = "o", typ = "FichierNoAbs", validators=[OnlyStr(), FileExtVal('py')]),
    TARGET_LIST = SIMP(statut = "o", typ = "TXM", min=1, max="**", into=F_InitChoice(),  validators=(VerifExiste(2))),
    )
"""

assim_data_method = """
def {assim_name}InNS(filename):
    if os.path.exists(filename):
        fc = open(filename, 'r').readlines()
        cr = re.compile("^{assim_name}[\s]*=")
        for ln in fc:
            if cr.match(ln): return 1
    return 0
{assim_name}InNS.info = u"The Python file has to contain explicitly a \\"{assim_name}\\" variable."
def F_{assim_name}(statut, fv=NoCheckInNS) : return FACT(
    statut=statut,
{storage}
    INPUT_TYPE = SIMP(statut="o", typ = "TXM", into=({choices}), defaut={default_choice}),{decl_choices}
    )
"""

assim_data_choice = """
    {choice_name} = BLOC ( condition = " INPUT_TYPE in ( '{choice_name}', ) ",
        data = F_{choice_name}("o", fv),
        ),"""

observers_choice = """
    {var_name} = BLOC (condition=" '{var_name}' in set(SELECTION) ",
        {var_name}_data = FACT(statut = "o",
            Scheduler    = SIMP(statut = "f", typ = "TXM"),
            Info         = SIMP(statut = "o", typ = "TXM", defaut = "{var_name}"),
            NodeType     = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "Template", into=("String", "Script", "Template")),
            PythonScript = BLOC (condition = " NodeType == 'String' ",
                Value = SIMP(statut = "o", typ = "TXM")
                ),
            UserFile = BLOC (condition = " NodeType == 'Script' ",
                Value = SIMP(statut = "o", typ = "FichierNoAbs", validators=[OnlyStr(), FileExtVal('py')])
                ),
            ObserverTemplate = F_ObserverTemplate(),
            ),
        ),"""

from daCore.Templates import ObserverTemplates
observers_list = ObserverTemplates.keys_in_presentation_order()
observers_list = '"%s"'%str('", "'.join(observers_list))
observers_cont = ""
for k in ObserverTemplates.keys_in_presentation_order():
    observers_cont += """                %s = BLOC (condition = " Template == '%s' ",\n"""%(k,k)
    observers_cont += """                    ValueTemplate = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "%s", fr="%s", ang="%s" ),\n"""%(
        ObserverTemplates[k].replace("\n","\\n").replace('"','\\"'),
        ObserverTemplates.getdoc(k, "fr_FR"),
        ObserverTemplates.getdoc(k, "en_EN"),
        )
    observers_cont += """                    ),\n"""
observers_method = """
def F_ObserverTemplate() : return BLOC(condition = " NodeType == 'Template' ",
                Template = SIMP(statut = "o", typ = "TXM", min=1, max=1, defaut = "ValuePrinter", into=(%s)),
%s                )

def F_Observers(statut) : return FACT(
    statut=statut,
    SELECTION = SIMP(statut="o", defaut=[], typ="TXM", min=0, max="**", homo="SansOrdreNiDoublon", validators=NoRepeat(), into=({choices})),{decl_choices}
    )
"""%(observers_list,observers_cont)

algo_choices = """
def AlgorithmParametersInNS(filename):
    if os.path.exists(filename):
        fc = open(filename, 'r').readlines()
        cr = re.compile("^AlgorithmParameters[\s]*=")
        for ln in fc:
            if cr.match(ln): return 1
    return 0
AlgorithmParametersInNS.info = u"The Python file has to contain explicitly an \\"AlgorithmParameters\\" variable."
def F_AlgorithmParameters(statut, algos_names, fv=NoCheckInNS) : return FACT(
    statut = statut,
    Algorithm = SIMP(statut="o", typ = "TXM", into = algos_names ),
    Parameters = SIMP(statut="f", typ = "TXM", into=("Defaults", "Dict"), defaut="Defaults"),
    Dict = BLOC ( condition = " Parameters == 'Dict' ",
        statut="f",
        data = F_Dict("o", fv),
        ),{all_algo_defaults}
    )
"""
one_algo_choices = """
    Parameters{algo_name} = BLOC (condition = " (Parameters == 'Defaults') and (Algorithm == '{algo_name}') ",
        statut="f",
{algo_parameters}        ),"""

assim_study = """
def F_variables(statut) : return FACT(
    statut=statut,
    regles = ( MEME_NOMBRE ('NAMES', 'SIZES')),
    NAMES = SIMP(statut="o", typ="TXM", max="**", validators=NoRepeat()),
    SIZES = SIMP(statut="o", typ="I", val_min=1, max="**")
    )
def ChDir(dirname):
    os.chdir(os.path.abspath(dirname))
    return 1
ChDir.info = u"This has to be a regular directory path."

ASSIMILATION_STUDY = PROC(nom="ASSIMILATION_STUDY",
    op=None,
    repetable           = "n",
    StudyName           = SIMP(statut="o", typ = "TXM", defaut="ADAO Calculation Case"),
    StudyRepertory      = SIMP(statut="f", typ = "Repertoire", validators=FunctionVal(ChDir), min=1, max=1),
    Debug               = SIMP(statut="f", typ = "I", into=(0, 1), defaut=0),
    AlgorithmParameters = F_AlgorithmParameters("o",({algos_names}), AlgorithmParametersInNS),
    Background          = F_Background("o", BackgroundInNS),
    BackgroundError     = F_BackgroundError("o", BackgroundErrorInNS),
    Observation         = F_Observation("o", ObservationInNS),
    ObservationError    = F_ObservationError("o", ObservationErrorInNS),
    ObservationOperator = F_ObservationOperator("o"),
    EvolutionModel      = F_EvolutionModel("f"),
    EvolutionError      = F_EvolutionError("f", EvolutionErrorInNS),
    ControlInput        = F_ControlInput("f"),
    UserDataInit        = F_Init("f"),
    UserPostAnalysis    = F_UserPostAnalysis("o"),
    InputVariables      = F_variables("f"),
    OutputVariables     = F_variables("f"),
    Observers           = F_Observers("f")
    )

CHECKING_STUDY = PROC(nom="CHECKING_STUDY",
    op=None,
    repetable           = "n",
    StudyName           = SIMP(statut="o", typ = "TXM", defaut="ADAO Checking Case"),
    StudyRepertory      = SIMP(statut="f", typ = "Repertoire", validators=FunctionVal(ChDir), min=1, max=1),
    Debug               = SIMP(statut="f", typ = "I", into=(0, 1), defaut=0),
    AlgorithmParameters = F_AlgorithmParameters("o", ({check_names}), AlgorithmParametersInNS),
    CheckingPoint       = F_CheckingPoint("o", CheckingPointInNS),
    Background          = F_Background("f", BackgroundInNS),
    BackgroundError     = F_BackgroundError("f", BackgroundErrorInNS),
    Observation         = F_Observation("f", ObservationInNS),
    ObservationError    = F_ObservationError("f", ObservationErrorInNS),
    ObservationOperator = F_ObservationOperator("o"),
    UserDataInit        = F_Init("f"),
    Observers           = F_Observers("f")
    )
"""

#----------- End of Templates Part ---------------#



#----------- Begin generation script -----------#

# Parse arguments
from argparse import ArgumentParser
usage = "usage: %(prog)s [options] catalog_path catalog_name"
version="%(prog)s 0.1"
my_parser = ArgumentParser(usage=usage)
my_parser.add_argument('-v', '--version', action='version', version=version)
my_parser.add_argument('catalog_path')
my_parser.add_argument('catalog_name')
args = my_parser.parse_args()

# Generates into a string
mem_file = io.StringIO()

# Start file
from time import strftime
mem_file.write(unicode(begin_catalog_file, 'utf-8').format(**{'date':strftime("%Y-%m-%d %H:%M:%S")}))

# Step initial: on obtient la liste des algos
algos_names = ""
check_names = ""
decl_algos  = ""
assim_study_object = daCore.AssimilationStudy.AssimilationStudy()
algos_list = assim_study_object.get_available_algorithms()
del assim_study_object
for algo_name in algos_list:
  if algo_name in infos.AssimAlgos:
    logging.debug("An assimilation algorithm is found: " + algo_name)
    algos_names += "\"" + algo_name + "\", "
  elif algo_name in infos.CheckAlgos:
    logging.debug("A checking algorithm is found: " + algo_name)
    check_names += "\"" + algo_name + "\", "
  else:
    logging.debug("This algorithm is not considered: " + algo_name)

# Step 1: A partir des infos, on cree les fonctions qui vont permettre
# d'entrer les donnees utilisateur
for data_input_name in infos.DataTypeDict:
  logging.debug('A data input Type is found: ' + data_input_name)
  data_name = data_input_name
  data_into = ""
  data_default = ""
  ms_default = ""

  # On recupere les differentes facon d'entrer les donnees
  for basic_type in infos.DataTypeDict[data_input_name]:
    data_into += "\"" + basic_type + "\", "

  # On choisit le default
  data_default = "\"" + infos.DataTypeDefaultDict[data_input_name] + "\""
  if data_input_name in infos.DataSValueDefaultDict:
    ms_default = " defaut=\"" + infos.DataSValueDefaultDict[data_input_name] + "\","

  mem_file.write(unicode(data_method, 'utf-8').format(**{
    'data_name'    : data_name,
    'data_into'    : data_into,
    'data_default' : data_default,
    'ms_default'   : ms_default,
    'algos_names'  : algos_names+check_names,
    }))

# Step 2: On cree les fonctions qui permettent de rentrer les donnees des algorithmes
for assim_data_input_name in infos.AssimDataDict:
  logging.debug("An input function data input is found: " + assim_data_input_name)
  # assim_name = assim_data_input_name
  storage = ""
  choices = ""
  default_choice = ""
  decl_choices = ""
  decl_opts = ""
  if infos.AssimDataDefaultDict[assim_data_input_name] in infos.StoredAssimData:
    storage = "    Stored = SIMP(statut=\"f\", typ = \"I\", into=(0, 1), defaut=0, fr=\"Choix de stockage interne ou non du concept parent\", ang=\"Choice of the storage or not of the parent concept\"),"
  for choice in infos.AssimDataDict[assim_data_input_name]:
    choices += "\"" + choice + "\", "
    decl_choices += assim_data_choice.format(**{'choice_name' : choice})
    if choice in infos.StoredAssimData:
      storage = "    Stored = SIMP(statut=\"f\", typ = \"I\", into=(0, 1), defaut=0, fr=\"Choix de stockage interne ou non du concept parent\", ang=\"Choice of the storage or not of the parent concept\"),"
  default_choice = "\"" + infos.AssimDataDefaultDict[assim_data_input_name] + "\""

  mem_file.write(unicode(assim_data_method, 'utf-8').format(**{
    'assim_name'     : assim_data_input_name,
    'storage'        : storage,
    'choices'        : choices,
    'decl_choices'   : decl_choices,
    'default_choice' : default_choice,
    }))

# Step 3: On ajoute les fonctions representant les options possibles
for opt_name in infos.OptDict:
  logging.debug("An optional node is found: " + opt_name)
  data_name = opt_name
  data_into = ""
  data_default = ""
  ms_default = ""

  for choice in infos.OptDict[opt_name]:
    data_into += "\"" + choice + "\", "

  # On choisit le default
  data_default = "\"" + infos.OptDefaultDict[opt_name] + "\""
  if opt_name in infos.DataSValueDefaultDict:
    ms_default = " defaut=\"" + infos.DataSValueDefaultDict[opt_name] + "\","

  mem_file.write(unicode(data_method, 'utf-8').format(**{
    'data_name'    : data_name,
    'data_into'    : data_into,
    'data_default' : data_default,
    'ms_default'   : ms_default,
    'algos_names'  : algos_names+check_names,
    }))

# Step 4: On ajoute la methode optionnelle init
# TODO uniformiser avec le step 3
mem_file.write(unicode(init_method, 'utf-8'))

# Step 5: Add observers
decl_choices = ""
for obs_var in infos.ObserversList:
  decl_choices += observers_choice.format(**{'var_name':obs_var})
mem_file.write(unicode(observers_method, 'utf-8').format(**{
  'choices' : infos.ObserversList,
  'decl_choices' : decl_choices,
  }))

# Step 5: Add algorithmic choices

all_names = eval((algos_names+check_names))
all_algo_defaults = ""
for algo in all_names:
    assim_study_object = daCore.AssimilationStudy.AssimilationStudy()
    assim_study_object.setAlgorithmParameters(Algorithm=algo)
    par_dict = assim_study_object.get("AlgorithmRequiredParameters",False)
    par_keys = sorted(par_dict.keys())
    algo_parameters = ""
    for pn in par_keys:
        if pn in ("StoreInternalVariables", "PlotAndSave", "ResultFile", "ResultTitle", "ResultLabel"): continue # Cles a supprimer
        pt = par_dict[pn]["typecast"] # Pointeur de type
        pd = par_dict[pn]["default"]
        pm = par_dict[pn]["message"]
        if "minval" in par_dict[pn] and par_dict[pn]["minval"] is not None:
            vi = ", val_min=%s"%par_dict[pn]["minval"]
        else:
            vi = ""
        if "minval" in par_dict[pn] and par_dict[pn]["maxval"] is not None:
            vs = ", val_max=%s"%par_dict[pn]["maxval"]
        else:
            vs = ""
        if   pt is int:
            algo_parameters += """        %s = SIMP(statut="f", typ="I"%s%s, min=1, max=1, defaut=%s, fr="%s"),\n"""%(pn,vi,vs,int(pd),pm)
        elif pt is float:
            algo_parameters += """        %s = SIMP(statut="f", typ="R"%s%s, min=1, max=1, defaut=%s, fr="%s"),\n"""%(pn,vi,vs,float(pd),pm)
        elif pt is bool:
            algo_parameters += """        %s = SIMP(statut="f", typ="I", min=1, max=1, defaut=%s, fr="%s"),\n"""%(pn,int(pd),pm)
        elif pt is str and "listval" in par_dict[pn]:
            algo_parameters += """        %s = SIMP(statut="f", typ="TXM", min=1, max=1, defaut="%s", into=%s, fr="%s"),\n"""%(pn,pd,par_dict[pn]["listval"],pm)
        elif pt is tuple and "listval" in par_dict[pn]:
            algo_parameters += """        %s = SIMP(statut="f", typ="TXM", max="**", into=%s, fr="%s"),\n"""%(pn,par_dict[pn]["listval"],pm)
        else:
            algo_parameters += """        %s = SIMP(statut="f", typ="TXM", fr="%s"),\n"""%(pn,pm)
    del assim_study_object
    if algo_parameters != "":
        all_algo_defaults += one_algo_choices.format(**{
            'algo_name':algo,
            'algo_parameters':algo_parameters,
            })
mem_file.write(unicode(algo_choices, 'utf-8').format(**{'all_algo_defaults':unicode(all_algo_defaults, 'utf-8')}))

# Final step: Add algorithm and assim_study
mem_file.write(unicode(assim_study, 'utf-8').format(**{
  'algos_names':algos_names,
  'check_names':check_names,
  'decl_algos':decl_algos,
  }))

# Write file
if sys.version_info.major > 2:
    with open(os.path.join(args.catalog_path, args.catalog_name), "w", encoding='utf8') as final_file:
        final_file.write(mem_file.getvalue())
else:
    with open(os.path.join(args.catalog_path, args.catalog_name), "wr") as final_file:
        final_file.write(mem_file.getvalue().encode('utf-8'))
mem_file.close()
