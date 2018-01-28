# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2018 EDF R&D
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

    Ce module est destiné à être appelée par AssimilationStudy.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os
import sys
import logging
import copy
import numpy
from daCore import Persistence
from daCore import PlatformInfo
from daCore import Templates

# ==============================================================================
class CacheManager(object):
    """
    Classe générale de gestion d'un cache de calculs
    """
    def __init__(self,
                 toleranceInRedundancy = 1.e-18,
                 lenghtOfRedundancy    = -1,
                ):
        """
        Les caractéristiques de tolérance peuvent être modifées à la création.
        """
        self.__tolerBP  = float(toleranceInRedundancy)
        self.__lenghtOR = int(lenghtOfRedundancy)
        self.__initlnOR = self.__lenghtOR
        self.clearCache()

    def clearCache(self):
        "Vide le cache"
        self.__listOPCV = [] # Operator Previous Calculated Points, Results, Point Norms
        # logging.debug("CM Tolerance de determination des doublons : %.2e", self.__tolerBP)

    def wasCalculatedIn(self, xValue ): #, info="" ):
        "Vérifie l'existence d'un calcul correspondant à la valeur"
        __alc = False
        __HxV = None
        for i in range(min(len(self.__listOPCV),self.__lenghtOR)-1,-1,-1):
            if xValue.size != self.__listOPCV[i][0].size:
                # logging.debug("CM Différence de la taille %s de X et de celle %s du point %i déjà calculé", xValue.shape,i,self.__listOPCP[i].shape)
                continue
            if numpy.linalg.norm(numpy.ravel(xValue) - self.__listOPCV[i][0]) < self.__tolerBP * self.__listOPCV[i][2]:
                __alc  = True
                __HxV = self.__listOPCV[i][1]
                # logging.debug("CM Cas%s déja calculé, portant le numéro %i", info, i)
                break
        return __alc, __HxV

    def storeValueInX(self, xValue, HxValue ):
        "Stocke un calcul correspondant à la valeur"
        if self.__lenghtOR < 0:
            self.__lenghtOR = 2 * xValue.size + 2
            self.__initlnOR = self.__lenghtOR
        while len(self.__listOPCV) > self.__lenghtOR:
            # logging.debug("CM Réduction de la liste des cas à %i éléments par suppression du premier", self.__lenghtOR)
            self.__listOPCV.pop(0)
        self.__listOPCV.append( (
            copy.copy(numpy.ravel(xValue)),
            copy.copy(HxValue),
            numpy.linalg.norm(xValue),
            ) )

    def disable(self):
        "Inactive le cache"
        self.__initlnOR = self.__lenghtOR
        self.__lenghtOR = 0

    def enable(self):
        "Active le cache"
        self.__lenghtOR = self.__initlnOR

# ==============================================================================
class Operator(object):
    """
    Classe générale d'interface de type opérateur simple
    """
    NbCallsAsMatrix = 0
    NbCallsAsMethod = 0
    NbCallsOfCached = 0
    CM = CacheManager()
    #
    def __init__(self, fromMethod=None, fromMatrix=None, avoidingRedundancy = True):
        """
        On construit un objet de ce type en fournissant à l'aide de l'un des
        deux mots-clé, soit une fonction python, soit une matrice.
        Arguments :
        - fromMethod : argument de type fonction Python
        - fromMatrix : argument adapté au constructeur numpy.matrix
        - avoidingRedundancy : évite ou pas les calculs redondants
        """
        self.__NbCallsAsMatrix, self.__NbCallsAsMethod, self.__NbCallsOfCached = 0, 0, 0
        self.__AvoidRC = bool( avoidingRedundancy )
        if   fromMethod is not None:
            self.__Method = fromMethod # logtimer(fromMethod)
            self.__Matrix = None
            self.__Type   = "Method"
        elif fromMatrix is not None:
            self.__Method = None
            self.__Matrix = numpy.matrix( fromMatrix, numpy.float )
            self.__Type   = "Matrix"
        else:
            self.__Method = None
            self.__Matrix = None
            self.__Type   = None

    def disableAvoidingRedundancy(self):
        "Inactive le cache"
        Operator.CM.disable()

    def enableAvoidingRedundancy(self):
        "Active le cache"
        if self.__AvoidRC:
            Operator.CM.enable()
        else:
            Operator.CM.disable()

    def isType(self):
        "Renvoie le type"
        return self.__Type

    def appliedTo(self, xValue, HValue = None):
        """
        Permet de restituer le résultat de l'application de l'opérateur à un
        argument xValue. Cette méthode se contente d'appliquer, son argument
        devant a priori être du bon type.
        Arguments :
        - xValue : argument adapté pour appliquer l'opérateur
        """
        if HValue is not None:
            HxValue = numpy.asmatrix( numpy.ravel( HValue ) ).T
            if self.__AvoidRC:
                Operator.CM.storeValueInX(xValue,HxValue)
        else:
            if self.__AvoidRC:
                __alreadyCalculated, __HxV = Operator.CM.wasCalculatedIn(xValue)
            else:
                __alreadyCalculated = False
            #
            if __alreadyCalculated:
                self.__addOneCacheCall()
                HxValue = __HxV
            else:
                if self.__Matrix is not None:
                    self.__addOneMatrixCall()
                    HxValue = self.__Matrix * xValue
                else:
                    self.__addOneMethodCall()
                    HxValue = self.__Method( xValue )
                if self.__AvoidRC:
                    Operator.CM.storeValueInX(xValue,HxValue)
        #
        return HxValue

    def appliedControledFormTo(self, paire ):
        """
        Permet de restituer le résultat de l'application de l'opérateur à une
        paire (xValue, uValue). Cette méthode se contente d'appliquer, son
        argument devant a priori être du bon type. Si la uValue est None,
        on suppose que l'opérateur ne s'applique qu'à xValue.
        Arguments :
        - xValue : argument X adapté pour appliquer l'opérateur
        - uValue : argument U adapté pour appliquer l'opérateur
        """
        assert len(paire) == 2, "Incorrect number of arguments"
        xValue, uValue = paire
        if self.__Matrix is not None:
            self.__addOneMatrixCall()
            return self.__Matrix * xValue
        elif uValue is not None:
            self.__addOneMethodCall()
            return self.__Method( (xValue, uValue) )
        else:
            self.__addOneMethodCall()
            return self.__Method( xValue )

    def appliedInXTo(self, paire ):
        """
        Permet de restituer le résultat de l'application de l'opérateur à un
        argument xValue, sachant que l'opérateur est valable en xNominal.
        Cette méthode se contente d'appliquer, son argument devant a priori
        être du bon type. Si l'opérateur est linéaire car c'est une matrice,
        alors il est valable en tout point nominal et il n'est pas nécessaire
        d'utiliser xNominal.
        Arguments : une liste contenant
        - xNominal : argument permettant de donner le point où l'opérateur
          est construit pour etre ensuite appliqué
        - xValue : argument adapté pour appliquer l'opérateur
        """
        assert len(paire) == 2, "Incorrect number of arguments"
        xNominal, xValue = paire
        if self.__Matrix is not None:
            self.__addOneMatrixCall()
            return self.__Matrix * xValue
        else:
            self.__addOneMethodCall()
            return self.__Method( (xNominal, xValue) )

    def asMatrix(self, ValueForMethodForm = "UnknownVoidValue"):
        """
        Permet de renvoyer l'opérateur sous la forme d'une matrice
        """
        if self.__Matrix is not None:
            self.__addOneMatrixCall()
            return self.__Matrix
        elif ValueForMethodForm is not "UnknownVoidValue": # Ne pas utiliser "None"
            self.__addOneMethodCall()
            return numpy.matrix( self.__Method( (ValueForMethodForm, None) ) )
        else:
            raise ValueError("Matrix form of the operator defined as a function/method requires to give an operating point.")

    def shape(self):
        """
        Renvoie la taille sous forme numpy si l'opérateur est disponible sous
        la forme d'une matrice
        """
        if self.__Matrix is not None:
            return self.__Matrix.shape
        else:
            raise ValueError("Matrix form of the operator is not available, nor the shape")

    def nbcalls(self, which=None):
        """
        Renvoie les nombres d'évaluations de l'opérateur
        """
        __nbcalls = (
            self.__NbCallsAsMatrix+self.__NbCallsAsMethod,
            self.__NbCallsAsMatrix,
            self.__NbCallsAsMethod,
            self.__NbCallsOfCached,
            Operator.NbCallsAsMatrix+Operator.NbCallsAsMethod,
            Operator.NbCallsAsMatrix,
            Operator.NbCallsAsMethod,
            Operator.NbCallsOfCached,
            )
        if which is None: return __nbcalls
        else:             return __nbcalls[which]

    def __addOneMatrixCall(self):
        "Comptabilise un appel"
        self.__NbCallsAsMatrix   += 1 # Decompte local
        Operator.NbCallsAsMatrix += 1 # Decompte global

    def __addOneMethodCall(self):
        "Comptabilise un appel"
        self.__NbCallsAsMethod   += 1 # Decompte local
        Operator.NbCallsAsMethod += 1 # Decompte global

    def __addOneCacheCall(self):
        "Comptabilise un appel"
        self.__NbCallsOfCached   += 1 # Decompte local
        Operator.NbCallsOfCached += 1 # Decompte global

