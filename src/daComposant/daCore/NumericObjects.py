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
    Définit les objets numériques génériques.
"""
__author__ = "Jean-Philippe ARGAUD"

import os
import copy
import types
import sys
import logging
import math
import numpy
import scipy
import itertools
import warnings
import scipy.linalg  # Py3.6
from daCore.BasicObjects import Operator, Covariance, PartialAlgorithm
from daCore.PlatformInfo import PlatformInfo, vt, vfloat

mpr = PlatformInfo().MachinePrecision()
mfp = PlatformInfo().MaximumPrecision()
# logging.getLogger().setLevel(logging.DEBUG)


# ==============================================================================
def ExecuteFunction(triplet):
    assert len(triplet) == 3, "Incorrect number of arguments"
    X, xArgs, funcrepr = triplet
    __X = numpy.ravel(X).reshape((-1, 1))
    __sys_path_tmp = sys.path
    sys.path.insert(0, funcrepr["__userFunction__path"])
    __module = __import__(funcrepr["__userFunction__modl"], globals(), locals(), [])
    __fonction = getattr(__module, funcrepr["__userFunction__name"])
    sys.path = __sys_path_tmp
    del __sys_path_tmp
    if isinstance(xArgs, dict):
        __HX = __fonction(__X, **xArgs)
    else:
        __HX = __fonction(__X)
    return numpy.ravel(__HX)


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

    __slots__ = (
        "__name",
        "__extraArgs",
        "__mpEnabled",
        "__mpWorkers",
        "__mfEnabled",
        "__rmEnabled",
        "__avoidRC",
        "__tolerBP",
        "__centeredDF",
        "__lengthRJ",
        "__listJPCP",
        "__listJPCI",
        "__listJPCR",
        "__listJPPN",
        "__listJPIN",
        "__userOperator",
        "__userFunction",
        "__increment",
        "__pool",
        "__dX",
        "__userFunction__name",
        "__userFunction__modl",
        "__userFunction__path",
    )

    def __init__(
        self,
        name="FDApproximation",
        Function=None,
        centeredDF=False,
        increment=0.01,
        dX=None,
        extraArguments=None,
        reducingMemoryUse=False,
        avoidingRedundancy=True,
        toleranceInRedundancy=1.0e-18,
        lengthOfRedundancy=-1,
        mpEnabled=False,
        mpWorkers=None,
        mfEnabled=False,
    ):
        #
        self.__name = str(name)
        self.__extraArgs = extraArguments
        #
        if mpEnabled:
            try:
                import multiprocessing  # noqa: F401

                self.__mpEnabled = True
            except ImportError:
                self.__mpEnabled = False
        else:
            self.__mpEnabled = False
        self.__mpWorkers = mpWorkers
        if self.__mpWorkers is not None and self.__mpWorkers < 1:
            self.__mpWorkers = None
        logging.debug(
            "FDA Calculs en multiprocessing : %s (nombre de processus : %s)"
            % (self.__mpEnabled, self.__mpWorkers)
        )
        #
        self.__mfEnabled = bool(mfEnabled)
        logging.debug("FDA Calculs en multifonctions : %s" % (self.__mfEnabled,))
        #
        self.__rmEnabled = bool(reducingMemoryUse)
        logging.debug("FDA Calculs avec réduction mémoire : %s" % (self.__rmEnabled,))
        #
        if avoidingRedundancy:
            self.__avoidRC = True
            self.__tolerBP = float(toleranceInRedundancy)
            self.__lengthRJ = int(lengthOfRedundancy)
            self.__listJPCP = []  # Jacobian Previous Calculated Points
            self.__listJPCI = []  # Jacobian Previous Calculated Increment
            self.__listJPCR = []  # Jacobian Previous Calculated Results
            self.__listJPPN = []  # Jacobian Previous Calculated Point Norms
            self.__listJPIN = []  # Jacobian Previous Calculated Increment Norms
        else:
            self.__avoidRC = False
        logging.debug("FDA Calculs avec réduction des doublons : %s" % self.__avoidRC)
        if self.__avoidRC:
            logging.debug(
                "FDA Tolérance de détermination des doublons : %.2e" % self.__tolerBP
            )
        #
        if self.__mpEnabled:
            if isinstance(Function, types.FunctionType):
                logging.debug("FDA Calculs en multiprocessing : FunctionType")
                self.__userFunction__name = Function.__name__
                try:
                    mod = os.path.join(
                        Function.__globals__["filepath"],
                        Function.__globals__["filename"],
                    )
                except Exception:
                    mod = os.path.abspath(Function.__globals__["__file__"])
                if not os.path.isfile(mod):
                    raise ImportError(
                        "No user defined function or method found with the name %s"
                        % (mod,)
                    )
                self.__userFunction__modl = (
                    os.path.basename(mod)
                    .replace(".pyc", "")
                    .replace(".pyo", "")
                    .replace(".py", "")
                )
                self.__userFunction__path = os.path.dirname(mod)
                del mod
                self.__userOperator = Operator(
                    name=self.__name,
                    fromMethod=Function,
                    avoidingRedundancy=self.__avoidRC,
                    inputAsMultiFunction=self.__mfEnabled,
                    extraArguments=self.__extraArgs,
                )
                self.__userFunction = (
                    self.__userOperator.appliedTo
                )  # Pour le calcul Direct
            elif isinstance(Function, types.MethodType):
                logging.debug("FDA Calculs en multiprocessing : MethodType")
                self.__userFunction__name = Function.__name__
                try:
                    mod = os.path.join(
                        Function.__globals__["filepath"],
                        Function.__globals__["filename"],
                    )
                except Exception:
                    mod = os.path.abspath(Function.__func__.__globals__["__file__"])
                if not os.path.isfile(mod):
                    raise ImportError(
                        "No user defined function or method found with the name %s"
                        % (mod,)
                    )
                self.__userFunction__modl = (
                    os.path.basename(mod)
                    .replace(".pyc", "")
                    .replace(".pyo", "")
                    .replace(".py", "")
                )
                self.__userFunction__path = os.path.dirname(mod)
                del mod
                self.__userOperator = Operator(
                    name=self.__name,
                    fromMethod=Function,
                    avoidingRedundancy=self.__avoidRC,
                    inputAsMultiFunction=self.__mfEnabled,
                    extraArguments=self.__extraArgs,
                )
                self.__userFunction = (
                    self.__userOperator.appliedTo
                )  # Pour le calcul Direct
            else:
                raise TypeError(
                    "User defined function or method has to be provided for finite differences approximation."
                )
        else:
            self.__userOperator = Operator(
                name=self.__name,
                fromMethod=Function,
                avoidingRedundancy=self.__avoidRC,
                inputAsMultiFunction=self.__mfEnabled,
                extraArguments=self.__extraArgs,
            )
            self.__userFunction = self.__userOperator.appliedTo
        #
        self.__centeredDF = bool(centeredDF)
        if abs(float(increment)) > 1.0e-15:
            self.__increment = float(increment)
        else:
            self.__increment = 0.01
        if dX is None:
            self.__dX = None
        else:
            self.__dX = numpy.ravel(dX)

    # ---------------------------------------------------------
    def __doublon__(self, __e, __l, __n, __v=None):
        __ac, __iac = False, -1
        for i in range(len(__l) - 1, -1, -1):
            if numpy.linalg.norm(__e - __l[i]) < self.__tolerBP * __n[i]:
                __ac, __iac = True, i
                if __v is not None:
                    logging.debug(
                        "FDA Cas%s déjà calculé, récupération du doublon %i"
                        % (__v, __iac)
                    )
                break
        return __ac, __iac

    # ---------------------------------------------------------
    def __listdotwith__(self, __LMatrix, __dotWith=None, __dotTWith=None):
        "Produit incrémental d'une matrice liste de colonnes avec un vecteur"
        if not isinstance(__LMatrix, (list, tuple)):
            raise TypeError(
                "Columnwise list matrix has not the proper type: %s" % type(__LMatrix)
            )
        if __dotWith is not None:
            __Idwx = numpy.ravel(__dotWith)
            assert len(__LMatrix) == __Idwx.size, "Incorrect size of elements"
            __Produit = numpy.zeros(__LMatrix[0].size)
            for i, col in enumerate(__LMatrix):
                __Produit += float(__Idwx[i]) * col
            return __Produit
        elif __dotTWith is not None:
            _Idwy = numpy.ravel(__dotTWith).T
            assert __LMatrix[0].size == _Idwy.size, "Incorrect size of elements"
            __Produit = numpy.zeros(len(__LMatrix))
            for i, col in enumerate(__LMatrix):
                __Produit[i] = vfloat(_Idwy @ col)
            return __Produit
        else:
            __Produit = None
        return __Produit

    # ---------------------------------------------------------
    def DirectOperator(self, X, **extraArgs):
        """
        Calcul du direct à l'aide de la fonction fournie.

        NB : les extraArgs sont là pour assurer la compatibilité d'appel, mais
        ne doivent pas être données ici à la fonction utilisateur.
        """
        logging.debug("FDA Calcul DirectOperator (explicite)")
        if self.__mfEnabled:
            _HX = self.__userFunction(X, argsAsSerie=True)
        else:
            _HX = numpy.ravel(self.__userFunction(numpy.ravel(X)))
        #
        return _HX

    # ---------------------------------------------------------
    def TangentMatrix(self, X, dotWith=None, dotTWith=None):
        """
        Calcul de l'opérateur tangent comme la Jacobienne par différences finies,
        c'est-à-dire le gradient de H en X. On utilise des différences finies
        directionnelles autour du point X. X est un numpy.ndarray.

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
        logging.debug("FDA   Incrément de............: %s*X" % float(self.__increment))
        logging.debug("FDA   Approximation centrée...: %s" % (self.__centeredDF))
        #
        if X is None or len(X) == 0:
            raise ValueError(
                "Nominal point X for approximate derivatives can not be None or void (given X: %s)."
                % (str(X),)
            )
        #
        _X = numpy.ravel(X)
        #
        if self.__dX is None:
            _dX = self.__increment * _X
        else:
            _dX = numpy.ravel(self.__dX)
        assert len(_X) == len(
            _dX
        ), "Inconsistent dX increment length with respect to the X one"
        assert (
            _X.size == _dX.size
        ), "Inconsistent dX increment size with respect to the X one"
        #
        if (_dX == 0.0).any():
            moyenne = _dX.mean()
            if moyenne == 0.0:
                _dX = numpy.where(_dX == 0.0, float(self.__increment), _dX)
            else:
                _dX = numpy.where(_dX == 0.0, moyenne, _dX)
        #
        __alreadyCalculated = False
        if self.__avoidRC:
            __bidon, __alreadyCalculatedP = self.__doublon__(
                _X, self.__listJPCP, self.__listJPPN, None
            )
            __bidon, __alreadyCalculatedI = self.__doublon__(
                _dX, self.__listJPCI, self.__listJPIN, None
            )
            if __alreadyCalculatedP == __alreadyCalculatedI > -1:
                __alreadyCalculated, __i = True, __alreadyCalculatedP
                logging.debug(
                    "FDA Cas J déjà calculé, récupération du doublon %i" % __i
                )
        #
        if __alreadyCalculated:
            logging.debug(
                "FDA   Calcul Jacobienne (par récupération du doublon %i)" % __i
            )
            _Jacobienne = self.__listJPCR[__i]
            logging.debug("FDA Fin du calcul de la Jacobienne")
            if dotWith is not None:
                return numpy.dot(_Jacobienne, numpy.ravel(dotWith))
            elif dotTWith is not None:
                return numpy.dot(_Jacobienne.T, numpy.ravel(dotTWith))
        else:
            logging.debug("FDA   Calcul Jacobienne (explicite)")
            if self.__centeredDF:
                #
                if self.__mpEnabled and not self.__mfEnabled:
                    funcrepr = {
                        "__userFunction__path": self.__userFunction__path,
                        "__userFunction__modl": self.__userFunction__modl,
                        "__userFunction__name": self.__userFunction__name,
                    }
                    _jobs = []
                    for i in range(len(_dX)):
                        _dXi = _dX[i]
                        _X_plus_dXi = numpy.array(_X, dtype=float)
                        _X_plus_dXi[i] = _X[i] + _dXi
                        _X_moins_dXi = numpy.array(_X, dtype=float)
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _jobs.append((_X_plus_dXi, self.__extraArgs, funcrepr))
                        _jobs.append((_X_moins_dXi, self.__extraArgs, funcrepr))
                    #
                    import multiprocessing

                    self.__pool = multiprocessing.Pool(self.__mpWorkers)
                    _HX_plusmoins_dX = self.__pool.map(ExecuteFunction, _jobs)
                    self.__pool.close()
                    self.__pool.join()
                    #
                    _Jacobienne = []
                    for i in range(len(_dX)):
                        _Jacobienne.append(
                            numpy.ravel(
                                _HX_plusmoins_dX[2 * i] - _HX_plusmoins_dX[2 * i + 1]
                            )
                            / (2.0 * _dX[i])
                        )
                    #
                elif self.__mfEnabled:
                    _xserie = []
                    for i in range(len(_dX)):
                        _dXi = _dX[i]
                        _X_plus_dXi = numpy.array(_X, dtype=float)
                        _X_plus_dXi[i] = _X[i] + _dXi
                        _X_moins_dXi = numpy.array(_X, dtype=float)
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _xserie.append(_X_plus_dXi)
                        _xserie.append(_X_moins_dXi)
                    #
                    _HX_plusmoins_dX = self.DirectOperator(_xserie)
                    #
                    _Jacobienne = []
                    for i in range(len(_dX)):
                        _Jacobienne.append(
                            numpy.ravel(
                                _HX_plusmoins_dX[2 * i] - _HX_plusmoins_dX[2 * i + 1]
                            )
                            / (2.0 * _dX[i])
                        )
                    #
                else:
                    _Jacobienne = []
                    for i in range(_dX.size):
                        _dXi = _dX[i]
                        _X_plus_dXi = numpy.array(_X, dtype=float)
                        _X_plus_dXi[i] = _X[i] + _dXi
                        _X_moins_dXi = numpy.array(_X, dtype=float)
                        _X_moins_dXi[i] = _X[i] - _dXi
                        #
                        _HX_plus_dXi = self.DirectOperator(_X_plus_dXi)
                        _HX_moins_dXi = self.DirectOperator(_X_moins_dXi)
                        #
                        _Jacobienne.append(
                            numpy.ravel(_HX_plus_dXi - _HX_moins_dXi) / (2.0 * _dXi)
                        )
                #
            else:
                #
                if self.__mpEnabled and not self.__mfEnabled:
                    funcrepr = {
                        "__userFunction__path": self.__userFunction__path,
                        "__userFunction__modl": self.__userFunction__modl,
                        "__userFunction__name": self.__userFunction__name,
                    }
                    _jobs = []
                    _jobs.append((_X, self.__extraArgs, funcrepr))
                    for i in range(len(_dX)):
                        _X_plus_dXi = numpy.array(_X, dtype=float)
                        _X_plus_dXi[i] = _X[i] + _dX[i]
                        #
                        _jobs.append((_X_plus_dXi, self.__extraArgs, funcrepr))
                    #
                    import multiprocessing

                    self.__pool = multiprocessing.Pool(self.__mpWorkers)
                    _HX_plus_dX = self.__pool.map(ExecuteFunction, _jobs)
                    self.__pool.close()
                    self.__pool.join()
                    #
                    _HX = _HX_plus_dX.pop(0)
                    #
                    _Jacobienne = []
                    for i in range(len(_dX)):
                        _Jacobienne.append(numpy.ravel((_HX_plus_dX[i] - _HX) / _dX[i]))
                    #
                elif self.__mfEnabled:
                    _xserie = []
                    _xserie.append(_X)
                    for i in range(len(_dX)):
                        _X_plus_dXi = numpy.array(_X, dtype=float)
                        _X_plus_dXi[i] = _X[i] + _dX[i]
                        #
                        _xserie.append(_X_plus_dXi)
                    #
                    _HX_plus_dX = self.DirectOperator(_xserie)
                    #
                    _HX = _HX_plus_dX.pop(0)
                    #
                    _Jacobienne = []
                    for i in range(len(_dX)):
                        _Jacobienne.append(numpy.ravel((_HX_plus_dX[i] - _HX) / _dX[i]))
                    #
                else:
                    _Jacobienne = []
                    _HX = self.DirectOperator(_X)
                    for i in range(_dX.size):
                        _dXi = _dX[i]
                        _X_plus_dXi = numpy.array(_X, dtype=float)
                        _X_plus_dXi[i] = _X[i] + _dXi
                        #
                        _HX_plus_dXi = self.DirectOperator(_X_plus_dXi)
                        #
                        _Jacobienne.append(numpy.ravel((_HX_plus_dXi - _HX) / _dXi))
            #
            if (dotWith is not None) or (dotTWith is not None):
                __Produit = self.__listdotwith__(_Jacobienne, dotWith, dotTWith)
            else:
                __Produit = None
            if __Produit is None or self.__avoidRC:
                _Jacobienne = numpy.transpose(numpy.vstack(_Jacobienne))
                if self.__avoidRC:
                    if self.__lengthRJ < 0:
                        self.__lengthRJ = 2 * _X.size
                    while len(self.__listJPCP) > self.__lengthRJ:
                        self.__listJPCP.pop(0)
                        self.__listJPCI.pop(0)
                        self.__listJPCR.pop(0)
                        self.__listJPPN.pop(0)
                        self.__listJPIN.pop(0)
                    self.__listJPCP.append(copy.copy(_X))
                    self.__listJPCI.append(copy.copy(_dX))
                    self.__listJPCR.append(copy.copy(_Jacobienne))
                    self.__listJPPN.append(numpy.linalg.norm(_X))
                    self.__listJPIN.append(numpy.linalg.norm(_Jacobienne))
            logging.debug("FDA Fin du calcul de la Jacobienne")
            if __Produit is not None:
                return __Produit
        #
        return _Jacobienne

    # ---------------------------------------------------------
    def TangentOperator(self, paire, **extraArgs):
        """
        Calcul du tangent à l'aide de la Jacobienne.

        NB : les extraArgs sont là pour assurer la compatibilité d'appel, mais
        ne doivent pas être données ici à la fonction utilisateur.
        """
        if self.__mfEnabled:
            assert len(paire) == 1, "Incorrect length of arguments"
            _paire = paire[0]
            assert len(_paire) == 2, "Incorrect number of arguments"
        else:
            assert len(paire) == 2, "Incorrect number of arguments"
            _paire = paire
        X, dX = _paire
        if dX is None or len(dX) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            _Jacobienne = self.TangentMatrix(X)
            if self.__mfEnabled:
                return [
                    _Jacobienne,
                ]
            else:
                return _Jacobienne
        else:
            #
            # Calcul de la valeur linéarisée de H en X appliqué à dX
            # ------------------------------------------------------
            _HtX = self.TangentMatrix(X, dotWith=dX)
            if self.__mfEnabled:
                return [
                    _HtX,
                ]
            else:
                return _HtX

    # ---------------------------------------------------------
    def AdjointOperator(self, paire, **extraArgs):
        """
        Calcul de l'adjoint à l'aide de la Jacobienne.

        NB : les extraArgs sont là pour assurer la compatibilité d'appel, mais
        ne doivent pas être données ici à la fonction utilisateur.
        """
        if self.__mfEnabled:
            assert len(paire) == 1, "Incorrect length of arguments"
            _paire = paire[0]
            assert len(_paire) == 2, "Incorrect number of arguments"
        else:
            assert len(paire) == 2, "Incorrect number of arguments"
            _paire = paire
        X, Y = _paire
        if Y is None or len(Y) == 0:
            #
            # Calcul de la forme matricielle si le second argument est None
            # -------------------------------------------------------------
            _JacobienneT = self.TangentMatrix(X).T
            if self.__mfEnabled:
                return [
                    _JacobienneT,
                ]
            else:
                return _JacobienneT
        else:
            #
            # Calcul de la valeur de l'adjoint en X appliqué à Y
            # --------------------------------------------------
            _HaY = self.TangentMatrix(X, dotTWith=Y)
            if self.__mfEnabled:
                return [
                    _HaY,
                ]
            else:
                return _HaY


