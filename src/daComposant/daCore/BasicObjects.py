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

"""
    Définit les outils généraux élémentaires.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os
import sys
import logging
import copy
import time
import numpy
import warnings
from functools import partial
from daCore import Persistence
from daCore import PlatformInfo
from daCore import Interfaces
from daCore import Templates


# ==============================================================================
class CacheManager(object):
    """
    Classe générale de gestion d'un cache de calculs
    """

    __slots__ = (
        "__tolerBP",
        "__lengthOR",
        "__initlnOR",
        "__seenNames",
        "__enabled",
        "__listOPCV",
    )

    def __init__(self, toleranceInRedundancy=1.0e-18, lengthOfRedundancy=-1):
        """
        Les caractéristiques de tolérance peuvent être modifiées à la création.
        """
        self.__tolerBP = float(toleranceInRedundancy)
        self.__lengthOR = int(lengthOfRedundancy)
        self.__initlnOR = self.__lengthOR
        self.__seenNames = []
        self.__enabled = True
        self.clearCache()

    def clearCache(self):
        "Vide le cache"
        self.__listOPCV = []
        self.__seenNames = []

    def wasCalculatedIn(self, xValue, oName=""):
        "Vérifie l'existence d'un calcul correspondant à la valeur"
        __alc = False
        __HxV = None
        if self.__enabled:
            for i in range(min(len(self.__listOPCV), self.__lengthOR) - 1, -1, -1):
                if not hasattr(xValue, "size"):
                    pass
                elif str(oName) != self.__listOPCV[i][3]:
                    pass
                elif xValue.size != self.__listOPCV[i][0].size:
                    pass
                elif (numpy.ravel(xValue)[0] - self.__listOPCV[i][0][0]) > (
                    self.__tolerBP * self.__listOPCV[i][2] / self.__listOPCV[i][0].size
                ):
                    pass
                elif numpy.linalg.norm(numpy.ravel(xValue) - self.__listOPCV[i][0]) < (
                    self.__tolerBP * self.__listOPCV[i][2]
                ):
                    __alc = True
                    __HxV = self.__listOPCV[i][1]
                    break
        return __alc, __HxV

    def storeValueInX(self, xValue, HxValue, oName=""):
        "Stocke pour un opérateur o un calcul Hx correspondant à la valeur x"
        if self.__lengthOR < 0:
            self.__lengthOR = 2 * min(numpy.size(xValue), 50) + 2
            self.__initlnOR = self.__lengthOR
            self.__seenNames.append(str(oName))
        if str(oName) not in self.__seenNames:  # Étend la liste si nouveau
            self.__lengthOR += 2 * min(numpy.size(xValue), 50) + 2
            self.__initlnOR += self.__lengthOR
            self.__seenNames.append(str(oName))
        while len(self.__listOPCV) > self.__lengthOR:
            self.__listOPCV.pop(0)
        self.__listOPCV.append(
            (
                copy.copy(numpy.ravel(xValue)),  # 0 Previous point
                copy.copy(HxValue),  # 1 Previous value
                numpy.linalg.norm(xValue),  # 2 Norm
                str(oName),  # 3 Operator name
            )
        )

    def disable(self):
        "Inactive le cache"
        self.__initlnOR = self.__lengthOR
        self.__lengthOR = 0
        self.__enabled = False

    def enable(self):
        "Active le cache"
        self.__lengthOR = self.__initlnOR
        self.__enabled = True


# ==============================================================================
class Operator(object):
    """
    Classe générale d'interface de type opérateur simple
    """

    __slots__ = (
        "__name",
        "__NbCallsAsMatrix",
        "__NbCallsAsMethod",
        "__NbCallsOfCached",
        "__reduceM",
        "__avoidRC",
        "__inputAsMF",
        "__mpEnabled",
        "__extraArgs",
        "__Method",
        "__Matrix",
        "__Type",
    )
    #
    NbCallsAsMatrix = 0
    NbCallsAsMethod = 0
    NbCallsOfCached = 0
    CM = CacheManager()

    def __init__(
        self,
        name="GenericOperator",
        fromMethod=None,
        fromMatrix=None,
        avoidingRedundancy=True,
        reducingMemoryUse=False,
        inputAsMultiFunction=False,
        enableMultiProcess=False,
        extraArguments=None,
    ):
        """
        On construit un objet de ce type en fournissant, à l'aide de l'un des
        deux mots-clé, soit une fonction ou un multi-fonction python, soit une
        matrice.
        Arguments :
        - name : nom d'opérateur
        - fromMethod : argument de type fonction Python
        - fromMatrix : argument adapté au constructeur numpy.array/matrix
        - avoidingRedundancy : booléen évitant (ou pas) les calculs redondants
        - reducingMemoryUse : booléen forçant (ou pas) des calculs pour qu'ils
          soient moins gourmands en mémoire
        - inputAsMultiFunction : booléen indiquant une fonction explicitement
          définie (ou pas) en multi-fonction
        - extraArguments : arguments supplémentaires passés à la fonction de
          base et ses dérivées (tuple ou dictionnaire)
        """
        self.__name = str(name)
        self.__NbCallsAsMatrix, self.__NbCallsAsMethod, self.__NbCallsOfCached = 0, 0, 0
        self.__reduceM = bool(reducingMemoryUse)
        self.__avoidRC = bool(avoidingRedundancy)
        self.__inputAsMF = bool(inputAsMultiFunction)
        self.__mpEnabled = bool(enableMultiProcess)
        self.__extraArgs = extraArguments
        if fromMethod is not None and self.__inputAsMF:
            self.__Method = fromMethod  # logtimer(fromMethod)
            self.__Matrix = None
            self.__Type = "Method"
        elif fromMethod is not None and not self.__inputAsMF:
            self.__Method = partial(
                MultiFonction, _sFunction=fromMethod, _mpEnabled=self.__mpEnabled
            )
            self.__Matrix = None
            self.__Type = "Method"
        elif fromMatrix is not None:
            self.__Method = None
            if isinstance(fromMatrix, str):
                fromMatrix = PlatformInfo.strmatrix2liststr(fromMatrix)
            self.__Matrix = numpy.asarray(fromMatrix, dtype=float)
            self.__Type = "Matrix"
        else:
            self.__Method = None
            self.__Matrix = None
            self.__Type = None

    def disableAvoidingRedundancy(self):
        "Inactive le cache"
        Operator.CM.disable()

    def enableAvoidingRedundancy(self):
        "Active le cache"
        if self.__avoidRC:
            Operator.CM.enable()
        else:
            Operator.CM.disable()

    def isType(self):
        "Renvoie le type"
        return self.__Type

    def appliedTo(
        self, xValue, HValue=None, argsAsSerie=False, returnSerieAsArrayMatrix=False
    ):
        """
        Permet de restituer le résultat de l'application de l'opérateur à une
        série d'arguments xValue. Cette méthode se contente d'appliquer, chaque
        argument devant a priori être du bon type.
        Arguments :
        - les arguments par série sont :
            - xValue : argument adapté pour appliquer l'opérateur
            - HValue : valeur précalculée de l'opérateur en ce point
        - argsAsSerie : indique si les arguments sont une mono ou multi-valeur
        """
        if argsAsSerie:
            _xValue = xValue
            _HValue = HValue
        else:
            _xValue = (xValue,)
            if HValue is not None:
                _HValue = (HValue,)
            else:
                _HValue = HValue
        PlatformInfo.isIterable(_xValue, True, " in Operator.appliedTo")
        #
        if _HValue is not None:
            assert len(_xValue) == len(
                _HValue
            ), "Incompatible number of elements in xValue and HValue"
            _HxValue = []
            for i in range(len(_HValue)):
                _HxValue.append(_HValue[i])
                if self.__avoidRC:
                    Operator.CM.storeValueInX(_xValue[i], _HxValue[-1], self.__name)
        else:
            _HxValue = []
            _xserie = []
            _hindex = []
            for i, xv in enumerate(_xValue):
                if self.__avoidRC:
                    __alreadyCalculated, __HxV = Operator.CM.wasCalculatedIn(
                        xv, self.__name
                    )
                else:
                    __alreadyCalculated = False
                #
                if __alreadyCalculated:
                    self.__addOneCacheCall()
                    _hv = __HxV
                else:
                    if self.__Matrix is not None:
                        self.__addOneMatrixCall()
                        _hv = self.__Matrix @ numpy.ravel(xv)
                    else:
                        self.__addOneMethodCall()
                        _xserie.append(xv)
                        _hindex.append(i)
                        _hv = None
                _HxValue.append(_hv)
            #
            if len(_xserie) > 0 and self.__Matrix is None:
                if self.__extraArgs is None:
                    _hserie = self.__Method(_xserie)  # Calcul MF
                else:
                    _hserie = self.__Method(_xserie, self.__extraArgs)  # Calcul MF
                if not hasattr(_hserie, "pop"):
                    raise TypeError(
                        "The user input multi-function doesn't seem to return a"
                        + " result sequence, behaving like a mono-function. It has"
                        + " to be checked."
                    )
                for i in _hindex:
                    _xv = _xserie.pop(0)
                    _hv = _hserie.pop(0)
                    _HxValue[i] = _hv
                    if self.__avoidRC:
                        Operator.CM.storeValueInX(_xv, _hv, self.__name)
        #
        if returnSerieAsArrayMatrix:
            _HxValue = numpy.stack([numpy.ravel(_hv) for _hv in _HxValue], axis=1)
        #
        if argsAsSerie:
            return _HxValue
        else:
            return _HxValue[-1]

    def appliedControledFormTo(
        self, paires, argsAsSerie=False, returnSerieAsArrayMatrix=False
    ):
        """
        Permet de restituer le résultat de l'application de l'opérateur à des
        paires (xValue, uValue). Cette méthode se contente d'appliquer, son
        argument devant a priori être du bon type. Si la uValue est None,
        on suppose que l'opérateur ne s'applique qu'à xValue.
        Arguments :
        - paires : les arguments par paire sont :
            - xValue : argument X adapté pour appliquer l'opérateur
            - uValue : argument U adapté pour appliquer l'opérateur
        - argsAsSerie : indique si l'argument est une mono ou multi-valeur
        """
        if argsAsSerie:
            _xuValue = paires
        else:
            _xuValue = (paires,)
        PlatformInfo.isIterable(_xuValue, True, " in Operator.appliedControledFormTo")
        #
        if self.__Matrix is not None:
            _HxValue = []
            for paire in _xuValue:
                _xValue, _uValue = paire
                self.__addOneMatrixCall()
                _HxValue.append(self.__Matrix @ numpy.ravel(_xValue))
        else:
            _xuArgs = []
            for paire in _xuValue:
                _xValue, _uValue = paire
                if _uValue is not None:
                    _xuArgs.append(paire)
                else:
                    _xuArgs.append(_xValue)
            self.__addOneMethodCall(len(_xuArgs))
            if self.__extraArgs is None:
                _HxValue = self.__Method(_xuArgs)  # Calcul MF
            else:
                _HxValue = self.__Method(_xuArgs, self.__extraArgs)  # Calcul MF
        #
        if returnSerieAsArrayMatrix:
            _HxValue = numpy.stack([numpy.ravel(_hv) for _hv in _HxValue], axis=1)
        #
        if argsAsSerie:
            return _HxValue
        else:
            return _HxValue[-1]

    def appliedInXTo(self, paires, argsAsSerie=False, returnSerieAsArrayMatrix=False):
        """
        Permet de restituer le résultat de l'application de l'opérateur à une
        série d'arguments xValue, sachant que l'opérateur est valable en
        xNominal. Cette méthode se contente d'appliquer, son argument devant a
        priori être du bon type. Si l'opérateur est linéaire car c'est une
        matrice, alors il est valable en tout point nominal et xNominal peut
        être quelconque. Il n'y a qu'une seule paire par défaut, et argsAsSerie
        permet d'indiquer que l'argument est multi-paires.
        Arguments :
        - paires : les arguments par paire sont :
            - xNominal : série d'arguments permettant de donner le point où
              l'opérateur est construit pour être ensuite appliqué
            - xValue : série d'arguments adaptés pour appliquer l'opérateur
        - argsAsSerie : indique si l'argument est une mono ou multi-valeur
        """
        if argsAsSerie:
            _nxValue = paires
        else:
            _nxValue = (paires,)
        PlatformInfo.isIterable(_nxValue, True, " in Operator.appliedInXTo")
        #
        if self.__Matrix is not None:
            _HxValue = []
            for paire in _nxValue:
                _xNominal, _xValue = paire
                self.__addOneMatrixCall()
                _HxValue.append(self.__Matrix @ numpy.ravel(_xValue))
        else:
            self.__addOneMethodCall(len(_nxValue))
            if self.__extraArgs is None:
                _HxValue = self.__Method(_nxValue)  # Calcul MF
            else:
                _HxValue = self.__Method(_nxValue, self.__extraArgs)  # Calcul MF
        #
        if returnSerieAsArrayMatrix:
            _HxValue = numpy.stack([numpy.ravel(_hv) for _hv in _HxValue], axis=1)
        #
        if argsAsSerie:
            return _HxValue
        else:
            return _HxValue[-1]

    def asMatrix(self, ValueForMethodForm="UnknownVoidValue", argsAsSerie=False):
        """
        Permet de renvoyer l'opérateur sous la forme d'une matrice
        """
        if self.__Matrix is not None:
            self.__addOneMatrixCall()
            mValue = [
                self.__Matrix,
            ]
        elif (
            not isinstance(ValueForMethodForm, str)
            or ValueForMethodForm != "UnknownVoidValue"
        ):  # Ne pas utiliser "None"
            mValue = []
            if argsAsSerie:
                self.__addOneMethodCall(len(ValueForMethodForm))
                for _vfmf in ValueForMethodForm:
                    mValue.append(self.__Method(((_vfmf, None),)))
            else:
                self.__addOneMethodCall()
                mValue = self.__Method(((ValueForMethodForm, None),))
        else:
            raise ValueError(
                "Matrix form of the operator defined as a function/method requires to give an operating point."
            )
        #
        if argsAsSerie:
            return mValue
        else:
            return mValue[-1]

    def shape(self):
        """
        Renvoie la taille sous forme numpy si l'opérateur est disponible sous
        la forme d'une matrice
        """
        if self.__Matrix is not None:
            return self.__Matrix.shape
        else:
            raise ValueError(
                "Matrix form of the operator is not available, nor the shape"
            )

    def nbcalls(self, which=None):
        """
        Renvoie les nombres d'évaluations de l'opérateur
        """
        __nbcalls = (
            self.__NbCallsAsMatrix + self.__NbCallsAsMethod,
            self.__NbCallsAsMatrix,
            self.__NbCallsAsMethod,
            self.__NbCallsOfCached,
            Operator.NbCallsAsMatrix + Operator.NbCallsAsMethod,
            Operator.NbCallsAsMatrix,
            Operator.NbCallsAsMethod,
            Operator.NbCallsOfCached,
        )
        if which is None:
            return __nbcalls
        else:
            return __nbcalls[which]

    def __addOneMatrixCall(self):
        "Comptabilise un appel"
        self.__NbCallsAsMatrix += 1  # Decompte local
        Operator.NbCallsAsMatrix += 1  # Decompte global

    def __addOneMethodCall(self, nb=1):
        "Comptabilise un appel"
        self.__NbCallsAsMethod += nb  # Decompte local
        Operator.NbCallsAsMethod += nb  # Decompte global

    def __addOneCacheCall(self):
        "Comptabilise un appel"
        self.__NbCallsOfCached += 1  # Décompte local
        Operator.NbCallsOfCached += 1  # Décompte global


# ==============================================================================
class FullOperator(object):
    """
    Classe générale d'interface de type opérateur complet
    (Direct, Linéaire Tangent, Adjoint)
    """

    __slots__ = (
        "__name",
        "__check",
        "__extraArgs",
        "__FO",
        "__T",
    )

    def __init__(
        self,
        name="GenericFullOperator",
        asMatrix=None,
        asOneFunction=None,  # 1 Fonction
        asThreeFunctions=None,  # 3 Fonctions in a dictionary
        asScript=None,  # 1 or 3 Fonction(s) by script
        asDict=None,  # Parameters
        appliedInX=None,
        extraArguments=None,
        performancePrf=None,
        inputAsMF=False,  # Fonction(s) as Multi-Functions
        scheduledBy=None,
        toBeChecked=False,
    ):
        """"""
        self.__name = str(name)
        self.__check = bool(toBeChecked)
        self.__extraArgs = extraArguments
        #
        self.__FO = {}
        #
        __Parameters = {}
        if (asDict is not None) and isinstance(asDict, dict):
            __Parameters.update(asDict)  # Copie mémoire
        # Deprecated parameters
        __Parameters = self.__deprecateOpt(
            collection=__Parameters,
            oldn="EnableMultiProcessing",
            newn="EnableWiseParallelism",
        )
        __Parameters = self.__deprecateOpt(
            collection=__Parameters,
            oldn="EnableMultiProcessingInEvaluation",
            newn="EnableParallelEvaluations",
        )
        __Parameters = self.__deprecateOpt(
            collection=__Parameters,
            oldn="EnableMultiProcessingInDerivatives",
            newn="EnableParallelDerivatives",
        )
        # Priorité à EnableParallelDerivatives=True
        if (
            "EnableWiseParallelism" in __Parameters
            and __Parameters["EnableWiseParallelism"]
        ):
            __Parameters["EnableParallelDerivatives"] = True
            __Parameters["EnableParallelEvaluations"] = False
        if "EnableParallelDerivatives" not in __Parameters:
            __Parameters["EnableParallelDerivatives"] = False
        if __Parameters["EnableParallelDerivatives"]:
            __Parameters["EnableParallelEvaluations"] = False
        if "EnableParallelEvaluations" not in __Parameters:
            __Parameters["EnableParallelEvaluations"] = False
        if "withIncrement" in __Parameters:  # Temporaire
            __Parameters["DifferentialIncrement"] = __Parameters["withIncrement"]
        #
        __reduceM, __avoidRC = True, True  # Défaut
        if performancePrf is not None:
            if performancePrf == "ReducedAmountOfCalculation":
                __reduceM, __avoidRC = False, True
            elif performancePrf == "ReducedMemoryFootprint":
                __reduceM, __avoidRC = True, False
            elif performancePrf == "NoSavings":
                __reduceM, __avoidRC = False, False
            # "ReducedOverallRequirements" et tous les autres choix (y.c rien)
            #  sont équivalents au défaut
        #
        if asScript is not None:
            __Matrix, __Function = None, None
            if asMatrix:
                __Matrix = Interfaces.ImportFromScript(asScript).getvalue(self.__name)
            elif asOneFunction:
                __Function = {
                    "Direct": Interfaces.ImportFromScript(asScript).getvalue(
                        "DirectOperator"
                    )
                }
                __Function.update({"useApproximatedDerivatives": True})
                __Function.update(__Parameters)
            elif asThreeFunctions:
                __Function = {
                    "Direct": Interfaces.ImportFromScript(asScript).getvalue(
                        "DirectOperator"
                    ),
                    "Tangent": Interfaces.ImportFromScript(asScript).getvalue(
                        "TangentOperator"
                    ),
                    "Adjoint": Interfaces.ImportFromScript(asScript).getvalue(
                        "AdjointOperator"
                    ),
                }
                __Function.update(__Parameters)
        else:
            __Matrix = asMatrix
            if asOneFunction is not None:
                if isinstance(asOneFunction, dict) and "Direct" in asOneFunction:
                    if asOneFunction["Direct"] is not None:
                        __Function = asOneFunction
                    else:
                        raise ValueError(
                            'The function has to be given in a dictionnary which have 1 key ("Direct")'
                        )
                else:
                    __Function = {"Direct": asOneFunction}
                __Function.update({"useApproximatedDerivatives": True})
                __Function.update(__Parameters)
            elif asThreeFunctions is not None:
                if (
                    isinstance(asThreeFunctions, dict)
                    and ("Tangent" in asThreeFunctions)
                    and (asThreeFunctions["Tangent"] is not None)
                    and ("Adjoint" in asThreeFunctions)
                    and (asThreeFunctions["Adjoint"] is not None)
                    and (
                        ("useApproximatedDerivatives" not in asThreeFunctions)
                        or not bool(asThreeFunctions["useApproximatedDerivatives"])
                    )
                ):
                    __Function = asThreeFunctions
                elif (
                    isinstance(asThreeFunctions, dict)
                    and ("Direct" in asThreeFunctions)
                    and (asThreeFunctions["Direct"] is not None)
                ):
                    __Function = asThreeFunctions
                    __Function.update({"useApproximatedDerivatives": True})
                else:
                    raise ValueError(
                        "The functions has to be given in a dictionnary which have either"
                        + ' 1 key ("Direct") or'
                        + ' 3 keys ("Direct" (optionnal), "Tangent" and "Adjoint")'
                    )
                if "Direct" not in asThreeFunctions:
                    __Function["Direct"] = asThreeFunctions["Tangent"]
                __Function.update(__Parameters)
            else:
                __Function = None
        #
        if appliedInX is not None and isinstance(appliedInX, dict):
            __appliedInX = appliedInX
        elif appliedInX is not None:
            __appliedInX = {"HXb": appliedInX}
        else:
            __appliedInX = None
        #
        if scheduledBy is not None:
            self.__T = scheduledBy
        #
        if (
            isinstance(__Function, dict)
            and ("useApproximatedDerivatives" in __Function)
            and bool(__Function["useApproximatedDerivatives"])
            and ("Direct" in __Function)
            and (__Function["Direct"] is not None)
        ):
            if "CenteredFiniteDifference" not in __Function:
                __Function["CenteredFiniteDifference"] = False
            if "DifferentialIncrement" not in __Function:
                __Function["DifferentialIncrement"] = 0.01
            if "withdX" not in __Function:
                __Function["withdX"] = None
            if "withReducingMemoryUse" not in __Function:
                __Function["withReducingMemoryUse"] = __reduceM
            if "withAvoidingRedundancy" not in __Function:
                __Function["withAvoidingRedundancy"] = __avoidRC
            if "withToleranceInRedundancy" not in __Function:
                __Function["withToleranceInRedundancy"] = 1.0e-18
            if "withLengthOfRedundancy" not in __Function:
                __Function["withLengthOfRedundancy"] = -1
            if "NumberOfProcesses" not in __Function:
                __Function["NumberOfProcesses"] = None
            if "withmfEnabled" not in __Function:
                __Function["withmfEnabled"] = inputAsMF
            from daCore import NumericObjects

            FDA = NumericObjects.FDApproximation(
                name=self.__name,
                Function=__Function["Direct"],
                centeredDF=__Function["CenteredFiniteDifference"],
                increment=__Function["DifferentialIncrement"],
                dX=__Function["withdX"],
                extraArguments=self.__extraArgs,
                reducingMemoryUse=__Function["withReducingMemoryUse"],
                avoidingRedundancy=__Function["withAvoidingRedundancy"],
                toleranceInRedundancy=__Function["withToleranceInRedundancy"],
                lengthOfRedundancy=__Function["withLengthOfRedundancy"],
                mpEnabled=__Function["EnableParallelDerivatives"],
                mpWorkers=__Function["NumberOfProcesses"],
                mfEnabled=__Function["withmfEnabled"],
            )
            self.__FO["Direct"] = Operator(
                name=self.__name,
                fromMethod=FDA.DirectOperator,
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
                extraArguments=self.__extraArgs,
                enableMultiProcess=__Parameters["EnableParallelEvaluations"],
            )
            self.__FO["Tangent"] = Operator(
                name=self.__name + "Tangent",
                fromMethod=FDA.TangentOperator,
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
                extraArguments=self.__extraArgs,
            )
            self.__FO["Adjoint"] = Operator(
                name=self.__name + "Adjoint",
                fromMethod=FDA.AdjointOperator,
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
                extraArguments=self.__extraArgs,
            )
            self.__FO["DifferentialIncrement"] = __Function["DifferentialIncrement"]
        elif (
            isinstance(__Function, dict)
            and ("Direct" in __Function)
            and ("Tangent" in __Function)
            and ("Adjoint" in __Function)
            and (__Function["Direct"] is not None)
            and (__Function["Tangent"] is not None)
            and (__Function["Adjoint"] is not None)
        ):
            self.__FO["Direct"] = Operator(
                name=self.__name,
                fromMethod=__Function["Direct"],
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
                extraArguments=self.__extraArgs,
                enableMultiProcess=__Parameters["EnableParallelEvaluations"],
            )
            self.__FO["Tangent"] = Operator(
                name=self.__name + "Tangent",
                fromMethod=__Function["Tangent"],
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
                extraArguments=self.__extraArgs,
            )
            self.__FO["Adjoint"] = Operator(
                name=self.__name + "Adjoint",
                fromMethod=__Function["Adjoint"],
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
                extraArguments=self.__extraArgs,
            )
            self.__FO["DifferentialIncrement"] = None
        elif asMatrix is not None:
            if isinstance(__Matrix, str):
                __Matrix = PlatformInfo.strmatrix2liststr(__Matrix)
            __matrice = numpy.asarray(__Matrix, dtype=float)
            self.__FO["Direct"] = Operator(
                name=self.__name,
                fromMatrix=__matrice,
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
                enableMultiProcess=__Parameters["EnableParallelEvaluations"],
            )
            self.__FO["Tangent"] = Operator(
                name=self.__name + "Tangent",
                fromMatrix=__matrice,
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
            )
            self.__FO["Adjoint"] = Operator(
                name=self.__name + "Adjoint",
                fromMatrix=__matrice.T,
                reducingMemoryUse=__reduceM,
                avoidingRedundancy=__avoidRC,
                inputAsMultiFunction=inputAsMF,
            )
            del __matrice
            self.__FO["DifferentialIncrement"] = None
        else:
            raise ValueError(
                "The %s object is improperly defined or undefined," % self.__name
                + " it requires at minima either a matrix, a Direct operator for"
                + " approximate derivatives or a Tangent/Adjoint operators pair."
                + " Please check your operator input."
            )
        #
        if __appliedInX is not None:
            self.__FO["AppliedInX"] = {}
            for key in __appliedInX:
                if isinstance(__appliedInX[key], str):
                    __appliedInX[key] = PlatformInfo.strvect2liststr(__appliedInX[key])
                self.__FO["AppliedInX"][key] = numpy.ravel(__appliedInX[key]).reshape(
                    (-1, 1)
                )
        else:
            self.__FO["AppliedInX"] = None

    def getO(self):
        return self.__FO

    def nbcalls(self, whot=None, which=None):
        """
        Renvoie les nombres d'évaluations de l'opérateur
        """
        __nbcalls = {}
        for otype in ["Direct", "Tangent", "Adjoint"]:
            if otype in self.__FO:
                __nbcalls[otype] = self.__FO[otype].nbcalls()
        if whot in __nbcalls and which is not None:
            return __nbcalls[whot][which]
        else:
            return __nbcalls

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__FO)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__FO)

    def __deprecateOpt(self, collection: dict, oldn: str, newn: str):
        if oldn in collection:
            collection[newn] = collection[oldn]
            del collection[oldn]
            __msg = 'the parameter "%s" used in this case is' % (oldn,)
            __msg += ' deprecated and has to be replaced by "%s".' % (newn,)
            __msg += " Please update your code."
            warnings.warn(__msg, FutureWarning, stacklevel=50)
        return collection


# ==============================================================================
class Algorithm(object):
    """
    Classe générale d'interface de type algorithme

    Elle donne un cadre pour l'écriture d'une classe élémentaire d'algorithme
    d'assimilation, en fournissant un container (dictionnaire) de variables
    persistantes initialisées, et des méthodes d'accès à ces variables stockées.

    Une classe élémentaire d'algorithme doit implémenter la méthode "run".
    """

    __slots__ = (
        "_name",
        "_parameters",
        "__internal_state",
        "__required_parameters",
        "_m",
        "__variable_names_not_public",
        "__canonical_parameter_name",
        "__canonical_stored_name",
        "__replace_by_the_new_name",
        "StoredVariables",
    )

    def __init__(self, name):
        """
        L'initialisation présente permet de fabriquer des variables de stockage
        disponibles de manière générique dans les algorithmes élémentaires. Ces
        variables de stockage sont ensuite conservées dans un dictionnaire
        interne à l'objet, mais auquel on accède par la méthode "get".

        Les variables prévues sont :
            - APosterioriCorrelations : matrice de corrélations de la matrice A
            - APosterioriCovariance : matrice de covariances a posteriori : A
            - APosterioriStandardDeviations : vecteur des écart-types de la matrice A
            - APosterioriVariances : vecteur des variances de la matrice A
            - Analysis : vecteur d'analyse : Xa
            - BMA : Background moins Analysis : Xa - Xb
            - CostFunctionJ  : fonction-coût globale, somme des deux parties suivantes Jb et Jo
            - CostFunctionJAtCurrentOptimum : fonction-coût globale à l'état optimal courant lors d'itérations
            - CostFunctionJb : partie ébauche ou background de la fonction-coût : Jb
            - CostFunctionJbAtCurrentOptimum : partie ébauche à l'état optimal courant lors d'itérations
            - CostFunctionJo : partie observations de la fonction-coût : Jo
            - CostFunctionJoAtCurrentOptimum : partie observations à l'état optimal courant lors d'itérations
            - CurrentIterationNumber : numéro courant d'itération dans les algorithmes itératifs, à partir de 0
            - CurrentOptimum : état optimal courant lors d'itérations
            - CurrentState : état courant lors d'itérations
            - CurrentStepNumber : pas courant d'avancement dans les algorithmes en évolution, à partir de 0
            - EnsembleOfSimulations : ensemble d'états (sorties, simulations) rangés par colonne dans une matrice
            - EnsembleOfSnapshots : ensemble d'états rangés par colonne dans une matrice
            - EnsembleOfStates : ensemble d'états (entrées, paramètres) rangés par colonne dans une matrice
            - ForecastCovariance : covariance de l'état prédit courant lors d'itérations
            - ForecastState : état prédit courant lors d'itérations
            - GradientOfCostFunctionJ  : gradient de la fonction-coût globale
            - GradientOfCostFunctionJb : gradient de la partie ébauche de la fonction-coût
            - GradientOfCostFunctionJo : gradient de la partie observations de la fonction-coût
            - IndexOfOptimum : index de l'état optimal courant lors d'itérations
            - Innovation : l'innovation : d = Y - H(X)
            - InnovationAtCurrentAnalysis : l'innovation à l'état analysé : da = Y - H(Xa)
            - InnovationAtCurrentState : l'innovation à l'état courant : dn = Y - H(Xn)
            - InternalCostFunctionJ : ensemble de valeurs internes de fonction-coût J dans un vecteur
            - InternalCostFunctionJb : ensemble de valeurs internes de fonction-coût Jb dans un vecteur
            - InternalCostFunctionJb : ensemble de valeurs internes de fonction-coût Jo dans un vecteur
            - InternalStates : ensemble d'états internes rangés par colonne dans une matrice (=EnsembleOfSnapshots)
            - JacobianMatrixAtBackground : matrice jacobienne à l'état d'ébauche
            - JacobianMatrixAtCurrentState : matrice jacobienne à l'état courant
            - JacobianMatrixAtOptimum : matrice jacobienne à l'optimum
            - KalmanGainAtOptimum : gain de Kalman à l'optimum
            - MahalanobisConsistency : indicateur de consistance des covariances
            - OMA : Observation moins Analyse : Y - Xa
            - OMB : Observation moins Background : Y - Xb
            - ReducedCoordinates : coordonnées dans la base réduite
            - Residu : dans le cas des algorithmes de vérification
            - SampledStateForQuantiles : échantillons d'états pour l'estimation des quantiles
            - SigmaBck2 : indicateur de correction optimale des erreurs d'ébauche
            - SigmaObs2 : indicateur de correction optimale des erreurs d'observation
            - SimulatedObservationAtBackground : l'état observé H(Xb) à l'ébauche
            - SimulatedObservationAtCurrentOptimum : l'état observé H(X) à l'état optimal courant
            - SimulatedObservationAtCurrentState : l'état observé H(X) à l'état courant
            - SimulatedObservationAtOptimum : l'état observé H(Xa) à l'optimum
            - SimulationQuantiles : états observés H(X) pour les quantiles demandés
            - SingularValues : valeurs singulières provenant d'une décomposition SVD
        On peut rajouter des variables à stocker dans l'initialisation de
        l'algorithme élémentaire qui va hériter de cette classe
        """
        logging.debug("%s Initialisation", str(name))
        self._m = PlatformInfo.SystemUsage()
        #
        self._name = str(name)
        self._parameters = {"StoreSupplementaryCalculations": []}
        self.__internal_state = {}
        self.__required_parameters = {}
        self.__required_inputs = {
            "RequiredInputValues": {"mandatory": (), "optional": ()},
            "AttributesTags": [],
            "AttributesFeatures": [],
        }
        self.__variable_names_not_public = {
            "nextStep": False
        }  # Duplication dans AlgorithmAndParameters
        self.__canonical_parameter_name = {}  # Correspondance "lower"->"correct"
        self.__canonical_stored_name = {}  # Correspondance "lower"->"correct"
        self.__replace_by_the_new_name = {}  # Nouveau nom à partir d'un nom ancien
        #
        self.StoredVariables = {}
        self.StoredVariables["APosterioriCorrelations"] = Persistence.OneMatrix(
            name="APosterioriCorrelations"
        )
        self.StoredVariables["APosterioriCovariance"] = Persistence.OneMatrix(
            name="APosterioriCovariance"
        )
        self.StoredVariables["APosterioriStandardDeviations"] = Persistence.OneVector(
            name="APosterioriStandardDeviations"
        )
        self.StoredVariables["APosterioriVariances"] = Persistence.OneVector(
            name="APosterioriVariances"
        )
        self.StoredVariables["Analysis"] = Persistence.OneVector(name="Analysis")
        self.StoredVariables["BMA"] = Persistence.OneVector(name="BMA")
        self.StoredVariables["CostFunctionJ"] = Persistence.OneScalar(
            name="CostFunctionJ"
        )
        self.StoredVariables["CostFunctionJAtCurrentOptimum"] = Persistence.OneScalar(
            name="CostFunctionJAtCurrentOptimum"
        )
        self.StoredVariables["CostFunctionJb"] = Persistence.OneScalar(
            name="CostFunctionJb"
        )
        self.StoredVariables["CostFunctionJbAtCurrentOptimum"] = Persistence.OneScalar(
            name="CostFunctionJbAtCurrentOptimum"
        )
        self.StoredVariables["CostFunctionJo"] = Persistence.OneScalar(
            name="CostFunctionJo"
        )
        self.StoredVariables["CostFunctionJoAtCurrentOptimum"] = Persistence.OneScalar(
            name="CostFunctionJoAtCurrentOptimum"
        )
        self.StoredVariables["CurrentEnsembleState"] = Persistence.OneMatrix(
            name="CurrentEnsembleState"
        )
        self.StoredVariables["CurrentIterationNumber"] = Persistence.OneIndex(
            name="CurrentIterationNumber"
        )
        self.StoredVariables["CurrentOptimum"] = Persistence.OneVector(
            name="CurrentOptimum"
        )
        self.StoredVariables["CurrentState"] = Persistence.OneVector(
            name="CurrentState"
        )
        self.StoredVariables["CurrentStepNumber"] = Persistence.OneIndex(
            name="CurrentStepNumber"
        )
        self.StoredVariables["EnsembleOfSimulations"] = Persistence.OneMatrice(
            name="EnsembleOfSimulations"
        )
        self.StoredVariables["EnsembleOfSnapshots"] = Persistence.OneMatrice(
            name="EnsembleOfSnapshots"
        )
        self.StoredVariables["EnsembleOfStates"] = Persistence.OneMatrice(
            name="EnsembleOfStates"
        )
        self.StoredVariables["ExcludedPoints"] = Persistence.OneVector(
            name="ExcludedPoints"
        )
        self.StoredVariables["ForecastCovariance"] = Persistence.OneMatrix(
            name="ForecastCovariance"
        )
        self.StoredVariables["ForecastState"] = Persistence.OneVector(
            name="ForecastState"
        )
        self.StoredVariables["GradientOfCostFunctionJ"] = Persistence.OneVector(
            name="GradientOfCostFunctionJ"
        )
        self.StoredVariables["GradientOfCostFunctionJb"] = Persistence.OneVector(
            name="GradientOfCostFunctionJb"
        )
        self.StoredVariables["GradientOfCostFunctionJo"] = Persistence.OneVector(
            name="GradientOfCostFunctionJo"
        )
        self.StoredVariables["IndexOfOptimum"] = Persistence.OneIndex(
            name="IndexOfOptimum"
        )
        self.StoredVariables["Innovation"] = Persistence.OneVector(name="Innovation")
        self.StoredVariables["InnovationAtCurrentAnalysis"] = Persistence.OneVector(
            name="InnovationAtCurrentAnalysis"
        )
        self.StoredVariables["InnovationAtCurrentState"] = Persistence.OneVector(
            name="InnovationAtCurrentState"
        )
        self.StoredVariables["InternalCostFunctionJ"] = Persistence.OneVector(
            name="InternalCostFunctionJ"
        )
        self.StoredVariables["InternalCostFunctionJb"] = Persistence.OneVector(
            name="InternalCostFunctionJb"
        )
        self.StoredVariables["InternalCostFunctionJo"] = Persistence.OneVector(
            name="InternalCostFunctionJo"
        )
        self.StoredVariables["InternalStates"] = Persistence.OneMatrix(
            name="InternalStates"
        )
        self.StoredVariables["JacobianMatrixAtBackground"] = Persistence.OneMatrix(
            name="JacobianMatrixAtBackground"
        )
        self.StoredVariables["JacobianMatrixAtCurrentState"] = Persistence.OneMatrix(
            name="JacobianMatrixAtCurrentState"
        )
        self.StoredVariables["JacobianMatrixAtOptimum"] = Persistence.OneMatrix(
            name="JacobianMatrixAtOptimum"
        )
        self.StoredVariables["KalmanGainAtOptimum"] = Persistence.OneMatrix(
            name="KalmanGainAtOptimum"
        )
        self.StoredVariables["MahalanobisConsistency"] = Persistence.OneScalar(
            name="MahalanobisConsistency"
        )
        self.StoredVariables["OMA"] = Persistence.OneVector(name="OMA")
        self.StoredVariables["OMB"] = Persistence.OneVector(name="OMB")
        self.StoredVariables["OptimalPoints"] = Persistence.OneVector(
            name="OptimalPoints"
        )
        self.StoredVariables["ReducedBasis"] = Persistence.OneMatrix(
            name="ReducedBasis"
        )
        self.StoredVariables["ReducedBasisMus"] = Persistence.OneVector(
            name="ReducedBasisMus"
        )
        self.StoredVariables["ReducedCoordinates"] = Persistence.OneVector(
            name="ReducedCoordinates"
        )
        self.StoredVariables["Residu"] = Persistence.OneScalar(name="Residu")
        self.StoredVariables["Residus"] = Persistence.OneVector(name="Residus")
        self.StoredVariables["SampledStateForQuantiles"] = Persistence.OneMatrix(
            name="SampledStateForQuantiles"
        )
        self.StoredVariables["SigmaBck2"] = Persistence.OneScalar(name="SigmaBck2")
        self.StoredVariables["SigmaObs2"] = Persistence.OneScalar(name="SigmaObs2")
        self.StoredVariables["SimulatedObservationAtBackground"] = (
            Persistence.OneVector(name="SimulatedObservationAtBackground")
        )
        self.StoredVariables["SimulatedObservationAtCurrentAnalysis"] = (
            Persistence.OneVector(name="SimulatedObservationAtCurrentAnalysis")
        )
        self.StoredVariables["SimulatedObservationAtCurrentOptimum"] = (
            Persistence.OneVector(name="SimulatedObservationAtCurrentOptimum")
        )
        self.StoredVariables["SimulatedObservationAtCurrentState"] = (
            Persistence.OneVector(name="SimulatedObservationAtCurrentState")
        )
        self.StoredVariables["SimulatedObservationAtOptimum"] = Persistence.OneVector(
            name="SimulatedObservationAtOptimum"
        )
        self.StoredVariables["SimulationQuantiles"] = Persistence.OneMatrix(
            name="SimulationQuantiles"
        )
        self.StoredVariables["SingularValues"] = Persistence.OneVector(
            name="SingularValues"
        )
        #
        for k in self.StoredVariables:
            self.__canonical_stored_name[k.lower()] = k
        #
        for k, v in self.__variable_names_not_public.items():
            self.__canonical_parameter_name[k.lower()] = k
        self.__canonical_parameter_name["algorithm"] = "Algorithm"
        self.__canonical_parameter_name["storesupplementarycalculations"] = (
            "StoreSupplementaryCalculations"
        )

    def _pre_run(
        self,
        Parameters,
        Xb=None,
        Y=None,
        U=None,
        HO=None,
        EM=None,
        CM=None,
        R=None,
        B=None,
        Q=None,
    ):
        "Pré-calcul"
        logging.debug("%s Lancement", self._name)
        logging.debug(
            "%s Taille mémoire utilisée de %.0f Mio"
            % (self._name, self._m.getUsedMemory("Mio"))
        )
        self._getTimeState(reset=True)
        #
        # Mise à jour des paramètres internes avec le contenu de Parameters, en
        # reprenant les valeurs par défauts pour toutes celles non définies
        self.__setParameters(Parameters, reset=True)  # Copie mémoire
        for k, v in self.__variable_names_not_public.items():
            if k not in self._parameters:
                self.__setParameters({k: v})

        def __test_vvalue(argument, variable, argname, symbol=None):
            "Corrections et compléments des vecteurs"
            if symbol is None:
                symbol = variable
            if argument is None:
                if (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["mandatory"]
                ):
                    raise ValueError(
                        "%s %s vector %s is not set and has to be properly defined!"
                        % (self._name, argname, symbol)
                    )
                elif (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["optional"]
                ):
                    logging.debug(
                        "%s %s vector %s is not set, but is optional."
                        % (self._name, argname, symbol)
                    )
                else:
                    logging.debug(
                        "%s %s vector %s is not set, but is not required."
                        % (self._name, argname, symbol)
                    )
            else:
                if (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["mandatory"]
                ):
                    logging.debug(
                        "%s %s vector %s is required and set, and its full size is %i."
                        % (self._name, argname, symbol, numpy.array(argument).size)
                    )
                elif (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["optional"]
                ):
                    logging.debug(
                        "%s %s vector %s is optional and set, and its full size is %i."
                        % (self._name, argname, symbol, numpy.array(argument).size)
                    )
                else:
                    logging.debug(
                        "%s %s vector %s is set although neither required nor optional, and its full size is %i."
                        % (self._name, argname, symbol, numpy.array(argument).size)
                    )
            return 0

        __test_vvalue(Xb, "Xb", "Background or initial state")
        __test_vvalue(Y, "Y", "Observation")
        __test_vvalue(U, "U", "Control")

        def __test_cvalue(argument, variable, argname, symbol=None):
            "Corrections et compléments des covariances"
            if symbol is None:
                symbol = variable
            if argument is None:
                if (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["mandatory"]
                ):
                    raise ValueError(
                        "%s %s error covariance matrix %s is not set and has to be properly defined!"
                        % (self._name, argname, symbol)
                    )
                elif (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["optional"]
                ):
                    logging.debug(
                        "%s %s error covariance matrix %s is not set, but is optional."
                        % (self._name, argname, symbol)
                    )
                else:
                    logging.debug(
                        "%s %s error covariance matrix %s is not set, but is not required."
                        % (self._name, argname, symbol)
                    )
            else:
                if (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["mandatory"]
                ):
                    logging.debug(
                        "%s %s error covariance matrix %s is required and set."
                        % (self._name, argname, symbol)
                    )
                elif (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["optional"]
                ):
                    logging.debug(
                        "%s %s error covariance matrix %s is optional and set."
                        % (self._name, argname, symbol)
                    )
                else:
                    logging.debug(
                        "%s %s error covariance matrix %s is set although neither required nor optional."
                        % (self._name, argname, symbol)
                    )
            return 0

        __test_cvalue(B, "B", "Background")
        __test_cvalue(R, "R", "Observation")
        __test_cvalue(Q, "Q", "Evolution")

        def __test_ovalue(argument, variable, argname, symbol=None):
            "Corrections et compléments des opérateurs"
            if symbol is None:
                symbol = variable
            if argument is None or (isinstance(argument, dict) and len(argument) == 0):
                if (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["mandatory"]
                ):
                    raise ValueError(
                        "%s %s operator %s is not set and has to be properly defined!"
                        % (self._name, argname, symbol)
                    )
                elif (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["optional"]
                ):
                    logging.debug(
                        "%s %s operator %s is not set, but is optional."
                        % (self._name, argname, symbol)
                    )
                else:
                    logging.debug(
                        "%s %s operator %s is not set, but is not required."
                        % (self._name, argname, symbol)
                    )
            else:
                if (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["mandatory"]
                ):
                    logging.debug(
                        "%s %s operator %s is required and set."
                        % (self._name, argname, symbol)
                    )
                elif (
                    variable
                    in self.__required_inputs["RequiredInputValues"]["optional"]
                ):
                    logging.debug(
                        "%s %s operator %s is optional and set."
                        % (self._name, argname, symbol)
                    )
                else:
                    logging.debug(
                        "%s %s operator %s is set although neither required nor optional."
                        % (self._name, argname, symbol)
                    )
            return 0

        __test_ovalue(HO, "HO", "Observation", "H")
        __test_ovalue(EM, "EM", "Evolution", "M")
        __test_ovalue(CM, "CM", "Control Model", "C")
        #
        # Corrections et compléments des bornes
        if ("Bounds" in self._parameters) and isinstance(
            self._parameters["Bounds"], (list, tuple)
        ):
            if len(self._parameters["Bounds"]) > 0:
                logging.debug("%s Bounds taken into account" % (self._name,))
            else:
                self._parameters["Bounds"] = None
        elif ("Bounds" in self._parameters) and isinstance(
            self._parameters["Bounds"], (numpy.ndarray, numpy.matrix)
        ):
            self._parameters["Bounds"] = (
                numpy.ravel(self._parameters["Bounds"]).reshape((-1, 2)).tolist()
            )
            if len(self._parameters["Bounds"]) > 0:
                logging.debug("%s Bounds for states taken into account" % (self._name,))
            else:
                self._parameters["Bounds"] = None
        else:
            self._parameters["Bounds"] = None
        if self._parameters["Bounds"] is None:
            logging.debug(
                "%s There are no bounds for states to take into account" % (self._name,)
            )
        #
        if (
            ("StateBoundsForQuantiles" in self._parameters)
            and isinstance(self._parameters["StateBoundsForQuantiles"], (list, tuple))
            and (len(self._parameters["StateBoundsForQuantiles"]) > 0)
        ):
            logging.debug(
                "%s Bounds for quantiles states taken into account" % (self._name,)
            )
        elif ("StateBoundsForQuantiles" in self._parameters) and isinstance(
            self._parameters["StateBoundsForQuantiles"], (numpy.ndarray, numpy.matrix)
        ):
            self._parameters["StateBoundsForQuantiles"] = (
                numpy.ravel(self._parameters["StateBoundsForQuantiles"])
                .reshape((-1, 2))
                .tolist()
            )
            if len(self._parameters["StateBoundsForQuantiles"]) > 0:
                logging.debug(
                    "%s Bounds for quantiles states taken into account" % (self._name,)
                )
            # Attention : contrairement à Bounds, il n'y a pas de défaut à None,
            #             sinon on ne peut pas être sans bornes
        #
        # Corrections et compléments de l'initialisation en X
        if "InitializationPoint" in self._parameters:
            if Xb is not None:
                if self._parameters["InitializationPoint"] is not None and hasattr(
                    self._parameters["InitializationPoint"], "size"
                ):
                    if (
                        self._parameters["InitializationPoint"].size
                        != numpy.ravel(Xb).size
                    ):
                        raise ValueError(
                            "Incompatible size %i of forced initial point that"
                            % self._parameters["InitializationPoint"].size
                            + " have to replace the background of size %i"
                            % numpy.ravel(Xb).size
                        )
                    # Obtenu par typecast : numpy.ravel(self._parameters["InitializationPoint"])
                else:
                    self._parameters["InitializationPoint"] = numpy.ravel(Xb)
            else:
                if self._parameters["InitializationPoint"] is None:
                    raise ValueError(
                        "Forced initial point can not be set without any given Background or required value"
                    )
        #
        # Correction pour pallier a un bug de TNC sur le retour du Minimum
        if "Minimizer" in self._parameters and self._parameters["Minimizer"] == "TNC":
            self.setParameterValue("StoreInternalVariables", True)
        #
        # Verbosité et logging
        if logging.getLogger().level < logging.WARNING:
            self._parameters["optiprint"], self._parameters["optdisp"] = 1, 1
            self._parameters["optmessages"] = 15
        else:
            self._parameters["optiprint"], self._parameters["optdisp"] = -1, 0
            self._parameters["optmessages"] = 0
        #
        return 0

    def _post_run(self, _oH=None, _oM=None):
        "Post-calcul"
        if (
            "StoreSupplementaryCalculations" in self._parameters
        ) and "APosterioriCovariance" in self._parameters[
            "StoreSupplementaryCalculations"
        ]:
            for _A in self.StoredVariables["APosterioriCovariance"]:
                if (
                    "APosterioriVariances"
                    in self._parameters["StoreSupplementaryCalculations"]
                ):
                    self.StoredVariables["APosterioriVariances"].store(numpy.diag(_A))
                if (
                    "APosterioriStandardDeviations"
                    in self._parameters["StoreSupplementaryCalculations"]
                ):
                    self.StoredVariables["APosterioriStandardDeviations"].store(
                        numpy.sqrt(numpy.diag(_A))
                    )
                if (
                    "APosterioriCorrelations"
                    in self._parameters["StoreSupplementaryCalculations"]
                ):
                    _EI = numpy.diag(1.0 / numpy.sqrt(numpy.diag(_A)))
                    _C = numpy.dot(_EI, numpy.dot(_A, _EI))
                    self.StoredVariables["APosterioriCorrelations"].store(_C)
        if (
            _oH is not None
            and "Direct" in _oH
            and "Tangent" in _oH
            and "Adjoint" in _oH
        ):
            logging.debug(
                "%s Nombre d'évaluation(s) de l'opérateur d'observation direct/tangent/adjoint.: %i/%i/%i",
                self._name,
                _oH["Direct"].nbcalls(0),
                _oH["Tangent"].nbcalls(0),
                _oH["Adjoint"].nbcalls(0),
            )
            logging.debug(
                "%s Nombre d'appels au cache d'opérateur d'observation direct/tangent/adjoint..: %i/%i/%i",
                self._name,
                _oH["Direct"].nbcalls(3),
                _oH["Tangent"].nbcalls(3),
                _oH["Adjoint"].nbcalls(3),
            )
        if (
            _oM is not None
            and "Direct" in _oM
            and "Tangent" in _oM
            and "Adjoint" in _oM
        ):
            logging.debug(
                "%s Nombre d'évaluation(s) de l'opérateur d'évolution direct/tangent/adjoint.: %i/%i/%i",
                self._name,
                _oM["Direct"].nbcalls(0),
                _oM["Tangent"].nbcalls(0),
                _oM["Adjoint"].nbcalls(0),
            )
            logging.debug(
                "%s Nombre d'appels au cache d'opérateur d'évolution direct/tangent/adjoint..: %i/%i/%i",
                self._name,
                _oM["Direct"].nbcalls(3),
                _oM["Tangent"].nbcalls(3),
                _oM["Adjoint"].nbcalls(3),
            )
        logging.debug(
            "%s Taille mémoire utilisée de %.0f Mio",
            self._name,
            self._m.getUsedMemory("Mio"),
        )
        logging.debug(
            "%s Durées d'utilisation CPU de %.1fs et elapsed de %.1fs",
            self._name,
            self._getTimeState()[0],
            self._getTimeState()[1],
        )
        logging.debug("%s Terminé", self._name)
        return 0

    def _toStore(self, key):
        "True if in StoreSupplementaryCalculations, else False"
        return key in self._parameters["StoreSupplementaryCalculations"]

    def get(self, key=None):
        """
        Renvoie l'une des variables stockées identifiée par la clé, ou le
        dictionnaire de l'ensemble des variables disponibles en l'absence de
        clé. Ce sont directement les variables sous forme objet qui sont
        renvoyées, donc les méthodes d'accès à l'objet individuel sont celles
        des classes de persistance.
        """
        if key is not None:
            return self.StoredVariables[self.__canonical_stored_name[key.lower()]]
        else:
            return self.StoredVariables

    def __contains__(self, key=None):
        "D.__contains__(k) -> True if D has a key k, else False"
        if key is None or key.lower() not in self.__canonical_stored_name:
            return False
        else:
            return self.__canonical_stored_name[key.lower()] in self.StoredVariables

    def keys(self):
        "D.keys() -> list of D's keys"
        if hasattr(self, "StoredVariables"):
            return self.StoredVariables.keys()
        else:
            return []

    def pop(self, k, d):
        "D.pop(k[,d]) -> v, remove specified key and return the corresponding value"
        if (
            hasattr(self, "StoredVariables")
            and k.lower() in self.__canonical_stored_name
        ):
            return self.StoredVariables.pop(self.__canonical_stored_name[k.lower()], d)
        else:
            try:
                msg = "'%s'" % k
            except Exception:
                raise TypeError("pop expected at least 1 arguments, got 0")
            "If key is not found, d is returned if given, otherwise KeyError is raised"
            try:
                return d
            except Exception:
                raise KeyError(msg)

    def run(
        self,
        Xb=None,
        Y=None,
        U=None,
        HO=None,
        EM=None,
        CM=None,
        R=None,
        B=None,
        Q=None,
        Parameters=None,
    ):
        """
        Doit implémenter l'opération élémentaire de calcul algorithmique.
        """
        raise NotImplementedError(
            "Mathematical algorithmic calculation has not been implemented!"
        )

    def defineRequiredParameter(
        self,
        name=None,
        default=None,
        typecast=None,
        message=None,
        minval=None,
        maxval=None,
        listval=None,
        listadv=None,
        oldname=None,
    ):
        """
        Permet de définir dans l'algorithme des paramètres requis et leurs
        caractéristiques par défaut.
        """
        if name is None:
            raise ValueError("A name is mandatory to define a required parameter.")
        #
        self.__required_parameters[name] = {
            "default": default,
            "typecast": typecast,
            "minval": minval,
            "maxval": maxval,
            "listval": listval,
            "listadv": listadv,
            "message": message,
            "oldname": oldname,
        }
        self.__canonical_parameter_name[name.lower()] = name
        if oldname is not None:
            self.__canonical_parameter_name[oldname.lower()] = name  # Conversion
            self.__replace_by_the_new_name[oldname.lower()] = name
        logging.debug(
            "%s %s (valeur par défaut = %s)",
            self._name,
            message,
            self.setParameterValue(name),
        )

    def getRequiredParameters(self, noDetails=True):
        """
        Renvoie la liste des noms de paramètres requis ou directement le
        dictionnaire des paramètres requis.
        """
        if noDetails:
            return sorted(self.__required_parameters.keys())
        else:
            return self.__required_parameters

    def setParameterValue(self, name=None, value=None):
        """
        Renvoie la valeur d'un paramètre requis de manière contrôlée
        """
        __k = self.__canonical_parameter_name[name.lower()]
        default = self.__required_parameters[__k]["default"]
        typecast = self.__required_parameters[__k]["typecast"]
        minval = self.__required_parameters[__k]["minval"]
        maxval = self.__required_parameters[__k]["maxval"]
        listval = self.__required_parameters[__k]["listval"]
        listadv = self.__required_parameters[__k]["listadv"]
        #
        if value is None and default is None:
            __val = None
        elif value is None and default is not None:
            if typecast is None:
                __val = default
            else:
                __val = typecast(default)
        else:
            if typecast is None:
                __val = value
            else:
                try:
                    __val = typecast(value)
                except Exception:
                    raise ValueError(
                        "The value '%s' for the parameter named '%s' can not be correctly evaluated with type '%s'."
                        % (value, __k, typecast)
                    )
        #
        if minval is not None and (numpy.array(__val, float) < minval).any():
            raise ValueError(
                "The parameter named '%s' of value '%s' can not be less than %s."
                % (__k, __val, minval)
            )
        if maxval is not None and (numpy.array(__val, float) > maxval).any():
            raise ValueError(
                "The parameter named '%s' of value '%s' can not be greater than %s."
                % (__k, __val, maxval)
            )
        if listval is not None or listadv is not None:
            if (
                typecast is list
                or typecast is tuple
                or isinstance(__val, list)
                or isinstance(__val, tuple)
            ):
                for v in __val:
                    if listval is not None and v in listval:
                        continue
                    elif listadv is not None and v in listadv:
                        continue
                    else:
                        raise ValueError(
                            "The value '%s' is not allowed for the parameter named '%s', it has to be in the list %s."
                            % (v, __k, listval)
                        )
            elif not (listval is not None and __val in listval) and not (
                listadv is not None and __val in listadv
            ):
                raise ValueError(
                    "The value '%s' is not allowed for the parameter named '%s', it has to be in the list %s."
                    % (__val, __k, listval)
                )
        #
        if __k in [
            "SetSeed",
        ]:
            __val = value
        #
        return __val

    def requireInputArguments(self, mandatory=(), optional=()):
        """
        Permet d'imposer des arguments de calcul requis en entrée.
        """
        self.__required_inputs["RequiredInputValues"]["mandatory"] = tuple(mandatory)
        self.__required_inputs["RequiredInputValues"]["optional"] = tuple(optional)

    def getInputArguments(self):
        """
        Permet d'obtenir les listes des arguments de calcul requis en entrée.
        """
        return (
            self.__required_inputs["RequiredInputValues"]["mandatory"],
            self.__required_inputs["RequiredInputValues"]["optional"],
        )

    def setAttributes(self, tags=(), features=()):
        """
        Permet d'adjoindre des attributs comme les tags de classification.
        Renvoie la liste actuelle dans tous les cas.
        """
        self.__required_inputs["AttributesTags"].extend(tags)
        self.__required_inputs["AttributesFeatures"].extend(features)
        return (
            self.__required_inputs["AttributesTags"],
            self.__required_inputs["AttributesFeatures"],
        )

    def __setParameters(self, fromDico={}, reset=False):
        """
        Permet de stocker les paramètres reçus dans le dictionnaire interne.
        """
        self._parameters.update(fromDico)
        __inverse_fromDico_keys = {}
        for k in fromDico.keys():
            if k.lower() in self.__canonical_parameter_name:
                __inverse_fromDico_keys[self.__canonical_parameter_name[k.lower()]] = k
        # __inverse_fromDico_keys = dict([(self.__canonical_parameter_name[k.lower()],k) for k in fromDico.keys()])
        __canonic_fromDico_keys = __inverse_fromDico_keys.keys()
        #
        for k in __inverse_fromDico_keys.values():
            if k.lower() in self.__replace_by_the_new_name:
                __newk = self.__replace_by_the_new_name[k.lower()]
                __msg = (
                    'the parameter "%s" used in "%s" algorithm case is deprecated and has to be replaced by "%s".'
                    % (k, self._name, __newk)
                )
                __msg += " Please update your code."
                warnings.warn(__msg, FutureWarning, stacklevel=50)
        #
        for k in self.__required_parameters.keys():
            if k in __canonic_fromDico_keys:
                self._parameters[k] = self.setParameterValue(
                    k, fromDico[__inverse_fromDico_keys[k]]
                )
            elif reset:
                self._parameters[k] = self.setParameterValue(k)
            else:
                pass
            if hasattr(self._parameters[k], "size") and self._parameters[k].size > 100:
                logging.debug(
                    "%s %s d'une taille totale de %s",
                    self._name,
                    self.__required_parameters[k]["message"],
                    self._parameters[k].size,
                )
            elif (
                hasattr(self._parameters[k], "__len__")
                and len(self._parameters[k]) > 100
            ):
                logging.debug(
                    "%s %s de longueur %s",
                    self._name,
                    self.__required_parameters[k]["message"],
                    len(self._parameters[k]),
                )
            else:
                logging.debug(
                    "%s %s : %s",
                    self._name,
                    self.__required_parameters[k]["message"],
                    self._parameters[k],
                )

    def _setInternalState(self, key=None, value=None, fromDico={}, reset=False):
        """
        Permet de stocker des variables nommées constituant l'état interne
        """
        if reset:  # Vide le dictionnaire préalablement
            self.__internal_state = {}
        if key is not None and value is not None:
            self.__internal_state[key] = value
        self.__internal_state.update(dict(fromDico))

    def _getInternalState(self, key=None):
        """
        Restitue un état interne sous la forme d'un dictionnaire de variables nommées
        """
        if key is not None and key in self.__internal_state:
            return self.__internal_state[key]
        else:
            return self.__internal_state

    def _getTimeState(self, reset=False):
        """
        Initialise ou restitue le temps de calcul (cpu/elapsed) à la seconde
        """
        if reset:
            self.__initial_cpu_time = time.process_time()
            self.__initial_elapsed_time = time.perf_counter()
            return 0.0, 0.0
        else:
            self.__cpu_time = time.process_time() - self.__initial_cpu_time
            self.__elapsed_time = time.perf_counter() - self.__initial_elapsed_time
            return self.__cpu_time, self.__elapsed_time

    def _StopOnTimeLimit(self, X=None, withReason=False):
        "Stop criteria on time limit: True/False [+ Reason]"
        c, e = self._getTimeState()
        if (
            "MaximumCpuTime" in self._parameters
            and c > self._parameters["MaximumCpuTime"]
        ):
            __SC, __SR = True, "Reached maximum CPU time (%.1fs > %.1fs)" % (
                c,
                self._parameters["MaximumCpuTime"],
            )
        elif (
            "MaximumElapsedTime" in self._parameters
            and e > self._parameters["MaximumElapsedTime"]
        ):
            __SC, __SR = True, "Reached maximum elapsed time (%.1fs > %.1fs)" % (
                e,
                self._parameters["MaximumElapsedTime"],
            )
        else:
            __SC, __SR = False, ""
        if withReason:
            return __SC, __SR
        else:
            return __SC


# ==============================================================================
class PartialAlgorithm(object):
    """
    Classe pour mimer "Algorithm" du point de vue stockage, mais sans aucune
    action avancée comme la vérification . Pour les méthodes reprises ici,
    le fonctionnement est identique à celles de la classe "Algorithm".
    """

    __slots__ = (
        "_name",
        "_parameters",
        "StoredVariables",
        "__canonical_stored_name",
    )

    def __init__(self, name):
        self._name = str(name)
        self._parameters = {"StoreSupplementaryCalculations": []}
        #
        self.StoredVariables = {}
        self.StoredVariables["Analysis"] = Persistence.OneVector(name="Analysis")
        self.StoredVariables["CostFunctionJ"] = Persistence.OneScalar(
            name="CostFunctionJ"
        )
        self.StoredVariables["CostFunctionJb"] = Persistence.OneScalar(
            name="CostFunctionJb"
        )
        self.StoredVariables["CostFunctionJo"] = Persistence.OneScalar(
            name="CostFunctionJo"
        )
        self.StoredVariables["CurrentIterationNumber"] = Persistence.OneIndex(
            name="CurrentIterationNumber"
        )
        self.StoredVariables["CurrentStepNumber"] = Persistence.OneIndex(
            name="CurrentStepNumber"
        )
        #
        self.__canonical_stored_name = {}
        for k in self.StoredVariables:
            self.__canonical_stored_name[k.lower()] = k

    def _toStore(self, key):
        "True if in StoreSupplementaryCalculations, else False"
        return key in self._parameters["StoreSupplementaryCalculations"]

    def get(self, key=None):
        """
        Renvoie l'une des variables stockées identifiée par la clé, ou le
        dictionnaire de l'ensemble des variables disponibles en l'absence de
        clé. Ce sont directement les variables sous forme objet qui sont
        renvoyées, donc les méthodes d'accès à l'objet individuel sont celles
        des classes de persistance.
        """
        if key is not None:
            return self.StoredVariables[self.__canonical_stored_name[key.lower()]]
        else:
            return self.StoredVariables


# ==============================================================================
class AlgorithmAndParameters(object):
    """
    Classe générale d'interface d'action pour l'algorithme et ses paramètres
    """

    __slots__ = (
        "__name",
        "__algorithm",
        "__algorithmFile",
        "__algorithmName",
        "__A",
        "__P",
        "__Xb",
        "__Y",
        "__U",
        "__HO",
        "__EM",
        "__CM",
        "__B",
        "__R",
        "__Q",
        "__variable_names_not_public",
    )

    def __init__(
        self, name="GenericAlgorithm", asAlgorithm=None, asDict=None, asScript=None
    ):
        """ """
        self.__name = str(name)
        self.__A = None
        self.__P = {}
        #
        self.__algorithm = {}
        self.__algorithmFile = None
        self.__algorithmName = None
        #
        self.updateParameters(asDict, asScript)
        #
        if asAlgorithm is None and asScript is not None:
            __Algo = Interfaces.ImportFromScript(asScript).getvalue("Algorithm")
        else:
            __Algo = asAlgorithm
        #
        if __Algo is not None:
            self.__A = str(__Algo)
            self.__P.update({"Algorithm": self.__A})
        #
        self.__setAlgorithm(self.__A)
        #
        self.__variable_names_not_public = {
            "nextStep": False
        }  # Duplication dans Algorithm

    def updateParameters(self, asDict=None, asScript=None):
        "Mise à jour des paramètres"
        if asDict is None and asScript is not None:
            __Dict = Interfaces.ImportFromScript(asScript).getvalue(
                self.__name, "Parameters"
            )
        else:
            __Dict = asDict
        #
        if __Dict is not None:
            self.__P.update(dict(__Dict))

    def executePythonScheme(self, asDictAO=None):
        "Permet de lancer le calcul d'assimilation"
        Operator.CM.clearCache()
        #
        if not isinstance(asDictAO, dict):
            raise ValueError(
                "The objects for algorithm calculation have to be given together as a dictionnary, and they are not"
            )
        if hasattr(asDictAO["Background"], "getO"):
            self.__Xb = asDictAO["Background"].getO()
        elif hasattr(asDictAO["CheckingPoint"], "getO"):
            self.__Xb = asDictAO["CheckingPoint"].getO()
        else:
            self.__Xb = None
        if hasattr(asDictAO["Observation"], "getO"):
            self.__Y = asDictAO["Observation"].getO()
        else:
            self.__Y = asDictAO["Observation"]
        if hasattr(asDictAO["ControlInput"], "getO"):
            self.__U = asDictAO["ControlInput"].getO()
        else:
            self.__U = asDictAO["ControlInput"]
        if hasattr(asDictAO["ObservationOperator"], "getO"):
            self.__HO = asDictAO["ObservationOperator"].getO()
        else:
            self.__HO = asDictAO["ObservationOperator"]
        if hasattr(asDictAO["EvolutionModel"], "getO"):
            self.__EM = asDictAO["EvolutionModel"].getO()
        else:
            self.__EM = asDictAO["EvolutionModel"]
        if hasattr(asDictAO["ControlModel"], "getO"):
            self.__CM = asDictAO["ControlModel"].getO()
        else:
            self.__CM = asDictAO["ControlModel"]
        self.__B = asDictAO["BackgroundError"]
        self.__R = asDictAO["ObservationError"]
        self.__Q = asDictAO["EvolutionError"]
        #
        self.__shape_validate()
        #
        self.__algorithm.run(
            Xb=self.__Xb,
            Y=self.__Y,
            U=self.__U,
            HO=self.__HO,
            EM=self.__EM,
            CM=self.__CM,
            R=self.__R,
            B=self.__B,
            Q=self.__Q,
            Parameters=self.__P,
        )
        return 0

    def executeYACSScheme(self, FileName=None):
        "Permet de lancer le calcul d'assimilation"
        if FileName is None or not os.path.exists(FileName):
            raise ValueError("a YACS file name has to be given for YACS execution.\n")
        else:
            __file = os.path.abspath(FileName)
            logging.debug('The YACS file name is "%s".' % __file)
        if (
            not PlatformInfo.has_salome
            or not PlatformInfo.has_yacs
            or not PlatformInfo.has_adao
        ):
            raise ImportError(
                "\n\n"
                + "Unable to get SALOME, YACS or ADAO environnement variables.\n"
                + "Please load the right environnement before trying to use it.\n"
            )
        #
        import pilot
        import SALOMERuntime
        import loader

        SALOMERuntime.RuntimeSALOME_setRuntime()

        r = pilot.getRuntime()
        xmlLoader = loader.YACSLoader()
        xmlLoader.registerProcCataLoader()
        try:
            catalogAd = r.loadCatalog("proc", __file)
            r.addCatalog(catalogAd)
        except Exception:
            pass

        try:
            p = xmlLoader.load(__file)
        except IOError as ex:
            print("The YACS XML schema file can not be loaded: %s" % (ex,))

        logger = p.getLogger("parser")
        if not logger.isEmpty():
            print("The imported YACS XML schema has errors on parsing:")
            print(logger.getStr())

        if not p.isValid():
            print("The YACS XML schema is not valid and will not be executed:")
            print(p.getErrorReport())

        info = pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
        p.checkConsistency(info)
        if info.areWarningsOrErrors():
            print("The YACS XML schema is not coherent and will not be executed:")
            print(info.getGlobalRepr())

        e = pilot.ExecutorSwig()
        e.RunW(p)
        if p.getEffectiveState() != pilot.DONE:
            print(p.getErrorReport())
        #
        return 0

    def get(self, key=None):
        "Vérifie l'existence d'une clé de variable ou de paramètres"
        if key in self.__algorithm:
            return self.__algorithm.get(key)
        elif key in self.__P:
            return self.__P[key]
        else:
            allvariables = self.__P
            for k in self.__variable_names_not_public:
                allvariables.pop(k, None)
            return allvariables

    def pop(self, k, d):
        "Necessaire pour le pickling"
        return self.__algorithm.pop(k, d)

    def getAlgorithmRequiredParameters(self, noDetails=True):
        "Renvoie la liste des paramètres requis selon l'algorithme"
        return self.__algorithm.getRequiredParameters(noDetails)

    def getAlgorithmInputArguments(self):
        "Renvoie la liste des entrées requises selon l'algorithme"
        return self.__algorithm.getInputArguments()

    def getAlgorithmAttributes(self):
        "Renvoie la liste des attributs selon l'algorithme"
        return self.__algorithm.setAttributes()

    def setObserver(self, __V, __O, __I, __A, __S):
        "Associe un observer à une variable unique"
        if (
            self.__algorithm is None
            or isinstance(self.__algorithm, dict)
            or not hasattr(self.__algorithm, "StoredVariables")
        ):
            raise ValueError("No observer can be build before choosing an algorithm.")
        if __V not in self.__algorithm:
            raise ValueError(
                "An observer requires to be set on a variable named %s which does not exist."
                % __V
            )
        else:
            self.__algorithm.StoredVariables[__V].setDataObserver(
                HookFunction=__O, HookParameters=__I, Scheduler=__S
            )

    def setCrossObserver(self, __V, __O, __I, __A, __S):
        "Associe un observer à une collection ordonnée de variables"
        if (
            self.__algorithm is None
            or isinstance(self.__algorithm, dict)
            or not hasattr(self.__algorithm, "StoredVariables")
        ):
            raise ValueError("No observer can be build before choosing an algorithm.")
        if not isinstance(__V, (list, tuple)):
            raise ValueError(
                "A cross observer requires to be set on a variable series which"
                + " is not the case of %s." % __V
            )
        if len(__V) != len(__I):
            raise ValueError(
                "The number of information fields has to be the same than the"
                + " number of variables on which to set the observer."
            )
        #
        for __eV in __V:
            if __eV not in self.__algorithm:
                raise ValueError(
                    "An observer requires to be set on a variable named %s which does not exist."
                    % __eV
                )
            else:
                self.__algorithm.StoredVariables[__eV].setDataObserver(
                    HookFunction=__O,
                    HookParameters=__I,
                    Scheduler=__S,
                    Order=__V,
                    OSync=__A,
                    DOVar=self.__algorithm.StoredVariables,
                )

    def removeObserver(self, __V, __O, __A=False):
        if (
            self.__algorithm is None
            or isinstance(self.__algorithm, dict)
            or not hasattr(self.__algorithm, "StoredVariables")
        ):
            raise ValueError("No observer can be removed before choosing an algorithm.")
        if __V not in self.__algorithm:
            raise ValueError(
                "An observer requires to be removed on a variable named %s which does not exist."
                % __V
            )
        else:
            return self.__algorithm.StoredVariables[__V].removeDataObserver(
                HookFunction=__O, AllObservers=__A
            )

    def hasObserver(self, __V):
        if (
            self.__algorithm is None
            or isinstance(self.__algorithm, dict)
            or not hasattr(self.__algorithm, "StoredVariables")
        ):
            return False
        if __V not in self.__algorithm:
            return False
        return self.__algorithm.StoredVariables[__V].hasDataObserver()

    def keys(self):
        __allvariables = list(self.__algorithm.keys()) + list(self.__P.keys())
        for k in self.__variable_names_not_public:
            if k in __allvariables:
                __allvariables.remove(k)
        return __allvariables

    def __contains__(self, key=None):
        "D.__contains__(k) -> True if D has a key k, else False"
        return key in self.__algorithm or key in self.__P

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__A) + ", " + repr(self.__P)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__A) + ", " + str(self.__P)

    def __setAlgorithm(self, choice=None):
        """
        Permet de sélectionner l'algorithme à utiliser pour mener à bien l'étude
        d'assimilation. L'argument est un champ caractère se rapportant au nom
        d'un algorithme réalisant l'opération sur les arguments fixes.
        """
        if choice is None:
            raise ValueError("Error: algorithm choice has to be given")
        if self.__algorithmName is not None:
            raise ValueError(
                'Error: algorithm choice has already been done as "%s", it can\'t be changed.'
                % self.__algorithmName
            )
        daDirectory = "daAlgorithms"
        #
        # Recherche explicitement le fichier complet
        # ------------------------------------------
        module_path = None
        for directory in sys.path:
            if os.path.isfile(
                os.path.join(directory, daDirectory, str(choice) + ".py")
            ):
                module_path = os.path.abspath(os.path.join(directory, daDirectory))
        if module_path is None:
            raise ImportError(
                'No algorithm module named "%s" has been found in the search path.'
                % choice
                + "\n             The search path is %s" % sys.path
            )
        #
        # Importe le fichier complet comme un module
        # ------------------------------------------
        try:
            sys_path_tmp = sys.path
            sys.path.insert(0, module_path)
            self.__algorithmFile = __import__(str(choice), globals(), locals(), [])
            if not hasattr(self.__algorithmFile, "ElementaryAlgorithm"):
                raise ImportError(
                    "this module does not define a valid elementary algorithm."
                )
            self.__algorithmName = str(choice)
            sys.path = sys_path_tmp
            del sys_path_tmp
        except ImportError as e:
            raise ImportError(
                'The module named "%s" was found, but is incorrect at the import stage.'
                % choice
                + "\n             The import error message is: %s" % e
            )
        #
        # Instancie un objet du type élémentaire du fichier
        # -------------------------------------------------
        self.__algorithm = self.__algorithmFile.ElementaryAlgorithm()
        return 0

    def __shape_validate(self):
        """
        Validation de la correspondance correcte des tailles des variables et
        des matrices s'il y en a.
        """
        if self.__Xb is None:
            __Xb_shape = (0,)
        elif hasattr(self.__Xb, "size"):
            __Xb_shape = (self.__Xb.size,)
        elif hasattr(self.__Xb, "shape"):
            if isinstance(self.__Xb.shape, tuple):
                __Xb_shape = self.__Xb.shape
            else:
                __Xb_shape = self.__Xb.shape()
        else:
            raise TypeError("The background (Xb) has no attribute of shape: problem!")
        #
        if self.__Y is None:
            __Y_shape = (0,)
        elif hasattr(self.__Y, "size"):
            __Y_shape = (self.__Y.size,)
        elif hasattr(self.__Y, "shape"):
            if isinstance(self.__Y.shape, tuple):
                __Y_shape = self.__Y.shape
            else:
                __Y_shape = self.__Y.shape()
        else:
            raise TypeError("The observation (Y) has no attribute of shape: problem!")
        #
        if self.__U is None:
            __U_shape = (0,)
        elif hasattr(self.__U, "size"):
            __U_shape = (self.__U.size,)
        elif hasattr(self.__U, "shape"):
            if isinstance(self.__U.shape, tuple):
                __U_shape = self.__U.shape
            else:
                __U_shape = self.__U.shape()
        else:
            raise TypeError("The control (U) has no attribute of shape: problem!")
        #
        if self.__B is None:
            __B_shape = (0, 0)
        elif hasattr(self.__B, "shape"):
            if isinstance(self.__B.shape, tuple):
                __B_shape = self.__B.shape
            else:
                __B_shape = self.__B.shape()
        else:
            raise TypeError(
                "The a priori errors covariance matrix (B) has no attribute of shape: problem!"
            )
        #
        if self.__R is None:
            __R_shape = (0, 0)
        elif hasattr(self.__R, "shape"):
            if isinstance(self.__R.shape, tuple):
                __R_shape = self.__R.shape
            else:
                __R_shape = self.__R.shape()
        else:
            raise TypeError(
                "The observation errors covariance matrix (R) has no attribute of shape: problem!"
            )
        #
        if self.__Q is None:
            __Q_shape = (0, 0)
        elif hasattr(self.__Q, "shape"):
            if isinstance(self.__Q.shape, tuple):
                __Q_shape = self.__Q.shape
            else:
                __Q_shape = self.__Q.shape()
        else:
            raise TypeError(
                "The evolution errors covariance matrix (Q) has no attribute of shape: problem!"
            )
        #
        if len(self.__HO) == 0:
            __HO_shape = (0, 0)
        elif isinstance(self.__HO, dict):
            __HO_shape = (0, 0)
        elif hasattr(self.__HO["Direct"], "shape"):
            if isinstance(self.__HO["Direct"].shape, tuple):
                __HO_shape = self.__HO["Direct"].shape
            else:
                __HO_shape = self.__HO["Direct"].shape()
        else:
            raise TypeError(
                "The observation operator (H) has no attribute of shape: problem!"
            )
        #
        if len(self.__EM) == 0:
            __EM_shape = (0, 0)
        elif isinstance(self.__EM, dict):
            __EM_shape = (0, 0)
        elif hasattr(self.__EM["Direct"], "shape"):
            if isinstance(self.__EM["Direct"].shape, tuple):
                __EM_shape = self.__EM["Direct"].shape
            else:
                __EM_shape = self.__EM["Direct"].shape()
        else:
            raise TypeError(
                "The evolution model (EM) has no attribute of shape: problem!"
            )
        #
        if len(self.__CM) == 0:
            __CM_shape = (0, 0)
        elif isinstance(self.__CM, dict):
            __CM_shape = (0, 0)
        elif hasattr(self.__CM["Direct"], "shape"):
            if isinstance(self.__CM["Direct"].shape, tuple):
                __CM_shape = self.__CM["Direct"].shape
            else:
                __CM_shape = self.__CM["Direct"].shape()
        else:
            raise TypeError(
                "The control model (CM) has no attribute of shape: problem!"
            )
        #
        # Vérification des conditions
        # ---------------------------
        if not (len(__Xb_shape) == 1 or min(__Xb_shape) == 1):
            raise ValueError(
                'Shape characteristic of background (Xb) is incorrect: "%s".'
                % (__Xb_shape,)
            )
        if not (len(__Y_shape) == 1 or min(__Y_shape) == 1):
            raise ValueError(
                'Shape characteristic of observation (Y) is incorrect: "%s".'
                % (__Y_shape,)
            )
        #
        if not (min(__B_shape) == max(__B_shape)):
            raise ValueError(
                'Shape characteristic of a priori errors covariance matrix (B) is incorrect: "%s".'
                % (__B_shape,)
            )
        if not (min(__R_shape) == max(__R_shape)):
            raise ValueError(
                'Shape characteristic of observation errors covariance matrix (R) is incorrect: "%s".'
                % (__R_shape,)
            )
        if not (min(__Q_shape) == max(__Q_shape)):
            raise ValueError(
                'Shape characteristic of evolution errors covariance matrix (Q) is incorrect: "%s".'
                % (__Q_shape,)
            )
        if not (min(__EM_shape) == max(__EM_shape)):
            raise ValueError(
                'Shape characteristic of evolution operator (EM) is incorrect: "%s".'
                % (__EM_shape,)
            )
        #
        if (
            len(self.__HO) > 0
            and not isinstance(self.__HO, dict)
            and not (__HO_shape[1] == max(__Xb_shape))
        ):
            raise ValueError(
                "Shape characteristic of observation operator (H)"
                + ' "%s" and state (X) "%s" are incompatible.'
                % (__HO_shape, __Xb_shape)
            )
        if (
            len(self.__HO) > 0
            and not isinstance(self.__HO, dict)
            and not (__HO_shape[0] == max(__Y_shape))
        ):
            raise ValueError(
                "Shape characteristic of observation operator (H)"
                + ' "%s" and observation (Y) "%s" are incompatible.'
                % (__HO_shape, __Y_shape)
            )
        if (
            len(self.__HO) > 0
            and not isinstance(self.__HO, dict)
            and len(self.__B) > 0
            and not (__HO_shape[1] == __B_shape[0])
        ):
            raise ValueError(
                "Shape characteristic of observation operator (H)"
                + ' "%s" and a priori errors covariance matrix (B) "%s" are incompatible.'
                % (__HO_shape, __B_shape)
            )
        if (
            len(self.__HO) > 0
            and not isinstance(self.__HO, dict)
            and len(self.__R) > 0
            and not (__HO_shape[0] == __R_shape[1])
        ):
            raise ValueError(
                "Shape characteristic of observation operator (H)"
                + ' "%s" and observation errors covariance matrix (R) "%s" are incompatible.'
                % (__HO_shape, __R_shape)
            )
        #
        if (
            self.__B is not None
            and len(self.__B) > 0
            and not (__B_shape[1] == max(__Xb_shape))
        ):
            if self.__algorithmName in [
                "EnsembleBlue",
            ]:
                asPersistentVector = self.__Xb.reshape((-1, min(__B_shape)))
                self.__Xb = Persistence.OneVector("Background")
                for member in asPersistentVector:
                    self.__Xb.store(numpy.asarray(member, dtype=float))
                __Xb_shape = min(__B_shape)
            else:
                raise ValueError(
                    "Shape characteristic of a priori errors covariance matrix (B)"
                    + ' "%s" and background vector (Xb) "%s" are incompatible.'
                    % (__B_shape, __Xb_shape)
                )
        #
        if (
            self.__R is not None
            and len(self.__R) > 0
            and not (__R_shape[1] == max(__Y_shape))
        ):
            raise ValueError(
                "Shape characteristic of observation errors covariance matrix (R)"
                + ' "%s" and observation vector (Y) "%s" are incompatible.'
                % (__R_shape, __Y_shape)
            )
        #
        if (
            self.__EM is not None
            and len(self.__EM) > 0
            and not isinstance(self.__EM, dict)
            and not (__EM_shape[1] == max(__Xb_shape))
        ):
            raise ValueError(
                "Shape characteristic of evolution model (EM)"
                + ' "%s" and state (X) "%s" are incompatible.'
                % (__EM_shape, __Xb_shape)
            )
        #
        if (
            self.__CM is not None
            and len(self.__CM) > 0
            and not isinstance(self.__CM, dict)
            and not (__CM_shape[1] == max(__U_shape))
        ):
            raise ValueError(
                "Shape characteristic of control model (CM)"
                + ' "%s" and control (U) "%s" are incompatible.'
                % (__CM_shape, __U_shape)
            )
        #
        if (
            ("Bounds" in self.__P)
            and isinstance(self.__P["Bounds"], (list, tuple))
            and (len(self.__P["Bounds"]) != max(__Xb_shape))
        ):
            if len(self.__P["Bounds"]) > 0:
                raise ValueError(
                    "The number '%s' of bound pairs for the state components"
                    % len(self.__P["Bounds"])
                    + " is different from the size '%s' of the state (X) itself."
                    % max(__Xb_shape)
                )
            else:
                self.__P["Bounds"] = None
        if (
            ("Bounds" in self.__P)
            and isinstance(self.__P["Bounds"], (numpy.ndarray, numpy.matrix))
            and (self.__P["Bounds"].shape[0] != max(__Xb_shape))
        ):
            if self.__P["Bounds"].size > 0:
                raise ValueError(
                    "The number '%s' of bound pairs for the state components"
                    % self.__P["Bounds"].shape[0]
                    + " is different from the size '%s' of the state (X) itself."
                    % max(__Xb_shape)
                )
            else:
                self.__P["Bounds"] = None
        #
        if (
            ("BoxBounds" in self.__P)
            and isinstance(self.__P["BoxBounds"], (list, tuple))
            and (len(self.__P["BoxBounds"]) != max(__Xb_shape))
        ):
            raise ValueError(
                "The number '%s' of bound pairs for the state box components"
                % len(self.__P["BoxBounds"])
                + " is different from the size '%s' of the state (X) itself."
                % max(__Xb_shape)
            )
        if (
            ("BoxBounds" in self.__P)
            and isinstance(self.__P["BoxBounds"], (numpy.ndarray, numpy.matrix))
            and (self.__P["BoxBounds"].shape[0] != max(__Xb_shape))
        ):
            raise ValueError(
                "The number '%s' of bound pairs for the state box components"
                % self.__P["BoxBounds"].shape[0]
                + " is different from the size '%s' of the state (X) itself."
                % max(__Xb_shape)
            )
        #
        if (
            ("StateBoundsForQuantiles" in self.__P)
            and isinstance(self.__P["StateBoundsForQuantiles"], (list, tuple))
            and (len(self.__P["StateBoundsForQuantiles"]) != max(__Xb_shape))
        ):
            raise ValueError(
                "The number '%s' of bound pairs for the quantile state components"
                % len(self.__P["StateBoundsForQuantiles"])
                + " is different from the size '%s' of the state (X) itself."
                % max(__Xb_shape)
            )
        #
        return 1


# ==============================================================================
class RegulationAndParameters(object):
    """
    Classe générale d'interface d'action pour la régulation et ses paramètres
    """

    __slots__ = ("__name", "__P")

    def __init__(
        self, name="GenericRegulation", asAlgorithm=None, asDict=None, asScript=None
    ):
        """ """
        self.__name = str(name)
        self.__P = {}
        #
        if asAlgorithm is None and asScript is not None:
            __Algo = Interfaces.ImportFromScript(asScript).getvalue("Algorithm")
        else:
            __Algo = asAlgorithm
        #
        if asDict is None and asScript is not None:
            __Dict = Interfaces.ImportFromScript(asScript).getvalue(
                self.__name, "Parameters"
            )
        else:
            __Dict = asDict
        #
        if __Dict is not None:
            self.__P.update(dict(__Dict))
        #
        if __Algo is not None:
            self.__P.update({"Algorithm": str(__Algo)})

    def get(self, key=None):
        "Vérifie l'existence d'une clé de variable ou de paramètres"
        if key in self.__P:
            return self.__P[key]
        else:
            return self.__P


# ==============================================================================
class DataObserver(object):
    """
    Classe générale d'interface de type observer
    """

    __slots__ = ("__name", "__V", "__O", "__I")

    def __init__(
        self,
        name="GenericObserver",
        onVariable=None,
        asTemplate=None,
        asString=None,
        asScript=None,
        asObsObject=None,
        withInfo=None,
        crossObs=False,
        syncObs=True,
        scheduledBy=None,
        withAlgo=None,
    ):
        """ """
        self.__name = str(name)
        self.__V = None
        self.__O = None
        self.__I = None
        #
        if onVariable is None:
            raise ValueError(
                "setting an observer has to be done over a variable name or a list of variable names, not over None."
            )
        elif isinstance(onVariable, (tuple, list)):
            self.__V = tuple(map(str, onVariable))
            if withInfo is None:
                self.__I = self.__V
            elif crossObs or isinstance(withInfo, (tuple, list)):
                self.__I = withInfo
            else:
                self.__I = (str(withInfo),) * len(self.__V)
        elif isinstance(onVariable, str):
            self.__V = (onVariable,)
            if withInfo is None:
                self.__I = (onVariable,)
            else:
                self.__I = (str(withInfo),)
        else:
            raise ValueError(
                "setting an observer has to be done over a variable name or a list of variable names."
            )
        #
        if asObsObject is not None:
            self.__O = asObsObject
        else:
            __FunctionText = str(UserScript("Observer", asTemplate, asString, asScript))
            __Function = Observer2Func(__FunctionText)
            self.__O = __Function.getfunc()
        #
        for k in range(len(self.__V)):
            if self.__V[k] not in withAlgo:
                raise ValueError(
                    "An observer is asked to be set on a variable named %s which does not exist."
                    % self.__V[k]
                )
        #
        if bool(crossObs):
            withAlgo.setCrossObserver(
                self.__V, self.__O, self.__I, syncObs, scheduledBy
            )
        else:
            for k in range(len(self.__V)):
                withAlgo.setObserver(
                    self.__V[k], self.__O, self.__I[k], syncObs, scheduledBy
                )

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__V) + "\n" + repr(self.__O)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__V) + "\n" + str(self.__O)


# ==============================================================================
class UserScript(object):
    """
    Classe générale d'interface de type texte de script utilisateur
    """

    __slots__ = ("__name", "__F")

    def __init__(
        self, name="GenericUserScript", asTemplate=None, asString=None, asScript=None
    ):
        """ """
        self.__name = str(name)
        #
        if asString is not None:
            self.__F = asString
        elif (
            self.__name == "UserPostAnalysis"
            and (asTemplate is not None)
            and (asTemplate in Templates.UserPostAnalysisTemplates)
        ):
            self.__F = Templates.UserPostAnalysisTemplates[asTemplate]
        elif (
            self.__name == "Observer"
            and (asTemplate is not None)
            and (asTemplate in Templates.ObserverTemplates)
        ):
            self.__F = Templates.ObserverTemplates[asTemplate]
        elif asScript is not None:
            self.__F = Interfaces.ImportFromScript(asScript).getstring()
        else:
            self.__F = ""

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__F)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__F)


# ==============================================================================
class ExternalParameters(object):
    """
    Classe générale d'interface pour le stockage des paramètres externes
    """

    __slots__ = ("__name", "__P")

    def __init__(self, name="GenericExternalParameters", asDict=None, asScript=None):
        """ """
        self.__name = str(name)
        self.__P = {}
        #
        self.updateParameters(asDict, asScript)

    def updateParameters(self, asDict=None, asScript=None):
        "Mise à jour des paramètres"
        if asDict is None and asScript is not None:
            __Dict = Interfaces.ImportFromScript(asScript).getvalue(
                self.__name, "ExternalParameters"
            )
        else:
            __Dict = asDict
        #
        if __Dict is not None:
            self.__P.update(dict(__Dict))

    def get(self, key=None):
        if key in self.__P:
            return self.__P[key]
        else:
            return list(self.__P.keys())

    def keys(self):
        return list(self.__P.keys())

    def pop(self, k, d):
        return self.__P.pop(k, d)

    def items(self):
        return self.__P.items()

    def __contains__(self, key=None):
        "D.__contains__(k) -> True if D has a key k, else False"
        return key in self.__P


# ==============================================================================
class State(object):
    """
    Classe générale d'interface de type état
    """

    __slots__ = (
        "__name",
        "__check",
        "__V",
        "__T",
        "__is_vector",
        "__is_series",
        "shape",
        "size",
    )

    def __init__(
        self,
        name="GenericVector",
        asVector=None,
        asPersistentVector=None,
        asScript=None,
        asDataFile=None,
        colNames=None,
        colMajor=False,
        scheduledBy=None,
        toBeChecked=False,
    ):
        """
        Permet de définir un vecteur :
        - asVector : entrée des données, comme un vecteur compatible avec le
          constructeur de numpy.matrix, ou "True" si entrée par script.
        - asPersistentVector : entrée des données, comme une série de vecteurs
          compatible avec le constructeur de numpy.matrix, ou comme un objet de
          type Persistence, ou "True" si entrée par script.
        - asScript : si un script valide est donné contenant une variable
          nommée "name", la variable est de type "asVector" (par défaut) ou
          "asPersistentVector" selon que l'une de ces variables est placée à
          "True".
        - asDataFile : si un ou plusieurs fichiers valides sont donnés
          contenant des valeurs en colonnes, elles-mêmes nommées "colNames"
          (s'il n'y a pas de nom de colonne indiquée, on cherche une colonne
          nommée "name"), on récupère les colonnes et on les range ligne après
          ligne (colMajor=False, par défaut) ou colonne après colonne
          (colMajor=True). La variable résultante est de type "asVector" (par
          défaut) ou "asPersistentVector" selon que l'une de ces variables est
          placée à "True".
        """
        self.__name = str(name)
        self.__check = bool(toBeChecked)
        #
        self.__V = None
        self.__T = None
        self.__is_vector = False
        self.__is_series = False
        #
        if asScript is not None:
            __Vector, __Series = None, None
            if asPersistentVector:
                __Series = Interfaces.ImportFromScript(asScript).getvalue(self.__name)
            else:
                __Vector = Interfaces.ImportFromScript(asScript).getvalue(self.__name)
        elif asDataFile is not None:
            __Vector, __Series = None, None
            if asPersistentVector:
                if colNames is not None:
                    __Series = Interfaces.ImportFromFile(asDataFile).getvalue(colNames)[
                        1
                    ]
                else:
                    __Series = Interfaces.ImportFromFile(asDataFile).getvalue(
                        [
                            self.__name,
                        ]
                    )[1]
                if (
                    bool(colMajor)
                    and not Interfaces.ImportFromFile(asDataFile).getformat()
                    == "application/numpy.npz"
                ):
                    __Series = numpy.transpose(__Series)
                elif (
                    not bool(colMajor)
                    and Interfaces.ImportFromFile(asDataFile).getformat()
                    == "application/numpy.npz"
                ):
                    __Series = numpy.transpose(__Series)
            else:
                if colNames is not None:
                    __Vector = Interfaces.ImportFromFile(asDataFile).getvalue(colNames)[
                        1
                    ]
                else:
                    __Vector = Interfaces.ImportFromFile(asDataFile).getvalue(
                        [
                            self.__name,
                        ]
                    )[1]
                if bool(colMajor):
                    __Vector = numpy.ravel(__Vector, order="F")
                else:
                    __Vector = numpy.ravel(__Vector, order="C")
        else:
            __Vector, __Series = asVector, asPersistentVector
        #
        if __Vector is not None:
            self.__is_vector = True
            if isinstance(__Vector, str):
                __Vector = PlatformInfo.strvect2liststr(__Vector)
            self.__V = numpy.ravel(numpy.asarray(__Vector, dtype=float)).reshape(
                (-1, 1)
            )
            self.shape = self.__V.shape
            self.size = self.__V.size
        elif __Series is not None:
            self.__is_series = True
            if isinstance(__Series, (tuple, list, numpy.ndarray, numpy.matrix, str)):
                self.__V = Persistence.OneVector(self.__name)
                if isinstance(__Series, str):
                    __Series = PlatformInfo.strmatrix2liststr(__Series)
                for member in __Series:
                    if isinstance(member, str):
                        member = PlatformInfo.strvect2liststr(member)
                    self.__V.store(numpy.asarray(member, dtype=float))
            else:
                self.__V = __Series
            if isinstance(self.__V.shape, (tuple, list)):
                self.shape = self.__V.shape
            else:
                self.shape = self.__V.shape()
            if len(self.shape) == 1:
                self.shape = (self.shape[0], 1)
            self.size = self.shape[0] * self.shape[1]
        else:
            raise ValueError(
                "The %s object is improperly defined or undefined," % self.__name
                + " it requires at minima either a vector, a list/tuple of"
                + " vectors or a persistent object. Please check your vector input."
            )
        #
        if scheduledBy is not None:
            self.__T = scheduledBy

    def getO(self, withScheduler=False):
        if withScheduler:
            return self.__V, self.__T
        elif self.__T is None:
            return self.__V
        else:
            return self.__V

    def isvector(self):
        "Vérification du type interne"
        return self.__is_vector

    def isseries(self):
        "Vérification du type interne"
        return self.__is_series

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__V)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__V)


# ==============================================================================
class Covariance(object):
    """
    Classe générale d'interface de type covariance
    """

    __slots__ = (
        "__name",
        "__check",
        "__C",
        "__is_scalar",
        "__is_vector",
        "__is_matrix",
        "__is_object",
        "shape",
        "size",
    )

    def __init__(
        self,
        name="GenericCovariance",
        asCovariance=None,
        asEyeByScalar=None,
        asEyeByVector=None,
        asCovObject=None,
        asScript=None,
        toBeChecked=False,
    ):
        """
        Permet de définir une covariance :
        - asCovariance : entrée des données, comme une matrice compatible avec
          le constructeur de numpy.matrix
        - asEyeByScalar : entrée des données comme un seul scalaire de variance,
          multiplicatif d'une matrice de corrélation identité, aucune matrice
          n'étant donc explicitement à donner
        - asEyeByVector : entrée des données comme un seul vecteur de variance,
          à mettre sur la diagonale d'une matrice de corrélation, aucune matrice
          n'étant donc explicitement à donner
        - asCovObject : entrée des données comme un objet python, qui a les
          methodes obligatoires "getT", "getI", "diag", "trace", "__add__",
          "__sub__", "__neg__", "__mul__", "__rmul__" et facultatives "shape",
          "size", "cholesky", "choleskyI", "asfullmatrix", "__repr__", "__str__"
        - toBeChecked : booléen indiquant si le caractère SDP de la matrice
          pleine doit être vérifié
        """
        self.__name = str(name)
        self.__check = bool(toBeChecked)
        #
        self.__C = None
        self.__is_scalar = False
        self.__is_vector = False
        self.__is_matrix = False
        self.__is_object = False
        #
        if asScript is not None:
            __Matrix, __Scalar, __Vector, __Object = None, None, None, None
            if asEyeByScalar:
                __Scalar = Interfaces.ImportFromScript(asScript).getvalue(self.__name)
            elif asEyeByVector:
                __Vector = Interfaces.ImportFromScript(asScript).getvalue(self.__name)
            elif asCovObject:
                __Object = Interfaces.ImportFromScript(asScript).getvalue(self.__name)
            else:
                __Matrix = Interfaces.ImportFromScript(asScript).getvalue(self.__name)
        else:
            __Matrix, __Scalar, __Vector, __Object = (
                asCovariance,
                asEyeByScalar,
                asEyeByVector,
                asCovObject,
            )
        #
        if __Scalar is not None:
            if isinstance(__Scalar, str):
                __Scalar = PlatformInfo.strvect2liststr(__Scalar)
                if len(__Scalar) > 0:
                    __Scalar = __Scalar[0]
            if numpy.array(__Scalar).size != 1:
                raise ValueError(
                    "  The diagonal multiplier given to define a sparse matrix is"
                    + " not a unique scalar value.\n  Its actual measured size is"
                    + " %i. Please check your scalar input."
                    % numpy.array(__Scalar).size
                )
            self.__is_scalar = True
            self.__C = numpy.abs(float(__Scalar))
            self.shape = (0, 0)
            self.size = 0
        elif __Vector is not None:
            if isinstance(__Vector, str):
                __Vector = PlatformInfo.strvect2liststr(__Vector)
            self.__is_vector = True
            self.__C = numpy.abs(numpy.ravel(numpy.asarray(__Vector, dtype=float)))
            self.shape = (self.__C.size, self.__C.size)
            self.size = self.__C.size**2
        elif __Matrix is not None:
            self.__is_matrix = True
            self.__C = numpy.matrix(__Matrix, float)
            self.shape = self.__C.shape
            self.size = self.__C.size
        elif __Object is not None:
            self.__is_object = True
            self.__C = __Object
            for at in (
                "getT",
                "getI",
                "diag",
                "trace",
                "__add__",
                "__sub__",
                "__neg__",
                "__matmul__",
                "__mul__",
                "__rmatmul__",
                "__rmul__",
            ):
                if not hasattr(self.__C, at):
                    raise ValueError(
                        'The matrix given for %s as an object has no attribute "%s". Please check your object input.'
                        % (self.__name, at)
                    )
            if hasattr(self.__C, "shape"):
                self.shape = self.__C.shape
            else:
                self.shape = (0, 0)
            if hasattr(self.__C, "size"):
                self.size = self.__C.size
            else:
                self.size = 0
        else:
            pass
        #
        self.__validate()

    def __validate(self):
        "Validation"
        if self.__C is None:
            raise UnboundLocalError(
                "%s covariance matrix value has not been set!" % (self.__name,)
            )
        if self.ismatrix() and min(self.shape) != max(self.shape):
            raise ValueError(
                "The given matrix for %s is not a square one, its shape is %s. Please check your matrix input."
                % (self.__name, self.shape)
            )
        if self.isobject() and min(self.shape) != max(self.shape):
            raise ValueError(
                'The matrix given for "%s" is not a square one, its shape is %s. Please check your object input.'
                % (self.__name, self.shape)
            )
        if self.isscalar() and self.__C <= 0:
            raise ValueError(
                'The "%s" covariance matrix is not positive-definite. Please check your scalar input %s.'
                % (self.__name, self.__C)
            )
        if self.isvector() and (self.__C <= 0).any():
            raise ValueError(
                'The "%s" covariance matrix is not positive-definite. Please check your vector input.'
                % (self.__name,)
            )
        if self.ismatrix() and (
            self.__check or logging.getLogger().level < logging.WARNING
        ):
            try:
                numpy.linalg.cholesky(self.__C)
            except Exception:
                raise ValueError(
                    "The %s covariance matrix is not symmetric positive-definite. Please check your matrix input."
                    % (self.__name,)
                )
        if self.isobject() and (
            self.__check or logging.getLogger().level < logging.WARNING
        ):
            try:
                self.__C.cholesky()
            except Exception:
                raise ValueError(
                    "The %s covariance object is not symmetric positive-definite. Please check your matrix input."
                    % (self.__name,)
                )

    def isscalar(self):
        "Vérification du type interne"
        return self.__is_scalar

    def isvector(self):
        "Vérification du type interne"
        return self.__is_vector

    def ismatrix(self):
        "Vérification du type interne"
        return self.__is_matrix

    def isobject(self):
        "Vérification du type interne"
        return self.__is_object

    def getI(self):
        "Inversion"
        if self.ismatrix():
            return Covariance(
                self.__name + "I", asCovariance=numpy.linalg.inv(self.__C)
            )
        elif self.isvector():
            return Covariance(self.__name + "I", asEyeByVector=1.0 / self.__C)
        elif self.isscalar():
            return Covariance(self.__name + "I", asEyeByScalar=1.0 / self.__C)
        elif self.isobject() and hasattr(self.__C, "getI"):
            return Covariance(self.__name + "I", asCovObject=self.__C.getI())
        else:
            return None  # Indispensable

    def getT(self):
        "Transposition"
        if self.ismatrix():
            return Covariance(self.__name + "T", asCovariance=self.__C.T)
        elif self.isvector():
            return Covariance(self.__name + "T", asEyeByVector=self.__C)
        elif self.isscalar():
            return Covariance(self.__name + "T", asEyeByScalar=self.__C)
        elif self.isobject() and hasattr(self.__C, "getT"):
            return Covariance(self.__name + "T", asCovObject=self.__C.getT())
        else:
            raise AttributeError(
                "the %s covariance matrix has no getT attribute." % (self.__name,)
            )

    def cholesky(self):
        "Décomposition de Cholesky"
        if self.ismatrix():
            return Covariance(
                self.__name + "C", asCovariance=numpy.linalg.cholesky(self.__C)
            )
        elif self.isvector():
            return Covariance(self.__name + "C", asEyeByVector=numpy.sqrt(self.__C))
        elif self.isscalar():
            return Covariance(self.__name + "C", asEyeByScalar=numpy.sqrt(self.__C))
        elif self.isobject() and hasattr(self.__C, "cholesky"):
            return Covariance(self.__name + "C", asCovObject=self.__C.cholesky())
        else:
            raise AttributeError(
                "the %s covariance matrix has no cholesky attribute." % (self.__name,)
            )

    def choleskyI(self):
        "Inversion de la décomposition de Cholesky"
        if self.ismatrix():
            return Covariance(
                self.__name + "H",
                asCovariance=numpy.linalg.inv(numpy.linalg.cholesky(self.__C)),
            )
        elif self.isvector():
            return Covariance(
                self.__name + "H", asEyeByVector=1.0 / numpy.sqrt(self.__C)
            )
        elif self.isscalar():
            return Covariance(
                self.__name + "H", asEyeByScalar=1.0 / numpy.sqrt(self.__C)
            )
        elif self.isobject() and hasattr(self.__C, "choleskyI"):
            return Covariance(self.__name + "H", asCovObject=self.__C.choleskyI())
        else:
            raise AttributeError(
                "the %s covariance matrix has no choleskyI attribute." % (self.__name,)
            )

    def sqrtm(self):
        "Racine carrée matricielle"
        if self.ismatrix():
            import scipy

            return Covariance(
                self.__name + "C", asCovariance=numpy.real(scipy.linalg.sqrtm(self.__C))
            )
        elif self.isvector():
            return Covariance(self.__name + "C", asEyeByVector=numpy.sqrt(self.__C))
        elif self.isscalar():
            return Covariance(self.__name + "C", asEyeByScalar=numpy.sqrt(self.__C))
        elif self.isobject() and hasattr(self.__C, "sqrtm"):
            return Covariance(self.__name + "C", asCovObject=self.__C.sqrtm())
        else:
            raise AttributeError(
                "the %s covariance matrix has no sqrtm attribute." % (self.__name,)
            )

    def sqrtmI(self):
        "Inversion de la racine carrée matricielle"
        if self.ismatrix():
            import scipy

            return Covariance(
                self.__name + "H",
                asCovariance=numpy.linalg.inv(numpy.real(scipy.linalg.sqrtm(self.__C))),
            )
        elif self.isvector():
            return Covariance(
                self.__name + "H", asEyeByVector=1.0 / numpy.sqrt(self.__C)
            )
        elif self.isscalar():
            return Covariance(
                self.__name + "H", asEyeByScalar=1.0 / numpy.sqrt(self.__C)
            )
        elif self.isobject() and hasattr(self.__C, "sqrtmI"):
            return Covariance(self.__name + "H", asCovObject=self.__C.sqrtmI())
        else:
            raise AttributeError(
                "the %s covariance matrix has no sqrtmI attribute." % (self.__name,)
            )

    def diag(self, msize=None):
        "Diagonale de la matrice"
        if self.ismatrix():
            return numpy.diag(self.__C)
        elif self.isvector():
            return self.__C
        elif self.isscalar():
            if msize is None:
                raise ValueError(
                    "the size of the %s covariance matrix has to be given in"
                    % (self.__name,)
                    + " case of definition as a scalar over the diagonal."
                )
            else:
                return self.__C * numpy.ones(int(msize))
        elif self.isobject() and hasattr(self.__C, "diag"):
            return self.__C.diag()
        else:
            raise AttributeError(
                "the %s covariance matrix has no diag attribute." % (self.__name,)
            )

    def trace(self, msize=None):
        "Trace de la matrice"
        if self.ismatrix():
            return numpy.trace(self.__C)
        elif self.isvector():
            return float(numpy.sum(self.__C))
        elif self.isscalar():
            if msize is None:
                raise ValueError(
                    "the size of the %s covariance matrix has to be given in"
                    % (self.__name,)
                    + " case of definition as a scalar over the diagonal."
                )
            else:
                return self.__C * int(msize)
        elif self.isobject():
            return self.__C.trace()
        else:
            raise AttributeError(
                "the %s covariance matrix has no trace attribute." % (self.__name,)
            )

    def asfullmatrix(self, msize=None):
        "Matrice pleine"
        if self.ismatrix():
            return numpy.asarray(self.__C, dtype=float)
        elif self.isvector():
            return numpy.asarray(numpy.diag(self.__C), dtype=float)
        elif self.isscalar():
            if msize is None:
                raise ValueError(
                    "the size of the %s covariance matrix has to be given in"
                    % (self.__name,)
                    + " case of definition as a scalar over the diagonal."
                )
            else:
                return numpy.asarray(self.__C * numpy.eye(int(msize)), dtype=float)
        elif self.isobject() and hasattr(self.__C, "asfullmatrix"):
            return self.__C.asfullmatrix()
        else:
            raise AttributeError(
                "the %s covariance matrix has no asfullmatrix attribute."
                % (self.__name,)
            )

    def assparsematrix(self):
        "Valeur sparse"
        return self.__C

    def getO(self):
        return self

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        if isinstance(self.__C, numpy.float64):
            return repr(float(self.__C))
        else:
            return repr(self.__C)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__C)

    def __add__(self, other):
        "x.__add__(y) <==> x+y"
        if self.ismatrix() or self.isobject():
            return self.__C + numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            if len(_A.shape) == 1:
                _A.reshape((-1, 1))[::2] += self.__C
            else:
                _A.reshape(_A.size)[:: _A.shape[1] + 1] += self.__C
            return numpy.asmatrix(_A)

    def __radd__(self, other):
        "x.__radd__(y) <==> y+x"
        raise NotImplementedError(
            "%s covariance matrix __radd__ method not available for %s type!"
            % (self.__name, type(other))
        )

    def __sub__(self, other):
        "x.__sub__(y) <==> x-y"
        if self.ismatrix() or self.isobject():
            return self.__C - numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            _A.reshape(_A.size)[:: _A.shape[1] + 1] = (
                self.__C - _A.reshape(_A.size)[:: _A.shape[1] + 1]
            )
            return numpy.asmatrix(_A)

    def __rsub__(self, other):
        "x.__rsub__(y) <==> y-x"
        raise NotImplementedError(
            "%s covariance matrix __rsub__ method not available for %s type!"
            % (self.__name, type(other))
        )

    def __neg__(self):
        "x.__neg__() <==> -x"
        return -self.__C

    def __matmul__(self, other):
        "x.__mul__(y) <==> x@y"
        if self.ismatrix() and isinstance(other, (int, float)):
            return numpy.asarray(self.__C) * other
        elif self.ismatrix() and isinstance(
            other, (list, numpy.matrix, numpy.ndarray, tuple)
        ):
            if numpy.ravel(other).size == self.shape[1]:  # Vecteur
                return numpy.ravel(self.__C @ numpy.ravel(other))
            elif numpy.asarray(other).shape[0] == self.shape[1]:  # Matrice
                return numpy.asarray(self.__C) @ numpy.asarray(other)
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (self.shape, numpy.asarray(other).shape, self.__name)
                )
        elif self.isvector() and isinstance(
            other, (list, numpy.matrix, numpy.ndarray, tuple)
        ):
            if numpy.ravel(other).size == self.shape[1]:  # Vecteur
                return numpy.ravel(self.__C) * numpy.ravel(other)
            elif numpy.asarray(other).shape[0] == self.shape[1]:  # Matrice
                return numpy.ravel(self.__C).reshape((-1, 1)) * numpy.asarray(other)
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (self.shape, numpy.ravel(other).shape, self.__name)
                )
        elif self.isscalar() and isinstance(other, numpy.matrix):
            return numpy.asarray(self.__C * other)
        elif self.isscalar() and isinstance(other, (list, numpy.ndarray, tuple)):
            if (
                len(numpy.asarray(other).shape) == 1
                or numpy.asarray(other).shape[1] == 1
                or numpy.asarray(other).shape[0] == 1
            ):
                return self.__C * numpy.ravel(other)
            else:
                return self.__C * numpy.asarray(other)
        elif self.isobject():
            return self.__C.__matmul__(other)
        else:
            raise NotImplementedError(
                "%s covariance matrix __matmul__ method not available for %s type!"
                % (self.__name, type(other))
            )

    def __mul__(self, other):
        "x.__mul__(y) <==> x*y"
        if self.ismatrix() and isinstance(other, (int, numpy.matrix, float)):
            return self.__C * other
        elif self.ismatrix() and isinstance(other, (list, numpy.ndarray, tuple)):
            if numpy.ravel(other).size == self.shape[1]:  # Vecteur
                return self.__C * numpy.asmatrix(numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]:  # Matrice
                return self.__C * numpy.asmatrix(other)
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (self.shape, numpy.asmatrix(other).shape, self.__name)
                )
        elif self.isvector() and isinstance(
            other, (list, numpy.matrix, numpy.ndarray, tuple)
        ):
            if numpy.ravel(other).size == self.shape[1]:  # Vecteur
                return numpy.asmatrix(self.__C * numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]:  # Matrice
                return numpy.asmatrix(
                    (self.__C * (numpy.asarray(other).transpose())).transpose()
                )
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (self.shape, numpy.ravel(other).shape, self.__name)
                )
        elif self.isscalar() and isinstance(other, numpy.matrix):
            return self.__C * other
        elif self.isscalar() and isinstance(other, (list, numpy.ndarray, tuple)):
            if (
                len(numpy.asarray(other).shape) == 1
                or numpy.asarray(other).shape[1] == 1
                or numpy.asarray(other).shape[0] == 1
            ):
                return self.__C * numpy.asmatrix(numpy.ravel(other)).T
            else:
                return self.__C * numpy.asmatrix(other)
        elif self.isobject():
            return self.__C.__mul__(other)
        else:
            raise NotImplementedError(
                "%s covariance matrix __mul__ method not available for %s type!"
                % (self.__name, type(other))
            )

    def __rmatmul__(self, other):
        "x.__rmul__(y) <==> y@x"
        if self.ismatrix() and isinstance(other, (int, numpy.matrix, float)):
            return other * self.__C
        elif self.ismatrix() and isinstance(other, (list, numpy.ndarray, tuple)):
            if numpy.ravel(other).size == self.shape[1]:  # Vecteur
                return numpy.asmatrix(numpy.ravel(other)) * self.__C
            elif numpy.asmatrix(other).shape[0] == self.shape[1]:  # Matrice
                return numpy.asmatrix(other) * self.__C
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (numpy.asmatrix(other).shape, self.shape, self.__name)
                )
        elif self.isvector() and isinstance(other, numpy.matrix):
            if numpy.ravel(other).size == self.shape[0]:  # Vecteur
                return numpy.asmatrix(numpy.ravel(other) * self.__C)
            elif numpy.asmatrix(other).shape[1] == self.shape[0]:  # Matrice
                return numpy.asmatrix(numpy.array(other) * self.__C)
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (numpy.ravel(other).shape, self.shape, self.__name)
                )
        elif self.isscalar() and isinstance(other, numpy.matrix):
            return other * self.__C
        elif self.isobject():
            return self.__C.__rmatmul__(other)
        else:
            raise NotImplementedError(
                "%s covariance matrix __rmatmul__ method not available for %s type!"
                % (self.__name, type(other))
            )

    def __rmul__(self, other):
        "x.__rmul__(y) <==> y*x"
        if self.ismatrix() and isinstance(other, (int, numpy.matrix, float)):
            return other * self.__C
        elif self.ismatrix() and isinstance(other, (list, numpy.ndarray, tuple)):
            if numpy.ravel(other).size == self.shape[1]:  # Vecteur
                return numpy.asmatrix(numpy.ravel(other)) * self.__C
            elif numpy.asmatrix(other).shape[0] == self.shape[1]:  # Matrice
                return numpy.asmatrix(other) * self.__C
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (numpy.asmatrix(other).shape, self.shape, self.__name)
                )
        elif self.isvector() and isinstance(other, numpy.matrix):
            if numpy.ravel(other).size == self.shape[0]:  # Vecteur
                return numpy.asmatrix(numpy.ravel(other) * self.__C)
            elif numpy.asmatrix(other).shape[1] == self.shape[0]:  # Matrice
                return numpy.asmatrix(numpy.array(other) * self.__C)
            else:
                raise ValueError(
                    "operands could not be broadcast together with shapes %s %s in %s matrix"
                    % (numpy.ravel(other).shape, self.shape, self.__name)
                )
        elif self.isscalar() and isinstance(other, numpy.matrix):
            return other * self.__C
        elif self.isscalar() and isinstance(other, float):
            return other * self.__C
        elif self.isobject():
            return self.__C.__rmul__(other)
        else:
            raise NotImplementedError(
                "%s covariance matrix __rmul__ method not available for %s type!"
                % (self.__name, type(other))
            )

    def __len__(self):
        "x.__len__() <==> len(x)"
        return self.shape[0]


# ==============================================================================
class DynamicalSimulator(object):
    """
    Classe de simulateur ODE d'ordre 1 pour modèles dynamiques :

        dy/dt = F_µ(t, y)

    avec y = f(t) et µ les paramètres intrinsèques. t est couramment le temps,
    mais il peut être une variable quelconque non temporelle.

    Paramètres d'initialisation :
    - mu         : paramètres intrinsèques du modèle
    - integrator : intégrateur choisi pour intégrer l'ODE
    - dt         : pas de temps d'intégration
    - t0         : temps initial d'intégration
    - tf         : temps final
    - y0         : condition initiale
    """

    __integrator_list = ["euler", "rk1", "rk2", "rk3", "rk4", "odeint", "solve_ivp"]
    __slots__ = (
        "_autonomous",
        "_mu",
        "_integrator",
        "_dt",
        "_do",
        "_t0",
        "_tf",
        "_y0",
    )

    def __init__(
        self,
        mu=None,
        integrator=None,
        dt=None,
        t0=None,
        tf=None,
        y0=None,
        autonomous=None,
    ):
        "None default values are mandatory to allow overriding"
        if hasattr(self, "CanonicalDescription"):
            self.CanonicalDescription()
        self._description(mu, integrator, dt, t0, tf, y0, autonomous)

    # --------------------------------------------------------------------------
    # User defined ODE model and canonical description

    def ODEModel(self, t, y):
        """
        ODE : return dy / dt = F_µ(t, y)
        """
        raise NotImplementedError()

    def CanonicalDescription(self):
        """
        User settings for default or recommended EDO description

        Setters/Getters that >>> can <<< be used:
            - self.Parameters
            - self.Integrator
            - self.IntegrationStep
            - self.ObservationStep
            - self.InitialTime
            - self.FinalTime
            - self.InitialCondition
            - self.Autonomous
        """
        pass

    # Optional implementation, used only if present and callable
    # def ODETLMModel(self, t, y):
        # """
        # Return the tangent linear matrix
        # """
        # nt = self.InitialCondition.size
        # tlm = numpy.zeros((nt, nt))
        # ...
        # return tlm

    # --------------------------------------------------------------------------

    @property
    def Parameters(self):
        return self._mu

    @Parameters.setter
    def Parameters(self, value):
        if value is None:
            pass
        else:
            self._mu = numpy.ravel(value)

    # -------
    @property
    def Integrator(self):
        return self._integrator

    @Integrator.setter
    def Integrator(self, value):
        if value is None:
            pass
        elif not (value in self.__integrator_list):
            raise ValueError(
                "wrong value %s set for the integrator scheme. \nAvailable integrator scheme are: %s"
                % (value, self.__integrator_list)
            )
        else:
            self._integrator = str(value)

    # -------
    @property
    def IntegrationStep(self):
        return self._dt

    @IntegrationStep.setter
    def IntegrationStep(self, value):
        if value is None:
            pass
        elif float(value) > 0:
            self._dt = max(2.0e-16, float(value))
        else:
            raise ValueError("integration step has to be strictly positive")

    # -------
    @property
    def ObservationStep(self):
        return self._do

    @ObservationStep.setter
    def ObservationStep(self, value):
        if value is None:
            pass
        elif float(value) > 0:
            self._do = max(2.0e-16, float(value))
            if hasattr(self, "_dt") and self._do < self._dt:
                raise ValueError(
                    "Observation step is inconsistent with integration one"
                )
        else:
            raise ValueError("observation step has to be strictly positive")

    # -------
    @property
    def InitialTime(self):
        return self._t0

    @InitialTime.setter
    def InitialTime(self, value):
        if value is None:
            pass
        else:
            self._t0 = float(value)
            if hasattr(self, "_tf") and self._t0 > self._tf:
                raise ValueError("initial time has to remain less than final time")

    # -------
    @property
    def FinalTime(self):
        return self._tf

    @FinalTime.setter
    def FinalTime(self, value):
        if value is None:
            pass
        else:
            self._tf = float(value)
            if hasattr(self, "_t0") and self._t0 > self._tf:
                raise ValueError("initial time has to remain less than final time")

    # -------
    @property
    def InitialCondition(self):
        return self._y0

    @InitialCondition.setter
    def InitialCondition(self, value):
        if value is None:
            pass
        else:
            self._y0 = numpy.ravel(value)

    # -------
    @property
    def Autonomous(self):
        return self._autonomous

    @Autonomous.setter
    def Autonomous(self, value):
        "Declare the system to be autonomous"
        if value is None:
            pass
        else:
            self._autonomous = bool(value)

    # --------------------------------------------------------------------------

    def ODETangentModel(self, t, pair):
        """
        ODE : return the tangent evaluation
        """
        y, dy = pair
        if not (hasattr(self, "ODETLMModel") and callable(self.ODETLMModel)):
            raise NotImplementedError("No TLM available, please implement one")
        #
        if dy is None or len(dy) == 0:
            return self.ODETLMModel(t, y)
        else:
            dy = numpy.ravel(dy)
            return self.ODETLMModel(t, y) @ dy

    def ODEAdjointModel(self, t, pair):
        """
        ODE : return the adjoint evaluation
        """
        y_in, y_out = pair
        if not (hasattr(self, "ODETLMModel") and callable(self.ODETLMModel)):
            raise NotImplementedError("No TLM available, please implement one")
        #
        if y_out is None or len(y_out) == 0:
            return numpy.transpose(self.ODETLMModel(t, y_in))
        else:
            y_out = numpy.ravel(y_out)
            return numpy.transpose(self.ODETLMModel(t, y_in)) @ y_out

    # --------------------------------------------------------------------------

    def _description(
        self,
        mu=None,
        integrator=None,
        dt=None,
        t0=None,
        tf=None,
        y0=None,
        autonomous=False,
    ):
        "Explicit setting of EDO description at init time"
        self.Parameters = mu
        self.Integrator = integrator
        self.IntegrationStep = dt
        self.InitialTime = t0
        self.FinalTime = tf
        self.InitialCondition = y0
        self.Autonomous = autonomous

    # --------------------------------------------------------------------------

    def _rk1_step(self, t, y, h, F):
        "Euler integration schema"
        y = y + h * F(t, y)
        t = t + h
        return [t, y]

    def _rk2_step(self, t, y, h, F):
        "Runge-Kutta integration schema of order 2 (RK2)"
        k1 = h * F(t, y)
        k2 = h * F(t + h / 2.0, y + k1 / 2.0)
        #
        y = y + k2
        t = t + h
        return [t, y]

    def _rk3_step(self, t, y, h, F):
        "Runge-Kutta integration schema of order 3 (RK3)"
        k1 = h * F(t, y)
        k2 = h * F(t + h / 2.0, y + k1 / 2.0)
        k3 = h * F(t + h, y - k1 + 2.0 * k2)
        #
        y = y + (k1 + 4.0 * k2 + k3) / 6.0
        t = t + h
        return [t, y]

    def _rk4_step(self, t, y, h, F):
        "Runge-Kutta integration schema of order 4 (RK4)"
        k1 = h * F(t, y)
        k2 = h * F(t + h / 2.0, y + k1 / 2.0)
        k3 = h * F(t + h / 2.0, y + k2 / 2.0)
        k4 = h * F(t + h, y + k3)
        #
        y = y + (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        t = t + h
        return [t, y]

    _euler_step = _rk1_step

    def Integration(self, y1=None, t1=None, t2=None, mu=None):
        """
        Exécute l'intégration du modèle entre t1 et t2, en partant de y1, via
        le schéma d'intégration choisi.
        """
        if y1 is None:
            _ly0 = self._y0
        else:
            _ly0 = numpy.ravel(y1)
        if t1 is None:
            _lt0 = self._t0
        else:
            _lt0 = float(t1)
        if t2 is None:
            _ltf = self._tf
        else:
            _ltf = float(t2)
        self.Parameters = mu
        if (
            (self._mu is None)
            or (self._integrator is None)
            or (self._dt is None)
            or (_lt0 is None)
            or (_ltf is None)
            or (_ly0 is None)
        ):
            raise ValueError(
                "Some integration input information are None and not defined\n(%s, %s, %s, %s, %s, %s)"
                % (
                    self._mu,
                    self._integrator,
                    self._dt,
                    _lt0,
                    _ltf,
                    _ly0,
                )
            )
        #
        times = numpy.arange(_lt0, _ltf + self._dt / 2, self._dt)
        if self._integrator == "odeint":
            # intégration 'automatique' dans le cas d'un système pouvant être
            # problématique avec rk4 ou euler (comme Van Der Pol)
            from scipy.integrate import odeint

            if hasattr(self, "ODETLMModel") and callable(self.ODETLMModel):
                trajectory = odeint(
                    self.ODEModel,
                    numpy.array(_ly0, dtype=float),
                    times,
                    Dfun=self.ODETLMModel,
                    tfirst=True,
                )
            else:
                trajectory = odeint(
                    self.ODEModel,
                    numpy.array(_ly0, dtype=float),
                    times,
                    tfirst=True,
                )
        elif self._integrator == "solve_ivp":
            # intégration 'automatique' dans le cas d'un système pouvant être
            # problématique avec rk4 ou euler (comme Van Der Pol)
            from scipy.integrate import solve_ivp

            sol = solve_ivp(
                self.ODEModel,
                (_lt0, _ltf),
                numpy.array(_ly0, dtype=float),
                t_eval=times,
            )
            trajectory = sol.y.T
        else:
            if hasattr(self, "_%s_step" % self._integrator):
                integration_step = getattr(self, "_%s_step" % self._integrator)
            else:
                raise ValueError(
                    "Error in setting the integrator method (no _%s_step method)"
                    % self._integrator
                )
            #
            t = _lt0
            y = _ly0
            trajectory = numpy.array([_ly0])
            #
            while t < _ltf - self._dt / 2:
                [t, y] = integration_step(t, y, self._dt, self.ODEModel)
                trajectory = numpy.concatenate((trajectory, numpy.array([y])), axis=0)
        #
        return [times, trajectory]

    def ForecastedPath(self, y1=None, t1=None, t2=None, mu=None):
        "Trajectoire de t1 à t2, en partant de y1, pour un paramètre donné mu"
        #
        _, trajectory_from_t1_to_t2 = self.Integration(y1, t1, t2, mu)
        #
        return trajectory_from_t1_to_t2

    def ForecastedState(self, y1=None, t1=None, t2=None, mu=None):
        "État à t2 en intégrant à partir de t1, y1, pour un paramètre donné mu"
        #
        _, trajectory_from_t1_to_t2 = self.Integration(y1, t1, t2, mu)
        #
        return trajectory_from_t1_to_t2[-1, :]

    def StateTransition(self, y1=None):
        "État y[n+1] intégré depuis y[n] sur un pas self.ObservationStep"
        if self.Autonomous:
            if not hasattr(self, "_do") or self._do is None:
                raise ValueError(
                    "    StateTransition requires an observation step size to be given"
                )
            return self.ForecastedState(y1, 0.0, self.ObservationStep, self.Parameters)
        else:
            raise NotImplementedError(
                "    StateTransition has to be provided by the user in case of non-autonomous ODE"
            )

    def HistoryBoard(
        self,
        t_s,
        y_s,
        i_s=None,
        filename="figure_of_trajectory.pdf",
        suptitle="",
        title="",
        xlabel="Time",
        ylabel="State variables",
        cmap="gist_gray_r",
        grid=False,
    ):
        """
        t_s : série des instants t
        y_s : série des valeurs 1D des variables du système dynamique, pour
              chaque pas de temps, sous forme d'un tableau 2D de type:
              SDyn(i,t) = SDyn[i][t] = [SDyn[i] pour chaque t]
        i_s : série des indices i des variables
        """
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MaxNLocator

        #
        if i_s is None:
            i_s = range(y_s.shape[0])
        levels = MaxNLocator(nbins=25).tick_values(
            numpy.ravel(y_s).min(), numpy.ravel(y_s).max()
        )
        fig, ax = plt.subplots(figsize=(15, 5))
        fig.subplots_adjust(bottom=0.1, left=0.05, right=0.95, top=0.9)
        im = plt.contourf(t_s, i_s, y_s, levels=levels, cmap=plt.get_cmap(cmap))
        fig.colorbar(im, ax=ax)
        if len(suptitle) > 0:
            plt.suptitle(suptitle)
        if len(title) > 0:
            plt.title(title)
        else:
            plt.title("Model trajectory with %i variables" % len(y_s[:, 0]))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if grid:
            ax.grid()
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)