# ==============================================================================
class FullOperator(object):
    """
    Classe générale d'interface de type opérateur complet
    (Direct, Linéaire Tangent, Adjoint)
    """
    def __init__(self,
                 name             = "GenericFullOperator",
                 asMatrix         = None,
                 asOneFunction    = None, # Fonction
                 asThreeFunctions = None, # Dictionnaire de fonctions
                 asScript         = None,
                 asDict           = None, # Parameters
                 appliedInX       = None,
                 avoidRC          = True,
                 scheduledBy      = None,
                 toBeChecked      = False,
                 ):
        ""
        self.__name       = str(name)
        self.__check      = bool(toBeChecked)
        #
        self.__FO          = {}
        #
        __Parameters = {}
        if (asDict is not None) and isinstance(asDict, dict):
            __Parameters.update( asDict )
            if "DifferentialIncrement" in asDict:
                __Parameters["withIncrement"]  = asDict["DifferentialIncrement"]
            if "CenteredFiniteDifference" in asDict:
                __Parameters["withCenteredDF"] = asDict["CenteredFiniteDifference"]
            if "EnableMultiProcessing" in asDict:
                __Parameters["withmpEnabled"]  = asDict["EnableMultiProcessing"]
            if "NumberOfProcesses" in asDict:
                __Parameters["withmpWorkers"]  = asDict["NumberOfProcesses"]
        #
        if asScript is not None:
            __Matrix, __Function = None, None
            if asMatrix:
                __Matrix = ImportFromScript(asScript).getvalue( self.__name )
            elif asOneFunction:
                __Function = { "Direct":ImportFromScript(asScript).getvalue( "DirectOperator" ) }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif asThreeFunctions:
                __Function = {
                    "Direct" :ImportFromScript(asScript).getvalue( "DirectOperator" ),
                    "Tangent":ImportFromScript(asScript).getvalue( "TangentOperator" ),
                    "Adjoint":ImportFromScript(asScript).getvalue( "AdjointOperator" ),
                    }
                __Function.update(__Parameters)
        else:
            __Matrix = asMatrix
            if asOneFunction is not None:
                if isinstance(asOneFunction, dict) and "Direct" in asOneFunction:
                    if asOneFunction["Direct"] is not None:
                        __Function = asOneFunction
                    else:
                        raise ValueError("The function has to be given in a dictionnary which have 1 key (\"Direct\")")
                else:
                    __Function = { "Direct":asOneFunction }
                __Function.update({"useApproximatedDerivatives":True})
                __Function.update(__Parameters)
            elif asThreeFunctions is not None:
                if isinstance(asThreeFunctions, dict) and \
                   ("Tangent" in asThreeFunctions) and (asThreeFunctions["Tangent"] is not None) and \
                   ("Adjoint" in asThreeFunctions) and (asThreeFunctions["Adjoint"] is not None) and \
                   (("useApproximatedDerivatives" not in asThreeFunctions) or not bool(asThreeFunctions["useApproximatedDerivatives"])):
                    __Function = asThreeFunctions
                elif isinstance(asThreeFunctions, dict) and \
                   ("Direct" in asThreeFunctions) and (asThreeFunctions["Direct"] is not None):
                    __Function = asThreeFunctions
                    __Function.update({"useApproximatedDerivatives":True})
                else:
                    raise ValueError("The functions has to be given in a dictionnary which have either 1 key (\"Direct\") or 3 keys (\"Direct\" (optionnal), \"Tangent\" and \"Adjoint\")")
                if "Direct"  not in asThreeFunctions:
                    __Function["Direct"] = asThreeFunctions["Tangent"]
                __Function.update(__Parameters)
            else:
                __Function = None
        #
        # if sys.version_info[0] < 3 and isinstance(__Function, dict):
        #     for k in ("Direct", "Tangent", "Adjoint"):
        #         if k in __Function and hasattr(__Function[k],"__class__"):
        #             if type(__Function[k]) is type(self.__init__):
        #                 raise TypeError("can't use a class method (%s) as a function for the \"%s\" operator. Use a real function instead."%(type(__Function[k]),k))
        #
        if   appliedInX is not None and isinstance(appliedInX, dict):
            __appliedInX = appliedInX
        elif appliedInX is not None:
            __appliedInX = {"HXb":appliedInX}
        else:
            __appliedInX = None
        #
        if scheduledBy is not None:
            self.__T = scheduledBy
        #
        if isinstance(__Function, dict) and \
                ("useApproximatedDerivatives" in __Function) and bool(__Function["useApproximatedDerivatives"]) and \
                ("Direct" in __Function) and (__Function["Direct"] is not None):
            if "withCenteredDF"            not in __Function: __Function["withCenteredDF"]            = False
            if "withIncrement"             not in __Function: __Function["withIncrement"]             = 0.01
            if "withdX"                    not in __Function: __Function["withdX"]                    = None
            if "withAvoidingRedundancy"    not in __Function: __Function["withAvoidingRedundancy"]    = True
            if "withToleranceInRedundancy" not in __Function: __Function["withToleranceInRedundancy"] = 1.e-18
            if "withLenghtOfRedundancy"    not in __Function: __Function["withLenghtOfRedundancy"]    = -1
            if "withmpEnabled"             not in __Function: __Function["withmpEnabled"]             = False
            if "withmpWorkers"             not in __Function: __Function["withmpWorkers"]             = None
            from daNumerics.ApproximatedDerivatives import FDApproximation
            FDA = FDApproximation(
                Function              = __Function["Direct"],
                centeredDF            = __Function["withCenteredDF"],
                increment             = __Function["withIncrement"],
                dX                    = __Function["withdX"],
                avoidingRedundancy    = __Function["withAvoidingRedundancy"],
                toleranceInRedundancy = __Function["withToleranceInRedundancy"],
                lenghtOfRedundancy    = __Function["withLenghtOfRedundancy"],
                mpEnabled             = __Function["withmpEnabled"],
                mpWorkers             = __Function["withmpWorkers"],
                )
            self.__FO["Direct"]  = Operator( fromMethod = FDA.DirectOperator,  avoidingRedundancy = avoidRC )
            self.__FO["Tangent"] = Operator( fromMethod = FDA.TangentOperator, avoidingRedundancy = avoidRC )
            self.__FO["Adjoint"] = Operator( fromMethod = FDA.AdjointOperator, avoidingRedundancy = avoidRC )
        elif isinstance(__Function, dict) and \
                ("Direct" in __Function) and ("Tangent" in __Function) and ("Adjoint" in __Function) and \
                (__Function["Direct"] is not None) and (__Function["Tangent"] is not None) and (__Function["Adjoint"] is not None):
            self.__FO["Direct"]  = Operator( fromMethod = __Function["Direct"],  avoidingRedundancy = avoidRC )
            self.__FO["Tangent"] = Operator( fromMethod = __Function["Tangent"], avoidingRedundancy = avoidRC )
            self.__FO["Adjoint"] = Operator( fromMethod = __Function["Adjoint"], avoidingRedundancy = avoidRC )
        elif asMatrix is not None:
            __matrice = numpy.matrix( __Matrix, numpy.float )
            self.__FO["Direct"]  = Operator( fromMatrix = __matrice,   avoidingRedundancy = avoidRC )
            self.__FO["Tangent"] = Operator( fromMatrix = __matrice,   avoidingRedundancy = avoidRC )
            self.__FO["Adjoint"] = Operator( fromMatrix = __matrice.T, avoidingRedundancy = avoidRC )
            del __matrice
        else:
            raise ValueError("Improperly defined observation operator, it requires at minima either a matrix, a Direct for approximate derivatives or a Tangent/Adjoint pair.")
        #
        if __appliedInX is not None:
            self.__FO["AppliedInX"] = {}
            if not isinstance(__appliedInX, dict):
                raise ValueError("Error: observation operator defined by \"AppliedInX\" need a dictionary as argument.")
            for key in list(__appliedInX.keys()):
                if type( __appliedInX[key] ) is type( numpy.matrix([]) ):
                    # Pour le cas où l'on a une vraie matrice
                    self.__FO["AppliedInX"][key] = numpy.matrix( __appliedInX[key].A1, numpy.float ).T
                elif type( __appliedInX[key] ) is type( numpy.array([]) ) and len(__appliedInX[key].shape) > 1:
                    # Pour le cas où l'on a un vecteur représenté en array avec 2 dimensions
                    self.__FO["AppliedInX"][key] = numpy.matrix( __appliedInX[key].reshape(len(__appliedInX[key]),), numpy.float ).T
                else:
                    self.__FO["AppliedInX"][key] = numpy.matrix( __appliedInX[key],    numpy.float ).T
        else:
            self.__FO["AppliedInX"] = None

    def getO(self):
        return self.__FO

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__V)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__V)

