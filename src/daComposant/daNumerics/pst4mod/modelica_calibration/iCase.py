# -*- coding: utf-8 -*-
#
# Copyright (C) 2025-2026 EDF R&D
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

__author__ = "Jean-Philippe ARGAUD"
__all__ = ["CalibrationProcessingObject", "__version__"]
__version__ = "1.09.9.16.0"  # "x.x"+"adao version"

# Initialisations informatiques
import os, sys, re, numpy, scipy, math, matplotlib, logging, platform, ast
import adao  # noqa: F401
from daCore.Interfaces import ImportScalarLinesFromFile
from modelica_calibration.case import Calibration

try:
    from IPython.display import display
    import ipywidgets as widgets
except ImportError:
    logging.warning(
        "===> Attention, IPython n'est pas disponible, les widgets ne pourront pas être créés."
    )
    display = print
import matplotlib.pyplot as plt
import PIL

# ------------------------------------------------------------------------------
from datetime import datetime

now = datetime.now()
print(
    "Ce document est évalué le %02i/%02i/%i à %02i:%02i:%02i, avec le script de support version %s."
    % (now.day, now.month, now.year, now.hour, now.minute, now.second, __version__)
)


# ==============================================================================
class CalibrationProcessingObject(object):

    def __init__(self, Model=""):
        self.BasePath = os.getcwd()
        self.x_checkboxes = []
        self.y_checkboxes = []
        sys.path.insert(0, self.BasePath)
        logging.info("Initialisation correcte, environnement vérifié")

    def __findAndShowSpecificFile(
        self, extensions=[], filters=[], appendAllFiles=False, label="", displayIt=False
    ):
        """
        Recherche des fichiers dans les sous-répertoire du notebook
        Il sont retenus par extension et par filtre de nom
        """
        # Inventaire des fichiers sélectionnés par extension
        allFiles = []
        selectedFiles = []
        for root, dirs, files in os.walk(self.BasePath):
            for f in files:
                ff = os.path.join(root, f)
                if os.path.isfile(ff):
                    if "__pycache__" not in ff and os.path.splitext(f)[-1] not in [
                        ".ipynb",
                        ".pdf",
                        ".png",
                        ".jpg",
                        ".gif",
                        ".docx",
                        ".xslx",
                        ".pptx",
                        ".csv",
                        ".bak",
                        ".txt",
                        ".dat",
                    ]:
                        allFiles.append(os.path.relpath(ff, self.BasePath))
                    if os.path.splitext(f)[-1] in extensions:
                        selectedFiles.append(os.path.relpath(ff, self.BasePath))
        allFiles = [f for f in allFiles if f not in selectedFiles]
        allFiles.sort()
        selectedFiles.sort()
        if len(selectedFiles) == 0:
            raise ValueError('Aucun fichier trouvé pour le "%s"' % label)
        # Essaie de trouver le fichier selon les filtres
        someFile = selectedFiles[0]  # Défaut : le premier
        for name in selectedFiles:
            for filt in filters:
                if filt.lower() in name.lower():
                    someFile = name
        # Rajoute ou pas tous les fichiers trouvés
        if appendAllFiles:
            theFiles = (
                selectedFiles
                + [
                    "----- Fichiers supplémentaires dont le choix est moins vraisemblable",
                ]
                + allFiles
            )
        else:
            theFiles = selectedFiles
        # Change de widget au-delà de 2 items
        if len(theFiles) > 2:
            serieChosenWidget = widgets.Dropdown
        else:
            serieChosenWidget = widgets.RadioButtons
        #
        theValue = (
            serieChosenWidget(
                options=theFiles,
                value=someFile,
                layout={"width": "max-content"},  # If the items' names are long
                disabled=False,
            ),
        )
        theWidget = widgets.VBox(
            [
                widgets.Label(value=label),
                theValue[0],
            ]
        )
        if displayIt:
            display(theWidget)
        #
        return theWidget, theValue[0]

    def __createParametersIfUnkown(self):
        selectedFiles = []
        for root, dirs, files in os.walk(self.BasePath):
            for f in files:
                ff = os.path.join(root, f)
                if (
                    os.path.isfile(ff)
                    and "parameters.py" in ff.lower()
                    and "parameters.py.bak" not in ff.lower()
                ):
                    selectedFiles.append(os.path.relpath(ff, self.BasePath))
        #
        if len(selectedFiles) == 0:
            # Création si fichier inexistant avec défauts raisonnables
            with open("parameters.py", "x") as parameters:
                parameters.write("""
Algorithm = "3DVAR"
Parameters = {
    "MaximumNumberOfIterations":2,
    "DifferentialIncrement":0.01,
    "EnableWiseParallelism":1,
    "StoreSupplementaryCalculations":[
        "SimulatedObservationAtOptimum",
        "CurrentIterationNumber",
        ],
    }
BackgroundError = 1e5
ObservationError = 1e-5
                """)

    def findAndSetAllPath(self):
        # --------
        x1_title = widgets.HTML(
            "<em>Le nom du répertoire courant est le suivant :</em>"
        )
        x1_info = widgets.HTML("<tt>%s</tt>" % self.BasePath)
        x3_title = widgets.HTML(
            "<em>Vérifier et corriger avec attention les informations ou fichiers trouvés :</em>"
        )
        # --------
        system = platform.system().lower()
        wModelName, ModelName = self.__findAndShowSpecificFile(
            extensions=[".fmu", ".exe", ""],
            filters=[system, "dymosim", "dsin"],
            appendAllFiles=True,
            label="- Simulateur ou modèle, fonctionnel pour le système informatique sous-jacent :",
        )
        # --------
        __ModelName = str(ModelName.value).lower()
        if os.path.splitext(__ModelName)[-1] in [".fmu", ".fmi", ".FMU", ".FMI"]:
            __ModelFormat = "FMI"
        elif "dymosim" in __ModelName.lower():
            __ModelFormat = "DYMOSIM"
        elif "openmodelica" in __ModelName:
            __ModelFormat = "OPENMODELICA"
        else:
            __ModelFormat = "GUESS"
        ModelFormat = (
            widgets.Dropdown(
                options=["FMI", "DYMOSIM", "OPENMODELICA", "PYSIM", "GUESS"],
                value=__ModelFormat,
                layout={"width": "max-content"},  # If the items' names are long
                disabled=False,
            ),
        )
        wModelFormat = widgets.VBox(
            [
                widgets.Label(value="- Format du modèle :"),
                ModelFormat[0],
            ]
        )
        # --------
        wBackgroundName, BackgroundName = self.__findAndShowSpecificFile(
            extensions=[".csv", ".txt", ".dat"],
            filters=["bauch", "back", "prior", "init"],
            label="- Ébauche ou valeur a priori pour les paramètres:",
        )
        wDataNames, DataNames = self.__findAndShowSpecificFile(
            extensions=[".csv", ".txt", ".dat"],
            filters=["obs", "meas", "mesu", "data"],
            label="- Observations ou mesures (en 1 seul fichier) :",
        )
        wLinkName, LinkName = self.__findAndShowSpecificFile(
            extensions=[".csv", ".txt", ".dat"],
            filters=["link", "cl", "limit"],
            label="- Conditions aux limites (fichier à indiquer même si facultatives):",
        )
        # --------
        self.__createParametersIfUnkown()
        wParametersName, ParametersName = self.__findAndShowSpecificFile(
            extensions=[
                ".py",
            ],
            filters=["parameters", "param"],
            label="- Paramétrisation numérique du recalage :",
        )
        # --------
        display(
            widgets.VBox(
                [
                    x1_title,
                    x1_info,
                    x3_title,
                    wModelName,
                    wModelFormat,
                    wBackgroundName,
                    wDataNames,
                    wLinkName,
                    wParametersName,
                ]
            )
        )
        # --------
        self.ModelName = ModelName
        self.ModelFormat = ModelFormat[0]
        self.BackgroundName = BackgroundName
        self.DataNames = DataNames
        self.LinkName = LinkName
        self.ParametersName = ParametersName

    def showTechFigures(self):
        allImg = []
        for root, dirs, files in os.walk(self.BasePath):
            for f in files:
                ff = os.path.join(root, f)
                if os.path.isfile(ff):
                    if os.path.splitext(f)[-1] in [".png", ".jpg", ".jpeg", ".gif"]:
                        allImg.append(os.path.relpath(ff, self.BasePath))
        allImg.sort()
        # --------
        nbr = len(allImg)
        if nbr == 0:
            print("Ce modèle ne semble pas contenir de figure technique associée.")
        else:
            fig, ax = plt.subplots(nbr, 1, figsize=(12, nbr * 6))
            for i, image in enumerate(allImg):
                with PIL.Image.open(image) as im:
                    if len(allImg) <= 1:
                        ax.imshow(im)
                        ax.axis("off")
                    else:
                        ax[i].imshow(im)
                        ax[i].axis("off")
        #
        self.TechFigures = allImg

    def findVariableNames(self):
        print(
            "- Le fichier identifié pour l'ébauche ou la valeur a priori est :\n    %s"
            % self.BackgroundName.value
        )
        self.AvailableParameters, _, _ = ImportScalarLinesFromFile(
            self.BackgroundName.value
        ).getvalue()
        print(
            "  et les variable découvertes pour le recalage sont :\n    %s"
            % (self.AvailableParameters,)
        )
        #
        print()
        print(
            "- Le fichier identifié pour les observations ou mesures est :\n    %s"
            % self.DataNames.value
        )
        with open(self.DataNames.value, "r") as obs:
            for line in obs.readlines():
                if line.count(",") > 0:
                    _delimiter = ","
                elif line.count(";") > 0:
                    _delimiter = ";"
                elif line.count("\t") > 0:
                    _delimiter = "\t"
                else:
                    _delimiter = None
                if len(line) <= 1:
                    continue
                if line.strip()[0] == "#":
                    continue
                if _delimiter is None:
                    self.AvailableObservations = line.strip().split()[2:]
                else:
                    self.AvailableObservations = line.strip().split(_delimiter)[2:]
                break
        print(
            "  et les observations découvertes pour le recalage sont :\n    %s"
            % (self.AvailableObservations,)
        )

    def showParametersSelectionByWidgets(self, liste=[]):
        if len(liste) == 0:
            liste = self.AvailableParameters
        x_checkboxes = [
            widgets.Checkbox(value=bool(box in liste), description=box, indent=True)
            for box in sorted(self.AvailableParameters)
        ]
        x_title = widgets.HTML("<em>Paramètres à recaler :</em>")
        #
        x_alltoggleOn = widgets.Button(description="Tout sélectionner", indent=True)

        def alltoggleOn(button):
            for box in x_checkboxes:
                box.value = True

        x_alltoggleOn.on_click(alltoggleOn)
        #
        x_alltoggleOff = widgets.Button(description="Tout désélectionner", indent=True)

        def alltoggleOff(button):
            for box in x_checkboxes:
                box.value = False

        x_alltoggleOff.on_click(alltoggleOff)
        #
        x_header = widgets.HBox(
            children=[
                x_title,
                x_alltoggleOn,
                x_alltoggleOff,
            ]
        )
        x_container = widgets.VBox(
            children=[
                x_header,
            ]
            + x_checkboxes,
            layout=widgets.Layout(
                overflow="auto", height="auto", width="auto", margin="20px 0 0 30px"
            ),
        )
        display(x_container)
        self.x_checkboxes = x_checkboxes

    def showObservationsSelectionByWidgets(self, liste=[]):
        if len(liste) == 0:
            liste = self.AvailableObservations
        y_checkboxes = [
            widgets.Checkbox(value=bool(box in liste), description=box, indent=True)
            for box in sorted(self.AvailableObservations)
        ]
        y_title = widgets.HTML("<em>Mesures à utiliser :</em>")
        #
        y_alltoggleOn = widgets.Button(description="Tout sélectionner", indent=True)

        def alltoggleOn(button):
            for box in y_checkboxes:
                box.value = True

        y_alltoggleOn.on_click(alltoggleOn)
        #
        y_alltoggleOff = widgets.Button(description="Tout désélectionner", indent=True)

        def alltoggleOff(button):
            for box in y_checkboxes:
                box.value = False

        y_alltoggleOff.on_click(alltoggleOff)
        #
        y_header = widgets.HBox(
            children=[
                y_title,
                y_alltoggleOn,
                y_alltoggleOff,
            ]
        )
        y_container = widgets.VBox(
            children=[
                y_header,
            ]
            + y_checkboxes,
            layout=widgets.Layout(
                overflow="auto", height="auto", width="auto", margin="20px 0 0 30px"
            ),
        )
        display(y_container)
        self.y_checkboxes = y_checkboxes

    def showOptionsSelectionByWidgets(self):
        __parameters = {}
        with open(self.ParametersName.value, "r") as infile:
            content = infile.read()
            if content.find("Parameters") > 1:
                content = re.split("Parameters[\\s]*=[\\s]*", content, maxsplit=1)[-1]
                content = re.split("}", content, maxsplit=1)[0]
                if len(content) > 1:
                    content += "}"
                    try:
                        __parameters = ast.literal_eval(content)
                    except SyntaxError:
                        pass
        if "EnableWiseParallelism" in __parameters:
            ewp = bool(__parameters["EnableWiseParallelism"])
        else:
            ewp = True
        if "MaximumNumberOfIterations" in __parameters:
            mni = int(__parameters["MaximumNumberOfIterations"])
        else:
            mni = 2
        #
        Title = widgets.HTML("""
        Choisir les caractéristiques particulières du calcul de recalage que vous souhaitez :
        <br><em>(Attention, chaque option nécessite des calculs supplémentaires, parfois nombreux)</em>
        """)
        VerifyFunction = widgets.Checkbox(
            value=False,
            description="Vérifier préalablement le bon fonctionnement du modèle utilisé pour la simulation",
            disabled=False,
            indent=False,
            layout={"width": "max-content"},
        )
        GlobalSensitivityCheck = widgets.Checkbox(
            value=False,
            description="Faire préalablement un test de sensibilité global du modèle",
            disabled=False,
            indent=False,
            layout={"width": "max-content"},
        )
        ParamSensitivityCheck = widgets.Checkbox(
            value=False,
            description="Faire préalablement un test de sensibilité du modèle paramètre par paramètre",
            disabled=False,
            indent=False,
            layout={"width": "max-content"},
        )
        ModelStabilityCheck = widgets.Checkbox(
            value=False,
            description="Faire préalablement un test de stabilité du modèle utilisé pour la simulation",
            disabled=False,
            indent=False,
            layout={"width": "max-content"},
        )
        CreateCSVoutputResults = widgets.Checkbox(
            value=False,
            description="Créer un fichier de sortie au format Excel/CSV pour les résultats du recalage",
            disabled=False,
            indent=False,
            layout={"width": "max-content"},
        )
        IntermediateInformation = widgets.Checkbox(
            value=False,
            description="Afficher des informations intermédiaires d'avancement pendant le recalage",
            disabled=False,
            indent=False,
            layout={"width": "max-content"},
        )
        EnableWiseParallelism = widgets.Checkbox(
            value=ewp,
            description="Exécuter le modèle en parallèle lorsque c'est possible",
            disabled=False,
            indent=False,
            layout={"width": "max-content"},
        )
        NbIter_e = widgets.HTML(
            "Nombre maximal d'itération pour la recherche optimale "
            + "(2 à 10 pour tester, 30 à 50 pour estimer, 100 à 150 pour optimiser)"
        )
        NbIter_v = widgets.BoundedIntText(
            value=mni,
            min=1,
            max=1000,
            step=1,
            disabled=False,
            layout={"width": "max-content"},
        )
        NbIter_w = widgets.HBox([NbIter_v, NbIter_e])
        # --------
        display(
            widgets.VBox(
                [
                    Title,
                    VerifyFunction,
                    GlobalSensitivityCheck,
                    ParamSensitivityCheck,
                    ModelStabilityCheck,
                    CreateCSVoutputResults,
                    IntermediateInformation,
                    EnableWiseParallelism,
                    NbIter_w,
                ]
            )
        )
        # --------
        self.VerifyFunction = VerifyFunction
        self.GlobalSensitivityCheck = GlobalSensitivityCheck
        self.ParamSensitivityCheck = ParamSensitivityCheck
        self.ModelStabilityCheck = ModelStabilityCheck
        self.CreateCSVoutputResults = CreateCSVoutputResults
        self.IntermediateInformation = IntermediateInformation
        self.EnableWiseParallelism = EnableWiseParallelism
        self.NbIter_v = NbIter_v

    def updateListsAndParametersPy(self):
        self.x_names = numpy.array(
            [cb.description for cb in self.x_checkboxes if cb.value]
        )
        self.y_names = numpy.array(
            [cb.description for cb in self.y_checkboxes if cb.value]
        )
        #
        parameterFile = os.path.join(self.BasePath, self.ParametersName.value)
        #
        if not os.path.exists(parameterFile):
            raise ValueError(
                "Le fichier de paramètres est introuvable sous le nom suivant :\n    %s"
                % parameterFile
            )
        #
        with open(parameterFile, "r") as infile:
            content = infile.read()
            with open(parameterFile + ".bak", "w") as bakfile:
                bakfile.write(content)
            content = re.sub(
                "[\"']MaximumNumberOfIterations[\"']:[0-9]*,",
                '"MaximumNumberOfIterations":%i,' % self.NbIter_v.value,
                content,
            )
            content = re.sub(
                "[\"']EnableWiseParallelism[\"']:.*,",
                '"EnableWiseParallelism":%i,' % self.EnableWiseParallelism.value,
                content,
            )
        with open(parameterFile, "w") as outfile:
            outfile.write(content)
        #
        return 0

    def showInternalContent(self):
        print()
        print(
            "Le récapitulatif des informations collectées jusqu'à présent est le suivant :"
        )
        print()
        print("- Le répertoire de calcul est :\n  %s" % self.BasePath)
        print()
        print(
            "- Le fichier identifié pour le simulateur ou le modèle est :\n  %s\n  au format %s"
            % (self.ModelName.value, self.ModelFormat.value)
        )
        print()
        print(
            "- Le fichier identifié pour l'ébauche ou la valeur a priori est :\n  %s"
            % self.BackgroundName.value
        )
        print()
        print(
            "- Le fichier identifié pour les observations ou mesures est :\n  %s"
            % self.DataNames.value
        )
        print()
        print(
            "- Le fichier identifié pour les conditions aux limites est:\n  %s"
            % self.LinkName.value
        )
        print()
        print(
            "- Le fichier identifié pour la paramétrisation numérique :\n  %s"
            % self.ParametersName.value
        )
        print()
        x_names = [cb.description for cb in self.x_checkboxes if cb.value]
        print("- Les noms des paramètres à recaler sont :")
        print(" ", x_names)
        print()
        y_names = [cb.description for cb in self.y_checkboxes if cb.value]
        print("- Les noms des observations à utiliser sont :")
        print(" ", y_names)
        print()

    def doCalibration(self):
        self.updateListsAndParametersPy()
        print("Lancement du calcul de recalage itératif, ça tourne...\n")
        os.chdir(self.BasePath)
        newcase = Calibration()
        self.resultats = newcase.calibrateMultiObs(
            DataNames=[
                self.DataNames.value,
            ],
            ModelName=os.path.dirname(self.ModelName.value),
            ModelFormat=self.ModelFormat.value,
            MethodName=self.ParametersName.value,
            LinkName=self.LinkName.value,
            BackgroundFormat="USER",
            BackgroundName=self.BackgroundName.value,
            VariablesToCalibrate=self.x_names,
            OutputVariables=self.y_names,
            ResultName="results.txt",
            Verbose=self.IntermediateInformation.value,
            NeedInitVariables=False,
            IntermediateInformation=self.IntermediateInformation.value,
            # CreateOptimaldsin       = True,
            InitialSimulation=True,
            VerifyFunction=self.VerifyFunction.value,
            GlobalSensitivityCheck=self.GlobalSensitivityCheck.value,
            ParamSensitivityCheck=self.ParamSensitivityCheck.value,
            CreateCSVoutputResults=self.CreateCSVoutputResults.value,
            # AdaptObservationError   = True,
            # ResultsSummary          = True,
            AdvancedDebugModel=True,
            ModelStabilityCheck=self.ParamSensitivityCheck.value,
            ModelStabilityCheckingPoints=5,
        )
        os.chdir(self.BasePath)
        print(
            "\n\nRecalage terminé, les résultats ont été enregistrés en fichier et peuvent être analysés."
        )
        #
        self.resultats["OMB"] = (
            self.resultats["Measures"] - self.resultats["InitialSimulation"]
        )
        self.resultats["OMA"] = (
            self.resultats["Measures"] - self.resultats["OptimalSimulation"]
        )
        Xb = self.resultats["InitialParameters"]
        Xa = self.resultats["OptimalParameters"]
        #
        synthese = "<p>Synthèse des résultats :<table border=1>\n"
        synthese += "<tr><th>Variable recalée</th><th>Avant</th><th>Après</th></tr>\n"
        for i in range(len(self.x_names)):
            synthese += (
                "<tr><td>%s</td><td align='right'>%.2f</td><td align='right'>%.2f</td></tr>\n"
                % (self.x_names[i], Xb[i], Xa[i])
            )
        synthese += "</table>\n"
        display(widgets.HTML(synthese))

    def postIndicators(self):
        mes = numpy.ravel(self.resultats["Measures"])
        bck = numpy.ravel(self.resultats["InitialSimulation"])
        opt = numpy.ravel(self.resultats["OptimalSimulation"])
        #
        mae_ini = numpy.mean(numpy.abs(mes - bck))
        mae_opt = numpy.mean(numpy.abs(mes - opt))
        #
        rmse_ini = numpy.linalg.norm(mes - bck) / math.sqrt(mes.size)
        rmse_opt = numpy.linalg.norm(mes - opt) / math.sqrt(mes.size)
        #
        r2_ini = (
            1.0
            - numpy.linalg.norm(mes - bck) ** 2
            / numpy.linalg.norm(mes - numpy.mean(mes)) ** 2
        )
        r2_opt = (
            1.0
            - numpy.linalg.norm(mes - opt) ** 2
            / numpy.linalg.norm(mes - numpy.mean(mes)) ** 2
        )
        #
        gain_mae = 100 * (mae_ini - mae_opt) / mae_ini
        gain_rmse = 100 * (rmse_ini - rmse_opt) / rmse_ini

        print()
        print("=" * 70)
        print("RESULTATS DU CALAGE")
        print("=" * 70)
        print()

        print(
            f"Nombre de paramètres à recaler  : {len(self.resultats['InitialParameters'])}"
        )
        print(f"Nombre de mesures utilisées     : {len(self.resultats['Measures'])}")
        print()
        print(f"Limite d'itérations de recalage : {self.NbIter_v.value}")
        print(f"Nombre d'itérations de recalage : {self.resultats['CurrentIterationNumber']+1}")
        print()

        print(f"MAE initial...: {mae_ini:,.2f}")
        print(f"MAE final.....: {mae_opt:,.2f}")
        print(f"Gain MAE......: {gain_mae:.2f} %")

        print()

        print(f"RMSE initial..: {rmse_ini:,.2f}")
        print(f"RMSE final....: {rmse_opt:,.2f}")
        print(f"Gain RMSE.....: {gain_rmse:.2f} %")

        print()

        print(f"R² initial....: {r2_ini:.5f}")
        print(f"R² final......: {r2_opt:.5f}")

        print()

    def postObsVsSim(self):
        fig, ax = plt.subplots(1, 1)
        ax.scatter(
            self.resultats["Measures"],
            self.resultats["InitialSimulation"],
            alpha=0.7,
            s=70,
            label="Simulation initiale",
        )
        ax.scatter(
            self.resultats["Measures"],
            self.resultats["OptimalSimulation"],
            alpha=0.7,
            s=70,
            label="Simulation après %i itérations" % (self.resultats['CurrentIterationNumber']+1,),
        )
        xmin = min(
            min(self.resultats["Measures"]),
            min(self.resultats["OptimalSimulation"]),
        )
        xmax = max(
            max(self.resultats["Measures"]),
            max(self.resultats["OptimalSimulation"]),
        )
        ax.plot(
            [xmin, xmax],
            [xmin, xmax],
            "k--",
        )
        ax.set_title("Comparaison entre mesures et simulation finale")
        ax.set_xlabel("Mesures (u.a.)")
        ax.set_ylabel("Simulation (u.a.)")
        ax.legend()
        plt.tight_layout()

    def postErrorDist(self):
        self.measure_err_ini = (
            self.resultats["InitialSimulation"] - self.resultats["Measures"]
        )
        self.measure_err_fin = (
            self.resultats["OptimalSimulation"] - self.resultats["Measures"]
        )
        self.measure_err_gain = numpy.abs(self.measure_err_ini) - numpy.abs(
            self.measure_err_fin
        )
        #
        kde_ini = scipy.stats.gaussian_kde(self.measure_err_ini)
        kde_fin = scipy.stats.gaussian_kde(self.measure_err_fin)
        mine = min(min(self.measure_err_ini), min(self.measure_err_fin))
        maxe = max(max(self.measure_err_ini), max(self.measure_err_fin))
        xx = numpy.linspace(mine, maxe, 200)
        #
        fig, (ax1, ax2) = plt.subplots(2, 1)
        fig.suptitle("Distribution des erreurs mesures-simulation")
        #
        ax1.set_xlim(mine, maxe)
        ax1.plot(xx, kde_ini(xx), label="Erreur initiale", color="blue", lw=0.5)
        ax1.fill_between(xx, 0, kde_ini(xx), alpha=0.5, color="lightblue")
        ax1.axvline(0, color="black", linestyle="--")
        ax1.set_xlabel("Erreur initiale (u.a.)")
        ax1.set_ylabel("Densité")
        #
        ax2.set_xlim(mine, maxe)
        ax2.plot(xx, kde_fin(xx), label="Erreur finale", color="red", lw=0.5)
        ax2.fill_between(xx, 0, kde_fin(xx), alpha=0.5, color="lightcoral")
        ax2.axvline(0, color="black", linestyle="--")
        ax2.set_xlabel("Erreur après %i itérations (u.a.)" % (self.resultats['CurrentIterationNumber']+1,))
        ax2.set_ylabel("Densité")
        #
        plt.tight_layout()

    def postMeasureGainDist(self):
        # gain_orders = self.measure_err_gain.argsort(descending=False)
        gain_orders = self.measure_err_gain.argsort()[::-1]
        gain_sorted = self.measure_err_gain[gain_orders]
        name_sorted = self.y_names[gain_orders]
        colors = numpy.where(gain_sorted >= 0, "forestgreen", "firebrick")
        #
        fig, ax1 = plt.subplots(1, 1, figsize=(7, 0.17 * len(gain_orders)))
        ax1.barh(name_sorted, gain_sorted, color=colors)
        ax1.tick_params(axis="y", labelsize="small")
        ax1.axvline(0, color="black")
        ax1.set_title("Gain par mesure, après %i itérations" % (self.resultats['CurrentIterationNumber']+1,))
        ax1.set_xlabel("Réduction relative de l'erreur absolue par mesure")
        ax1.set_ylabel("Mesure")

    def postEquipementGainDist(self):
        def get_equipment(name):
            return name.split(".")[0]

        def get_variable(name):
            return name.split(".")[-1]

        #
        name_equi = [get_equipment(name) for name in self.y_names]
        gain_equi = dict([(name, []) for name in name_equi])
        for i in range(len(self.y_names)):
            gain_equi[name_equi[i]].append(self.measure_err_gain[i])
        gain_equi_name, gain_equi_mean = [], []
        for k, v in gain_equi.items():
            gain_equi_name.append(k)
            gain_equi_mean.append(float(numpy.mean(gain_equi[k])))
        gain_equi_mean = numpy.array(gain_equi_mean)
        gain_equi_name = numpy.array(gain_equi_name)
        #
        # gain_orders = gain_equi_mean.argsort(descending=False)
        gain_orders = gain_equi_mean.argsort()[::-1]
        gain_sorted = gain_equi_mean[gain_orders]
        name_sorted = gain_equi_name[gain_orders]
        colors = numpy.where(gain_sorted >= 0, "forestgreen", "firebrick")
        #
        fig, ax1 = plt.subplots(1, 1, figsize=(7, 0.17 * len(gain_orders)))
        ax1.barh(name_sorted, gain_sorted, color=colors)
        ax1.tick_params(axis="y", labelsize="small")
        ax1.axvline(0, color="black")
        ax1.set_title("Gains regroupés par équipement (moyenne multi-mesures)")
        ax1.set_xlabel("Réduction relative de l'erreur absolue par équipement")
        ax1.set_ylabel("Équipement")
        #
        self.equi_name_sorted = name_sorted[::-1]

    def postGainHeatMap(self):
        def get_equipment(name):
            return name.split(".")[0]

        def get_variable(name):
            return name.split(".")[-1]

        name_equi = numpy.unique([get_equipment(name) for name in self.y_names])
        name_vari = numpy.unique([get_variable(name) for name in self.y_names])
        heat_valu = dict(
            [str(ne), dict([str(nv), []] for nv in name_vari)] for ne in name_equi
        )
        for i, name in enumerate(self.y_names):
            equi = get_equipment(name)
            vari = get_variable(name)
            heat_valu[equi][vari].append(float(self.measure_err_gain[i]))
        heat_tabl = numpy.zeros((len(name_equi), len(name_vari)))
        for i, equi in enumerate(self.equi_name_sorted):
            for j, vari in enumerate(name_vari):
                if vari in heat_valu[equi] and len(heat_valu[equi][vari])>0:
                    heat_tabl[i][j] = float(numpy.mean(heat_valu[equi][vari]))
                else:
                    heat_tabl[i][j] = 0.0
        #
        nbr = len(name_vari)
        figs = plt.figure(figsize=(4, nbr * 6))
        for sub in range(nbr):
            ax = figs.add_subplot(nbr, 1, sub + 1)
            ax.imshow(heat_tabl[:, sub].reshape((-1, 1)), aspect="auto", cmap="autumn")
            ax.set_xticks(
                [
                    0,
                ],
                labels=[
                    "Variable physique %s" % name_vari[sub],
                ],
            )
            ax.set_yticks(
                range(len(self.equi_name_sorted)), labels=self.equi_name_sorted
            )
            valfmt = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
            for i in range(len(self.equi_name_sorted)):
                # for j in range(len(name_vari)):
                ax.text(
                    0,
                    i,
                    valfmt(heat_tabl[i, sub], None),
                    ha="center",
                    va="center",
                    color="k",
                )
            ax.set_title("Gains par équipement")
            ax.set_ylabel("Équipement")


# ==============================================================================
if __name__ == "__main__":
    print()
    print("EXECUTION DIRECTE")
    print()
    etude = CalibrationProcessingObject()
    print()
