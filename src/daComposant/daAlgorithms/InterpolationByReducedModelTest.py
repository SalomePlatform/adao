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

import numpy, math
from daCore import BasicObjects, PlatformInfo
from daCore.PlatformInfo import vfloat
from daAlgorithms.Atoms import ecweim
mpr = PlatformInfo.PlatformInfo().MachinePrecision()
mfp = PlatformInfo.PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        #
        BasicObjects.Algorithm.__init__(self, "INTERPOLATIONBYREDUCEDMODELTEST")
        self.defineRequiredParameter(
            name     = "ReducedBasis",
            default  = [],
            typecast = numpy.array,
            message  = "Base réduite, 1 vecteur par colonne",
        )
        self.defineRequiredParameter(
            name     = "MeasurementLocations",
            default  = [],
            typecast = tuple,
            message  = "Liste des indices ou noms de positions optimales de mesure selon l'ordre interne d'un vecteur de base",  # noqa: E501
        )
        self.defineRequiredParameter(
            name     = "EnsembleOfSnapshots",
            default  = [],
            typecast = numpy.array,
            message  = "Ensemble de vecteurs d'état physique (snapshots), 1 état par colonne (Test Set)",
        )
        self.defineRequiredParameter(
            name     = "ErrorNorm",
            default  = "L2",
            typecast = str,
            message  = "Norme d'erreur utilisée pour le critère d'optimalité des positions",
            listval  = ["L2", "Linf"]
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
        self.requireInputArguments(
            mandatory= (),
            optional = (),
        )
        self.setAttributes(
            tags=(
                "Reduction",
                "Interpolation",
            ),
            features=(
                "DerivativeFree",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        __rb  = self._parameters["ReducedBasis"]
        __ip  = self._parameters["MeasurementLocations"]
        __eos = self._parameters["EnsembleOfSnapshots"]
        __rdim, __nrb = __rb.shape
        __fdim, __nsn = __eos.shape
        #
        if __fdim != __rdim:
            raise ValueError("The dimension of each snapshot (%i) has to be equal to the dimension of each reduced basis vector (%i)."%(__fdim, __rdim))  # noqa: E501
        if __fdim < len(__ip):
            raise ValueError("The dimension of each snapshot (%i) has to be greater or equal to the number of optimal measurement locations (%i)."%(__fdim, len(__ip)))  # noqa: E501
        #
        # --------------------------
        __s = self._parameters["ShowElementarySummary"]
        __p = self._parameters["NumberOfPrintedDigits"]
        __r = __nsn
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
        msgs += (__marge + "This test allows to analyze the quality of the interpolation of states,\n")
        msgs += (__marge + "using a reduced basis and measurements at specified points.\n")
        msgs += ("\n")
        msgs += (__marge + "The output shows simple statistics related to normalized errors of the\n")
        msgs += (__marge + "interpolation with reduced basis using pseudo-measures coming from each\n")
        msgs += (__marge + "snapshot included in the given test set.\n")
        msgs += ("\n")
        msgs += (__marge + "Warning:  in order to be coherent, this test has to use the same norm\n")
        msgs += (__marge + "than the one used to build the reduced basis. The user chosen norm in\n")
        msgs += (__marge + "this test is presently \"%s\". Check the RB building one.\n"%(self._parameters["ErrorNorm"],))  # noqa: E501
        msgs += ("\n")
        msgs += (__flech + "Information before launching:\n")
        msgs += (__marge + "-----------------------------\n")
        msgs += ("\n")
        msgs += (__marge + "Characteristics of input data:\n")
        msgs += (__marge + "  State dimension................: %i\n")%__fdim
        msgs += (__marge + "  Dimension of RB................: %i\n")%__nrb
        msgs += (__marge + "  Number of measures locations...: %i\n")%len(__ip)
        msgs += (__marge + "  Number of snapshots to test....: %i\n")%__nsn
        msgs += ("\n")
        msgs += (__marge + "%s\n\n"%("-" * 75,))
        #
        st = "Normalized interpolation error test using \"%s\" norm for all given states:"%self._parameters["ErrorNorm"]
        msgs += (__flech + "%s\n"%st)
        msgs += (__marge + "%s\n"%("-" * len(st),))
        msgs += ("\n")
        Ns, Es = [], []
        for ns in range(__nsn):
            # __rm = __eos[__ip, ns]
            __im = ecweim.EIM_online(self, __rb, __eos[__ip, ns], __ip)
            #
            if self._parameters["ErrorNorm"] == "L2":
                __norms = numpy.linalg.norm( __eos[:, ns] )
                __ecart = vfloat(numpy.linalg.norm( __eos[:, ns] - __im ) / __norms )
            else:
                __norms = numpy.linalg.norm( __eos[:, ns], ord=numpy.inf )
                __ecart = vfloat(numpy.linalg.norm( __eos[:, ns] - __im, ord=numpy.inf ) / __norms )
            Ns.append( __norms )
            Es.append( __ecart )
            if __s:
                msgs += (__marge + "State %0" + str(__ordre) + "i: error of %." + str(__p) + "e for a state norm of %." + str(__p) + "e (= %3i%s)\n")%(ns, __ecart, __norms, 100 * __ecart / __norms, "%")  # noqa: E501
        msgs += ("\n")
        msgs += (__marge + "%s\n"%("-" * 75,))
        #
        if __r > 1:
            msgs += ("\n")
            msgs += (__flech + "Launching statistical summary calculation for %i states\n"%__r)
            msgs += ("\n")
            msgs += (__marge + "Statistical analysis of the errors Es obtained over the collection of states\n")
            msgs += (__marge + "(Remark: numbers that are (about) under %.0e represent 0 to machine precision)\n"%mpr)
            msgs += ("\n")
            Yy = numpy.array( Es )
            msgs += (__marge + "Number of evaluations...........................: %i\n")%len( Es )
            msgs += ("\n")
            msgs += (__marge + "Characteristics of the whole set of error outputs Es:\n")
            msgs += (__marge + "  Minimum value of the whole set of outputs.....: %." + str(__p) + "e\n")%numpy.min(  Yy )  # noqa: E501
            msgs += (__marge + "  Maximum value of the whole set of outputs.....: %." + str(__p) + "e\n")%numpy.max(  Yy )  # noqa: E501
            msgs += (__marge + "  Mean of vector of the whole set of outputs....: %." + str(__p) + "e\n")%numpy.mean( Yy, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the whole set of outputs....: %." + str(__p) + "e\n")%numpy.std(  Yy, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "%s\n"%("-" * 75,))
        #
        msgs += ("\n")
        msgs += (__marge + "End of the \"%s\" verification\n\n"%self._name)
        msgs += (__marge + "%s\n"%("-" * 75,))
        print(msgs)  # 1
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
