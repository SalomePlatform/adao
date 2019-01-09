# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2019 EDF R&D
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
import numpy, math
mfp = PlatformInfo.PlatformInfo().MaximumPrecision()

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "ENSEMBLEKALMANFILTER")
        self.defineRequiredParameter(
            name     = "NumberOfMembers",
            default  = 100,
            typecast = int,
            message  = "Nombre de membres dans l'ensemble",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'etat ou de parametres",
            listval  = ["State", "Parameters"],
            )
        self.defineRequiredParameter(
            name     = "SetSeed",
            typecast = numpy.random.seed,
            message  = "Graine fixée pour le générateur aléatoire",
            )
        self.defineRequiredParameter(
            name     = "StoreInternalVariables",
            default  = False,
            typecast = bool,
            message  = "Stockage des variables internes ou intermédiaires du calcul",
            )
        self.defineRequiredParameter(
            name     = "StoreSupplementaryCalculations",
            default  = [],
            typecast = tuple,
            message  = "Liste de calculs supplémentaires à stocker et/ou effectuer",
            listval  = [
                "APosterioriCorrelations",
                "APosterioriCovariance",
                "APosterioriStandardDeviations",
                "APosterioriVariances",
                "BMA",
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "CurrentState",
                "Innovation",
                ]
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            optional = ("U", "EM", "CM", "Q"),
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        if self._parameters["EstimationOf"] == "Parameters":
            self._parameters["StoreInternalVariables"] = True
        #
        # Opérateurs
        # ----------
        H = HO["Direct"].appliedControledFormTo
        #
        if self._parameters["EstimationOf"] == "State":
            M = EM["Direct"].appliedControledFormTo
        #
        if CM is not None and "Tangent" in CM and U is not None:
            Cm = CM["Tangent"].asMatrix(Xb)
        else:
            Cm = None
        #
        # Nombre de pas identique au nombre de pas d'observations
        # -------------------------------------------------------
        if hasattr(Y,"stepnumber"):
            duration = Y.stepnumber()
            __p = numpy.cumprod(Y.shape())[-1]
        else:
            duration = 2
            __p = numpy.array(Y).size
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if self._parameters["StoreInternalVariables"] or \
            self._toStore("CostFunctionJ") or \
            self._toStore("CostFunctionJb") or \
            self._toStore("CostFunctionJo") or \
            self._toStore("APosterioriCovariance"):
            BI = B.getI()
            RI = R.getI()
        BIdemi = B.choleskyI()
        RIdemi = R.choleskyI()
        #
        # Initialisation
        # --------------
        __n = Xb.size
        __m = self._parameters["NumberOfMembers"]
        Xn = numpy.asmatrix(numpy.dot( Xb.reshape(__n,1), numpy.ones((1,__m)) ))
        if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(__n)
        else:                         Pn = B
        if hasattr(R,"asfullmatrix"): Rn = R.asfullmatrix(__p)
        else:                         Rn = R
        if hasattr(Q,"asfullmatrix"): Qn = Q.asfullmatrix(__n)
        else:                         Qn = Q
        #
        self.StoredVariables["Analysis"].store( Xb.A1 )
        if self._toStore("APosterioriCovariance"):
            self.StoredVariables["APosterioriCovariance"].store( Pn )
            covarianceXa = Pn
        Xa               = Xb
        previousJMinimum = numpy.finfo(float).max
        #
        # Predimensionnement
        Xn_predicted = numpy.asmatrix(numpy.zeros((__n,__m)))
        HX_predicted = numpy.asmatrix(numpy.zeros((__p,__m)))
        #
        for step in range(duration-1):
            if hasattr(Y,"store"):
                Ynpu = numpy.asmatrix(numpy.ravel( Y[step+1] )).T
            else:
                Ynpu = numpy.asmatrix(numpy.ravel( Y )).T
            #
            if U is not None:
                if hasattr(U,"store") and len(U)>1:
                    Un = numpy.asmatrix(numpy.ravel( U[step] )).T
                elif hasattr(U,"store") and len(U)==1:
                    Un = numpy.asmatrix(numpy.ravel( U[0] )).T
                else:
                    Un = numpy.asmatrix(numpy.ravel( U )).T
            else:
                Un = None
            #
            if self._parameters["EstimationOf"] == "State":
                for i in range(__m):
                    qi = numpy.asmatrix(numpy.random.multivariate_normal(numpy.zeros(__n), Qn)).T
                    Xn_predicted[:,i] = numpy.asmatrix(numpy.ravel( M((Xn[:,i], Un)) )).T + qi
                    HX_predicted[:,i] = numpy.asmatrix(numpy.ravel( H((Xn_predicted[:,i], Un)) )).T
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                    Xn_predicted = Xn_predicted + Cm * Un
            elif self._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                Xn_predicted = Xn
            #
            Xfm = numpy.asmatrix(numpy.ravel(Xn_predicted.mean(axis=1, dtype=mfp))).T
            Hfm = numpy.asmatrix(numpy.ravel(HX_predicted.mean(axis=1, dtype=mfp))).T
            Af  = Xn_predicted - Xfm
            Hf  = HX_predicted - Hfm
            #
            PfHT, HPfHT = 0., 0.
            for i in range(__m):
                PfHT  += Af[:,i] * Hf[:,i].T
                HPfHT += Hf[:,i] * Hf[:,i].T
            PfHT  = (1./(__m-1)) * PfHT
            HPfHT = (1./(__m-1)) * HPfHT
            #
            K = PfHT * ( R + HPfHT ).I
            #
            Yo = numpy.asmatrix(numpy.zeros((__p,__m)))
            for i in range(__m):
                ri = numpy.asmatrix(numpy.random.multivariate_normal(numpy.zeros(__p), Rn)).T
                Yo[:,i] = Ynpu + ri
            #
            for i in range(__m):
                Xn[:,i] = Xn_predicted[:,i] + K * (Yo[:,i] - HX_predicted[:,i])
            #
            Xa = Xn.mean(axis=1, dtype=mfp)
            self.StoredVariables["Analysis"].store( Xa )
            #
            del Yo, PfHT, HPfHT
            if self._parameters["StoreInternalVariables"] or \
                self._toStore("CostFunctionJ") or \
                self._toStore("CostFunctionJb") or \
                self._toStore("CostFunctionJo") or \
                self._toStore("APosterioriCovariance") or \
                self._toStore("Innovation"):
                d = Ynpu - numpy.asmatrix(numpy.ravel( H((Xa, Un)) )).T
                self.StoredVariables["Innovation"].store( d )
            if self._parameters["StoreInternalVariables"] \
                or self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( Xn )
            if self._parameters["StoreInternalVariables"] or \
                self._toStore("CostFunctionJ") or \
                self._toStore("CostFunctionJb") or \
                self._toStore("CostFunctionJo") or \
                self._toStore("APosterioriCovariance"):
                Jb  = 0.5 * (Xa - Xb).T * BI * (Xa - Xb)
                Jo  = 0.5 * d.T * RI * d
                J   = float( Jb ) + float( Jo )
                self.StoredVariables["CostFunctionJb"].store( Jb )
                self.StoredVariables["CostFunctionJo"].store( Jo )
                self.StoredVariables["CostFunctionJ" ].store( J )
            if self._toStore("APosterioriCovariance"):
                Ht = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
                Ht = Ht.reshape(__p,__n) # ADAO & check shape
                Pf = 0.
                for i in range(__m):
                    Pf += Af[:,i] * Af[:,i].T
                Pf = (1./(__m-1)) * Pf
                Pn = (1. - K * Ht) * Pf
                self.StoredVariables["APosterioriCovariance"].store( Pn )
                if J < previousJMinimum:
                    previousJMinimum  = J
                    Xa                = Xn
                    covarianceXa      = Pn
        #
        # Stockage supplementaire de l'optimum en estimation de parametres
        # ----------------------------------------------------------------
        if self._parameters["EstimationOf"] == "Parameters":
            self.StoredVariables["Analysis"].store( Xa.A1 )
            if self._toStore("APosterioriCovariance"):
                self.StoredVariables["APosterioriCovariance"].store( covarianceXa )
        #
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')
