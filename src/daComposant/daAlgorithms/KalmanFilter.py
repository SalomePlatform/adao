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

import logging
from daCore import BasicObjects
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "KALMANFILTER")
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'etat ou de parametres",
            listval  = ["State", "Parameters"],
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
                "Analysis",
                "APosterioriCorrelations",
                "APosterioriCovariance",
                "APosterioriStandardDeviations",
                "APosterioriVariances",
                "BMA",
                "CostFunctionJ",
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJb",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJo",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentOptimum",
                "CurrentState",
                "ForecastState",
                "IndexOfOptimum",
                "InnovationAtCurrentAnalysis",
                "InnovationAtCurrentState",
                "SimulatedObservationAtCurrentAnalysis",
                "SimulatedObservationAtCurrentOptimum",
                "SimulatedObservationAtCurrentState",
                ]
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R", "B"),
            optional = ("U", "EM", "CM", "Q"),
            )
        self.setAttributes(tags=(
            "DataAssimilation",
            "Linear",
            "Filter",
            "Dynamic",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        if self._parameters["EstimationOf"] == "Parameters":
            self._parameters["StoreInternalVariables"] = True
        #
        # Opérateurs
        # ----------
        Ht = HO["Tangent"].asMatrix(Xb)
        Ha = HO["Adjoint"].asMatrix(Xb)
        #
        if self._parameters["EstimationOf"] == "State":
            Mt = EM["Tangent"].asMatrix(Xb)
            Ma = EM["Adjoint"].asMatrix(Xb)
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
        else:
            duration = 2
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        if self._parameters["StoreInternalVariables"] \
            or self._toStore("CostFunctionJ") \
            or self._toStore("CostFunctionJb") \
            or self._toStore("CostFunctionJo") \
            or self._toStore("CurrentOptimum") \
            or self._toStore("APosterioriCovariance"):
            BI = B.getI()
            RI = R.getI()
        #
        # Initialisation
        # --------------
        Xn = Xb
        Pn = B
        #
        if len(self.StoredVariables["Analysis"])==0 or not self._parameters["nextStep"]:
            self.StoredVariables["Analysis"].store( numpy.ravel(Xn) )
            if self._toStore("APosterioriCovariance"):
                self.StoredVariables["APosterioriCovariance"].store( Pn.asfullmatrix(Xn.size) )
                covarianceXa = Pn
        #
        Xa               = Xn
        previousJMinimum = numpy.finfo(float).max
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
                Xn_predicted = Mt * Xn
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                    Cm = Cm.reshape(Xn.size,Un.size) # ADAO & check shape
                    Xn_predicted = Xn_predicted + Cm * Un
                Pn_predicted = Q + Mt * Pn * Ma
            elif self._parameters["EstimationOf"] == "Parameters":
                # --- > Par principe, M = Id, Q = 0
                Xn_predicted = Xn
                Pn_predicted = Pn
            #
            if self._parameters["EstimationOf"] == "State":
                _HX          = Ht * Xn_predicted
                _Innovation  = Ynpu - _HX
            elif self._parameters["EstimationOf"] == "Parameters":
                _HX          = Ht * Xn_predicted
                _Innovation  = Ynpu - _HX
                if Cm is not None and Un is not None: # Attention : si Cm est aussi dans H, doublon !
                    _Innovation = _Innovation - Cm * Un
            #
            _A = R + numpy.dot(Ht, Pn_predicted * Ha)
            _u = numpy.linalg.solve( _A , _Innovation )
            Xn = Xn_predicted + Pn_predicted * Ha * _u
            Kn = Pn_predicted * Ha * (R + numpy.dot(Ht, Pn_predicted * Ha)).I
            Pn = Pn_predicted - Kn * Ht * Pn_predicted
            Xa, _HXa = Xn, _HX # Pointeurs
            #
            # ---> avec analysis
            self.StoredVariables["Analysis"].store( Xa )
            if self._toStore("SimulatedObservationAtCurrentAnalysis"):
                self.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
            if self._toStore("InnovationAtCurrentAnalysis"):
                self.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
            # ---> avec current state
            if self._parameters["StoreInternalVariables"] \
                or self._toStore("CurrentState"):
                self.StoredVariables["CurrentState"].store( Xn )
            if self._toStore("ForecastState"):
                self.StoredVariables["ForecastState"].store( Xn_predicted )
            if self._toStore("BMA"):
                self.StoredVariables["BMA"].store( Xn_predicted - Xa )
            if self._toStore("InnovationAtCurrentState"):
                self.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
            if self._toStore("SimulatedObservationAtCurrentState") \
                or self._toStore("SimulatedObservationAtCurrentOptimum"):
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            # ---> autres
            if self._parameters["StoreInternalVariables"] \
                or self._toStore("CostFunctionJ") \
                or self._toStore("CostFunctionJb") \
                or self._toStore("CostFunctionJo") \
                or self._toStore("CurrentOptimum") \
                or self._toStore("APosterioriCovariance"):
                Jb  = float( 0.5 * (Xa - Xb).T * BI * (Xa - Xb) )
                Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
                J   = Jb + Jo
                self.StoredVariables["CostFunctionJb"].store( Jb )
                self.StoredVariables["CostFunctionJo"].store( Jo )
                self.StoredVariables["CostFunctionJ" ].store( J )
                #
                if self._toStore("IndexOfOptimum") \
                    or self._toStore("CurrentOptimum") \
                    or self._toStore("CostFunctionJAtCurrentOptimum") \
                    or self._toStore("CostFunctionJbAtCurrentOptimum") \
                    or self._toStore("CostFunctionJoAtCurrentOptimum") \
                    or self._toStore("SimulatedObservationAtCurrentOptimum"):
                    IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
                if self._toStore("IndexOfOptimum"):
                    self.StoredVariables["IndexOfOptimum"].store( IndexMin )
                if self._toStore("CurrentOptimum"):
                    self.StoredVariables["CurrentOptimum"].store( self.StoredVariables["Analysis"][IndexMin] )
                if self._toStore("SimulatedObservationAtCurrentOptimum"):
                    self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( self.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
                if self._toStore("CostFunctionJbAtCurrentOptimum"):
                    self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJb"][IndexMin] )
                if self._toStore("CostFunctionJoAtCurrentOptimum"):
                    self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJo"][IndexMin] )
                if self._toStore("CostFunctionJAtCurrentOptimum"):
                    self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( self.StoredVariables["CostFunctionJ" ][IndexMin] )
            if self._toStore("APosterioriCovariance"):
                self.StoredVariables["APosterioriCovariance"].store( Pn )
            if self._parameters["EstimationOf"] == "Parameters" \
                and J < previousJMinimum:
                previousJMinimum    = J
                XaMin               = Xa
                if self._toStore("APosterioriCovariance"):
                    covarianceXaMin = Pn
        #
        # Stockage final supplémentaire de l'optimum en estimation de paramètres
        # ----------------------------------------------------------------------
        if self._parameters["EstimationOf"] == "Parameters":
            self.StoredVariables["Analysis"].store( XaMin )
            if self._toStore("APosterioriCovariance"):
                self.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
            if self._toStore("BMA"):
                self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
