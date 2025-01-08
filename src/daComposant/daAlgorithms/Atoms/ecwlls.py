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
    Linear Least Squares
"""
__author__ = "Jean-Philippe ARGAUD"

from daCore.PlatformInfo import vfloat

# ==============================================================================
def ecwlls(selfA, Xb, Y, U, HO, CM, R, B, __storeState = False):
    """
    Correction
    """
    #
    # Initialisations
    # ---------------
    Hm = HO["Tangent"].asMatrix(Xb)
    Hm = Hm.reshape(Y.size, -1)  # ADAO & check shape
    Ha = HO["Adjoint"].asMatrix(Xb)
    Ha = Ha.reshape(-1, Y.size)  # ADAO & check shape
    #
    if R is None:
        RI = 1.
    else:
        RI = R.getI()
    #
    # Calcul de l'analyse
    # -------------------
    K = (Ha * (RI * Hm)).I * Ha * RI
    Xa = K * Y
    #
    if __storeState:
        selfA._setInternalState("Xn", Xa)
    # --------------------------
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    # Calcul de la fonction coût
    # --------------------------
    if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CostFunctionJ" ) or selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJb") or selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJo") or selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("OMA") or \
            selfA._toStore("InnovationAtCurrentAnalysis") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtOptimum"):
        HXa = Hm @ Xa
        oma = Y - HXa.reshape((-1, 1))
    if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CostFunctionJ" ) or selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJb") or selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJo") or selfA._toStore("CostFunctionJoAtCurrentOptimum"):
        Jb  = 0.
        Jo  = vfloat( 0.5 * oma.T * (RI * oma) )
        J   = Jb + Jo
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( Jb )
        selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( Jo )
        selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( J )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        selfA.StoredVariables["CurrentState"].store( Xa )
    if selfA._toStore("CurrentOptimum"):
        selfA.StoredVariables["CurrentOptimum"].store( Xa )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( oma )
    if selfA._toStore("InnovationAtCurrentAnalysis"):
        selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( oma )
    if selfA._toStore("SimulatedObservationAtCurrentState"):
        selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HXa )
    if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
        selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( HXa )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( HXa )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