# ==============================================================================
class Algorithm(object):
    """
    Classe générale d'interface de type algorithme

    Elle donne un cadre pour l'écriture d'une classe élémentaire d'algorithme
    d'assimilation, en fournissant un container (dictionnaire) de variables
    persistantes initialisées, et des méthodes d'accès à ces variables stockées.

    Une classe élémentaire d'algorithme doit implémenter la méthode "run".
    """
    def __init__(self, name):
        """
        L'initialisation présente permet de fabriquer des variables de stockage
        disponibles de manière générique dans les algorithmes élémentaires. Ces
        variables de stockage sont ensuite conservées dans un dictionnaire
        interne à l'objet, mais auquel on accède par la méthode "get".

        Les variables prévues sont :
            - CostFunctionJ  : fonction-cout globale, somme des deux parties suivantes
            - CostFunctionJb : partie ébauche ou background de la fonction-cout
            - CostFunctionJo : partie observations de la fonction-cout
            - GradientOfCostFunctionJ  : gradient de la fonction-cout globale
            - GradientOfCostFunctionJb : gradient de la partie ébauche de la fonction-cout
            - GradientOfCostFunctionJo : gradient de la partie observations de la fonction-cout
            - CurrentState : état courant lors d'itérations
            - Analysis : l'analyse Xa
            - SimulatedObservationAtBackground : l'état observé H(Xb) à l'ébauche
            - SimulatedObservationAtCurrentState : l'état observé H(X) à l'état courant
            - SimulatedObservationAtOptimum : l'état observé H(Xa) à l'optimum
            - Innovation : l'innovation : d = Y - H(X)
            - InnovationAtCurrentState : l'innovation à l'état courant : dn = Y - H(Xn)
            - SigmaObs2 : indicateur de correction optimale des erreurs d'observation
            - SigmaBck2 : indicateur de correction optimale des erreurs d'ébauche
            - MahalanobisConsistency : indicateur de consistance des covariances
            - OMA : Observation moins Analysis : Y - Xa
            - OMB : Observation moins Background : Y - Xb
            - AMB : Analysis moins Background : Xa - Xb
            - APosterioriCovariance : matrice A
            - APosterioriVariances : variances de la matrice A
            - APosterioriStandardDeviations : écart-types de la matrice A
            - APosterioriCorrelations : correlations de la matrice A
            - Residu : dans le cas des algorithmes de vérification
        On peut rajouter des variables à stocker dans l'initialisation de
        l'algorithme élémentaire qui va hériter de cette classe
        """
        logging.debug("%s Initialisation", str(name))
        self._m = PlatformInfo.SystemUsage()
        #
        self._name = str( name )
        self._parameters = {"StoreSupplementaryCalculations":[]}
        self.__required_parameters = {}
        self.__required_inputs = {"RequiredInputValues":{"mandatory":(), "optional":()}}
        #
        self.StoredVariables = {}
        self.StoredVariables["CostFunctionJ"]                        = Persistence.OneScalar(name = "CostFunctionJ")
        self.StoredVariables["CostFunctionJb"]                       = Persistence.OneScalar(name = "CostFunctionJb")
        self.StoredVariables["CostFunctionJo"]                       = Persistence.OneScalar(name = "CostFunctionJo")
        self.StoredVariables["CostFunctionJAtCurrentOptimum"]        = Persistence.OneScalar(name = "CostFunctionJAtCurrentOptimum")
        self.StoredVariables["CostFunctionJbAtCurrentOptimum"]       = Persistence.OneScalar(name = "CostFunctionJbAtCurrentOptimum")
        self.StoredVariables["CostFunctionJoAtCurrentOptimum"]       = Persistence.OneScalar(name = "CostFunctionJoAtCurrentOptimum")
        self.StoredVariables["GradientOfCostFunctionJ"]              = Persistence.OneVector(name = "GradientOfCostFunctionJ")
        self.StoredVariables["GradientOfCostFunctionJb"]             = Persistence.OneVector(name = "GradientOfCostFunctionJb")
        self.StoredVariables["GradientOfCostFunctionJo"]             = Persistence.OneVector(name = "GradientOfCostFunctionJo")
        self.StoredVariables["CurrentState"]                         = Persistence.OneVector(name = "CurrentState")
        self.StoredVariables["Analysis"]                             = Persistence.OneVector(name = "Analysis")
        self.StoredVariables["IndexOfOptimum"]                       = Persistence.OneIndex(name = "IndexOfOptimum")
        self.StoredVariables["CurrentOptimum"]                       = Persistence.OneVector(name = "CurrentOptimum")
        self.StoredVariables["SimulatedObservationAtBackground"]     = Persistence.OneVector(name = "SimulatedObservationAtBackground")
        self.StoredVariables["SimulatedObservationAtCurrentState"]   = Persistence.OneVector(name = "SimulatedObservationAtCurrentState")
        self.StoredVariables["SimulatedObservationAtOptimum"]        = Persistence.OneVector(name = "SimulatedObservationAtOptimum")
        self.StoredVariables["SimulatedObservationAtCurrentOptimum"] = Persistence.OneVector(name = "SimulatedObservationAtCurrentOptimum")
        self.StoredVariables["Innovation"]                           = Persistence.OneVector(name = "Innovation")
        self.StoredVariables["InnovationAtCurrentState"]             = Persistence.OneVector(name = "InnovationAtCurrentState")
        self.StoredVariables["SigmaObs2"]                            = Persistence.OneScalar(name = "SigmaObs2")
        self.StoredVariables["SigmaBck2"]                            = Persistence.OneScalar(name = "SigmaBck2")
        self.StoredVariables["MahalanobisConsistency"]               = Persistence.OneScalar(name = "MahalanobisConsistency")
        self.StoredVariables["OMA"]                                  = Persistence.OneVector(name = "OMA")
        self.StoredVariables["OMB"]                                  = Persistence.OneVector(name = "OMB")
        self.StoredVariables["BMA"]                                  = Persistence.OneVector(name = "BMA")
        self.StoredVariables["APosterioriCovariance"]                = Persistence.OneMatrix(name = "APosterioriCovariance")
        self.StoredVariables["APosterioriVariances"]                 = Persistence.OneVector(name = "APosterioriVariances")
        self.StoredVariables["APosterioriStandardDeviations"]        = Persistence.OneVector(name = "APosterioriStandardDeviations")
        self.StoredVariables["APosterioriCorrelations"]              = Persistence.OneMatrix(name = "APosterioriCorrelations")
        self.StoredVariables["SimulationQuantiles"]                  = Persistence.OneMatrix(name = "SimulationQuantiles")
        self.StoredVariables["Residu"]                               = Persistence.OneScalar(name = "Residu")

    def _pre_run(self, Parameters, Xb=None, Y=None, R=None, B=None, Q=None ):
        "Pré-calcul"
        logging.debug("%s Lancement", self._name)
        logging.debug("%s Taille mémoire utilisée de %.0f Mio", self._name, self._m.getUsedMemory("Mio"))
        #
        # Mise a jour de self._parameters avec Parameters
        self.__setParameters(Parameters)
        #
        # Corrections et complements
        def __test_vvalue( argument, variable, argname):
            if argument is None:
                if variable in self.__required_inputs["RequiredInputValues"]["mandatory"]:
                    raise ValueError("%s %s vector %s has to be properly defined!"%(self._name,argname,variable))
                elif variable in self.__required_inputs["RequiredInputValues"]["optional"]:
                    logging.debug("%s %s vector %s is not set, but is optional."%(self._name,argname,variable))
                else:
                    logging.debug("%s %s vector %s is not set, but is not required."%(self._name,argname,variable))
            else:
                logging.debug("%s %s vector %s is set, and its size is %i."%(self._name,argname,variable,numpy.array(argument).size))
        __test_vvalue( Xb, "Xb", "Background or initial state" )
        __test_vvalue( Y,  "Y",  "Observation" )
        def __test_cvalue( argument, variable, argname):
            if argument is None:
                if variable in self.__required_inputs["RequiredInputValues"]["mandatory"]:
                    raise ValueError("%s %s error covariance matrix %s has to be properly defined!"%(self._name,argname,variable))
                elif variable in self.__required_inputs["RequiredInputValues"]["optional"]:
                    logging.debug("%s %s error covariance matrix %s is not set, but is optional."%(self._name,argname,variable))
                else:
                    logging.debug("%s %s error covariance matrix %s is not set, but is not required."%(self._name,argname,variable))
            else:
                logging.debug("%s %s error covariance matrix %s is set."%(self._name,argname,variable))
        __test_cvalue( R, "R", "Observation" )
        __test_cvalue( B, "B", "Background" )
        __test_cvalue( Q, "Q", "Evolution" )
        #
        if ("Bounds" in self._parameters) and isinstance(self._parameters["Bounds"], (list, tuple)) and (len(self._parameters["Bounds"]) > 0):
            logging.debug("%s Prise en compte des bornes effectuee"%(self._name,))
        else:
            self._parameters["Bounds"] = None
        #
        if logging.getLogger().level < logging.WARNING:
            self._parameters["optiprint"], self._parameters["optdisp"] = 1, 1
            if PlatformInfo.has_scipy:
                import scipy.optimize
                self._parameters["optmessages"] = scipy.optimize.tnc.MSG_ALL
            else:
                self._parameters["optmessages"] = 15
        else:
            self._parameters["optiprint"], self._parameters["optdisp"] = -1, 0
            if PlatformInfo.has_scipy:
                import scipy.optimize
                self._parameters["optmessages"] = scipy.optimize.tnc.MSG_NONE
            else:
                self._parameters["optmessages"] = 15
        #
        return 0

    def _post_run(self,_oH=None):
        "Post-calcul"
        if ("StoreSupplementaryCalculations" in self._parameters) and \
            "APosterioriCovariance" in self._parameters["StoreSupplementaryCalculations"]:
            for _A in self.StoredVariables["APosterioriCovariance"]:
                if "APosterioriVariances" in self._parameters["StoreSupplementaryCalculations"]:
                    self.StoredVariables["APosterioriVariances"].store( numpy.diag(_A) )
                if "APosterioriStandardDeviations" in self._parameters["StoreSupplementaryCalculations"]:
                    self.StoredVariables["APosterioriStandardDeviations"].store( numpy.sqrt(numpy.diag(_A)) )
                if "APosterioriCorrelations" in self._parameters["StoreSupplementaryCalculations"]:
                    _EI = numpy.diag(1./numpy.sqrt(numpy.diag(_A)))
                    _C = numpy.dot(_EI, numpy.dot(_A, _EI))
                    self.StoredVariables["APosterioriCorrelations"].store( _C )
        if _oH is not None:
            logging.debug("%s Nombre d'évaluation(s) de l'opérateur d'observation direct/tangent/adjoint.: %i/%i/%i", self._name, _oH["Direct"].nbcalls(0),_oH["Tangent"].nbcalls(0),_oH["Adjoint"].nbcalls(0))
            logging.debug("%s Nombre d'appels au cache d'opérateur d'observation direct/tangent/adjoint..: %i/%i/%i", self._name, _oH["Direct"].nbcalls(3),_oH["Tangent"].nbcalls(3),_oH["Adjoint"].nbcalls(3))
        logging.debug("%s Taille mémoire utilisée de %.0f Mio", self._name, self._m.getUsedMemory("Mio"))
        logging.debug("%s Terminé", self._name)
        return 0

    def get(self, key=None):
        """
        Renvoie l'une des variables stockées identifiée par la clé, ou le
        dictionnaire de l'ensemble des variables disponibles en l'absence de
        clé. Ce sont directement les variables sous forme objet qui sont
        renvoyées, donc les méthodes d'accès à l'objet individuel sont celles
        des classes de persistance.
        """
        if key is not None:
            return self.StoredVariables[key]
        else:
            return self.StoredVariables

    def __contains__(self, key=None):
        "D.__contains__(k) -> True if D has a key k, else False"
        return key in self.StoredVariables

    def keys(self):
        "D.keys() -> list of D's keys"
        if hasattr(self, "StoredVariables"):
            return self.StoredVariables.keys()
        else:
            return []

    def pop(self, k, d):
        "D.pop(k[,d]) -> v, remove specified key and return the corresponding value"
        if hasattr(self, "StoredVariables"):
            return self.StoredVariables.pop(k, d)
        else:
            try:
                msg = "'%s'"%k
            except:
                raise TypeError("pop expected at least 1 arguments, got 0")
            "If key is not found, d is returned if given, otherwise KeyError is raised"
            try:
                return d
            except:
                raise KeyError(msg)

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Doit implémenter l'opération élémentaire de calcul d'assimilation sous
        sa forme mathématique la plus naturelle possible.
        """
        raise NotImplementedError("Mathematical assimilation calculation has not been implemented!")

    def defineRequiredParameter(self, name = None, default = None, typecast = None, message = None, minval = None, maxval = None, listval = None):
        """
        Permet de définir dans l'algorithme des paramètres requis et leurs
        caractéristiques par défaut.
        """
        if name is None:
            raise ValueError("A name is mandatory to define a required parameter.")
        #
        self.__required_parameters[name] = {
            "default"  : default,
            "typecast" : typecast,
            "minval"   : minval,
            "maxval"   : maxval,
            "listval"  : listval,
            "message"  : message,
            }
        logging.debug("%s %s (valeur par défaut = %s)", self._name, message, self.setParameterValue(name))

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
        default  = self.__required_parameters[name]["default"]
        typecast = self.__required_parameters[name]["typecast"]
        minval   = self.__required_parameters[name]["minval"]
        maxval   = self.__required_parameters[name]["maxval"]
        listval  = self.__required_parameters[name]["listval"]
        #
        if value is None and default is None:
            __val = None
        elif value is None and default is not None:
            if typecast is None: __val = default
            else:                __val = typecast( default )
        else:
            if typecast is None: __val = value
            else:                __val = typecast( value )
        #
        if minval is not None and (numpy.array(__val, float) < minval).any():
            raise ValueError("The parameter named \"%s\" of value \"%s\" can not be less than %s."%(name, __val, minval))
        if maxval is not None and (numpy.array(__val, float) > maxval).any():
            raise ValueError("The parameter named \"%s\" of value \"%s\" can not be greater than %s."%(name, __val, maxval))
        if listval is not None:
            if typecast is list or typecast is tuple or isinstance(__val,list) or isinstance(__val,tuple):
                for v in __val:
                    if v not in listval:
                        raise ValueError("The value \"%s\" of the parameter named \"%s\" is not allowed, it has to be in the list %s."%(v, name, listval))
            elif __val not in listval:
                raise ValueError("The value \"%s\" of the parameter named \"%s\" is not allowed, it has to be in the list %s."%( __val, name,listval))
        return __val

    def requireInputArguments(self, mandatory=(), optional=()):
        """
        Permet d'imposer des arguments requises en entrée
        """
        self.__required_inputs["RequiredInputValues"]["mandatory"] = tuple( mandatory )
        self.__required_inputs["RequiredInputValues"]["optional"]  = tuple( optional )

    def __setParameters(self, fromDico={}):
        """
        Permet de stocker les paramètres reçus dans le dictionnaire interne.
        """
        self._parameters.update( fromDico )
        for k in self.__required_parameters.keys():
            if k in fromDico.keys():
                self._parameters[k] = self.setParameterValue(k,fromDico[k])
            else:
                self._parameters[k] = self.setParameterValue(k)
            logging.debug("%s %s : %s", self._name, self.__required_parameters[k]["message"], self._parameters[k])

# ==============================================================================
class Diagnostic(object):
    """
    Classe générale d'interface de type diagnostic

    Ce template s'utilise de la manière suivante : il sert de classe "patron" en
    même temps que l'une des classes de persistance, comme "OneScalar" par
    exemple.

    Une classe élémentaire de diagnostic doit implémenter ses deux méthodes, la
    méthode "_formula" pour écrire explicitement et proprement la formule pour
    l'écriture mathématique du calcul du diagnostic (méthode interne non
    publique), et "calculate" pour activer la précédente tout en ayant vérifié
    et préparé les données, et pour stocker les résultats à chaque pas (méthode
    externe d'activation).
    """
    def __init__(self, name = "", parameters = {}):
        "Initialisation"
        self.name       = str(name)
        self.parameters = dict( parameters )

    def _formula(self, *args):
        """
        Doit implémenter l'opération élémentaire de diagnostic sous sa forme
        mathématique la plus naturelle possible.
        """
        raise NotImplementedError("Diagnostic mathematical formula has not been implemented!")

    def calculate(self, *args):
        """
        Active la formule de calcul avec les arguments correctement rangés
        """
        raise NotImplementedError("Diagnostic activation method has not been implemented!")

# ==============================================================================
class DiagnosticAndParameters(object):
    """
    Classe générale d'interface d'interface de type diagnostic
    """
    def __init__(self,
                 name               = "GenericDiagnostic",
                 asDiagnostic       = None,
                 asIdentifier       = None,
                 asDict             = None,
                 asScript           = None,
                 asUnit             = None,
                 asBaseType         = None,
                 asExistingDiags    = None,
                ):
        """
        """
        self.__name       = str(name)
        self.__D          = None
        self.__I          = None
        self.__P          = {}
        self.__U          = ""
        self.__B          = None
        self.__E          = tuple(asExistingDiags)
        self.__TheDiag    = None
        #
        if asScript is not None:
            __Diag = ImportFromScript(asScript).getvalue( "Diagnostic" )
            __Iden = ImportFromScript(asScript).getvalue( "Identifier" )
            __Dict = ImportFromScript(asScript).getvalue( self.__name, "Parameters" )
            __Unit = ImportFromScript(asScript).getvalue( "Unit" )
            __Base = ImportFromScript(asScript).getvalue( "BaseType" )
        else:
            __Diag = asDiagnostic
            __Iden = asIdentifier
            __Dict = asDict
            __Unit = asUnit
            __Base = asBaseType
       #
        if __Diag is not None:
            self.__D = str(__Diag)
        if __Iden is not None:
            self.__I = str(__Iden)
        else:
            self.__I = str(__Diag)
        if __Dict is not None:
            self.__P.update( dict(__Dict) )
        if __Unit is None or __Unit == "None":
            self.__U = ""
        if __Base is None or __Base == "None":
            self.__B = None
        #
        self.__setDiagnostic( self.__D, self.__I, self.__U, self.__B, self.__P, self.__E )

    def get(self):
        "Renvoie l'objet"
        return self.__TheDiag

    def __setDiagnostic(self, __choice = None, __name = "", __unit = "", __basetype = None, __parameters = {}, __existings = () ):
        """
        Permet de sélectionner un diagnostic a effectuer
        """
        if __choice is None:
            raise ValueError("Error: diagnostic choice has to be given")
        __daDirectory = "daDiagnostics"
        #
        # Recherche explicitement le fichier complet
        # ------------------------------------------
        __module_path = None
        for directory in sys.path:
            if os.path.isfile(os.path.join(directory, __daDirectory, str(__choice)+'.py')):
                __module_path = os.path.abspath(os.path.join(directory, __daDirectory))
        if __module_path is None:
            raise ImportError("No diagnostic module named \"%s\" was found in a \"%s\" subdirectory\n             The search path is %s"%(__choice, __daDirectory, sys.path))
        #
        # Importe le fichier complet comme un module
        # ------------------------------------------
        try:
            __sys_path_tmp = sys.path ; sys.path.insert(0,__module_path)
            self.__diagnosticFile = __import__(str(__choice), globals(), locals(), [])
            sys.path = __sys_path_tmp ; del __sys_path_tmp
        except ImportError as e:
            raise ImportError("The module named \"%s\" was found, but is incorrect at the import stage.\n             The import error message is: %s"%(__choice,e))
        #
        # Instancie un objet du type élémentaire du fichier
        # -------------------------------------------------
        if __name in __existings:
            raise ValueError("A default input with the same name \"%s\" already exists."%str(__name))
        else:
            self.__TheDiag = self.__diagnosticFile.ElementaryDiagnostic(
                name       = __name,
                unit       = __unit,
                basetype   = __basetype,
                parameters = __parameters )
        return 0

# ==============================================================================
class AlgorithmAndParameters(object):
    """
    Classe générale d'interface d'action pour l'algorithme et ses paramètres
    """
    def __init__(self,
                 name               = "GenericAlgorithm",
                 asAlgorithm        = None,
                 asDict             = None,
                 asScript           = None,
                ):
        """
        """
        self.__name       = str(name)
        self.__A          = None
        self.__P          = {}
        #
        self.__algorithm         = {}
        self.__algorithmFile     = None
        self.__algorithmName     = None
        #
        self.updateParameters( asDict, asScript )
        #
        if asScript is not None:
            __Algo = ImportFromScript(asScript).getvalue( "Algorithm" )
        else:
            __Algo = asAlgorithm
        #
        if __Algo is not None:
            self.__A = str(__Algo)
            self.__P.update( {"Algorithm":self.__A} )
        #
        self.__setAlgorithm( self.__A )

    def updateParameters(self,
                 asDict     = None,
                 asScript   = None,
                ):
        "Mise a jour des parametres"
        if asScript is not None:
            __Dict = ImportFromScript(asScript).getvalue( self.__name, "Parameters" )
        else:
            __Dict = asDict
        #
        if __Dict is not None:
            self.__P.update( dict(__Dict) )

    def executePythonScheme(self, asDictAO = None):
        "Permet de lancer le calcul d'assimilation"
        Operator.CM.clearCache()
        #
        if not isinstance(asDictAO, dict):
            raise ValueError("The objects for algorithm calculation have to be given together as a dictionnary, and they are not")
        if   hasattr(asDictAO["Background"],"getO"):        self.__Xb = asDictAO["Background"].getO()
        elif hasattr(asDictAO["CheckingPoint"],"getO"):     self.__Xb = asDictAO["CheckingPoint"].getO()
        else:                                               self.__Xb = None
        if hasattr(asDictAO["Observation"],"getO"):         self.__Y  = asDictAO["Observation"].getO()
        else:                                               self.__Y  = asDictAO["Observation"]
        if hasattr(asDictAO["ControlInput"],"getO"):        self.__U  = asDictAO["ControlInput"].getO()
        else:                                               self.__U  = asDictAO["ControlInput"]
        if hasattr(asDictAO["ObservationOperator"],"getO"): self.__HO = asDictAO["ObservationOperator"].getO()
        else:                                               self.__HO = asDictAO["ObservationOperator"]
        if hasattr(asDictAO["EvolutionModel"],"getO"):      self.__EM = asDictAO["EvolutionModel"].getO()
        else:                                               self.__EM = asDictAO["EvolutionModel"]
        if hasattr(asDictAO["ControlModel"],"getO"):        self.__CM = asDictAO["ControlModel"].getO()
        else:                                               self.__CM = asDictAO["ControlModel"]
        self.__B = asDictAO["BackgroundError"]
        self.__R = asDictAO["ObservationError"]
        self.__Q = asDictAO["EvolutionError"]
        #
        self.__shape_validate()
        #
        self.__algorithm.run(
            Xb         = self.__Xb,
            Y          = self.__Y,
            U          = self.__U,
            HO         = self.__HO,
            EM         = self.__EM,
            CM         = self.__CM,
            R          = self.__R,
            B          = self.__B,
            Q          = self.__Q,
            Parameters = self.__P,
            )
        return 0

    def executeYACSScheme(self, FileName=None):
        "Permet de lancer le calcul d'assimilation"
        if FileName is None or not os.path.exists(FileName):
            raise ValueError("a YACS file name has to be given for YACS execution.\n")
        if not PlatformInfo.has_salome or not PlatformInfo.has_yacs or not PlatformInfo.has_adao:
            raise ImportError("Unable to get SALOME, YACS or ADAO environnement variables. Please launch SALOME before executing.\n")
        #
        import pilot
        import SALOMERuntime
        import loader
        SALOMERuntime.RuntimeSALOME_setRuntime()

        r = pilot.getRuntime()
        xmlLoader = loader.YACSLoader()
        xmlLoader.registerProcCataLoader()
        try:
            catalogAd = r.loadCatalog("proc", os.path.abspath(FileName))
        except:
            pass
        r.addCatalog(catalogAd)

        try:
            p = xmlLoader.load(os.path.abspath(FileName))
        except IOError as ex:
            print("The YACS XML schema file can not be loaded: %s"%(ex,))

        logger = p.getLogger("parser")
        if not logger.isEmpty():
            print("The imported YACS XML schema has errors on parsing:")
            print(logger.getStr())

        if not p.isValid():
            print("The YACS XML schema is not valid and will not be executed:")
            print(p.getErrorReport())

        info=pilot.LinkInfo(pilot.LinkInfo.ALL_DONT_STOP)
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

    def get(self, key = None):
        "Vérifie l'existence d'une clé de variable ou de paramètres"
        if key in self.__algorithm:
            return self.__algorithm.get( key )
        elif key in self.__P:
            return self.__P[key]
        else:
            return self.__P

    def pop(self, k, d):
        "Necessaire pour le pickling"
        return self.__algorithm.pop(k, d)

    def getAlgorithmRequiredParameters(self, noDetails=True):
        "Renvoie la liste des paramètres requis selon l'algorithme"
        return self.__algorithm.getRequiredParameters(noDetails)

    def setObserver(self, __V, __O, __I, __S):
        if self.__algorithm is None \
            or isinstance(self.__algorithm, dict) \
            or not hasattr(self.__algorithm,"StoredVariables"):
            raise ValueError("No observer can be build before choosing an algorithm.")
        if __V not in self.__algorithm:
            raise ValueError("An observer requires to be set on a variable named %s which does not exist."%__V)
        else:
            self.__algorithm.StoredVariables[ __V ].setDataObserver(
                    Scheduler      = __S,
                    HookFunction   = __O,
                    HookParameters = __I,
                    )

    def removeObserver(self, __V, __O, __A = False):
        if self.__algorithm is None \
            or isinstance(self.__algorithm, dict) \
            or not hasattr(self.__algorithm,"StoredVariables"):
            raise ValueError("No observer can be removed before choosing an algorithm.")
        if __V not in self.__algorithm:
            raise ValueError("An observer requires to be removed on a variable named %s which does not exist."%__V)
        else:
            return self.__algorithm.StoredVariables[ __V ].removeDataObserver(
                    HookFunction   = __O,
                    AllObservers   = __A,
                    )

    def hasObserver(self, __V):
        if self.__algorithm is None \
            or isinstance(self.__algorithm, dict) \
            or not hasattr(self.__algorithm,"StoredVariables"):
            return False
        if __V not in self.__algorithm:
            return False
        return self.__algorithm.StoredVariables[ __V ].hasDataObserver()

    def keys(self):
        return list(self.__algorithm.keys()) + list(self.__P.keys())

    def __contains__(self, key=None):
        "D.__contains__(k) -> True if D has a key k, else False"
        return key in self.__algorithm or key in self.__P

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__A)+", "+repr(self.__P)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__A)+", "+str(self.__P)

    def __setAlgorithm(self, choice = None ):
        """
        Permet de sélectionner l'algorithme à utiliser pour mener à bien l'étude
        d'assimilation. L'argument est un champ caractère se rapportant au nom
        d'un fichier contenu dans "../daAlgorithms" et réalisant l'opération
        d'assimilation sur les arguments fixes.
        """
        if choice is None:
            raise ValueError("Error: algorithm choice has to be given")
        if self.__algorithmName is not None:
            raise ValueError("Error: algorithm choice has already been done as \"%s\", it can't be changed."%self.__algorithmName)
        daDirectory = "daAlgorithms"
        #
        # Recherche explicitement le fichier complet
        # ------------------------------------------
        module_path = None
        for directory in sys.path:
            if os.path.isfile(os.path.join(directory, daDirectory, str(choice)+'.py')):
                module_path = os.path.abspath(os.path.join(directory, daDirectory))
        if module_path is None:
            raise ImportError("No algorithm module named \"%s\" was found in a \"%s\" subdirectory\n             The search path is %s"%(choice, daDirectory, sys.path))
        #
        # Importe le fichier complet comme un module
        # ------------------------------------------
        try:
            sys_path_tmp = sys.path ; sys.path.insert(0,module_path)
            self.__algorithmFile = __import__(str(choice), globals(), locals(), [])
            self.__algorithmName = str(choice)
            sys.path = sys_path_tmp ; del sys_path_tmp
        except ImportError as e:
            raise ImportError("The module named \"%s\" was found, but is incorrect at the import stage.\n             The import error message is: %s"%(choice,e))
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
        if self.__Xb is None:                      __Xb_shape = (0,)
        elif hasattr(self.__Xb,"size"):            __Xb_shape = (self.__Xb.size,)
        elif hasattr(self.__Xb,"shape"):
            if isinstance(self.__Xb.shape, tuple): __Xb_shape = self.__Xb.shape
            else:                                  __Xb_shape = self.__Xb.shape()
        else: raise TypeError("The background (Xb) has no attribute of shape: problem !")
        #
        if self.__Y is None:                       __Y_shape = (0,)
        elif hasattr(self.__Y,"size"):             __Y_shape = (self.__Y.size,)
        elif hasattr(self.__Y,"shape"):
            if isinstance(self.__Y.shape, tuple):  __Y_shape = self.__Y.shape
            else:                                  __Y_shape = self.__Y.shape()
        else: raise TypeError("The observation (Y) has no attribute of shape: problem !")
        #
        if self.__U is None:                       __U_shape = (0,)
        elif hasattr(self.__U,"size"):             __U_shape = (self.__U.size,)
        elif hasattr(self.__U,"shape"):
            if isinstance(self.__U.shape, tuple):  __U_shape = self.__U.shape
            else:                                  __U_shape = self.__U.shape()
        else: raise TypeError("The control (U) has no attribute of shape: problem !")
        #
        if self.__B is None:                       __B_shape = (0,0)
        elif hasattr(self.__B,"shape"):
            if isinstance(self.__B.shape, tuple):  __B_shape = self.__B.shape
            else:                                  __B_shape = self.__B.shape()
        else: raise TypeError("The a priori errors covariance matrix (B) has no attribute of shape: problem !")
        #
        if self.__R is None:                       __R_shape = (0,0)
        elif hasattr(self.__R,"shape"):
            if isinstance(self.__R.shape, tuple):  __R_shape = self.__R.shape
            else:                                  __R_shape = self.__R.shape()
        else: raise TypeError("The observation errors covariance matrix (R) has no attribute of shape: problem !")
        #
        if self.__Q is None:                       __Q_shape = (0,0)
        elif hasattr(self.__Q,"shape"):
            if isinstance(self.__Q.shape, tuple):  __Q_shape = self.__Q.shape
            else:                                  __Q_shape = self.__Q.shape()
        else: raise TypeError("The evolution errors covariance matrix (Q) has no attribute of shape: problem !")
        #
        if len(self.__HO) == 0:                              __HO_shape = (0,0)
        elif isinstance(self.__HO, dict):                    __HO_shape = (0,0)
        elif hasattr(self.__HO["Direct"],"shape"):
            if isinstance(self.__HO["Direct"].shape, tuple): __HO_shape = self.__HO["Direct"].shape
            else:                                            __HO_shape = self.__HO["Direct"].shape()
        else: raise TypeError("The observation operator (H) has no attribute of shape: problem !")
        #
        if len(self.__EM) == 0:                              __EM_shape = (0,0)
        elif isinstance(self.__EM, dict):                    __EM_shape = (0,0)
        elif hasattr(self.__EM["Direct"],"shape"):
            if isinstance(self.__EM["Direct"].shape, tuple): __EM_shape = self.__EM["Direct"].shape
            else:                                            __EM_shape = self.__EM["Direct"].shape()
        else: raise TypeError("The evolution model (EM) has no attribute of shape: problem !")
        #
        if len(self.__CM) == 0:                              __CM_shape = (0,0)
        elif isinstance(self.__CM, dict):                    __CM_shape = (0,0)
        elif hasattr(self.__CM["Direct"],"shape"):
            if isinstance(self.__CM["Direct"].shape, tuple): __CM_shape = self.__CM["Direct"].shape
            else:                                            __CM_shape = self.__CM["Direct"].shape()
        else: raise TypeError("The control model (CM) has no attribute of shape: problem !")
        #
        # Vérification des conditions
        # ---------------------------
        if not( len(__Xb_shape) == 1 or min(__Xb_shape) == 1 ):
            raise ValueError("Shape characteristic of background (Xb) is incorrect: \"%s\"."%(__Xb_shape,))
        if not( len(__Y_shape) == 1 or min(__Y_shape) == 1 ):
            raise ValueError("Shape characteristic of observation (Y) is incorrect: \"%s\"."%(__Y_shape,))
        #
        if not( min(__B_shape) == max(__B_shape) ):
            raise ValueError("Shape characteristic of a priori errors covariance matrix (B) is incorrect: \"%s\"."%(__B_shape,))
        if not( min(__R_shape) == max(__R_shape) ):
            raise ValueError("Shape characteristic of observation errors covariance matrix (R) is incorrect: \"%s\"."%(__R_shape,))
        if not( min(__Q_shape) == max(__Q_shape) ):
            raise ValueError("Shape characteristic of evolution errors covariance matrix (Q) is incorrect: \"%s\"."%(__Q_shape,))
        if not( min(__EM_shape) == max(__EM_shape) ):
            raise ValueError("Shape characteristic of evolution operator (EM) is incorrect: \"%s\"."%(__EM_shape,))
        #
        if len(self.__HO) > 0 and not isinstance(self.__HO, dict) and not( __HO_shape[1] == max(__Xb_shape) ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and state (X) \"%s\" are incompatible."%(__HO_shape,__Xb_shape))
        if len(self.__HO) > 0 and not isinstance(self.__HO, dict) and not( __HO_shape[0] == max(__Y_shape) ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and observation (Y) \"%s\" are incompatible."%(__HO_shape,__Y_shape))
        if len(self.__HO) > 0 and not isinstance(self.__HO, dict) and len(self.__B) > 0 and not( __HO_shape[1] == __B_shape[0] ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and a priori errors covariance matrix (B) \"%s\" are incompatible."%(__HO_shape,__B_shape))
        if len(self.__HO) > 0 and not isinstance(self.__HO, dict) and len(self.__R) > 0 and not( __HO_shape[0] == __R_shape[1] ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and observation errors covariance matrix (R) \"%s\" are incompatible."%(__HO_shape,__R_shape))
        #
        if self.__B is not None and len(self.__B) > 0 and not( __B_shape[1] == max(__Xb_shape) ):
            if self.__algorithmName in ["EnsembleBlue",]:
                asPersistentVector = self.__Xb.reshape((-1,min(__B_shape)))
                self.__Xb = Persistence.OneVector("Background", basetype=numpy.matrix)
                for member in asPersistentVector:
                    self.__Xb.store( numpy.matrix( numpy.ravel(member), numpy.float ).T )
                __Xb_shape = min(__B_shape)
            else:
                raise ValueError("Shape characteristic of a priori errors covariance matrix (B) \"%s\" and background (Xb) \"%s\" are incompatible."%(__B_shape,__Xb_shape))
        #
        if self.__R is not None and len(self.__R) > 0 and not( __R_shape[1] == max(__Y_shape) ):
            raise ValueError("Shape characteristic of observation errors covariance matrix (R) \"%s\" and observation (Y) \"%s\" are incompatible."%(__R_shape,__Y_shape))
        #
        if self.__EM is not None and len(self.__EM) > 0 and not isinstance(self.__EM, dict) and not( __EM_shape[1] == max(__Xb_shape) ):
            raise ValueError("Shape characteristic of evolution model (EM) \"%s\" and state (X) \"%s\" are incompatible."%(__EM_shape,__Xb_shape))
        #
        if self.__CM is not None and len(self.__CM) > 0 and not isinstance(self.__CM, dict) and not( __CM_shape[1] == max(__U_shape) ):
            raise ValueError("Shape characteristic of control model (CM) \"%s\" and control (U) \"%s\" are incompatible."%(__CM_shape,__U_shape))
        #
        if ("Bounds" in self.__P) \
            and (isinstance(self.__P["Bounds"], list) or isinstance(self.__P["Bounds"], tuple)) \
            and (len(self.__P["Bounds"]) != max(__Xb_shape)):
            raise ValueError("The number \"%s\" of bound pairs for the state (X) components is different of the size \"%s\" of the state itself." \
                %(len(self.__P["Bounds"]),max(__Xb_shape)))
        #
        return 1

# ==============================================================================
class DataObserver(object):
    """
    Classe générale d'interface de type observer
    """
    def __init__(self,
                 name        = "GenericObserver",
                 onVariable  = None,
                 asTemplate  = None,
                 asString    = None,
                 asScript    = None,
                 asObsObject = None,
                 withInfo    = None,
                 scheduledBy = None,
                 withAlgo    = None,
                ):
        """
        """
        self.__name       = str(name)
        self.__V          = None
        self.__O          = None
        self.__I          = None
        #
        if onVariable is None:
            raise ValueError("setting an observer has to be done over a variable name or a list of variable names, not over None.")
        elif type(onVariable) in (tuple, list):
            self.__V = tuple(map( str, onVariable ))
            if withInfo is None:
                self.__I = self.__V
            else:
                self.__I = (str(withInfo),)*len(self.__V)
        elif isinstance(onVariable, str):
            self.__V = (onVariable,)
            if withInfo is None:
                self.__I = (onVariable,)
            else:
                self.__I = (str(withInfo),)
        else:
            raise ValueError("setting an observer has to be done over a variable name or a list of variable names.")
        #
        if asString is not None:
            __FunctionText = asString
        elif (asTemplate is not None) and (asTemplate in Templates.ObserverTemplates):
            __FunctionText = Templates.ObserverTemplates[asTemplate]
        elif asScript is not None:
            __FunctionText = ImportFromScript(asScript).getstring()
        else:
            __FunctionText = ""
        __Function = ObserverF(__FunctionText)
        #
        if asObsObject is not None:
            self.__O = asObsObject
        else:
            self.__O = __Function.getfunc()
        #
        for k in range(len(self.__V)):
            ename = self.__V[k]
            einfo = self.__I[k]
            if ename not in withAlgo:
                raise ValueError("An observer is asked to be set on a variable named %s which does not exist."%ename)
            else:
                withAlgo.setObserver(ename, self.__O, einfo, scheduledBy)

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__V)+"\n"+repr(self.__O)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__V)+"\n"+str(self.__O)

# ==============================================================================
class State(object):
    """
    Classe générale d'interface de type état
    """
    def __init__(self,
                 name               = "GenericVector",
                 asVector           = None,
                 asPersistentVector = None,
                 asScript           = None,
                 scheduledBy        = None,
                 toBeChecked        = False,
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
        """
        self.__name       = str(name)
        self.__check      = bool(toBeChecked)
        #
        self.__V          = None
        self.__T          = None
        self.__is_vector  = False
        self.__is_series  = False
        #
        if asScript is not None:
            __Vector, __Series = None, None
            if asPersistentVector:
                __Series = ImportFromScript(asScript).getvalue( self.__name )
            else:
                __Vector = ImportFromScript(asScript).getvalue( self.__name )
        else:
            __Vector, __Series = asVector, asPersistentVector
        #
        if __Vector is not None:
            self.__is_vector = True
            self.__V         = numpy.matrix( numpy.asmatrix(__Vector).A1, numpy.float ).T
            self.shape       = self.__V.shape
            self.size        = self.__V.size
        elif __Series is not None:
            self.__is_series  = True
            if isinstance(__Series, (tuple, list, numpy.ndarray, numpy.matrix)):
                self.__V = Persistence.OneVector(self.__name, basetype=numpy.matrix)
                for member in __Series:
                    self.__V.store( numpy.matrix( numpy.asmatrix(member).A1, numpy.float ).T )
                import sys ; sys.stdout.flush()
            else:
                self.__V = __Series
            if isinstance(self.__V.shape, (tuple, list)):
                self.shape       = self.__V.shape
            else:
                self.shape       = self.__V.shape()
            if len(self.shape) == 1:
                self.shape       = (self.shape[0],1)
            self.size        = self.shape[0] * self.shape[1]
        else:
            raise ValueError("The %s object is improperly defined, it requires at minima either a vector, a list/tuple of vectors or a persistent object. Please check your vector input."%self.__name)
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
    def __init__(self,
                 name          = "GenericCovariance",
                 asCovariance  = None,
                 asEyeByScalar = None,
                 asEyeByVector = None,
                 asCovObject   = None,
                 asScript      = None,
                 toBeChecked   = False,
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
        self.__name       = str(name)
        self.__check      = bool(toBeChecked)
        #
        self.__C          = None
        self.__is_scalar  = False
        self.__is_vector  = False
        self.__is_matrix  = False
        self.__is_object  = False
        #
        if asScript is not None:
            __Matrix, __Scalar, __Vector, __Object = None, None, None, None
            if asEyeByScalar:
                __Scalar = ImportFromScript(asScript).getvalue( self.__name )
            elif asEyeByVector:
                __Vector = ImportFromScript(asScript).getvalue( self.__name )
            elif asCovObject:
                __Object = ImportFromScript(asScript).getvalue( self.__name )
            else:
                __Matrix = ImportFromScript(asScript).getvalue( self.__name )
        else:
            __Matrix, __Scalar, __Vector, __Object = asCovariance, asEyeByScalar, asEyeByVector, asCovObject
        #
        if __Scalar is not None:
            if numpy.matrix(__Scalar).size != 1:
                raise ValueError('  The diagonal multiplier given to define a sparse matrix is not a unique scalar value.\n  Its actual measured size is %i. Please check your scalar input.'%numpy.matrix(__Scalar).size)
            self.__is_scalar = True
            self.__C         = numpy.abs( float(__Scalar) )
            self.shape       = (0,0)
            self.size        = 0
        elif __Vector is not None:
            self.__is_vector = True
            self.__C         = numpy.abs( numpy.array( numpy.ravel( numpy.matrix(__Vector, float ) ) ) )
            self.shape       = (self.__C.size,self.__C.size)
            self.size        = self.__C.size**2
        elif __Matrix is not None:
            self.__is_matrix = True
            self.__C         = numpy.matrix( __Matrix, float )
            self.shape       = self.__C.shape
            self.size        = self.__C.size
        elif __Object is not None:
            self.__is_object = True
            self.__C         = __Object
            for at in ("getT","getI","diag","trace","__add__","__sub__","__neg__","__mul__","__rmul__"):
                if not hasattr(self.__C,at):
                    raise ValueError("The matrix given for %s as an object has no attribute \"%s\". Please check your object input."%(self.__name,at))
            if hasattr(self.__C,"shape"):
                self.shape       = self.__C.shape
            else:
                self.shape       = (0,0)
            if hasattr(self.__C,"size"):
                self.size        = self.__C.size
            else:
                self.size        = 0
        else:
            pass
            # raise ValueError("The %s covariance matrix has to be specified either as a matrix, a vector for its diagonal or a scalar multiplying an identity matrix."%self.__name)
        #
        self.__validate()

    def __validate(self):
        "Validation"
        if self.__C is None:
            raise UnboundLocalError("%s covariance matrix value has not been set!"%(self.__name,))
        if self.ismatrix() and min(self.shape) != max(self.shape):
            raise ValueError("The given matrix for %s is not a square one, its shape is %s. Please check your matrix input."%(self.__name,self.shape))
        if self.isobject() and min(self.shape) != max(self.shape):
            raise ValueError("The matrix given for \"%s\" is not a square one, its shape is %s. Please check your object input."%(self.__name,self.shape))
        if self.isscalar() and self.__C <= 0:
            raise ValueError("The \"%s\" covariance matrix is not positive-definite. Please check your scalar input %s."%(self.__name,self.__C))
        if self.isvector() and (self.__C <= 0).any():
            raise ValueError("The \"%s\" covariance matrix is not positive-definite. Please check your vector input."%(self.__name,))
        if self.ismatrix() and (self.__check or logging.getLogger().level < logging.WARNING):
            try:
                L = numpy.linalg.cholesky( self.__C )
            except:
                raise ValueError("The %s covariance matrix is not symmetric positive-definite. Please check your matrix input."%(self.__name,))
        if self.isobject() and (self.__check or logging.getLogger().level < logging.WARNING):
            try:
                L = self.__C.cholesky()
            except:
                raise ValueError("The %s covariance object is not symmetric positive-definite. Please check your matrix input."%(self.__name,))

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
        if   self.ismatrix():
            return Covariance(self.__name+"I", asCovariance  = self.__C.I )
        elif self.isvector():
            return Covariance(self.__name+"I", asEyeByVector = 1. / self.__C )
        elif self.isscalar():
            return Covariance(self.__name+"I", asEyeByScalar = 1. / self.__C )
        elif self.isobject():
            return Covariance(self.__name+"I", asCovObject   = self.__C.getI() )
        else:
            return None # Indispensable

    def getT(self):
        "Transposition"
        if   self.ismatrix():
            return Covariance(self.__name+"T", asCovariance  = self.__C.T )
        elif self.isvector():
            return Covariance(self.__name+"T", asEyeByVector = self.__C )
        elif self.isscalar():
            return Covariance(self.__name+"T", asEyeByScalar = self.__C )
        elif self.isobject():
            return Covariance(self.__name+"T", asCovObject   = self.__C.getT() )

    def cholesky(self):
        "Décomposition de Cholesky"
        if   self.ismatrix():
            return Covariance(self.__name+"C", asCovariance  = numpy.linalg.cholesky(self.__C) )
        elif self.isvector():
            return Covariance(self.__name+"C", asEyeByVector = numpy.sqrt( self.__C ) )
        elif self.isscalar():
            return Covariance(self.__name+"C", asEyeByScalar = numpy.sqrt( self.__C ) )
        elif self.isobject() and hasattr(self.__C,"cholesky"):
            return Covariance(self.__name+"C", asCovObject   = self.__C.cholesky() )

    def choleskyI(self):
        "Inversion de la décomposition de Cholesky"
        if   self.ismatrix():
            return Covariance(self.__name+"H", asCovariance  = numpy.linalg.cholesky(self.__C).I )
        elif self.isvector():
            return Covariance(self.__name+"H", asEyeByVector = 1.0 / numpy.sqrt( self.__C ) )
        elif self.isscalar():
            return Covariance(self.__name+"H", asEyeByScalar = 1.0 / numpy.sqrt( self.__C ) )
        elif self.isobject() and hasattr(self.__C,"choleskyI"):
            return Covariance(self.__name+"H", asCovObject   = self.__C.choleskyI() )

    def diag(self, msize=None):
        "Diagonale de la matrice"
        if   self.ismatrix():
            return numpy.diag(self.__C)
        elif self.isvector():
            return self.__C
        elif self.isscalar():
            if msize is None:
                raise ValueError("the size of the %s covariance matrix has to be given in case of definition as a scalar over the diagonal."%(self.__name,))
            else:
                return self.__C * numpy.ones(int(msize))
        elif self.isobject():
            return self.__C.diag()

    def asfullmatrix(self, msize=None):
        "Matrice pleine"
        if   self.ismatrix():
            return self.__C
        elif self.isvector():
            return numpy.matrix( numpy.diag(self.__C), float )
        elif self.isscalar():
            if msize is None:
                raise ValueError("the size of the %s covariance matrix has to be given in case of definition as a scalar over the diagonal."%(self.__name,))
            else:
                return numpy.matrix( self.__C * numpy.eye(int(msize)), float )
        elif self.isobject() and hasattr(self.__C,"asfullmatrix"):
            return self.__C.asfullmatrix()

    def trace(self, msize=None):
        "Trace de la matrice"
        if   self.ismatrix():
            return numpy.trace(self.__C)
        elif self.isvector():
            return float(numpy.sum(self.__C))
        elif self.isscalar():
            if msize is None:
                raise ValueError("the size of the %s covariance matrix has to be given in case of definition as a scalar over the diagonal."%(self.__name,))
            else:
                return self.__C * int(msize)
        elif self.isobject():
            return self.__C.trace()

    def getO(self):
        return self

    def __repr__(self):
        "x.__repr__() <==> repr(x)"
        return repr(self.__C)

    def __str__(self):
        "x.__str__() <==> str(x)"
        return str(self.__C)

    def __add__(self, other):
        "x.__add__(y) <==> x+y"
        if   self.ismatrix() or self.isobject():
            return self.__C + numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            _A.reshape(_A.size)[::_A.shape[1]+1] += self.__C
            return numpy.asmatrix(_A)

    def __radd__(self, other):
        "x.__radd__(y) <==> y+x"
        raise NotImplementedError("%s covariance matrix __radd__ method not available for %s type!"%(self.__name,type(other)))

    def __sub__(self, other):
        "x.__sub__(y) <==> x-y"
        if   self.ismatrix() or self.isobject():
            return self.__C - numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            _A.reshape(_A.size)[::_A.shape[1]+1] = self.__C - _A.reshape(_A.size)[::_A.shape[1]+1]
            return numpy.asmatrix(_A)

    def __rsub__(self, other):
        "x.__rsub__(y) <==> y-x"
        raise NotImplementedError("%s covariance matrix __rsub__ method not available for %s type!"%(self.__name,type(other)))

    def __neg__(self):
        "x.__neg__() <==> -x"
        return - self.__C

    def __mul__(self, other):
        "x.__mul__(y) <==> x*y"
        if   self.ismatrix() and isinstance(other,numpy.matrix):
            return self.__C * other
        elif self.ismatrix() and isinstance(other, (list, numpy.ndarray, tuple)):
            if numpy.ravel(other).size == self.shape[1]: # Vecteur
                return self.__C * numpy.asmatrix(numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]: # Matrice
                return self.__C * numpy.asmatrix(other)
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.asmatrix(other).shape,self.__name))
        elif self.isvector() and isinstance(other, (list, numpy.matrix, numpy.ndarray, tuple)):
            if numpy.ravel(other).size == self.shape[1]: # Vecteur
                return numpy.asmatrix(self.__C * numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]: # Matrice
                return numpy.asmatrix((self.__C * (numpy.asarray(other).transpose())).transpose())
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.ravel(other).shape,self.__name))
        elif self.isscalar() and isinstance(other,numpy.matrix):
            return self.__C * other
        elif self.isscalar() and isinstance(other, (list, numpy.ndarray, tuple)):
            if len(numpy.asarray(other).shape) == 1 or numpy.asarray(other).shape[1] == 1 or numpy.asarray(other).shape[0] == 1:
                return self.__C * numpy.asmatrix(numpy.ravel(other)).T
            else:
                return self.__C * numpy.asmatrix(other)
        elif self.isobject():
            return self.__C.__mul__(other)
        else:
            raise NotImplementedError("%s covariance matrix __mul__ method not available for %s type!"%(self.__name,type(other)))

    def __rmul__(self, other):
        "x.__rmul__(y) <==> y*x"
        if self.ismatrix() and isinstance(other,numpy.matrix):
            return other * self.__C
        elif self.isvector() and isinstance(other,numpy.matrix):
            if numpy.ravel(other).size == self.shape[0]: # Vecteur
                return numpy.asmatrix(numpy.ravel(other) * self.__C)
            elif numpy.asmatrix(other).shape[1] == self.shape[0]: # Matrice
                return numpy.asmatrix(numpy.array(other) * self.__C)
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.ravel(other).shape,self.__name))
        elif self.isscalar() and isinstance(other,numpy.matrix):
            return other * self.__C
        elif self.isobject():
            return self.__C.__rmul__(other)
        else:
            raise NotImplementedError("%s covariance matrix __rmul__ method not available for %s type!"%(self.__name,type(other)))

    def __len__(self):
        "x.__len__() <==> len(x)"
        return self.shape[0]

