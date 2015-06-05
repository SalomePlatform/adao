#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2015 EDF R&D
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
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

import logging
from daCore import BasicObjects
import numpy, math

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "TANGENTTEST")
        self.defineRequiredParameter(
            name     = "ResiduFormula",
            default  = "Taylor",
            typecast = str,
            message  = "Formule de résidu utilisée",
            listval  = ["Taylor"],
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
            name     = "ResultTitle",
            default  = "",
            typecast = str,
            message  = "Titre du tableau et de la figure",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        # Opérateurs
        # ----------
        Hm = HO["Direct"].appliedTo
        Ht = HO["Tangent"].appliedInXTo
        #
        # Construction des perturbations
        # ------------------------------
        Perturbations = [ 10**i for i in xrange(self._parameters["EpsilonMinimumExponent"],1) ]
        Perturbations.reverse()
        #
        # Calcul du point courant
        # -----------------------
        Xn      = numpy.asmatrix(numpy.ravel( Xb )).T
        FX      = numpy.asmatrix(numpy.ravel( Hm( Xn ) )).T
        NormeX  = numpy.linalg.norm( Xn )
        NormeFX = numpy.linalg.norm( FX )
        #
        # Fabrication de la direction de  l'incrément dX
        # ----------------------------------------------
        if len(self._parameters["InitialDirection"]) == 0:
            dX0 = []
            for v in Xn.A1:
                if abs(v) > 1.e-8:
                    dX0.append( numpy.random.normal(0.,abs(v)) )
                else:
                    dX0.append( numpy.random.normal(0.,Xn.mean()) )
        else:
            dX0 = numpy.ravel( self._parameters["InitialDirection"] )
        #
        dX0 = float(self._parameters["AmplitudeOfInitialDirection"]) * numpy.matrix( dX0 ).T
        #
        # Calcul du gradient au point courant X pour l'incrément dX
        # qui est le tangent en X multiplié par dX
        # ---------------------------------------------------------
        dX1      = float(self._parameters["AmplitudeOfTangentPerturbation"]) * dX0
        GradFxdX = Ht( (Xn, dX1) )
        GradFxdX = numpy.asmatrix(numpy.ravel( GradFxdX )).T
        GradFxdX = float(1./self._parameters["AmplitudeOfTangentPerturbation"]) * GradFxdX
        NormeGX  = numpy.linalg.norm( GradFxdX )
        #
        # Entete des resultats
        # --------------------
        __marge =  12*" "
        if self._parameters["ResiduFormula"] == "Taylor":
            __entete = "  i   Alpha     ||X||      ||F(X)||   |     R(Alpha)    |R-1|/Alpha  "
            __msgdoc = """
            On observe le résidu provenant du rapport d'incréments utilisant le
            linéaire tangent :

                          || F(X+Alpha*dX) - F(X) ||
              R(Alpha) = -----------------------------
                         || Alpha * TangentF_X * dX ||

            qui doit rester stable en 1+O(Alpha) jusqu'à ce que l'on atteigne la
            précision du calcul.
            
            Lorsque |R-1|/Alpha est inférieur ou égal à une valeur stable
            lorsque Alpha varie, le tangent est valide, jusqu'à ce que l'on
            atteigne la précision du calcul.
            
            Si |R-1|/Alpha est très faible, le code F est vraisemblablement
            linéaire ou quasi-linéaire, et le tangent est valide jusqu'à ce que
            l'on atteigne la précision du calcul.

            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.
            """
        #
        if len(self._parameters["ResultTitle"]) > 0:
            msgs  = "\n"
            msgs += __marge + "====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
            msgs += __marge + "    " + self._parameters["ResultTitle"] + "\n"
            msgs += __marge + "====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
        else:
            msgs  = ""
        msgs += __msgdoc
        #
        __nbtirets = len(__entete)
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n" + __marge + __entete
        msgs += "\n" + __marge + "-"*__nbtirets
        #
        # Boucle sur les perturbations
        # ----------------------------
        for i,amplitude in enumerate(Perturbations):
            dX      = amplitude * dX0
            #
            if self._parameters["ResiduFormula"] == "Taylor":
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                #
                Residu = numpy.linalg.norm( FX_plus_dX - FX ) / (amplitude * NormeGX)
                #
                self.StoredVariables["CostFunctionJ"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %11.5e    %5.1e"%(i,amplitude,NormeX,NormeFX,Residu,abs(Residu-1.)/amplitude)
                msgs += "\n" + __marge + msg
        #
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n"
        #
        # Sorties eventuelles
        # -------------------
        print
        print "Results of tangent check by \"%s\" formula:"%self._parameters["ResiduFormula"]
        print msgs
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
