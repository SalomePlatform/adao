#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2013 EDF R&D
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
    D�finit les outils g�n�raux �l�mentaires.
    
    Ce module est destin� � etre appel�e par AssimilationStudy pour constituer
    les objets �l�mentaires de l'algorithme.
"""
__author__ = "Jean-Philippe ARGAUD"

import logging
import numpy
import Persistence

# ==============================================================================
class Operator:
    """
    Classe g�n�rale d'interface de type op�rateur
    """
    def __init__(self, fromMethod=None, fromMatrix=None):
        """
        On construit un objet de ce type en fournissant � l'aide de l'un des
        deux mots-cl�, soit une fonction python, soit matrice.
        Arguments :
        - fromMethod : argument de type fonction Python
        - fromMatrix : argument adapt� au constructeur numpy.matrix
        """
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
        if self.__Matrix is not None:
            return self.__Matrix * xValue
        else:
            return self.__Method( xValue )

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
            return self.__Matrix * xValue
        elif uValue is not None:
            return self.__Method( (xValue, uValue) )
        else:
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
            return self.__Matrix * xValue
        else:
            return self.__Method( (xNominal, xValue) )

    def asMatrix(self, ValueForMethodForm = "UnknownVoidValue"):
        """
        Permet de renvoyer l'op�rateur sous la forme d'une matrice
        """
        if self.__Matrix is not None:
            return self.__Matrix
        elif ValueForMethodForm is not "UnknownVoidValue": # Ne pas utiliser "None"
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
            - Analysis : l'analyse
            - Innovation : l'innovation : d = Y - H Xb
            - SigmaObs2 : indicateur de correction optimale des erreurs d'observation
            - SigmaBck2 : indicateur de correction optimale des erreurs d'�bauche
            - MahalanobisConsistency : indicateur de consistance des covariances
            - OMA : Observation moins Analysis : Y - Xa
            - OMB : Observation moins Background : Y - Xb
            - AMB : Analysis moins Background : Xa - Xb
            - APosterioriCovariance : matrice A
        On peut rajouter des variables � stocker dans l'initialisation de
        l'algorithme �l�mentaire qui va h�riter de cette classe
        """
        logging.debug("%s Initialisation"%str(name))
        self._name = str( name )
        self._parameters = {}
        self.__required_parameters = {}
        self.StoredVariables = {}
        #
        self.StoredVariables["CostFunctionJ"]            = Persistence.OneScalar(name = "CostFunctionJ")
        self.StoredVariables["CostFunctionJb"]           = Persistence.OneScalar(name = "CostFunctionJb")
        self.StoredVariables["CostFunctionJo"]           = Persistence.OneScalar(name = "CostFunctionJo")
        self.StoredVariables["GradientOfCostFunctionJ"]  = Persistence.OneVector(name = "GradientOfCostFunctionJ")
        self.StoredVariables["GradientOfCostFunctionJb"] = Persistence.OneVector(name = "GradientOfCostFunctionJb")
        self.StoredVariables["GradientOfCostFunctionJo"] = Persistence.OneVector(name = "GradientOfCostFunctionJo")
        self.StoredVariables["CurrentState"]             = Persistence.OneVector(name = "CurrentState")
        self.StoredVariables["Analysis"]                 = Persistence.OneVector(name = "Analysis")
        self.StoredVariables["Innovation"]               = Persistence.OneVector(name = "Innovation")
        self.StoredVariables["SigmaObs2"]                = Persistence.OneScalar(name = "SigmaObs2")
        self.StoredVariables["SigmaBck2"]                = Persistence.OneScalar(name = "SigmaBck2")
        self.StoredVariables["MahalanobisConsistency"]   = Persistence.OneScalar(name = "MahalanobisConsistency")
        self.StoredVariables["OMA"]                      = Persistence.OneVector(name = "OMA")
        self.StoredVariables["OMB"]                      = Persistence.OneVector(name = "OMB")
        self.StoredVariables["BMA"]                      = Persistence.OneVector(name = "BMA")
        self.StoredVariables["APosterioriCovariance"]    = Persistence.OneMatrix(name = "APosterioriCovariance")

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
        if minval is not None and __val < minval:
            raise ValueError("The parameter named \"%s\" of value \"%s\" can not be less than %s."%(name, __val, minval))
        if maxval is not None and __val > maxval:
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
        """
        self.__name       = str(name)
        #
        self.__B          = None
        self.__is_scalar  = False
        self.__is_vector  = False
        self.__is_matrix  = False
        if asEyeByScalar is not None:
            self.__is_scalar = True
            self.__B         = numpy.abs( float(asEyeByScalar) )
            self.shape       = (0,0)
            self.size        = 0
        elif asEyeByVector is not None:
            self.__is_vector = True
            self.__B         = numpy.abs( numpy.array( numpy.ravel( asEyeByVector ), float ) )
            self.shape       = (self.__B.size,self.__B.size)
            self.size        = self.__B.size**2
        elif asCovariance is not None:
            self.__is_matrix = True
            self.__B         = numpy.matrix( asCovariance, float )
            self.shape       = self.__B.shape
            self.size        = self.__B.size
        else:
            pass
            # raise ValueError("The %s covariance matrix has to be specified either as a matrix, a vector for its diagonal or a scalar multiplying an identity matrix."%self.__name)
        #
        self.__validate()
    
    def __validate(self):
        if self.ismatrix() and min(self.shape) != max(self.shape):
            raise ValueError("The given matrix for %s is not a square one, its shape is %s. Please check your matrix input."%(self.__name,self.shape))
        if self.isscalar() and self.__B <= 0:
            raise ValueError("The %s covariance matrix is not positive-definite. Please check your scalar input %s."%(self.__name,self.__B_scalar))
        if self.isvector() and (self.__B <= 0).any():
            raise ValueError("The %s covariance matrix is not positive-definite. Please check your vector input."%(self.__name,))
        if self.ismatrix() and logging.getLogger().level < logging.WARNING: # La verification n'a lieu qu'en debug
            try:
                L = numpy.linalg.cholesky( self.__B )
            except:
                raise ValueError("The %s covariance matrix is not symmetric positive-definite. Please check your matrix input."%(self.__name,))
        
    def isscalar(self):
        return self.__is_scalar
    
    def isvector(self):
        return self.__is_vector
    
    def ismatrix(self):
        return self.__is_matrix
    
    def getI(self):
        if   self.ismatrix():
            return Covariance(self.__name+"I", asCovariance  = self.__B.I )
        elif self.isvector():
            return Covariance(self.__name+"I", asEyeByVector = 1. / self.__B )
        elif self.isscalar():
            return Covariance(self.__name+"I", asEyeByScalar = 1. / self.__B )
        else:
            return None
    
    def getT(self):
        if   self.ismatrix():
            return Covariance(self.__name+"T", asCovariance  = self.__B.T )
        elif self.isvector():
            return Covariance(self.__name+"T", asEyeByVector = self.__B )
        elif self.isscalar():
            return Covariance(self.__name+"T", asEyeByScalar = self.__B )
    
    def cholesky(self):
        if   self.ismatrix():
            return Covariance(self.__name+"C", asCovariance  = numpy.linalg.cholesky(self.__B) )
        elif self.isvector():
            return Covariance(self.__name+"C", asEyeByVector = numpy.sqrt( self.__B ) )
        elif self.isscalar():
            return Covariance(self.__name+"C", asEyeByScalar = numpy.sqrt( self.__B ) )
    
    def choleskyI(self):
        if   self.ismatrix():
            return Covariance(self.__name+"H", asCovariance  = numpy.linalg.cholesky(self.__B).I )
        elif self.isvector():
            return Covariance(self.__name+"H", asEyeByVector = 1.0 / numpy.sqrt( self.__B ) )
        elif self.isscalar():
            return Covariance(self.__name+"H", asEyeByScalar = 1.0 / numpy.sqrt( self.__B ) )
    
    def diag(self, msize=None):
        if   self.ismatrix():
            return numpy.diag(self.__B)
        elif self.isvector():
            return self.__B
        elif self.isscalar():
            if msize is None:
                raise ValueError("the size of the %s covariance matrix has to be given in case of definition as a scalar over the diagonal."%(self.__name,))
            else:
                return self.__B * numpy.ones(int(msize))
    
    def trace(self, msize=None):
        if   self.ismatrix():
            return numpy.trace(self.__B)
        elif self.isvector():
            return float(numpy.sum(self.__B))
        elif self.isscalar():
            if msize is None:
                raise ValueError("the size of the %s covariance matrix has to be given in case of definition as a scalar over the diagonal."%(self.__name,))
            else:
                return self.__B * int(msize)
    
    def __repr__(self):
        return repr(self.__B)
    
    def __str__(self):
        return str(self.__B)
    
    def __add__(self, other):
        if   self.ismatrix():
            return self.__B + numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            _A.reshape(_A.size)[::_A.shape[1]+1] += self.__B
            return numpy.asmatrix(_A)

    def __radd__(self, other):
        raise NotImplementedError("%s covariance matrix __radd__ method not available for %s type!"%(self.__name,type(other)))

    def __sub__(self, other):
        if   self.ismatrix():
            return self.__B - numpy.asmatrix(other)
        elif self.isvector() or self.isscalar():
            _A = numpy.asarray(other)
            _A.reshape(_A.size)[::_A.shape[1]+1] = self.__B - _A.reshape(_A.size)[::_A.shape[1]+1]
            return numpy.asmatrix(_A)

    def __rsub__(self, other):
        raise NotImplementedError("%s covariance matrix __rsub__ method not available for %s type!"%(self.__name,type(other)))

    def __neg__(self):
        return - self.__B
    
    def __mul__(self, other):
        if   self.ismatrix() and isinstance(other,numpy.matrix):
            return self.__B * other
        elif self.ismatrix() and (isinstance(other,numpy.ndarray) \
                               or isinstance(other,list) \
                               or isinstance(other,tuple)):
            if numpy.ravel(other).size == self.shape[1]: # Vecteur
                return self.__B * numpy.asmatrix(numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]: # Matrice
                return self.__B * numpy.asmatrix(other)
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.asmatrix(other).shape,self.__name))
        elif self.isvector() and (isinstance(other,numpy.matrix) \
                               or isinstance(other,numpy.ndarray) \
                               or isinstance(other,list) \
                               or isinstance(other,tuple)):
            if numpy.ravel(other).size == self.shape[1]: # Vecteur
                return numpy.asmatrix(self.__B * numpy.ravel(other)).T
            elif numpy.asmatrix(other).shape[0] == self.shape[1]: # Matrice
                return numpy.asmatrix((self.__B * (numpy.asarray(other).transpose())).transpose())
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.ravel(other).shape,self.__name))
        elif self.isscalar() and isinstance(other,numpy.matrix):
            return self.__B * other
        elif self.isscalar() and (isinstance(other,numpy.ndarray) \
                               or isinstance(other,list) \
                               or isinstance(other,tuple)):
            if len(numpy.asarray(other).shape) == 1 or numpy.asarray(other).shape[1] == 1 or numpy.asarray(other).shape[0] == 1:
                return self.__B * numpy.asmatrix(numpy.ravel(other)).T
            else:
                return self.__B * numpy.asmatrix(other)
        else:
            raise NotImplementedError("%s covariance matrix __mul__ method not available for %s type!"%(self.__name,type(other)))

    def __rmul__(self, other):
        if self.ismatrix() and isinstance(other,numpy.matrix):
            return other * self.__B
        elif self.isvector() and isinstance(other,numpy.matrix):
            if numpy.ravel(other).size == self.shape[0]: # Vecteur
                return numpy.asmatrix(numpy.ravel(other) * self.__B)
            elif numpy.asmatrix(other).shape[1] == self.shape[0]: # Matrice
                return numpy.asmatrix(numpy.array(other) * self.__B)
            else:
                raise ValueError("operands could not be broadcast together with shapes %s %s in %s matrix"%(self.shape,numpy.ravel(other).shape,self.__name))
        elif self.isscalar() and isinstance(other,numpy.matrix):
            return other * self.__B
        else:
            raise NotImplementedError("%s covariance matrix __rmul__ method not available for %s type!"%(self.__name,type(other)))

    def __len__(self):
        return self.shape[0]

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