# ==============================================================================
def SetInitialDirection(__Direction=[], __Amplitude=1.0, __Position=None):
    "Établit ou élabore une direction avec une amplitude"
    #
    if len(__Direction) == 0 and __Position is None:
        raise ValueError(
            "If initial direction is void, current position has to be given"
        )
    if abs(float(__Amplitude)) < mpr:
        raise ValueError("Amplitude of perturbation can not be zero")
    #
    if len(__Direction) > 0:
        __dX0 = numpy.asarray(__Direction)
    else:
        __dX0 = []
        __X0 = numpy.ravel(numpy.asarray(__Position))
        __mX0 = numpy.mean(__X0, dtype=mfp)
        if abs(__mX0) < 2 * mpr:
            __mX0 = 1.0  # Évite le problème de position nulle
        for v in __X0:
            if abs(v) > 1.0e-8:
                __dX0.append(numpy.random.normal(0.0, abs(v)))
            else:
                __dX0.append(numpy.random.normal(0.0, __mX0))
    #
    __dX0 = numpy.asarray(__dX0, float)  # Évite le problème d'array de taille 1
    __dX0 = numpy.ravel(__dX0)  # Redresse les vecteurs
    __dX0 = float(__Amplitude) * __dX0
    #
    return __dX0


# ==============================================================================
def EnsembleOfCenteredPerturbations(__bgCenter, __bgCovariance, __nbMembers):
    "Génération d'un ensemble de taille __nbMembers-1 d'états aléatoires centrés"
    #
    __bgCenter = numpy.ravel(__bgCenter)[:, None]
    if __nbMembers < 1:
        raise ValueError(
            "Number of members has to be strictly more than 1 (given number: %s)."
            % (str(__nbMembers),)
        )
    #
    if __bgCovariance is None:
        _Perturbations = numpy.tile(__bgCenter, __nbMembers)
    else:
        _Z = numpy.random.multivariate_normal(
            numpy.zeros(__bgCenter.size), __bgCovariance, size=__nbMembers
        ).T
        _Perturbations = numpy.tile(__bgCenter, __nbMembers) + _Z
    #
    return _Perturbations


