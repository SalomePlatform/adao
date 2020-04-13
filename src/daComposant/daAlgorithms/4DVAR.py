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
import numpy, scipy.optimize, scipy.version

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "4DVAR")
        self.defineRequiredParameter(
            name     = "ConstrainedBy",
            default  = "EstimateProjection",
            typecast = str,
            message  = "Prise en compte des contraintes",
            listval  = ["EstimateProjection"],
            )
        self.defineRequiredParameter(
            name     = "EstimationOf",
            default  = "State",
            typecast = str,
            message  = "Estimation d'etat ou de parametres",
            listval  = ["State", "Parameters"],
            )
        self.defineRequiredParameter(
            name     = "Minimizer",
            default  = "LBFGSB",
            typecast = str,
            message  = "Minimiseur utilisé",
            listval  = ["LBFGSB","TNC", "CG", "NCG", "BFGS"],
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
            minval   = 0.,
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
            minval   = 0.,
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
                "BMA",
                "CostFunctionJ",
                "CostFunctionJAtCurrentOptimum",
                "CostFunctionJb",
                "CostFunctionJbAtCurrentOptimum",
                "CostFunctionJo",
                "CostFunctionJoAtCurrentOptimum",
                "CurrentOptimum",
                "CurrentState",
                "IndexOfOptimum",
                ]
            )
        self.defineRequiredParameter( # Pas de type
            name     = "Bounds",
            message  = "Liste des valeurs de bornes",
            )
        self.requireInputArguments(
            mandatory= ("Xb", "Y", "HO", "EM", "R", "B" ),
            optional = ("U", "CM"),
            )
        self.setAttributes(tags=(
            "DataAssimilation",
            "NonLinear",
            "Variational",
            "Dynamic",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        if "Minimizer" in self._parameters and self._parameters["Minimizer"] == "TNC":
            self.setParameterValue("StoreInternalVariables",True)
        #
        # Opérateurs
        # ----------
        Hm = HO["Direct"].appliedControledFormTo
        #
        Mm = EM["Direct"].appliedControledFormTo
        #
        if CM is not None and "Tangent" in CM and U is not None:
            Cm = CM["Tangent"].asMatrix(Xb)
        else:
            Cm = None
        #
        def Un(_step):
            if U is not None:
                if hasattr(U,"store") and 1<=_step<len(U) :
                    _Un = numpy.asmatrix(numpy.ravel( U[_step] )).T
                elif hasattr(U,"store") and len(U)==1:
                    _Un = numpy.asmatrix(numpy.ravel( U[0] )).T
                else:
                    _Un = numpy.asmatrix(numpy.ravel( U )).T
            else:
                _Un = None
            return _Un
        def CmUn(_xn,_un):
            if Cm is not None and _un is not None: # Attention : si Cm est aussi dans M, doublon !
                _Cm   = Cm.reshape(_xn.size,_un.size) # ADAO & check shape
                _CmUn = _Cm * _un
            else:
                _CmUn = 0.
            return _CmUn
        #
        # Remarque : les observations sont exploitées à partir du pas de temps
        # numéro 1, et sont utilisées dans Yo comme rangées selon ces indices.
        # Donc le pas 0 n'est pas utilisé puisque la première étape commence
        # avec l'observation du pas 1.
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
        BI = B.getI()
        RI = R.getI()
        #
        # Définition de la fonction-coût
        # ------------------------------
        self.DirectCalculation = [None,] # Le pas 0 n'est pas observé
        self.DirectInnovation  = [None,] # Le pas 0 n'est pas observé
        def CostFunction(x):
            _X  = numpy.asmatrix(numpy.ravel( x )).T
            if self._parameters["StoreInternalVariables"] or \
                self._toStore("CurrentState") or \
                self._toStore("CurrentOptimum"):
                self.StoredVariables["CurrentState"].store( _X )
            Jb  = 0.5 * (_X - Xb).T * BI * (_X - Xb)
            self.DirectCalculation = [None,]
            self.DirectInnovation  = [None,]
            Jo  = 0.
            _Xn = _X
            for step in range(0,duration-1):
                self.DirectCalculation.append( _Xn )
                if hasattr(Y,"store"):
                    _Ynpu = numpy.asmatrix(numpy.ravel( Y[step+1] )).T
                else:
                    _Ynpu = numpy.asmatrix(numpy.ravel( Y )).T
                _Un = Un(step)
                #
                # Etape d'évolution
                if self._parameters["EstimationOf"] == "State":
                    _Xn = Mm( (_Xn, _Un) ) + CmUn(_Xn, _Un)
                elif self._parameters["EstimationOf"] == "Parameters":
                    pass
                #
                if self._parameters["Bounds"] is not None and self._parameters["ConstrainedBy"] == "EstimateProjection":
                    _Xn = numpy.max(numpy.hstack((_Xn,numpy.asmatrix(self._parameters["Bounds"])[:,0])),axis=1)
                    _Xn = numpy.min(numpy.hstack((_Xn,numpy.asmatrix(self._parameters["Bounds"])[:,1])),axis=1)
                #
                # Etape de différence aux observations
                if self._parameters["EstimationOf"] == "State":
                    _YmHMX = _Ynpu - numpy.asmatrix(numpy.ravel( Hm( (_Xn, None) ) )).T
                elif self._parameters["EstimationOf"] == "Parameters":
                    _YmHMX = _Ynpu - numpy.asmatrix(numpy.ravel( Hm( (_Xn, _Un) ) )).T - CmUn(_Xn, _Un)
                self.DirectInnovation.append( _YmHMX )
                # Ajout dans la fonctionnelle d'observation
                Jo = Jo + _YmHMX.T * RI * _YmHMX
            Jo  = 0.5 * Jo
            J   = float( Jb ) + float( Jo )
            self.StoredVariables["CostFunctionJb"].store( Jb )
            self.StoredVariables["CostFunctionJo"].store( Jo )
            self.StoredVariables["CostFunctionJ" ].store( J )
            if self._toStore("IndexOfOptimum") or \
                self._toStore("CurrentOptimum") or \
                self._toStore("CostFunctionJAtCurrentOptimum") or \
                self._toStore("CostFunctionJbAtCurrentOptimum") or \
                self._toStore("CostFunctionJoAtCurrentOptimum"):
                IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if self._toStore("IndexOfOptimum"):
                self.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if self._toStore("CurrentOptimum"):
                self.StoredVariables["CurrentOptimum"].store( self.StoredVariables["CurrentState"][IndexMin] )
            if self._toStore("CostFunctionJAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( self.StoredVariables["CostFunctionJ" ][IndexMin] )
            if self._toStore("CostFunctionJbAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJb"][IndexMin] )
            if self._toStore("CostFunctionJoAtCurrentOptimum"):
                self.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( self.StoredVariables["CostFunctionJo"][IndexMin] )
            return J
        #
        def GradientOfCostFunction(x):
            _X      = numpy.asmatrix(numpy.ravel( x )).T
            GradJb  = BI * (_X - Xb)
            GradJo  = 0.
            for step in range(duration-1,0,-1):
                # Etape de récupération du dernier stockage de l'évolution
                _Xn = self.DirectCalculation.pop()
                # Etape de récupération du dernier stockage de l'innovation
                _YmHMX = self.DirectInnovation.pop()
                # Calcul des adjoints
                Ha = HO["Adjoint"].asMatrix(ValueForMethodForm = _Xn)
                Ha = Ha.reshape(_Xn.size,_YmHMX.size) # ADAO & check shape
                Ma = EM["Adjoint"].asMatrix(ValueForMethodForm = _Xn)
                Ma = Ma.reshape(_Xn.size,_Xn.size) # ADAO & check shape
                # Calcul du gradient par etat adjoint
                GradJo = GradJo + Ha * RI * _YmHMX # Equivaut pour Ha lineaire à : Ha( (_Xn, RI * _YmHMX) )
                GradJo = Ma * GradJo               # Equivaut pour Ma lineaire à : Ma( (_Xn, GradJo) )
            GradJ   = numpy.asmatrix( numpy.ravel( GradJb ) - numpy.ravel( GradJo ) ).T
            return GradJ.A1
        #
        # Point de démarrage de l'optimisation : Xini = Xb
        # ------------------------------------
        if isinstance(Xb, type(numpy.matrix([]))):
            Xini = Xb.A1.tolist()
        else:
            Xini = list(Xb)
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = self.StoredVariables["CostFunctionJ"].stepnumber()
        #
        if self._parameters["Minimizer"] == "LBFGSB":
            # Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
            if "0.19" <= scipy.version.version <= "1.1.0":
                import lbfgsbhlt as optimiseur
            else:
                import scipy.optimize as optimiseur
            Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
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
        else:
            raise ValueError("Error in Minimizer name: %s"%self._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( self.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = self.StoredVariables["CostFunctionJ"][IndexMin]
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        # ----------------------------------------------------------------
        if self._parameters["StoreInternalVariables"] or self._toStore("CurrentState"):
            Minimum = self.StoredVariables["CurrentState"][IndexMin]
        #
        # Obtention de l'analyse
        # ----------------------
        Xa = numpy.asmatrix(numpy.ravel( Minimum )).T
        #
        self.StoredVariables["Analysis"].store( Xa.A1 )
        #
        # Calculs et/ou stockages supplémentaires
        # ---------------------------------------
        if self._toStore("BMA"):
            self.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
