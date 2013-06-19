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
    Définit les versions approximées des opérateurs tangents et adjoints.
"""
__author__ = "Jean-Philippe ARGAUD"

import os, numpy, time
import logging
# logging.getLogger().setLevel(logging.DEBUG)

# ==============================================================================
class FDApproximation:
    """
    Cette classe sert d'interface pour définir les opérateurs approximés. A la
    création d'un objet, en fournissant une fonction "Function", on obtient un
    objet qui dispose de 3 méthodes "DirectOperator", "TangentOperator" et
    "AdjointOperator". On contrôle l'approximation DF avec l'incrément
    multiplicatif "increment" valant par défaut 1%, ou avec l'incrément fixe
    "dX" qui sera multiplié par "increment" (donc en %), et on effectue de DF
    centrées si le booléen "centeredDF" est vrai.
    """
    def __init__(self,
            Function              = None,
            centeredDF            = False,
            increment             = 0.01,
            dX                    = None,
            avoidingRedundancy    = True,
            toleranceInRedundancy = 1.e-15,
            lenghtOfRedundancy    = -1,
            ):
        self.__userFunction = Function
        self.__centeredDF = bool(centeredDF)
        if avoidingRedundancy:
            self.__avoidRC = True
            self.__tolerBP = float(toleranceInRedundancy)
            self.__lenghtR = int(lenghtOfRedundancy)
            self.__listDPCP = [] # Direct Operator Previous Calculated Points
            self.__listDPCR = [] # Direct Operator Previous Calculated Results
            self.__listDPCN = [] # Direct Operator Previous Calculated Point Norms
            self.__listJPCP = [] # Jacobian Previous Calculated Points
            self.__listJPCI = [] # Jacobian Previous Calculated Increment
            self.__listJPCR = [] # Jacobian Previous Calculated Results
            self.__listJPPN = [] # Jacobian Previous Calculated Point Norms
            self.__listJPIN = [] # Jacobian Previous Calculated Increment Norms
        else:
            self.__avoidRC = False
        if float(increment) <> 0.:
            self.__increment  = float(increment)
        else:
            self.__increment  = 0.01
        if dX is None:  
            self.__dX     = None
        else:
            self.__dX     = numpy.asmatrix(numpy.ravel( dX )).T
        logging.debug("FDA Reduction des doublons de calcul : %s"%self.__avoidRC)
        if self.__avoidRC:
            logging.debug("FDA Tolerance de determination des doublons : %.2e"%self.__tolerBP)

    # ---------------------------------------------------------
    def __doublon__(self, e, l, n, v=""):
        __ac, __i = False, -1
        for i in xrange(len(l)-1,-1,-1):
            if numpy.linalg.norm(e - l[i]) < self.__tolerBP * n[i]:
                __ac, __i = True, i
                if v is not None: logging.debug("FDA Cas%s déja calculé, récupération du doublon"%v)
                break
        return __ac, __i

    # ---------------------------------------------------------
    def DirectOperator(self, X ):
        """
        Calcul du direct à l'aide de la fonction fournie.
        """
        _X = numpy.asmatrix(numpy.ravel( X )).T
        #
        __alreadyCalculated = False
        if self.__avoidRC:
            __alreadyCalculated, __i = self.__doublon__(_X, self.__listDPCP, self.__listDPCN, " H")
        #
        if __alreadyCalculated:
            logging.debug("FDA Calcul DirectOperator (par récupération)")
            _HX = self.__listDPCR[__i]
        else:
            logging.debug("FDA Calcul DirectOperator (explicite)")
            _HX  = self.__userFunction( _X )
            if self.__avoidRC:
                if self.__lenghtR < 0: self.__lenghtR = 2 * _X.size
                if len(self.__listDPCP) > self.__lenghtR:
                    self.__listDPCP.pop(0)
                    self.__listDPCR.pop(0)
                    self.__listDPCN.pop(0)
                self.__listDPCP.append( _X )
                self.__listDPCR.append( _HX )
                self.__listDPCN.append( numpy.linalg.norm(_X) )
        #
        return numpy.ravel( _HX )

    # ---------------------------------------------------------
    def TangentMatrix(self, X ):
        """
        Calcul de l'opérateur tangent comme la Jacobienne par différences finies,
        c'est-à-dire le gradient de H en X. On utilise des différences finies
        directionnelles autour du point X. X est un numpy.matrix.
        
        Différences finies centrées (approximation d'ordre 2):
        1/ Pour chaque composante i de X, on ajoute et on enlève la perturbation
           dX[i] à la  composante X[i], pour composer X_plus_dXi et X_moins_dXi, et
           on calcule les réponses HX_plus_dXi = H( X_plus_dXi ) et HX_moins_dXi =
           H( X_moins_dXi )
        2/ On effectue les différences (HX_plus_dXi-HX_moins_dXi) et on divise par
           le pas 2*dXi
        3/ Chaque résultat, par composante, devient une colonne de la Jacobienne
        
        Différences finies non centrées (approximation d'ordre 1):
        1/ Pour chaque composante i de X, on ajoute la perturbation dX[i] à la 
           composante X[i] pour composer X_plus_dXi, et on calcule la réponse
           HX_plus_dXi = H( X_plus_dXi )
        2/ On calcule la valeur centrale HX = H(X)
        3/ On effectue les différences (HX_plus_dXi-HX) et on divise par
           le pas dXi
        4/ Chaque résultat, par composante, devient une colonne de la Jacobienne
        
        """
        logging.debug("FDA Calcul de la Jacobienne")
        logging.debug("FDA   Incrément de............: %s*X"%float(self.__increment))
        logging.debug("FDA   Approximation centrée...: %s"%(self.__centeredDF))
        #
        if X is None or len(X)==0:
            raise ValueError("Nominal point X for approximate derivatives can not be None or void.")
        #
        _X = numpy.asmatrix(numpy.ravel( X )).T
        #
        if self.__dX is None:
            _dX  = self.__increment * _X
        else:
            _dX = numpy.asmatrix(numpy.ravel( self.__dX )).T
        #
        if (_dX == 0.).any():
            moyenne = _dX.mean()
            if moyenne == 0.:
                _dX = numpy.where( _dX == 0., float(self.__increment), _dX )
            else:
                _dX = numpy.where( _dX == 0., moyenne, _dX )
        #
        __alreadyCalculated  = False
        if self.__avoidRC:
            __bidon, __alreadyCalculatedP = self.__doublon__(_X,  self.__listJPCP, self.__listJPPN, None)
            __bidon, __alreadyCalculatedI = self.__doublon__(_dX, self.__listJPCI, self.__listJPIN, None)
            if __alreadyCalculatedP == __alreadyCalculatedI > -1:
                __alreadyCalculated, __i = True, __alreadyCalculatedP
        #
        if __alreadyCalculated:
            logging.debug("FDA   Calcul Jacobienne (par récupération)")
            _Jacobienne = self.__listJPCR[__i]
        else:
            logging.debug("FDA   Calcul Jacobienne (explicite)")
            if self.__centeredDF:
                #
                _Jacobienne  = []
                for i in range( _dX.size ):
                    _dXi            = _dX[i]
                    _X_plus_dXi     = numpy.array( _X.A1, dtype=float )
                    _X_plus_dXi[i]  = _X[i] + _dXi
                    _X_moins_dXi    = numpy.array( _X.A1, dtype=float )
                    _X_moins_dXi[i] = _X[i] - _dXi
                    #
                    _HX_plus_dXi    = self.DirectOperator( _X_plus_dXi )
                    _HX_moins_dXi   = self.DirectOperator( _X_moins_dXi )
                    #
                    _Jacobienne.append( numpy.ravel( _HX_plus_dXi - _HX_moins_dXi ) / (2.*_dXi) )
                #
            else:
                #
                _Jacobienne  = []
                _HX = self.DirectOperator( _X )
                for i in range( _dX.size ):
                    _dXi            = _dX[i]
                    _X_plus_dXi     = numpy.array( _X.A1, dtype=float )
                    _X_plus_dXi[i]  = _X[i] + _dXi
                    #
                    _HX_plus_dXi = self.DirectOperator( _X_plus_dXi )
                    #
                    _Jacobienne.append( numpy.ravel(( _HX_plus_dXi - _HX ) / _dXi) )
                #
            #
            _Jacobienne = numpy.matrix( numpy.vstack( _Jacobienne ) ).T
            if self.__avoidRC:
                if self.__lenghtR < 0: self.__lenghtR = 2 * _X.size
                if len(self.__listJPCP) > self.__lenghtR:
                    self.__listJPCP.pop(0)
                    self.__listJPCI.pop(0)
                    self.__listJPCR.pop(0)
                    self.__listJPPN.pop(0)
                    self.__listJPIN.pop(0)
                self.__listJPCP.append( _X )
                self.__listJPCI.append( _dX )
                self.__listJPCR.append( _Jacobienne )
                self.__listJPPN.append( numpy.linalg.norm(_X) )
                self.__listJPIN.append( numpy.linalg.norm(_Jacobienne) )
        #
        logging.debug("FDA Fin du calcul de la Jacobienne")
        #
        return _Jacobienne

    # ---------------------------------------------------------
    def TangentOperator(self, (X, dX) ):
        """
        Calcul du tangent à l'aide de la Jacobienne.
        """
        _Jacobienne = self.TangentMatrix( X )
        if dX is None or len(dX) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            return _Jacobienne
        else:
            #
            # Calcul de la valeur linéarisée de H en X appliqué à dX
            # ------------------------------------------------------
            _dX = numpy.asmatrix(numpy.ravel( dX )).T
            _HtX = numpy.dot(_Jacobienne, _dX)
            return _HtX.A1

    # ---------------------------------------------------------
    def AdjointOperator(self, (X, Y) ):
        """
        Calcul de l'adjoint à l'aide de la Jacobienne.
        """
        _JacobienneT = self.TangentMatrix( X ).T
        if Y is None or len(Y) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            return _JacobienneT
        else:
            #
            # Calcul de la valeur de l'adjoint en X appliqué à Y
            # --------------------------------------------------
            _Y = numpy.asmatrix(numpy.ravel( Y )).T
            _HaY = numpy.dot(_JacobienneT, _Y)
            return _HaY.A1

# ==============================================================================
#
def test1( XX ):
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
 
    FDA = FDApproximation( test1 )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(3,3+2*len(X0))) )
    print
    del FDA
    FDA = FDApproximation( test1, centeredDF=True )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(3,3+2*len(X0))) )
    print
    del FDA

    print "=============="
    print
    X0 = range(5)
 
    FDA = FDApproximation( test1 )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(7,7+2*len(X0))) )
    print
    del FDA
    FDA = FDApproximation( test1, centeredDF=True )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(7,7+2*len(X0))) )
    print
    del FDA

    print "=============="
    print
    X0 = numpy.arange(3)
 
    FDA = FDApproximation( test1 )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(7,7+2*len(X0))) )
    print
    del FDA
    FDA = FDApproximation( test1, centeredDF=True )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(7,7+2*len(X0))) )
    print
    del FDA

    print "=============="
    print
    X0 = numpy.asmatrix(numpy.arange(4)).T
 
    FDA = FDApproximation( test1 )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(7,7+2*len(X0))) )
    print
    del FDA
    FDA = FDApproximation( test1, centeredDF=True )
    print "H(X)       =",   FDA.DirectOperator( X0 )
    print "Tg matrice =\n", FDA.TangentMatrix( X0 )
    print "Tg(X)      =",   FDA.TangentOperator( (X0, X0) )
    print "Ad((X,Y))  =",   FDA.AdjointOperator( (X0,range(7,7+2*len(X0))) )
    print
    del FDA

