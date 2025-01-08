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
        BasicObjects.Algorithm.__init__(self, "GRADIENTTEST")
        self.defineRequiredParameter(
            name     = "ResiduFormula",
            default  = "Taylor",
            typecast = str,
            message  = "Formule de résidu utilisée",
            listval  = ["Norm", "TaylorOnNorm", "Taylor"],
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
            name     = "ResultLabel",
            default  = "",
            typecast = str,
            message  = "Label de la courbe tracée dans la figure",
        )
        self.defineRequiredParameter(
            name     = "ResultFile",
            default  = self._name + "_result_file",
            typecast = str,
            message  = "Nom de base (hors extension) des fichiers de sauvegarde des résultats",
        )
        self.defineRequiredParameter(
            name     = "PlotAndSave",
            default  = False,
            typecast = bool,
            message  = "Trace et sauve les résultats",
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
        #
        Hm = HO["Direct"].appliedTo
        if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
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
        msgs += (__marge + "This test allows to analyze the numerical stability of the gradient of some\n")
        msgs += (__marge + "given simulation operator F, applied to one single vector argument x.\n")
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
        if self._parameters["ResiduFormula"] == "Taylor":
            msgs += (__marge + "               || F(X+Alpha*dX) - F(X) - Alpha * GradientF_X(dX) ||\n")
            msgs += (__marge + "    R(Alpha) = ----------------------------------------------------\n")
            msgs += (__marge + "                               || F(X) ||\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue decreases and if the decay is in Alpha**2 according to\n")
            msgs += (__marge + "Alpha, it means that the gradient is well calculated up to the stopping\n")
            msgs += (__marge + "precision of the quadratic decay, and that F is not linear.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue decreases and if the decay is done in Alpha according\n")
            msgs += (__marge + "to Alpha, until a certain threshold after which the residue is small\n")
            msgs += (__marge + "and constant, it means that F is linear and that the residue decreases\n")
            msgs += (__marge + "from the error made in the calculation of the GradientF_X term.\n")
            #
            __entete = u"  i   Alpha       ||X||    ||F(X)||  ||F(X+dX)||    ||dX||  ||F(X+dX)-F(X)||   ||F(X+dX)-F(X)||/||dX||      R(Alpha)   log( R )"  # noqa: E501
            #
        if self._parameters["ResiduFormula"] == "TaylorOnNorm":
            msgs += (__marge + "               || F(X+Alpha*dX) - F(X) - Alpha * GradientF_X(dX) ||\n")
            msgs += (__marge + "    R(Alpha) = ----------------------------------------------------\n")
            msgs += (__marge + "                                  Alpha**2\n")
            msgs += ("\n")
            msgs += (__marge + "It is a residue essentially similar to the classical Taylor criterion,\n")
            msgs += (__marge + "but its behavior may differ depending on the numerical properties of\n")
            msgs += (__marge + "the calculations of its various terms.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue is constant up to a certain threshold and increasing\n")
            msgs += (__marge + "afterwards, it means that the gradient is well computed up to this\n")
            msgs += (__marge + "stopping precision, and that F is not linear.\n")
            msgs += ("\n")
            msgs += (__marge + "If the residue is systematically increasing starting from a small\n")
            msgs += (__marge + "value compared to ||F(X)||, it means that F is (quasi-)linear and that\n")
            msgs += (__marge + "the calculation of the gradient is correct until the residue is of the\n")
            msgs += (__marge + "order of magnitude of ||F(X)||.\n")
            #
            __entete = u"  i   Alpha       ||X||    ||F(X)||  ||F(X+dX)||    ||dX||  ||F(X+dX)-F(X)||   ||F(X+dX)-F(X)||/||dX||      R(Alpha)   log( R )"  # noqa: E501
            #
        if self._parameters["ResiduFormula"] == "Norm":
            msgs += (__marge + "               || F(X+Alpha*dX) - F(X) ||\n")
            msgs += (__marge + "    R(Alpha) = --------------------------\n")
            msgs += (__marge + "                         Alpha\n")
            msgs += ("\n")
            msgs += (__marge + "which must remain constant until the accuracy of the calculation is\n")
            msgs += (__marge + "reached.\n")
            #
            __entete = u"  i   Alpha       ||X||    ||F(X)||  ||F(X+dX)||    ||dX||  ||F(X+dX)-F(X)||   ||F(X+dX)-F(X)||/||dX||      R(Alpha)   log( R )"  # noqa: E501
            #
        msgs += ("\n")
        msgs += (__marge + "We take dX0 = Normal(0,X) and dX = Alpha*dX0. F is the calculation code.\n")
        if "DifferentialIncrement" in HO and HO["DifferentialIncrement"] is not None:
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
        if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
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
        NormesdX     = []
        NormesFXdX   = []
        NormesdFX    = []
        NormesdFXsdX = []
        NormesdFXsAm = []
        NormesdFXGdX = []
        #
        for ip, amplitude in enumerate(Perturbations):
            dX      = amplitude * dX0.reshape((-1, 1))
            #
            X_plus_dX = X0 + dX
            FX_plus_dX = Hm( X_plus_dX )
            FX_plus_dX = numpy.ravel( FX_plus_dX ).reshape((-1, 1))
            #
            if self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( X_plus_dX )
            if self._toStore("SimulatedObservationAtCurrentState"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_plus_dX) )
            #
            NormedX     = numpy.linalg.norm( dX )
            NormeFXdX   = numpy.linalg.norm( FX_plus_dX )
            NormedFX    = numpy.linalg.norm( FX_plus_dX - FX )
            NormedFXsdX = NormedFX / NormedX
            # Residu Taylor
            if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
                NormedFXGdX = numpy.linalg.norm( FX_plus_dX - FX - amplitude * GradFxdX )
            # Residu Norm
            NormedFXsAm = NormedFX / amplitude
            #
            # if numpy.abs(NormedFX) < 1.e-20:
            #     break
            #
            NormesdX.append(     NormedX     )
            NormesFXdX.append(   NormeFXdX   )
            NormesdFX.append(    NormedFX    )
            if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
                NormesdFXGdX.append( NormedFXGdX )
            NormesdFXsdX.append( NormedFXsdX )
            NormesdFXsAm.append( NormedFXsAm )
            #
            if self._parameters["ResiduFormula"] == "Taylor":
                Residu = NormedFXGdX / NormeFX
            elif self._parameters["ResiduFormula"] == "TaylorOnNorm":
                Residu = NormedFXGdX / (amplitude * amplitude)
            elif self._parameters["ResiduFormula"] == "Norm":
                Residu = NormedFXsAm
            #
            self.StoredVariables["Residu"].store( Residu )
            ttsep = "  %2i  %5.0e   %9.3e   %9.3e   %9.3e   %9.3e   %9.3e      |      %9.3e          |   %9.3e   %4.0f\n"%(ip, amplitude, NormeX, NormeFX, NormeFXdX, NormedX, NormedFX, NormedFXsdX, Residu, math.log10(max(1.e-99, Residu)))  # noqa: E501
            msgs += __marge + ttsep
        #
        msgs += (__marge + "-" * __nbtirets + "\n\n")
        msgs += (__marge + "End of the \"%s\" verification by the \"%s\" formula.\n\n"%(self._name, self._parameters["ResiduFormula"]))  # noqa: E501
        msgs += (__marge + "%s\n"%("-" * 75,))
        print(msgs)  # 2
        #
        if self._parameters["PlotAndSave"]:
            f = open(str(self._parameters["ResultFile"]) + ".txt", 'a')
            f.write(msgs)
            f.close()
            #
            Residus = self.StoredVariables["Residu"][-len(Perturbations):]
            if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
                PerturbationsCarre = [ 10**(2 * i) for i in range(-len(NormesdFXGdX) + 1, 1) ]
                PerturbationsCarre.reverse()
                dessiner(
                    Perturbations,
                    Residus,
                    titre    = self._parameters["ResultTitle"],
                    label    = self._parameters["ResultLabel"],
                    logX     = True,
                    logY     = True,
                    filename = str(self._parameters["ResultFile"]) + ".ps",
                    YRef     = PerturbationsCarre,
                    normdY0  = numpy.log10( NormesdFX[0] ),
                )
            elif self._parameters["ResiduFormula"] == "Norm":
                dessiner(
                    Perturbations,
                    Residus,
                    titre    = self._parameters["ResultTitle"],
                    label    = self._parameters["ResultLabel"],
                    logX     = True,
                    logY     = True,
                    filename = str(self._parameters["ResultFile"]) + ".ps",
                )
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================

