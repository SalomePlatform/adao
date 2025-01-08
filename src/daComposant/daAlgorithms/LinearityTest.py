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

import math, numpy
from daCore import BasicObjects, NumericObjects, PlatformInfo
mpr = PlatformInfo.PlatformInfo().MachinePrecision()
mfp = PlatformInfo.PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "LINEARITYTEST")
        self.defineRequiredParameter(
            name     = "ResiduFormula",
            default  = "CenteredDL",
            typecast = str,
            message  = "Formule de résidu utilisée",
            listval  = ["CenteredDL", "Taylor", "NominalTaylor", "NominalTaylorRMS"],
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
            name     = "AmplitudeOfInitialDirection",
            default  = 1.,
            typecast = float,
            message  = "Amplitude de la direction initiale de la dérivée directionnelle autour du point nominal",
        )
        self.defineRequiredParameter(
            name     = "AmplitudeOfTangentPerturbation",
            default  = 1.e-2,
            typecast = float,
            message  = "Amplitude de la perturbation pour le calcul de la forme tangente",
            minval   = 1.e-10,
            maxval   = 1.,
        )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
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

        def RMS(V1, V2):
            import math
            return math.sqrt( ((numpy.ravel(V2) - numpy.ravel(V1))**2).sum() / float(numpy.ravel(V1).size) )
        #
        Hm = HO["Direct"].appliedTo
        if self._parameters["ResiduFormula"] in ["Taylor", "NominalTaylor", "NominalTaylorRMS"]:
            Ht = HO["Tangent"].appliedInXTo
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
        msgs += (__marge + "This test allows to analyze the linearity property of some given\n")
        msgs += (__marge + "simulation operator F, applied to one single vector argument x.\n")
        msgs += (__marge + "The output shows simple statistics related to its stability for various\n")
        msgs += (__marge + "increments, around an input checking point X.\n")
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
        msgs += (__marge + "Using the \"%s\" formula, one observes the residue R which is the\n"%self._parameters["ResiduFormula"])  # noqa: E501
        msgs += (__marge + "following ratio or comparison:\n")
        msgs += ("\n")
        #
        if self._parameters["ResiduFormula"] == "CenteredDL":
            msgs += (__marge + "               || F(X+Alpha*dX) + F(X-Alpha*dX) - 2*F(X) ||\n")
            msgs += (__marge + "    R(Alpha) = --------------------------------------------\n")
            msgs += (__marge + "                               || F(X) ||\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue remains always very small compared to 1, the linearity\n")
            msgs += (__marge + "assumption of F is verified.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue varies a lot, or is of the order of 1 or more, and is\n")
            msgs += (__marge + "small only under a certain order of Alpha increment, the linearity\n")
            msgs += (__marge + "assumption of F is not verified.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue decreases and if the decay is in Alpha**2 according to\n")
            msgs += (__marge + "Alpha, it means that the gradient is well calculated up to the stopping\n")
            msgs += (__marge + "precision of the quadratic decay.\n")
            #
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)  log10( R )"
            #
        if self._parameters["ResiduFormula"] == "Taylor":
            msgs += (__marge + "               || F(X+Alpha*dX) - F(X) - Alpha * GradientF_X(dX) ||\n")
            msgs += (__marge + "    R(Alpha) = ----------------------------------------------------\n")
            msgs += (__marge + "                               || F(X) ||\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue remains always very small compared to 1, the linearity\n")
            msgs += (__marge + "assumption of F is verified.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue varies a lot, or is of the order of 1 or more, and is\n")
            msgs += (__marge + "small only under a certain order of Alpha increment, the linearity\n")
            msgs += (__marge + "assumption of F is not verified.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue decreases and if the decay is in Alpha**2 according to\n")
            msgs += (__marge + "Alpha, it means that the gradient is well calculated up to the stopping\n")
            msgs += (__marge + "precision of the quadratic decay.\n")
            #
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)  log10( R )"
            #
        if self._parameters["ResiduFormula"] == "NominalTaylor":
            msgs += (__marge + "    R(Alpha) = max(\n")
            msgs += (__marge + "        || F(X+Alpha*dX) - Alpha * F(dX) || / || F(X) ||,\n")
            msgs += (__marge + "        || F(X-Alpha*dX) + Alpha * F(dX) || / || F(X) ||,\n")
            msgs += (__marge + "    )\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue remains always equal to 1 within 2 or 3 percent (i.e.\n")
            msgs += (__marge + "|R-1| remains equal to 2 or 3 percent), then the linearity assumption of\n")
            msgs += (__marge + "F is verified.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue is equal to 1 over only a part of the range of variation\n")
            msgs += (__marge + "of the Alpha increment, it is over this part that the linearity assumption\n")
            msgs += (__marge + "of F is verified.\n")
            #
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)   |R-1| in %"
            #
        if self._parameters["ResiduFormula"] == "NominalTaylorRMS":
            msgs += (__marge + "    R(Alpha) = max(\n")
            msgs += (__marge + "        RMS( F(X), F(X+Alpha*dX) - Alpha * F(dX) ) / || F(X) ||,\n")
            msgs += (__marge + "        RMS( F(X), F(X-Alpha*dX) + Alpha * F(dX) ) / || F(X) ||,\n")
            msgs += (__marge + "    )\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue remains always equal to 0 within 1 or 2 percent then the\n")
            msgs += (__marge + "linearity assumption of F is verified.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue is equal to 0 over only a part of the range of variation\n")
            msgs += (__marge + "of the Alpha increment, it is over this part that the linearity assumption\n")
            msgs += (__marge + "of F is verified.\n")
            #
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)    |R| in %"
            #
        msgs += ("\n")
        msgs += (__marge + "We take dX0 = Normal(0,X) and dX = Alpha*dX0. F is the calculation code.\n")
        if (self._parameters["ResiduFormula"] == "Taylor") and ("DifferentialIncrement" in HO and HO["DifferentialIncrement"] is not None):  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "Reminder: gradient operator is obtained internally by finite differences,\n")
            msgs += (__marge + "with a differential increment of value %.2e.\n"%HO["DifferentialIncrement"])
        msgs += ("\n")
        msgs += (__marge + "(Remark: numbers that are (about) under %.0e represent 0 to machine precision)\n"%mpr)
        print(msgs)  # 1
        #
        Perturbations = [ 10**i for i in range(self._parameters["EpsilonMinimumExponent"], 1) ]
        Perturbations.reverse()
        #
        FX      = numpy.ravel( Hm( X0 ) ).reshape((-1, 1))
        NormeX  = numpy.linalg.norm( X0 )
        NormeFX = numpy.linalg.norm( FX )
        if NormeFX < mpr:
            NormeFX = mpr
        if self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( X0 )
        if self._toStore("SimulatedObservationAtCurrentState"):
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX )
        #
        dX0 = NumericObjects.SetInitialDirection(
            self._parameters["InitialDirection"],
            self._parameters["AmplitudeOfInitialDirection"],
            X0,
        )
        #
        if self._parameters["ResiduFormula"] == "Taylor":
            dX1      = float(self._parameters["AmplitudeOfTangentPerturbation"]) * dX0
            GradFxdX = Ht( (X0, dX1) )
            GradFxdX = numpy.ravel( GradFxdX ).reshape((-1, 1))
            GradFxdX = float(1. / self._parameters["AmplitudeOfTangentPerturbation"]) * GradFxdX
        #
        # Boucle sur les perturbations
        # ----------------------------
        __nbtirets = len(__entete) + 2
        msgs  = ("")  # 2
        msgs += "\n" + __marge + "-" * __nbtirets
        msgs += "\n" + __marge + __entete
        msgs += "\n" + __marge + "-" * __nbtirets
        msgs += ("\n")
        #
        for ip, amplitude in enumerate(Perturbations):
            dX      = amplitude * dX0.reshape((-1, 1))
            #
            if self._parameters["ResiduFormula"] == "CenteredDL":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( X0 + dX )
                    self.StoredVariables["CurrentState"].store( X0 - dX )
                #
                FX_plus_dX  = numpy.ravel( Hm( X0 + dX ) ).reshape((-1, 1))
                FX_moins_dX = numpy.ravel( Hm( X0 - dX ) ).reshape((-1, 1))
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX_plus_dX )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX_moins_dX )
                #
                Residu = numpy.linalg.norm( FX_plus_dX + FX_moins_dX - 2 * FX ) / NormeFX
                #
                self.StoredVariables["Residu"].store( Residu )
                ttsep = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %4.0f\n"%(ip, amplitude, NormeX, NormeFX, Residu, math.log10(max(1.e-99, Residu)))  # noqa: E501
                msgs += __marge + ttsep
            #
            if self._parameters["ResiduFormula"] == "Taylor":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( X0 + dX )
                #
                FX_plus_dX  = numpy.ravel( Hm( X0 + dX ) ).reshape((-1, 1))
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX_plus_dX )
                #
                Residu = numpy.linalg.norm( FX_plus_dX - FX - amplitude * GradFxdX ) / NormeFX
                #
                self.StoredVariables["Residu"].store( Residu )
                ttsep = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %4.0f\n"%(ip, amplitude, NormeX, NormeFX, Residu, math.log10(max(1.e-99, Residu)))  # noqa: E501
                msgs += __marge + ttsep
            #
            if self._parameters["ResiduFormula"] == "NominalTaylor":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( X0 + dX )
                    self.StoredVariables["CurrentState"].store( X0 - dX )
                    self.StoredVariables["CurrentState"].store( dX )
                #
                FX_plus_dX  = numpy.ravel( Hm( X0 + dX ) ).reshape((-1, 1))
                FX_moins_dX = numpy.ravel( Hm( X0 - dX ) ).reshape((-1, 1))
                FdX         = numpy.ravel( Hm( dX )      ).reshape((-1, 1))
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX_plus_dX )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX_moins_dX )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FdX )
                #
                Residu = max(
                    numpy.linalg.norm( FX_plus_dX  - amplitude * FdX ) / NormeFX,
                    numpy.linalg.norm( FX_moins_dX + amplitude * FdX ) / NormeFX,
                )
                #
                self.StoredVariables["Residu"].store( Residu )
                ttsep = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %5i %s\n"%(ip, amplitude, NormeX, NormeFX, Residu, 100. * abs(Residu - 1.), "%")  # noqa: E501
                msgs += __marge + ttsep
            #
            if self._parameters["ResiduFormula"] == "NominalTaylorRMS":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( X0 + dX )
                    self.StoredVariables["CurrentState"].store( X0 - dX )
                    self.StoredVariables["CurrentState"].store( dX )
                #
                FX_plus_dX  = numpy.ravel( Hm( X0 + dX ) ).reshape((-1, 1))
                FX_moins_dX = numpy.ravel( Hm( X0 - dX ) ).reshape((-1, 1))
                FdX         = numpy.ravel( Hm( dX )      ).reshape((-1, 1))
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX_plus_dX )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FX_moins_dX )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( FdX )
                #
                Residu = max(
                    RMS( FX, FX_plus_dX   - amplitude * FdX ) / NormeFX,
                    RMS( FX, FX_moins_dX  + amplitude * FdX ) / NormeFX,
                )
                #
                self.StoredVariables["Residu"].store( Residu )
                ttsep = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %5i %s\n"%(ip, amplitude, NormeX, NormeFX, Residu, 100. * Residu, "%")  # noqa: E501
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