# ==============================================================================
def EnsembleOfBackgroundPerturbations(
    __bgCenter, __bgCovariance, __nbMembers, __withSVD=True
):
    "Génération d'un ensemble de taille __nbMembers-1 d'états aléatoires centrés"

    def __CenteredRandomAnomalies(Zr, N):
        """
        Génère une matrice de N anomalies aléatoires centrées sur Zr selon les
        notes manuscrites de MB et conforme au code de PS avec eps = -1
        """
        eps = -1
        Q = numpy.identity(N - 1) - numpy.ones((N - 1, N - 1)) / numpy.sqrt(N) / (
            numpy.sqrt(N) - eps
        )
        Q = numpy.concatenate((Q, [eps * numpy.ones(N - 1) / numpy.sqrt(N)]), axis=0)
        R, _ = numpy.linalg.qr(numpy.random.normal(size=(N - 1, N - 1)))
        Q = numpy.dot(Q, R)
        Zr = numpy.dot(Q, Zr)
        return Zr.T

    #
    __bgCenter = numpy.ravel(__bgCenter).reshape((-1, 1))
    if __nbMembers < 1:
        raise ValueError(
            "Number of members has to be strictly more than 1 (given number: %s)."
            % (str(__nbMembers),)
        )
    if __bgCovariance is None:
        _Perturbations = numpy.tile(__bgCenter, __nbMembers)
    else:
        if __withSVD:
            _U, _s, _V = numpy.linalg.svd(__bgCovariance, full_matrices=False)
            _nbctl = __bgCenter.size
            if __nbMembers > _nbctl:
                _Z = numpy.concatenate(
                    (
                        numpy.dot(numpy.diag(numpy.sqrt(_s[:_nbctl])), _V[:_nbctl]),
                        numpy.random.multivariate_normal(
                            numpy.zeros(_nbctl),
                            __bgCovariance,
                            __nbMembers - 1 - _nbctl,
                        ),
                    ),
                    axis=0,
                )
            else:
                _Z = numpy.dot(
                    numpy.diag(numpy.sqrt(_s[: __nbMembers - 1])), _V[: __nbMembers - 1]
                )
            _Zca = __CenteredRandomAnomalies(_Z, __nbMembers)
            _Perturbations = __bgCenter + _Zca
        else:
            if max(abs(__bgCovariance.flatten())) > 0:
                _nbctl = __bgCenter.size
                _Z = numpy.random.multivariate_normal(
                    numpy.zeros(_nbctl), __bgCovariance, __nbMembers - 1
                )
                _Zca = __CenteredRandomAnomalies(_Z, __nbMembers)
                _Perturbations = __bgCenter + _Zca
            else:
                _Perturbations = numpy.tile(__bgCenter, __nbMembers)
    #
    return _Perturbations


# ==============================================================================
def EnsembleMean(__Ensemble):
    "Renvoie la moyenne empirique d'un ensemble"
    return (
        numpy.asarray(__Ensemble)
        .mean(axis=1, dtype=mfp)
        .astype("float")
        .reshape((-1, 1))
    )


# ==============================================================================
def EnsembleOfAnomalies(__Ensemble, __OptMean=None, __Normalisation=1.0):
    "Renvoie les anomalies centrées à partir d'un ensemble"
    if __OptMean is None:
        __Em = EnsembleMean(__Ensemble)
    else:
        __Em = numpy.ravel(__OptMean).reshape((-1, 1))
    #
    return __Normalisation * (numpy.asarray(__Ensemble) - __Em)


# ==============================================================================
def EnsembleErrorCovariance(__Ensemble, __Quick=False):
    "Renvoie l'estimation empirique de la covariance d'ensemble"
    if __Quick:
        # Covariance rapide mais rarement définie positive
        __Covariance = numpy.cov(__Ensemble)
    else:
        # Résultat souvent identique à numpy.cov, mais plus robuste
        __n, __m = numpy.asarray(__Ensemble).shape
        __Anomalies = EnsembleOfAnomalies(__Ensemble)
        # Estimation empirique
        __Covariance = (__Anomalies @ __Anomalies.T) / (__m - 1)
        # Assure la symétrie
        __Covariance = (__Covariance + __Covariance.T) * 0.5
        # Assure la positivité
        __epsilon = mpr * numpy.trace(__Covariance)
        __Covariance = __Covariance + __epsilon * numpy.identity(__n)
    #
    return __Covariance


# ==============================================================================
def SingularValuesEstimation(__Ensemble, __Using="SVDVALS"):
    "Renvoie les valeurs singulières de l'ensemble et leur carré"
    if __Using == "SVDVALS":  # Recommandé
        __sv = scipy.linalg.svdvals(__Ensemble)
        __svsq = __sv**2
    elif __Using == "SVD":
        _, __sv, _ = numpy.linalg.svd(__Ensemble)
        __svsq = __sv**2
    elif __Using == "EIG":  # Lent
        __eva, __eve = numpy.linalg.eig(__Ensemble @ __Ensemble.T)
        __svsq = numpy.sort(numpy.abs(numpy.real(__eva)))[::-1]
        __sv = numpy.sqrt(__svsq)
    elif __Using == "EIGH":
        __eva, __eve = numpy.linalg.eigh(__Ensemble @ __Ensemble.T)
        __svsq = numpy.sort(numpy.abs(numpy.real(__eva)))[::-1]
        __sv = numpy.sqrt(__svsq)
    elif __Using == "EIGVALS":
        __eva = numpy.linalg.eigvals(__Ensemble @ __Ensemble.T)
        __svsq = numpy.sort(numpy.abs(numpy.real(__eva)))[::-1]
        __sv = numpy.sqrt(__svsq)
    elif __Using == "EIGVALSH":
        __eva = numpy.linalg.eigvalsh(__Ensemble @ __Ensemble.T)
        __svsq = numpy.sort(numpy.abs(numpy.real(__eva)))[::-1]
        __sv = numpy.sqrt(__svsq)
    else:
        raise ValueError("Error in requested variant name: %s" % __Using)
    #
    __tisv = __svsq / __svsq.sum()
    __qisv = 1.0 - __svsq.cumsum() / __svsq.sum()
    # Différence à 1.e-16 : __qisv = 1. - __tisv.cumsum()
    #
    return __sv, __svsq, __tisv, __qisv


