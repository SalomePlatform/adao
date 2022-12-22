# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2023 EDF R&D
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

import logging
from daCore import BasicObjects, PlatformInfo
import numpy, copy
mpr = PlatformInfo.PlatformInfo().MachinePrecision()
mfp = PlatformInfo.PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "FUNCTIONTEST")
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
            )
        self.setAttributes(tags=(
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        Hm = HO["Direct"].appliedTo
        #
        Xn = copy.copy( Xb )
        #
        # ----------
        __s = self._parameters["ShowElementarySummary"]
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
        msgs += ("     This test allows to analyze the (repetition of) launch of some given\n")
        msgs += ("     operator. It shows simple statistics related to its successful execution,\n")
        msgs += ("     or related to the similarities of repetition of its execution.\n")
        msgs += ("\n")
        msgs += ("===> Information before launching:\n")
        msgs += ("     -----------------------------\n")
        msgs += ("     Characteristics of input vector X, internally converted:\n")
        msgs += ("       Type...............: %s\n")%type( Xn )
        msgs += ("       Length of vector...: %i\n")%max(numpy.ravel( Xn ).shape)
        msgs += ("       Minimum value......: %."+str(__p)+"e\n")%numpy.min( Xn )
        msgs += ("       Maximum value......: %."+str(__p)+"e\n")%numpy.max( Xn )
        msgs += ("       Mean of vector.....: %."+str(__p)+"e\n")%numpy.mean( Xn, dtype=mfp )
        msgs += ("       Standard error.....: %."+str(__p)+"e\n")%numpy.std( Xn, dtype=mfp )
        msgs += ("       L2 norm of vector..: %."+str(__p)+"e\n")%numpy.linalg.norm( Xn )
        print(msgs)
        #
        print("     %s\n"%("-"*75,))
        if self._parameters["SetDebug"]:
            CUR_LEVEL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.DEBUG)
            print("===> Beginning of repeated evaluation, activating debug\n")
        else:
            print("===> Beginning of repeated evaluation, without activating debug\n")
        #
        # ----------
        HO["Direct"].disableAvoidingRedundancy()
        # ----------
        Ys = []
        for i in range(self._parameters["NumberOfRepetition"]):
            if self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( numpy.ravel(Xn) )
            if __s:
                print("     %s\n"%("-"*75,))
                if self._parameters["NumberOfRepetition"] > 1:
                    print("===> Repetition step number %i on a total of %i\n"%(i+1,self._parameters["NumberOfRepetition"]))
                print("===> Launching operator sequential evaluation\n")
            #
            Yn = Hm( Xn )
            #
            if __s:
                print("\n===> End of operator sequential evaluation\n")
                #
                msgs  = ("===> Information after evaluation:\n")
                msgs += ("\n     Characteristics of simulated output vector Y=H(X), to compare to others:\n")
                msgs += ("       Type...............: %s\n")%type( Yn )
                msgs += ("       Length of vector...: %i\n")%max(numpy.ravel( Yn ).shape)
                msgs += ("       Minimum value......: %."+str(__p)+"e\n")%numpy.min( Yn )
                msgs += ("       Maximum value......: %."+str(__p)+"e\n")%numpy.max( Yn )
                msgs += ("       Mean of vector.....: %."+str(__p)+"e\n")%numpy.mean( Yn, dtype=mfp )
                msgs += ("       Standard error.....: %."+str(__p)+"e\n")%numpy.std( Yn, dtype=mfp )
                msgs += ("       L2 norm of vector..: %."+str(__p)+"e\n")%numpy.linalg.norm( Yn )
                print(msgs)
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
        print("     %s\n"%("-"*75,))
        if self._parameters["SetDebug"]:
            print("===> End of repeated evaluation, deactivating debug if necessary\n")
            logging.getLogger().setLevel(CUR_LEVEL)
        else:
            print("===> End of repeated evaluation, without deactivating debug\n")
        #
        if self._parameters["NumberOfRepetition"] > 1:
            print("     %s\n"%("-"*75,))
            print("===> Launching statistical summary calculation for %i states\n"%self._parameters["NumberOfRepetition"])
            msgs  = ("     %s\n"%("-"*75,))
            msgs += ("\n===> Statistical analysis of the outputs obtained through sequential repeated evaluations\n")
            msgs += ("\n     (Remark: numbers that are (about) under %.0e represent 0 to machine precision)\n"%mpr)
            Yy = numpy.array( Ys )
            msgs += ("\n     Characteristics of the whole set of outputs Y:\n")
            msgs += ("       Number of evaluations.........................: %i\n")%len( Ys )
            msgs += ("       Minimum value of the whole set of outputs.....: %."+str(__p)+"e\n")%numpy.min( Yy )
            msgs += ("       Maximum value of the whole set of outputs.....: %."+str(__p)+"e\n")%numpy.max( Yy )
            msgs += ("       Mean of vector of the whole set of outputs....: %."+str(__p)+"e\n")%numpy.mean( Yy, dtype=mfp )
            msgs += ("       Standard error of the whole set of outputs....: %."+str(__p)+"e\n")%numpy.std( Yy, dtype=mfp )
            Ym = numpy.mean( numpy.array( Ys ), axis=0, dtype=mfp )
            msgs += ("\n     Characteristics of the vector Ym, mean of the outputs Y:\n")
            msgs += ("       Size of the mean of the outputs...............: %i\n")%Ym.size
            msgs += ("       Minimum value of the mean of the outputs......: %."+str(__p)+"e\n")%numpy.min( Ym )
            msgs += ("       Maximum value of the mean of the outputs......: %."+str(__p)+"e\n")%numpy.max( Ym )
            msgs += ("       Mean of the mean of the outputs...............: %."+str(__p)+"e\n")%numpy.mean( Ym, dtype=mfp )
            msgs += ("       Standard error of the mean of the outputs.....: %."+str(__p)+"e\n")%numpy.std( Ym, dtype=mfp )
            Ye = numpy.mean( numpy.array( Ys ) - Ym, axis=0, dtype=mfp )
            msgs += "\n     Characteristics of the mean of the differences between the outputs Y and their mean Ym:\n"
            msgs += ("       Size of the mean of the differences...........: %i\n")%Ym.size
            msgs += ("       Minimum value of the mean of the differences..: %."+str(__p)+"e\n")%numpy.min( Ye )
            msgs += ("       Maximum value of the mean of the differences..: %."+str(__p)+"e\n")%numpy.max( Ye )
            msgs += ("       Mean of the mean of the differences...........: %."+str(__p)+"e\n")%numpy.mean( Ye, dtype=mfp )
            msgs += ("       Standard error of the mean of the differences.: %."+str(__p)+"e\n")%numpy.std( Ye, dtype=mfp )
            msgs += ("\n     %s\n"%("-"*75,))
            print(msgs)
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
