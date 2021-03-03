# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2021 EDF R&D
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
    Définit les objets numériques génériques.
"""
__author__ = "Jean-Philippe ARGAUD"

import os, time, copy, types, sys, logging
import math, numpy, scipy, scipy.optimize, scipy.version
from daCore.BasicObjects import Operator
from daCore.PlatformInfo import PlatformInfo
mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()
# logging.getLogger().setLevel(logging.DEBUG)

# ==============================================================================
def ExecuteFunction( paire ):
    assert len(paire) == 2, "Incorrect number of arguments"
    X, funcrepr = paire
    __X = numpy.asmatrix(numpy.ravel( X )).T
    __sys_path_tmp = sys.path ; sys.path.insert(0,funcrepr["__userFunction__path"])
    __module = __import__(funcrepr["__userFunction__modl"], globals(), locals(), [])
    __fonction = getattr(__module,funcrepr["__userFunction__name"])
    sys.path = __sys_path_tmp ; del __sys_path_tmp
    __HX  = __fonction( __X )
    return numpy.ravel( __HX )

# ==============================================================================
class FDApproximation(object):
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
            name                  = "FDApproximation",
            Function              = None,
            centeredDF            = False,
            increment             = 0.01,
            dX                    = None,
            avoidingRedundancy    = True,
            toleranceInRedundancy = 1.e-18,
            lenghtOfRedundancy    = -1,
            mpEnabled             = False,
            mpWorkers             = None,
            mfEnabled             = False,
            ):
        self.__name = str(name)
        if mpEnabled:
            try:
                import multiprocessing
                self.__mpEnabled = True
            except ImportError:
                self.__mpEnabled = False
        else:
            self.__mpEnabled = False
        self.__mpWorkers = mpWorkers
        if self.__mpWorkers is not None and self.__mpWorkers < 1:
            self.__mpWorkers = None
        logging.debug("FDA Calculs en multiprocessing : %s (nombre de processus : %s)"%(self.__mpEnabled,self.__mpWorkers))
        #
        if mfEnabled:
            self.__mfEnabled = True
        else:
            self.__mfEnabled = False
        logging.debug("FDA Calculs en multifonctions : %s"%(self.__mfEnabled,))
        #
        if avoidingRedundancy:
            self.__avoidRC = True
            self.__tolerBP = float(toleranceInRedundancy)
            self.__lenghtRJ = int(lenghtOfRedundancy)
            self.__listJPCP = [] # Jacobian Previous Calculated Points
            self.__listJPCI = [] # Jacobian Previous Calculated Increment
            self.__listJPCR = [] # Jacobian Previous Calculated Results
            self.__listJPPN = [] # Jacobian Previous Calculated Point Norms
            self.__listJPIN = [] # Jacobian Previous Calculated Increment Norms
        else:
            self.__avoidRC = False
        #
        if self.__mpEnabled:
            if isinstance(Function,types.FunctionType):
                logging.debug("FDA Calculs en multiprocessing : FunctionType")
                self.__userFunction__name = Function.__name__
                try:
                    mod = os.path.join(Function.__globals__['filepath'],Function.__globals__['filename'])
                except:
                    mod = os.path.abspath(Function.__globals__['__file__'])
                if not os.path.isfile(mod):
                    raise ImportError("No user defined function or method found with the name %s"%(mod,))
                self.__userFunction__modl = os.path.basename(mod).replace('.pyc','').replace('.pyo','').replace('.py','')
                self.__userFunction__path = os.path.dirname(mod)
                del mod
                self.__userOperator = Operator( name = self.__name, fromMethod = Function, avoidingRedundancy = self.__avoidRC, inputAsMultiFunction = self.__mfEnabled )
                self.__userFunction = self.__userOperator.appliedTo # Pour le calcul Direct
            elif isinstance(Function,types.MethodType):
                logging.debug("FDA Calculs en multiprocessing : MethodType")
                self.__userFunction__name = Function.__name__
                try:
                    mod = os.path.join(Function.__globals__['filepath'],Function.__globals__['filename'])
                except:
                    mod = os.path.abspath(Function.__func__.__globals__['__file__'])
                if not os.path.isfile(mod):
                    raise ImportError("No user defined function or method found with the name %s"%(mod,))
                self.__userFunction__modl = os.path.basename(mod).replace('.pyc','').replace('.pyo','').replace('.py','')
                self.__userFunction__path = os.path.dirname(mod)
                del mod
                self.__userOperator = Operator( name = self.__name, fromMethod = Function, avoidingRedundancy = self.__avoidRC, inputAsMultiFunction = self.__mfEnabled )
                self.__userFunction = self.__userOperator.appliedTo # Pour le calcul Direct
            else:
                raise TypeError("User defined function or method has to be provided for finite differences approximation.")
        else:
            self.__userOperator = Operator( name = self.__name, fromMethod = Function, avoidingRedundancy = self.__avoidRC, inputAsMultiFunction = self.__mfEnabled )
            self.__userFunction = self.__userOperator.appliedTo
        #
        self.__centeredDF = bool(centeredDF)
        if abs(float(increment)) > 1.e-15:
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
    def __doublon__(self, e, l, n, v=None):
        __ac, __iac = False, -1
        for i in range(len(l)-1,-1,-1):
            if numpy.linalg.norm(e - l[i]) < self.__tolerBP * n[i]:
                __ac, __iac = True, i
                if v is not None: logging.debug("FDA Cas%s déja calculé, récupération du doublon %i"%(v,__iac))
                break
        return __ac, __iac

    # ---------------------------------------------------------
    def DirectOperator(self, X ):
        """
        Calcul du direct à l'aide de la fonction fournie.
        """
        logging.debug("FDA Calcul DirectOperator (explicite)")
        if self.__mfEnabled:
            _HX = self.__userFunction( X, argsAsSerie = True )
        else:
            _X = numpy.asmatrix(numpy.ravel( X )).T
            _HX = numpy.ravel(self.__userFunction( _X ))
        #
        return _HX

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
        logging.debug("FDA Début du calcul de la Jacobienne")
        logging.debug("FDA   Incrément de............: %s*X"%float(self.__increment))
        logging.debug("FDA   Approximation centrée...: %s"%(self.__centeredDF))
        #
        if X is None or len(X)==0:
            raise ValueError("Nominal point X for approximate derivatives can not be None or void (given X: %s)."%(str(X),))
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
                logging.debug("FDA Cas J déja calculé, récupération du doublon %i"%__i)
        #
        if __alreadyCalculated:
            logging.debug("FDA   Calcul Jacobienne (par récupération du doublon %i)"%__i)
            _Jacobienne = self.__listJPCR[__i]
        else:
            logging.debug("FDA   Calcul Jacobienne (explicite)")
            if self.__centeredDF:
                #
                if self.__mpEnabled and not self.__mfEnabled:
                    funcrepr = {
                        "__userFunction__path" : self.__userFunction__path,
                        "__userFunction__modl" : self.__userFunction__modl,
                        "__userFunction__name" : self.__userFunction__name,
                    }
                    _jobs = []
                    for i in range( len(_dX) ):
                        _dXi            = _dX[i]
                        _X_plus_dXi     = numpy.array( _X.A1, dtype=float )
                        _X_plus_dXi[i]  = _X[i] + _dXi
                        _X_moins_dXi    = numpy.array( _X.A1, dtype=float )
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _jobs.append( (_X_plus_dXi,  funcrepr) )
                        _jobs.append( (_X_moins_dXi, funcrepr) )
                    #
                    import multiprocessing
                    self.__pool = multiprocessing.Pool(self.__mpWorkers)
                    _HX_plusmoins_dX = self.__pool.map( ExecuteFunction, _jobs )
                    self.__pool.close()
                    self.__pool.join()
                    #
                    _Jacobienne  = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel( _HX_plusmoins_dX[2*i] - _HX_plusmoins_dX[2*i+1] ) / (2.*_dX[i]) )
                    #
                elif self.__mfEnabled:
                    _xserie = []
                    for i in range( len(_dX) ):
                        _dXi            = _dX[i]
                        _X_plus_dXi     = numpy.array( _X.A1, dtype=float )
                        _X_plus_dXi[i]  = _X[i] + _dXi
                        _X_moins_dXi    = numpy.array( _X.A1, dtype=float )
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _xserie.append( _X_plus_dXi )
                        _xserie.append( _X_moins_dXi )
                    #
                    _HX_plusmoins_dX = self.DirectOperator( _xserie )
                     #
                    _Jacobienne  = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel( _HX_plusmoins_dX[2*i] - _HX_plusmoins_dX[2*i+1] ) / (2.*_dX[i]) )
                    #
                else:
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
                if self.__mpEnabled and not self.__mfEnabled:
                    funcrepr = {
                        "__userFunction__path" : self.__userFunction__path,
                        "__userFunction__modl" : self.__userFunction__modl,
                        "__userFunction__name" : self.__userFunction__name,
                    }
                    _jobs = []
                    _jobs.append( (_X.A1, funcrepr) )
                    for i in range( len(_dX) ):
                        _X_plus_dXi    = numpy.array( _X.A1, dtype=float )
                        _X_plus_dXi[i] = _X[i] + _dX[i]
                        #
                        _jobs.append( (_X_plus_dXi, funcrepr) )
                    #
                    import multiprocessing
                    self.__pool = multiprocessing.Pool(self.__mpWorkers)
                    _HX_plus_dX = self.__pool.map( ExecuteFunction, _jobs )
                    self.__pool.close()
                    self.__pool.join()
                    #
                    _HX = _HX_plus_dX.pop(0)
                    #
                    _Jacobienne = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel(( _HX_plus_dX[i] - _HX ) / _dX[i]) )
                    #
                elif self.__mfEnabled:
                    _xserie = []
                    _xserie.append( _X.A1 )
                    for i in range( len(_dX) ):
                        _X_plus_dXi    = numpy.array( _X.A1, dtype=float )
                        _X_plus_dXi[i] = _X[i] + _dX[i]
                        #
                        _xserie.append( _X_plus_dXi )
                    #
                    _HX_plus_dX = self.DirectOperator( _xserie )
                    #
                    _HX = _HX_plus_dX.pop(0)
                    #
                    _Jacobienne = []
                    for i in range( len(_dX) ):
                        _Jacobienne.append( numpy.ravel(( _HX_plus_dX[i] - _HX ) / _dX[i]) )
                   #
                else:
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
            _Jacobienne = numpy.asmatrix( numpy.vstack( _Jacobienne ) ).T
            if self.__avoidRC:
                if self.__lenghtRJ < 0: self.__lenghtRJ = 2 * _X.size
                while len(self.__listJPCP) > self.__lenghtRJ:
                    self.__listJPCP.pop(0)
                    self.__listJPCI.pop(0)
                    self.__listJPCR.pop(0)
                    self.__listJPPN.pop(0)
                    self.__listJPIN.pop(0)
                self.__listJPCP.append( copy.copy(_X) )
                self.__listJPCI.append( copy.copy(_dX) )
                self.__listJPCR.append( copy.copy(_Jacobienne) )
                self.__listJPPN.append( numpy.linalg.norm(_X) )
                self.__listJPIN.append( numpy.linalg.norm(_Jacobienne) )
        #
        logging.debug("FDA Fin du calcul de la Jacobienne")
        #
        return _Jacobienne

    # ---------------------------------------------------------
    def TangentOperator(self, paire ):
        """
        Calcul du tangent à l'aide de la Jacobienne.
        """
        if self.__mfEnabled:
            assert len(paire) == 1, "Incorrect lenght of arguments"
            _paire = paire[0]
            assert len(_paire) == 2, "Incorrect number of arguments"
        else:
            assert len(paire) == 2, "Incorrect number of arguments"
            _paire = paire
        X, dX = _paire
        _Jacobienne = self.TangentMatrix( X )
        if dX is None or len(dX) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            if self.__mfEnabled: return [_Jacobienne,]
            else:                return _Jacobienne
        else:
            #
            # Calcul de la valeur linéarisée de H en X appliqué à dX
            # ------------------------------------------------------
            _dX = numpy.asmatrix(numpy.ravel( dX )).T
            _HtX = numpy.dot(_Jacobienne, _dX)
            if self.__mfEnabled: return [_HtX.A1,]
            else:                return _HtX.A1

    # ---------------------------------------------------------
    def AdjointOperator(self, paire ):
        """
        Calcul de l'adjoint à l'aide de la Jacobienne.
        """
        if self.__mfEnabled:
            assert len(paire) == 1, "Incorrect lenght of arguments"
            _paire = paire[0]
            assert len(_paire) == 2, "Incorrect number of arguments"
        else:
            assert len(paire) == 2, "Incorrect number of arguments"
            _paire = paire
        X, Y = _paire
        _JacobienneT = self.TangentMatrix( X ).T
        if Y is None or len(Y) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            if self.__mfEnabled: return [_JacobienneT,]
            else:                return _JacobienneT
        else:
            #
            # Calcul de la valeur de l'adjoint en X appliqué à Y
            # --------------------------------------------------
            _Y = numpy.asmatrix(numpy.ravel( Y )).T
            _HaY = numpy.dot(_JacobienneT, _Y)
            if self.__mfEnabled: return [_HaY.A1,]
            else:                return _HaY.A1

# ==============================================================================
def mmqr(
        func     = None,
        x0       = None,
        fprime   = None,
        bounds   = None,
        quantile = 0.5,
        maxfun   = 15000,
        toler    = 1.e-06,
        y        = None,
        ):
    """
    Implémentation informatique de l'algorithme MMQR, basée sur la publication :
    David R. Hunter, Kenneth Lange, "Quantile Regression via an MM Algorithm",
    Journal of Computational and Graphical Statistics, 9, 1, pp.60-77, 2000.
    """
    #
    # Recuperation des donnees et informations initiales
    # --------------------------------------------------
    variables = numpy.ravel( x0 )
    mesures   = numpy.ravel( y )
    increment = sys.float_info[0]
    p         = variables.size
    n         = mesures.size
    quantile  = float(quantile)
    #
    # Calcul des parametres du MM
    # ---------------------------
    tn      = float(toler) / n
    e0      = -tn / math.log(tn)
    epsilon = (e0-tn)/(1+math.log(e0))
    #
    # Calculs d'initialisation
    # ------------------------
    residus  = mesures - numpy.ravel( func( variables ) )
    poids    = 1./(epsilon+numpy.abs(residus))
    veps     = 1. - 2. * quantile - residus * poids
    lastsurrogate = -numpy.sum(residus*veps) - (1.-2.*quantile)*numpy.sum(residus)
    iteration = 0
    #
    # Recherche iterative
    # -------------------
    while (increment > toler) and (iteration < maxfun) :
        iteration += 1
        #
        Derivees  = numpy.array(fprime(variables))
        Derivees  = Derivees.reshape(n,p) # Necessaire pour remettre en place la matrice si elle passe par des tuyaux YACS
        DeriveesT = Derivees.transpose()
        M         =   numpy.dot( DeriveesT , (numpy.array(numpy.matrix(p*[poids,]).T)*Derivees) )
        SM        =   numpy.transpose(numpy.dot( DeriveesT , veps ))
        step      = - numpy.linalg.lstsq( M, SM, rcond=-1 )[0]
        #
        variables = variables + step
        if bounds is not None:
            # Attention : boucle infinie à éviter si un intervalle est trop petit
            while( (variables < numpy.ravel(numpy.asmatrix(bounds)[:,0])).any() or (variables > numpy.ravel(numpy.asmatrix(bounds)[:,1])).any() ):
                step      = step/2.
                variables = variables - step
        residus   = mesures - numpy.ravel( func(variables) )
        surrogate = numpy.sum(residus**2 * poids) + (4.*quantile-2.) * numpy.sum(residus)
        #
        while ( (surrogate > lastsurrogate) and ( max(list(numpy.abs(step))) > 1.e-16 ) ) :
            step      = step/2.
            variables = variables - step
            residus   = mesures - numpy.ravel( func(variables) )
            surrogate = numpy.sum(residus**2 * poids) + (4.*quantile-2.) * numpy.sum(residus)
        #
        increment     = lastsurrogate-surrogate
        poids         = 1./(epsilon+numpy.abs(residus))
        veps          = 1. - 2. * quantile - residus * poids
        lastsurrogate = -numpy.sum(residus * veps) - (1.-2.*quantile)*numpy.sum(residus)
    #
    # Mesure d'écart
    # --------------
    Ecart = quantile * numpy.sum(residus) - numpy.sum( residus[residus<0] )
    #
    return variables, Ecart, [n,p,iteration,increment,0]

# ==============================================================================
def EnsembleOfCenteredPerturbations( _bgcenter, _bgcovariance, _nbmembers ):
    "Génération d'un ensemble de taille _nbmembers-1 d'états aléatoires centrés"
    #
    _bgcenter = numpy.ravel(_bgcenter)[:,None]
    if _nbmembers < 1:
        raise ValueError("Number of members has to be strictly more than 1 (given number: %s)."%(str(_nbmembers),))
    #
    if _bgcovariance is None:
        BackgroundEnsemble = numpy.tile( _bgcenter, _nbmembers)
    else:
        _Z = numpy.random.multivariate_normal(numpy.zeros(_bgcenter.size), _bgcovariance, size=_nbmembers).T
        BackgroundEnsemble = numpy.tile( _bgcenter, _nbmembers) + _Z
    #
    return BackgroundEnsemble

# ==============================================================================
def EnsembleOfBackgroundPerturbations( _bgcenter, _bgcovariance, _nbmembers, _withSVD = True):
    "Génération d'un ensemble de taille _nbmembers-1 d'états aléatoires centrés"
    def __CenteredRandomAnomalies(Zr, N):
        """
        Génère une matrice de N anomalies aléatoires centrées sur Zr selon les
        notes manuscrites de MB et conforme au code de PS avec eps = -1
        """
        eps = -1
        Q = numpy.eye(N-1)-numpy.ones((N-1,N-1))/numpy.sqrt(N)/(numpy.sqrt(N)-eps)
        Q = numpy.concatenate((Q, [eps*numpy.ones(N-1)/numpy.sqrt(N)]), axis=0)
        R, _ = numpy.linalg.qr(numpy.random.normal(size = (N-1,N-1)))
        Q = numpy.dot(Q,R)
        Zr = numpy.dot(Q,Zr)
        return Zr.T
    #
    _bgcenter = numpy.ravel(_bgcenter)[:,None]
    if _nbmembers < 1:
        raise ValueError("Number of members has to be strictly more than 1 (given number: %s)."%(str(_nbmembers),))
    if _bgcovariance is None:
        BackgroundEnsemble = numpy.tile( _bgcenter, _nbmembers)
    else:
        if _withSVD:
            U, s, V = numpy.linalg.svd(_bgcovariance, full_matrices=False)
            _nbctl = _bgcenter.size
            if _nbmembers > _nbctl:
                _Z = numpy.concatenate((numpy.dot(
                    numpy.diag(numpy.sqrt(s[:_nbctl])), V[:_nbctl]),
                    numpy.random.multivariate_normal(numpy.zeros(_nbctl),_bgcovariance,_nbmembers-1-_nbctl)), axis = 0)
            else:
                _Z = numpy.dot(numpy.diag(numpy.sqrt(s[:_nbmembers-1])), V[:_nbmembers-1])
            _Zca = __CenteredRandomAnomalies(_Z, _nbmembers)
            BackgroundEnsemble = _bgcenter + _Zca
        else:
            if max(abs(_bgcovariance.flatten())) > 0:
                _nbctl = _bgcenter.size
                _Z = numpy.random.multivariate_normal(numpy.zeros(_nbctl),_bgcovariance,_nbmembers-1)
                _Zca = __CenteredRandomAnomalies(_Z, _nbmembers)
                BackgroundEnsemble = _bgcenter + _Zca
            else:
                BackgroundEnsemble = numpy.tile( _bgcenter, _nbmembers)
    #
    return BackgroundEnsemble

# ==============================================================================
def EnsembleOfAnomalies( _ensemble, _optmean = None):
    "Renvoie les anomalies centrées à partir d'un ensemble TailleEtat*NbMembres"
    if _optmean is None:
        Em = numpy.asarray(_ensemble).mean(axis=1, dtype=mfp).astype('float')[:,numpy.newaxis]
    else:
        Em = numpy.ravel(_optmean)[:,numpy.newaxis]
    #
    return numpy.asarray(_ensemble) - Em

# ==============================================================================
def CovarianceInflation(
        InputCovOrEns,
        InflationType   = None,
        InflationFactor = None,
        BackgroundCov   = None,
        ):
    """
    Inflation applicable soit sur Pb ou Pa, soit sur les ensembles EXb ou EXa

    Synthèse : Hunt 2007, section 2.3.5
    """
    if InflationFactor is None:
        return InputCovOrEns
    else:
        InflationFactor = float(InflationFactor)
    #
    if InflationType in ["MultiplicativeOnAnalysisCovariance", "MultiplicativeOnBackgroundCovariance"]:
        if InflationFactor < 1.:
            raise ValueError("Inflation factor for multiplicative inflation has to be greater or equal than 1.")
        if InflationFactor < 1.+mpr:
            return InputCovOrEns
        OutputCovOrEns = InflationFactor**2 * InputCovOrEns
    #
    elif InflationType in ["MultiplicativeOnAnalysisAnomalies", "MultiplicativeOnBackgroundAnomalies"]:
        if InflationFactor < 1.:
            raise ValueError("Inflation factor for multiplicative inflation has to be greater or equal than 1.")
        if InflationFactor < 1.+mpr:
            return InputCovOrEns
        InputCovOrEnsMean = InputCovOrEns.mean(axis=1, dtype=mfp).astype('float')
        OutputCovOrEns = InputCovOrEnsMean[:,numpy.newaxis] \
            + InflationFactor * (InputCovOrEns - InputCovOrEnsMean[:,numpy.newaxis])
    #
    elif InflationType in ["AdditiveOnAnalysisCovariance", "AdditiveOnBackgroundCovariance"]:
        if InflationFactor < 0.:
            raise ValueError("Inflation factor for additive inflation has to be greater or equal than 0.")
        if InflationFactor < mpr:
            return InputCovOrEns
        __n, __m = numpy.asarray(InputCovOrEns).shape
        if __n != __m:
            raise ValueError("Additive inflation can only be applied to squared (covariance) matrix.")
        OutputCovOrEns = (1. - InflationFactor) * InputCovOrEns + InflationFactor * numpy.eye(__n)
    #
    elif InflationType == "HybridOnBackgroundCovariance":
        if InflationFactor < 0.:
            raise ValueError("Inflation factor for hybrid inflation has to be greater or equal than 0.")
        if InflationFactor < mpr:
            return InputCovOrEns
        __n, __m = numpy.asarray(InputCovOrEns).shape
        if __n != __m:
            raise ValueError("Additive inflation can only be applied to squared (covariance) matrix.")
        if BackgroundCov is None:
            raise ValueError("Background covariance matrix B has to be given for hybrid inflation.")
        if InputCovOrEns.shape != BackgroundCov.shape:
            raise ValueError("Ensemble covariance matrix has to be of same size than background covariance matrix B.")
        OutputCovOrEns = (1. - InflationFactor) * InputCovOrEns + InflationFactor * BackgroundCov
    #
    elif InflationType == "Relaxation":
        raise NotImplementedError("InflationType Relaxation")
    #
    else:
        raise ValueError("Error in inflation type, '%s' is not a valid keyword."%InflationType)
    #
    return OutputCovOrEns

# ==============================================================================
def multi3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, oneCycle):
    """
    Chapeau : 3DVAR multi-pas et multi-méthodes
    """
    #
    # Initialisation
    # --------------
    Xn = numpy.ravel(Xb).reshape((-1,1))
    #
    if selfA._parameters["EstimationOf"] == "State":
        M = EM["Direct"].appliedTo
        #
        if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
            selfA.StoredVariables["Analysis"].store( Xn )
            if selfA._toStore("APosterioriCovariance"):
                if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(Xn.size)
                else:                         Pn = B
                selfA.StoredVariables["APosterioriCovariance"].store( Pn )
            if selfA._toStore("ForecastState"):
                selfA.StoredVariables["ForecastState"].store( Xn )
    #
    if hasattr(Y,"stepnumber"):
        duration = Y.stepnumber()
    else:
        duration = 2
    #
    # Multi-pas
    # ---------
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((-1,1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((-1,1))
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast
            Xn = selfA.StoredVariables["Analysis"][-1]
            Xn_predicted = M( Xn )
            if selfA._toStore("ForecastState"):
                selfA.StoredVariables["ForecastState"].store( Xn_predicted )
        elif selfA._parameters["EstimationOf"] == "Parameters": # No forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
        Xn_predicted = numpy.ravel(Xn_predicted).reshape((-1,1))
        #
        oneCycle(selfA, Xn_predicted, Ynpu, U, HO, None, None, R, B, None)
    #
    return 0

# ==============================================================================
def std3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR (Bouttier 1999, Courtier 1993)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    if "Minimizer" in selfA._parameters and selfA._parameters["Minimizer"] == "TNC":
        selfA.setParameterValue("StoreInternalVariables",True)
    #
    # Opérateurs
    # ----------
    Hm = HO["Direct"].appliedTo
    Ha = HO["Adjoint"].appliedInXTo
    #
    # Utilisation éventuelle d'un vecteur H(Xb) précalculé
    # ----------------------------------------------------
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = Hm( Xb, HO["AppliedInX"]["HXb"] )
    else:
        HXb = Hm( Xb )
    HXb = numpy.asmatrix(numpy.ravel( HXb )).T
    if Y.size != HXb.size:
        raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
    if max(Y.shape) != max(HXb.shape):
        raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
    #
    if selfA._toStore("JacobianMatrixAtBackground"):
        HtMb = HO["Tangent"].asMatrix(ValueForMethodForm = Xb)
        HtMb = HtMb.reshape(Y.size,Xb.size) # ADAO & check shape
        selfA.StoredVariables["JacobianMatrixAtBackground"].store( HtMb )
    #
    # Précalcul des inversions de B et R
    # ----------------------------------
    BI = B.getI()
    RI = R.getI()
    #
    # Point de démarrage de l'optimisation
    # ------------------------------------
    Xini = selfA._parameters["InitializationPoint"]
    #
    # Définition de la fonction-coût
    # ------------------------------
    def CostFunction(x):
        _X  = numpy.asmatrix(numpy.ravel( x )).T
        if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CurrentState") or \
            selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( _X )
        _HX = Hm( _X )
        _HX = numpy.asmatrix(numpy.ravel( _HX )).T
        _Innovation = Y - _HX
        if selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        #
        Jb  = float( 0.5 * (_X - Xb).T * BI * (_X - Xb) )
        Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
        J   = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
            selfA._toStore("CurrentOptimum") or \
            selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        return J
    #
    def GradientOfCostFunction(x):
        _X      = numpy.asmatrix(numpy.ravel( x )).T
        _HX     = Hm( _X )
        _HX     = numpy.asmatrix(numpy.ravel( _HX )).T
        GradJb  = BI * (_X - Xb)
        GradJo  = - Ha( (_X, RI * (Y - _HX)) )
        GradJ   = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        if "0.19" <= scipy.version.version <= "1.1.0":
            import lbfgsbhlt as optimiseur
        else:
            import scipy.optimize as optimiseur
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
            factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
            )
        nfeval = Informations['funcalls']
        rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    else:
        raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = numpy.asmatrix(numpy.ravel( Minimum )).T
    #
    selfA.StoredVariables["Analysis"].store( Xa.A1 )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    # Calcul de la covariance d'analyse
    # ---------------------------------
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        HessienneI = []
        nb = Xa.size
        for i in range(nb):
            _ee    = numpy.matrix(numpy.zeros(nb)).T
            _ee[i] = 1.
            _HtEE  = numpy.dot(HtM,_ee)
            _HtEE  = numpy.asmatrix(numpy.ravel( _HtEE )).T
            HessienneI.append( numpy.ravel( BI*_ee + HaM * (RI * _HtEE) ) )
        HessienneI = numpy.matrix( HessienneI )
        A = HessienneI.I
        if min(A.shape) != max(A.shape):
            raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(selfA._name,str(A.shape)))
        if (numpy.diag(A) < 0).any():
            raise ValueError("The %s a posteriori covariance matrix A has at least one negative value on its diagonal. There is an error in the observation operator, please check it."%(selfA._name,))
        if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
            try:
                L = numpy.linalg.cholesky( A )
            except:
                raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(selfA._name,))
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( numpy.ravel(d) )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( numpy.ravel(d) )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(Y)).T-numpy.asmatrix(numpy.ravel(HXa)).T)) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        nech = selfA._parameters["NumberOfSamplesForQuantiles"]
        HXa  = numpy.matrix(numpy.ravel( HXa )).T
        YfQ  = None
        for i in range(nech):
            if selfA._parameters["SimulationForQuantiles"] == "Linear":
                dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                dYr = numpy.matrix(numpy.ravel( HtM * dXr )).T
                Yr = HXa + dYr
            elif selfA._parameters["SimulationForQuantiles"] == "NonLinear":
                Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                Yr = numpy.matrix(numpy.ravel( Hm( Xr ) )).T
            if YfQ is None:
                YfQ = Yr
            else:
                YfQ = numpy.hstack((YfQ,Yr))
        YfQ.sort(axis=-1)
        YQ = None
        for quantile in selfA._parameters["Quantiles"]:
            if not (0. <= float(quantile) <= 1.): continue
            indice = int(nech * float(quantile) - 1./nech)
            if YQ is None: YQ = YfQ[:,indice]
            else:          YQ = numpy.hstack((YQ,YfQ[:,indice]))
        selfA.StoredVariables["SimulationQuantiles"].store( YQ )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
    #
    return 0

# ==============================================================================
def van3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR variational analysis with no inversion of B (Huang 2000)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    if "Minimizer" in selfA._parameters and selfA._parameters["Minimizer"] == "TNC":
        selfA.setParameterValue("StoreInternalVariables",True)
    #
    # Initialisations
    # ---------------
    Hm = HO["Direct"].appliedTo
    Ha = HO["Adjoint"].appliedInXTo
    #
    # Précalcul des inversions de B et R
    BT = B.getT()
    RI = R.getI()
    #
    # Point de démarrage de l'optimisation
    Xini = numpy.zeros(Xb.shape)
    #
    # Définition de la fonction-coût
    # ------------------------------
    def CostFunction(v):
        _V = numpy.asmatrix(numpy.ravel( v )).T
        _X = Xb + B * _V
        if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CurrentState") or \
            selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( _X )
        _HX = Hm( _X )
        _HX = numpy.asmatrix(numpy.ravel( _HX )).T
        _Innovation = Y - _HX
        if selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( _HX )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( _Innovation )
        #
        Jb  = float( 0.5 * _V.T * BT * _V )
        Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
        J   = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
            selfA._toStore("CurrentOptimum") or \
            selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        return J
    #
    def GradientOfCostFunction(v):
        _V = numpy.asmatrix(numpy.ravel( v )).T
        _X = Xb + B * _V
        _HX     = Hm( _X )
        _HX     = numpy.asmatrix(numpy.ravel( _HX )).T
        GradJb  = BT * _V
        GradJo  = - Ha( (_X, RI * (Y - _HX)) )
        GradJ   = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
        if "0.19" <= scipy.version.version <= "1.1.0":
            import lbfgsbhlt as optimiseur
        else:
            import scipy.optimize as optimiseur
        Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
            factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
            )
        nfeval = Informations['funcalls']
        rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    else:
        raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
        Minimum = numpy.asmatrix(numpy.ravel( Minimum )).T
    else:
        Minimum = Xb + B * numpy.asmatrix(numpy.ravel( Minimum )).T
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = Minimum
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    # Calcul de la covariance d'analyse
    # ---------------------------------
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        BI = B.getI()
        HessienneI = []
        nb = Xa.size
        for i in range(nb):
            _ee    = numpy.matrix(numpy.zeros(nb)).T
            _ee[i] = 1.
            _HtEE  = numpy.dot(HtM,_ee)
            _HtEE  = numpy.asmatrix(numpy.ravel( _HtEE )).T
            HessienneI.append( numpy.ravel( BI*_ee + HaM * (RI * _HtEE) ) )
        HessienneI = numpy.matrix( HessienneI )
        A = HessienneI.I
        if min(A.shape) != max(A.shape):
            raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(selfA._name,str(A.shape)))
        if (numpy.diag(A) < 0).any():
            raise ValueError("The %s a posteriori covariance matrix A has at least one negative value on its diagonal. There is an error in the observation operator, please check it."%(selfA._name,))
        if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
            try:
                L = numpy.linalg.cholesky( A )
            except:
                raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(selfA._name,))
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( numpy.ravel(d) )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( numpy.ravel(d) )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(Y)).T-numpy.asmatrix(numpy.ravel(HXa)).T)) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        nech = selfA._parameters["NumberOfSamplesForQuantiles"]
        HXa  = numpy.matrix(numpy.ravel( HXa )).T
        YfQ  = None
        for i in range(nech):
            if selfA._parameters["SimulationForQuantiles"] == "Linear":
                dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                dYr = numpy.matrix(numpy.ravel( HtM * dXr )).T
                Yr = HXa + dYr
            elif selfA._parameters["SimulationForQuantiles"] == "NonLinear":
                Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                Yr = numpy.matrix(numpy.ravel( Hm( Xr ) )).T
            if YfQ is None:
                YfQ = Yr
            else:
                YfQ = numpy.hstack((YfQ,Yr))
        YfQ.sort(axis=-1)
        YQ = None
        for quantile in selfA._parameters["Quantiles"]:
            if not (0. <= float(quantile) <= 1.): continue
            indice = int(nech * float(quantile) - 1./nech)
            if YQ is None: YQ = YfQ[:,indice]
            else:          YQ = numpy.hstack((YQ,YfQ[:,indice]))
        selfA.StoredVariables["SimulationQuantiles"].store( YQ )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
    #
    return 0

# ==============================================================================
def incr3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR incrémental (Courtier 1994, 1997)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    if "Minimizer" in selfA._parameters and selfA._parameters["Minimizer"] == "TNC":
        selfA.setParameterValue("StoreInternalVariables",True)
    #
    # Initialisations
    # ---------------
    #
    # Opérateur non-linéaire pour la boucle externe
    Hm = HO["Direct"].appliedTo
    #
    # Précalcul des inversions de B et R
    BI = B.getI()
    RI = R.getI()
    #
    # Point de démarrage de l'optimisation
    Xini = selfA._parameters["InitializationPoint"]
    #
    HXb = numpy.asmatrix(numpy.ravel( Hm( Xb ) )).T
    Innovation = Y - HXb
    #
    # Outer Loop
    # ----------
    iOuter = 0
    J      = 1./mpr
    DeltaJ = 1./mpr
    Xr     = Xini.reshape((-1,1))
    while abs(DeltaJ) >= selfA._parameters["CostDecrementTolerance"] and iOuter <= selfA._parameters["MaximumNumberOfSteps"]:
        #
        # Inner Loop
        # ----------
        Ht = HO["Tangent"].asMatrix(Xr)
        Ht = Ht.reshape(Y.size,Xr.size) # ADAO & check shape
        #
        # Définition de la fonction-coût
        # ------------------------------
        def CostFunction(dx):
            _dX  = numpy.asmatrix(numpy.ravel( dx )).T
            if selfA._parameters["StoreInternalVariables"] or \
                selfA._toStore("CurrentState") or \
                selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentState"].store( Xb + _dX )
            _HdX = Ht * _dX
            _HdX = numpy.asmatrix(numpy.ravel( _HdX )).T
            _dInnovation = Innovation - _HdX
            if selfA._toStore("SimulatedObservationAtCurrentState") or \
                selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HXb + _HdX )
            if selfA._toStore("InnovationAtCurrentState"):
                selfA.StoredVariables["InnovationAtCurrentState"].store( _dInnovation )
            #
            Jb  = float( 0.5 * _dX.T * BI * _dX )
            Jo  = float( 0.5 * _dInnovation.T * RI * _dInnovation )
            J   = Jb + Jo
            #
            selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            if selfA._toStore("IndexOfOptimum") or \
                selfA._toStore("CurrentOptimum") or \
                selfA._toStore("CostFunctionJAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
                selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
                selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
            return J
        #
        def GradientOfCostFunction(dx):
            _dX          = numpy.asmatrix(numpy.ravel( dx )).T
            _HdX         = Ht * _dX
            _HdX         = numpy.asmatrix(numpy.ravel( _HdX )).T
            _dInnovation = Innovation - _HdX
            GradJb       = BI * _dX
            GradJo       = - Ht.T @ (RI * _dInnovation)
            GradJ        = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
            return GradJ
        #
        # Minimisation de la fonctionnelle
        # --------------------------------
        nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
        #
        if selfA._parameters["Minimizer"] == "LBFGSB":
            # Minimum, J_optimal, Informations = scipy.optimize.fmin_l_bfgs_b(
            if "0.19" <= scipy.version.version <= "1.1.0":
                import lbfgsbhlt as optimiseur
            else:
                import scipy.optimize as optimiseur
            Minimum, J_optimal, Informations = optimiseur.fmin_l_bfgs_b(
                func        = CostFunction,
                x0          = numpy.zeros(Xini.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = selfA._parameters["Bounds"],
                maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
                factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
                pgtol       = selfA._parameters["ProjectedGradientTolerance"],
                iprint      = selfA._parameters["optiprint"],
                )
            nfeval = Informations['funcalls']
            rc     = Informations['warnflag']
        elif selfA._parameters["Minimizer"] == "TNC":
            Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
                func        = CostFunction,
                x0          = numpy.zeros(Xini.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                bounds      = selfA._parameters["Bounds"],
                maxfun      = selfA._parameters["MaximumNumberOfSteps"],
                pgtol       = selfA._parameters["ProjectedGradientTolerance"],
                ftol        = selfA._parameters["CostDecrementTolerance"],
                messages    = selfA._parameters["optmessages"],
                )
        elif selfA._parameters["Minimizer"] == "CG":
            Minimum, fopt, nfeval, grad_calls, rc = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(Xini.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = selfA._parameters["MaximumNumberOfSteps"],
                gtol        = selfA._parameters["GradientNormTolerance"],
                disp        = selfA._parameters["optdisp"],
                full_output = True,
                )
        elif selfA._parameters["Minimizer"] == "NCG":
            Minimum, fopt, nfeval, grad_calls, hcalls, rc = scipy.optimize.fmin_ncg(
                f           = CostFunction,
                x0          = numpy.zeros(Xini.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = selfA._parameters["MaximumNumberOfSteps"],
                avextol     = selfA._parameters["CostDecrementTolerance"],
                disp        = selfA._parameters["optdisp"],
                full_output = True,
                )
        elif selfA._parameters["Minimizer"] == "BFGS":
            Minimum, fopt, gopt, Hopt, nfeval, grad_calls, rc = scipy.optimize.fmin_bfgs(
                f           = CostFunction,
                x0          = numpy.zeros(Xini.size),
                fprime      = GradientOfCostFunction,
                args        = (),
                maxiter     = selfA._parameters["MaximumNumberOfSteps"],
                gtol        = selfA._parameters["GradientNormTolerance"],
                disp        = selfA._parameters["optdisp"],
                full_output = True,
                )
        else:
            raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
        #
        IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
        #
        if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
            Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
            Minimum = numpy.asmatrix(numpy.ravel( Minimum )).T
        else:
            Minimum = Xb + numpy.asmatrix(numpy.ravel( Minimum )).T
        #
        Xr     = Minimum
        DeltaJ = selfA.StoredVariables["CostFunctionJ" ][-1] - J
        iOuter = selfA.StoredVariables["CurrentIterationNumber"][-1]
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = Xr
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    # Calcul de la covariance d'analyse
    # ---------------------------------
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        HessienneI = []
        nb = Xa.size
        for i in range(nb):
            _ee    = numpy.matrix(numpy.zeros(nb)).T
            _ee[i] = 1.
            _HtEE  = numpy.dot(HtM,_ee)
            _HtEE  = numpy.asmatrix(numpy.ravel( _HtEE )).T
            HessienneI.append( numpy.ravel( BI*_ee + HaM * (RI * _HtEE) ) )
        HessienneI = numpy.matrix( HessienneI )
        A = HessienneI.I
        if min(A.shape) != max(A.shape):
            raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(selfA._name,str(A.shape)))
        if (numpy.diag(A) < 0).any():
            raise ValueError("The %s a posteriori covariance matrix A has at least one negative value on its diagonal. There is an error in the observation operator, please check it."%(selfA._name,))
        if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
            try:
                L = numpy.linalg.cholesky( A )
            except:
                raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(selfA._name,))
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( numpy.ravel(d) )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( numpy.ravel(d) )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(Y)).T-numpy.asmatrix(numpy.ravel(HXa)).T)) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        nech = selfA._parameters["NumberOfSamplesForQuantiles"]
        HXa  = numpy.matrix(numpy.ravel( HXa )).T
        YfQ  = None
        for i in range(nech):
            if selfA._parameters["SimulationForQuantiles"] == "Linear":
                dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                dYr = numpy.matrix(numpy.ravel( HtM * dXr )).T
                Yr = HXa + dYr
            elif selfA._parameters["SimulationForQuantiles"] == "NonLinear":
                Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                Yr = numpy.matrix(numpy.ravel( Hm( Xr ) )).T
            if YfQ is None:
                YfQ = Yr
            else:
                YfQ = numpy.hstack((YfQ,Yr))
        YfQ.sort(axis=-1)
        YQ = None
        for quantile in selfA._parameters["Quantiles"]:
            if not (0. <= float(quantile) <= 1.): continue
            indice = int(nech * float(quantile) - 1./nech)
            if YQ is None: YQ = YfQ[:,indice]
            else:          YQ = numpy.hstack((YQ,YfQ[:,indice]))
        selfA.StoredVariables["SimulationQuantiles"].store( YQ )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
    #
    return 0

# ==============================================================================
def psas3dvar(selfA, Xb, Y, U, HO, EM, CM, R, B, Q):
    """
    3DVAR PSAS (Huang 2000)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    if "Minimizer" in selfA._parameters and selfA._parameters["Minimizer"] == "TNC":
        selfA.setParameterValue("StoreInternalVariables",True)
    #
    # Initialisations
    # ---------------
    #
    # Opérateurs
    Hm = HO["Direct"].appliedTo
    #
    # Utilisation éventuelle d'un vecteur H(Xb) précalculé
    if HO["AppliedInX"] is not None and "HXb" in HO["AppliedInX"]:
        HXb = Hm( Xb, HO["AppliedInX"]["HXb"] )
    else:
        HXb = Hm( Xb )
    HXb = numpy.asmatrix(numpy.ravel( HXb )).T
    if Y.size != HXb.size:
        raise ValueError("The size %i of observations Y and %i of observed calculation H(X) are different, they have to be identical."%(Y.size,HXb.size))
    if max(Y.shape) != max(HXb.shape):
        raise ValueError("The shapes %s of observations Y and %s of observed calculation H(X) are different, they have to be identical."%(Y.shape,HXb.shape))
    #
    if selfA._toStore("JacobianMatrixAtBackground"):
        HtMb = HO["Tangent"].asMatrix(ValueForMethodForm = Xb)
        HtMb = HtMb.reshape(Y.size,Xb.size) # ADAO & check shape
        selfA.StoredVariables["JacobianMatrixAtBackground"].store( HtMb )
    #
    Ht = HO["Tangent"].asMatrix(Xb)
    BHT = B * Ht.T
    HBHTpR = R + Ht * BHT
    Innovation = Y - HXb
    #
    # Point de démarrage de l'optimisation
    Xini = numpy.zeros(Xb.shape)
    #
    # Définition de la fonction-coût
    # ------------------------------
    def CostFunction(w):
        _W = numpy.asmatrix(numpy.ravel( w )).T
        if selfA._parameters["StoreInternalVariables"] or \
            selfA._toStore("CurrentState") or \
            selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentState"].store( Xb + BHT * _W )
        if selfA._toStore("SimulatedObservationAtCurrentState") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( Hm( Xb + BHT * _W ) )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( Innovation )
        #
        Jb  = float( 0.5 * _W.T * HBHTpR * _W )
        Jo  = float( - _W.T * Innovation )
        J   = Jb + Jo
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["CostFunctionJ"]) )
        selfA.StoredVariables["CostFunctionJb"].store( Jb )
        selfA.StoredVariables["CostFunctionJo"].store( Jo )
        selfA.StoredVariables["CostFunctionJ" ].store( J )
        if selfA._toStore("IndexOfOptimum") or \
            selfA._toStore("CurrentOptimum") or \
            selfA._toStore("CostFunctionJAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJbAtCurrentOptimum") or \
            selfA._toStore("CostFunctionJoAtCurrentOptimum") or \
            selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
        if selfA._toStore("IndexOfOptimum"):
            selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
        if selfA._toStore("CurrentOptimum"):
            selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["CurrentState"][IndexMin] )
        if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin] )
        if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
        if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
        if selfA._toStore("CostFunctionJAtCurrentOptimum"):
            selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        return J
    #
    def GradientOfCostFunction(w):
        _W = numpy.asmatrix(numpy.ravel( w )).T
        GradJb  = HBHTpR * _W
        GradJo  = - Innovation
        GradJ   = numpy.ravel( GradJb ) + numpy.ravel( GradJo )
        return GradJ
    #
    # Minimisation de la fonctionnelle
    # --------------------------------
    nbPreviousSteps = selfA.StoredVariables["CostFunctionJ"].stepnumber()
    #
    if selfA._parameters["Minimizer"] == "LBFGSB":
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
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"]-1,
            factr       = selfA._parameters["CostDecrementTolerance"]*1.e14,
            pgtol       = selfA._parameters["ProjectedGradientTolerance"],
            iprint      = selfA._parameters["optiprint"],
            )
        nfeval = Informations['funcalls']
        rc     = Informations['warnflag']
    elif selfA._parameters["Minimizer"] == "TNC":
        Minimum, nfeval, rc = scipy.optimize.fmin_tnc(
            func        = CostFunction,
            x0          = Xini,
            fprime      = GradientOfCostFunction,
            args        = (),
            bounds      = selfA._parameters["Bounds"],
            maxfun      = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
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
            maxiter     = selfA._parameters["MaximumNumberOfSteps"],
            gtol        = selfA._parameters["GradientNormTolerance"],
            disp        = selfA._parameters["optdisp"],
            full_output = True,
            )
    else:
        raise ValueError("Error in Minimizer name: %s"%selfA._parameters["Minimizer"])
    #
    IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
    MinJ     = selfA.StoredVariables["CostFunctionJ"][IndexMin]
    #
    # Correction pour pallier a un bug de TNC sur le retour du Minimum
    # ----------------------------------------------------------------
    if selfA._parameters["StoreInternalVariables"] or selfA._toStore("CurrentState"):
        Minimum = selfA.StoredVariables["CurrentState"][IndexMin]
        Minimum = numpy.asmatrix(numpy.ravel( Minimum )).T
    else:
        Minimum = Xb + BHT * numpy.asmatrix(numpy.ravel( Minimum )).T
    #
    # Obtention de l'analyse
    # ----------------------
    Xa = Minimum
    #
    selfA.StoredVariables["Analysis"].store( Xa )
    #
    if selfA._toStore("OMA") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("SimulatedObservationAtOptimum"):
        if selfA._toStore("SimulatedObservationAtCurrentState"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentState"][IndexMin]
        elif selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            HXa = selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"][-1]
        else:
            HXa = Hm( Xa )
    #
    # Calcul de la covariance d'analyse
    # ---------------------------------
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("JacobianMatrixAtOptimum") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HtM = HO["Tangent"].asMatrix(ValueForMethodForm = Xa)
        HtM = HtM.reshape(Y.size,Xa.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles") or \
        selfA._toStore("KalmanGainAtOptimum"):
        HaM = HO["Adjoint"].asMatrix(ValueForMethodForm = Xa)
        HaM = HaM.reshape(Xa.size,Y.size) # ADAO & check shape
    if selfA._toStore("APosterioriCovariance") or \
        selfA._toStore("SimulationQuantiles"):
        BI = B.getI()
        RI = R.getI()
        HessienneI = []
        nb = Xa.size
        for i in range(nb):
            _ee    = numpy.matrix(numpy.zeros(nb)).T
            _ee[i] = 1.
            _HtEE  = numpy.dot(HtM,_ee)
            _HtEE  = numpy.asmatrix(numpy.ravel( _HtEE )).T
            HessienneI.append( numpy.ravel( BI*_ee + HaM * (RI * _HtEE) ) )
        HessienneI = numpy.matrix( HessienneI )
        A = HessienneI.I
        if min(A.shape) != max(A.shape):
            raise ValueError("The %s a posteriori covariance matrix A is of shape %s, despites it has to be a squared matrix. There is an error in the observation operator, please check it."%(selfA._name,str(A.shape)))
        if (numpy.diag(A) < 0).any():
            raise ValueError("The %s a posteriori covariance matrix A has at least one negative value on its diagonal. There is an error in the observation operator, please check it."%(selfA._name,))
        if logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
            try:
                L = numpy.linalg.cholesky( A )
            except:
                raise ValueError("The %s a posteriori covariance matrix A is not symmetric positive-definite. Please check your a priori covariances and your observation operator."%(selfA._name,))
    if selfA._toStore("APosterioriCovariance"):
        selfA.StoredVariables["APosterioriCovariance"].store( A )
    if selfA._toStore("JacobianMatrixAtOptimum"):
        selfA.StoredVariables["JacobianMatrixAtOptimum"].store( HtM )
    if selfA._toStore("KalmanGainAtOptimum"):
        if   (Y.size <= Xb.size): KG  = B * HaM * (R + numpy.dot(HtM, B * HaM)).I
        elif (Y.size >  Xb.size): KG = (BI + numpy.dot(HaM, RI * HtM)).I * HaM * RI
        selfA.StoredVariables["KalmanGainAtOptimum"].store( KG )
    #
    # Calculs et/ou stockages supplémentaires
    # ---------------------------------------
    if selfA._toStore("Innovation") or \
        selfA._toStore("SigmaObs2") or \
        selfA._toStore("MahalanobisConsistency") or \
        selfA._toStore("OMB"):
        d  = Y - HXb
    if selfA._toStore("Innovation"):
        selfA.StoredVariables["Innovation"].store( numpy.ravel(d) )
    if selfA._toStore("BMA"):
        selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(Xa) )
    if selfA._toStore("OMA"):
        selfA.StoredVariables["OMA"].store( numpy.ravel(Y) - numpy.ravel(HXa) )
    if selfA._toStore("OMB"):
        selfA.StoredVariables["OMB"].store( numpy.ravel(d) )
    if selfA._toStore("SigmaObs2"):
        TraceR = R.trace(Y.size)
        selfA.StoredVariables["SigmaObs2"].store( float( (d.T * (numpy.asmatrix(numpy.ravel(Y)).T-numpy.asmatrix(numpy.ravel(HXa)).T)) ) / TraceR )
    if selfA._toStore("MahalanobisConsistency"):
        selfA.StoredVariables["MahalanobisConsistency"].store( float( 2.*MinJ/d.size ) )
    if selfA._toStore("SimulationQuantiles"):
        nech = selfA._parameters["NumberOfSamplesForQuantiles"]
        HXa  = numpy.matrix(numpy.ravel( HXa )).T
        YfQ  = None
        for i in range(nech):
            if selfA._parameters["SimulationForQuantiles"] == "Linear":
                dXr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A) - Xa.A1).T
                dYr = numpy.matrix(numpy.ravel( HtM * dXr )).T
                Yr = HXa + dYr
            elif selfA._parameters["SimulationForQuantiles"] == "NonLinear":
                Xr = numpy.matrix(numpy.random.multivariate_normal(Xa.A1,A)).T
                Yr = numpy.matrix(numpy.ravel( Hm( Xr ) )).T
            if YfQ is None:
                YfQ = Yr
            else:
                YfQ = numpy.hstack((YfQ,Yr))
        YfQ.sort(axis=-1)
        YQ = None
        for quantile in selfA._parameters["Quantiles"]:
            if not (0. <= float(quantile) <= 1.): continue
            indice = int(nech * float(quantile) - 1./nech)
            if YQ is None: YQ = YfQ[:,indice]
            else:          YQ = numpy.hstack((YQ,YfQ[:,indice]))
        selfA.StoredVariables["SimulationQuantiles"].store( YQ )
    if selfA._toStore("SimulatedObservationAtBackground"):
        selfA.StoredVariables["SimulatedObservationAtBackground"].store( numpy.ravel(HXb) )
    if selfA._toStore("SimulatedObservationAtOptimum"):
        selfA.StoredVariables["SimulatedObservationAtOptimum"].store( numpy.ravel(HXa) )
    #
    return 0