def dessiner(
        X,
        Y,
        titre     = "",
        label     = "",
        logX      = False,
        logY      = False,
        filename  = "",
        pause     = False,
        YRef      = None,  # Vecteur de reference a comparer a Y
        recalYRef = True,  # Decalage du point 0 de YRef a Y[0]
        normdY0   = 0.):   # Norme de DeltaY[0]
    import Gnuplot
    __gnuplot = Gnuplot
    __g = __gnuplot.Gnuplot(persist=1)  # persist=1
    # __g('set terminal '+__gnuplot.GnuplotOpts.default_term)
    __g('set style data lines')
    __g('set grid')
    __g('set autoscale')
    __g('set title  "' + titre + '"')
    # __g('set range [] reverse')
    # __g('set yrange [0:2]')
    #
    if logX:
        steps = numpy.log10( X )
        __g('set xlabel "Facteur multiplicatif de dX, en echelle log10"')
    else:
        steps = X
        __g('set xlabel "Facteur multiplicatif de dX"')
    #
    if logY:
        values = numpy.log10( Y )
        __g('set ylabel "Amplitude du residu, en echelle log10"')
    else:
        values = Y
        __g('set ylabel "Amplitude du residu"')
    #
    __g.plot( __gnuplot.Data( steps, values, title=label, with_='lines lw 3' ) )
    if YRef is not None:
        if logY:
            valuesRef = numpy.log10( YRef )
        else:
            valuesRef = YRef
        if recalYRef and not numpy.all(values < -8):
            valuesRef = valuesRef + values[0]
        elif recalYRef and numpy.all(values < -8):
            valuesRef = valuesRef + normdY0
        else:
            pass
        __g.replot( __gnuplot.Data( steps, valuesRef, title="Reference", with_='lines lw 1' ) )
    #
    if filename != "":
        __g.hardcopy( filename, color=1)
    if pause:
        eval(input('Please press return to continue...\n'))

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
