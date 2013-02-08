#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2013 EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

__doc__ = """
    ADAO skeleton case, for wide script usage in case definition
    ------------------------------------------------------------

    External definition of the physical simulation operator, its tangent and
    its adjoint form. In case adjoint is not known, a finite difference version
    is given by default in this skeleton.
    """
__author__ = "Jean-Philippe ARGAUD"
#
import os, numpy, time
#
# ==============================================================================
#
def FunctionH( XX ):
    """ Direct non-linear simulation operator """
    #
    # --------------------------------------> EXAMPLE TO BE REMOVED
    if type(XX) is type(numpy.matrix([])):  # EXAMPLE TO BE REMOVED
        HX = XX.A1.tolist()                 # EXAMPLE TO BE REMOVED
    elif type(XX) is type(numpy.array([])): # EXAMPLE TO BE REMOVED
        HX = numpy.matrix(XX).A1.tolist()   # EXAMPLE TO BE REMOVED
    else:                                   # EXAMPLE TO BE REMOVED
        HX = XX                             # EXAMPLE TO BE REMOVED
    # --------------------------------------> EXAMPLE TO BE REMOVED
    #
    return numpy.array( HX )
#
def TangentHMatrix( X, increment = 0.01, centeredDF = False ):
    """ Tangent operator (Jacobian) calculated by finite differences """
    #
    dX  = increment * X.A1
    #
    if centeredDF:
        # 
        Jacobian  = []
        for i in range( len(dX) ):
            X_plus_dXi     = numpy.array( X.A1 )
            X_plus_dXi[i]  = X[i] + dX[i]
            X_moins_dXi    = numpy.array( X.A1 )
            X_moins_dXi[i] = X[i] - dX[i]
            #
            HX_plus_dXi  = FunctionH( X_plus_dXi )
            HX_moins_dXi = FunctionH( X_moins_dXi )
            #
            HX_Diff = ( HX_plus_dXi - HX_moins_dXi ) / (2.*dX[i])
            #
            Jacobian.append( HX_Diff )
        #
    else:
        #
        HX_plus_dX = []
        for i in range( len(dX) ):
            X_plus_dXi    = numpy.array( X.A1 )
            X_plus_dXi[i] = X[i] + dX[i]
            #
            HX_plus_dXi = FunctionH( X_plus_dXi )
            #
            HX_plus_dX.append( HX_plus_dXi )
        #
        HX = FunctionH( X )
        #
        Jacobian = []
        for i in range( len(dX) ):
            Jacobian.append( ( HX_plus_dX[i] - HX ) / dX[i] )
    #
    Jacobian = numpy.matrix( Jacobian )
    #
    return Jacobian
#
def TangentH( X ):
    """ Tangent operator """
    _X = numpy.asmatrix(X).flatten().T
    HtX = self.TangentHMatrix( _X ) * _X
    return HtX.A1
#
def AdjointH( (X, Y) ):
    """ Ajoint operator """
    #
    Jacobian = TangentHMatrix( X, centeredDF = False )
    #
    Y = numpy.asmatrix(Y).flatten().T
    HaY = numpy.dot(Jacobian, Y)
    #
    return HaY.A1

# ==============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    from Physical_data_and_covariance_matrices import True_state
    X0, noms = True_state()
 
    FX = FunctionH( X0 )
    print "FX =", FX
    print
