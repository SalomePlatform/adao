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

__doc__ = """
    Définit les versions approximées des opérateurs tangents et adjoints.
"""
__author__ = "Jean-Philippe ARGAUD"

import os, time, copy, types, sys, logging
import math, numpy, scipy
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

def _BackgroundEnsembleGeneration( _bgcenter, _bgcovariance, _nbmembers, _withSVD = True):
    "Génération d'un ensemble d'ébauche de taille _nbmembers-1"
    # ~ numpy.random.seed(1234567)
    if _nbmembers < 1:
        raise ValueError("Number of members has to be strictly more than 1 (given number: %s)."%(str(_nbmembers),))
    if _withSVD:
        U, s, V = numpy.linalg.svd(_bgcovariance, full_matrices=False)
        _nbctl = len(_bgcenter)
        if _nbmembers > _nbctl:
            _Z = numpy.concatenate((numpy.dot(
                numpy.diag(numpy.sqrt(s[:_nbctl])), V[:_nbctl]),
                numpy.random.multivariate_normal(numpy.zeros(_nbctl),_bgcovariance,_nbmembers-1-_nbctl)), axis = 0)
        else:
            _Z = numpy.dot(numpy.diag(numpy.sqrt(s[:_nbmembers-1])), V[:_nbmembers-1])
        _Zca = _CenteredAnomalies(_Z, _nbmembers)
        BackgroundEnsemble = (_bgcenter + _Zca.T).T
    else:
        if max(abs(_bgcovariance.flatten())) > 0:
            _nbctl = len(_bgcenter)
            _Z = numpy.random.multivariate_normal(numpy.zeros(_nbctl),_bgcovariance,_nbmembers-1)
            _Zca = _CenteredAnomalies(_Z, _nbmembers)
            BackgroundEnsemble = (_bgcenter + _Zca.T).T
        else:
            BackgroundEnsemble = numpy.tile([_bgcenter],(_nbmembers,1)).T
    return BackgroundEnsemble

def _CenteredAnomalies(Zr, N):
    """
    Génère une matrice d'anomalies centrées selon les notes manuscrites de MB
    et conforme au code de PS avec eps = -1
    """
    eps = -1
    Q = numpy.eye(N-1)-numpy.ones((N-1,N-1))/numpy.sqrt(N)/(numpy.sqrt(N)-eps)
    Q = numpy.concatenate((Q, [eps*numpy.ones(N-1)/numpy.sqrt(N)]), axis=0)
    R, _ = numpy.linalg.qr(numpy.random.normal(size = (N-1,N-1)))
    Q = numpy.dot(Q,R)
    Zr = numpy.dot(Q,Zr)
    return Zr.T

