#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2015 EDF R&D
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

"""
    D�finit les outils g�n�raux �l�mentaires.

    Ce module est destin� � etre appel�e par AssimilationStudy pour constituer
    les objets �l�mentaires de l'algorithme.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import logging, copy
import numpy
import Persistence
import PlatformInfo

# ==============================================================================
class CacheManager:
    """
    Classe g�n�rale de gestion d'un cache de calculs
    """
    def __init__(self,
            toleranceInRedundancy = 1.e-18,
            lenghtOfRedundancy    = -1,
            ):
        """
        Les caract�ristiques de tol�rance peuvent �tre modif�es � la cr�ation.
        """
        self.__tolerBP  = float(toleranceInRedundancy)
        self.__lenghtOR = int(lenghtOfRedundancy)
        self.clearCache()

    def clearCache(self):
        self.__listOPCV = [] # Operator Previous Calculated Points, Results, Point Norms
        # logging.debug("CM Tolerance de determination des doublons : %.2e"%self.__tolerBP)

    def wasCalculatedIn(self, xValue ): #, info="" ):
        __alc = False
        __HxV = None
        for i in xrange(min(len(self.__listOPCV),self.__lenghtOR)-1,-1,-1):
            if xValue.size != self.__listOPCV[i][0].size:
                # logging.debug("CM Diff�rence de la taille %s de X et de celle %s du point %i d�j� calcul�"%(xValue.shape,i,self.__listOPCP[i].shape))
                continue
            if numpy.linalg.norm(numpy.ravel(xValue) - self.__listOPCV[i][0]) < self.__tolerBP * self.__listOPCV[i][2]:
                __alc  = True
                __HxV = self.__listOPCV[i][1]
                # logging.debug("CM Cas%s d�ja calcul�, portant le num�ro %i"%(info,i))
                break
        return __alc, __HxV

    def storeValueInX(self, xValue, HxValue ):
        if self.__lenghtOR < 0: self.__lenghtOR = 2 * xValue.size + 2
        while len(self.__listOPCV) > self.__lenghtOR:
            # logging.debug("CM R�duction de la liste des cas � %i �l�ments par suppression du premier"%self.__lenghtOR)
            self.__listOPCV.pop(0)
        self.__listOPCV.append( (
            copy.copy(numpy.ravel(xValue)),
            copy.copy(HxValue),
            numpy.linalg.norm(xValue),
            ) )

# ==============================================================================
class Operator:
    """
    Classe g�n�rale d'interface de type op�rateur
    """
    NbCallsAsMatrix = 0
    NbCallsAsMethod = 0
    NbCallsOfCached = 0
    CM = CacheManager()
    #
    def __init__(self, fromMethod=None, fromMatrix=None, avoidingRedundancy = True):
        """
        On construit un objet de ce type en fournissant � l'aide de l'un des
        deux mots-cl�, soit une fonction python, soit une matrice.
        Arguments :
        - fromMethod : argument de type fonction Python
        - fromMatrix : argument adapt� au constructeur numpy.matrix
        - avoidingRedundancy : �vite ou pas les calculs redondants
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

    def isType(self):
        return self.__Type

    def appliedTo(self, xValue):
        """
        Permet de restituer le r�sultat de l'application de l'op�rateur � un
        argument xValue. Cette m�thode se contente d'appliquer, son argument
        devant a priori �tre du bon type.
        Arguments :
        - xValue : argument adapt� pour appliquer l'op�rateur
        """
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
        Permet de restituer le r�sultat de l'application de l'op�rateur � une
        paire (xValue, uValue). Cette m�thode se contente d'appliquer, son
        argument devant a priori �tre du bon type. Si la uValue est None,
        on suppose que l'op�rateur ne s'applique qu'� xValue.
        Arguments :
        - xValue : argument X adapt� pour appliquer l'op�rateur
        - uValue : argument U adapt� pour appliquer l'op�rateur
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
        Permet de restituer le r�sultat de l'application de l'op�rateur � un
        argument xValue, sachant que l'op�rateur est valable en xNominal.
        Cette m�thode se contente d'appliquer, son argument devant a priori
        �tre du bon type. Si l'op�rateur est lin�aire car c'est une matrice,
        alors il est valable en tout point nominal et il n'est pas n�cessaire
        d'utiliser xNominal.
        Arguments : une liste contenant
        - xNominal : argument permettant de donner le point o� l'op�rateur
          est construit pour etre ensuite appliqu�
        - xValue : argument adapt� pour appliquer l'op�rateur
        """
        if self.__Matrix is not None:
            self.__addOneMatrixCall()
            return self.__Matrix * xValue
        else:
            self.__addOneMethodCall()
            return self.__Method( (xNominal, xValue) )

    def asMatrix(self, ValueForMethodForm = "UnknownVoidValue"):
        """
        Permet de renvoyer l'op�rateur sous la forme d'une matrice
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
        Renvoie la taille sous forme numpy si l'op�rateur est disponible sous
        la forme d'une matrice
        """
        if self.__Matrix is not None:
            return self.__Matrix.shape
        else:
            raise ValueError("Matrix form of the operator is not available, nor the shape")

    def nbcalls(self, which=None):
        """
        Renvoie les nombres d'�valuations de l'op�rateur
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
        self.__NbCallsAsMatrix   += 1 # Decompte local
        Operator.NbCallsAsMatrix += 1 # Decompte global

    def __addOneMethodCall(self):
        self.__NbCallsAsMethod   += 1 # Decompte local
        Operator.NbCallsAsMethod += 1 # Decompte global

    def __addOneCacheCall(self):
        self.__NbCallsOfCached   += 1 # Decompte local
        Operator.NbCallsOfCached += 1 # Decompte global