# ==============================================================================
def MaxL2NormByColumn(__Ensemble, __LcCsts=False, __IncludedPoints=[]):
    "Maximum des normes L2 calculées par colonne"
    if __LcCsts and len(__IncludedPoints) > 0:
        normes = numpy.linalg.norm(
            numpy.take(__Ensemble, __IncludedPoints, axis=0, mode="clip"),
            axis=0,
        )
    else:
        normes = numpy.linalg.norm(__Ensemble, axis=0)
    nmax = numpy.max(normes)
    imax = numpy.argmax(normes)
    return nmax, imax, normes


def MaxLinfNormByColumn(__Ensemble, __LcCsts=False, __IncludedPoints=[]):
    "Maximum des normes Linf calculées par colonne"
    if __LcCsts and len(__IncludedPoints) > 0:
        normes = numpy.linalg.norm(
            numpy.take(__Ensemble, __IncludedPoints, axis=0, mode="clip"),
            axis=0,
            ord=numpy.inf,
        )
    else:
        normes = numpy.linalg.norm(__Ensemble, axis=0, ord=numpy.inf)
    nmax = numpy.max(normes)
    imax = numpy.argmax(normes)
    return nmax, imax, normes


def InterpolationErrorByColumn(
    __Ensemble=None,
    __Basis=None,
    __Points=None,
    __M=2,  # Usage 1
    __Differences=None,  # Usage 2
    __ErrorNorm=None,  # Commun
    __LcCsts=False,
    __IncludedPoints=[],  # Commun
    __CDM=False,  # ComputeMaxDifference                        # Commun
    __RMU=False,  # ReduceMemoryUse                             # Commun
    __FTL=False,  # ForceTril                                   # Commun
):
    "Analyse des normes d'erreurs d'interpolation calculées par colonne"
    if __ErrorNorm == "L2":
        NormByColumn = MaxL2NormByColumn
    else:
        NormByColumn = MaxLinfNormByColumn
    #
    if __Differences is None and not __RMU:  # Usage 1
        if __FTL:
            rBasis = numpy.tril(__Basis[__Points, :])
        else:
            rBasis = __Basis[__Points, :]
        rEnsemble = __Ensemble[__Points, :]
        #
        if __M > 1:
            rBasis_inv = numpy.linalg.inv(rBasis)
            Interpolator = numpy.dot(__Basis, numpy.dot(rBasis_inv, rEnsemble))
        else:
            rBasis_inv = 1.0 / rBasis
            Interpolator = numpy.outer(__Basis, numpy.outer(rBasis_inv, rEnsemble))
        #
        differences = __Ensemble - Interpolator
        #
        error, nbr, _ = NormByColumn(differences, __LcCsts, __IncludedPoints)
        #
        if __CDM:
            maxDifference = differences[:, nbr]
        #
    elif __Differences is None and __RMU:  # Usage 1
        if __FTL:
            rBasis = numpy.tril(__Basis[__Points, :])
        else:
            rBasis = __Basis[__Points, :]
        rEnsemble = __Ensemble[__Points, :]
        #
        if __M > 1:
            rBasis_inv = numpy.linalg.inv(rBasis)
            rCoordinates = numpy.dot(rBasis_inv, rEnsemble)
        else:
            rBasis_inv = 1.0 / rBasis
            rCoordinates = numpy.outer(rBasis_inv, rEnsemble)
        #
        error = 0.0
        nbr = -1
        for iCol in range(__Ensemble.shape[1]):
            if __M > 1:
                iDifference = __Ensemble[:, iCol] - numpy.dot(
                    __Basis, rCoordinates[:, iCol]
                )
            else:
                iDifference = __Ensemble[:, iCol] - numpy.ravel(
                    numpy.outer(__Basis, rCoordinates[:, iCol])
                )
            #
            normDifference, _, _ = NormByColumn(iDifference, __LcCsts, __IncludedPoints)
            #
            if normDifference > error:
                error = normDifference
                nbr = iCol
        #
        if __CDM:
            maxDifference = __Ensemble[:, nbr] - numpy.dot(
                __Basis, rCoordinates[:, nbr]
            )
        #
    else:  # Usage 2
        differences = __Differences
        #
        error, nbr, _ = NormByColumn(differences, __LcCsts, __IncludedPoints)
        #
        if __CDM:
            # faire cette variable intermédiaire coûte cher
            maxDifference = differences[:, nbr]
    #
    if __CDM:
        return error, nbr, maxDifference
    else:
        return error, nbr


# ==============================================================================
def EnsemblePerturbationWithGivenCovariance(__Ensemble, __Covariance, __Seed=None):
    "Ajout d'une perturbation à chaque membre d'un ensemble selon une covariance prescrite"
    if hasattr(__Covariance, "assparsematrix"):
        if (abs(__Ensemble).mean() > mpr) and (
            abs(__Covariance.assparsematrix()) / abs(__Ensemble).mean() < mpr
        ).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
        if (abs(__Ensemble).mean() <= mpr) and (
            abs(__Covariance.assparsematrix()) < mpr
        ).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
    else:
        if (abs(__Ensemble).mean() > mpr) and (
            abs(__Covariance) / abs(__Ensemble).mean() < mpr
        ).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
        if (abs(__Ensemble).mean() <= mpr) and (abs(__Covariance) < mpr).all():
            # Traitement d'une covariance nulle ou presque
            return __Ensemble
    #
    __n, __m = __Ensemble.shape
    if __Seed is not None:
        numpy.random.seed(__Seed)
    #
    if hasattr(__Covariance, "isscalar") and __Covariance.isscalar():
        # Traitement d'une covariance multiple de l'identité
        __zero = 0.0
        __std = numpy.sqrt(__Covariance.assparsematrix())
        __Ensemble += numpy.random.normal(__zero, __std, size=(__m, __n)).T
    #
    elif hasattr(__Covariance, "isvector") and __Covariance.isvector():
        # Traitement d'une covariance diagonale avec variances non identiques
        __zero = numpy.zeros(__n)
        __std = numpy.sqrt(__Covariance.assparsematrix())
        __Ensemble += numpy.asarray(
            [numpy.random.normal(__zero, __std) for i in range(__m)]
        ).T
    #
    elif hasattr(__Covariance, "ismatrix") and __Covariance.ismatrix():
        # Traitement d'une covariance pleine
        __Ensemble += numpy.random.multivariate_normal(
            numpy.zeros(__n), __Covariance.asfullmatrix(__n), size=__m
        ).T
    #
    elif isinstance(__Covariance, numpy.ndarray):
        # Traitement d'une covariance numpy pleine, sachant qu'on arrive ici en dernier
        __Ensemble += numpy.random.multivariate_normal(
            numpy.zeros(__n), __Covariance, size=__m
        ).T
    #
    else:
        raise ValueError(
            "Error in ensemble perturbation with inadequate covariance specification"
        )
    #
    return __Ensemble


# ==============================================================================
def CovarianceInflation(
    __InputCovOrEns, __InflationType=None, __InflationFactor=None, __BackgroundCov=None
):
    """
    Inflation applicable soit sur Pb ou Pa, soit sur les ensembles EXb ou EXa

    Synthèse : Hunt 2007, section 2.3.5
    """
    if __InflationFactor is None:
        return __InputCovOrEns
    else:
        __InflationFactor = float(__InflationFactor)
    #
    __InputCovOrEns = numpy.asarray(__InputCovOrEns)
    if __InputCovOrEns.size == 0:
        return __InputCovOrEns
    #
    if __InflationType in [
        "MultiplicativeOnAnalysisCovariance",
        "MultiplicativeOnBackgroundCovariance",
    ]:
        if __InflationFactor < 1.0:
            raise ValueError(
                "Inflation factor for multiplicative inflation has to be greater or equal than 1."
            )
        if __InflationFactor < 1.0 + mpr:  # No inflation = 1
            return __InputCovOrEns
        __OutputCovOrEns = __InflationFactor**2 * __InputCovOrEns
    #
    elif __InflationType in [
        "MultiplicativeOnAnalysisAnomalies",
        "MultiplicativeOnBackgroundAnomalies",
    ]:
        if __InflationFactor < 1.0:
            raise ValueError(
                "Inflation factor for multiplicative inflation has to be greater or equal than 1."
            )
        if __InflationFactor < 1.0 + mpr:  # No inflation = 1
            return __InputCovOrEns
        __InputCovOrEnsMean = __InputCovOrEns.mean(axis=1, dtype=mfp).astype("float")
        __OutputCovOrEns = __InputCovOrEnsMean[:, numpy.newaxis] + __InflationFactor * (
            __InputCovOrEns - __InputCovOrEnsMean[:, numpy.newaxis]
        )
    #
    elif __InflationType in [
        "AdditiveOnAnalysisCovariance",
        "AdditiveOnBackgroundCovariance",
    ]:
        if __InflationFactor < 0.0:
            raise ValueError(
                "Inflation factor for additive inflation has to be greater or equal than 0."
            )
        if __InflationFactor < mpr:  # No inflation = 0
            return __InputCovOrEns
        __n, __m = __InputCovOrEns.shape
        if __n != __m:
            raise ValueError(
                "Additive inflation can only be applied to squared (covariance) matrix."
            )
        __tr = __InputCovOrEns.trace() / __n
        if __InflationFactor > __tr:
            raise ValueError(
                "Inflation factor for additive inflation has to be small over %.0e."
                % __tr
            )
        __OutputCovOrEns = (
            1.0 - __InflationFactor
        ) * __InputCovOrEns + __InflationFactor * numpy.identity(__n)
    #
    elif __InflationType == "HybridOnBackgroundCovariance":
        if __InflationFactor < 0.0:
            raise ValueError(
                "Inflation factor for hybrid inflation has to be greater or equal than 0."
            )
        if __InflationFactor < mpr:  # No inflation = 0
            return __InputCovOrEns
        __n, __m = __InputCovOrEns.shape
        if __n != __m:
            raise ValueError(
                "Additive inflation can only be applied to squared (covariance) matrix."
            )
        if __BackgroundCov is None:
            raise ValueError(
                "Background covariance matrix B has to be given for hybrid inflation."
            )
        if __InputCovOrEns.shape != __BackgroundCov.shape:
            raise ValueError(
                "Ensemble covariance matrix has to be of same size than background covariance matrix B."
            )
        __OutputCovOrEns = (
            1.0 - __InflationFactor
        ) * __InputCovOrEns + __InflationFactor * __BackgroundCov
    #
    elif __InflationType == "Relaxation":
        raise NotImplementedError("Relaxation inflation type not implemented")
    #
    else:
        raise ValueError(
            "Error in inflation type, '%s' is not a valid keyword." % __InflationType
        )
    #
    return __OutputCovOrEns