def _IEnKF_cycle_Lag_1_SDA_GN(
        E0         = None,
        yObs       = None,
        RIdemi     = None,
        Mnnpu      = None,
        Hn         = None,
        variant    = "IEnKF", # IEnKF or IEKF
        iMaximum   = 15000,
        sTolerance = mfp,
        jTolerance = mfp,
        epsilonE   = 1e-5,
        nbPS       = 0,  # nbPreviousSteps
        ):
    # 201206
    if logging.getLogger().level < logging.WARNING:
        assert len(E0.shape) == 2, "Ensemble E0 is not well formed: not of shape 2!"
        assert len(RIdemi.shape) == 2, "R^{-1/2} is not well formed: not of shape 2!"
        assert variant in ("IEnKF", "IEKF"), "Variant has to be IEnKF or IEKF"
    #
    nbCtl, nbMbr = E0.shape
    nbObs = yObs.size
    #
    if logging.getLogger().level < logging.WARNING:
        assert RIdemi.shape[0] == RIdemi.shape[1] == nbObs, "R^{-1} not of good size: not of size nbObs!"
    #
    yo  = yObs.reshape((nbObs,1))
    IN  = numpy.identity(nbMbr)
    if variant == "IEnKF":
        T    = numpy.identity(nbMbr)
        Tinv = numpy.identity(nbMbr)
    x00 = numpy.mean(E0, axis = 1)
    Ah0 = E0 - x00
    Ap0 = numpy.linalg.pinv( Ah0.T.dot(Ah0) )
    if logging.getLogger().level < logging.WARNING:
        assert len(Ah0.shape) == 2, "Ensemble A0 is not well formed, of shape 2!"
        assert Ah0.shape[0] == nbCtl and Ah0.shape[1] == nbMbr, "Ensemble A0 is not well shaped!"
        assert abs(max(numpy.mean(Ah0, axis = 1))) < nbMbr*mpr, "Ensemble A0 seems not to be centered!"
    #
    def _convergence_condition(j, dx, JCurr, JPrev):
        if j > iMaximum:
            logging.debug("Convergence on maximum number of iterations per cycle, that reach the limit of %i."%iMaximum)
            return True
        #---------
        if j == 1:
            _deltaOnJ = 1.
        else:
            _deltaOnJ = abs(JCurr - JPrev) / JPrev
        if _deltaOnJ <= jTolerance:
            logging.debug("Convergence on cost decrement tolerance, that is below the threshold of %.1e."%jTolerance)
            return True
        #---------
        _deltaOnX = numpy.linalg.norm(dx)
        if _deltaOnX <= sTolerance:
            logging.debug("Convergence on norm of state correction, that is below the threshold of %.1e."%sTolerance)
            return True # En correction de l'état
        #---------
        return False
    #
    St = dict([(k,[]) for k in [
        "CurrentState", "CurrentEnsemble",
        "CostFunctionJb", "CostFunctionJo", "CostFunctionJ",
        ]])
    #
    j, convergence, JPrev = 1, False, numpy.nan
    x1 = x00
    while not convergence:
        logging.debug("Internal IEnKS step number %i"%j)
        St["CurrentState"].append( x1.squeeze() )
        if variant == "IEnKF": # Transform
            E1 = x1 + Ah0.dot(T)
        else: # IEKF
            E1 = x1 + epsilonE * Ah0
        St["CurrentEnsemble"].append( E1 )
        E2  = numpy.array([Mnnpu(_x) for _x in E1.T]).reshape((nbCtl, nbMbr)) # Evolution 1->2
        HEL = numpy.array([Hn(_x) for _x in E2.T]).T     # Observation à 2
        yLm = numpy.mean( HEL, axis = 1).reshape((nbObs,1))
        HA2 = HEL - yLm
        if variant == "IEnKF":
            HA2 = HA2.dot(Tinv)
        else:
            HA2 = HA2 / epsilonE
        RIdemidy = RIdemi.dot(yo - yLm)
        xs = RIdemidy / math.sqrt(nbMbr-1)
        ES = RIdemi.dot(HA2) / math.sqrt(nbMbr-1)
        G  = numpy.linalg.inv(IN + ES.T.dot(ES))
        xb = G.dot(ES.T.dot(xs))
        dx = Ah0.dot(xb) + Ah0.dot(G.dot(Ap0.dot(Ah0.T.dot(x00 - x1))))
        #
        Jb = float(dx.T.dot(dx))
        Jo = float(RIdemidy.T.dot(RIdemidy))
        J  = Jo + Jb
        logging.debug("Values for cost functions are: J = %.5e  Jo = %.5e  Jb = %.5e"%(J,Jo,Jb))
        St["CostFunctionJb"].append( Jb )
        St["CostFunctionJo"].append( Jo )
        St["CostFunctionJ"].append( J )
        #
        x1 = x1 + dx
        j = j + 1
        convergence = _convergence_condition(j, dx, J, JPrev)
        JPrev = J
        #
        if variant == "IEnKF":
            T    = numpy.real_if_close(scipy.linalg.sqrtm(G))
            Tinv = numpy.linalg.inv(T)
    #
    # Stocke le dernier pas
    x2 = numpy.mean( E2, axis = 1)
    if variant == "IEKF":
        A2 = E2 - x2
        A2 = A2.dot(numpy.linalg.cholesky(G)) / epsilonE
        E2 = x2 + A2
    St["CurrentState"].append( x2.squeeze() )
    St["CurrentEnsemble"].append( E2 )
    #
    IndexMin = numpy.argmin( St["CostFunctionJ"][nbPS:] ) + nbPS
    xa = St["CurrentState"][IndexMin]
    Ea = St["CurrentEnsemble"][IndexMin]
    #
    return (xa, Ea, St)

