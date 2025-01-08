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

import numpy
from daCore import BasicObjects, NumericObjects
from daCore.PlatformInfo import PlatformInfo, vfloat
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ADJOINTTEST")
        self.defineRequiredParameter(
            name     = "ResiduFormula",
            default  = "ScalarProduct",
            typecast = str,
            message  = "Formule de résidu utilisée",
            listval  = ["ScalarProduct"],
        )
        self.defineRequiredParameter(
            name     = "AmplitudeOfInitialDirection",
            default  = 1.,
            typecast = float,
            message  = "Amplitude de la direction initiale de la dérivée directionnelle autour du point nominal",
        )
        self.defineRequiredParameter(
            name     = "EpsilonMinimumExponent",
            default  = -8,
            typecast = int,
            message  = "Exposant minimal en puissance de 10 pour le multiplicateur d'incrément",
            minval   = -20,
            maxval   = 0,
        )
        self.defineRequiredParameter(
            name     = "InitialDirection",
            default  = [],
            typecast = list,
            message  = "Direction initiale de la dérivée directionnelle autour du point nominal",
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
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
        )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "CurrentState",
                "Residu",
                "SimulatedObservationAtCurrentState",
            ]
        )
        self.requireInputArguments(
            mandatory= ("Xb", "HO"),
            optional = ("Y", ),
        )
        self.setAttributes(
            tags=(
                "Checking",
            ),
            features=(
                "DerivativeNeeded",
                "ParallelDerivativesOnly",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        Hm = HO["Direct"].appliedTo
        Ht = HO["Tangent"].appliedInXTo
        Ha = HO["Adjoint"].appliedInXTo
        #
        X0      = numpy.ravel( Xb ).reshape((-1, 1))
        #
        # ----------
        __p = self._parameters["NumberOfPrintedDigits"]
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
        msgs += (__marge + "This test allows to analyze the quality of an adjoint operator associated\n")
        msgs += (__marge + "to some given direct operator F, applied to one single vector argument x.\n")
        msgs += (__marge + "If the adjoint operator is approximated and not given, the test measures\n")
        msgs += (__marge + "the quality of the automatic approximation, around an input checking point X.\n")
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
        msgs += (__marge + "%s\n\n"%("-" * 75,))
        msgs += (__flech + "Numerical quality indicators:\n")
        msgs += (__marge + "-----------------------------\n")
        msgs += ("\n")
        #
        if self._parameters["ResiduFormula"] == "ScalarProduct":
            msgs += (__marge + "Using the \"%s\" formula, one observes the residue R which is the\n"%self._parameters["ResiduFormula"])  # noqa: E501
            msgs += (__marge + "difference of two scalar products:\n")
            msgs += ("\n")
            msgs += (__marge + "    R(Alpha) = | < TangentF_X(dX) , Y > - < dX , AdjointF_X(Y) > |\n")
            msgs += ("\n")
            msgs += (__marge + "which must remain constantly equal to zero to the accuracy of the calculation.\n")
            msgs += (__marge + "One takes dX0 = Normal(0,X) and dX = Alpha*dX0, where F is the calculation\n")
            msgs += (__marge + "operator. If it is given, Y must be in the image of F. If it is not given,\n")
            msgs += (__marge + "one takes Y = F(X).\n")
            #
            __entete = str.rstrip(
                "  i   Alpha  " + \
                str.center("||X||", 2 + __p + 7)  + \
                str.center("||Y||", 2 + __p + 7)  + \
                str.center("||dX||", 2 + __p + 7) + \
                str.center("R(Alpha)", 2 + __p + 7)
            )
            __nbtirets = len(__entete) + 2
            #
        msgs += ("\n")
        msgs += (__marge + "(Remark: numbers that are (about) under %.0e represent 0 to machine precision)\n"%mpr)
        print(msgs)  # 1
        #
        Perturbations = [ 10**i for i in range(self._parameters["EpsilonMinimumExponent"], 1) ]
        Perturbations.reverse()
        #
        NormeX  = numpy.linalg.norm( X0 )
        if Y is None:
            Yn = numpy.ravel( Hm( X0 ) ).reshape((-1, 1))
        else:
            Yn = numpy.ravel( Y ).reshape((-1, 1))
        NormeY = numpy.linalg.norm( Yn )
        if self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( X0 )
        if self._toStore("SimulatedObservationAtCurrentState"):
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( Yn )
        #
        dX0 = NumericObjects.SetInitialDirection(
            self._parameters["InitialDirection"],
            self._parameters["AmplitudeOfInitialDirection"],
            X0,
        )
        #
        # Boucle sur les perturbations
        # ----------------------------
        msgs  = ("")  # 2
        msgs += "\n" + __marge + "-" * __nbtirets
        msgs += "\n" + __marge + __entete
        msgs += "\n" + __marge + "-" * __nbtirets
        msgs += ("\n")
        __pf = "  %" + str(__p + 7) + "." + str(__p) + "e"
        __ms = "  %2i  %5.0e" + (__pf * 4) + "\n"
        for ip, amplitude in enumerate(Perturbations):
            dX          = amplitude * dX0
            NormedX     = numpy.linalg.norm( dX )
            #
            if self._parameters["ResiduFormula"] == "ScalarProduct":
                TangentFXdX = numpy.ravel( Ht( (X0, dX) ) )
                AdjointFXY  = numpy.ravel( Ha( (X0, Yn)  ) )
                #
                Residu = abs(vfloat(numpy.dot( TangentFXdX, Yn ) - numpy.dot( dX, AdjointFXY )))
                #
                self.StoredVariables["Residu"].store( Residu )
                ttsep = __ms%(ip, amplitude, NormeX, NormeY, NormedX, Residu)
                msgs += __marge + ttsep
        #
        msgs += (__marge + "-" * __nbtirets + "\n\n")
        msgs += (__marge + "End of the \"%s\" verification by the \"%s\" formula.\n\n"%(self._name, self._parameters["ResiduFormula"]))  # noqa: E501
        msgs += (__marge + "%s\n"%("-" * 75,))
        print(msgs)  # 2
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