# ==============================================================================
class Observer2Func(object):
    """
    Création d'une fonction d'observateur a partir de son texte
    """

    __slots__ = ("__corps",)

    def __init__(self, corps=""):
        self.__corps = corps

    def func(self, var, info):
        "Fonction d'observation"
        exec(self.__corps)

    def getfunc(self):
        "Restitution du pointeur de fonction dans l'objet"
        return self.func


# ==============================================================================
class CaseLogger(object):
    """
    Conservation des commandes de création d'un cas
    """

    __slots__ = (
        "__name",
        "__objname",
        "__logSerie",
        "__switchoff",
        "__viewers",
        "__loaders",
    )

    def __init__(
        self, __name="", __objname="case", __addViewers=None, __addLoaders=None
    ):
        self.__name = str(__name)
        self.__objname = str(__objname)
        self.__logSerie = []
        self.__switchoff = False
        self.__viewers = {
            "TUI": Interfaces._TUIViewer,
            "SCD": Interfaces._SCDViewer,
            "YACS": Interfaces._YACSViewer,
            "SimpleReportInRst": Interfaces._SimpleReportInRstViewer,
            "SimpleReportInHtml": Interfaces._SimpleReportInHtmlViewer,
            "SimpleReportInPlainTxt": Interfaces._SimpleReportInPlainTxtViewer,
        }
        self.__loaders = {
            "TUI": Interfaces._TUIViewer,
            "COM": Interfaces._COMViewer,
        }
        if __addViewers is not None:
            self.__viewers.update(dict(__addViewers))
        if __addLoaders is not None:
            self.__loaders.update(dict(__addLoaders))

    def register(
        self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False
    ):
        "Enregistrement d'une commande individuelle"
        if (
            __command is not None
            and __keys is not None
            and __local is not None
            and not self.__switchoff
        ):
            if "self" in __keys:
                __keys.remove("self")
            self.__logSerie.append(
                (str(__command), __keys, __local, __pre, __switchoff)
            )
            if __switchoff:
                self.__switchoff = True
        if not __switchoff:
            self.__switchoff = False

    def dump(self, __filename=None, __format="TUI", __upa=""):
        "Restitution normalisée des commandes"
        if __format in self.__viewers:
            __formater = self.__viewers[__format](
                self.__name, self.__objname, self.__logSerie
            )
        else:
            raise ValueError('Dumping as "%s" is not available' % __format)
        return __formater.dump(__filename, __upa)

    def load(self, __filename=None, __content=None, __object=None, __format="TUI"):
        "Chargement normalisé des commandes"
        if __format in self.__loaders:
            __formater = self.__loaders[__format]()
        else:
            raise ValueError('Loading as "%s" is not available' % __format)
        return __formater.load(__filename, __content, __object)


