#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2012 EDF R&D
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
    Définit les versions approximées des opérateurs tangents et adjoints.
"""
__author__ = "Jean-Philippe ARGAUD"

import os, numpy, time
import logging
# logging.getLogger().setLevel(logging.DEBUG)

# ==============================================================================
class FDApproximation:
    """
    Cette classe sert d'interface pour définir les opérateurs approximés. A la
    création d'un objet, en fournissant une fonction "FunctionH", on obtient un
    objet qui dispose de 3 méthodes "FunctionH", "TangentH" et "AdjointH". On
    contrôle l'approximation DF avec l'incrément multiplicatif "increment"
    valant par défaut 1%, ou avec l'incrément fixe "dX" qui sera multiplié par
    "increment" (donc en %), et on effectue de DF centrées si le booléen
    "centeredDF" est vrai.
    """
    def __init__(self, FunctionH = None, centeredDF = False, increment = 0.01, dX = None):
        self.FunctionH    = FunctionH
        self.__centeredDF = bool(centeredDF)
        if float(increment) <> 0.:
            self.__increment  = float(increment)
        else:
            self.__increment  = 0.01
        if dX is None:  
            self.__dX     = None
        else:
            self.__dX     = numpy.asmatrix(dX).flatten().T

    # ---------------------------------------------------------
    def TangentHMatrix(self, X ):
        """
        Calcul de l'opérateur tangent comme la Jacobienne par différences finies,
        c'est-à-dire le gradient de H en X. On utilise des différences finies
        directionnelles autour du point X. X est un numpy.matrix.
        
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
        logging.debug("  == Calcul de la Jacobienne")
        logging.debug("     Incrément de............: %s*X"%float(self.__increment))
        logging.debug("     Approximation centrée...: %s"%(self.__centeredDF))
        #
        _X = numpy.asmatrix(X).flatten().T
        #
        if self.__dX is None:
            _dX  = self.__increment * _X
        else:
            _dX = numpy.asmatrix(self.__dX).flatten().T
        logging.debug("     Incrément non corrigé...: %s"%(_dX))
        #
        if (_dX == 0.).any():
            moyenne = _dX.mean()
            if moyenne == 0.:
                _dX = numpy.where( _dX == 0., float(self.__increment), _dX )
            else:
                _dX = numpy.where( _dX == 0., moyenne, _dX )
        logging.debug("     Incrément dX............: %s"%(_dX))
        #
        if self.__centeredDF:
            #
            # Boucle de calcul des colonnes de la Jacobienne
            # ----------------------------------------------
            Jacobienne  = []
            for i in range( len(_dX) ):
                X_plus_dXi     = numpy.array( _X.A1, dtype=float )
                X_plus_dXi[i]  = _X[i] + _dX[i]
                X_moins_dXi    = numpy.array( _X.A1, dtype=float )
                X_moins_dXi[i] = _X[i] - _dX[i]
                #
                HX_plus_dXi  = self.FunctionH( X_plus_dXi )
                HX_moins_dXi = self.FunctionH( X_moins_dXi )
                #
                HX_Diff = ( HX_plus_dXi - HX_moins_dXi ) / (2.*_dX[i])
                #
                Jacobienne.append( HX_Diff )
            #
        else:
            #
            # Boucle de calcul des colonnes de la Jacobienne
            # ----------------------------------------------
            HX_plus_dX = []
            for i in range( len(_dX) ):
                X_plus_dXi    = numpy.array( _X.A1, dtype=float )
                X_plus_dXi[i] = _X[i] + _dX[i]
                #
                HX_plus_dXi = self.FunctionH( X_plus_dXi )
                #
                HX_plus_dX.append( HX_plus_dXi )
            #
            # Calcul de la valeur centrale
            # ----------------------------
            HX = self.FunctionH( _X )
            #
            # Calcul effectif de la Jacobienne par différences finies
            # -------------------------------------------------------
            Jacobienne = []
            for i in range( len(_dX) ):
                Jacobienne.append( numpy.asmatrix(( HX_plus_dX[i] - HX ) / _dX[i]).flatten().A1 )
        #
        Jacobienne = numpy.matrix( numpy.vstack( Jacobienne ) ).T
        logging.debug("  == Fin du calcul de la Jacobienne")
        #
        return Jacobienne

    # ---------------------------------------------------------
    def TangentH(self, (X, dX) ):
        """
        Calcul du tangent à l'aide de la Jacobienne.
        """
        Jacobienne = self.TangentHMatrix( X )
        if dX is None or len(dX) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            return Jacobienne
        else:
            #
            # Calcul de la valeur linéarisée de H en X appliqué à dX
            # ------------------------------------------------------
            _dX = numpy.asmatrix(dX).flatten().T
            HtX = numpy.dot(Jacobienne, _dX)
            return HtX.A1

    # ---------------------------------------------------------
    def AdjointH(self, (X, Y) ):
        """
        Calcul de l'adjoint à l'aide de la Jacobienne.
        """
        JacobienneT = self.TangentHMatrix( X ).T
        if Y is None or len(Y) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            return JacobienneT
        else:
            #
            # Calcul de la valeur de l'adjoint en X appliqué à Y
            # --------------------------------------------------
            _Y = numpy.asmatrix(Y).flatten().T
            HaY = numpy.dot(JacobienneT, _Y)
            return HaY.A1

# ==============================================================================
#
def test1FunctionH( XX ):
    """ Direct non-linear simulation operator """
    #
    # NEED TO BE COMPLETED
    # NEED TO BE COMPLETED
    # NEED TO BE COMPLETED
    #
    # --------------------------------------> # EXAMPLE TO BE REMOVED
    # Example of Identity operator            # EXAMPLE TO BE REMOVED
    if type(XX) is type(numpy.matrix([])):    # EXAMPLE TO BE REMOVED
        HX = XX.A1.tolist()                   # EXAMPLE TO BE REMOVED
    elif type(XX) is type(numpy.array([])):   # EXAMPLE TO BE REMOVED
        HX = numpy.matrix(XX).A1.tolist()     # EXAMPLE TO BE REMOVED
    else:                                     # EXAMPLE TO BE REMOVED
        HX = XX                               # EXAMPLE TO BE REMOVED
    #                                         # EXAMPLE TO BE REMOVED
    HHX = []                                  # EXAMPLE TO BE REMOVED
    HHX.extend( HX )                          # EXAMPLE TO BE REMOVED
    HHX.extend( HX )                          # EXAMPLE TO BE REMOVED
    # --------------------------------------> # EXAMPLE TO BE REMOVED
    #
    return numpy.array( HHX )

# ==============================================================================
if __name__ == "__main__":

    print
    print "AUTODIAGNOSTIC"
    print "=============="
    
    X0 = [1, 2, 3]
 
    FDA = FDApproximation( test1FunctionH )
    print "H(X)       =",   FDA.FunctionH( X0 )
    print "Tg matrice =\n", FDA.TangentHMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentH( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointH( (X0,range(3,3+2*len(X0))) )
    print
    del FDA
 
    FDA = FDApproximation( test1FunctionH, centeredDF=True )
    print "H(X)       =",   FDA.FunctionH( X0 )
    print "Tg matrice =\n", FDA.TangentHMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentH( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointH( (X0,range(3,3+2*len(X0))) )
    print
    del FDA

    X0 = range(5)
 
    FDA = FDApproximation( test1FunctionH )
    print "H(X)       =",   FDA.FunctionH( X0 )
    print "Tg matrice =\n", FDA.TangentHMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentH( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointH( (X0,range(7,7+2*len(X0))) )
    print
    del FDA