# ==============================================================================
def HessienneEstimation(__selfA, __nb, __HaM, __HtM, __BI, __RI):
    "Estimation de la Hessienne"
    #
    __HessienneI = []
    for i in range(int(__nb)):
        __ee = numpy.zeros((__nb, 1))
        __ee[i] = 1.0
        __HtEE = __HtM[:,i].reshape((-1,1))
        __HessienneI.append(numpy.ravel(__BI * __ee + __HaM * (__RI * __HtEE)))
    #
    __A = numpy.linalg.inv(numpy.array(__HessienneI))
    __A = (__A + __A.T) * 0.5  # Symétrie
    __A = __A + mpr * numpy.trace(__A) * numpy.identity(__nb)  # Positivité
    #
    if min(__A.shape) != max(__A.shape):
        raise ValueError(
            "The %s a posteriori covariance matrix A" % (__selfA._name,)
            + " is of shape %s, despites it has to be a" % (str(__A.shape),)
            + " squared matrix. There is an error in the observation operator,"
            + " please check it."
        )
    if (numpy.diag(__A) < 0).any():
        raise ValueError(
            "The %s a posteriori covariance matrix A" % (__selfA._name,)
            + " has at least one negative value on its diagonal. There is an"
            + " error in the observation operator, please check it."
        )
    if (
        logging.getLogger().level < logging.WARNING
    ):  # La vérification n'a lieu qu'en debug
        try:
            numpy.linalg.cholesky(__A)
            logging.debug(
                "%s La matrice de covariance a posteriori A est bien symétrique définie positive."
                % (__selfA._name,)
            )
        except Exception:
            raise ValueError(
                "The %s a posteriori covariance matrix A" % (__selfA._name,)
                + " is not symmetric positive-definite. Please check your a"
                + " priori covariances and your observation operator."
            )
    #
    return __A


# ==============================================================================
def QuantilesEstimations(selfA, A, Xa, HXa=None, Hm=None, HtM=None):
    "Estimation des quantiles a posteriori à partir de A>0 (selfA est modifié)"
    nbsamples = selfA._parameters["NumberOfSamplesForQuantiles"]
    #
    # Traitement des bornes
    if "StateBoundsForQuantiles" in selfA._parameters:
        LBounds = selfA._parameters["StateBoundsForQuantiles"]  # Prioritaire
    elif "Bounds" in selfA._parameters:
        LBounds = selfA._parameters["Bounds"]  # Défaut raisonnable
    else:
        LBounds = None
    if LBounds is not None:
        LBounds = ForceNumericBounds(LBounds)
    __Xa = numpy.ravel(Xa)
    #
    # Échantillonnage des états
    YfQ = None
    EXr = None
    for i in range(nbsamples):
        if (
            selfA._parameters["SimulationForQuantiles"] == "Linear"
            and HtM is not None
            and HXa is not None
        ):
            dXr = (numpy.random.multivariate_normal(__Xa, A) - __Xa).reshape((-1, 1))
            if LBounds is not None:  # "EstimateProjection" par défaut
                dXr = numpy.max(
                    numpy.hstack(
                        (dXr, LBounds[:, 0].reshape((-1, 1))) - __Xa.reshape((-1, 1))
                    ),
                    axis=1,
                )
                dXr = numpy.min(
                    numpy.hstack(
                        (dXr, LBounds[:, 1].reshape((-1, 1))) - __Xa.reshape((-1, 1))
                    ),
                    axis=1,
                )
            dYr = HtM @ dXr
            Yr = HXa.reshape((-1, 1)) + dYr
            if selfA._toStore("SampledStateForQuantiles"):
                Xr = __Xa + numpy.ravel(dXr)
        elif (
            selfA._parameters["SimulationForQuantiles"] == "NonLinear"
            and Hm is not None
        ):
            Xr = numpy.random.multivariate_normal(__Xa, A)
            if LBounds is not None:  # "EstimateProjection" par défaut
                Xr = numpy.max(
                    numpy.hstack((Xr.reshape((-1, 1)), LBounds[:, 0].reshape((-1, 1)))),
                    axis=1,
                )
                Xr = numpy.min(
                    numpy.hstack((Xr.reshape((-1, 1)), LBounds[:, 1].reshape((-1, 1)))),
                    axis=1,
                )
            Yr = numpy.asarray(Hm(Xr))
        else:
            raise ValueError("Quantile simulations has only to be Linear or NonLinear.")
        #
        if YfQ is None:
            YfQ = Yr.reshape((-1, 1))
            if selfA._toStore("SampledStateForQuantiles"):
                EXr = Xr.reshape((-1, 1))
        else:
            YfQ = numpy.hstack((YfQ, Yr.reshape((-1, 1))))
            if selfA._toStore("SampledStateForQuantiles"):
                EXr = numpy.hstack((EXr, Xr.reshape((-1, 1))))
    #
    # Extraction des quantiles
    YfQ.sort(axis=-1)
    YQ = None
    for quantile in selfA._parameters["Quantiles"]:
        if not (0.0 <= float(quantile) <= 1.0):
            continue
        indice = int(nbsamples * float(quantile) - 1.0 / nbsamples)
        if YQ is None:
            YQ = YfQ[:, indice].reshape((-1, 1))
        else:
            YQ = numpy.hstack((YQ, YfQ[:, indice].reshape((-1, 1))))
    if YQ is not None:  # Liste non vide de quantiles
        selfA.StoredVariables["SimulationQuantiles"].store(YQ)
    if selfA._toStore("SampledStateForQuantiles"):
        selfA.StoredVariables["SampledStateForQuantiles"].store(EXr)
    #
    return 0


# ==============================================================================
def ForceNumericBounds(__Bounds, __infNumbers=True):
    "Force les bornes à être des valeurs numériques, sauf si globalement None"
    # Conserve une valeur par défaut à None s'il n'y a pas de bornes
    if __Bounds is None:
        return None
    #
    # Converti toutes les bornes individuelles None à +/- l'infini chiffré
    __Bounds = numpy.asarray(__Bounds, dtype=float).reshape((-1, 2))
    if len(__Bounds.shape) != 2 or __Bounds.shape[0] == 0 or __Bounds.shape[1] != 2:
        raise ValueError(
            "Incorrectly shaped bounds data (effective shape is %s)" % (__Bounds.shape,)
        )
    if __infNumbers:
        __Bounds[numpy.isnan(__Bounds[:, 0]), 0] = -float("inf")
        __Bounds[numpy.isnan(__Bounds[:, 1]), 1] = float("inf")
    else:
        __Bounds[numpy.isnan(__Bounds[:, 0]), 0] = -sys.float_info.max
        __Bounds[numpy.isnan(__Bounds[:, 1]), 1] = sys.float_info.max
    return __Bounds


# ==============================================================================
def RecentredBounds(__Bounds, __Center, __Scale=None):
    "Recentre les bornes autour de 0, sauf si globalement None"
    # Conserve une valeur par défaut à None s'il n'y a pas de bornes
    if __Bounds is None:
        return None
    #
    if __Scale is None:
        # Recentre les valeurs numériques de bornes
        return ForceNumericBounds(__Bounds) - numpy.ravel(__Center).reshape((-1, 1))
    else:
        # Recentre les valeurs numériques de bornes et change l'échelle par une matrice
        return __Scale @ (
            ForceNumericBounds(__Bounds, False) - numpy.ravel(__Center).reshape((-1, 1))
        )


