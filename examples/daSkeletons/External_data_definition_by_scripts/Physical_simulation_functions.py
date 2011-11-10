#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2011  EDF R&D
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
# ==============================================================================
#
import os, numpy, time
#
def FunctionH( XX ):
    """ Direct non-linear simulation operator """
    #
    # NEED TO BE COMPLETED
    # NEED TO BE COMPLETED
    # NEED TO BE COMPLETED
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

# ==============================================================================
def TangentH( X, increment = 0.01, centeredDF = False ):
    """
    Calcul de l'opérateur tangent comme la Jacobienne par différences finies,
    c'est-à-dire le gradient de H en X. On utilise des différences finies
    directionnelles autour du point X.
    
    Différences finies centrées :
    1/ Pour chaque composante i de X, on ajoute et on enlève la perturbation
       dX[i] à la  composante X[i], pour composer X_plus_dXi et X_moins_dXi, et
       on calcule les réponses HX_plus_dXi = H( X_plus_dXi ) et HX_moins_dXi =
       H( X_moins_dXi )
    2/ On effectue les différences (HX_plus_dXi-HX_moins_dXi) et on divise par
       le pas 2*dXi
    3/ Chaque résultat, par composante, devient une colonne de la Jacobienne
    
    Différences finies non centrées :
    1/ Pour chaque composante i de X, on ajoute la perturbation dX[i] à la 
       composante X[i] pour composer X_plus_dXi, et on calcule la réponse
       HX_plus_dXi = H( X_plus_dXi )
    2/ On calcule la valeur centrale HX = H(X)
    3/ On effectue les différences (HX_plus_dXi-HX) et on divise par
       le pas dXi
    4/ Chaque résultat, par composante, devient une colonne de la Jacobienne
    
    """
    print
    print "  == Calcul de la Jacobienne avec un incrément de %s*X"%increment
    #
    dX  = increment * X.A1
    #
    if centeredDF:
        #
        # Boucle de calcul des colonnes de la Jacobienne
        # ----------------------------------------------
        Jacobienne  = []
        for i in range( len(dX) ):
            X_plus_dXi     = X.A1
            X_plus_dXi[i]  = X[i] + dX[i]
            X_moins_dXi    = X.A1
            X_moins_dXi[i] = X[i] - dX[i]
            #
            HX_plus_dXi  = FunctionH( X_plus_dXi )
            HX_moins_dXi = FunctionH( X_moins_dXi )
            #
            HX_Diff = ( HX_plus_dXi - HX_moins_dXi ) / (2.*dX[i])
            #
            Jacobienne.append( HX_Diff )
        #
    else:
        #
        # Boucle de calcul des colonnes de la Jacobienne
        # ----------------------------------------------
        HX_plus_dX = []
        for i in range( len(dX) ):
            X_plus_dXi    = X.A1
            X_plus_dXi[i] = X[i] + dX[i]
            #
            HX_plus_dXi = FunctionH( X_plus_dXi )
            #
            HX_plus_dX.append( HX_plus_dXi )
        #
        # Calcul de la valeur centrale
        # ----------------------------
        HX = FunctionH( X )
        #
        # Calcul effectif de la Jacobienne par différences finies
        # -------------------------------------------------------
        Jacobienne = []
        for i in range( len(dX) ):
            Jacobienne.append( ( HX_plus_dX[i] - HX ) / dX[i] )
    #
    Jacobienne = numpy.matrix( Jacobienne )
    print
    print "  == Fin du calcul de la Jacobienne"
    #
    return Jacobienne

# ==============================================================================
def AdjointH( (X, Y) ):
    """
    Calcul de l'adjoint à l'aide de la Jacobienne.
    """
    Jacobienne = TangentH( X, centeredDF = False )
    #
    # Calcul de la valeur de l'adjoint en X appliqué à Y
    # --------------------------------------------------
    Y = numpy.asmatrix(Y).flatten().T
    HtY = numpy.dot(Jacobienne, Y)
    #
    return HtY.A1

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