# ==============================================================================
class Algorithm:
    """
    Classe g�n�rale d'interface de type algorithme

    Elle donne un cadre pour l'�criture d'une classe �l�mentaire d'algorithme
    d'assimilation, en fournissant un container (dictionnaire) de variables
    persistantes initialis�es, et des m�thodes d'acc�s � ces variables stock�es.

    Une classe �l�mentaire d'algorithme doit impl�menter la m�thode "run".
    """
    def __init__(self, name):
        """
        L'initialisation pr�sente permet de fabriquer des variables de stockage
        disponibles de mani�re g�n�rique dans les algorithmes �l�mentaires. Ces
        variables de stockage sont ensuite conserv�es dans un dictionnaire
        interne � l'objet, mais auquel on acc�de par la m�thode "get".

        Les variables pr�vues sont :
            - CostFunctionJ  : fonction-cout globale, somme des deux parties suivantes
            - CostFunctionJb : partie �bauche ou background de la fonction-cout
            - CostFunctionJo : partie observations de la fonction-cout
            - GradientOfCostFunctionJ  : gradient de la fonction-cout globale
            - GradientOfCostFunctionJb : gradient de la partie �bauche de la fonction-cout
            - GradientOfCostFunctionJo : gradient de la partie observations de la fonction-cout
            - CurrentState : �tat courant lors d'it�rations
            - Analysis : l'analyse Xa
            - SimulatedObservationAtBackground : l'�tat observ� H(Xb) � l'�bauche
            - SimulatedObservationAtCurrentState : l'�tat observ� H(X) � l'�tat courant
            - SimulatedObservationAtOptimum : l'�tat observ� H(Xa) � l'optimum
            - Innovation : l'innovation : d = Y - H(X)
            - SigmaObs2 : indicateur de correction optimale des erreurs d'observation
            - SigmaBck2 : indicateur de correction optimale des erreurs d'�bauche
            - MahalanobisConsistency : indicateur de consistance des covariances
            - OMA : Observation moins Analysis : Y - Xa
            - OMB : Observation moins Background : Y - Xb
            - AMB : Analysis moins Background : Xa - Xb
            - APosterioriCovariance : matrice A
            - APosterioriVariances : variances de la matrice A
            - APosterioriStandardDeviations : �cart-types de la matrice A
            - APosterioriCorrelations : correlations de la matrice A
        On peut rajouter des variables � stocker dans l'initialisation de
        l'algorithme �l�mentaire qui va h�riter de cette classe
        """
        logging.debug("%s Initialisation"%str(name))
        self._m = PlatformInfo.SystemUsage()
        #
        self._name = str( name )
        self._parameters = {"StoreSupplementaryCalculations":[]}
        self.__required_parameters = {}
        self.StoredVariables = {}
        #
        self.StoredVariables["CostFunctionJ"]                      = Persistence.OneScalar(name = "CostFunctionJ")
        self.StoredVariables["CostFunctionJb"]                     = Persistence.OneScalar(name = "CostFunctionJb")
        self.StoredVariables["CostFunctionJo"]                     = Persistence.OneScalar(name = "CostFunctionJo")
        self.StoredVariables["GradientOfCostFunctionJ"]            = Persistence.OneVector(name = "GradientOfCostFunctionJ")
        self.StoredVariables["GradientOfCostFunctionJb"]           = Persistence.OneVector(name = "GradientOfCostFunctionJb")
        self.StoredVariables["GradientOfCostFunctionJo"]           = Persistence.OneVector(name = "GradientOfCostFunctionJo")
        self.StoredVariables["CurrentState"]                       = Persistence.OneVector(name = "CurrentState")
        self.StoredVariables["Analysis"]                           = Persistence.OneVector(name = "Analysis")
        self.StoredVariables["SimulatedObservationAtBackground"]   = Persistence.OneVector(name = "SimulatedObservationAtBackground")
        self.StoredVariables["SimulatedObservationAtCurrentState"] = Persistence.OneVector(name = "SimulatedObservationAtCurrentState")
        self.StoredVariables["SimulatedObservationAtOptimum"]      = Persistence.OneVector(name = "SimulatedObservationAtOptimum")
        self.StoredVariables["Innovation"]                         = Persistence.OneVector(name = "Innovation")
        self.StoredVariables["SigmaObs2"]                          = Persistence.OneScalar(name = "SigmaObs2")
        self.StoredVariables["SigmaBck2"]                          = Persistence.OneScalar(name = "SigmaBck2")
        self.StoredVariables["MahalanobisConsistency"]             = Persistence.OneScalar(name = "MahalanobisConsistency")
        self.StoredVariables["OMA"]                                = Persistence.OneVector(name = "OMA")
        self.StoredVariables["OMB"]                                = Persistence.OneVector(name = "OMB")
        self.StoredVariables["BMA"]                                = Persistence.OneVector(name = "BMA")
        self.StoredVariables["APosterioriCovariance"]              = Persistence.OneMatrix(name = "APosterioriCovariance")
        self.StoredVariables["APosterioriVariances"]               = Persistence.OneVector(name = "APosterioriVariances")
        self.StoredVariables["APosterioriStandardDeviations"]      = Persistence.OneVector(name = "APosterioriStandardDeviations")
        self.StoredVariables["APosterioriCorrelations"]            = Persistence.OneMatrix(name = "APosterioriCorrelations")
        self.StoredVariables["SimulationQuantiles"]                = Persistence.OneMatrix(name = "SimulationQuantiles")

    def _pre_run(self):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille m�moire utilis�e de %.1f Mio"%(self._name, self._m.getUsedMemory("Mio")))
        return 0

    def _post_run(self,_oH=None):
        if self._parameters.has_key("StoreSupplementaryCalculations") and \
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
            logging.debug("%s Nombre d'�valuation(s) de l'op�rateur d'observation direct/tangent/adjoint.: %i/%i/%i"%(self._name, _oH["Direct"].nbcalls(0),_oH["Tangent"].nbcalls(0),_oH["Adjoint"].nbcalls(0)))
            logging.debug("%s Nombre d'appels au cache d'op�rateur d'observation direct/tangent/adjoint..: %i/%i/%i"%(self._name, _oH["Direct"].nbcalls(3),_oH["Tangent"].nbcalls(3),_oH["Adjoint"].nbcalls(3)))
        logging.debug("%s Taille m�moire utilis�e de %.1f Mio"%(self._name, self._m.getUsedMemory("Mio")))
        logging.debug("%s Termin�"%self._name)
        return 0

    def get(self, key=None):
        """
        Renvoie l'une des variables stock�es identifi�e par la cl�, ou le
        dictionnaire de l'ensemble des variables disponibles en l'absence de
        cl�. Ce sont directement les variables sous forme objet qui sont
        renvoy�es, donc les m�thodes d'acc�s � l'objet individuel sont celles
        des classes de persistance.
        """
        if key is not None:
            return self.StoredVariables[key]
        else:
            return self.StoredVariables

    def has_key(self, key=None):
        """
        V�rifie si l'une des variables stock�es est identifi�e par la cl�.
        """
        return self.StoredVariables.has_key(key)

    def keys(self):
        """
        Renvoie la liste des cl�s de variables stock�es.
        """
        return self.StoredVariables.keys()

    def run(self, Xb=None, Y=None, H=None, M=None, R=None, B=None, Q=None, Parameters=None):
        """
        Doit impl�menter l'op�ration �l�mentaire de calcul d'assimilation sous
        sa forme math�matique la plus naturelle possible.
        """
        raise NotImplementedError("Mathematical assimilation calculation has not been implemented!")

    def defineRequiredParameter(self, name = None, default = None, typecast = None, message = None, minval = None, maxval = None, listval = None):
        """
        Permet de d�finir dans l'algorithme des param�tres requis et leurs
        caract�ristiques par d�faut.
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
        logging.debug("%s %s (valeur par d�faut = %s)"%(self._name, message, self.setParameterValue(name)))

    def getRequiredParameters(self, noDetails=True):
        """
        Renvoie la liste des noms de param�tres requis ou directement le
        dictionnaire des param�tres requis.
        """
        if noDetails:
            ks = self.__required_parameters.keys()
            ks.sort()
            return ks
        else:
            return self.__required_parameters

    def setParameterValue(self, name=None, value=None):
        """
        Renvoie la valeur d'un param�tre requis de mani�re contr�l�e
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
            if typecast is list or typecast is tuple or type(__val) is list or type(__val) is tuple:
                for v in __val:
                    if v not in listval:
                        raise ValueError("The value \"%s\" of the parameter named \"%s\" is not allowed, it has to be in the list %s."%(v, name, listval))
            elif __val not in listval:
                raise ValueError("The value \"%s\" of the parameter named \"%s\" is not allowed, it has to be in the list %s."%( __val, name,listval))
        return __val

    def setParameters(self, fromDico={}):
        """
        Permet de stocker les param�tres re�us dans le dictionnaire interne.
        """
        self._parameters.update( fromDico )
        for k in self.__required_parameters.keys():
            if k in fromDico.keys():
                self._parameters[k] = self.setParameterValue(k,fromDico[k])
            else:
                self._parameters[k] = self.setParameterValue(k)
            logging.debug("%s %s : %s"%(self._name, self.__required_parameters[k]["message"], self._parameters[k]))

