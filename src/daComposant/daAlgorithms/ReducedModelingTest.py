# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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

import math, numpy, logging
import daCore
from daCore import BasicObjects, PlatformInfo
from daCore.NumericObjects import FindIndexesFromNames, SingularValuesEstimation
from daAlgorithms.Atoms import eosg
lpi = PlatformInfo.PlatformInfo()
mpr = lpi.MachinePrecision()
mfp = lpi.MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "REDUCEDMODELINGTEST")
        self.defineRequiredParameter(
            name     = "EnsembleOfSnapshots",
            default  = [],
            typecast = numpy.array,
            message  = "Ensemble de vecteurs d'état physique (snapshots), 1 état par colonne (Training Set)",
        )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfLocations",
            default  = 1,
            typecast = int,
            message  = "Nombre maximal de positions",
            minval   = 0,
        )
        self.defineRequiredParameter(
            name     = "ExcludeLocations",
            default  = [],
            typecast = tuple,
            message  = "Liste des indices ou noms de positions exclues selon l'ordre interne d'un snapshot",
        )
        self.defineRequiredParameter(
            name     = "NameOfLocations",
            default  = [],
            typecast = tuple,
            message  = "Liste des noms de positions selon l'ordre interne d'un snapshot",
        )
        self.defineRequiredParameter(
            name     = "SampleAsnUplet",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par une liste de n-uplet",
        )
        self.defineRequiredParameter(
            name     = "SampleAsExplicitHyperCube",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonnages explicites de chaque variable comme une liste",  # noqa: E501
        )
        self.defineRequiredParameter(
            name     = "SampleAsMinMaxStepHyperCube",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont on donne la liste des échantillonnages implicites de chaque variable par un triplet [min,max,step]",  # noqa: E501
        )
        self.defineRequiredParameter(
            name     = "SampleAsMinMaxLatinHyperCube",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube Latin dont on donne les bornes de chaque variable par une paire [min,max], suivi du nombre de points demandés",  # noqa: E501
        )
        self.defineRequiredParameter(
            name     = "SampleAsMinMaxSobolSequence",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par une séquence de Sobol dont on donne les bornes de chaque variable par une paire [min,max], suivi de la paire [dimension, nombre minimal de points demandés]",  # noqa: E501
        )
        self.defineRequiredParameter(
            name     = "SampleAsIndependantRandomVariables",
            default  = [],
            typecast = tuple,
            message  = "Points de calcul définis par un hyper-cube dont les points sur chaque axe proviennent de l'échantillonnage indépendant de la variable selon la spécification ['distribution',[parametres],nombre]",  # noqa: E501
        )
        self.defineRequiredParameter(
            name     = "SetDebug",
            default  = False,
            typecast = bool,
            message  = "Activation du mode debug lors de l'exécution",
        )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "EnsembleOfSimulations",
                "EnsembleOfStates",
                "Residus",
                "SingularValues",
            ]
        )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
        )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfModes",
            default  = 1000000,
            typecast = int,
            message  = "Nombre maximal de modes pour l'analyse",
            minval   = 0,
        )
        self.defineRequiredParameter(
            name     = "ShowElementarySummary",
            default  = True,
            typecast = bool,
            message  = "Calcule et affiche un résumé à chaque évaluation élémentaire",
        )
        self.defineRequiredParameter(
            name     = "NumberOfPrintedDigits",
            default  = 5,
            typecast = int,
            message  = "Nombre de chiffres affichés pour les impressions de réels",
            minval   = 0,
        )
        self.defineRequiredParameter(
            name     = "ResultTitle",
            default  = "",
            typecast = str,
            message  = "Titre du tableau et de la figure",
        )
        self.defineRequiredParameter(
            name     = "ResultFile",
            default  = self._name + "_result_file.pdf",
            typecast = str,
            message  = "Nom de base (y.c. extension) des fichiers de sauvegarde des résultats",
        )
        self.defineRequiredParameter(
            name     = "PlotAndSave",
            default  = False,
            typecast = bool,
            message  = "Trace et sauve les résultats",
        )
        self.requireInputArguments(
            mandatory= (),
            optional = ("Xb", "HO"),
        )
        self.setAttributes(
            tags=(
                "Reduction",
                "Checking",
            ),
            features=(
                "DerivativeFree",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        if len(self._parameters["EnsembleOfSnapshots"]) > 0:
            if self._toStore("EnsembleOfSimulations"):
                self.StoredVariables["EnsembleOfSimulations"].store( self._parameters["EnsembleOfSnapshots"] )
            EOS = self._parameters["EnsembleOfSnapshots"]
        elif isinstance(HO, dict):
            EOS = eosg.eosg(self, Xb, HO)
        else:
            raise ValueError("Snapshots or Operator have to be given in order to launch the analysis")
        #
        if isinstance(EOS, (numpy.ndarray, numpy.matrix)):
            __EOS = numpy.asarray(EOS)
        elif isinstance(EOS, (list, tuple, daCore.Persistence.Persistence)):
            __EOS = numpy.stack([numpy.ravel(_sn) for _sn in EOS], axis=1)
        else:
            raise ValueError("EnsembleOfSnapshots has to be an array/matrix (each column being a vector) or a list/tuple (each element being a vector).")  # noqa: E501
        __dimS, __nbmS = __EOS.shape
        logging.debug("%s Using a collection of %i snapshots of individual size of %i"%(self._name, __nbmS, __dimS))
        #
        __fdim, __nsn = __EOS.shape
        #
        # --------------------------
        __s = self._parameters["ShowElementarySummary"]
        __p = self._parameters["NumberOfPrintedDigits"]
        #
        __marge = 5 * u" "
        __flech = 3 * "=" + "> "
        __ordre = int(math.log10(__nsn)) + 1
        msgs  = ("\n")  # 1
        if len(self._parameters["ResultTitle"]) > 0:
            __rt = str(self._parameters["ResultTitle"])
            msgs += (__marge + "====" + "=" * len(__rt) + "====\n")
            msgs += (__marge + "    " + __rt + "\n")
            msgs += (__marge + "====" + "=" * len(__rt) + "====\n")
        else:
            msgs += (__marge + "%s\n"%self._name)
            msgs += (__marge + "%s\n"%("=" * len(self._name),))
        #
        msgs += ("\n")
        msgs += (__marge + "This test allows to analyze the characteristics of the collection of\n")
        msgs += (__marge + "states from a reduction point of view. Using an SVD, it measures how\n")
        msgs += (__marge + "the information decreases with the number of singular values, either\n")
        msgs += (__marge + "as values or, with a statistical point of view, as remaining variance.\n")
        msgs += ("\n")
        msgs += (__flech + "Information before launching:\n")
        msgs += (__marge + "-----------------------------\n")
        msgs += ("\n")
        msgs += (__marge + "Characteristics of input data:\n")
        msgs += (__marge + "  State dimension................: %i\n")%__fdim
        msgs += (__marge + "  Number of snapshots to test....: %i\n")%__nsn
        #
        if "ExcludeLocations" in self._parameters:
            __ExcludedPoints = self._parameters["ExcludeLocations"]
        else:
            __ExcludedPoints = ()
        if "NameOfLocations" in self._parameters:
            if isinstance(self._parameters["NameOfLocations"], (list, numpy.ndarray, tuple)) \
                    and len(self._parameters["NameOfLocations"]) == __dimS:
                __NameOfLocations = self._parameters["NameOfLocations"]
            else:
                __NameOfLocations = ()
        else:
            __NameOfLocations = ()
        if len(__ExcludedPoints) > 0:
            __ExcludedPoints = FindIndexesFromNames( __NameOfLocations, __ExcludedPoints )
            __ExcludedPoints = numpy.ravel(numpy.asarray(__ExcludedPoints, dtype=int))
            __IncludedPoints = numpy.setdiff1d(
                numpy.arange(__EOS.shape[0]),
                __ExcludedPoints,
                assume_unique = True,
            )
        else:
            __IncludedPoints = []
        if len(__IncludedPoints) > 0:
            __Ensemble = numpy.take(__EOS, __IncludedPoints, axis=0, mode='clip')
        else:
            __Ensemble = __EOS
        #
        __sv, __svsq, __tisv, __qisv = SingularValuesEstimation( __Ensemble )
        if self._parameters["MaximumNumberOfModes"] < len(__sv):
            __sv   = __sv[:self._parameters["MaximumNumberOfModes"]]
            __tisv = __tisv[:self._parameters["MaximumNumberOfModes"]]
            __qisv = __qisv[:self._parameters["MaximumNumberOfModes"]]
        #
        if self._toStore("SingularValues"):
            self.StoredVariables["SingularValues"].store( __sv )
        if self._toStore("Residus"):
            self.StoredVariables["Residus"].store( __qisv )
        #
        nbsv = min(5, self._parameters["MaximumNumberOfModes"])
        msgs += ("\n")
        msgs += (__flech + "Summary of the %i first singular values:\n"%nbsv)
        msgs += (__marge + "---------------------------------------\n")
        msgs += ("\n")
        msgs += (__marge + "Singular values σ:\n")
        for i in range(nbsv):
            msgs += __marge + ("  σ[%i] = %." + str(__p) + "e\n")%(i + 1, __sv[i])
        msgs += ("\n")
        msgs += (__marge + "Singular values σ divided by the first one σ[1]:\n")
        for i in range(nbsv):
            msgs += __marge + ("  σ[%i] / σ[1] = %." + str(__p) + "e\n")%(i + 1, __sv[i] / __sv[0])
        #
        if __s:
            msgs += ("\n")
            msgs += (__flech + "Ordered singular values and remaining variance:\n")
            msgs += (__marge + "-----------------------------------------------\n")
            __entete = ("  %" + str(__ordre) + "s  | %16s | %16s | Variance: part, remaining")%("i", "Singular value σ", "σ[i]/σ[1]")  # noqa: E501
            #
            __nbtirets = len(__entete) + 2
            msgs += "\n" + __marge + "-" * __nbtirets
            msgs += "\n" + __marge + __entete
            msgs += "\n" + __marge + "-" * __nbtirets
            msgs += ("\n")
        #
        cut1pd, cut1pc, cut1pm, cut1pi = 1, 1, 1, 1
        for ns in range(len(__sv)):
            svalue = __sv[ns]
            rvalue = __sv[ns] / __sv[0]
            vsinfo = 100 * __tisv[ns]
            rsinfo = max(100 * __qisv[ns], 0.)
            if __s:
                msgs += (__marge + "  %0" + str(__ordre) + "i  | %16." + str(__p) + "e | %16." + str(__p) + "e |           %2i%s ,    %4.1f%s\n")%(ns, svalue, rvalue, vsinfo, "%", rsinfo, "%")  # noqa: E501
            if rsinfo > 10:
                cut1pd = ns + 2  # 10%
            if rsinfo > 1:
                cut1pc = ns + 2  # 1%
            if rsinfo > 0.1:
                cut1pm = ns + 2  # 1‰
            if rsinfo > 0.01:
                cut1pi = ns + 2  # 0.1‰
        #
        if __s:
            msgs += __marge + "-" * __nbtirets + "\n"
        msgs += ("\n")
        msgs += (__flech + "Summary of variance cut-off:\n")
        msgs += (__marge + "----------------------------\n")
        if cut1pd > 0:
            msgs += __marge + "Representing more than 90%s    of variance requires at least %i mode(s).\n"%("%", cut1pd)
        if cut1pc > 0:
            msgs += __marge + "Representing more than 99%s    of variance requires at least %i mode(s).\n"%("%", cut1pc)
        if cut1pm > 0:
            msgs += __marge + "Representing more than 99.9%s  of variance requires at least %i mode(s).\n"%("%", cut1pm)
        if cut1pi > 0:
            msgs += __marge + "Representing more than 99.99%s of variance requires at least %i mode(s).\n"%("%", cut1pi)
        #
        if lpi.has_matplotlib and self._parameters["PlotAndSave"]:
            # Evite les message debug de matplotlib
            dL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.WARNING)
            try:
                msgs += ("\n")
                msgs += (__marge + "Plot and save results in a file named \"%s\"\n"%str(self._parameters["ResultFile"]))
                #
                import matplotlib.pyplot as plt
                fig = plt.figure(figsize=(10, 15))
                plt.tight_layout()
                if len(self._parameters["ResultTitle"]) > 0:
                    fig.suptitle(self._parameters["ResultTitle"])
                else:
                    fig.suptitle("Singular values analysis on an ensemble of %i snapshots\n"%__nsn)
                # ----
                ax = fig.add_subplot(3, 1, 1)
                ax.set_xlabel("Singular values index, numbered from 1 (first %i ones)"%len(__qisv))
                ax.set_ylabel("Remaining variance to be explained (%, linear scale)", color="tab:blue")
                ax.grid(True, which='both', color="tab:blue")
                ax.set_xlim(1, 1 + len(__qisv))
                ax.set_ylim(0, 100)
                ax.plot(range(1, 1 + len(__qisv)), 100 * __qisv, linewidth=2, color="b", label="On linear scale")
                ax.tick_params(axis='y', labelcolor="tab:blue")
                ax.yaxis.set_major_formatter('{x:.0f}%')
                #
                rg = ax.twinx()
                rg.set_ylabel("Remaining variance to be explained (%, log scale)", color="tab:red")
                rg.grid(True, which='both', color="tab:red")
                rg.set_xlim(1, 1 + len(__qisv))
                rg.set_yscale("log")
                rg.plot(range(1, 1 + len(__qisv)), 100 * __qisv, linewidth=2, color="r", label="On log10 scale")
                rg.set_ylim(rg.get_ylim()[0], 101)
                rg.tick_params(axis='y', labelcolor="tab:red")
                # ----
                ax = fig.add_subplot(3, 1, 2)
                ax.set_ylabel("Singular values")
                ax.set_xlim(1, 1 + len(__sv))
                ax.plot(range(1, 1 + len(__sv)), __sv, linewidth=2)
                ax.grid(True)
                # ----
                ax = fig.add_subplot(3, 1, 3)
                ax.set_ylabel("Singular values (log scale)")
                ax.grid(True, which='both')
                ax.set_xlim(1, 1 + len(__sv))
                ax.set_xscale("log")
                ax.set_yscale("log")
                ax.plot(range(1, 1 + len(__sv)), __sv, linewidth=2)
                # ----
                plt.savefig(str(self._parameters["ResultFile"]))
                plt.close(fig)
            except Exception:
                msgs += ("\n")
                msgs += (__marge + "Saving figure fail, please update your Matplolib version.\n")
                msgs += ("\n")
            logging.getLogger().setLevel(dL)
            #
        msgs += ("\n")
        msgs += (__marge + "%s\n"%("-" * 75,))
        msgs += ("\n")
        msgs += (__marge + "End of the \"%s\" verification\n\n"%self._name)
        msgs += (__marge + "%s\n"%("-" * 75,))
        print(msgs)  # 3
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
