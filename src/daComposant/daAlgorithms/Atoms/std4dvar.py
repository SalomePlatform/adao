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

__doc__ = """
    4DVAR
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy, scipy, scipy.optimize, scipy.version
from daCore.NumericObjects import ForceNumericBounds, ApplyBounds
from daCore.PlatformInfo import PlatformInfo, vt, vfloat, trmo
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()

# ==============================================================================
def std4dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    Correction
    """
    #
    # Initialisations
    # ---------------
    #
    # Opérateurs
    Hm = HO["Direct"].appliedControledFormTo
    Mm = EM["Direct"].appliedControledFormTo
    #
    if CM is not None and "Tangent" in CM and U is not None:
        Cm = CM["Tangent"].asMatrix(Xb)
    else:
        Cm = None

    def Un(_step):
        if U is not None:
            if hasattr(U, "store") and 1 <= _step < len(U):
                _Un = numpy.ravel( U[_step] ).reshape((-1, 1))
            elif hasattr(U, "store") and len(U) == 1:
                _Un = numpy.ravel( U[0] ).reshape((-1, 1))
            else:
                _Un = numpy.ravel( U ).reshape((-1, 1))
        else:
            _Un = None
        return _Un

    def CmUn(_xn, _un):
        if Cm is not None and _un is not None:  # Attention : si Cm est aussi dans M, doublon !
            _Cm   = Cm.reshape(_xn.size, _un.size)  # ADAO & check shape
            _CmUn = (_Cm @ _un).reshape((-1, 1))
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
    if hasattr(Y, "stepnumber"):
        duration = Y.stepnumber()
    else:
        duration = 2
    #
    # Précalcul des inversions de B et R
    BI = B.getI()
    RI = R.getI()
    #
    # Point de démarrage de l'optimisation
    Xini = selfA._parameters["InitializationPoint"]
    #
    # Définition de la fonction-coût
    # ------------------------------
    selfA.DirectCalculation = [None,]  # Le pas 0 n'est pas observé
    selfA.DirectInnovation  = [None,]  # Le pas 0 n'est pas observé

    def CostFunction(x):
        _X  = numpy.asarray(x).reshape((-1, 1))
        if selfA._parameters["StoreInternalVariables"] or \
                selfA._toStore("CurrentState") or \
                selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( _X )
        Jb  = vfloat( 0.5 * (_X - Xb).T * (BI * (_X - Xb)) )
        selfA.DirectCalculation = [None,]
        selfA.DirectInnovation  = [None,]
        Jo  = 0.
        _Xn = _X
        for step in range(0, duration - 1):
            if hasattr(Y, "store"):
                _Ynpu = numpy.ravel( Y[step + 1] ).reshape((-1, 1))
            else:
                _Ynpu = numpy.ravel( Y ).reshape((-1, 1))
            _Un = Un(step)
            #
            # Etape d'évolution
            if selfA._parameters["EstimationOf"] == "State":
                _Xn = Mm( (_Xn, _Un) ).reshape((-1, 1)) + CmUn(_Xn, _Un)
            elif selfA._parameters["EstimationOf"] == "Parameters":
                pass
            #
            if selfA._parameters["Bounds"] is not None and selfA._parameters["ConstrainedBy"] == "EstimateProjection":
                _Xn = ApplyBounds( _Xn, ForceNumericBounds(selfA._parameters["Bounds"]) )
            #
            # Etape de différence aux observations
            if selfA._parameters["EstimationOf"] == "State":
                _YmHMX = _Ynpu - numpy.ravel( Hm( (_Xn, None) ) ).reshape((-1, 1))
            elif selfA._parameters["EstimationOf"] == "Parameters":
                _YmHMX = _Ynpu - numpy.ravel( Hm( (_Xn, None) ) ).reshape((-1, 1)) - CmUn(_Xn, _Un)
            #
            # Stockage de l'état
            selfA.DirectCalculation.append( _Xn )
            selfA.DirectInnovation.append( _YmHMX )
            #
            # Ajout dans la fonctionnelle d'observation
            Jo = Jo + 0.5 * vfloat( _YmHMX.T * (RI * _YmHMX) )
        J = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
                selfA._toStore("CurrentOptimum") or \
                selfA._toStore("CostFunctionJAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )  # noqa: E501
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )  # noqa: E501
        return J

    def GradientOfCostFunction(x):
        _X      = numpy.asarray(x).reshape((-1, 1))
        GradJb  = BI * (_X - Xb)
        GradJo  = 0.
        for step in range(duration - 1, 0, -1):
            # Étape de récupération du dernier stockage de l'évolution
            _Xn = selfA.DirectCalculation.pop()
            # Étape de récupération du dernier stockage de l'innovation
            _YmHMX = selfA.DirectInnovation.pop()
            # Calcul des adjoints
            Ha = HO["Adjoint"].asMatrix(ValueForMethodForm = _Xn)
            Ha = Ha.reshape(_Xn.size, _YmHMX.size)  # ADAO & check shape
            Ma = EM["Adjoint"].asMatrix(ValueForMethodForm = _Xn)
            Ma = Ma.reshape(_Xn.size, _Xn.size)  # ADAO & check shape
            # Calcul du gradient par état adjoint
            GradJo = GradJo + Ha * (RI * _YmHMX)  # Équivaut pour Ha linéaire à : Ha( (_Xn, RI * _YmHMX) )
            GradJo = Ma * GradJo                  # Équivaut pour Ma linéaire à : Ma( (_Xn, GradJo) )
        GradJ = numpy.ravel( GradJb ) - numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        optimiseur = trmo()
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfIterations"] - 1,
            factr       = selfA._parameters["CostDecrementTolerance"] * 1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
        )
        # nfeval = Informations['funcalls']
        # rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfIterations"],
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            ftol        = selfA._parameters["CostDecrementTolerance"],
            messages    = selfA._parameters["optmessages"],
        )
    elif selfA._parameters["Minimizer"] == "CG":
        Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
        )
    elif selfA._parameters["Minimizer"] == "NCG":
        Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"],
            avextol     = selfA._parameters["CostDecrementTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
        )
    elif selfA._parameters["Minimizer"] == "BFGS":
        Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
            f           = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            maxiter     = selfA._parameters["MaximumNumberOfIterations"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
        )
    else:
        raise ValueError("Error in minimizer name: %s is unkown"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = Minimum
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