# ==============================================================================
class ObserverF(object):
    """
    Creation d'une fonction d'observateur a partir de son texte
    """
    def __init__(self, corps=""):
        self.__corps = corps
    def func(self,var,info):
        "Fonction d'observation"
        exec(self.__corps)
    def getfunc(self):
        "Restitution du pointeur de fonction dans l'objet"
        return self.func

# ==============================================================================
class CaseLogger(object):
    """
    Conservation des commandes de creation d'un cas
    """
    def __init__(self, __name="", __objname="case", __addViewers=None, __addLoaders=None):
        self.__name     = str(__name)
        self.__objname  = str(__objname)
        self.__logSerie = []
        self.__switchoff = False
        self.__viewers = self.__loaders = {
            "TUI":_TUIViewer,
            "DCT":_DCTViewer,
            "SCD":_SCDViewer,
            "YACS":_YACSViewer,
            }
        if __addViewers is not None:
            self.__viewers.update(dict(__addViewers))
        if __addLoaders is not None:
            self.__loaders.update(dict(__addLoaders))

    def register(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Enregistrement d'une commande individuelle"
        if __command is not None and __keys is not None and __local is not None and not self.__switchoff:
            if "self" in __keys: __keys.remove("self")
            self.__logSerie.append( (str(__command), __keys, __local, __pre, __switchoff) )
            if __switchoff:
                self.__switchoff = True
        if not __switchoff:
            self.__switchoff = False

    def dump(self, __filename=None, __format="TUI"):
        "Restitution normalisée des commandes (par les *GenericCaseViewer)"
        if __format in self.__viewers:
            __formater = self.__viewers[__format](self.__name, self.__objname, self.__logSerie)
        else:
            raise ValueError("Dumping as \"%s\" is not available"%__format)
        return __formater.dump(__filename)

    def load(self, __filename=None, __format="TUI"):
        "Chargement normalisé des commandes"
        if __format in self.__loaders:
            __formater = self.__loaders[__format]()
        else:
            raise ValueError("Loading as \"%s\" is not available"%__format)
        return __formater.load(__filename)

# ==============================================================================
class GenericCaseViewer(object):
    """
    Gestion des commandes de creation d'une vue de cas
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        self._name     = str(__name)
        self._objname  = str(__objname)
        self._lineSerie = []
        self._switchoff = False
        self._numobservers = 2
        self._content = __content
        self._missing = """raise ValueError("This case requires beforehand to import or define the variable named <%s>. When corrected, remove this command, correct and uncomment the following one.")\n# """
    def _append(self):
        "Transformation de commande individuelle en enregistrement"
        raise NotImplementedError()
    def _extract(self):
        "Transformation d'enregistrement en commande individuelle"
        raise NotImplementedError()
    def _finalize(self):
        "Enregistrement du final"
        pass
    def _addLine(self, line=""):
        "Ajoute un enregistrement individuel"
        self._lineSerie.append(line)
    def dump(self, __filename=None):
        "Restitution normalisée des commandes"
        self._finalize()
        __text = "\n".join(self._lineSerie)
        __text +="\n"
        if __filename is not None:
            __file = os.path.abspath(__filename)
            __fid = open(__file,"w")
            __fid.write(__text)
            __fid.close()
        return __text
    def load(self, __filename=None):
        "Chargement normalisé des commandes"
        if os.path.exists(__filename):
            self._content = open(__filename, 'r').read()
        __commands = self._extract(self._content)
        return __commands

    # --> Inutile d'accrocher l'interpretation au cas
    # def _interpret(self):
    #     "Interprétation d'une commande"
    #     raise NotImplementedError()
    # def execCase(self, __filename=None):
    #     "Exécution normalisée des commandes"
    #     if os.path.exists(__filename):
    #         self._content = open(__filename, 'r').read()
    #     __retcode = self._interpret(self._content)
    #     return __retcode

class _TUIViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas TUI
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content)
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Python script for ADAO TUI\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("import adaoBuilder")
        self._addLine("%s = adaoBuilder.New('%s')"%(self._objname, self._name))
        if self._content is not None:
            for command in self._content:
                self._append(*command)
    def _append(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Transformation d'une commande individuelle en un enregistrement"
        if __command is not None and __keys is not None and __local is not None:
            __text  = ""
            if __pre is not None:
                __text += "%s = "%__pre
            __text += "%s.%s( "%(self._objname,str(__command))
            if "self" in __keys: __keys.remove("self")
            if __command not in ("set","get") and "Concept" in __keys: __keys.remove("Concept")
            for k in __keys:
                __v = __local[k]
                if __v is None: continue
                if   k == "Checked" and not __v: continue
                if   k == "Stored"  and not __v: continue
                if   k == "AvoidRC" and __v: continue
                if   k == "noDetails": continue
                if isinstance(__v,Persistence.Persistence): __v = __v.values()
                if callable(__v): __text = self._missing%__v.__name__+__text
                if isinstance(__v,dict):
                    for val in __v.values():
                        if callable(val): __text = self._missing%val.__name__+__text
                numpy.set_printoptions(precision=15,threshold=1000000,linewidth=1000*15)
                __text += "%s=%s, "%(k,repr(__v))
                numpy.set_printoptions(precision=8,threshold=1000,linewidth=75)
            __text.rstrip(", ")
            __text += ")"
            self._addLine(__text)
    def _extract(self, __content=""):
        "Transformation un enregistrement en une commande individuelle"
        __is_case = False
        __commands = []
        __content = __content.replace("\r\n","\n")
        for line in __content.split("\n"):
            if "adaoBuilder.New" in line and "=" in line:
                self._objname = line.split("=")[0].strip()
                __is_case = True
            if not __is_case:
                continue
            else:
                if self._objname+".set" in line:
                    __commands.append( line.replace(self._objname+".","",1) )
        return __commands

    # def _interpret(self, __content=""):
    #     "Interprétation d'une commande"
    #     __content = __content.replace("\r\n","\n")
    #     exec(__content)
    #     return 0

class _DCTViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas DCT
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content)
        self._observerIndex = 0
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Python script for ADAO DCT\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("#")
        self._addLine("%s = {}"%__objname)
        if self._content is not None:
            for command in self._content:
                self._append(*command)
    def _append(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Transformation d'une commande individuelle en un enregistrement"
        if __command is not None and __keys is not None and __local is not None:
            __text  = ""
            if "execute" in __command: return
            if "self" in __keys: __keys.remove("self")
            if __command in ("set","get") and "Concept" in __keys:
                __key = __local["Concept"]
                __keys.remove("Concept")
            else:
                __key = __command.replace("set","").replace("get","")
            if "Observer" in __key and 'Variable' in __keys:
                self._observerIndex += 1
                __key += "_%i"%self._observerIndex
            __text += "%s['%s'] = {"%(self._objname,str(__key))
            for k in __keys:
                __v = __local[k]
                if __v is None: continue
                if   k == "Checked" and not __v: continue
                if   k == "Stored"  and not __v: continue
                if   k == "AvoidRC" and __v: continue
                if   k == "noDetails": continue
                if isinstance(__v,Persistence.Persistence): __v = __v.values()
                if callable(__v): __text = self._missing%__v.__name__+__text
                if isinstance(__v,dict):
                    for val in __v.values():
                        if callable(val): __text = self._missing%val.__name__+__text
                numpy.set_printoptions(precision=15,threshold=1000000,linewidth=1000*15)
                __text += "'%s':%s, "%(k,repr(__v))
                numpy.set_printoptions(precision=8,threshold=1000,linewidth=75)
            __text.rstrip(", ").rstrip()
            __text += "}"
            if __text[-2:] == "{}": return # Supprime les *Debug et les variables
            self._addLine(__text)
    def _extract(self, __content=""):
        "Transformation un enregistrement en une commande individuelle"
        __is_case = False
        __commands = []
        __content = __content.replace("\r\n","\n")
        exec(__content)
        self._objdata = None
        __getlocals = locals()
        for k in __getlocals:
            try:
                if 'AlgorithmParameters' in __getlocals[k] and type(__getlocals[k]) is dict:
                    self._objname = k
                    self._objdata = __getlocals[k]
            except:
                continue
        if self._objdata is None:
            raise ValueError("Impossible to load given content as a ADAO DCT one (no 'AlgorithmParameters' key found).")
        for k in self._objdata:
            if 'Observer_' in k:
                __command = k.split('_',1)[0]
            else:
                __command = k
            __arguments = ["%s = %s"%(k,repr(v)) for k,v in self._objdata[k].items()]
            __commands.append( "set( Concept='%s', %s )"%(__command, ", ".join(__arguments)))
        __commands.sort() # Pour commencer par 'AlgorithmParameters'
        return __commands

class _SCDViewer(GenericCaseViewer):
    """
    Etablissement des commandes d'un cas SCD (Study Config Dictionary)
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content)
        self._addLine("# -*- coding: utf-8 -*-")
        self._addLine("#\n# Input for ADAO converter to YACS\n#")
        self._addLine("from numpy import array, matrix")
        self._addLine("#")
        self._addLine("study_config = {}")
        self._addLine("study_config['StudyType'] = 'ASSIMILATION_STUDY'")
        self._addLine("study_config['Name'] = '%s'"%self._name)
        self._addLine("observers = {}")
        self._addLine("study_config['Observers'] = observers")
        self._addLine("#")
        self._addLine("inputvariables_config = {}")
        self._addLine("inputvariables_config['Order'] =['adao_default']")
        self._addLine("inputvariables_config['adao_default'] = -1")
        self._addLine("study_config['InputVariables'] = inputvariables_config")
        self._addLine("#")
        self._addLine("outputvariables_config = {}")
        self._addLine("outputvariables_config['Order'] = ['adao_default']")
        self._addLine("outputvariables_config['adao_default'] = -1")
        self._addLine("study_config['OutputVariables'] = outputvariables_config")
        if __content is not None:
            for command in __content:
                self._append(*command)
    def _append(self, __command=None, __keys=None, __local=None, __pre=None, __switchoff=False):
        "Transformation d'une commande individuelle en un enregistrement"
        if __command == "set": __command = __local["Concept"]
        else:                  __command = __command.replace("set", "", 1)
        #
        __text  = None
        if __command in (None, 'execute', 'executePythonScheme', 'executeYACSScheme', 'get'):
            return
        elif __command in ['Debug', 'setDebug']:
            __text  = "#\nstudy_config['Debug'] = '1'"
        elif __command in ['NoDebug', 'setNoDebug']:
            __text  = "#\nstudy_config['Debug'] = '0'"
        elif __command in ['Observer', 'setObserver']:
            __obs   = __local['Variable']
            self._numobservers += 1
            __text  = "#\n"
            __text += "observers['%s'] = {}\n"%__obs
            if __local['String'] is not None:
                __text += "observers['%s']['nodetype'] = '%s'\n"%(__obs, 'String')
                __text += "observers['%s']['String'] = \"\"\"%s\"\"\"\n"%(__obs, __local['String'])
            if __local['Script'] is not None:
                __text += "observers['%s']['nodetype'] = '%s'\n"%(__obs, 'Script')
                __text += "observers['%s']['Script'] = \"%s\"\n"%(__obs, __local['Script'])
            if __local['Template'] is not None and __local['Template'] in Templates.ObserverTemplates:
                __text += "observers['%s']['nodetype'] = '%s'\n"%(__obs, 'String')
                __text += "observers['%s']['String'] = \"\"\"%s\"\"\"\n"%(__obs, Templates.ObserverTemplates[__local['Template']])
            if __local['Info'] is not None:
                __text += "observers['%s']['info'] = \"\"\"%s\"\"\"\n"%(__obs, __local['Info'])
            else:
                __text += "observers['%s']['info'] = \"\"\"%s\"\"\"\n"%(__obs, __obs)
            __text += "observers['%s']['number'] = %s"%(__obs, self._numobservers)
        elif __local is not None: # __keys is not None and
            numpy.set_printoptions(precision=15,threshold=1000000,linewidth=1000*15)
            __text  = "#\n"
            __text += "%s_config = {}\n"%__command
            if 'self' in __local: __local.pop('self')
            __to_be_removed = []
            for __k,__v in __local.items():
                if __v is None: __to_be_removed.append(__k)
            for __k in __to_be_removed:
                __local.pop(__k)
            for __k,__v in __local.items():
                if __k == "Concept": continue
                if __k in ['ScalarSparseMatrix','DiagonalSparseMatrix','Matrix','OneFunction','ThreeFunctions'] and 'Script' in __local: continue
                if __k == 'Algorithm':
                    __text += "study_config['Algorithm'] = %s\n"%(repr(__v))
                elif __k == 'Script':
                    __k = 'Vector'
                    __f = 'Script'
                    __v = "'"+repr(__v)+"'"
                    for __lk in ['ScalarSparseMatrix','DiagonalSparseMatrix','Matrix']:
                        if __lk in __local and __local[__lk]: __k = __lk
                    if __command == "AlgorithmParameters": __k = "Dict"
                    if 'OneFunction' in __local and __local['OneFunction']:
                        __text += "%s_ScriptWithOneFunction = {}\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['Script'] = {}\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['Script']['Direct'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithOneFunction['Script']['Tangent'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithOneFunction['Script']['Adjoint'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithOneFunction['DifferentialIncrement'] = 1e-06\n"%(__command,)
                        __text += "%s_ScriptWithOneFunction['CenteredFiniteDifference'] = 0\n"%(__command,)
                        __k = 'Function'
                        __f = 'ScriptWithOneFunction'
                        __v = '%s_ScriptWithOneFunction'%(__command,)
                    if 'ThreeFunctions' in __local and __local['ThreeFunctions']:
                        __text += "%s_ScriptWithFunctions = {}\n"%(__command,)
                        __text += "%s_ScriptWithFunctions['Function'] = ['Direct', 'Tangent', 'Adjoint']\n"%(__command,)
                        __text += "%s_ScriptWithFunctions['Script'] = {}\n"%(__command,)
                        __text += "%s_ScriptWithFunctions['Script']['Direct'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithFunctions['Script']['Tangent'] = %s\n"%(__command,__v)
                        __text += "%s_ScriptWithFunctions['Script']['Adjoint'] = %s\n"%(__command,__v)
                        __k = 'Function'
                        __f = 'ScriptWithFunctions'
                        __v = '%s_ScriptWithFunctions'%(__command,)
                    __text += "%s_config['Type'] = '%s'\n"%(__command,__k)
                    __text += "%s_config['From'] = '%s'\n"%(__command,__f)
                    __text += "%s_config['Data'] = %s\n"%(__command,__v)
                    __text = __text.replace("''","'")
                elif __k in ('Stored', 'Checked'):
                    if bool(__v):
                        __text += "%s_config['%s'] = '%s'\n"%(__command,__k,int(bool(__v)))
                elif __k in ('AvoidRC', 'noDetails'):
                    if not bool(__v):
                        __text += "%s_config['%s'] = '%s'\n"%(__command,__k,int(bool(__v)))
                else:
                    if __k == 'Parameters': __k = "Dict"
                    if isinstance(__v,Persistence.Persistence): __v = __v.values()
                    if callable(__v): __text = self._missing%__v.__name__+__text
                    if isinstance(__v,dict):
                        for val in __v.values():
                            if callable(val): __text = self._missing%val.__name__+__text
                    __text += "%s_config['Type'] = '%s'\n"%(__command,__k)
                    __text += "%s_config['From'] = '%s'\n"%(__command,'String')
                    __text += "%s_config['Data'] = \"\"\"%s\"\"\"\n"%(__command,repr(__v))
            __text += "study_config['%s'] = %s_config"%(__command,__command)
            numpy.set_printoptions(precision=8,threshold=1000,linewidth=75)
            if __switchoff:
                self._switchoff = True
        if __text is not None: self._addLine(__text)
        if not __switchoff:
            self._switchoff = False
    def _finalize(self):
        self.__loadVariablesByScript()
        self._addLine("#")
        self._addLine("Analysis_config = {}")
        self._addLine("Analysis_config['From'] = 'String'")
        self._addLine("Analysis_config['Data'] = \"\"\"import numpy")
        self._addLine("xa=numpy.ravel(ADD.get('Analysis')[-1])")
        self._addLine("print 'Analysis:',xa\"\"\"")
        self._addLine("study_config['UserPostAnalysis'] = Analysis_config")
    def __loadVariablesByScript(self):
        __ExecVariables = {} # Necessaire pour recuperer la variable
        exec("\n".join(self._lineSerie), __ExecVariables)
        study_config = __ExecVariables['study_config']
        self.__hasAlgorithm = bool(study_config['Algorithm'])
        if not self.__hasAlgorithm and \
                "AlgorithmParameters" in study_config and \
                isinstance(study_config['AlgorithmParameters'], dict) and \
                "From" in study_config['AlgorithmParameters'] and \
                "Data" in study_config['AlgorithmParameters'] and \
                study_config['AlgorithmParameters']['From'] == 'Script':
            __asScript = study_config['AlgorithmParameters']['Data']
            __var = ImportFromScript(__asScript).getvalue( "Algorithm" )
            __text = "#\nstudy_config['Algorithm'] = '%s'"%(__var,)
            self._addLine(__text)
        if self.__hasAlgorithm and \
                "AlgorithmParameters" in study_config and \
                isinstance(study_config['AlgorithmParameters'], dict) and \
                "From" not in study_config['AlgorithmParameters'] and \
                "Data" not in study_config['AlgorithmParameters']:
            __text  = "#\n"
            __text += "AlgorithmParameters_config['Type'] = 'Dict'\n"
            __text += "AlgorithmParameters_config['From'] = 'String'\n"
            __text += "AlgorithmParameters_config['Data'] = '{}'\n"
            self._addLine(__text)
        del study_config

class _XMLViewer(GenericCaseViewer):
    """
    Etablissement des commandes de creation d'un cas XML
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content)
        raise NotImplementedError()

