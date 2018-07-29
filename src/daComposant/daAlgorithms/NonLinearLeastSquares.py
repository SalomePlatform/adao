# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2018 EDF R&D
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
import numpy, scipy.optimize

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "NONLINEARLEASTSQUARES")
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "LBFGSB",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = ["LBFGSB","TNC", "CG", "NCG", "BFGS", "LM"],
            )
        self.defineRequiredParameter(
            name     = "MaximumNumberOfSteps",
            default  = 15000,
            typecast = int,
            message  = "Nombre maximal de pas d'optimisation",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "CostDecrementTolerance",
            default  = 1.e-7,
            typecast = float,
            message  = "Diminution relative minimale du coût lors de l'arrêt",
            )
        self.defineRequiredParameter(
            name     = "ProjectedGradientTolerance",
            default  = -1,
            typecast = float,
            message  = "Maximum des composantes du gradient projeté lors de l'arrêt",
            minval   = -1,
            )
        self.defineRequiredParameter(
            name     = "GradientNormTolerance",
            default  = 1.e-05,
            typecast = float,
            message  = "Maximum des composantes du gradient lors de l'arrêt",
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
                "BMA",
                "OMA",
                "OMB",
                "CostFunctionJ",
                "CostFunctionJb",
                "CostFunctionJo",
                "CurrentState",
                "CurrentOptimum",
                "IndexOfOptimum",
                "Innovation",
                "InnovationAtCurrentState",
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJoAtCurrentOptimum",
                "SimulatedObservationAtBackground",
                "SimulatedObservationAtCurrentState",
                "SimulatedObservationAtOptimum",
                "SimulatedObservationAtCurrentOptimum",
                ]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "R"),
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        if "Minimizer" in self._parameters and self._parameters["Minimizer"] == "TNC":
            self.setParameterValue("StoreInternalVariables",True)
        #
        # Opérateurs
        # ----------
        Hm = HO["Direct"].appliedTo
        Ha = HO["Adjoint"].appliedInXTo
        #
        # Utilisation éventuelle d'un vecteur H(Xb) précalculé
        # ----------------------------------------------------
        if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
            HXb = Hm( Xb, HO["AppliedInX"]["HXb"])
        else:
            HXb = Hm( Xb )
        HXb = numpy.asmatrix(numpy.ravel( HXb )).T
        if Y.size != HXb.size:
            raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
        if max(Y.shape) != max(HXb.shape):
            raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
        #
        # Précalcul des inversions de B et R
        # ----------------------------------
        RI = R.getI()
        if self._parameters["Minimizer"] == "LM":
            RdemiI = R.choleskyI()
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(x):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            if self._parameters["StoreInternalVariables"] or \
                "CurrentState" in self._parameters["StoreSupplementaryCalculations"] or \
                "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentState"].store( _X )
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            _Innovation = Y - _HX
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"] or \
               "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
            if "InnovationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
            #
            Jb  = 0.
            Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
            J   = Jb + Jo
            #
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            if "IndexOfOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "CostFunctionJAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "CostFunctionJbAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "CostFunctionJoAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"] or \
               "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if "IndexOfOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if "CurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentOptimum"].store( self.StoredVariables["CurrentState"][IndexMin] )
            if "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
            if "CostFunctionJAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( self.StoredVariables["CostFunctionJ" ][IndexMin] )
            if "CostFunctionJbAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJb"][IndexMin] )
            if "CostFunctionJoAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJo"][IndexMin] )
            return J
        #
        def GradientOfCostFunction(x):
            _X      = numpy.asmatrix(numpy.ravel( x )).T
            _HX     = Hm( _X )
            _HX     = numpy.asmatrix(numpy.ravel( _HX )).T
            GradJb  = 0.
            GradJo  = - Ha( (_X, RI * (Y - _HX)) )
            GradJ   = numpy.asmatrix( numpy.ravel( GradJb ) + numpy.ravel( GradJo ) ).T
            return GradJ.A1
        #
        def CostFunctionLM(x):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            _HX = Hm( _X )
            _HX = numpy.asmatrix(numpy.ravel( _HX )).T
            _Innovation = Y - _HX
            Jb  = 0.
            Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
            J   = Jb + Jo
            if self._parameters["StoreInternalVariables"] or \
                "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                self.StoredVariables["CurrentState"].store( _X )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            #
            return numpy.ravel( RdemiI*_Innovation )
        #
        def GradientOfCostFunctionLM(x):
            _X      = numpy.asmatrix(numpy.ravel( x )).T
            _HX     = Hm( _X )
            _HX     = numpy.asmatrix(numpy.ravel( _HX )).T
            GradJb  = 0.
            GradJo  = - Ha( (_X, RI * (Y - _HX)) )
            GradJ   = numpy.asmatrix( numpy.ravel( GradJb ) + numpy.ravel( GradJo ) ).T
            return - RdemiI*HO["Tangent"].asMatrix( _X )
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        Xini = numpy.ravel(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = self.StoredVariables["CostFunctionJ"].stepnumber()
        #
        if self._parameters["Minimizer"] == "LBFGSB":
            # Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
            import lbfgsbhlt
            Minimum, J_optimal, Informations = lbfgsbhlt.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = self._parameters["Bounds"],
                maxfun      = self._parameters["MaximumNumberOfSteps"]-1,
                factr       = self._parameters["CostDecrementTolerance"]*1.e14,
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                iprint      = self._parameters["optiprint"],
                )
            nfeval = Informations['funcalls']
            rc     = Informations['warnflag']
        elif self._parameters["Minimizer"] == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = self._parameters["Bounds"],
                maxfun      = self._parameters["MaximumNumberOfSteps"],
                pgtol       = self._parameters["ProjectedGradientTolerance"],
                ftol        = self._parameters["CostDecrementTolerance"],
                messages    = self._parameters["optmessages"],
                )
        elif self._parameters["Minimizer"] == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                disp        = self._parameters["optdisp"],
                full_output = True,
                )
        elif self._parameters["Minimizer"] == "NCG":
            Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                avextol     = self._parameters["CostDecrementTolerance"],
                disp        = self._parameters["optdisp"],
                full_output = True,
                )
        elif self._parameters["Minimizer"] == "BFGS":
            Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
                f           = CostFunction,
                x0          = Xini,
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                disp        = self._parameters["optdisp"],
                full_output = True,
                )
        elif self._parameters["Minimizer"] == "LM":
            Minimum, cov_x, infodict, mesg, rc = scipy.optimize.leastsq(
                func        = CostFunctionLM,
                x0          = Xini,
                Dfun        = GradientOfCostFunctionLM,
                args        = (),
                ftol        = self._parameters["CostDecrementTolerance"],
                maxfev      = self._parameters["MaximumNumberOfSteps"],
                gtol        = self._parameters["GradientNormTolerance"],
                full_output = True,
                )
            nfeval = infodict['nfev']
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = self.StoredVariables["CostFunctionJ"][IndexMin]
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        # ----------------------------------------------------------------
        if self._parameters["StoreInternalVariables"] or "CurrentState" in self._parameters["StoreSupplementaryCalculations"]:
            Minimum = self.StoredVariables["CurrentState"][IndexMin]
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( Minimum )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        if "OMA"                           in self._parameters["StoreSupplementaryCalculations"] or \
           "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            if "SimulatedObservationAtCurrentState" in self._parameters["StoreSupplementaryCalculations"]:
                HXa = self.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
            elif "SimulatedObservationAtCurrentOptimum" in self._parameters["StoreSupplementaryCalculations"]:
                HXa = self.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
            else:
                HXa = Hm(Xa)
        #
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"] or \
            "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            d  = Y - HXb
        if "Innovation" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["Innovation"].store( numpy.ravel(d) )
        if "BMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        if "OMA" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
        if "OMB" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["OMB"].store( numpy.ravel(d) )
        if "SimulatedObservationAtBackground" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
        if "SimulatedObservationAtOptimum" in self._parameters["StoreSupplementaryCalculations"]:
            self.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')
