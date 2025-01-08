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

import numpy, copy, logging
from daCore import BasicObjects, PlatformInfo
mpr = PlatformInfo.PlatformInfo().MachinePrecision()
mfp = PlatformInfo.PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "CONTROLEDFUNCTIONTEST")
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
            name     = "NumberOfRepetition",
            default  = 1,
            typecast = int,
            message  = "Nombre de fois où l'exécution de la fonction est répétée",
            minval   = 1,
        )
        self.defineRequiredParameter(
            name     = "ResultTitle",
            default  = "",
            typecast = str,
            message  = "Titre du tableau et de la figure",
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
                "CurrentState",
                "SimulatedObservationAtCurrentState",
            ]
        )
        self.requireInputArguments(
            mandatory= ("Xb", "HO"),
            optional = ("U"),
        )
        self.setAttributes(
            tags=(
                "Checking",
            ),
            features=(
                "DerivativeFree",
                "ParallelFree",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        FunctionToTest = HO["Direct"].appliedControledFormTo
        #
        X0 = copy.copy( Xb )
        if U is not None:
            if hasattr(U, "store") and len(U) > 1:
                Un = numpy.ravel( U[-1] ).reshape((-1, 1))
            elif hasattr(U, "store") and len(U) == 1:
                Un = numpy.ravel( U[0] ).reshape((-1, 1))
            else:
                Un = numpy.ravel( U ).reshape((-1, 1))
        else:
            Un = None
        #
        # ----------
        __s = self._parameters["ShowElementarySummary"]
        __p = self._parameters["NumberOfPrintedDigits"]
        __r = self._parameters["NumberOfRepetition"]
        #
        __marge = 5 * u" "
        __flech = 3 * "=" + "> "
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
        msgs += (__marge + "This test allows to analyze the (repetition of the) launch of some\n")
        msgs += (__marge + "given simulation operator F, applied to one single vector x and to\n")
        msgs += (__marge + "one control vector u as arguments, in a sequential way.\n")
        msgs += (__marge + "The output shows simple statistics related to its successful execution,\n")
        msgs += (__marge + "or related to the similarities of repetition of its execution.\n")
        msgs += ("\n")
        msgs += (__flech + "Information before launching:\n")
        msgs += (__marge + "-----------------------------\n")
        msgs += ("\n")
        msgs += (__marge + "Characteristics of input vector X, internally converted:\n")
        msgs += (__marge + "  Type...............: %s\n")%type( X0 )
        msgs += (__marge + "  Length of vector...: %i\n")%max(numpy.ravel( X0 ).shape)
        msgs += (__marge + "  Minimum value......: %." + str(__p) + "e\n")%numpy.min(  X0 )
        msgs += (__marge + "  Maximum value......: %." + str(__p) + "e\n")%numpy.max(  X0 )
        msgs += (__marge + "  Mean of vector.....: %." + str(__p) + "e\n")%numpy.mean( X0, dtype=mfp )
        msgs += (__marge + "  Standard error.....: %." + str(__p) + "e\n")%numpy.std(  X0, dtype=mfp )
        msgs += (__marge + "  L2 norm of vector..: %." + str(__p) + "e\n")%numpy.linalg.norm( X0 )
        msgs += ("\n")
        if Un is None:
            msgs += (__marge + "Characteristics of control parameter U, internally converted: None\n")
        else:
            msgs += (__marge + "Characteristics of control parameter U, internally converted:\n")
            msgs += (__marge + "  Type...............: %s\n")%type( Un )
            msgs += (__marge + "  Length of vector...: %i\n")%max(numpy.ravel( Un ).shape)
            msgs += (__marge + "  Minimum value......: %." + str(__p) + "e\n")%numpy.min(  Un )
            msgs += (__marge + "  Maximum value......: %." + str(__p) + "e\n")%numpy.max(  Un )
            msgs += (__marge + "  Mean of vector.....: %." + str(__p) + "e\n")%numpy.mean( Un, dtype=mfp )
            msgs += (__marge + "  Standard error.....: %." + str(__p) + "e\n")%numpy.std(  Un, dtype=mfp )
            msgs += (__marge + "  L2 norm of vector..: %." + str(__p) + "e\n")%numpy.linalg.norm( Un )
        msgs += ("\n")
        msgs += (__marge + "%s\n\n"%("-" * 75,))
        #
        if self._parameters["SetDebug"]:
            CUR_LEVEL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.DEBUG)
            if __r > 1:
                msgs += (__flech + "Beginning of repeated evaluation, activating debug\n")
            else:
                msgs += (__flech + "Beginning of evaluation, activating debug\n")
        else:
            if __r > 1:
                msgs += (__flech + "Beginning of repeated evaluation, without activating debug\n")
            else:
                msgs += (__flech + "Beginning of evaluation, without activating debug\n")
        print(msgs)  # 1
        #
        # ----------
        HO["Direct"].disableAvoidingRedundancy()
        # ----------
        Ys = []
        for i in range(__r):
            if self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( X0 )
            if __s:
                msgs  = (__marge + "%s\n"%("-" * 75,))  # 2-1
                if __r > 1:
                    msgs += ("\n")
                    msgs += (__flech + "Repetition step number %i on a total of %i\n"%(i + 1, __r))
                msgs += ("\n")
                msgs += (__flech + "Launching operator sequential evaluation\n")
                print(msgs)  # 2-1
            #
            Yn = FunctionToTest( (X0, Un) )
            #
            if __s:
                msgs  = ("\n")  # 2-2
                msgs += (__flech + "End of operator sequential evaluation\n")
                msgs += ("\n")
                msgs += (__flech + "Information after evaluation:\n")
                msgs += ("\n")
                msgs += (__marge + "Characteristics of simulated output vector Y=F((X,U)), to compare to others:\n")
                msgs += (__marge + "  Type...............: %s\n")%type( Yn )
                msgs += (__marge + "  Length of vector...: %i\n")%max(numpy.ravel( Yn ).shape)
                msgs += (__marge + "  Minimum value......: %." + str(__p) + "e\n")%numpy.min(  Yn )
                msgs += (__marge + "  Maximum value......: %." + str(__p) + "e\n")%numpy.max(  Yn )
                msgs += (__marge + "  Mean of vector.....: %." + str(__p) + "e\n")%numpy.mean( Yn, dtype=mfp )
                msgs += (__marge + "  Standard error.....: %." + str(__p) + "e\n")%numpy.std(  Yn, dtype=mfp )
                msgs += (__marge + "  L2 norm of vector..: %." + str(__p) + "e\n")%numpy.linalg.norm( Yn )
                print(msgs)  # 2-2
            if self._toStore("SimulatedObservationAtCurrentState"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(Yn) )
            #
            Ys.append( copy.copy( numpy.ravel(
                Yn
            ) ) )
        # ----------
        HO["Direct"].enableAvoidingRedundancy()
        # ----------
        #
        msgs  = (__marge + "%s\n\n"%("-" * 75,))  # 3
        if self._parameters["SetDebug"]:
            if __r > 1:
                msgs += (__flech + "End of repeated evaluation, deactivating debug if necessary\n")
            else:
                msgs += (__flech + "End of evaluation, deactivating debug if necessary\n")
            logging.getLogger().setLevel(CUR_LEVEL)
        else:
            if __r > 1:
                msgs += (__flech + "End of repeated evaluation, without deactivating debug\n")
            else:
                msgs += (__flech + "End of evaluation, without deactivating debug\n")
        msgs += ("\n")
        msgs += (__marge + "%s\n"%("-" * 75,))
        #
        if __r > 1:
            msgs += ("\n")
            msgs += (__flech + "Launching statistical summary calculation for %i states\n"%__r)
            msgs += ("\n")
            msgs += (__marge + "%s\n"%("-" * 75,))
            msgs += ("\n")
            msgs += (__flech + "Statistical analysis of the outputs obtained through sequential repeated evaluations\n")  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "(Remark: numbers that are (about) under %.0e represent 0 to machine precision)\n"%mpr)  # noqa: E501
            msgs += ("\n")
            Yy = numpy.array( Ys )
            msgs += (__marge + "Number of evaluations...........................: %i\n")%len( Ys )
            msgs += ("\n")
            msgs += (__marge + "Characteristics of the whole set of outputs Y:\n")
            msgs += (__marge + "  Size of each of the outputs...................: %i\n")%Ys[0].size
            msgs += (__marge + "  Minimum value of the whole set of outputs.....: %." + str(__p) + "e\n")%numpy.min(  Yy )  # noqa: E501
            msgs += (__marge + "  Maximum value of the whole set of outputs.....: %." + str(__p) + "e\n")%numpy.max(  Yy )  # noqa: E501
            msgs += (__marge + "  Mean of vector of the whole set of outputs....: %." + str(__p) + "e\n")%numpy.mean( Yy, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the whole set of outputs....: %." + str(__p) + "e\n")%numpy.std(  Yy, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            Ym = numpy.mean( numpy.array( Ys ), axis=0, dtype=mfp )
            msgs += (__marge + "Characteristics of the vector Ym, mean of the outputs Y:\n")
            msgs += (__marge + "  Size of the mean of the outputs...............: %i\n")%Ym.size
            msgs += (__marge + "  Minimum value of the mean of the outputs......: %." + str(__p) + "e\n")%numpy.min(  Ym )  # noqa: E501
            msgs += (__marge + "  Maximum value of the mean of the outputs......: %." + str(__p) + "e\n")%numpy.max(  Ym )  # noqa: E501
            msgs += (__marge + "  Mean of the mean of the outputs...............: %." + str(__p) + "e\n")%numpy.mean( Ym, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the mean of the outputs.....: %." + str(__p) + "e\n")%numpy.std(  Ym, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            Ye = numpy.mean( numpy.array( Ys ) - Ym, axis=0, dtype=mfp )
            msgs += (__marge + "Characteristics of the mean of the differences between the outputs Y and their mean Ym:\n")  # noqa: E501
            msgs += (__marge + "  Size of the mean of the differences...........: %i\n")%Ye.size
            msgs += (__marge + "  Minimum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.min(  Ye )  # noqa: E501
            msgs += (__marge + "  Maximum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.max(  Ye )  # noqa: E501
            msgs += (__marge + "  Mean of the mean of the differences...........: %." + str(__p) + "e\n")%numpy.mean( Ye, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the mean of the differences.: %." + str(__p) + "e\n")%numpy.std(  Ye, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "%s\n"%("-" * 75,))
        #
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
