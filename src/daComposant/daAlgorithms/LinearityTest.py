#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2013 EDF R&D
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
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

import numpy
import math

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "FUNCTIONTEST")
        self.defineRequiredParameter(
            name     = "ResiduFormula",
            default  = "CenteredDL",
            typecast = str,
            message  = "Formule de r�sidu utilis�e",
            listval  = ["CenteredDL", "Taylor", "NominalTaylor", "NominalTaylorRMS"],
            )
        self.defineRequiredParameter(
            name     = "EpsilonMinimumExponent",
            default  = -8,
            typecast = int,
            message  = "Exposant minimal en puissance de 10 pour le multiplicateur d'incr�ment",
            minval   = -20,
            maxval   = 0,
            )
        self.defineRequiredParameter(
            name     = "InitialDirection",
            default  = [],
            typecast = list,
            message  = "Direction initiale de la d�riv�e directionnelle autour du point nominal",
            )
        self.defineRequiredParameter(
            name     = "AmplitudeOfInitialDirection",
            default  = 1.,
            typecast = float,
            message  = "Amplitude de la direction initiale de la d�riv�e directionnelle autour du point nominal",
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fix�e pour le g�n�rateur al�atoire",
            )
        self.defineRequiredParameter(
            name     = "ResultTitle",
            default  = "",
            typecast = str,
            message  = "Titre du tableau et de la figure",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        # Param�tres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        def RMS(V1, V2):
            import math
            return math.sqrt( ((numpy.ravel(V2) - numpy.ravel(V1))**2).sum() / float(numpy.ravel(V1).size) )
        #
        # Op�rateurs
        # ----------
        Hm = HO["Direct"].appliedTo
        if self._parameters["ResiduFormula"] in ["Taylor", "NominalTaylor", "NotNominalTaylor", "NominalTaylorRMS", "NotNominalTaylorRMS"]:
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
        # Fabrication de la direction de  l'incr�ment dX
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
        # Calcul du gradient au point courant X pour l'incr�ment dX
        # ---------------------------------------------------------
        if self._parameters["ResiduFormula"] in ["Taylor", "NominalTaylor", "NotNominalTaylor", "NominalTaylorRMS", "NotNominalTaylorRMS"]:
            GradFxdX = Ht( (Xn, dX0) )
            GradFxdX = numpy.asmatrix(numpy.ravel( GradFxdX )).T
        #
        # Entete des resultats
        # --------------------
        marge =  12*" "
        if self._parameters["ResiduFormula"] is "CenteredDL":
            entete = "  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)   log( R )  "
            __doc__ = """
            On observe le residu provenant de la diff�rence centr�e des valeurs de F
            au point nominal et aux points perturb�s, normalis�e par la valeur au
            point nominal :
            
                         || F(X+Alpha*dX) + F(X-Alpha*dX) - 2*F(X) ||
              R(Alpha) = --------------------------------------------
                                         || F(X) ||

            S'il reste constamment tr�s faible par rapport � 1, l'hypoth�se de lin�arit�
            de F est v�rifi�e.

            Si le r�sidu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
            faible qu'� partir d'un certain ordre d'incr�ment, l'hypoth�se de lin�arit�
            de F n'est pas v�rifi�e.

            Si le r�sidu d�croit et que la d�croissance se fait en Alpha**2 selon Alpha,
            cela signifie que le gradient est bien calcul� jusqu'� la pr�cision d'arr�t
            de la d�croissance quadratique.
            
            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.
            """
        if self._parameters["ResiduFormula"] is "Taylor":
            entete = "  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)   log( R )  "
            __doc__ = """
            On observe le residu issu du d�veloppement de Taylor de la fonction F,
            normalis�e par la valeur au point nominal :

                         || F(X+Alpha*dX) - F(X) - Alpha * GradientF_X(dX) ||
              R(Alpha) = ----------------------------------------------------
                                         || F(X) ||

            S'il reste constamment tr�s faible par rapport � 1, l'hypoth�se de lin�arit�
            de F est v�rifi�e.

            Si le r�sidu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
            faible qu'� partir d'un certain ordre d'incr�ment, l'hypoth�se de lin�arit�
            de F n'est pas v�rifi�e.

            Si le r�sidu d�croit et que la d�croissance se fait en Alpha**2 selon Alpha,
            cela signifie que le gradient est bien calcul� jusqu'� la pr�cision d'arr�t
            de la d�croissance.
            
            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.
            """
        if self._parameters["ResiduFormula"] is "NominalTaylor":
            entete = "  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)   |R-1| en %  "
            __doc__ = """
            On observe le residu obtenu � partir de deux approximations d'ordre 1 de F(X),
            normalis�es par la valeur au point nominal :

              R(Alpha) = max(
                || F(X+Alpha*dX) - Alpha * F(dX) || / || F(X) ||,
                || F(X-Alpha*dX) + Alpha * F(dX) || / || F(X) ||,
              )

            S'il reste constamment �gal � 1 � moins de 2 ou 3 pourcents pr�s, c'est
            que l'hypoth�se de lin�arit� de F est v�rifi�e.
            
            S'il est �gal � 1 sur une partie seulement du domaine de variation de
            l'incr�ment Alpha, c'est sur cette partie que l'hypoth�se de lin�arit� de F
            est v�rifi�e.
            
            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.
            """
        if self._parameters["ResiduFormula"] is "NominalTaylorRMS":
            entete = "  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)    |R| en %  "
            __doc__ = """
            On observe le residu obtenu � partir de deux approximations d'ordre 1 de F(X),
            normalis�es par la valeur au point nominal :

              R(Alpha) = max(
                RMS( F(X), F(X+Alpha*dX) - Alpha * F(dX) ) / || F(X) ||,
                RMS( F(X), F(X-Alpha*dX) + Alpha * F(dX) ) / || F(X) ||,
              )

            S'il reste constamment �gal � 0 � moins de 1 ou 2 pourcents pr�s, c'est
            que l'hypoth�se de lin�arit� de F est v�rifi�e.
            
            S'il est �gal � 0 sur une partie seulement du domaine de variation de
            l'incr�ment Alpha, c'est sur cette partie que l'hypoth�se de lin�arit� de F
            est v�rifi�e.
            
            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.
            """
        #
        if len(self._parameters["ResultTitle"]) > 0:
            msgs  = marge + "====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
            msgs += marge + "   " + self._parameters["ResultTitle"] + "\n"
            msgs += marge + "====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
        else:
            msgs  = ""
        msgs += __doc__
        #
        nbtirets = len(entete)
        msgs += "\n" + marge + "-"*nbtirets
        msgs += "\n" + marge + entete
        msgs += "\n" + marge + "-"*nbtirets
        #
        # Boucle sur les perturbations
        # ----------------------------
        for i,amplitude in enumerate(Perturbations):
            dX      = amplitude * dX0
            #
            if self._parameters["ResiduFormula"] is "CenteredDL":
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                FX_moins_dX = numpy.asmatrix(numpy.ravel( Hm( Xn - dX ) )).T
                #
                Residu = numpy.linalg.norm( FX_plus_dX + FX_moins_dX - 2 * FX ) / NormeFX
                #
                self.StoredVariables["CostFunctionJ"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %4.0f"%(i,amplitude,NormeX,NormeFX,Residu,math.log10(max(1.e-99,Residu)))
                msgs += "\n" + marge + msg
            #
            if self._parameters["ResiduFormula"] is "Taylor":
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                #
                Residu = numpy.linalg.norm( FX_plus_dX - FX - amplitude * GradFxdX ) / NormeFX
                #
                self.StoredVariables["CostFunctionJ"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %4.0f"%(i,amplitude,NormeX,NormeFX,Residu,math.log10(max(1.e-99,Residu)))
                msgs += "\n" + marge + msg
            #
            if self._parameters["ResiduFormula"] is "NominalTaylor":
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                FX_moins_dX = numpy.asmatrix(numpy.ravel( Hm( Xn - dX ) )).T
                FdX         = numpy.asmatrix(numpy.ravel( Hm( dX ) )).T
                #
                Residu = max(
                    numpy.linalg.norm( FX_plus_dX  - amplitude * FdX ) / NormeFX,
                    numpy.linalg.norm( FX_moins_dX + amplitude * FdX ) / NormeFX,
                    )
                #
                self.StoredVariables["CostFunctionJ"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %5i %s"%(i,amplitude,NormeX,NormeFX,Residu,100*abs(Residu-1),"%")
                msgs += "\n" + marge + msg
            #
            if self._parameters["ResiduFormula"] is "NominalTaylorRMS":
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                FX_moins_dX = numpy.asmatrix(numpy.ravel( Hm( Xn - dX ) )).T
                FdX         = numpy.asmatrix(numpy.ravel( Hm( dX ) )).T
                #
                Residu = max(
                    RMS( FX, FX_plus_dX   - amplitude * FdX ) / NormeFX,
                    RMS( FX, FX_moins_dX  + amplitude * FdX ) / NormeFX,
                    )
                #
                self.StoredVariables["CostFunctionJ"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %5i %s"%(i,amplitude,NormeX,NormeFX,Residu,100*Residu,"%")
                msgs += "\n" + marge + msg
        #
        msgs += "\n" + marge + "-"*nbtirets
        msgs += "\n"
        #
        # Sorties eventuelles
        # -------------------
        print
        print "Results of linearity check by \"%s\" formula:\n"%self._parameters["ResiduFormula"]
        print msgs
        #
        logging.debug("%s Taille m�moire utilis�e de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Termin�"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'