# ==============================================================================
def ApplyBounds(__Vector, __Bounds, __newClip=True):
    "Applique des bornes numériques à un point"
    # Conserve une valeur par défaut s'il n'y a pas de bornes
    if __Bounds is None:
        return __Vector
    #
    if not isinstance(__Vector, numpy.ndarray):  # Is an array
        raise ValueError("Incorrect array definition of vector data")
    if not isinstance(__Bounds, numpy.ndarray):  # Is an array
        raise ValueError("Incorrect array definition of bounds data")
    if 2 * __Vector.size != __Bounds.size:  # Is a 2 column array of vector length
        raise ValueError(
            "Incorrect bounds number (%i) to be applied for this vector (of size %i)"
            % (__Bounds.size, __Vector.size)
        )
    if len(__Bounds.shape) != 2 or min(__Bounds.shape) <= 0 or __Bounds.shape[1] != 2:
        raise ValueError("Incorrectly shaped bounds data")
    #
    if __newClip:
        __Vector = __Vector.clip(
            __Bounds[:, 0].reshape(__Vector.shape),
            __Bounds[:, 1].reshape(__Vector.shape),
        )
    else:
        __Vector = numpy.max(
            numpy.hstack((__Vector.reshape((-1, 1)), numpy.asmatrix(__Bounds)[:, 0])),
            axis=1,
        )
        __Vector = numpy.min(
            numpy.hstack((__Vector.reshape((-1, 1)), numpy.asmatrix(__Bounds)[:, 1])),
            axis=1,
        )
        __Vector = numpy.asarray(__Vector)
    #
    return __Vector


# ==============================================================================
def VariablesAndIncrementsBounds(
    __Bounds, __BoxBounds, __Xini, __Name, __Multiplier=1.0
):
    __Bounds = ForceNumericBounds(__Bounds)
    __BoxBounds = ForceNumericBounds(__BoxBounds)
    if __Bounds is None and __BoxBounds is None:
        raise ValueError(
            "Algorithm %s requires bounds on all variables (by Bounds), or on all"
            % (__Name,)
            + " variable increments (by BoxBounds), or both, to be explicitly given."
        )
    elif __Bounds is None and __BoxBounds is not None:
        __Bounds = __BoxBounds
        logging.debug(
            "%s Definition of parameter bounds from current parameter increment bounds"
            % (__Name,)
        )
    elif __Bounds is not None and __BoxBounds is None:
        __BoxBounds = __Multiplier * (
            __Bounds - __Xini.reshape((-1, 1))
        )  # "M * [Xmin,Xmax]-Xini"
        logging.debug(
            "%s Definition of parameter increment bounds from current parameter bounds"
            % (__Name,)
        )
    return __Bounds, __BoxBounds


# ==============================================================================
def Apply3DVarRecentringOnEnsemble(__EnXn, __EnXf, __Ynpu, __HO, __R, __B, __SuppPars):
    "Recentre l'ensemble Xn autour de l'analyse 3DVAR"
    __Betaf = __SuppPars["HybridCovarianceEquilibrium"]
    #
    Xf = EnsembleMean(__EnXf)
    Pf = Covariance(asCovariance=EnsembleErrorCovariance(__EnXf))
    Pf = (1 - __Betaf) * __B.asfullmatrix(Xf.size) + __Betaf * Pf
    #
    selfB = PartialAlgorithm("3DVAR")
    selfB._parameters["Minimizer"] = "LBFGSB"
    selfB._parameters["MaximumNumberOfIterations"] = __SuppPars[
        "HybridMaximumNumberOfIterations"
    ]
    selfB._parameters["CostDecrementTolerance"] = __SuppPars[
        "HybridCostDecrementTolerance"
    ]
    selfB._parameters["ProjectedGradientTolerance"] = -1
    selfB._parameters["GradientNormTolerance"] = 1.0e-05
    selfB._parameters["StoreInternalVariables"] = False
    selfB._parameters["optiprint"] = -1
    selfB._parameters["optdisp"] = 0
    selfB._parameters["Bounds"] = None
    selfB._parameters["InitializationPoint"] = Xf
    from daAlgorithms.Atoms import std3dvar

    std3dvar.std3dvar(selfB, Xf, __Ynpu, None, __HO, None, __R, Pf)
    Xa = selfB.get("Analysis")[-1].reshape((-1, 1))
    del selfB
    #
    return Xa + EnsembleOfAnomalies(__EnXn)


# ==============================================================================
def GenerateRandomPointInHyperSphere(__Center, __Radius):
    "Génère un point aléatoire uniformément à l'intérieur d'une hyper-sphère"
    __Dimension = numpy.asarray(__Center).size
    __GaussDelta = numpy.random.normal(0, 1, size=__Center.shape)
    __VectorNorm = numpy.linalg.norm(__GaussDelta)
    __PointOnHS = __Radius * (__GaussDelta / __VectorNorm)
    __MoveInHS = math.exp(math.log(numpy.random.uniform()) / __Dimension)  # rand()**1/n
    __PointInHS = __MoveInHS * __PointOnHS
    return __Center + __PointInHS


# ==============================================================================
class GenerateWeightsAndSigmaPoints(object):
    "Génère les points sigma et les poids associés"

    def __init__(
        self, Nn=0, EO="State", VariantM="UKF", Alpha=None, Beta=2.0, Kappa=0.0
    ):
        self.Nn = int(Nn)
        self.Alpha = numpy.longdouble(Alpha)
        self.Beta = numpy.longdouble(Beta)
        if abs(Kappa) < 2 * mpr:
            if EO == "Parameters" and VariantM == "UKF":
                self.Kappa = 3 - self.Nn
            else:  # EO == "State":
                self.Kappa = 0
        else:
            self.Kappa = Kappa
        self.Kappa = numpy.longdouble(self.Kappa)
        self.Lambda = self.Alpha**2 * (self.Nn + self.Kappa) - self.Nn
        self.Gamma = self.Alpha * numpy.sqrt(self.Nn + self.Kappa)
        # Rq.: Gamma = sqrt(n+Lambda) = Alpha*sqrt(n+Kappa)
        assert (
            0.0 < self.Alpha <= 1.0
        ), "Alpha has to be between 0 strictly and 1 included"
        #
        if VariantM == "UKF":
            self.Wm, self.Wc, self.SC = self.__UKF2000()
        elif VariantM == "S3F":
            self.Wm, self.Wc, self.SC = self.__S3F2022()
        elif VariantM == "MSS":
            self.Wm, self.Wc, self.SC = self.__MSS2011()
        elif VariantM == "5OS":
            self.Wm, self.Wc, self.SC = self.__5OS2002()
        else:
            raise ValueError('Variant "%s" is not a valid one.' % VariantM)

    def __UKF2000(self):
        "Standard Set, Julier et al. 2000 (aka Canonical UKF)"
        # Rq.: W^{(m)}_{i=/=0} = 1. / (2.*(n + Lambda))
        Winn = 1.0 / (2.0 * (self.Nn + self.Kappa) * self.Alpha**2)
        Ww = []
        Ww.append(0.0)
        for point in range(2 * self.Nn):
            Ww.append(Winn)
        # Rq.: LsLpL = Lambda / (n + Lambda)
        LsLpL = 1.0 - self.Nn / (self.Alpha**2 * (self.Nn + self.Kappa))
        Wm = numpy.array(Ww)
        Wm[0] = LsLpL
        Wc = numpy.array(Ww)
        Wc[0] = LsLpL + (1.0 - self.Alpha**2 + self.Beta)
        # OK: assert abs(Wm.sum()-1.) < self.Nn*mpr, "UKF ill-conditioned %s >= %s"%(abs(Wm.sum()-1.), self.Nn*mpr)
        #
        SC = numpy.zeros((self.Nn, len(Ww)))
        for ligne in range(self.Nn):
            it = ligne + 1
            SC[ligne, it] = self.Gamma
            SC[ligne, self.Nn + it] = -self.Gamma
        #
        return Wm, Wc, SC

    def __S3F2022(self):
        "Scaled Spherical Simplex Set, Papakonstantinou et al. 2022"
        # Rq.: W^{(m)}_{i=/=0} = (n + Kappa) / ((n + Lambda) * (n + 1 + Kappa))
        Winn = 1.0 / ((self.Nn + 1.0 + self.Kappa) * self.Alpha**2)
        Ww = []
        Ww.append(0.0)
        for point in range(self.Nn + 1):
            Ww.append(Winn)
        # Rq.: LsLpL = Lambda / (n + Lambda)
        LsLpL = 1.0 - self.Nn / (self.Alpha**2 * (self.Nn + self.Kappa))
        Wm = numpy.array(Ww)
        Wm[0] = LsLpL
        Wc = numpy.array(Ww)
        Wc[0] = LsLpL + (1.0 - self.Alpha**2 + self.Beta)
        # OK: assert abs(Wm.sum()-1.) < self.Nn*mpr, "S3F ill-conditioned %s >= %s"%(abs(Wm.sum()-1.), self.Nn*mpr)
        #
        SC = numpy.zeros((self.Nn, len(Ww)))
        for ligne in range(self.Nn):
            it = ligne + 1
            q_t = it / math.sqrt(it * (it + 1) * Winn)
            SC[ligne, 1 : it + 1] = -q_t / it  # noqa: E203
            SC[ligne, it + 1] = q_t
        #
        return Wm, Wc, SC

    def __MSS2011(self):
        "Minimum Set, Menegaz et al. 2011"
        rho2 = (1 - self.Alpha) / self.Nn
        Cc = numpy.real(scipy.linalg.sqrtm(numpy.identity(self.Nn) - rho2))
        Ww = (
            self.Alpha
            * rho2
            * scipy.linalg.inv(Cc)
            @ numpy.ones(self.Nn)
            @ scipy.linalg.inv(Cc.T)
        )
        Wm = Wc = numpy.concatenate((Ww, [self.Alpha]))
        # OK: assert abs(Wm.sum()-1.) < self.Nn*mpr, "MSS ill-conditioned %s >= %s"%(abs(Wm.sum()-1.), self.Nn*mpr)
        Wm = Wc = Wm / numpy.sum(Wm)  # Renormalisation explicite
        #
        # inv(sqrt(W)) = diag(inv(sqrt(W)))
        SC1an = Cc @ numpy.diag(1.0 / numpy.sqrt(Ww))
        SCnpu = (-numpy.sqrt(rho2) / numpy.sqrt(self.Alpha)) * numpy.ones(
            self.Nn
        ).reshape((-1, 1))
        SC = numpy.concatenate((SC1an, SCnpu), axis=1)
        #
        return Wm, Wc, SC

    def __5OS2002(self):
        "Fifth Order Set, Lerner 2002"
        Ww = []
        for point in range(2 * self.Nn):
            Ww.append((4.0 - self.Nn) / 18.0)
        for point in range(2 * self.Nn, 2 * self.Nn**2):
            Ww.append(1.0 / 36.0)
        Ww.append((self.Nn**2 - 7 * self.Nn) / 18.0 + 1.0)
        Wm = Wc = numpy.array(Ww)
        # OK: assert abs(Wm.sum()-1.) < self.Nn*mpr, "5OS ill-conditioned %s >= %s"%(abs(Wm.sum()-1.), self.Nn*mpr)
        #
        xi1n = numpy.diag(math.sqrt(3) * numpy.ones(self.Nn))
        xi2n = numpy.diag(-math.sqrt(3) * numpy.ones(self.Nn))
        #
        xi3n1 = numpy.zeros((int((self.Nn - 1) * self.Nn / 2), self.Nn), dtype=float)
        xi3n2 = numpy.zeros((int((self.Nn - 1) * self.Nn / 2), self.Nn), dtype=float)
        xi4n1 = numpy.zeros((int((self.Nn - 1) * self.Nn / 2), self.Nn), dtype=float)
        xi4n2 = numpy.zeros((int((self.Nn - 1) * self.Nn / 2), self.Nn), dtype=float)
        ia = 0
        for i1 in range(self.Nn - 1):
            for i2 in range(i1 + 1, self.Nn):
                xi3n1[ia, i1] = xi3n2[ia, i2] = math.sqrt(3)
                xi3n2[ia, i1] = xi3n1[ia, i2] = -math.sqrt(3)
                # --------------------------------
                xi4n1[ia, i1] = xi4n1[ia, i2] = math.sqrt(3)
                xi4n2[ia, i1] = xi4n2[ia, i2] = -math.sqrt(3)
                ia += 1
        SC = numpy.concatenate(
            (xi1n, xi2n, xi3n1, xi3n2, xi4n1, xi4n2, numpy.zeros((1, self.Nn)))
        ).T
        #
        return Wm, Wc, SC

    def nbOfPoints(self):
        assert self.Nn == self.SC.shape[0], "Size mismatch %i =/= %i" % (
            self.Nn,
            self.SC.shape[0],
        )
        assert self.Wm.size == self.SC.shape[1], "Size mismatch %i =/= %i" % (
            self.Wm.size,
            self.SC.shape[1],
        )
        assert self.Wm.size == self.Wc.size, "Size mismatch %i =/= %i" % (
            self.Wm.size,
            self.Wc.size,
        )
        return self.Wm.size

    def get(self):
        return self.Wm, self.Wc, self.SC

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        msg = ""
        msg += "    Alpha   = %s\n" % self.Alpha
        msg += "    Beta    = %s\n" % self.Beta
        msg += "    Kappa   = %s\n" % self.Kappa
        msg += "    Lambda  = %s\n" % self.Lambda
        msg += "    Gamma   = %s\n" % self.Gamma
        msg += "    Wm      = %s\n" % self.Wm
        msg += "    Wc      = %s\n" % self.Wc
        msg += "    sum(Wm) = %s\n" % numpy.sum(self.Wm)
        msg += "    SC      =\n%s\n" % self.SC
        return msg


