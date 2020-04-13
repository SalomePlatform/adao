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
        self.setAttributes(tags=(
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        def RMS(V1, V2):
            import math
            return math.sqrt( ((numpy.ravel(V2) - numpy.ravel(V1))**2).sum() / float(numpy.ravel(V1).size) )
        #
        # Operateurs
        # ----------
        Hm = HO["Direct"].appliedTo
        if self._parameters["ResiduFormula"] in ["Taylor", "NominalTaylor", "NominalTaylorRMS"]:
            Ht = HO["Tangent"].appliedInXTo
        #
        # Construction des perturbations
        # ------------------------------
        Perturbations = [ 10**i for i in range(self._parameters["EpsilonMinimumExponent"],1) ]
        Perturbations.reverse()
        #
        # Calcul du point courant
        # -----------------------
        Xn      = numpy.asmatrix(numpy.ravel( Xb )).T
        FX      = numpy.asmatrix(numpy.ravel( Hm( Xn ) )).T
        NormeX  = numpy.linalg.norm( Xn )
        NormeFX = numpy.linalg.norm( FX )
        if self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( numpy.ravel(Xn) )
        if self._toStore("SimulatedObservationAtCurrentState"):
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX) )
        #
        # Fabrication de la direction de l'increment dX
        # ---------------------------------------------
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
        # Calcul du gradient au point courant X pour l'increment dX
        # ---------------------------------------------------------
        if self._parameters["ResiduFormula"] in ["Taylor", "NominalTaylor", "NominalTaylorRMS"]:
            dX1      = float(self._parameters["AmplitudeOfTangentPerturbation"]) * dX0
            GradFxdX = Ht( (Xn, dX1) )
            GradFxdX = numpy.asmatrix(numpy.ravel( GradFxdX )).T
            GradFxdX = float(1./self._parameters["AmplitudeOfTangentPerturbation"]) * GradFxdX
        #
        # Entete des resultats
        # --------------------
        __marge =  12*u" "
        __precision = u"""
            Remarque : les nombres inferieurs a %.0e (environ) representent un zero
                       a la precision machine.\n"""%mpr
        if self._parameters["ResiduFormula"] == "CenteredDL":
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)  log10( R )"
            __msgdoc = u"""
            On observe le residu provenant de la difference centree des valeurs de F
            au point nominal et aux points perturbes, normalisee par la valeur au
            point nominal :

                         || F(X+Alpha*dX) + F(X-Alpha*dX) - 2*F(X) ||
              R(Alpha) = --------------------------------------------
                                         || F(X) ||

            S'il reste constamment tres faible par rapport a 1, l'hypothese de linearite
            de F est verifiee.

            Si le residu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
            faible qu'a partir d'un certain ordre d'increment, l'hypothese de linearite
            de F n'est pas verifiee.

            Si le residu decroit et que la decroissance se fait en Alpha**2 selon Alpha,
            cela signifie que le gradient est calculable jusqu'a la precision d'arret
            de la decroissance quadratique.

            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.\n""" + __precision
        if self._parameters["ResiduFormula"] == "Taylor":
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)  log10( R )"
            __msgdoc = u"""
            On observe le residu issu du developpement de Taylor de la fonction F,
            normalisee par la valeur au point nominal :

                         || F(X+Alpha*dX) - F(X) - Alpha * GradientF_X(dX) ||
              R(Alpha) = ----------------------------------------------------
                                         || F(X) ||

            S'il reste constamment tres faible par rapport a 1, l'hypothese de linearite
            de F est verifiee.

            Si le residu varie, ou qu'il est de l'ordre de 1 ou plus, et qu'il n'est
            faible qu'a partir d'un certain ordre d'increment, l'hypothese de linearite
            de F n'est pas verifiee.

            Si le residu decroit et que la decroissance se fait en Alpha**2 selon Alpha,
            cela signifie que le gradient est bien calcule jusqu'a la precision d'arret
            de la decroissance quadratique.

            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.\n""" + __precision
        if self._parameters["ResiduFormula"] == "NominalTaylor":
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)   |R-1| en %"
            __msgdoc = u"""
            On observe le residu obtenu a partir de deux approximations d'ordre 1 de F(X),
            normalisees par la valeur au point nominal :

              R(Alpha) = max(
                || F(X+Alpha*dX) - Alpha * F(dX) || / || F(X) ||,
                || F(X-Alpha*dX) + Alpha * F(dX) || / || F(X) ||,
              )

            S'il reste constamment egal a 1 a moins de 2 ou 3 pourcents pres (c'est-a-dire
            que |R-1| reste egal a 2 ou 3 pourcents), c'est que l'hypothese de linearite
            de F est verifiee.

            S'il est egal a 1 sur une partie seulement du domaine de variation de
            l'increment Alpha, c'est sur cette partie que l'hypothese de linearite de F
            est verifiee.

            On prend dX0 = Normal(0,X) et dX = Alpha*dX0. F est le code de calcul.\n""" + __precision
        if self._parameters["ResiduFormula"] == "NominalTaylorRMS":
            __entete = u"  i   Alpha     ||X||      ||F(X)||   |   R(Alpha)    |R| en %"
            __msgdoc = u"""
            On observe le residu obtenu a partir de deux approximations d'ordre 1 de F(X),
            normalisees par la valeur au point nominal :

              R(Alpha) = max(
                RMS( F(X), F(X+Alpha*dX) - Alpha * F(dX) ) / || F(X) ||,
                RMS( F(X), F(X-Alpha*dX) + Alpha * F(dX) ) / || F(X) ||,
              )

            S'il reste constamment egal a 0 a moins de 1 ou 2 pourcents pres, c'est
            que l'hypothese de linearite de F est verifiee.

            S'il est egal a 0 sur une partie seulement du domaine de variation de
            l'increment Alpha, c'est sur cette partie que l'hypothese de linearite de F
            est verifiee.

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
        for i,amplitude in enumerate(Perturbations):
            dX      = amplitude * dX0
            #
            if self._parameters["ResiduFormula"] == "CenteredDL":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( numpy.ravel(Xn + dX) )
                    self.StoredVariables["CurrentState"].store( numpy.ravel(Xn - dX) )
                #
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                FX_moins_dX = numpy.asmatrix(numpy.ravel( Hm( Xn - dX ) )).T
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_plus_dX) )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_moins_dX) )
                #
                Residu = numpy.linalg.norm( FX_plus_dX + FX_moins_dX - 2 * FX ) / NormeFX
                #
                self.StoredVariables["Residu"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %4.0f"%(i,amplitude,NormeX,NormeFX,Residu,math.log10(max(1.e-99,Residu)))
                msgs += "\n" + __marge + msg
            #
            if self._parameters["ResiduFormula"] == "Taylor":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( numpy.ravel(Xn + dX) )
                #
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_plus_dX) )
                #
                Residu = numpy.linalg.norm( FX_plus_dX - FX - amplitude * GradFxdX ) / NormeFX
                #
                self.StoredVariables["Residu"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %4.0f"%(i,amplitude,NormeX,NormeFX,Residu,math.log10(max(1.e-99,Residu)))
                msgs += "\n" + __marge + msg
            #
            if self._parameters["ResiduFormula"] == "NominalTaylor":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( numpy.ravel(Xn + dX) )
                    self.StoredVariables["CurrentState"].store( numpy.ravel(Xn - dX) )
                    self.StoredVariables["CurrentState"].store( numpy.ravel(dX) )
                #
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                FX_moins_dX = numpy.asmatrix(numpy.ravel( Hm( Xn - dX ) )).T
                FdX         = numpy.asmatrix(numpy.ravel( Hm( dX ) )).T
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_plus_dX) )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_moins_dX) )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FdX) )
                #
                Residu = max(
                    numpy.linalg.norm( FX_plus_dX  - amplitude * FdX ) / NormeFX,
                    numpy.linalg.norm( FX_moins_dX + amplitude * FdX ) / NormeFX,
                    )
                #
                self.StoredVariables["Residu"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %5i %s"%(i,amplitude,NormeX,NormeFX,Residu,100.*abs(Residu-1.),"%")
                msgs += "\n" + __marge + msg
            #
            if self._parameters["ResiduFormula"] == "NominalTaylorRMS":
                if self._toStore("CurrentState"):
                    self.StoredVariables["CurrentState"].store( numpy.ravel(Xn + dX) )
                    self.StoredVariables["CurrentState"].store( numpy.ravel(Xn - dX) )
                    self.StoredVariables["CurrentState"].store( numpy.ravel(dX) )
                #
                FX_plus_dX  = numpy.asmatrix(numpy.ravel( Hm( Xn + dX ) )).T
                FX_moins_dX = numpy.asmatrix(numpy.ravel( Hm( Xn - dX ) )).T
                FdX         = numpy.asmatrix(numpy.ravel( Hm( dX ) )).T
                #
                if self._toStore("SimulatedObservationAtCurrentState"):
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_plus_dX) )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FX_moins_dX) )
                    self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(FdX) )
                #
                Residu = max(
                    RMS( FX, FX_plus_dX   - amplitude * FdX ) / NormeFX,
                    RMS( FX, FX_moins_dX  + amplitude * FdX ) / NormeFX,
                    )
                #
                self.StoredVariables["Residu"].store( Residu )
                msg = "  %2i  %5.0e   %9.3e   %9.3e   |   %9.3e   %5i %s"%(i,amplitude,NormeX,NormeFX,Residu,100.*Residu,"%")
                msgs += "\n" + __marge + msg
        #
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n"
        #
        # Sorties eventuelles
        # -------------------
        print("\nResults of linearity check by \"%s\" formula:"%self._parameters["ResiduFormula"])
        print(msgs)
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