# ==============================================================================
def senkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula"):
    """
    Stochastic EnKF (Envensen 1994, Burgers 1998)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    # ----------
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
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
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    #
    # Initialisation
    # --------------
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(__n)
    else:                         Pn = B
    if hasattr(R,"asfullmatrix"): Rn = R.asfullmatrix(__p)
    else:                         Rn = R
    if hasattr(Q,"asfullmatrix"): Qn = Q.asfullmatrix(__n)
    else:                         Qn = Q
    Xn = EnsembleOfBackgroundPerturbations( Xb, None, __m )
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        selfA.StoredVariables["Analysis"].store( numpy.ravel(Xb) )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
            covarianceXa = Pn
    #
    previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,-1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,-1))
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
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            EMX = M( [(Xn[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            qi = numpy.random.multivariate_normal(numpy.zeros(__n), Qn, size=__m).T
            Xn_predicted = EMX + qi
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm * Un
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
        #
        # Mean of forecast and observation of forecast
        Xfm  = Xn_predicted.mean(axis=1, dtype=mfp).astype('float').reshape((__n,-1))
        Hfm  = HX_predicted.mean(axis=1, dtype=mfp).astype('float').reshape((__p,-1))
        #
        #--------------------------
        if VariantM == "KalmanFilterFormula05":
            PfHT, HPfHT = 0., 0.
            for i in range(__m):
                Exfi = Xn_predicted[:,i].reshape((__n,-1)) - Xfm
                Eyfi = HX_predicted[:,i].reshape((__p,-1)) - Hfm
                PfHT  += Exfi * Eyfi.T
                HPfHT += Eyfi * Eyfi.T
            PfHT  = (1./(__m-1)) * PfHT
            HPfHT = (1./(__m-1)) * HPfHT
            Kn     = PfHT * ( R + HPfHT ).I
            del PfHT, HPfHT
            #
            for i in range(__m):
                ri = numpy.random.multivariate_normal(numpy.zeros(__p), Rn)
                Xn[:,i] = numpy.ravel(Xn_predicted[:,i]) + Kn @ (numpy.ravel(Ynpu) + ri - HX_predicted[:,i])
        #--------------------------
        elif VariantM == "KalmanFilterFormula16":
            EpY   = EnsembleOfCenteredPerturbations(Ynpu, Rn, __m)
            EpYm  = EpY.mean(axis=1, dtype=mfp).astype('float').reshape((__p,-1))
            #
            EaX   = EnsembleOfAnomalies( Xn_predicted ) / numpy.sqrt(__m-1)
            EaY = (HX_predicted - Hfm - EpY + EpYm) / numpy.sqrt(__m-1)
            #
            Kn = EaX @ EaY.T @ numpy.linalg.inv( EaY @ EaY.T)
            #
            for i in range(__m):
                Xn[:,i] = numpy.ravel(Xn_predicted[:,i]) + Kn @ (numpy.ravel(EpY[:,i]) - HX_predicted[:,i])
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        Xa = Xn.mean(axis=1, dtype=mfp).astype('float').reshape((__n,-1))
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.asmatrix(numpy.ravel( H((Xa, Un)) )).T
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( EMX )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( EMX - Xa.reshape((__n,1)) )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HX_predicted + Ynpu )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * BI * (Xa - Xb) )
            Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            Eai = EnsembleOfAnomalies( Xn ) / numpy.sqrt(__m-1) # Anomalies
            Pn = Eai @ Eai.T
            Pn = 0.5 * (Pn + Pn.T)
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = Pn
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def etkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="KalmanFilterFormula"):
    """
    Ensemble-Transform EnKF (ETKF or Deterministic EnKF: Bishop 2001, Hunt 2007)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    # ----------
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
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
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
        RI = R.getI()
    elif VariantM != "KalmanFilterFormula":
        RI = R.getI()
    if VariantM == "KalmanFilterFormula":
        RIdemi = R.choleskyI()
    #
    # Initialisation
    # --------------
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(__n)
    else:                         Pn = B
    if hasattr(R,"asfullmatrix"): Rn = R.asfullmatrix(__p)
    else:                         Rn = R
    if hasattr(Q,"asfullmatrix"): Qn = Q.asfullmatrix(__n)
    else:                         Qn = Q
    Xn = EnsembleOfBackgroundPerturbations( Xb, None, __m )
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        selfA.StoredVariables["Analysis"].store( numpy.ravel(Xb) )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
            covarianceXa = Pn
    #
    previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,-1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,-1))
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
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            EMX = M( [(Xn[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            qi = numpy.random.multivariate_normal(numpy.zeros(__n), Qn, size=__m).T
            Xn_predicted = EMX + qi
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm * Un
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
            HX_predicted = H( [(Xn_predicted[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
        #
        # Mean of forecast and observation of forecast
        Xfm  = Xn_predicted.mean(axis=1, dtype=mfp).astype('float').reshape((__n,-1))
        Hfm  = HX_predicted.mean(axis=1, dtype=mfp).astype('float').reshape((__p,1))
        #
        # Anomalies
        EaX   = EnsembleOfAnomalies( Xn_predicted )
        EaHX  = numpy.array(HX_predicted - Hfm)
        #
        #--------------------------
        if VariantM == "KalmanFilterFormula":
            mS    = RIdemi * EaHX / numpy.sqrt(__m-1)
            delta = RIdemi * ( Ynpu - Hfm )
            mT    = numpy.linalg.inv( numpy.eye(__m) + mS.T @ mS )
            vw    = mT @ mS.transpose() @ delta
            #
            Tdemi = numpy.real(scipy.linalg.sqrtm(mT))
            mU    = numpy.eye(__m)
            #
            EaX   = EaX / numpy.sqrt(__m-1)
            Xn    = Xfm + EaX @ ( vw.reshape((__m,-1)) + numpy.sqrt(__m-1) * Tdemi @ mU )
        #--------------------------
        elif VariantM == "Variational":
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * (__m-1) * w.T @ w
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = (__m-1) * w.reshape((__m,1))
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX)
            Htb = (__m-1) * numpy.eye(__m)
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw[:,None] + EWa)
        #--------------------------
        elif VariantM == "FiniteSize11": # Jauge Boc2011
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * __m * math.log(1 + 1/__m + w.T @ w)
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = __m * w.reshape((__m,1)) / (1 + 1/__m + w.T @ w)
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX)
            Htb = __m * \
                ( (1 + 1/__m + vw.T @ vw) * numpy.eye(__m) - 2 * vw @ vw.T ) \
                / (1 + 1/__m + vw.T @ vw)**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw.reshape((__m,-1)) + EWa)
        #--------------------------
        elif VariantM == "FiniteSize15": # Jauge Boc2015
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _Jo = 0.5 * _A.T * RI * _A
                _Jb = 0.5 * (__m+1) * math.log(1 + 1/__m + w.T @ w)
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = (__m+1) * w.reshape((__m,1)) / (1 + 1/__m + w.T @ w)
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX)
            Htb = (__m+1) * \
                ( (1 + 1/__m + vw.T @ vw) * numpy.eye(__m) - 2 * vw @ vw.T ) \
                / (1 + 1/__m + vw.T @ vw)**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw.reshape((__m,-1)) + EWa)
        #--------------------------
        elif VariantM == "FiniteSize16": # Jauge Boc2016
            HXfm = H((Xfm[:,None], Un)) # Eventuellement Hfm
            def CostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _Jo = 0.5 * _A.T @ (RI * _A)
                _Jb = 0.5 * (__m+1) * math.log(1 + 1/__m + w.T @ w / (__m-1))
                _J  = _Jo + _Jb
                return float(_J)
            def GradientOfCostFunction(w):
                _A  = Ynpu - HXfm.reshape((__p,-1)) - (EaHX @ w).reshape((__p,-1))
                _GardJo = - EaHX.T @ (RI * _A)
                _GradJb = ((__m+1) / (__m-1)) * w.reshape((__m,1)) / (1 + 1/__m + w.T @ w / (__m-1))
                _GradJ  = _GardJo + _GradJb
                return numpy.ravel(_GradJ)
            vw = scipy.optimize.fmin_cg(
                f           = CostFunction,
                x0          = numpy.zeros(__m),
                fprime      = GradientOfCostFunction,
                args        = (),
                disp        = False,
                )
            #
            Hto = EaHX.T @ (RI * EaHX)
            Htb = ((__m+1) / (__m-1)) * \
                ( (1 + 1/__m + vw.T @ vw / (__m-1)) * numpy.eye(__m) - 2 * vw @ vw.T / (__m-1) ) \
                / (1 + 1/__m + vw.T @ vw / (__m-1))**2
            Hta = Hto + Htb
            #
            Pta = numpy.linalg.inv( Hta )
            EWa = numpy.real(scipy.linalg.sqrtm((__m-1)*Pta)) # Partie imaginaire ~= 10^-18
            #
            Xn  = Xfm + EaX @ (vw[:,None] + EWa)
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        Xa = Xn.mean(axis=1, dtype=mfp).astype('float').reshape((__n,-1))
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.asmatrix(numpy.ravel( H((Xa, Un)) )).T
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( EMX )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( EMX - Xa.reshape((__n,1)) )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HX_predicted + Ynpu.reshape((__p,1)) )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HX_predicted )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * BI * (Xa - Xb) )
            Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            Eai = EnsembleOfAnomalies( Xn ) / numpy.sqrt(__m-1) # Anomalies
            Pn = Eai @ Eai.T
            Pn = 0.5 * (Pn + Pn.T)
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = Pn
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def mlef(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="MLEF13",
    BnotT=False, _epsilon=1.e-3, _e=1.e-7, _jmax=15000):
    """
    Maximum Likelihood Ensemble Filter (EnKF/MLEF Zupanski 2005, Bocquet 2013)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    # ----------
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
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
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
    RI = R.getI()
    #
    # Initialisation
    # --------------
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(__n)
    else:                         Pn = B
    if hasattr(R,"asfullmatrix"): Rn = R.asfullmatrix(__p)
    else:                         Rn = R
    if hasattr(Q,"asfullmatrix"): Qn = Q.asfullmatrix(__n)
    else:                         Qn = Q
    Xn = EnsembleOfBackgroundPerturbations( Xb, None, __m )
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        selfA.StoredVariables["Analysis"].store( numpy.ravel(Xb) )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
            covarianceXa = Pn
    #
    previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,-1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,-1))
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
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        if selfA._parameters["EstimationOf"] == "State": # Forecast + Q and observation of forecast
            EMX = M( [(Xn[:,i], Un) for i in range(__m)],
                argsAsSerie = True,
                returnSerieAsArrayMatrix = True )
            qi = numpy.random.multivariate_normal(numpy.zeros(__n), Qn, size=__m).T
            Xn_predicted = EMX + qi
            if Cm is not None and Un is not None: # Attention : si Cm est aussi dans M, doublon !
                Cm = Cm.reshape(__n,Un.size) # ADAO & check shape
                Xn_predicted = Xn_predicted + Cm * Un
        elif selfA._parameters["EstimationOf"] == "Parameters": # Observation of forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
        #
        #--------------------------
        if VariantM == "MLEF13":
            Xfm = numpy.ravel(Xn_predicted.mean(axis=1, dtype=mfp).astype('float'))
            EaX = EnsembleOfAnomalies( Xn_predicted ) / numpy.sqrt(__m-1)
            Ua  = numpy.eye(__m)
            __j = 0
            Deltaw = 1
            if not BnotT:
                Ta  = numpy.eye(__m)
            vw  = numpy.zeros(__m)
            while numpy.linalg.norm(Deltaw) >= _e and __j <= _jmax:
                vx1 = (Xfm + EaX @ vw).reshape((__n,-1))
                #
                if BnotT:
                    E1 = vx1 + _epsilon * EaX
                else:
                    E1 = vx1 + numpy.sqrt(__m-1) * EaX @ Ta
                #
                HE2 = H( [(E1[:,i,numpy.newaxis], Un) for i in range(__m)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
                vy2 = HE2.mean(axis=1, dtype=mfp).astype('float').reshape((__p,-1))
                #
                if BnotT:
                    EaY = (HE2 - vy2) / _epsilon
                else:
                    EaY = ( (HE2 - vy2) @ numpy.linalg.inv(Ta) ) / numpy.sqrt(__m-1)
                #
                GradJ = numpy.ravel(vw[:,None] - EaY.transpose() @ (RI * ( Ynpu - vy2 )))
                mH = numpy.eye(__m) + EaY.transpose() @ (RI * EaY)
                Deltaw = - numpy.linalg.solve(mH,GradJ)
                #
                vw = vw + Deltaw
                #
                if not BnotT:
                    Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                #
                __j = __j + 1
            #
            if BnotT:
                Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
            #
            Xn = vx1 + numpy.sqrt(__m-1) * EaX @ Ta @ Ua
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        Xa = Xn.mean(axis=1, dtype=mfp).astype('float').reshape((__n,-1))
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.asmatrix(numpy.ravel( H((Xa, Un)) )).T
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( EMX )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( EMX - Xa.reshape((__n,1)) )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HE2 + Ynpu.reshape((__p,-1)) )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HE2 )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * BI * (Xa - Xb) )
            Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            Eai = EnsembleOfAnomalies( Xn ) / numpy.sqrt(__m-1) # Anomalies
            Pn = Eai @ Eai.T
            Pn = 0.5 * (Pn + Pn.T)
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = Pn
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
def ienkf(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, VariantM="IEnKF12",
    BnotT=False, _epsilon=1.e-3, _e=1.e-7, _jmax=15000):
    """
    Iterative EnKF (Sakov 2012, Sakov 2018)

    selfA est identique au "self" d'algorithme appelant et contient les
    valeurs.
    """
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA._parameters["StoreInternalVariables"] = True
    #
    # Opérateurs
    # ----------
    H = HO["Direct"].appliedControledFormTo
    #
    if selfA._parameters["EstimationOf"] == "State":
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
    if selfA._parameters["StoreInternalVariables"] \
        or selfA._toStore("CostFunctionJ") \
        or selfA._toStore("CostFunctionJb") \
        or selfA._toStore("CostFunctionJo") \
        or selfA._toStore("CurrentOptimum") \
        or selfA._toStore("APosterioriCovariance"):
        BI = B.getI()
    RI = R.getI()
    #
    # Initialisation
    # --------------
    __n = Xb.size
    __m = selfA._parameters["NumberOfMembers"]
    if hasattr(B,"asfullmatrix"): Pn = B.asfullmatrix(__n)
    else:                         Pn = B
    if hasattr(R,"asfullmatrix"): Rn = R.asfullmatrix(__p)
    else:                         Rn = R
    if hasattr(Q,"asfullmatrix"): Qn = Q.asfullmatrix(__n)
    else:                         Qn = Q
    Xn = EnsembleOfBackgroundPerturbations( Xb, Pn, __m )
    #
    if len(selfA.StoredVariables["Analysis"])==0 or not selfA._parameters["nextStep"]:
        selfA.StoredVariables["Analysis"].store( numpy.ravel(Xb) )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
            covarianceXa = Pn
    #
    previousJMinimum = numpy.finfo(float).max
    #
    for step in range(duration-1):
        if hasattr(Y,"store"):
            Ynpu = numpy.ravel( Y[step+1] ).reshape((__p,-1))
        else:
            Ynpu = numpy.ravel( Y ).reshape((__p,-1))
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
        if selfA._parameters["InflationType"] == "MultiplicativeOnBackgroundAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        #--------------------------
        if VariantM == "IEnKF12":
            Xfm = numpy.ravel(Xn.mean(axis=1, dtype=mfp).astype('float'))
            EaX = EnsembleOfAnomalies( Xn ) / numpy.sqrt(__m-1)
            __j = 0
            Deltaw = 1
            if not BnotT:
                Ta  = numpy.eye(__m)
            vw  = numpy.zeros(__m)
            while numpy.linalg.norm(Deltaw) >= _e and __j <= _jmax:
                vx1 = (Xfm + EaX @ vw).reshape((__n,-1))
                #
                if BnotT:
                    E1 = vx1 + _epsilon * EaX
                else:
                    E1 = vx1 + numpy.sqrt(__m-1) * EaX @ Ta
                #
                if selfA._parameters["EstimationOf"] == "State": # Forecast + Q
                    E2 = M( [(E1[:,i,numpy.newaxis], Un) for i in range(__m)],
                        argsAsSerie = True,
                        returnSerieAsArrayMatrix = True )
                elif selfA._parameters["EstimationOf"] == "Parameters":
                    # --- > Par principe, M = Id
                    E2 = Xn
                vx2 = E2.mean(axis=1, dtype=mfp).astype('float').reshape((__n,-1))
                vy1 = H((vx2, Un)).reshape((__p,-1))
                #
                HE2 = H( [(E2[:,i,numpy.newaxis], Un) for i in range(__m)],
                    argsAsSerie = True,
                    returnSerieAsArrayMatrix = True )
                vy2 = HE2.mean(axis=1, dtype=mfp).astype('float').reshape((__p,-1))
                #
                if BnotT:
                    EaY = (HE2 - vy2) / _epsilon
                else:
                    EaY = ( (HE2 - vy2) @ numpy.linalg.inv(Ta) ) / numpy.sqrt(__m-1)
                #
                GradJ = numpy.ravel(vw[:,None] - EaY.transpose() @ (RI * ( Ynpu - vy1 )))
                mH = numpy.eye(__m) + EaY.transpose() @ (RI * EaY)
                Deltaw = - numpy.linalg.solve(mH,GradJ)
                #
                vw = vw + Deltaw
                #
                if not BnotT:
                    Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                #
                __j = __j + 1
            #
            A2 = EnsembleOfAnomalies( E2 )
            #
            if BnotT:
                Ta = numpy.real(scipy.linalg.sqrtm(numpy.linalg.inv( mH )))
                A2 = numpy.sqrt(__m-1) * A2 @ Ta / _epsilon
            #
            Xn = vx2 + A2
        #--------------------------
        else:
            raise ValueError("VariantM has to be chosen in the authorized methods list.")
        #
        if selfA._parameters["InflationType"] == "MultiplicativeOnAnalysisAnomalies":
            Xn = CovarianceInflation( Xn,
                selfA._parameters["InflationType"],
                selfA._parameters["InflationFactor"],
                )
        #
        Xa = Xn.mean(axis=1, dtype=mfp).astype('float').reshape((__n,-1))
        #--------------------------
        #
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("APosterioriCovariance") \
            or selfA._toStore("InnovationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentAnalysis") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            _HXa = numpy.asmatrix(numpy.ravel( H((Xa, Un)) )).T
            _Innovation = Ynpu - _HXa
        #
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        # ---> avec analysis
        selfA.StoredVariables["Analysis"].store( Xa )
        if selfA._toStore("SimulatedObservationAtCurrentAnalysis"):
            selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"].store( _HXa )
        if selfA._toStore("InnovationAtCurrentAnalysis"):
            selfA.StoredVariables["InnovationAtCurrentAnalysis"].store( _Innovation )
        # ---> avec current state
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CurrentState"):
            selfA.StoredVariables["CurrentState"].store( Xn )
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store( E2 )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( E2 - Xa )
        if selfA._toStore("InnovationAtCurrentState"):
            selfA.StoredVariables["InnovationAtCurrentState"].store( - HE2 + Ynpu.reshape((__p,-1)) )
        if selfA._toStore("SimulatedObservationAtCurrentState") \
            or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
            selfA.StoredVariables["SimulatedObservationAtCurrentState"].store( HE2 )
        # ---> autres
        if selfA._parameters["StoreInternalVariables"] \
            or selfA._toStore("CostFunctionJ") \
            or selfA._toStore("CostFunctionJb") \
            or selfA._toStore("CostFunctionJo") \
            or selfA._toStore("CurrentOptimum") \
            or selfA._toStore("APosterioriCovariance"):
            Jb  = float( 0.5 * (Xa - Xb).T * BI * (Xa - Xb) )
            Jo  = float( 0.5 * _Innovation.T * RI * _Innovation )
            J   = Jb + Jo
            selfA.StoredVariables["CostFunctionJb"].store( Jb )
            selfA.StoredVariables["CostFunctionJo"].store( Jo )
            selfA.StoredVariables["CostFunctionJ" ].store( J )
            #
            if selfA._toStore("IndexOfOptimum") \
                or selfA._toStore("CurrentOptimum") \
                or selfA._toStore("CostFunctionJAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJbAtCurrentOptimum") \
                or selfA._toStore("CostFunctionJoAtCurrentOptimum") \
                or selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                IndexMin = numpy.argmin( selfA.StoredVariables["CostFunctionJ"][nbPreviousSteps:] ) + nbPreviousSteps
            if selfA._toStore("IndexOfOptimum"):
                selfA.StoredVariables["IndexOfOptimum"].store( IndexMin )
            if selfA._toStore("CurrentOptimum"):
                selfA.StoredVariables["CurrentOptimum"].store( selfA.StoredVariables["Analysis"][IndexMin] )
            if selfA._toStore("SimulatedObservationAtCurrentOptimum"):
                selfA.StoredVariables["SimulatedObservationAtCurrentOptimum"].store( selfA.StoredVariables["SimulatedObservationAtCurrentAnalysis"][IndexMin] )
            if selfA._toStore("CostFunctionJbAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJbAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJb"][IndexMin] )
            if selfA._toStore("CostFunctionJoAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJoAtCurrentOptimum"].store( selfA.StoredVariables["CostFunctionJo"][IndexMin] )
            if selfA._toStore("CostFunctionJAtCurrentOptimum"):
                selfA.StoredVariables["CostFunctionJAtCurrentOptimum" ].store( selfA.StoredVariables["CostFunctionJ" ][IndexMin] )
        if selfA._toStore("APosterioriCovariance"):
            Eai = EnsembleOfAnomalies( Xn ) / numpy.sqrt(__m-1) # Anomalies
            Pn = Eai @ Eai.T
            Pn = 0.5 * (Pn + Pn.T)
            selfA.StoredVariables["APosterioriCovariance"].store( Pn )
        if selfA._parameters["EstimationOf"] == "Parameters" \
            and J < previousJMinimum:
            previousJMinimum    = J
            XaMin               = Xa
            if selfA._toStore("APosterioriCovariance"):
                covarianceXaMin = Pn
    #
    # Stockage final supplémentaire de l'optimum en estimation de paramètres
    # ----------------------------------------------------------------------
    if selfA._parameters["EstimationOf"] == "Parameters":
        selfA.StoredVariables["CurrentIterationNumber"].store( len(selfA.StoredVariables["Analysis"]) )
        selfA.StoredVariables["Analysis"].store( XaMin )
        if selfA._toStore("APosterioriCovariance"):
            selfA.StoredVariables["APosterioriCovariance"].store( covarianceXaMin )
        if selfA._toStore("BMA"):
            selfA.StoredVariables["BMA"].store( numpy.ravel(Xb) - numpy.ravel(XaMin) )
    #
    return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