# ==============================================================================
def GetNeighborhoodTopology(__ntype, __ipop):
    "Renvoi une topologie de connexion pour une population de points"
    if __ntype in [
        "FullyConnectedNeighborhood",
        "FullyConnectedNeighbourhood",
        "gbest",
    ]:
        __topology = [__ipop for __i in __ipop]
    elif __ntype in [
        "RingNeighborhoodWithRadius1",
        "RingNeighbourhoodWithRadius1",
        "lbest",
    ]:
        __cpop = list(__ipop[-1:]) + list(__ipop) + list(__ipop[:1])
        __topology = [__cpop[__n : __n + 3] for __n in range(len(__ipop))]  # noqa: E203
    elif __ntype in ["RingNeighborhoodWithRadius2", "RingNeighbourhoodWithRadius2"]:
        __cpop = list(__ipop[-2:]) + list(__ipop) + list(__ipop[:2])
        __topology = [__cpop[__n : __n + 5] for __n in range(len(__ipop))]  # noqa: E203
    elif __ntype in [
        "AdaptativeRandomWith3Neighbors",
        "AdaptativeRandomWith3Neighbours",
        "abest",
    ]:
        __cpop = 3 * list(__ipop)
        __topology = [[__i] + list(numpy.random.choice(__cpop, 3)) for __i in __ipop]
    elif __ntype in [
        "AdaptativeRandomWith5Neighbors",
        "AdaptativeRandomWith5Neighbours",
    ]:
        __cpop = 5 * list(__ipop)
        __topology = [[__i] + list(numpy.random.choice(__cpop, 5)) for __i in __ipop]
    else:
        raise ValueError(
            'Swarm topology type unavailable because name "%s" is unknown.' % __ntype
        )
    return __topology


# ==============================================================================
def FindIndexesFromNames(
    __NameOfLocations=None, __ExcludeLocations=None, ForceArray=False
):
    "Exprime les indices des noms exclus, en ignorant les absents"
    if __ExcludeLocations is None:
        __ExcludeIndexes = ()
    elif (
        isinstance(__ExcludeLocations, (list, numpy.ndarray, tuple))
        and len(__ExcludeLocations) == 0
    ):
        __ExcludeIndexes = ()
    # ----------
    elif __NameOfLocations is None:
        try:
            __ExcludeIndexes = numpy.asarray(__ExcludeLocations, dtype=int)
        except ValueError as e:
            if "invalid literal for int() with base 10:" in str(e):
                raise ValueError(
                    "to exclude named locations, initial location name list can"
                    + " not be void and has to have the same length as one state"
                )
            else:
                raise ValueError(str(e))
    elif (
        isinstance(__NameOfLocations, (list, numpy.ndarray, tuple))
        and len(__NameOfLocations) == 0
    ):
        try:
            __ExcludeIndexes = numpy.asarray(__ExcludeLocations, dtype=int)
        except ValueError as e:
            if "invalid literal for int() with base 10:" in str(e):
                raise ValueError(
                    "to exclude named locations, initial location name list can"
                    + " not be void and has to have the same length as one state"
                )
            else:
                raise ValueError(str(e))
    # ----------
    else:
        try:
            __ExcludeIndexes = numpy.asarray(__ExcludeLocations, dtype=int)
        except ValueError as e:
            if "invalid literal for int() with base 10:" in str(e):
                if (
                    len(__NameOfLocations) < 1.0e6 + 1
                    and len(__ExcludeLocations) > 1500
                ):
                    __Heuristic = True
                else:
                    __Heuristic = False
                if ForceArray or __Heuristic:
                    # Recherche par array permettant des noms invalides, peu efficace
                    __NameToIndex = dict(
                        numpy.array(
                            (__NameOfLocations, range(len(__NameOfLocations)))
                        ).T
                    )
                    __ExcludeIndexes = numpy.asarray(
                        [__NameToIndex.get(k, -1) for k in __ExcludeLocations],
                        dtype=int,
                    )
                    #
                else:
                    # Recherche par liste permettant des noms invalides, très efficace
                    def __NameToIndex_get(cle, default=-1):
                        if cle in __NameOfLocations:
                            return __NameOfLocations.index(cle)
                        else:
                            return default

                    __ExcludeIndexes = numpy.asarray(
                        [__NameToIndex_get(k, -1) for k in __ExcludeLocations],
                        dtype=int,
                    )
                    #
                    # Exemple de recherche par liste encore un peu plus efficace,
                    # mais interdisant des noms invalides :
                    # __ExcludeIndexes = numpy.asarray(
                    #     [__NameOfLocations.index(k) for k in __ExcludeLocations],
                    #     dtype=int,
                    # )
                    #
                # Ignore les noms absents
                __ExcludeIndexes = numpy.compress(
                    __ExcludeIndexes > -1, __ExcludeIndexes
                )
                if len(__ExcludeIndexes) == 0:
                    __ExcludeIndexes = ()
            else:
                raise ValueError(str(e))
    # ----------
    return __ExcludeIndexes


