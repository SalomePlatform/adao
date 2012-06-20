#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2012 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

import logging
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "GRADIENTTEST")
        self.defineRequiredParameter(
            name     = "ResiduFormula",
            default  = "Taylor",
            typecast = str,
            message  = "Formule de résidu utilisée",
            listval  = ["Norm", "Taylor"],
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
            default  = "",
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

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Opérateur d'observation
        # -----------------------
        Hm = H["Direct"].appliedTo
        if self._parameters["ResiduFormula"] is "Taylor":
            Ht = H["Tangent"].appliedInXTo
        #
        # Construction des perturbations
        # ------------------------------
        Perturbations = [ 10**i for i in xrange(self._parameters["EpsilonMinimumExponent"],1) ]
        Perturbations.reverse()
        #
        # Calcul du point courant
        # -----------------------
        X       = numpy.asmatrix(Xb).flatten().T
        FX      = numpy.asmatrix( Hm( X ) ).flatten().T
        FX      = numpy.asmatrix(FX).flatten().T
        NormeX  = numpy.linalg.norm( X )
        NormeFX = numpy.linalg.norm( FX )
        #
        # Fabrication de la direction de  l'incrément dX
        # ----------------------------------------------
        if len(self._parameters["InitialDirection"]) == 0:
            dX0 = []
            for v in X.A1:
                if abs(v) > 1.e-8:
                    dX0.append( numpy.random.normal(0.,abs(v)) )
                else:
                    dX0.append( numpy.random.normal(0.,X.mean()) )
        else:
            dX0 = numpy.asmatrix(self._parameters["InitialDirection"]).flatten()
        #
        dX0 = float(self._parameters["AmplitudeOfInitialDirection"]) * numpy.matrix( dX0 ).T
        #
        # Calcul du gradient au point courant X pour l'incrément dX
        # ---------------------------------------------------------
        if self._parameters["ResiduFormula"] is "Taylor":
            GradFxdX = Ht( (X, dX0) )
            GradFxdX = numpy.asmatrix(GradFxdX).flatten().T
        #
        # Entete des resultats
        # --------------------
        if self._parameters["ResiduFormula"] is "Taylor":
            __doc__ = """
            On observe le residu issu du développement de Taylor de la fonction H :

              R(Alpha) = || H(x+Alpha*dx) - H(x) - Alpha * TangentH_x(dx) ||

            Ce résidu doit décroître en Alpha**2 selon Alpha.
            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. H est le code de calcul.
            """
        elif self._parameters["ResiduFormula"] is "Norm":
            __doc__ = """
            On observe le residu, qui est une approximation du gradient :

                          || H(X+Alpha*dX) - H(X) ||
              R(Alpha) =  ---------------------------
                                    Alpha

            qui doit rester constant jusqu'à ce qu'on atteigne la précision du calcul.
            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. H est le code de calcul.
            """
        else:
            __doc__ = ""
        #
        msgs  = "         ====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
        msgs += "             " + self._parameters["ResultTitle"] + "\n"
        msgs += "         ====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
        msgs += __doc__
        #
        msg = "  i   Alpha       ||X||    ||H(X)||  ||H(X+dX)||    ||dX||  ||H(X+dX)-H(X)||   ||H(X+dX)-H(X)||/||dX||      R(Alpha)  "
        nbtirets = len(msg)
        msgs += "\n" + "-"*nbtirets
        msgs += "\n" + msg
        msgs += "\n" + "-"*nbtirets
        #
        Normalisation= -1
        NormesdX     = []
        NormesFXdX   = []
        NormesdFX    = []
        NormesdFXsdX = []
        NormesdFXsAm = []
        NormesdFXGdX = []
        #
        # Boucle sur les perturbations
        # ----------------------------
        for i,amplitude in enumerate(Perturbations):
            logging.debug("%s Etape de calcul numéro %i, avec la perturbation %8.3e"%(self._name, i, amplitude))
            #
            dX      = amplitude * dX0
            #
            FX_plus_dX = Hm( X + dX )
            FX_plus_dX = numpy.asmatrix(FX_plus_dX).flatten().T
            #
            NormedX     = numpy.linalg.norm( dX )
            NormeFXdX   = numpy.linalg.norm( FX_plus_dX )
            NormedFX    = numpy.linalg.norm( FX_plus_dX - FX )
            NormedFXsdX = NormedFX/NormedX
            # Residu Taylor
            if self._parameters["ResiduFormula"] is "Taylor":
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
            if self._parameters["ResiduFormula"] is "Taylor":
                NormesdFXGdX.append( NormedFXGdX )
            NormesdFXsdX.append( NormedFXsdX )
            NormesdFXsAm.append( NormedFXsAm )
            #
            if self._parameters["ResiduFormula"] is "Taylor":
                Residu = NormedFXGdX
            elif self._parameters["ResiduFormula"] is "Norm":
                Residu = NormedFXsAm
            if Normalisation < 0 : Normalisation = Residu
            #
            msg = "  %2i  %5.0e   %8.3e   %8.3e   %8.3e   %8.3e   %8.3e      |      %8.3e          |   %8.3e"%(i,amplitude,NormeX,NormeFX,NormeFXdX,NormedX,NormedFX,NormedFXsdX,Residu)
            msgs += "\n" + msg
            #
            self.StoredVariables["CostFunctionJ"].store( Residu )
        msgs += "\n" + "-"*nbtirets
        msgs += "\n"
        #
        # Sorties eventuelles
        # -------------------
        logging.debug("%s Résultats :\n%s"%(self._name, msgs))
        print
        print "Results of gradient stability check:"
        print msgs
        #
        if self._parameters["PlotAndSave"]:
            f = open(str(self._parameters["ResultFile"])+".txt",'a')
            f.write(msgs)
            f.close()
            #
            Residus = self.StoredVariables["CostFunctionJ"].valueserie()[-len(Perturbations):]
            if self._parameters["ResiduFormula"] is "Taylor":
                PerturbationsCarre = [ 10**(2*i) for i in xrange(-len(NormesdFXGdX)+1,1) ]
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
            elif self._parameters["ResiduFormula"] is "Norm":
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
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("Mo")))
        logging.debug("%s Terminé"%self._name)
        #
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
        recalYRef = True, # Decalage du point 0 de YRef à Y[0]
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
    # __g('set xrange [] reverse')
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
    if filename is not "":
        __g.hardcopy( filename, color=1)
    if pause:
        raw_input('Please press return to continue...\n')

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