class _YACSViewer(GenericCaseViewer):
    """
    Etablissement des commandes de creation d'un cas YACS
    """
    def __init__(self, __name="", __objname="case", __content=None):
        "Initialisation et enregistrement de l'entete"
        GenericCaseViewer.__init__(self, __name, __objname, __content)
        self.__internalSCD = _SCDViewer(__name, __objname, __content)
        self._append       = self.__internalSCD._append
    def dump(self, __filename=None):
        "Restitution normalisée des commandes"
        self.__internalSCD._finalize()
        # -----
        if __filename is not None:
            __file    = os.path.abspath(__filename)
            __SCDfile = __file[:__file.rfind(".")] + '_SCD.py'
            __SCDdump = self.__internalSCD.dump(__SCDfile)
        else:
            raise ValueError("A file name has to be given for YACS XML output.")
        # -----
        if not PlatformInfo.has_salome or \
            not PlatformInfo.has_adao:
            raise ImportError("\n\n"+\
                "Unable to get SALOME or ADAO environnement variables.\n"+\
                "Please load the right environnement before trying to use it.\n")
        else:
            if os.path.isfile(__file) or os.path.islink(__file):
                os.remove(__file)
            __converterExe = os.path.join(os.environ["ADAO_ROOT_DIR"], "bin/salome", "AdaoYacsSchemaCreator.py")
            __args = ["python", __converterExe, __SCDfile, __file]
            import subprocess
            __p = subprocess.Popen(__args)
            (__stdoutdata, __stderrdata) = __p.communicate()
            if not os.path.exists(__file):
                __msg  = "An error occured during the ADAO YACS Schema build.\n"
                __msg += "Creator applied on the input file:\n"
                __msg += "  %s\n"%__SCDfile
                __msg += "If SALOME GUI is launched by command line, see errors\n"
                __msg += "details in your terminal.\n"
                raise ValueError(__msg)
            os.remove(__SCDfile)
        # -----
        __fid = open(__file,"r")
        __text = __fid.read()
        __fid.close()
        return __text

