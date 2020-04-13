# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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

import sys, logging
from daCore import BasicObjects, PlatformInfo
import numpy, math
mpr = PlatformInfo.PlatformInfo().MachinePrecision()
if sys.version_info.major > 2:
    unicode = str

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
            name     = "PlotAndSave",
            default  = False,
            typecast = bool,
            message  = "Trace et sauve les résultats",
            )
        self.defineRequiredParameter(
            name     = "ResultFile",
            default  = self._name+"_result_file",
            typecast = str,
            message  = "Nom de base (hors extension) des fichiers de sauvegarde des résultats",
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
        self.setAttributes(tags=(
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        Hm = HO["Direct"].appliedTo
        if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
            Ht = HO["Tangent"].appliedInXTo
        #
        # ----------
        Perturbations = [ 10**i for i in range(self._parameters["EpsilonMinimumExponent"],1) ]
        Perturbations.reverse()
        #
        X       = numpy.asmatrix(numpy.ravel(    Xb   )).T
        FX      = numpy.asmatrix(numpy.ravel( Hm( X ) )).T
        NormeX  = numpy.linalg.norm( X )
        NormeFX = numpy.linalg.norm( FX )
        if self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( numpy.ravel(Xn) )
        if self._toStore("SimulatedObservationAtCurrentState"):
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX) )
        #
        if len(self._parameters["InitialDirection"]) == 0:
            dX0 = []
            for v in X.A1:
                if abs(v) > 1.e-8:
                    dX0.append( numpy.random.normal(0.,abs(v)) )
                else:
                    dX0.append( numpy.random.normal(0.,X.mean()) )
        else:
            dX0 = numpy.ravel( self._parameters["InitialDirection"] )
        #
        dX0 = float(self._parameters["AmplitudeOfInitialDirection"]) * numpy.matrix( dX0 ).T
        #
        if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
            dX1      = float(self._parameters["AmplitudeOfTangentPerturbation"]) * dX0
            GradFxdX = Ht( (X, dX1) )
            GradFxdX = numpy.asmatrix(numpy.ravel( GradFxdX )).T
            GradFxdX = float(1./self._parameters["AmplitudeOfTangentPerturbation"]) * GradFxdX
        #
        # Entete des resultats
        # --------------------
        __marge =  12*u" "
        __precision = u"""
            Remarque : les nombres inferieurs a %.0e (environ) representent un zero
                       a la precision machine.\n"""%mpr
        if self._parameters["ResiduFormula"] == "Taylor":
            __entete = u"  i   Alpha       ||X||    ||F(X)||  ||F(X+dX)||    ||dX||  ||F(X+dX)-F(X)||   ||F(X+dX)-F(X)||/||dX||      R(Alpha)   log( R )"
            __msgdoc = u"""
            On observe le residu issu du developpement de Taylor de la fonction F,
            normalise par la valeur au point nominal :

                         || F(X+Alpha*dX) - F(X) - Alpha * GradientF_X(dX) ||
              R(Alpha) = ----------------------------------------------------
                                         || F(X) ||

            Si le residu decroit et que la decroissance se fait en Alpha**2 selon Alpha,
            cela signifie que le gradient est bien calcule jusqu'a la precision d'arret
            de la decroissance quadratique, et que F n'est pas lineaire.

            Si le residu decroit et que la decroissance se fait en Alpha selon Alpha,
            jusqu'a un certain seuil apres lequel le residu est faible et constant, cela
            signifie que F est lineaire et que le residu decroit a partir de l'erreur
            faite dans le calcul du terme GradientF_X.

            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.\n""" + __precision
        if self._parameters["ResiduFormula"] == "TaylorOnNorm":
            __entete = u"  i   Alpha       ||X||    ||F(X)||  ||F(X+dX)||    ||dX||  ||F(X+dX)-F(X)||   ||F(X+dX)-F(X)||/||dX||      R(Alpha)   log( R )"
            __msgdoc = u"""
            On observe le residu issu du developpement de Taylor de la fonction F,
            rapporte au parametre Alpha au carre :

                         || F(X+Alpha*dX) - F(X) - Alpha * GradientF_X(dX) ||
              R(Alpha) = ----------------------------------------------------
                                            Alpha**2

            C'est un residu essentiellement similaire au critere classique de Taylor,
            mais son comportement peut differer selon les proprietes numeriques des
            calculs de ses differents termes.

            Si le residu est constant jusqu'a un certain seuil et croissant ensuite,
            cela signifie que le gradient est bien calcule jusqu'a cette precision
            d'arret, et que F n'est pas lineaire.

            Si le residu est systematiquement croissant en partant d'une valeur faible
            par rapport a ||F(X)||, cela signifie que F est (quasi-)lineaire et que le
            calcul du gradient est correct jusqu'au moment ou le residu est de l'ordre de
            grandeur de ||F(X)||.

            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.\n""" + __precision
        if self._parameters["ResiduFormula"] == "Norm":
            __entete = u"  i   Alpha       ||X||    ||F(X)||  ||F(X+dX)||    ||dX||  ||F(X+dX)-F(X)||   ||F(X+dX)-F(X)||/||dX||      R(Alpha)   log( R )"
            __msgdoc = u"""
            On observe le residu, qui est base sur une approximation du gradient :

                          || F(X+Alpha*dX) - F(X) ||
              R(Alpha) =  ---------------------------
                                    Alpha

            qui doit rester constant jusqu'a ce que l'on atteigne la precision du calcul.

            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.\n""" + __precision
        #
        if len(self._parameters["ResultTitle"]) > 0:
            __rt = unicode(self._parameters["ResultTitle"])
            msgs  = u"\n"
            msgs += __marge + "====" + "="*len(__rt) + "====\n"
            msgs += __marge + "    " + __rt + "\n"
            msgs += __marge + "====" + "="*len(__rt) + "====\n"
        else:
            msgs  = u""
        msgs += __msgdoc
        #
        __nbtirets = len(__entete) + 2
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n" + __marge + __entete
        msgs += "\n" + __marge + "-"*__nbtirets
        #
        # Boucle sur les perturbations
        # ----------------------------
        NormesdX     = []
        NormesFXdX   = []
        NormesdFX    = []
        NormesdFXsdX = []
        NormesdFXsAm = []
        NormesdFXGdX = []
        #
        for i,amplitude in enumerate(Perturbations):
            dX      = amplitude * dX0
            #
            FX_plus_dX = Hm( X + dX )
            FX_plus_dX = numpy.asmatrix(numpy.ravel( FX_plus_dX )).T
            #
            if self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( numpy.ravel(X + dX) )
            if self._toStore("SimulatedObservationAtCurrentState"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_plus_dX) )
            #
            NormedX     = numpy.linalg.norm( dX )
            NormeFXdX   = numpy.linalg.norm( FX_plus_dX )
            NormedFX    = numpy.linalg.norm( FX_plus_dX - FX )
            NormedFXsdX = NormedFX/NormedX
            # Residu Taylor
            if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
                NormedFXGdX = numpy.linalg.norm( FX_plus_dX - FX - amplitude * GradFxdX )
            # Residu Norm
            NormedFXsAm = NormedFX/amplitude
            #
            # if numpy.abs(NormedFX) < 1.e-20:
            #     break
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
                Residu = NormedFXGdX / (amplitude*amplitude)
            elif self._parameters["ResiduFormula"] == "Norm":
                Residu = NormedFXsAm
            #
            msg = "  %2i  %5.0e   %9.3e   %9.3e   %9.3e   %9.3e   %9.3e      |      %9.3e          |   %9.3e   %4.0f"%(i,amplitude,NormeX,NormeFX,NormeFXdX,NormedX,NormedFX,NormedFXsdX,Residu,math.log10(max(1.e-99,Residu)))
            msgs += "\n" + __marge + msg
            #
            self.StoredVariables["Residu"].store( Residu )
        #
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n"
        #
        # ----------
        print("\nResults of gradient check by \"%s\" formula:"%self._parameters["ResiduFormula"])
        print(msgs)
        #
        if self._parameters["PlotAndSave"]:
            f = open(str(self._parameters["ResultFile"])+".txt",'a')
            f.write(msgs)
            f.close()
            #
            Residus = self.StoredVariables["Residu"][-len(Perturbations):]
            if self._parameters["ResiduFormula"] in ["Taylor", "TaylorOnNorm"]:
                PerturbationsCarre = [ 10**(2*i) for i in range(-len(NormesdFXGdX)+1,1) ]
                PerturbationsCarre.reverse()
                dessiner(
                    Perturbations,
                    Residus,
                    titre    = self._parameters["ResultTitle"],
                    label    = self._parameters["ResultLabel"],
                    logX     = True,
                    logY     = True,
                    filename = str(self._parameters["ResultFile"])+".ps",
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
                    filename = str(self._parameters["ResultFile"])+".ps",
                    )
        #
        self._post_run(HO)
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
        YRef      = None, # Vecteur de reference a comparer a Y
        recalYRef = True, # Decalage du point 0 de YRef a Y[0]
        normdY0   = 0.,   # Norme de DeltaY[0]
        ):
    import Gnuplot
    __gnuplot = Gnuplot
    __g = __gnuplot.Gnuplot(persist=1) # persist=1
    # __g('set terminal '+__gnuplot.GnuplotOpts.default_term)
    __g('set style data lines')
    __g('set grid')
    __g('set autoscale')
    __g('set title  "'+titre+'"')
    # __g('set range [] reverse')
    # __g('set yrange [0:2]')
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
    print('\n AUTODIAGNOSTIC\n')