# ==============================================================================
def BuildComplexSampleList(
    __SampleAsnUplet,
    __SampleAsExplicitHyperCube,
    __SampleAsMinMaxStepHyperCube,
    __SampleAsMinMaxLatinHyperCube,
    __SampleAsMinMaxSobolSequence,
    __SampleAsIndependantRandomVariables,
    __X0,
    __Seed=None,
):
    # ---------------------------
    if len(__SampleAsnUplet) > 0:
        sampleList = __SampleAsnUplet
        for i, Xx in enumerate(sampleList):
            if numpy.ravel(Xx).size != __X0.size:
                raise ValueError(
                    "The size %i of the %ith state X in the sample and %i of the"
                    % (numpy.ravel(Xx).size, i + 1, __X0.size)
                    + " checking point Xb are different, they have to be identical."
                )
    # ---------------------------
    elif len(__SampleAsExplicitHyperCube) > 0:
        sampleList = itertools.product(*list(__SampleAsExplicitHyperCube))
    # ---------------------------
    elif len(__SampleAsMinMaxStepHyperCube) > 0:
        coordinatesList = []
        for i, dim in enumerate(__SampleAsMinMaxStepHyperCube):
            if len(dim) != 3:
                raise ValueError(
                    'For dimension %i, the variable definition "%s" is incorrect,'
                    % (i, dim)
                    + " it should be [min,max,step]."
                )
            else:
                coordinatesList.append(
                    numpy.linspace(
                        dim[0],
                        dim[1],
                        1 + int((float(dim[1]) - float(dim[0])) / float(dim[2])),
                    )
                )
        sampleList = itertools.product(*coordinatesList)
    # ---------------------------
    elif len(__SampleAsMinMaxLatinHyperCube) > 0:
        if vt(scipy.version.version) <= vt("1.7.0"):
            __msg = (
                "In order to use Latin Hypercube sampling, you must at least use"
                + " Scipy version 1.7.0 (and you are presently using"
                + " Scipy %s). A void sample is then generated." % scipy.version.version
            )
            warnings.warn(__msg, FutureWarning, stacklevel=50)
            sampleList = []
        else:
            __spDesc = list(__SampleAsMinMaxLatinHyperCube)
            __nbDime, __nbSamp = map(int, __spDesc.pop())  # Réduction du dernier
            __sample = scipy.stats.qmc.LatinHypercube(
                d=len(__spDesc),
                seed=numpy.random.default_rng(__Seed),
            )
            __sample = __sample.random(n=__nbSamp)
            __bounds = numpy.array(__spDesc)[:, 0:2]
            __l_bounds = __bounds[:, 0]
            __u_bounds = __bounds[:, 1]
            sampleList = scipy.stats.qmc.scale(__sample, __l_bounds, __u_bounds)
    # ---------------------------
    elif len(__SampleAsMinMaxSobolSequence) > 0:
        if vt(scipy.version.version) <= vt("1.7.0"):
            __msg = (
                "In order to use Latin Hypercube sampling, you must at least use"
                + " Scipy version 1.7.0 (and you are presently using"
                + " Scipy %s). A void sample is then generated." % scipy.version.version
            )
            warnings.warn(__msg, FutureWarning, stacklevel=50)
            sampleList = []
        else:
            __spDesc = list(__SampleAsMinMaxSobolSequence)
            __nbDime, __nbSamp = map(int, __spDesc.pop())  # Réduction du dernier
            if __nbDime != len(__spDesc):
                __msg = (
                    "Declared space dimension"
                    + " (%i) is not equal to number of bounds (%i),"
                    % (__nbDime, len(__spDesc))
                    + " the last one will be used."
                )
                warnings.warn(
                    __msg,
                    FutureWarning,
                    stacklevel=50,
                )
            __sample = scipy.stats.qmc.Sobol(
                d=len(__spDesc),
                seed=numpy.random.default_rng(__Seed),
            )
            __sample = __sample.random_base2(m=int(math.log2(__nbSamp)) + 1)
            __bounds = numpy.array(__spDesc)[:, 0:2]
            __l_bounds = __bounds[:, 0]
            __u_bounds = __bounds[:, 1]
            sampleList = scipy.stats.qmc.scale(__sample, __l_bounds, __u_bounds)
    # ---------------------------
    elif len(__SampleAsIndependantRandomVariables) > 0:
        coordinatesList = []
        for i, dim in enumerate(__SampleAsIndependantRandomVariables):
            if len(dim) != 3:
                raise ValueError(
                    'For dimension %i, the variable definition "%s" is incorrect,'
                    % (i, dim)
                    + " it should be ('distribution',(parameters),length) with"
                    + " distribution in ['normal'(mean,std), 'lognormal'(mean,sigma),"
                    + " 'uniform'(low,high), 'weibull'(shape)]."
                )
            elif not (
                str(dim[0]) in ["normal", "lognormal", "uniform", "weibull"]
                and hasattr(numpy.random, str(dim[0]))
            ):
                raise ValueError(
                    'For dimension %i, the distribution name "%s" is not allowed,'
                    % (i, str(dim[0]))
                    + " please choose in ['normal'(mean,std), 'lognormal'(mean,sigma),"
                    + " 'uniform'(low,high), 'weibull'(shape)]"
                )
            else:
                distribution = getattr(numpy.random, str(dim[0]), "normal")
                coordinatesList.append(distribution(*dim[1], size=max(1, int(dim[2]))))
        sampleList = itertools.product(*coordinatesList)
    else:
        sampleList = iter(
            [
                __X0,
            ]
        )
    # ----------
    return sampleList


# ==============================================================================
def multiXOsteps(selfA, Xb, Y, U, HO, EM, CM, R, B, Q, oneCycle, __CovForecast=False):
    """
    Prévision multi-pas avec une correction par pas (multi-méthodes)
    """
    #
    # Initialisation
    # --------------
    if selfA._parameters["EstimationOf"] == "State":
        if (
            len(selfA.StoredVariables["Analysis"]) == 0
            or not selfA._parameters["nextStep"]
        ):
            Xn = numpy.asarray(Xb)
            if __CovForecast:
                Pn = B
            selfA.StoredVariables["Analysis"].store(Xn)
            if selfA._toStore("APosterioriCovariance"):
                if hasattr(B, "asfullmatrix"):
                    selfA.StoredVariables["APosterioriCovariance"].store(
                        B.asfullmatrix(Xn.size)
                    )
                else:
                    selfA.StoredVariables["APosterioriCovariance"].store(B)
            selfA._setInternalState("seed", numpy.random.get_state())
        elif selfA._parameters["nextStep"]:
            Xn = selfA._getInternalState("Xn")
            if __CovForecast:
                Pn = selfA._getInternalState("Pn")
    else:
        Xn = numpy.asarray(Xb)
        if __CovForecast:
            Pn = B
    #
    if hasattr(Y, "stepnumber"):
        duration = Y.stepnumber()
    else:
        duration = 2
    #
    # Multi-steps
    # -----------
    for step in range(duration - 1):
        selfA.StoredVariables["CurrentStepNumber"].store(
            len(selfA.StoredVariables["Analysis"])
        )
        #
        if hasattr(Y, "store"):
            Ynpu = numpy.asarray(Y[step + 1]).reshape((-1, 1))
        else:
            Ynpu = numpy.asarray(Y).reshape((-1, 1))
        #
        if U is not None:
            if hasattr(U, "store") and len(U) > 1:
                Un = numpy.asarray(U[step]).reshape((-1, 1))
            elif hasattr(U, "store") and len(U) == 1:
                Un = numpy.asarray(U[0]).reshape((-1, 1))
            else:
                Un = numpy.asarray(U).reshape((-1, 1))
        else:
            Un = None
        #
        # Predict (Time Update)
        # ---------------------
        if selfA._parameters["EstimationOf"] == "State":
            if __CovForecast:
                Mt = EM["Tangent"].asMatrix(Xn)
                Mt = Mt.reshape(Xn.size, Xn.size)  # ADAO & check shape
                Ma = EM["Adjoint"].asMatrix(Xn)
                Ma = Ma.reshape(Xn.size, Xn.size)  # ADAO & check shape
                Pn_predicted = Q + Mt @ (Pn @ Ma)
            Mm = EM["Direct"].appliedControledFormTo
            Xn_predicted = Mm((Xn, Un)).reshape((-1, 1))
            if (
                CM is not None and "Tangent" in CM and Un is not None
            ):  # Attention : si Cm est aussi dans M, doublon !
                Cm = CM["Tangent"].asMatrix(Xn_predicted)
                Cm = Cm.reshape(Xn.size, Un.size)  # ADAO & check shape
                Xn_predicted = Xn_predicted + (Cm @ Un).reshape((-1, 1))
        elif selfA._parameters["EstimationOf"] == "Parameters":  # No forecast
            # --- > Par principe, M = Id, Q = 0
            Xn_predicted = Xn
            if __CovForecast:
                Pn_predicted = Pn
        Xn_predicted = numpy.asarray(Xn_predicted).reshape((-1, 1))
        if selfA._toStore("ForecastState"):
            selfA.StoredVariables["ForecastState"].store(Xn_predicted)
        if __CovForecast:
            if hasattr(Pn_predicted, "asfullmatrix"):
                Pn_predicted = Pn_predicted.asfullmatrix(Xn.size)
            else:
                Pn_predicted = numpy.asarray(Pn_predicted).reshape((Xn.size, Xn.size))
            if selfA._toStore("ForecastCovariance"):
                selfA.StoredVariables["ForecastCovariance"].store(Pn_predicted)
        #
        # Correct (Measurement Update)
        # ----------------------------
        if __CovForecast:
            oneCycle(selfA, Xn_predicted, Ynpu, Un, HO, CM, R, Pn_predicted, True)
        else:
            oneCycle(selfA, Xn_predicted, Ynpu, Un, HO, CM, R, B, True)
        #
        # --------------------------
        Xn = selfA._getInternalState("Xn")
        if __CovForecast:
            Pn = selfA._getInternalState("Pn")
    #
    return 0


# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