# ==============================================================================
class ImportFromScript(object):
    """
    Obtention d'une variable nommee depuis un fichier script importe
    """
    def __init__(self, __filename=None):
        "Verifie l'existence et importe le script"
        self.__filename = __filename.rstrip(".py")
        if self.__filename is None:
            raise ValueError("The name of the file, containing the variable to be read, has to be specified.")
        if not os.path.isfile(str(self.__filename)+".py"):
            raise ValueError("The file containing the variable to be imported doesn't seem to exist. Please check the file. The given file name is:\n  \"%s\""%self.__filename)
        self.__scriptfile = __import__(self.__filename, globals(), locals(), [])
        self.__scriptstring = open(self.__filename+".py",'r').read()
    def getvalue(self, __varname=None, __synonym=None ):
        "Renvoie la variable demandee"
        if __varname is None:
            raise ValueError("The name of the variable to be read has to be specified. Please check the content of the file and the syntax.")
        if not hasattr(self.__scriptfile, __varname):
            if __synonym is None:
                raise ValueError("The imported script file \"%s\" doesn't contain the mandatory variable \"%s\" to be read. Please check the content of the file and the syntax."%(str(self.__filename)+".py",__varname))
            elif not hasattr(self.__scriptfile, __synonym):
                raise ValueError("The imported script file \"%s\" doesn't contain the mandatory variable \"%s\" to be read. Please check the content of the file and the syntax."%(str(self.__filename)+".py",__synonym))
            else:
                return getattr(self.__scriptfile, __synonym)
        else:
            return getattr(self.__scriptfile, __varname)
    def getstring(self):
        "Renvoie le script complet"
        return self.__scriptstring

