# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2022 EDF R&D
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
from daCore import BasicObjects, NumericObjects, PlatformInfo
mpr = PlatformInfo.PlatformInfo().MachinePrecision()

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
            mandatory= ("Xb", "HO" ),
            optional = ("Y", ),
            )
        self.setAttributes(tags=(
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        Hm = HO["Direct"].appliedTo
        Ht = HO["Tangent"].appliedInXTo
        Ha = HO["Adjoint"].appliedInXTo
        #
        Perturbations = [ 10**i for i in range(self._parameters["EpsilonMinimumExponent"],1) ]
        Perturbations.reverse()
        #
        Xn       = numpy.ravel( Xb ).reshape((-1,1))
        NormeX  = numpy.linalg.norm( Xn )
        if Y is None:
            Yn = numpy.ravel( Hm( Xn ) ).reshape((-1,1))
        else:
            Yn = numpy.ravel( Y ).reshape((-1,1))
        NormeY = numpy.linalg.norm( Yn )
        if self._toStore("CurrentState"):
            self.StoredVariables["CurrentState"].store( Xn )
        if self._toStore("SimulatedObservationAtCurrentState"):
            self.StoredVariables["SimulatedObservationAtCurrentState"].store( Yn )
        #
        dX0 = NumericObjects.SetInitialDirection(
            self._parameters["InitialDirection"],
            self._parameters["AmplitudeOfInitialDirection"],
            Xn,
            )
        #
        # --------------------
        __p = self._parameters["NumberOfPrintedDigits"]
        #
        __marge =  5*u" "
        if len(self._parameters["ResultTitle"]) > 0:
            __rt = str(self._parameters["ResultTitle"])
            msgs  = ("\n")
            msgs += (__marge + "====" + "="*len(__rt) + "====\n")
            msgs += (__marge + "    " + __rt + "\n")
            msgs += (__marge + "====" + "="*len(__rt) + "====\n")
        else:
            msgs  = ("\n")
            msgs += ("     %s\n"%self._name)
            msgs += ("     %s\n"%("="*len(self._name),))
        #
        msgs += ("\n")
        msgs += ("     This test allows to analyze the quality of an adjoint operator associated\n")
        msgs += ("     to some given direct operator. If the adjoint operator is approximated and\n")
        msgs += ("     not given, the test measures the quality of the automatic approximation.\n")
        #
        if self._parameters["ResiduFormula"] == "ScalarProduct":
            msgs += ("\n")
            msgs += ("     Using the \"%s\" formula, one observes the residue R which is the\n"%self._parameters["ResiduFormula"])
            msgs += ("     difference of two scalar products:\n")
            msgs += ("\n")
            msgs += ("         R(Alpha) = | < TangentF_X(dX) , Y > - < dX , AdjointF_X(Y) > |\n")
            msgs += ("\n")
            msgs += ("     which must remain constantly equal to zero to the accuracy of the calculation.\n")
            msgs += ("     One takes dX0 = Normal(0,X) and dX = Alpha*dX0, where F is the calculation\n")
            msgs += ("     operator. If it is given, Y must be in the image of F. If it is not given,\n")
            msgs += ("     one takes Y = F(X).\n")
        msgs += ("\n")
        msgs += ("     (Remark: numbers that are (about) under %.0e represent 0 to machine precision)"%mpr)
        print(msgs)
        #
        # --------------------
        __pf = "  %"+str(__p+7)+"."+str(__p)+"e"
        __ms = "  %2i  %5.0e"+(__pf*4)
        __bl = "  %"+str(__p+7)+"s  "
        __entete = str.rstrip("  i   Alpha  "     + \
            str.center("||X||",2+__p+7)  + \
            str.center("||Y||",2+__p+7)  + \
            str.center("||dX||",2+__p+7) + \
            str.center("R(Alpha)",2+__p+7))
        __nbtirets = len(__entete) + 2
        #
        msgs  = ""
        msgs += "\n" + __marge + "-"*__nbtirets
        msgs += "\n" + __marge + __entete
        msgs += "\n" + __marge + "-"*__nbtirets
        #
        for i,amplitude in enumerate(Perturbations):
            dX          = amplitude * dX0
            NormedX     = numpy.linalg.norm( dX )
            #
            TangentFXdX = numpy.ravel( Ht( (Xn,dX) ) )
            AdjointFXY  = numpy.ravel( Ha( (Xn,Yn)  ) )
            #
            Residu = abs(float(numpy.dot( TangentFXdX, Yn ) - numpy.dot( dX, AdjointFXY )))
            #
            msg = __ms%(i,amplitude,NormeX,NormeY,NormedX,Residu)
            msgs += "\n" + __marge + msg
            #
            self.StoredVariables["Residu"].store( Residu )
        #
        msgs += "\n" + __marge + "-"*__nbtirets
        print(msgs)
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