# ==============================================================================
class Diagnostic:
    """
    Classe g�n�rale d'interface de type diagnostic

    Ce template s'utilise de la mani�re suivante : il sert de classe "patron" en
    m�me temps que l'une des classes de persistance, comme "OneScalar" par
    exemple.

    Une classe �l�mentaire de diagnostic doit impl�menter ses deux m�thodes, la
    m�thode "_formula" pour �crire explicitement et proprement la formule pour
    l'�criture math�matique du calcul du diagnostic (m�thode interne non
    publique), et "calculate" pour activer la pr�c�dente tout en ayant v�rifi�
    et pr�par� les donn�es, et pour stocker les r�sultats � chaque pas (m�thode
    externe d'activation).
    """
    def __init__(self, name = "", parameters = {}):
        self.name       = str(name)
        self.parameters = dict( parameters )

    def _formula(self, *args):
        """
        Doit impl�menter l'op�ration �l�mentaire de diagnostic sous sa forme
        math�matique la plus naturelle possible.
        """
        raise NotImplementedError("Diagnostic mathematical formula has not been implemented!")

    def calculate(self, *args):
        """
        Active la formule de calcul avec les arguments correctement rang�s
        """
        raise NotImplementedError("Diagnostic activation method has not been implemented!")

# ==============================================================================
class Covariance:
    """
    Classe g�n�rale d'interface de type covariance
    """
    def __init__(self,
            name          = "GenericCovariance",
            asCovariance  = None,
            asEyeByScalar = None,
            asEyeByVector = None,
            asCovObject   = None,
            ):
        """
        Permet de d�finir une covariance :
        - asCovariance : entr�e des donn�es, comme une matrice compatible avec
          le constructeur de numpy.matrix
        - asEyeByScalar : entr�e des donn�es comme un seul scalaire de variance,
          multiplicatif d'une matrice de corr�lation identit�, aucune matrice
          n'�tant donc explicitement � donner
        - asEyeByVector : entr�e des donn�es comme un seul vecteur de variance,
          � mettre sur la diagonale d'une matrice de corr�lation, aucune matrice
          n'�tant donc explicitement � donner
        - asCovObject : entr�e des donn�es comme un objet python, qui a les
          methodes obligatoires "getT", "getI", "diag", "trace", "__add__",
          "__sub__", "__neg__", "__mul__", "__rmul__" et facultatives "shape",
          "size", "cholesky", "choleskyI", "asfullmatrix", "__repr__", "__str__"
        """
        self.__name       = str(name)
        #
        self.__C          = None
        self.__is_scalar  = False
        self.__is_vector  = False
        self.__is_matrix  = False
        self.__is_object  = False
        if asEyeByScalar is not None:
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
        if self.ismatrix() and min(self.shape) != max(self.shape):
            raise ValueError("The given matrix for %s is not a square one, its shape is %s. Please check your matrix input."%(self.__name,self.shape))
        if self.isobject() and min(self.shape) != max(self.shape):
            raise ValueError("The matrix given for \"%s\" is not a square one, its shape is %s. Please check your object input."%(self.__name,self.shape))
        if self.isscalar() and self.__C <= 0:
            raise ValueError("The \"%s\" covariance matrix is not positive-definite. Please check your scalar input %s."%(self.__name,self.__C))
        if self.isvector() and (self.__C <= 0).any():
            raise ValueError("The \"%s\" covariance matrix is not positive-definite. Please check your vector input."%(self.__name,))
        if self.ismatrix() and logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
            try:
                L = numpy.linalg.cholesky( self.__C )
            except:
                raise ValueError("The %s covariance matrix is not symmetric positive-definite. Please check your matrix input."%(self.__name,))

    def isscalar(self):
        return self.__is_scalar

    def isvector(self):
        return self.__is_vector

    def ismatrix(self):
        return self.__is_matrix

    def isobject(self):
        return self.__is_object

    def getI(self):
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
        if   self.ismatrix():
            return Covariance(self.__name+"T", asCovariance  = self.__C.T )
        elif self.isvector():
            return Covariance(self.__name+"T", asEyeByVector = self.__C )
        elif self.isscalar():
            return Covariance(self.__name+"T", asEyeByScalar = self.__C )
        elif self.isobject():
            return Covariance(self.__name+"T", asCovObject   = self.__C.getT() )

    def cholesky(self):
        if   self.ismatrix():
            return Covariance(self.__name+"C", asCovariance  = numpy.linalg.cholesky(self.__C) )
        elif self.isvector():
            return Covariance(self.__name+"C", asEyeByVector = numpy.sqrt( self.__C ) )
        elif self.isscalar():
            return Covariance(self.__name+"C", asEyeByScalar = numpy.sqrt( self.__C ) )
        elif self.isobject() and hasattr(self.__C,"cholesky"):
            return Covariance(self.__name+"C", asCovObject   = self.__C.cholesky() )

    def choleskyI(self):
        if   self.ismatrix():
            return Covariance(self.__name+"H", asCovariance  = numpy.linalg.cholesky(self.__C).I )
        elif self.isvector():
            return Covariance(self.__name+"H", asEyeByVector = 1.0 / numpy.sqrt( self.__C ) )
        elif self.isscalar():
            return Covariance(self.__name+"H", asEyeByScalar = 1.0 / numpy.sqrt( self.__C ) )
        elif self.isobject() and hasattr(self.__C,"choleskyI"):
            return Covariance(self.__name+"H", asCovObject   = self.__C.choleskyI() )

    def diag(self, msize=None):
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
        return repr(self.__C)

    def __str__(self):
        return str(self.__C)

    def __add__(self, other):
        if   self.ismatrix() or self.isobject():
            return self.__C + numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            _A.reshape(_A.size)[::_A.shape[1]+1] += self.__C
            return numpy.asmatrix(_A)

    def __radd__(self, other):
        raise NotImplementedError("%s covariance matrix __radd__ method not available for %s type!"%(self.__name,type(other)))

    def __sub__(self, other):
        if   self.ismatrix() or self.isobject():
            return self.__C - numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            _A.reshape(_A.size)[::_A.shape[1]+1] = self.__C - _A.reshape(_A.size)[::_A.shape[1]+1]
            return numpy.asmatrix(_A)

    def __rsub__(self, other):
        raise NotImplementedError("%s covariance matrix __rsub__ method not available for %s type!"%(self.__name,type(other)))

    def __neg__(self):
        return - self.__C

    def __mul__(self, other):
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
        return self.shape[0]

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