def ienkf(
        xb         = None,          # Background (None si E0)
        E0         = None,          # Background ensemble (None si xb)
        yObs       = None,          # Observation (série)
        B          = None,          # B
        RIdemi     = None,          # R^(-1/2)
        Mnnpu      = None,          # Evolution operator
        Hn         = None,          # Observation operator
        variant    = "IEnKF",       # IEnKF or IEKF
        nMembers   = 5,             # Number of members
        sMaximum   = 0,             # Number of spinup steps
        cMaximum   = 15000,         # Number of steps or cycles
        iMaximum   = 15000,         # Number of iterations per cycle
        sTolerance = mfp,           # State correction tolerance
        jTolerance = mfp,           # Cost decrement tolerance
        epsilon    = 1e-5,
        inflation  = 1.,
        nbPS       = 0,             # Number of previous steps
        setSeed    = None,
        ):
    #
    # Initial
    if setSeed is not None: numpy.random.seed(setSeed)
    if E0 is None: E0 = _BackgroundEnsembleGeneration( xb, B, nMembers)
    #
    # Spinup
    # ------
    #
    # Cycles
    # ------
    xa, Ea, Sa = [xb,], [E0,], [{}]
    for step in range(cMaximum):
        if hasattr(yObs,"store"):         Ynpu = numpy.ravel( yObs[step+1] )
        elif type(yObs) in [list, tuple]: Ynpu = numpy.ravel( yObs[step+1] )
        else:                             Ynpu = numpy.ravel( yObs )
        #
        (xa_c, Ea_c, Sa_c) = _IEnKF_cycle_Lag_1_SDA_GN(
            E0,
            Ynpu,
            RIdemi,
            Mnnpu,
            Hn,
            variant,
            iMaximum,
            sTolerance,
            jTolerance,
            epsilon,
            nbPS,
            )
        xa.append( xa_c )
        Ea.append( Ea_c )
        Sa.append( Sa_c )
        #
        # Inflation for next cycle
        E0 = xa_c + inflation * (Ea_c - xa_c)
    #
    return (xa, Ea, Sa)

def _IEnKS_cycle_Lag_L_SDA_GN(
        E0         = None,
        yObs       = None,
        RIdemi     = None,
        Mnnpu      = None,
        Hn         = None,
        method     = "Transform",
        iMaximum   = 15000,
        sTolerance = mfp,
        jTolerance = mfp,
        Lag        = 1,
        epsilon    = -1.,
        nbPS       = 0,
        ):
    # 201407 & 201905
    if logging.getLogger().level < logging.WARNING:
        assert len(E0.shape) == 2, "Ensemble E0 is not well formed: not of shape 2!"
        assert len(RIdemi.shape) == 2, "R^{-1/2} is not well formed: not of shape 2!"
        assert method in ("Transform", "Bundle"), "Method has to be Transform or Bundle"
    #
    nbCtl, nbMbr = E0.shape
    nbObs = yObs.size
    #
    if logging.getLogger().level < logging.WARNING:
        assert RIdemi.shape[0] == RIdemi.shape[1] == nbObs, "R^{-1} not of good size: not of size nbObs!"
    #
    yo  = yObs.reshape((nbObs,1))
    IN  = numpy.identity(nbMbr)
    if method == "Transform":
        T    = numpy.identity(nbMbr)
        Tinv = numpy.identity(nbMbr)
    x00 = numpy.mean(E0, axis = 1)
    Ah0 = E0 - x00
    Am0  = (1/math.sqrt(nbMbr - 1)) * Ah0
    w   = numpy.zeros((nbMbr,1))
    if logging.getLogger().level < logging.WARNING:
        assert len(Ah0.shape) == 2, "Ensemble A0 is not well formed, of shape 2!"
        assert Ah0.shape[0] == nbCtl and Ah0.shape[1] == nbMbr, "Ensemble A0 is not well shaped!"
        assert abs(max(numpy.mean(Ah0, axis = 1))) < nbMbr*mpr, "Ensemble A0 seems not to be centered!"
    #
    def _convergence_condition(j, dw, JCurr, JPrev):
        if j > iMaximum:
            logging.debug("Convergence on maximum number of iterations per cycle, that reach the limit of %i."%iMaximum)
            return True
        #---------
        if j == 1:
            _deltaOnJ = 1.
        else:
            _deltaOnJ = abs(JCurr - JPrev) / JPrev
        if _deltaOnJ <= jTolerance:
            logging.debug("Convergence on cost decrement tolerance, that is below the threshold of %.1e."%jTolerance)
            return True
        #---------
        _deltaOnW = numpy.sqrt(numpy.mean(dw.squeeze()**2))
        if _deltaOnW <= sTolerance:
            logging.debug("Convergence on norm of weights correction, that is below the threshold of %.1e."%sTolerance)
            return True # En correction des poids
        #---------
        return False
    #
    St = dict([(k,[]) for k in [
        "CurrentState", "CurrentEnsemble", "CurrentWeights",
        "CostFunctionJb", "CostFunctionJo", "CostFunctionJ",
        ]])
    #
    j, convergence, JPrev = 1, False, numpy.nan
    while not convergence:
        logging.debug("Internal IEnKS step number %i"%j)
        x0 = x00 + Am0.dot( w )
        St["CurrentState"].append( x0.squeeze() )
        if method == "Transform":
            E0 = x0 + Ah0.dot(T)
        else:
            E0 = x0 + epsilon * Am0
        St["CurrentEnsemble"].append( E0 )
        Ek = E0
        yHmean = numpy.mean(E0, axis = 1)
        for k in range(1, Lag+1):
            Ek  = numpy.array([Mnnpu(_x) for _x in Ek.T]).reshape((nbCtl, nbMbr)) # Evolution 0->L
            if method == "Transform":
                yHmean = Mnnpu(yHmean)
        HEL = numpy.array([Hn(_x) for _x in Ek.T]).T     # Observation à L
        #
        if method == "Transform":
            yLm = Hn( yHmean ).reshape((nbObs,1))
            YL = RIdemi.dot( (HEL - numpy.mean( HEL, axis = 1).reshape((nbObs,1))).dot(Tinv) ) / math.sqrt(nbMbr-1)
        else:
            yLm = numpy.mean( HEL, axis = 1).reshape((nbObs,1))
            YL = RIdemi.dot(HEL - yLm) / epsilon
        dy = RIdemi.dot(yo - yLm)
        #
        Jb = float(w.T.dot(w))
        Jo = float(dy.T.dot(dy))
        J  = Jo + Jb
        logging.debug("Values for cost functions are: J = %.5e  Jo = %.5e  Jb = %.5e"%(J,Jo,Jb))
        St["CurrentWeights"].append( w.squeeze() )
        St["CostFunctionJb"].append( Jb )
        St["CostFunctionJo"].append( Jo )
        St["CostFunctionJ"].append( J )
        if method == "Transform":
            GradJ = w - YL.T.dot(dy)
            HTild = IN + YL.T.dot(YL)
        else:
            GradJ = (nbMbr - 1)*w - YL.T.dot(RIdemi.dot(dy))
            HTild = (nbMbr - 1)*IN + YL.T.dot(RIdemi.dot(YL))
        HTild = numpy.array(HTild, dtype=float)
        dw = numpy.linalg.solve( HTild, numpy.array(GradJ, dtype=float) )
        w = w - dw
        j = j + 1
        convergence = _convergence_condition(j, dw, J, JPrev)
        JPrev = J
        #
        if method == "Transform":
            (U, s, _) = numpy.linalg.svd(HTild, full_matrices=False) # Hess = U s V
            T    = U.dot(numpy.diag(numpy.sqrt(1./s)).dot(U.T))   # T = Hess^(-1/2)
            Tinv = U.dot(numpy.diag(numpy.sqrt(s)).dot(U.T))      # Tinv = T^(-1)
    #
    # Stocke le dernier pas
    St["CurrentState"].append( numpy.mean( Ek, axis = 1).squeeze() )
    St["CurrentEnsemble"].append( Ek )
    #
    IndexMin = numpy.argmin( St["CostFunctionJ"][nbPS:] ) + nbPS
    xa = St["CurrentState"][IndexMin]
    Ea = St["CurrentEnsemble"][IndexMin]
    #
    return (xa, Ea, St)