# ==============================================================================
def CostFunction3D(_x,
                   _Hm  = None,  # Pour simuler Hm(x) : HO["Direct"].appliedTo
                   _HmX = None,  # Simulation déjà faite de Hm(x)
                   _arg = None,  # Arguments supplementaires pour Hm, sous la forme d'un tuple
                   _BI  = None,
                   _RI  = None,
                   _Xb  = None,
                   _Y   = None,
                   _SIV = False, # A résorber pour la 8.0
                   _SSC = [],    # self._parameters["StoreSupplementaryCalculations"]
                   _nPS = 0,     # nbPreviousSteps
                   _QM  = "DA",  # QualityMeasure
                   _SSV = {},    # Entrée et/ou sortie : self.StoredVariables
                   _fRt = False, # Restitue ou pas la sortie étendue
                   _sSc = True,  # Stocke ou pas les SSC
                  ):
    """
    Fonction-coût générale utile pour les algorithmes statiques/3D : 3DVAR, BLUE
    et dérivés, Kalman et dérivés, LeastSquares, SamplingTest, PSO, SA, Tabu,
    DFO, QuantileRegression
    """
    if not _sSc:
        _SIV = False
        _SSC = {}
    else:
        for k in ["CostFunctionJ",
                  "CostFunctionJb",
                  "CostFunctionJo",
                  "CurrentOptimum",
                  "CurrentState",
                  "IndexOfOptimum",
                  "SimulatedObservationAtCurrentOptimum",
                  "SimulatedObservationAtCurrentState",
                 ]:
            if k not in _SSV:
                _SSV[k] = []
            if hasattr(_SSV[k],"store"):
                _SSV[k].append = _SSV[k].store # Pour utiliser "append" au lieu de "store"
    #
    _X  = numpy.asmatrix(numpy.ravel( _x )).T
    if _SIV or "CurrentState" in _SSC or "CurrentOptimum" in _SSC:
        _SSV["CurrentState"].append( _X )
    #
    if _HmX is not None:
        _HX = _HmX
    else:
        if _Hm is None:
            raise ValueError("COSTFUNCTION3D Operator has to be defined.")
        if _arg is None:
            _HX = _Hm( _X )
        else:
            _HX = _Hm( _X, *_arg )
    _HX = numpy.asmatrix(numpy.ravel( _HX )).T
    #
    if "SimulatedObservationAtCurrentState" in _SSC or \
       "SimulatedObservationAtCurrentOptimum" in _SSC:
        _SSV["SimulatedObservationAtCurrentState"].append( _HX )
    #
    if numpy.any(numpy.isnan(_HX)):
        Jb, Jo, J = numpy.nan, numpy.nan, numpy.nan
    else:
        _Y   = numpy.asmatrix(numpy.ravel( _Y )).T
        if _QM in ["AugmentedWeightedLeastSquares", "AWLS", "AugmentedPonderatedLeastSquares", "APLS", "DA"]:
            if _BI is None or _RI is None:
                raise ValueError("Background and Observation error covariance matrix has to be properly defined!")
            _Xb  = numpy.asmatrix(numpy.ravel( _Xb )).T
            Jb  = 0.5 * (_X - _Xb).T * _BI * (_X - _Xb)
            Jo  = 0.5 * (_Y - _HX).T * _RI * (_Y - _HX)
        elif _QM in ["WeightedLeastSquares", "WLS", "PonderatedLeastSquares", "PLS"]:
            if _RI is None:
                raise ValueError("Observation error covariance matrix has to be properly defined!")
            Jb  = 0.
            Jo  = 0.5 * (_Y - _HX).T * _RI * (_Y - _HX)
        elif _QM in ["LeastSquares", "LS", "L2"]:
            Jb  = 0.
            Jo  = 0.5 * (_Y - _HX).T * (_Y - _HX)
        elif _QM in ["AbsoluteValue", "L1"]:
            Jb  = 0.
            Jo  = numpy.sum( numpy.abs(_Y - _HX) )
        elif _QM in ["MaximumError", "ME"]:
            Jb  = 0.
            Jo  = numpy.max( numpy.abs(_Y - _HX) )
        elif _QM in ["QR", "Null"]:
            Jb  = 0.
            Jo  = 0.
        else:
            raise ValueError("Unknown asked quality measure!")
        #
        J   = float( Jb ) + float( Jo )
    #
    if _sSc:
        _SSV["CostFunctionJb"].append( Jb )
        _SSV["CostFunctionJo"].append( Jo )
        _SSV["CostFunctionJ" ].append( J )
    #
    if "IndexOfOptimum" in _SSC or \
       "CurrentOptimum" in _SSC or \
       "SimulatedObservationAtCurrentOptimum" in _SSC:
        IndexMin = numpy.argmin( _SSV["CostFunctionJ"][_nPS:] ) + _nPS
    if "IndexOfOptimum" in _SSC:
        _SSV["IndexOfOptimum"].append( IndexMin )
    if "CurrentOptimum" in _SSC:
        _SSV["CurrentOptimum"].append( _SSV["CurrentState"][IndexMin] )
    if "SimulatedObservationAtCurrentOptimum" in _SSC:
        _SSV["SimulatedObservationAtCurrentOptimum"].append( _SSV["SimulatedObservationAtCurrentState"][IndexMin] )
    #
    if _fRt:
        return _SSV
    else:
        if _QM in ["QR"]: # Pour le QuantileRegression
            return _HX
        else:
            return J

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')
