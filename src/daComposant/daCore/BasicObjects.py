#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2017 EDF R&D
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

import logging, copy
import numpy
import Persistence
import PlatformInfo

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
        for i in xrange(min(len(self.__listOPCV),self.__lenghtOR)-1,-1,-1):
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
    Classe générale d'interface de type opérateur
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
            self.__Method = fromMethod
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

    def appliedControledFormTo(self, (xValue, uValue) ):
        """
        Permet de restituer le résultat de l'application de l'opérateur à une
        paire (xValue, uValue). Cette méthode se contente d'appliquer, son
        argument devant a priori être du bon type. Si la uValue est None,
        on suppose que l'opérateur ne s'applique qu'à xValue.
        Arguments :
        - xValue : argument X adapté pour appliquer l'opérateur
        - uValue : argument U adapté pour appliquer l'opérateur
        """
        if self.__Matrix is not None:
            self.__addOneMatrixCall()
            return self.__Matrix * xValue
        elif uValue is not None:
            self.__addOneMethodCall()
            return self.__Method( (xValue, uValue) )
        else:
            self.__addOneMethodCall()
            return self.__Method( xValue )

    def appliedInXTo(self, (xNominal, xValue) ):
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
        self.StoredVariables = {}
        #
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

    def _pre_run(self, Parameters ):
        "Pré-calcul"
        logging.debug("%s Lancement", self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mio", self._name, self._m.getUsedMemory("Mio"))
        #
        # Mise a jour de self._parameters avec Parameters
        self.__setParameters(Parameters)
        #
        # Corrections et complements
        if self._parameters.has_key("Bounds") and (type(self._parameters["Bounds"]) is type([]) or type(self._parameters["Bounds"]) is type(())) and (len(self._parameters["Bounds"]) > 0):
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
        logging.debug("%s Taille mémoire utilisée de %.1f Mio", self._name, self._m.getUsedMemory("Mio"))
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
        return self.StoredVariables.keys()

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
            ks = self.__required_parameters.keys()
            ks.sort()
            return ks
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
        if asEyeByScalar is not None:
            if numpy.matrix(asEyeByScalar).size != 1:
                raise ValueError('  The diagonal multiplier given to define a sparse matrix is not a unique scalar value.\n  Its actual measured size is %i. Please check your scalar input.'%numpy.matrix(asEyeByScalar).size)
            self.__is_scalar = True
            self.__C         = numpy.abs( float(asEyeByScalar) )
            self.shape       = (0,0)
            self.size        = 0
        elif asEyeByVector is not None:
            self.__is_vector = True
            self.__C         = numpy.abs( numpy.array( numpy.ravel( numpy.matrix(asEyeByVector, float ) ) ) )
            self.shape       = (self.__C.size,self.__C.size)
            self.size        = self.__C.size**2
        elif asCovariance is not None:
            self.__is_matrix = True
            self.__C         = numpy.matrix( asCovariance, float )
            self.shape       = self.__C.shape
            self.size        = self.__C.size
        elif asCovObject is not None:
            self.__is_object = True
            self.__C         = asCovObject
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
        elif self.ismatrix() and (isinstance(other,numpy.ndarray) \
                               or isinstance(other,list) \
                               or isinstance(other,tuple)):
            if numpy.ravel(other).size == self.shape[1]: # Vecteur
                return self.__C * numpy.asmatrix(numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]: # Matrice
                return self.__C * numpy.asmatrix(other)
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.asmatrix(other).shape,self.__name))
        elif self.isvector() and (isinstance(other,numpy.matrix) \
                               or isinstance(other,numpy.ndarray) \
                               or isinstance(other,list) \
                               or isinstance(other,tuple)):
            if numpy.ravel(other).size == self.shape[1]: # Vecteur
                return numpy.asmatrix(self.__C * numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]: # Matrice
                return numpy.asmatrix((self.__C * (numpy.asarray(other).transpose())).transpose())
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.ravel(other).shape,self.__name))
        elif self.isscalar() and isinstance(other,numpy.matrix):
            return self.__C * other
        elif self.isscalar() and (isinstance(other,numpy.ndarray) \
                               or isinstance(other,list) \
                               or isinstance(other,tuple)):
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