def ienks(
        xb         = None,          # Background
        yObs       = None,          # Observation (série)
        E0         = None,          # Background ensemble
        B          = None,          # B
        RIdemi     = None,          # R^(-1/2)
        Mnnpu      = None,          # Evolution operator
        Hn         = None,          # Observation operator
        method     = "Transform",   # Bundle ou Transform
        nMembers   = 5,             # Number of members
        cMaximum   = 15000,         # Number of steps or cycles
        iMaximum   = 15000,         # Number of iterations per cycle
        sTolerance = mfp,           # Weights correction tolerance
        jTolerance = mfp,           # Cost decrement tolerance
        Lag        = 1,             # Lenght of smoothing window
        epsilon    = -1.,
        inflation  = 1.,
        nbPS       = 0,             # Number of previous steps
        setSeed    = None,
        ):
    #
    # Initial
    if setSeed is not None: numpy.random.seed(setSeed)
    if E0 is None: E0 = _BackgroundEnsembleGeneration( xb, B, nMembers)
    #
    # Spinup
    # ------
    #
    # Cycles
    # ------
    xa, Ea, Sa = [], [], []
    for i in range(Lag): # Lag void results
        xa.append([])
        Ea.append([])
        Sa.append([])
    for i in range(Lag,cMaximum):
        (xa_c, Ea_c, Sa_c) = _IEnKS_cycle_Lag_L_SDA_GN(
            E0,
            yObs[i-Lag:i],
            RIdemi,
            Mnnpu,
            Hn,
            method,
            iMaximum,
            sTolerance,
            jTolerance,
            Lag,
            epsilon,
            nbPS,
            )
        xa.append( xa_c )
        Ea.append( Ea_c )
        Sa.append( Sa_c )
        #
        # Inflation for next cycle
        E0 = xa_c + inflation * (Ea_c - xa_c)
    #
    return (xa, Ea, Sa)

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
