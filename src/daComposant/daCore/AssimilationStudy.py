#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2009  EDF R&D
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
__doc__ = """
    D�finit les outils g�n�raux �l�mentaires.
    
    Ce module est destin� � etre appel�e par AssimilationStudy pour constituer
    les objets �l�mentaires de l'algorithme.
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

import os, sys
import numpy
import Logging ; Logging.Logging() # A importer en premier
import Persistence
from BasicObjects import Operator

# ==============================================================================
class AssimilationStudy:
    """
    Cette classe sert d'interface pour l'utilisation de l'assimilation de
    donn�es. Elle contient les m�thodes ou accesseurs n�cessaires � la
    construction d'un calcul d'assimilation.
    """
    def __init__(self, name=""):
        """
        Pr�voit de conserver l'ensemble des variables n�cssaires � un algorithme
        �l�mentaire. Ces variables sont ensuite disponibles pour impl�menter un
        algorithme �l�mentaire particulier.

        Background............: vecteur Xb
        Observation...........: vecteur Y (potentiellement temporel)
            d'observations
        State.................: vecteur d'�tat dont une partie est le vecteur de
            contr�le. Cette information n'est utile que si l'on veut faire des
            calculs sur l'�tat complet, mais elle n'est pas indispensable pour
            l'assimilation.
        Control...............: vecteur X contenant toutes les variables de
            contr�le, i.e. les param�tres ou l'�tat dont on veut estimer la
            valeur pour obtenir les observations
        ObservationOperator...: op�rateur d'observation H

        Les observations pr�sentent une erreur dont la matrice de covariance est
        R. L'�bauche du vecteur de contr�le pr�sente une erreur dont la matrice
        de covariance est B.
        """
        self.__name = str(name)
        self.__Xb = None
        self.__Y  = None
        self.__B  = None
        self.__R  = None
        self.__Q  = None
        self.__H  = {}
        self.__M  = {}
        #
        self.__X  = Persistence.OneVector()
        self.__Parameters = {}
        self.__StoredDiagnostics = {}
        #
        # Variables temporaires
        self.__algorithm     = {}
        self.__algorithmFile = None
        self.__algorithmName = None
        self.__diagnosticFile = None
        #
        # R�cup�re le chemin du r�pertoire parent et l'ajoute au path
        # (Cela compl�te l'action de la classe PathManagement dans PlatformInfo,
        # qui est activ�e dans Persistence)
        self.__parent = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        sys.path.insert(0, self.__parent)
        sys.path = list(set(sys.path)) # Conserve en unique exemplaire chaque chemin

    # ---------------------------------------------------------
    def setBackground(self,
            asVector           = None,
            asPersistentVector = None,
            Scheduler          = None,
            ):
        """
        Permet de d�finir l'estimation a priori :
        - asVector : entr�e des donn�es, comme un vecteur compatible avec le
          constructeur de numpy.matrix
        - asPersistentVector : entr�e des donn�es, comme un vecteur de type
          persistent contruit avec la classe ad-hoc "Persistence"
        - Scheduler est le contr�le temporel des donn�es
        """
        if asVector is not None:
            if type( asVector ) is type( numpy.matrix([]) ):
                self.__Xb = numpy.matrix( asVector.A1, numpy.float ).T
            else:
                self.__Xb = numpy.matrix( asVector,    numpy.float ).T
        elif asPersistentVector is not None:
            self.__Xb = asPersistentVector
        else:
            raise ValueError("Error: improperly defined background")
        return 0
    
    def setBackgroundError(self, asCovariance=None):
        """
        Permet de d�finir la covariance des erreurs d'�bauche :
        - asCovariance : entr�e des donn�es, comme une matrice compatible avec
          le constructeur de numpy.matrix
        """
        self.__B  = numpy.matrix( asCovariance, numpy.float )
        return 0

    # -----------------------------------------------------------
    def setObservation(self,
            asVector           = None,
            asPersistentVector = None,
            Scheduler          = None,
            ):
        """
        Permet de d�finir les observations :
        - asVector : entr�e des donn�es, comme un vecteur compatible avec le
          constructeur de numpy.matrix
        - asPersistentVector : entr�e des donn�es, comme un vecteur de type
          persistent contruit avec la classe ad-hoc "Persistence"
        - Scheduler est le contr�le temporel des donn�es disponibles
        """
        if asVector is not None:
            if type( asVector ) is type( numpy.matrix([]) ):
                self.__Y = numpy.matrix( asVector.A1, numpy.float ).T
            else:
                self.__Y = numpy.matrix( asVector,    numpy.float ).T
        elif asPersistentVector is not None:
            self.__Y = asPersistentVector
        else:
            raise ValueError("Error: improperly defined observations")
        return 0

    def setObservationError(self, asCovariance=None):
        """
        Permet de d�finir la covariance des erreurs d'observations :
        - asCovariance : entr�e des donn�es, comme une matrice compatible avec
          le constructeur de numpy.matrix
        """
        self.__R  = numpy.matrix( asCovariance, numpy.float )
        return 0

    def setObservationOperator(self,
            asFunction = {"Direct":None, "Tangent":None, "Adjoint":None},
            asMatrix   = None,
            appliedToX = None,
            ):
        """
        Permet de d�finir un op�rateur d'observation H. L'ordre de priorit� des
        d�finitions et leur sens sont les suivants :
        - si asFunction["Tangent"] et asFunction["Adjoint"] ne sont pas None
          alors on d�finit l'op�rateur � l'aide de fonctions. Si la fonction
          "Direct" n'est pas d�finie, on prend la fonction "Tangent".
        - si les fonctions ne sont pas disponibles et si asMatrix n'est pas
          None, alors on d�finit l'op�rateur "Direct" et "Tangent" � l'aide de
          la matrice, et l'op�rateur "Adjoint" � l'aide de la transpos�e. La
          matrice fournie doit �tre sous une forme compatible avec le
          constructeur de numpy.matrix.
        - si l'argument "appliedToX" n'est pas None, alors on d�finit, pour des
          X divers, l'op�rateur par sa valeur appliqu�e � cet X particulier,
          sous la forme d'un dictionnaire appliedToX[NAME] avec NAME un nom.
          L'op�rateur doit n�anmoins d�j� avoir �t� d�fini comme d'habitude.
        """
        if (type(asFunction) is type({})) and (asFunction["Tangent"] is not None) and (asFunction["Adjoint"] is not None):
            if not asFunction.has_key("Direct") or (asFunction["Direct"] is None):
                self.__H["Direct"]  = Operator( fromMethod = asFunction["Tangent"]  )
            else:
                self.__H["Direct"] = Operator( fromMethod = asFunction["Direct"]  )
            self.__H["Tangent"]    = Operator( fromMethod = asFunction["Tangent"] )
            self.__H["Adjoint"]    = Operator( fromMethod = asFunction["Adjoint"] )
        elif asMatrix is not None:
            mat = numpy.matrix( asMatrix, numpy.float )
            self.__H["Direct"]  = Operator( fromMatrix = mat )
            self.__H["Tangent"] = Operator( fromMatrix = mat )
            self.__H["Adjoint"] = Operator( fromMatrix = mat.T )
        else:
            raise ValueError("Error: improperly defined observation operator")
        #
        if appliedToX is not None:
            self.__H["AppliedToX"] = {}
            if type(appliedToX) is not dict:
                raise ValueError("Error: observation operator defined by \"appliedToX\" need a dictionary as argument.")
            for key in appliedToX.keys():
                if type( appliedToX[key] ) is type( numpy.matrix([]) ):
                    # Pour le cas o� l'on a une vraie matrice
                    self.__H["AppliedToX"][key] = numpy.matrix( appliedToX[key].A1, numpy.float ).T
                elif type( appliedToX[key] ) is type( numpy.array([]) ) and len(appliedToX[key].shape) > 1:
                    # Pour le cas o� l'on a un vecteur repr�sent� en array avec 2 dimensions
                    self.__H["AppliedToX"][key] = numpy.matrix( appliedToX[key].reshape(len(appliedToX[key]),), numpy.float ).T
                else:
                    self.__H["AppliedToX"][key] = numpy.matrix( appliedToX[key],    numpy.float ).T
        else:
            self.__H["AppliedToX"] = None
        #
        return 0

    # -----------------------------------------------------------
    def setEvolutionModel(self,
            asFunction = {"Direct":None, "Tangent":None, "Adjoint":None},
            asMatrix   = None,
            Scheduler  = None,
            ):
        """
        Permet de d�finir un op�rateur d'�volution M. L'ordre de priorit� des
        d�finitions et leur sens sont les suivants :
        - si asFunction["Tangent"] et asFunction["Adjoint"] ne sont pas None
          alors on d�finit l'op�rateur � l'aide de fonctions. Si la fonction
          "Direct" n'est pas d�finie, on prend la fonction "Tangent".
        - si les fonctions ne sont pas disponibles et si asMatrix n'est pas
          None, alors on d�finit l'op�rateur "Direct" et "Tangent" � l'aide de
          la matrice, et l'op�rateur "Adjoint" � l'aide de la transpos�e. La
          matrice fournie doit �tre sous une forme compatible avec le
          constructeur de numpy.matrix.
        """
        if (type(asFunction) is type({})) and (asFunction["Tangent"] is not None) and (asFunction["Adjoint"] is not None):
            if not asFunction.has_key("Direct") or (asFunction["Direct"] is None):
                self.__M["Direct"] = Operator( fromMethod = asFunction["Tangent"]  )
            else:
                self.__M["Direct"] = Operator( fromMethod = asFunction["Direct"]  )
            self.__M["Tangent"]    = Operator( fromMethod = asFunction["Tangent"] )
            self.__M["Adjoint"]    = Operator( fromMethod = asFunction["Adjoint"] )
        elif asMatrix is not None:
            matrice = numpy.matrix( asMatrix, numpy.float )
            self.__M["Direct"]  = Operator( fromMatrix = matrice )
            self.__M["Tangent"] = Operator( fromMatrix = matrice )
            self.__M["Adjoint"] = Operator( fromMatrix = matrice.T )
        else:
            raise ValueError("Error: improperly defined evolution operator")
        return 0

    def setEvolutionError(self, asCovariance=None):
        """
        Permet de d�finir la covariance des erreurs de mod�le :
        - asCovariance : entr�e des donn�es, comme une matrice compatible avec
          le constructeur de numpy.matrix
        """
        self.__Q  = numpy.matrix( asCovariance, numpy.float )
        return 0

    # -----------------------------------------------------------
    def setControls (self, asVector = None ):
        """
        Permet de d�finir la valeur initiale du vecteur X contenant toutes les
        variables de contr�le, i.e. les param�tres ou l'�tat dont on veut
        estimer la valeur pour obtenir les observations. C'est utile pour un
        algorithme it�ratif/incr�mental
        - asVector : entr�e des donn�es, comme un vecteur compatible avec le
          constructeur de numpy.matrix.
        """
        if asVector is not None:
            self.__X.store( asVector )
        return 0

    # -----------------------------------------------------------
    def setAlgorithm(self, choice = None ):
        """
        Permet de s�lectionner l'algorithme � utiliser pour mener � bien l'�tude
        d'assimilation. L'argument est un champ caract�re se rapportant au nom
        d'un fichier contenu dans "../daAlgorithms" et r�alisant l'op�ration
        d'assimilation sur les arguments (Xb,Y,H,R,B,Xa).
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
        except ImportError, e:
            raise ImportError("The module named \"%s\" was found, but is incorrect at the import stage.\n             The import error message is: %s"%(choice,e))
        #
        # Instancie un objet du type �l�mentaire du fichier
        # -------------------------------------------------
        self.__algorithm = self.__algorithmFile.ElementaryAlgorithm()
        return 0

    def setAlgorithmParameters(self, asDico=None):
        """
        Permet de d�finir les param�tres de l'algorithme, sous la forme d'un
        dictionnaire.
        """
        self.__Parameters = dict( asDico )
        return 0

    # -----------------------------------------------------------
    def setDiagnostic(self, choice = None, name = "", unit = "", basetype = None, parameters = {} ):
        """
        Permet de s�lectionner un diagnostic a effectuer.
        """
        if choice is None:
            raise ValueError("Error: diagnostic choice has to be given")
        daDirectory = "daDiagnostics"
        #
        # Recherche explicitement le fichier complet
        # ------------------------------------------
        module_path = None
        for directory in sys.path:
            if os.path.isfile(os.path.join(directory, daDirectory, str(choice)+'.py')):
                module_path = os.path.abspath(os.path.join(directory, daDirectory))
        if module_path is None:
            raise ImportError("No diagnostic module named \"%s\" was found in a \"%s\" subdirectory\n             The search path is %s"%(choice, daDirectory, sys.path))
        #
        # Importe le fichier complet comme un module
        # ------------------------------------------
        try:
            sys_path_tmp = sys.path ; sys.path.insert(0,module_path)
            self.__diagnosticFile = __import__(str(choice), globals(), locals(), [])
            sys.path = sys_path_tmp ; del sys_path_tmp
        except ImportError, e:
            raise ImportError("The module named \"%s\" was found, but is incorrect at the import stage.\n             The import error message is: %s"%(choice,e))
        #
        # Instancie un objet du type �l�mentaire du fichier
        # -------------------------------------------------
        if self.__StoredDiagnostics.has_key(name):
            raise ValueError("A diagnostic with the same name already exists")
        else:
            self.__StoredDiagnostics[name] = self.__diagnosticFile.ElementaryDiagnostic(
                name       = name,
                unit       = unit,
                basetype   = basetype,
                parameters = parameters )
        return 0

    # -----------------------------------------------------------
    def shape_validate(self):
        """
        Validation de la correspondance correcte des tailles des variables et
        des matrices s'il y en a.
        """
        if self.__Xb is None:                  __Xb_shape = (0,)
        elif hasattr(self.__Xb,"shape"):
            if type(self.__Xb.shape) is tuple: __Xb_shape = self.__Xb.shape
            else:                              __Xb_shape = self.__Xb.shape()
        else: raise TypeError("Xb has no attribute of shape: problem !")
        #
        if self.__Y is None:                  __Y_shape = (0,)
        elif hasattr(self.__Y,"shape"):
            if type(self.__Y.shape) is tuple: __Y_shape = self.__Y.shape
            else:                             __Y_shape = self.__Y.shape()
        else: raise TypeError("Y has no attribute of shape: problem !")
        #
        if self.__B is None:                  __B_shape = (0,0)
        elif hasattr(self.__B,"shape"):
            if type(self.__B.shape) is tuple: __B_shape = self.__B.shape
            else:                             __B_shape = self.__B.shape()
        else: raise TypeError("B has no attribute of shape: problem !")
        #
        if self.__R is None:                  __R_shape = (0,0)
        elif hasattr(self.__R,"shape"):
            if type(self.__R.shape) is tuple: __R_shape = self.__R.shape
            else:                             __R_shape = self.__R.shape()
        else: raise TypeError("R has no attribute of shape: problem !")
        #
        if self.__Q is None:                  __Q_shape = (0,0)
        elif hasattr(self.__Q,"shape"):
            if type(self.__Q.shape) is tuple: __Q_shape = self.__Q.shape
            else:                             __Q_shape = self.__Q.shape()
        else: raise TypeError("Q has no attribute of shape: problem !")
        #
        if len(self.__H) == 0:                          __H_shape = (0,0)
        elif type(self.__H) is type({}):                __H_shape = (0,0)
        elif hasattr(self.__H["Direct"],"shape"):
            if type(self.__H["Direct"].shape) is tuple: __H_shape = self.__H["Direct"].shape
            else:                                       __H_shape = self.__H["Direct"].shape()
        else: raise TypeError("H has no attribute of shape: problem !")
        #
        if len(self.__M) == 0:                          __M_shape = (0,0)
        elif type(self.__M) is type({}):                __M_shape = (0,0)
        elif hasattr(self.__M["Direct"],"shape"):
            if type(self.__M["Direct"].shape) is tuple: __M_shape = self.__M["Direct"].shape
            else:                                       __M_shape = self.__M["Direct"].shape()
        else: raise TypeError("M has no attribute of shape: problem !")
        #
        # V�rification des conditions
        # ---------------------------
        if not( len(__Xb_shape) == 1 or min(__Xb_shape) == 1 ):
            raise ValueError("Shape characteristic of Xb is incorrect: \"%s\""%(__Xb_shape,))
        if not( len(__Y_shape) == 1 or min(__Y_shape) == 1 ):
            raise ValueError("Shape characteristic of Y is incorrect: \"%s\""%(__Y_shape,))
        #
        if not( min(__B_shape) == max(__B_shape) ):
            raise ValueError("Shape characteristic of B is incorrect: \"%s\""%(__B_shape,))
        if not( min(__R_shape) == max(__R_shape) ):
            raise ValueError("Shape characteristic of R is incorrect: \"%s\""%(__R_shape,))
        if not( min(__Q_shape) == max(__Q_shape) ):
            raise ValueError("Shape characteristic of Q is incorrect: \"%s\""%(__Q_shape,))
        if not( min(__M_shape) == max(__M_shape) ):
            raise ValueError("Shape characteristic of M is incorrect: \"%s\""%(__M_shape,))
        #
        if len(self.__H) > 0 and not(type(self.__H) is type({})) and not( __H_shape[1] == max(__Xb_shape) ):
            raise ValueError("Shape characteristic of H \"%s\" and X \"%s\" are incompatible"%(__H_shape,__Xb_shape))
        if len(self.__H) > 0 and not(type(self.__H) is type({})) and not( __H_shape[0] == max(__Y_shape) ):
            raise ValueError("Shape characteristic of H \"%s\" and Y \"%s\" are incompatible"%(__H_shape,__Y_shape))
        if len(self.__H) > 0 and not(type(self.__H) is type({})) and len(self.__B) > 0 and not( __H_shape[1] == __B_shape[0] ):
            raise ValueError("Shape characteristic of H \"%s\" and B \"%s\" are incompatible"%(__H_shape,__B_shape))
        if len(self.__H) > 0 and not(type(self.__H) is type({})) and len(self.__R) > 0 and not( __H_shape[0] == __R_shape[1] ):
            raise ValueError("Shape characteristic of H \"%s\" and R \"%s\" are incompatible"%(__H_shape,__R_shape))
        #
        if len(self.__B) > 0 and not( __B_shape[1] == max(__Xb_shape) ):
            raise ValueError("Shape characteristic of B \"%s\" and Xb \"%s\" are incompatible"%(__B_shape,__Xb_shape))
        #
        if len(self.__R) > 0 and not( __R_shape[1] == max(__Y_shape) ):
            raise ValueError("Shape characteristic of R \"%s\" and Y \"%s\" are incompatible"%(__R_shape,__Y_shape))
        #
        if len(self.__M) > 0 and not(type(self.__M) is type({})) and not( __M_shape[1] == max(__Xb_shape) ):
            raise ValueError("Shape characteristic of M \"%s\" and X \"%s\" are incompatible"%(__M_shape,__Xb_shape))
        #
        return 1

    # -----------------------------------------------------------
    def analyze(self):
        """
        Permet de lancer le calcul d'assimilation.
        
        Le nom de la m�thode � activer est toujours "run". Les param�tres en
        arguments de la m�thode sont fix�s. En sortie, on obtient les r�sultats
        dans la variable de type dictionnaire "StoredVariables", qui contient en
        particulier des objets de Persistence pour les analyses, OMA...
        """
        self.shape_validate()
        #
        self.__algorithm.run(
            Xb  = self.__Xb,
            Y   = self.__Y,
            H   = self.__H,
            M   = self.__M,
            R   = self.__R,
            B   = self.__B,
            Q   = self.__Q,
            Par = self.__Parameters,
            )
        return 0

    # -----------------------------------------------------------
    def get(self, key=None):
        """
        Renvoie les r�sultats disponibles apr�s l'ex�cution de la m�thode
        d'assimilation, ou les diagnostics disponibles. Attention, quand un
        diagnostic porte le m�me nom qu'un variable stock�e, c'est la variable
        stock�e qui est renvoy�e, et le diagnostic est inatteignable.
        """
        if key is not None:
            if self.__algorithm.has_key(key):
                return self.__algorithm.get( key )
            elif self.__StoredDiagnostics.has_key(key):
                return self.__StoredDiagnostics[key]
            else:
                raise ValueError("The requested key \"%s\" does not exists as a diagnostic or as a stored variable."%key)
        else:
            allvariables = self.__algorithm.get()
            allvariables.update( self.__StoredDiagnostics )
            return allvariables
    
    def get_available_algorithms(self):
        """
        Renvoie la liste des algorithmes identifi�s par les cha�nes de
        caract�res
        """
        files = []
        for directory in sys.path:
            if os.path.isdir(os.path.join(directory,"daAlgorithms")):
                for fname in os.listdir(os.path.join(directory,"daAlgorithms")):
                    root, ext = os.path.splitext(fname)
                    if ext == '.py' and root != '__init__':
                        files.append(root)
        files.sort()
        return files
        
    def get_available_diagnostics(self):
        """
        Renvoie la liste des diagnostics identifi�s par les cha�nes de
        caract�res
        """
        files = []
        for directory in sys.path:
            if os.path.isdir(os.path.join(directory,"daDiagnostics")):
                for fname in os.listdir(os.path.join(directory,"daDiagnostics")):
                    root, ext = os.path.splitext(fname)
                    if ext == '.py' and root != '__init__':
                        files.append(root)
        files.sort()
        return files

    # -----------------------------------------------------------
    def get_algorithms_main_path(self):
        """
        Renvoie le chemin pour le r�pertoire principal contenant les algorithmes
        dans un sous-r�pertoire "daAlgorithms"
        """
        return self.__parent

    def add_algorithms_path(self, asPath=None):
        """
        Ajoute au chemin de recherche des algorithmes un r�pertoire dans lequel
        se trouve un sous-r�pertoire "daAlgorithms"
        
        Remarque : si le chemin a d�j� �t� ajout� pour les diagnostics, il n'est
        pas indispensable de le rajouter ici.
        """
        if not os.path.isdir(asPath):
            raise ValueError("The given "+asPath+" argument must exist as a directory")
        if not os.path.isdir(os.path.join(asPath,"daAlgorithms")):
            raise ValueError("The given \""+asPath+"\" argument must contain a subdirectory named \"daAlgorithms\"")
        if not os.path.isfile(os.path.join(asPath,"daAlgorithms","__init__.py")):
            raise ValueError("The given \""+asPath+"/daAlgorithms\" path must contain a file named \"__init__.py\"")
        sys.path.insert(0, os.path.abspath(asPath))
        sys.path = list(set(sys.path)) # Conserve en unique exemplaire chaque chemin
        return 1

    def get_diagnostics_main_path(self):
        """
        Renvoie le chemin pour le r�pertoire principal contenant les diagnostics
        dans un sous-r�pertoire "daDiagnostics"
        """
        return self.__parent

    def add_diagnostics_path(self, asPath=None):
        """
        Ajoute au chemin de recherche des algorithmes un r�pertoire dans lequel
        se trouve un sous-r�pertoire "daDiagnostics"
        
        Remarque : si le chemin a d�j� �t� ajout� pour les algorithmes, il n'est
        pas indispensable de le rajouter ici.
        """
        if not os.path.isdir(asPath):
            raise ValueError("The given "+asPath+" argument must exist as a directory")
        if not os.path.isdir(os.path.join(asPath,"daDiagnostics")):
            raise ValueError("The given \""+asPath+"\" argument must contain a subdirectory named \"daDiagnostics\"")
        if not os.path.isfile(os.path.join(asPath,"daDiagnostics","__init__.py")):
            raise ValueError("The given \""+asPath+"/daDiagnostics\" path must contain a file named \"__init__.py\"")
        sys.path.insert(0, os.path.abspath(asPath))
        sys.path = list(set(sys.path)) # Conserve en unique exemplaire chaque chemin
        return 1

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
    
    ADD = AssimilationStudy("Ma premiere etude BLUE")
    
    ADD.setBackground         (asVector     = [0, 1, 2])
    ADD.setBackgroundError    (asCovariance = "1 0 0;0 1 0;0 0 1")
    ADD.setObservation        (asVector     = [0.5, 1.5, 2.5])
    ADD.setObservationError   (asCovariance = "1 0 0;0 1 0;0 0 1")
    ADD.setObservationOperator(asMatrix     = "1 0 0;0 1 0;0 0 1")
    
    ADD.setAlgorithm(choice="Blue")
    
    ADD.analyze()
    
    print "Nombre d'analyses  :", ADD.get("Analysis").stepnumber()
    print "Analyse r�sultante :", ADD.get("Analysis").valueserie(0)
    print "Innovation         :", ADD.get("Innovation").valueserie(0)
    print
    
    print "Algorithmes disponibles :", ADD.get_available_algorithms()
    #�print " Chemin des algorithmes :", ADD.get_algorithms_main_path()
    print "Diagnostics disponibles :", ADD.get_available_diagnostics()
    #�print " Chemin des diagnostics :", ADD.get_diagnostics_main_path()
    print

    ADD.setDiagnostic("RMS", "Ma RMS")
    
    liste = ADD.get().keys()
    liste.sort()
    print "Variables et diagnostics disponibles :", liste
    print