# ==============================================================================
def MultiFonction(
    __xserie,
    _extraArguments=None,
    _sFunction=lambda x: x,
    _mpEnabled=False,
    _mpWorkers=None,
):
    """
    Pour une liste ordonnée de vecteurs en entrée, renvoie en sortie la liste
    correspondante de valeurs de la fonction en argument
    """
    # Vérifications et définitions initiales
    # logging.debug("MULTF Internal multifonction calculations begin with function %s"%(_sFunction.__name__,))
    if not PlatformInfo.isIterable(__xserie):
        raise TypeError(
            "MultiFonction not iterable unkown input type: %s" % (type(__xserie),)
        )
    if _mpEnabled:
        if (_mpWorkers is None) or (_mpWorkers is not None and _mpWorkers < 1):
            __mpWorkers = None
        else:
            __mpWorkers = int(_mpWorkers)
        try:
            import multiprocessing

            __mpEnabled = True
        except ImportError:
            __mpEnabled = False
    else:
        __mpEnabled = False
        __mpWorkers = None
    #
    # Calculs effectifs
    if __mpEnabled:
        _jobs = __xserie
        # logging.debug("MULTF Internal multiprocessing calculations begin : evaluation of %i point(s)"%(len(_jobs),))
        with multiprocessing.Pool(__mpWorkers) as pool:
            __multiHX = pool.map(_sFunction, _jobs)
            pool.close()
            pool.join()
        # logging.debug("MULTF Internal multiprocessing calculation end")
    else:
        # logging.debug("MULTF Internal monoprocessing calculation begin")
        __multiHX = []
        if _extraArguments is None:
            for __xvalue in __xserie:
                __multiHX.append(_sFunction(__xvalue))
        elif _extraArguments is not None and isinstance(
            _extraArguments, (list, tuple, map)
        ):
            for __xvalue in __xserie:
                __multiHX.append(_sFunction(__xvalue, *_extraArguments))
        elif _extraArguments is not None and isinstance(_extraArguments, dict):
            for __xvalue in __xserie:
                __multiHX.append(_sFunction(__xvalue, **_extraArguments))
        else:
            raise TypeError(
                "MultiFonction extra arguments unkown input type: %s"
                % (type(_extraArguments),)
            )
        # logging.debug("MULTF Internal monoprocessing calculation end")
    #
    # logging.debug("MULTF Internal multifonction calculations end")
    return __multiHX


# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
