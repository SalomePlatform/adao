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

import numpy, copy, logging
from daCore import BasicObjects
from daCore.PlatformInfo import PlatformInfo, vfloat
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "OBSERVATIONSIMULATIONCOMPARISONTEST")
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
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "CurrentState",
                "Innovation",
                "InnovationAtCurrentState",
                "OMB",
                "SimulatedObservationAtCurrentState",
            ]
        )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
        )
        self.setAttributes(
            tags=(
                "Checking",
            ),
            features=(
                "DerivativeFree",
            ),
        )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, U, HO, EM, CM, R, B, Q)
        #
        Hm = HO["Direct"].appliedTo
        #
        X0 = copy.copy( Xb )
        Y0 = copy.copy( Y )
        #
        # ----------
        if len(self._parameters["StoreSupplementaryCalculations"]) > 0:
            BI = B.getI()
            RI = R.getI()

            def CostFunction(x, HmX):
                _X  = numpy.ravel(  x  )
                _HX = numpy.ravel( HmX )
                _X0 = numpy.ravel( X0 )
                _Y0 = numpy.ravel( Y0 )
                Jb  = vfloat( 0.5 *  (_X - _X0).T * (BI * (_X - _X0))  )  # noqa: E222
                Jo  = vfloat( 0.5 * (_Y0 - _HX).T * (RI * (_Y0 - _HX)) )
                J   = Jb + Jo
                self.StoredVariables["CostFunctionJb"].store( Jb )
                self.StoredVariables["CostFunctionJo"].store( Jo )
                self.StoredVariables["CostFunctionJ" ].store( J )
                return J, Jb, Jo
        # ----------
        __s = self._parameters["ShowElementarySummary"]
        __p = self._parameters["NumberOfPrintedDigits"]
        __r = self._parameters["NumberOfRepetition"]
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
        msgs += (__marge + "This test allows to analyze the (repetition of the) launch of some\n")
        msgs += (__marge + "given simulation operator F, applied to one single vector argument x,\n")
        msgs += (__marge + "and its comparison to observations or measures y through the innovation\n")
        msgs += (__marge + "difference OMB = y - F(x) (Observation minus evaluation at Background)\n")
        msgs += (__marge + "and (if required) the data assimilation standard cost function J.\n")
        msgs += (__marge + "The output shows simple statistics related to its successful execution,\n")
        msgs += (__marge + "or related to the similarities of repetition of its execution.\n")
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
        msgs += (__marge + "Characteristics of input vector of observations Yobs, internally converted:\n")
        msgs += (__marge + "  Type...............: %s\n")%type( Y0 )
        msgs += (__marge + "  Length of vector...: %i\n")%max(numpy.ravel( Y0 ).shape)
        msgs += (__marge + "  Minimum value......: %." + str(__p) + "e\n")%numpy.min(  Y0 )
        msgs += (__marge + "  Maximum value......: %." + str(__p) + "e\n")%numpy.max(  Y0 )
        msgs += (__marge + "  Mean of vector.....: %." + str(__p) + "e\n")%numpy.mean( Y0, dtype=mfp )
        msgs += (__marge + "  Standard error.....: %." + str(__p) + "e\n")%numpy.std(  Y0, dtype=mfp )
        msgs += (__marge + "  L2 norm of vector..: %." + str(__p) + "e\n")%numpy.linalg.norm( Y0 )
        msgs += ("\n")
        msgs += (__marge + "%s\n\n"%("-" * 75,))
        #
        if self._parameters["SetDebug"]:
            CUR_LEVEL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.DEBUG)
            if __r > 1:
                msgs += (__flech + "Beginning of repeated evaluation, activating debug\n")
            else:
                msgs += (__flech + "Beginning of evaluation, activating debug\n")
        else:
            if __r > 1:
                msgs += (__flech + "Beginning of repeated evaluation, without activating debug\n")
            else:
                msgs += (__flech + "Beginning of evaluation, without activating debug\n")
        print(msgs)  # 1
        #
        # ----------
        HO["Direct"].disableAvoidingRedundancy()
        # ----------
        Ys = []
        Ds = []
        Js = []
        _Y0 = numpy.ravel( Y0 )
        for i in range(__r):
            if self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( X0 )
            if __s:
                msgs  = (__marge + "%s\n"%("-" * 75,))  # 2-1
                if __r > 1:
                    msgs += ("\n")
                    msgs += (__flech + "Repetition step number %i on a total of %i\n"%(i + 1, __r))
                msgs += ("\n")
                msgs += (__flech + "Launching operator sequential evaluation\n")
                print(msgs)  # 2-1
            #
            Yn = Hm( X0 )
            #
            if _Y0.size != Yn.size:
                raise ValueError("The size %i of observations Y and %i of observed calculation F(X) are different, they have to be identical."%(Y0.size, Yn.size))  # noqa: E501
            #
            Dn = _Y0 - numpy.ravel( Yn )
            #
            if len(self._parameters["StoreSupplementaryCalculations"]) > 0:
                J, Jb, Jo = CostFunction( X0, Yn )
                if self._toStore("CostFunctionJ"):
                    Js.append( J )
            if __s:
                msgs  = ("\n")  # 2-2
                msgs += (__flech + "End of operator sequential evaluation\n")
                msgs += ("\n")
                msgs += (__flech + "Information after evaluation:\n")
                msgs += ("\n")
                msgs += (__marge + "Characteristics of simulated output vector Y=F(X), to compare to others:\n")
                msgs += (__marge + "  Type...............: %s\n")%type( Yn )
                msgs += (__marge + "  Length of vector...: %i\n")%max(numpy.ravel( Yn ).shape)
                msgs += (__marge + "  Minimum value......: %." + str(__p) + "e\n")%numpy.min(  Yn )
                msgs += (__marge + "  Maximum value......: %." + str(__p) + "e\n")%numpy.max(  Yn )
                msgs += (__marge + "  Mean of vector.....: %." + str(__p) + "e\n")%numpy.mean( Yn, dtype=mfp )
                msgs += (__marge + "  Standard error.....: %." + str(__p) + "e\n")%numpy.std(  Yn, dtype=mfp )
                msgs += (__marge + "  L2 norm of vector..: %." + str(__p) + "e\n")%numpy.linalg.norm( Yn )
                msgs += ("\n")
                msgs += (__marge + "Characteristics of OMB differences between observations Yobs and simulated output vector Y=F(X):\n")  # noqa: E501
                msgs += (__marge + "  Type...............: %s\n")%type( Dn )
                msgs += (__marge + "  Length of vector...: %i\n")%max(numpy.ravel( Dn ).shape)
                msgs += (__marge + "  Minimum value......: %." + str(__p) + "e\n")%numpy.min(  Dn )
                msgs += (__marge + "  Maximum value......: %." + str(__p) + "e\n")%numpy.max(  Dn )
                msgs += (__marge + "  Mean of vector.....: %." + str(__p) + "e\n")%numpy.mean( Dn, dtype=mfp )
                msgs += (__marge + "  Standard error.....: %." + str(__p) + "e\n")%numpy.std(  Dn, dtype=mfp )
                msgs += (__marge + "  L2 norm of vector..: %." + str(__p) + "e\n")%numpy.linalg.norm( Dn )
                if len(self._parameters["StoreSupplementaryCalculations"]) > 0:
                    if self._toStore("CostFunctionJ"):
                        msgs += ("\n")
                        msgs += (__marge + "  Cost function J....: %." + str(__p) + "e\n")%J
                        msgs += (__marge + "  Cost function Jb...: %." + str(__p) + "e\n")%Jb
                        msgs += (__marge + "  Cost function Jo...: %." + str(__p) + "e\n")%Jo
                        msgs += (__marge + "  (Remark: the Jb background part of the cost function J is zero by hypothesis)\n")  # noqa: E501
                print(msgs)  # 2-2
            if self._toStore("SimulatedObservationAtCurrentState"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( numpy.ravel(Yn) )
            if self._toStore("Innovation"):
                self.StoredVariables["Innovation"].store( Dn )
            if self._toStore("OMB"):
                self.StoredVariables["OMB"].store( Dn )
            if self._toStore("InnovationAtCurrentState"):
                self.StoredVariables["InnovationAtCurrentState"].store( Dn )
            #
            Ys.append( copy.copy( numpy.ravel(
                Yn
            ) ) )
            Ds.append( copy.copy( numpy.ravel(
                Dn
            ) ) )
        # ----------
        HO["Direct"].enableAvoidingRedundancy()
        # ----------
        #
        msgs  = (__marge + "%s\n\n"%("-" * 75,))  # 3
        if self._parameters["SetDebug"]:
            if __r > 1:
                msgs += (__flech + "End of repeated evaluation, deactivating debug if necessary\n")
            else:
                msgs += (__flech + "End of evaluation, deactivating debug if necessary\n")
            logging.getLogger().setLevel(CUR_LEVEL)
        else:
            if __r > 1:
                msgs += (__flech + "End of repeated evaluation, without deactivating debug\n")
            else:
                msgs += (__flech + "End of evaluation, without deactivating debug\n")
        msgs += ("\n")
        msgs += (__marge + "%s\n"%("-" * 75,))
        #
        if __r > 1:
            msgs += ("\n")
            msgs += (__flech + "Launching statistical summary calculation for %i states\n"%__r)
            msgs += ("\n")
            msgs += (__marge + "%s\n"%("-" * 75,))
            msgs += ("\n")
            msgs += (__flech + "Statistical analysis of the outputs obtained through sequential repeated evaluations\n")  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "(Remark: numbers that are (about) under %.0e represent 0 to machine precision)\n"%mpr)  # noqa: E501
            msgs += ("\n")
            Yy = numpy.array( Ys )
            msgs += (__marge + "Number of evaluations...........................: %i\n")%len( Ys )
            msgs += ("\n")
            msgs += (__marge + "Characteristics of the whole set of outputs Y:\n")
            msgs += (__marge + "  Size of each of the outputs...................: %i\n")%Ys[0].size
            msgs += (__marge + "  Minimum value of the whole set of outputs.....: %." + str(__p) + "e\n")%numpy.min(  Yy )  # noqa: E501
            msgs += (__marge + "  Maximum value of the whole set of outputs.....: %." + str(__p) + "e\n")%numpy.max(  Yy )  # noqa: E501
            msgs += (__marge + "  Mean of vector of the whole set of outputs....: %." + str(__p) + "e\n")%numpy.mean( Yy, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the whole set of outputs....: %." + str(__p) + "e\n")%numpy.std(  Yy, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            Ym = numpy.mean( numpy.array( Ys ), axis=0, dtype=mfp )
            msgs += (__marge + "Characteristics of the vector Ym, mean of the outputs Y:\n")
            msgs += (__marge + "  Size of the mean of the outputs...............: %i\n")%Ym.size
            msgs += (__marge + "  Minimum value of the mean of the outputs......: %." + str(__p) + "e\n")%numpy.min(  Ym )  # noqa: E501
            msgs += (__marge + "  Maximum value of the mean of the outputs......: %." + str(__p) + "e\n")%numpy.max(  Ym )  # noqa: E501
            msgs += (__marge + "  Mean of the mean of the outputs...............: %." + str(__p) + "e\n")%numpy.mean( Ym, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the mean of the outputs.....: %." + str(__p) + "e\n")%numpy.std(  Ym, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            Ye = numpy.mean( numpy.array( Ys ) - Ym, axis=0, dtype=mfp )
            msgs += (__marge + "Characteristics of the mean of the differences between the outputs Y and their mean Ym:\n")  # noqa: E501
            msgs += (__marge + "  Size of the mean of the differences...........: %i\n")%Ye.size
            msgs += (__marge + "  Minimum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.min(  Ye )  # noqa: E501
            msgs += (__marge + "  Maximum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.max(  Ye )  # noqa: E501
            msgs += (__marge + "  Mean of the mean of the differences...........: %." + str(__p) + "e\n")%numpy.mean( Ye, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the mean of the differences.: %." + str(__p) + "e\n")%numpy.std(  Ye, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "%s\n"%("-" * 75,))
            msgs += ("\n")
            msgs += (__flech + "Statistical analysis of the OMB differences obtained through sequential repeated evaluations\n")  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "(Remark: numbers that are (about) under %.0e represent 0 to machine precision)\n"%mpr)  # noqa: E501
            msgs += ("\n")
            Dy = numpy.array( Ds )
            msgs += (__marge + "Number of evaluations...........................: %i\n")%len( Ds )
            msgs += ("\n")
            msgs += (__marge + "Characteristics of the whole set of OMB differences:\n")
            msgs += (__marge + "  Size of each of the outputs...................: %i\n")%Ds[0].size
            msgs += (__marge + "  Minimum value of the whole set of differences.: %." + str(__p) + "e\n")%numpy.min(  Dy )  # noqa: E501
            msgs += (__marge + "  Maximum value of the whole set of differences.: %." + str(__p) + "e\n")%numpy.max(  Dy )  # noqa: E501
            msgs += (__marge + "  Mean of vector of the whole set of differences: %." + str(__p) + "e\n")%numpy.mean( Dy, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the whole set of differences: %." + str(__p) + "e\n")%numpy.std(  Dy, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            Dm = numpy.mean( numpy.array( Ds ), axis=0, dtype=mfp )
            msgs += (__marge + "Characteristics of the vector Dm, mean of the OMB differences:\n")
            msgs += (__marge + "  Size of the mean of the differences...........: %i\n")%Dm.size
            msgs += (__marge + "  Minimum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.min(  Dm )  # noqa: E501
            msgs += (__marge + "  Maximum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.max(  Dm )  # noqa: E501
            msgs += (__marge + "  Mean of the mean of the differences...........: %." + str(__p) + "e\n")%numpy.mean( Dm, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the mean of the differences.: %." + str(__p) + "e\n")%numpy.std(  Dm, dtype=mfp )  # noqa: E501
            msgs += ("\n")
            De = numpy.mean( numpy.array( Ds ) - Dm, axis=0, dtype=mfp )
            msgs += (__marge + "Characteristics of the mean of the differences between the OMB differences and their mean Dm:\n")  # noqa: E501
            msgs += (__marge + "  Size of the mean of the differences...........: %i\n")%De.size
            msgs += (__marge + "  Minimum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.min( De )  # noqa: E501
            msgs += (__marge + "  Maximum value of the mean of the differences..: %." + str(__p) + "e\n")%numpy.max( De )  # noqa: E501
            msgs += (__marge + "  Mean of the mean of the differences...........: %." + str(__p) + "e\n")%numpy.mean( De, dtype=mfp )  # noqa: E501
            msgs += (__marge + "  Standard error of the mean of the differences.: %." + str(__p) + "e\n")%numpy.std( De, dtype=mfp )  # noqa: E501
            #
            if self._toStore("CostFunctionJ"):
                msgs += ("\n")
                Jj = numpy.array( Js )
                msgs += (__marge + "%s\n\n"%("-" * 75,))
                msgs += (__flech + "Statistical analysis of the cost function J values obtained through sequential repeated evaluations\n")  # noqa: E501
                msgs += ("\n")
                msgs += (__marge + "Number of evaluations...........................: %i\n")%len( Js )
                msgs += ("\n")
                msgs += (__marge + "Characteristics of the whole set of data assimilation cost function J values:\n")
                msgs += (__marge + "  Minimum value of the whole set of J...........: %." + str(__p) + "e\n")%numpy.min(  Jj )  # noqa: E501
                msgs += (__marge + "  Maximum value of the whole set of J...........: %." + str(__p) + "e\n")%numpy.max(  Jj )  # noqa: E501
                msgs += (__marge + "  Mean of vector of the whole set of J..........: %." + str(__p) + "e\n")%numpy.mean( Jj, dtype=mfp )  # noqa: E501
                msgs += (__marge + "  Standard error of the whole set of J..........: %." + str(__p) + "e\n")%numpy.std(  Jj, dtype=mfp )  # noqa: E501
                msgs += (__marge + "  (Remark: variations of the cost function J only come from the observation part Jo of J)\n")  # noqa: E501
            msgs += ("\n")
            msgs += (__marge + "%s\n"%("-" * 75,))
        #
        msgs += ("\n")
        msgs += (__marge + "End of the \"%s\" verification\n\n"%self._name)
        msgs += (__marge + "%s\n"%("-" * 75,))
        print(msgs)  # 3
        #
        self._post_run(HO, EM)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
