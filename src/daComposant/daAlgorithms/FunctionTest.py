#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2017 EDF R&D
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
mfp = PlatformInfo.PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "FUNCTIONTEST")
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
            listval  = ["CurrentState", "SimulatedObservationAtCurrentState"]
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        #
        self.setParameters(Parameters)
        #
        Hm = HO["Direct"].appliedTo
        #
        Xn = copy.copy( Xb )
        #
        # ----------
        _p = self._parameters["NumberOfPrintedDigits"]
        if len(self._parameters["ResultTitle"]) > 0:
            msg  = "     ====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
            msg += "        " + self._parameters["ResultTitle"] + "\n"
            msg += "     ====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
            print("%s"%msg)
        #
        msg  = ("===> Information before launching:\n")
        msg += ("     -----------------------------\n")
        msg += ("     Characteristics of input vector X, internally converted:\n")
        msg += ("       Type...............: %s\n")%type( Xn )
        msg += ("       Lenght of vector...: %i\n")%max(numpy.matrix( Xn ).shape)
        msg += ("       Minimum value......: %."+str(_p)+"e\n")%numpy.min( Xn )
        msg += ("       Maximum value......: %."+str(_p)+"e\n")%numpy.max( Xn )
        msg += ("       Mean of vector.....: %."+str(_p)+"e\n")%numpy.mean( Xn, dtype=mfp )
        msg += ("       Standard error.....: %."+str(_p)+"e\n")%numpy.std( Xn, dtype=mfp )
        msg += ("       L2 norm of vector..: %."+str(_p)+"e\n")%numpy.linalg.norm( Xn )
        print(msg)
        #
        if self._parameters["SetDebug"]:
            CUR_LEVEL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.DEBUG)
            print("===> Beginning of evaluation, activating debug\n")
        else:
            print("===> Beginning of evaluation, without activating debug\n")
        #
        # ----------
        HO["Direct"].disableAvoidingRedundancy()
        # ----------
        Ys = []
        for i in range(self._parameters["NumberOfRepetition"]):
            if "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentState"].store( numpy.ravel(Xn) )
            print("     %s\n"%("-"*75,))
            if self._parameters["NumberOfRepetition"] > 1:
                print("===> Repetition step number %i on a total of %i\n"%(i+1,self._parameters["NumberOfRepetition"]))
            print("===> Launching direct operator evaluation\n")
            #
            Yn = Hm( Xn )
            #
            print("\n===> End of direct operator evaluation\n")
            #
            msg  = ("===> Information after evaluation:\n")
            msg += ("\n     Characteristics of simulated output vector Y=H(X), to compare to others:\n")
            msg += ("       Type...............: %s\n")%type( Yn )
            msg += ("       Lenght of vector...: %i\n")%max(numpy.matrix( Yn ).shape)
            msg += ("       Minimum value......: %."+str(_p)+"e\n")%numpy.min( Yn )
            msg += ("       Maximum value......: %."+str(_p)+"e\n")%numpy.max( Yn )
            msg += ("       Mean of vector.....: %."+str(_p)+"e\n")%numpy.mean( Yn, dtype=mfp )
            msg += ("       Standard error.....: %."+str(_p)+"e\n")%numpy.std( Yn, dtype=mfp )
            msg += ("       L2 norm of vector..: %."+str(_p)+"e\n")%numpy.linalg.norm( Yn )
            print(msg)
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
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
            print("===> End evaluation, deactivating debug if necessary\n")
            logging.getLogger().setLevel(CUR_LEVEL)
        #
        if self._parameters["NumberOfRepetition"] > 1:
            msg  = ("     %s\n"%("-"*75,))
            msg += ("\n===> Statistical analysis of the outputs obtained throught repeated evaluations\n")
            msg += ("\n     (Remark: numbers that are (about) under 1.e-16 represent 0 to machine precision)\n")
            Yy = numpy.array( Ys )
            msg += ("\n     Characteristics of the whole set of outputs Y:\n")
            msg += ("       Number of evaluations.........................: %i\n")%len( Ys )
            msg += ("       Minimum value of the whole set of outputs.....: %."+str(_p)+"e\n")%numpy.min( Yy )
            msg += ("       Maximum value of the whole set of outputs.....: %."+str(_p)+"e\n")%numpy.max( Yy )
            msg += ("       Mean of vector of the whole set of outputs....: %."+str(_p)+"e\n")%numpy.mean( Yy, dtype=mfp )
            msg += ("       Standard error of the whole set of outputs....: %."+str(_p)+"e\n")%numpy.std( Yy, dtype=mfp )
            Ym = numpy.mean( numpy.array( Ys ), axis=0, dtype=mfp )
            msg += ("\n     Characteristics of the vector Ym, mean of the outputs Y:\n")
            msg += ("       Size of the mean of the outputs...............: %i\n")%Ym.size
            msg += ("       Minimum value of the mean of the outputs......: %."+str(_p)+"e\n")%numpy.min( Ym )
            msg += ("       Maximum value of the mean of the outputs......: %."+str(_p)+"e\n")%numpy.max( Ym )
            msg += ("       Mean of the mean of the outputs...............: %."+str(_p)+"e\n")%numpy.mean( Ym, dtype=mfp )
            msg += ("       Standard error of the mean of the outputs.....: %."+str(_p)+"e\n")%numpy.std( Ym, dtype=mfp )
            Ye = numpy.mean( numpy.array( Ys ) - Ym, axis=0, dtype=mfp )
            msg += "\n     Characteristics of the mean of the differences between the outputs Y and their mean Ym:\n"
            msg += ("       Size of the mean of the differences...........: %i\n")%Ym.size
            msg += ("       Minimum value of the mean of the differences..: %."+str(_p)+"e\n")%numpy.min( Ye )
            msg += ("       Maximum value of the mean of the differences..: %."+str(_p)+"e\n")%numpy.max( Ye )
            msg += ("       Mean of the mean of the differences...........: %."+str(_p)+"e\n")%numpy.mean( Ye, dtype=mfp )
            msg += ("       Standard error of the mean of the differences.: %."+str(_p)+"e\n")%numpy.std( Ye, dtype=mfp )
            msg += ("\n     %s\n"%("-"*75,))
            print(msg)
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
