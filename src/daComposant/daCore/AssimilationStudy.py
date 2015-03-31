#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2015 EDF R&D
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
    Classe principale pour la pr�paration, la r�alisation et la restitution de
    calculs d'assimilation de donn�es.

    Ce module est destin� � �tre appel� par AssimilationStudy pour constituer
    les objets �l�mentaires de l'�tude.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = ["AssimilationStudy"]

import os, sys
import numpy
import ExtendedLogging ; ExtendedLogging.ExtendedLogging() # A importer en premier
import logging
try:
    import scipy.optimize
    logging.debug("Succeed initial import of scipy.optimize with Scipy %s", scipy.version.version)
except ImportError:
    logging.debug("Fail initial import of scipy.optimize")
import Persistence
from BasicObjects import Operator, Covariance
from PlatformInfo import uniq

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

        - Background : vecteur Xb
        - Observation : vecteur Y (potentiellement temporel) d'observations
        - State : vecteur d'�tat dont une partie est le vecteur de contr�le.
          Cette information n'est utile que si l'on veut faire des calculs sur
          l'�tat complet, mais elle n'est pas indispensable pour l'assimilation.
        - Control : vecteur X contenant toutes les variables de contr�le, i.e.
          les param�tres ou l'�tat dont on veut estimer la valeur pour obtenir
          les observations
        - ObservationOperator...: op�rateur d'observation H

        Les observations pr�sentent une erreur dont la matrice de covariance est
        R. L'�bauche du vecteur de contr�le pr�sente une erreur dont la matrice
        de covariance est B.
        """
        self.__name = str(name)
        self.__Xb  = None
        self.__Y   = None
        self.__U   = None
        self.__B   = None
        self.__R   = None
        self.__Q   = None
        self.__HO  = {}
        self.__EM  = {}
        self.__CM  = {}
        #
        self.__X  = Persistence.OneVector()
        self.__Parameters        = {}
        self.__StoredDiagnostics = {}
        self.__StoredInputs      = {}
        #
        # Variables temporaires
        self.__algorithm         = {}
        self.__algorithmFile     = None
        self.__algorithmName     = None
        self.__diagnosticFile    = None
        #
        # R�cup�re le chemin du r�pertoire parent et l'ajoute au path
        # (Cela compl�te l'action de la classe PathManagement dans PlatformInfo,
        # qui est activ�e dans Persistence)
        self.__parent = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        sys.path.insert(0, self.__parent)
        sys.path = uniq( sys.path ) # Conserve en unique exemplaire chaque chemin

    # ---------------------------------------------------------
    def setBackground(self,
            asVector           = None,
            asPersistentVector = None,
            Scheduler          = None,
            toBeStored         = False,
            ):
        """
        Permet de d�finir l'estimation a priori :
        - asVector : entr�e des donn�es, comme un vecteur compatible avec le
          constructeur de numpy.matrix
        - asPersistentVector : entr�e des donn�es, comme un vecteur de type
          persistent contruit avec la classe ad-hoc "Persistence"
        - Scheduler est le contr�le temporel des donn�es
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        if asVector is not None:
            if type( asVector ) is type( numpy.matrix([]) ):
                self.__Xb = numpy.matrix( asVector.A1, numpy.float ).T
            else:
                self.__Xb = numpy.matrix( asVector,    numpy.float ).T
        elif asPersistentVector is not None:
            if type(asPersistentVector) in [type([]),type(()),type(numpy.array([])),type(numpy.matrix([]))]:
                self.__Xb = Persistence.OneVector("Background", basetype=numpy.matrix)
                for member in asPersistentVector:
                    self.__Xb.store( numpy.matrix( numpy.asmatrix(member).A1, numpy.float ).T )
            else:
                self.__Xb = asPersistentVector
        else:
            raise ValueError("Error: improperly defined background, it requires at minima either a vector, a list/tuple of vectors or a persistent object")
        if toBeStored:
            self.__StoredInputs["Background"] = self.__Xb
        return 0

    def setBackgroundError(self,
            asCovariance  = None,
            asEyeByScalar = None,
            asEyeByVector = None,
            asCovObject   = None,
            toBeStored    = False,
            ):
        """
        Permet de d�finir la covariance des erreurs d'�bauche :
        - asCovariance : entr�e des donn�es, comme une matrice compatible avec
          le constructeur de numpy.matrix
        - asEyeByScalar : entr�e des donn�es comme un seul scalaire de variance,
          multiplicatif d'une matrice de corr�lation identit�, aucune matrice
          n'�tant donc explicitement � donner
        - asEyeByVector : entr�e des donn�es comme un seul vecteur de variance,
          � mettre sur la diagonale d'une matrice de corr�lation, aucune matrice
          n'�tant donc explicitement � donner
        - asCovObject : entr�e des donn�es comme un objet ayant des m�thodes
          particulieres de type matriciel
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        self.__B = Covariance(
            name          = "BackgroundError",
            asCovariance  = asCovariance,
            asEyeByScalar = asEyeByScalar,
            asEyeByVector = asEyeByVector,
            asCovObject   = asCovObject,
            )
        if toBeStored:
            self.__StoredInputs["BackgroundError"] = self.__B
        return 0

    # -----------------------------------------------------------
    def setObservation(self,
            asVector           = None,
            asPersistentVector = None,
            Scheduler          = None,
            toBeStored         = False,
            ):
        """
        Permet de d�finir les observations :
        - asVector : entr�e des donn�es, comme un vecteur compatible avec le
          constructeur de numpy.matrix
        - asPersistentVector : entr�e des donn�es, comme un vecteur de type
          persistent contruit avec la classe ad-hoc "Persistence"
        - Scheduler est le contr�le temporel des donn�es disponibles
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        if asVector is not None:
            if type( asVector ) is type( numpy.matrix([]) ):
                self.__Y = numpy.matrix( asVector.A1, numpy.float ).T
            else:
                self.__Y = numpy.matrix( asVector,    numpy.float ).T
        elif asPersistentVector is not None:
            if type(asPersistentVector) in [type([]),type(()),type(numpy.array([])),type(numpy.matrix([]))]:
                self.__Y = Persistence.OneVector("Observation", basetype=numpy.matrix)
                for member in asPersistentVector:
                    self.__Y.store( numpy.matrix( numpy.asmatrix(member).A1, numpy.float ).T )
            else:
                self.__Y = asPersistentVector
        else:
            raise ValueError("Error: improperly defined observations, it requires at minima either a vector, a list/tuple of vectors or a persistent object")
        if toBeStored:
            self.__StoredInputs["Observation"] = self.__Y
        return 0

    def setObservationError(self,
            asCovariance  = None,
            asEyeByScalar = None,
            asEyeByVector = None,
            asCovObject   = None,
            toBeStored    = False,
            ):
        """
        Permet de d�finir la covariance des erreurs d'observations :
        - asCovariance : entr�e des donn�es, comme une matrice compatible avec
          le constructeur de numpy.matrix
        - asEyeByScalar : entr�e des donn�es comme un seul scalaire de variance,
          multiplicatif d'une matrice de corr�lation identit�, aucune matrice
          n'�tant donc explicitement � donner
        - asEyeByVector : entr�e des donn�es comme un seul vecteur de variance,
          � mettre sur la diagonale d'une matrice de corr�lation, aucune matrice
          n'�tant donc explicitement � donner
        - asCovObject : entr�e des donn�es comme un objet ayant des m�thodes
          particulieres de type matriciel
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        self.__R = Covariance(
            name          = "ObservationError",
            asCovariance  = asCovariance,
            asEyeByScalar = asEyeByScalar,
            asEyeByVector = asEyeByVector,
            asCovObject   = asCovObject,
            )
        if toBeStored:
            self.__StoredInputs["ObservationError"] = self.__R
        return 0

    def setObservationOperator(self,
            asFunction = None,
            asMatrix   = None,
            appliedToX = None,
            toBeStored = False,
            avoidRC    = True,
            ):
        """
        Permet de d�finir un op�rateur d'observation H. L'ordre de priorit� des
        d�finitions et leur sens sont les suivants :
        - si asFunction["Tangent"] et asFunction["Adjoint"] ne sont pas None
          alors on d�finit l'op�rateur � l'aide de fonctions. Si la fonction
          "Direct" n'est pas d�finie, on prend la fonction "Tangent".
          Si "useApproximatedDerivatives" est vrai, on utilise une approximation
          des op�rateurs tangents et adjoints. On utilise par d�faut des
          diff�rences finies non centr�es ou centr�es (si "withCenteredDF" est
          vrai) avec un incr�ment multiplicatif "withIncrement" de 1% autour
          du point courant ou sur le point fixe "withdX".
        - si les fonctions ne sont pas disponibles et si asMatrix n'est pas
          None, alors on d�finit l'op�rateur "Direct" et "Tangent" � l'aide de
          la matrice, et l'op�rateur "Adjoint" � l'aide de la transpos�e. La
          matrice fournie doit �tre sous une forme compatible avec le
          constructeur de numpy.matrix.
        - si l'argument "appliedToX" n'est pas None, alors on d�finit, pour des
          X divers, l'op�rateur par sa valeur appliqu�e � cet X particulier,
          sous la forme d'un dictionnaire appliedToX[NAME] avec NAME un nom.
          L'op�rateur doit n�anmoins d�j� avoir �t� d�fini comme d'habitude.
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        L'argument "asFunction" peut prendre la forme compl�te suivante, avec
        les valeurs par d�faut standards :
          asFunction = {"Direct":None, "Tangent":None, "Adjoint":None,
                        "useApproximatedDerivatives":False,
                        "withCenteredDF"            :False,
                        "withIncrement"             :0.01,
                        "withdX"                    :None,
                        "withAvoidingRedundancy"    :True,
                        "withToleranceInRedundancy" :1.e-18,
                        "withLenghtOfRedundancy"    :-1,
                        "withmpEnabled"             :False,
                        "withmpWorkers"             :None,
                       }
        """
        if (type(asFunction) is type({})) and \
                asFunction.has_key("useApproximatedDerivatives") and bool(asFunction["useApproximatedDerivatives"]) and \
                asFunction.has_key("Direct") and (asFunction["Direct"] is not None):
            if not asFunction.has_key("withCenteredDF"):            asFunction["withCenteredDF"]            = False
            if not asFunction.has_key("withIncrement"):             asFunction["withIncrement"]             = 0.01
            if not asFunction.has_key("withdX"):                    asFunction["withdX"]                    = None
            if not asFunction.has_key("withAvoidingRedundancy"):    asFunction["withAvoidingRedundancy"]    = True
            if not asFunction.has_key("withToleranceInRedundancy"): asFunction["withToleranceInRedundancy"] = 1.e-18
            if not asFunction.has_key("withLenghtOfRedundancy"):    asFunction["withLenghtOfRedundancy"]    = -1
            if not asFunction.has_key("withmpEnabled"):             asFunction["withmpEnabled"]             = False
            if not asFunction.has_key("withmpWorkers"):             asFunction["withmpWorkers"]             = None
            from daNumerics.ApproximatedDerivatives import FDApproximation
            FDA = FDApproximation(
                Function              = asFunction["Direct"],
                centeredDF            = asFunction["withCenteredDF"],
                increment             = asFunction["withIncrement"],
                dX                    = asFunction["withdX"],
                avoidingRedundancy    = asFunction["withAvoidingRedundancy"],
                toleranceInRedundancy = asFunction["withToleranceInRedundancy"],
                lenghtOfRedundancy    = asFunction["withLenghtOfRedundancy"],
                mpEnabled             = asFunction["withmpEnabled"],
                mpWorkers             = asFunction["withmpWorkers"],
                )
            self.__HO["Direct"]  = Operator( fromMethod = FDA.DirectOperator,  avoidingRedundancy = avoidRC )
            self.__HO["Tangent"] = Operator( fromMethod = FDA.TangentOperator, avoidingRedundancy = avoidRC )
            self.__HO["Adjoint"] = Operator( fromMethod = FDA.AdjointOperator, avoidingRedundancy = avoidRC )
        elif (type(asFunction) is type({})) and \
                asFunction.has_key("Tangent") and asFunction.has_key("Adjoint") and \
                (asFunction["Tangent"] is not None) and (asFunction["Adjoint"] is not None):
            if not asFunction.has_key("Direct") or (asFunction["Direct"] is None):
                self.__HO["Direct"] = Operator( fromMethod = asFunction["Tangent"], avoidingRedundancy = avoidRC )
            else:
                self.__HO["Direct"] = Operator( fromMethod = asFunction["Direct"],  avoidingRedundancy = avoidRC  )
            self.__HO["Tangent"]    = Operator( fromMethod = asFunction["Tangent"], avoidingRedundancy = avoidRC )
            self.__HO["Adjoint"]    = Operator( fromMethod = asFunction["Adjoint"], avoidingRedundancy = avoidRC )
        elif asMatrix is not None:
            matrice = numpy.matrix( asMatrix, numpy.float )
            self.__HO["Direct"]  = Operator( fromMatrix = matrice,   avoidingRedundancy = avoidRC )
            self.__HO["Tangent"] = Operator( fromMatrix = matrice,   avoidingRedundancy = avoidRC )
            self.__HO["Adjoint"] = Operator( fromMatrix = matrice.T, avoidingRedundancy = avoidRC )
            del matrice
        else:
            raise ValueError("Improperly defined observation operator, it requires at minima either a matrix, a Direct for approximate derivatives or a Tangent/Adjoint pair.")
        #
        if appliedToX is not None:
            self.__HO["AppliedToX"] = {}
            if type(appliedToX) is not dict:
                raise ValueError("Error: observation operator defined by \"appliedToX\" need a dictionary as argument.")
            for key in appliedToX.keys():
                if type( appliedToX[key] ) is type( numpy.matrix([]) ):
                    # Pour le cas o� l'on a une vraie matrice
                    self.__HO["AppliedToX"][key] = numpy.matrix( appliedToX[key].A1, numpy.float ).T
                elif type( appliedToX[key] ) is type( numpy.array([]) ) and len(appliedToX[key].shape) > 1:
                    # Pour le cas o� l'on a un vecteur repr�sent� en array avec 2 dimensions
                    self.__HO["AppliedToX"][key] = numpy.matrix( appliedToX[key].reshape(len(appliedToX[key]),), numpy.float ).T
                else:
                    self.__HO["AppliedToX"][key] = numpy.matrix( appliedToX[key],    numpy.float ).T
        else:
            self.__HO["AppliedToX"] = None
        #
        if toBeStored:
            self.__StoredInputs["ObservationOperator"] = self.__HO
        return 0

    # -----------------------------------------------------------
    def setEvolutionModel(self,
            asFunction = None,
            asMatrix   = None,
            Scheduler  = None,
            toBeStored = False,
            avoidRC    = True,
            ):
        """
        Permet de d�finir un op�rateur d'�volution M. L'ordre de priorit� des
        d�finitions et leur sens sont les suivants :
        - si asFunction["Tangent"] et asFunction["Adjoint"] ne sont pas None
          alors on d�finit l'op�rateur � l'aide de fonctions. Si la fonction
          "Direct" n'est pas d�finie, on prend la fonction "Tangent".
          Si "useApproximatedDerivatives" est vrai, on utilise une approximation
          des op�rateurs tangents et adjoints. On utilise par d�faut des
          diff�rences finies non centr�es ou centr�es (si "withCenteredDF" est
          vrai) avec un incr�ment multiplicatif "withIncrement" de 1% autour
          du point courant ou sur le point fixe "withdX".
        - si les fonctions ne sont pas disponibles et si asMatrix n'est pas
          None, alors on d�finit l'op�rateur "Direct" et "Tangent" � l'aide de
          la matrice, et l'op�rateur "Adjoint" � l'aide de la transpos�e. La
          matrice fournie doit �tre sous une forme compatible avec le
          constructeur de numpy.matrix.
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        L'argument "asFunction" peut prendre la forme compl�te suivante, avec
        les valeurs par d�faut standards :
          asFunction = {"Direct":None, "Tangent":None, "Adjoint":None,
                        "useApproximatedDerivatives":False,
                        "withCenteredDF"            :False,
                        "withIncrement"             :0.01,
                        "withdX"                    :None,
                        "withAvoidingRedundancy"    :True,
                        "withToleranceInRedundancy" :1.e-18,
                        "withLenghtOfRedundancy"    :-1,
                        "withmpEnabled"             :False,
                        "withmpWorkers"             :None,
                       }
        """
        if (type(asFunction) is type({})) and \
                asFunction.has_key("useApproximatedDerivatives") and bool(asFunction["useApproximatedDerivatives"]) and \
                asFunction.has_key("Direct") and (asFunction["Direct"] is not None):
            if not asFunction.has_key("withCenteredDF"):            asFunction["withCenteredDF"]            = False
            if not asFunction.has_key("withIncrement"):             asFunction["withIncrement"]             = 0.01
            if not asFunction.has_key("withdX"):                    asFunction["withdX"]                    = None
            if not asFunction.has_key("withAvoidingRedundancy"):    asFunction["withAvoidingRedundancy"]    = True
            if not asFunction.has_key("withToleranceInRedundancy"): asFunction["withToleranceInRedundancy"] = 1.e-18
            if not asFunction.has_key("withLenghtOfRedundancy"):    asFunction["withLenghtOfRedundancy"]    = -1
            if not asFunction.has_key("withmpEnabled"):             asFunction["withmpEnabled"]             = False
            if not asFunction.has_key("withmpWorkers"):             asFunction["withmpWorkers"]             = None
            from daNumerics.ApproximatedDerivatives import FDApproximation
            FDA = FDApproximation(
                Function              = asFunction["Direct"],
                centeredDF            = asFunction["withCenteredDF"],
                increment             = asFunction["withIncrement"],
                dX                    = asFunction["withdX"],
                avoidingRedundancy    = asFunction["withAvoidingRedundancy"],
                toleranceInRedundancy = asFunction["withToleranceInRedundancy"],
                lenghtOfRedundancy    = asFunction["withLenghtOfRedundancy"],
                mpEnabled             = asFunction["withmpEnabled"],
                mpWorkers             = asFunction["withmpWorkers"],
                )
            self.__EM["Direct"]  = Operator( fromMethod = FDA.DirectOperator,  avoidingRedundancy = avoidRC  )
            self.__EM["Tangent"] = Operator( fromMethod = FDA.TangentOperator, avoidingRedundancy = avoidRC )
            self.__EM["Adjoint"] = Operator( fromMethod = FDA.AdjointOperator, avoidingRedundancy = avoidRC )
        elif (type(asFunction) is type({})) and \
                asFunction.has_key("Tangent") and asFunction.has_key("Adjoint") and \
                (asFunction["Tangent"] is not None) and (asFunction["Adjoint"] is not None):
            if not asFunction.has_key("Direct") or (asFunction["Direct"] is None):
                self.__EM["Direct"] = Operator( fromMethod = asFunction["Tangent"], avoidingRedundancy = avoidRC )
            else:
                self.__EM["Direct"] = Operator( fromMethod = asFunction["Direct"],  avoidingRedundancy = avoidRC )
            self.__EM["Tangent"]    = Operator( fromMethod = asFunction["Tangent"], avoidingRedundancy = avoidRC )
            self.__EM["Adjoint"]    = Operator( fromMethod = asFunction["Adjoint"], avoidingRedundancy = avoidRC )
        elif asMatrix is not None:
            matrice = numpy.matrix( asMatrix, numpy.float )
            self.__EM["Direct"]  = Operator( fromMatrix = matrice,   avoidingRedundancy = avoidRC )
            self.__EM["Tangent"] = Operator( fromMatrix = matrice,   avoidingRedundancy = avoidRC )
            self.__EM["Adjoint"] = Operator( fromMatrix = matrice.T, avoidingRedundancy = avoidRC )
            del matrice
        else:
            raise ValueError("Improperly defined evolution model, it requires at minima either a matrix, a Direct for approximate derivatives or a Tangent/Adjoint pair.")
        #
        if toBeStored:
            self.__StoredInputs["EvolutionModel"] = self.__EM
        return 0

    def setEvolutionError(self,
            asCovariance  = None,
            asEyeByScalar = None,
            asEyeByVector = None,
            asCovObject   = None,
            toBeStored    = False,
            ):
        """
        Permet de d�finir la covariance des erreurs de mod�le :
        - asCovariance : entr�e des donn�es, comme une matrice compatible avec
          le constructeur de numpy.matrix
        - asEyeByScalar : entr�e des donn�es comme un seul scalaire de variance,
          multiplicatif d'une matrice de corr�lation identit�, aucune matrice
          n'�tant donc explicitement � donner
        - asEyeByVector : entr�e des donn�es comme un seul vecteur de variance,
          � mettre sur la diagonale d'une matrice de corr�lation, aucune matrice
          n'�tant donc explicitement � donner
        - asCovObject : entr�e des donn�es comme un objet ayant des m�thodes
          particulieres de type matriciel
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        self.__Q = Covariance(
            name          = "EvolutionError",
            asCovariance  = asCovariance,
            asEyeByScalar = asEyeByScalar,
            asEyeByVector = asEyeByVector,
            asCovObject   = asCovObject,
            )
        if toBeStored:
            self.__StoredInputs["EvolutionError"] = self.__Q
        return 0

    # -----------------------------------------------------------
    def setControlModel(self,
            asFunction = {"Direct":None, "Tangent":None, "Adjoint":None,
                          "useApproximatedDerivatives":False,
                          "withCenteredDF"            :False,
                          "withIncrement"             :0.01,
                          "withdX"                    :None,
                         },
            asMatrix   = None,
            Scheduler  = None,
            toBeStored = False,
            avoidRC    = True,
            ):
        """
        Permet de d�finir un op�rateur de controle C. L'ordre de priorit� des
        d�finitions et leur sens sont les suivants :
        - si asFunction["Tangent"] et asFunction["Adjoint"] ne sont pas None
          alors on d�finit l'op�rateur � l'aide de fonctions. Si la fonction
          "Direct" n'est pas d�finie, on prend la fonction "Tangent".
          Si "useApproximatedDerivatives" est vrai, on utilise une approximation
          des op�rateurs tangents et adjoints. On utilise par d�faut des
          diff�rences finies non centr�es ou centr�es (si "withCenteredDF" est
          vrai) avec un incr�ment multiplicatif "withIncrement" de 1% autour
          du point courant ou sur le point fixe "withdX".
        - si les fonctions ne sont pas disponibles et si asMatrix n'est pas
          None, alors on d�finit l'op�rateur "Direct" et "Tangent" � l'aide de
          la matrice, et l'op�rateur "Adjoint" � l'aide de la transpos�e. La
          matrice fournie doit �tre sous une forme compatible avec le
          constructeur de numpy.matrix.
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        if (type(asFunction) is type({})) and \
                asFunction.has_key("useApproximatedDerivatives") and bool(asFunction["useApproximatedDerivatives"]) and \
                asFunction.has_key("Direct") and (asFunction["Direct"] is not None):
            if not asFunction.has_key("withCenteredDF"): asFunction["withCenteredDF"] = False
            if not asFunction.has_key("withIncrement"):  asFunction["withIncrement"]  = 0.01
            if not asFunction.has_key("withdX"):         asFunction["withdX"]         = None
            from daNumerics.ApproximatedDerivatives import FDApproximation
            FDA = FDApproximation(
                Function   = asFunction["Direct"],
                centeredDF = asFunction["withCenteredDF"],
                increment  = asFunction["withIncrement"],
                dX         = asFunction["withdX"] )
            self.__CM["Direct"]  = Operator( fromMethod = FDA.DirectOperator,  avoidingRedundancy = avoidRC  )
            self.__CM["Tangent"] = Operator( fromMethod = FDA.TangentOperator, avoidingRedundancy = avoidRC )
            self.__CM["Adjoint"] = Operator( fromMethod = FDA.AdjointOperator, avoidingRedundancy = avoidRC )
        elif (type(asFunction) is type({})) and \
                asFunction.has_key("Tangent") and asFunction.has_key("Adjoint") and \
                (asFunction["Tangent"] is not None) and (asFunction["Adjoint"] is not None):
            if not asFunction.has_key("Direct") or (asFunction["Direct"] is None):
                self.__CM["Direct"] = Operator( fromMethod = asFunction["Tangent"], avoidingRedundancy = avoidRC )
            else:
                self.__CM["Direct"] = Operator( fromMethod = asFunction["Direct"],  avoidingRedundancy = avoidRC  )
            self.__CM["Tangent"]    = Operator( fromMethod = asFunction["Tangent"], avoidingRedundancy = avoidRC )
            self.__CM["Adjoint"]    = Operator( fromMethod = asFunction["Adjoint"], avoidingRedundancy = avoidRC )
        elif asMatrix is not None:
            matrice = numpy.matrix( asMatrix, numpy.float )
            self.__CM["Direct"]  = Operator( fromMatrix = matrice,   avoidingRedundancy = avoidRC )
            self.__CM["Tangent"] = Operator( fromMatrix = matrice,   avoidingRedundancy = avoidRC )
            self.__CM["Adjoint"] = Operator( fromMatrix = matrice.T, avoidingRedundancy = avoidRC )
            del matrice
        else:
            raise ValueError("Improperly defined input control model, it requires at minima either a matrix, a Direct for approximate derivatives or a Tangent/Adjoint pair.")
        #
        if toBeStored:
            self.__StoredInputs["ControlModel"] = self.__CM
        return 0

    def setControlInput(self,
            asVector           = None,
            asPersistentVector = None,
            Scheduler          = None,
            toBeStored         = False,
            ):
        """
        Permet de d�finir le controle en entree :
        - asVector : entr�e des donn�es, comme un vecteur compatible avec le
          constructeur de numpy.matrix
        - asPersistentVector : entr�e des donn�es, comme un vecteur de type
          persistent contruit avec la classe ad-hoc "Persistence"
        - Scheduler est le contr�le temporel des donn�es disponibles
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        if asVector is not None:
            if isinstance(asVector,numpy.matrix):
                self.__U = numpy.matrix( asVector.A1, numpy.float ).T
            else:
                self.__U = numpy.matrix( asVector,    numpy.float ).T
        elif asPersistentVector is not None:
            if type(asPersistentVector) in [type([]),type(()),type(numpy.array([])),type(numpy.matrix([]))]:
                self.__U = Persistence.OneVector("ControlInput", basetype=numpy.matrix)
                for member in asPersistentVector:
                    self.__U.store( numpy.matrix( numpy.asmatrix(member).A1, numpy.float ).T )
            else:
                self.__U = asPersistentVector
        else:
            raise ValueError("Error: improperly defined control input, it requires at minima either a vector, a list/tuple of vectors or a persistent object")
        if toBeStored:
            self.__StoredInputs["ControlInput"] = self.__U
        return 0

    # -----------------------------------------------------------
    def setControls (self,
            asVector = None,
            toBeStored   = False,
            ):
        """
        Permet de d�finir la valeur initiale du vecteur X contenant toutes les
        variables de contr�le, i.e. les param�tres ou l'�tat dont on veut
        estimer la valeur pour obtenir les observations. C'est utile pour un
        algorithme it�ratif/incr�mental.
        - asVector : entr�e des donn�es, comme un vecteur compatible avec le
          constructeur de numpy.matrix.
        - toBeStored : bool�en indiquant si la donn�e d'entr�e est sauv�e pour
          �tre rendue disponible au m�me titre que les variables de calcul
        """
        if asVector is not None:
            self.__X.store( asVector )
        if toBeStored:
            self.__StoredInputs["Controls"] = self.__X
        return 0

    # -----------------------------------------------------------
    def setAlgorithm(self, choice = None ):
        """
        Permet de s�lectionner l'algorithme � utiliser pour mener � bien l'�tude
        d'assimilation. L'argument est un champ caract�re se rapportant au nom
        d'un fichier contenu dans "../daAlgorithms" et r�alisant l'op�ration
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
        except ImportError, e:
            raise ImportError("The module named \"%s\" was found, but is incorrect at the import stage.\n             The import error message is: %s"%(choice,e))
        #
        # Instancie un objet du type �l�mentaire du fichier
        # -------------------------------------------------
        self.__algorithm = self.__algorithmFile.ElementaryAlgorithm()
        self.__StoredInputs["AlgorithmName"] = self.__algorithmName
        return 0

    def setAlgorithmParameters(self, asDico=None):
        """
        Permet de d�finir les param�tres de l'algorithme, sous la forme d'un
        dictionnaire.
        """
        if asDico is not None:
            self.__Parameters.update( dict( asDico ) )
        #
        self.__StoredInputs["AlgorithmParameters"] = self.__Parameters
        return 0

    def getAlgorithmParameters(self, noDetails=True):
        """
        Renvoie la liste des param�tres requis selon l'algorithme
        """
        return self.__algorithm.getRequiredParameters(noDetails)

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
        if self.__StoredInputs.has_key(name):
            raise ValueError("A default input with the same name \"%s\" already exists."%str(name))
        elif self.__StoredDiagnostics.has_key(name):
            raise ValueError("A diagnostic with the same name \"%s\" already exists."%str(name))
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
        elif hasattr(self.__Xb,"size"):        __Xb_shape = (self.__Xb.size,)
        elif hasattr(self.__Xb,"shape"):
            if type(self.__Xb.shape) is tuple: __Xb_shape = self.__Xb.shape
            else:                              __Xb_shape = self.__Xb.shape()
        else: raise TypeError("The background (Xb) has no attribute of shape: problem !")
        #
        if self.__Y is None:                  __Y_shape = (0,)
        elif hasattr(self.__Y,"size"):        __Y_shape = (self.__Y.size,)
        elif hasattr(self.__Y,"shape"):
            if type(self.__Y.shape) is tuple: __Y_shape = self.__Y.shape
            else:                             __Y_shape = self.__Y.shape()
        else: raise TypeError("The observation (Y) has no attribute of shape: problem !")
        #
        if self.__U is None:                  __U_shape = (0,)
        elif hasattr(self.__U,"size"):        __U_shape = (self.__U.size,)
        elif hasattr(self.__U,"shape"):
            if type(self.__U.shape) is tuple: __U_shape = self.__U.shape
            else:                             __U_shape = self.__U.shape()
        else: raise TypeError("The control (U) has no attribute of shape: problem !")
        #
        if self.__B is None:                  __B_shape = (0,0)
        elif hasattr(self.__B,"shape"):
            if type(self.__B.shape) is tuple: __B_shape = self.__B.shape
            else:                             __B_shape = self.__B.shape()
        else: raise TypeError("The a priori errors covariance matrix (B) has no attribute of shape: problem !")
        #
        if self.__R is None:                  __R_shape = (0,0)
        elif hasattr(self.__R,"shape"):
            if type(self.__R.shape) is tuple: __R_shape = self.__R.shape
            else:                             __R_shape = self.__R.shape()
        else: raise TypeError("The observation errors covariance matrix (R) has no attribute of shape: problem !")
        #
        if self.__Q is None:                  __Q_shape = (0,0)
        elif hasattr(self.__Q,"shape"):
            if type(self.__Q.shape) is tuple: __Q_shape = self.__Q.shape
            else:                             __Q_shape = self.__Q.shape()
        else: raise TypeError("The evolution errors covariance matrix (Q) has no attribute of shape: problem !")
        #
        if len(self.__HO) == 0:                          __HO_shape = (0,0)
        elif type(self.__HO) is type({}):                __HO_shape = (0,0)
        elif hasattr(self.__HO["Direct"],"shape"):
            if type(self.__HO["Direct"].shape) is tuple: __HO_shape = self.__HO["Direct"].shape
            else:                                        __HO_shape = self.__HO["Direct"].shape()
        else: raise TypeError("The observation operator (H) has no attribute of shape: problem !")
        #
        if len(self.__EM) == 0:                          __EM_shape = (0,0)
        elif type(self.__EM) is type({}):                __EM_shape = (0,0)
        elif hasattr(self.__EM["Direct"],"shape"):
            if type(self.__EM["Direct"].shape) is tuple: __EM_shape = self.__EM["Direct"].shape
            else:                                        __EM_shape = self.__EM["Direct"].shape()
        else: raise TypeError("The evolution model (EM) has no attribute of shape: problem !")
        #
        if len(self.__CM) == 0:                          __CM_shape = (0,0)
        elif type(self.__CM) is type({}):                __CM_shape = (0,0)
        elif hasattr(self.__CM["Direct"],"shape"):
            if type(self.__CM["Direct"].shape) is tuple: __CM_shape = self.__CM["Direct"].shape
            else:                                        __CM_shape = self.__CM["Direct"].shape()
        else: raise TypeError("The control model (CM) has no attribute of shape: problem !")
        #
        # V�rification des conditions
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
        if len(self.__HO) > 0 and not(type(self.__HO) is type({})) and not( __HO_shape[1] == max(__Xb_shape) ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and state (X) \"%s\" are incompatible."%(__HO_shape,__Xb_shape))
        if len(self.__HO) > 0 and not(type(self.__HO) is type({})) and not( __HO_shape[0] == max(__Y_shape) ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and observation (Y) \"%s\" are incompatible."%(__HO_shape,__Y_shape))
        if len(self.__HO) > 0 and not(type(self.__HO) is type({})) and len(self.__B) > 0 and not( __HO_shape[1] == __B_shape[0] ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and a priori errors covariance matrix (B) \"%s\" are incompatible."%(__HO_shape,__B_shape))
        if len(self.__HO) > 0 and not(type(self.__HO) is type({})) and len(self.__R) > 0 and not( __HO_shape[0] == __R_shape[1] ):
            raise ValueError("Shape characteristic of observation operator (H) \"%s\" and observation errors covariance matrix (R) \"%s\" are incompatible."%(__HO_shape,__R_shape))
        #
        if self.__B is not None and len(self.__B) > 0 and not( __B_shape[1] == max(__Xb_shape) ):
            if self.__StoredInputs["AlgorithmName"] in ["EnsembleBlue",]:
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
        if self.__EM is not None and len(self.__EM) > 0 and not(type(self.__EM) is type({})) and not( __EM_shape[1] == max(__Xb_shape) ):
            raise ValueError("Shape characteristic of evolution model (EM) \"%s\" and state (X) \"%s\" are incompatible."%(__EM_shape,__Xb_shape))
        #
        if self.__CM is not None and len(self.__CM) > 0 and not(type(self.__CM) is type({})) and not( __CM_shape[1] == max(__U_shape) ):
            raise ValueError("Shape characteristic of control model (CM) \"%s\" and control (U) \"%s\" are incompatible."%(__CM_shape,__U_shape))
        #
        if self.__StoredInputs.has_key("AlgorithmParameters") \
            and self.__StoredInputs["AlgorithmParameters"].has_key("Bounds") \
            and (type(self.__StoredInputs["AlgorithmParameters"]["Bounds"]) is type([]) or type(self.__StoredInputs["AlgorithmParameters"]["Bounds"]) is type(())) \
            and (len(self.__StoredInputs["AlgorithmParameters"]["Bounds"]) != max(__Xb_shape)):
            raise ValueError("The number \"%s\" of bound pairs for the state (X) components is different of the size \"%s\" of the state itself." \
                %(len(self.__StoredInputs["AlgorithmParameters"]["Bounds"]),max(__Xb_shape)))
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
        Operator.CM.clearCache()
        self.shape_validate()
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
            Parameters = self.__Parameters,
            )
        return 0

    # -----------------------------------------------------------
    def get(self, key=None):
        """
        Renvoie les r�sultats disponibles apr�s l'ex�cution de la m�thode
        d'assimilation, ou les diagnostics disponibles. Attention, quand un
        diagnostic porte le m�me nom qu'une variable stock�e, c'est la variable
        stock�e qui est renvoy�e, et le diagnostic est inatteignable.
        """
        if key is not None:
            if self.__algorithm.has_key(key):
                return self.__algorithm.get( key )
            elif self.__StoredInputs.has_key(key):
                return self.__StoredInputs[key]
            elif self.__StoredDiagnostics.has_key(key):
                return self.__StoredDiagnostics[key]
            else:
                raise ValueError("The requested key \"%s\" does not exists as an input, a diagnostic or a stored variable."%key)
        else:
            allvariables = self.__algorithm.get()
            allvariables.update( self.__StoredDiagnostics )
            allvariables.update( self.__StoredInputs )
            return allvariables

    def get_available_variables(self):
        """
        Renvoie les variables potentiellement utilisables pour l'�tude,
        initialement stock�es comme donn�es d'entr�es ou dans les algorithmes,
        identifi�s par les cha�nes de caract�res. L'algorithme doit avoir �t�
        pr�alablement choisi sinon la m�thode renvoie "None".
        """
        if len( self.__algorithm.keys()) == 0 and len( self.__StoredInputs.keys() ) == 0:
            return None
        else:
            variables = []
            if len( self.__algorithm.keys()) > 0:
                variables.extend( self.__algorithm.get().keys() )
            if len( self.__StoredInputs.keys() ) > 0:
                variables.extend( self.__StoredInputs.keys() )
            variables.sort()
            return variables

    def get_available_algorithms(self):
        """
        Renvoie la liste des algorithmes potentiellement utilisables, identifi�s
        par les cha�nes de caract�res.
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
        Renvoie la liste des diagnostics potentiellement utilisables, identifi�s
        par les cha�nes de caract�res.
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
        sys.path = uniq( sys.path ) # Conserve en unique exemplaire chaque chemin
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
        sys.path = uniq( sys.path ) # Conserve en unique exemplaire chaque chemin
        return 1

    # -----------------------------------------------------------
    def setDataObserver(self,
            VariableName   = None,
            HookFunction   = None,
            HookParameters = None,
            Scheduler      = None,
            ):
        """
        Permet d'associer un observer � une ou des variables nomm�es g�r�es en
        interne, activable selon des r�gles d�finies dans le Scheduler. A chaque
        pas demand� dans le Scheduler, il effectue la fonction HookFunction avec
        les arguments (variable persistante VariableName, param�tres HookParameters).
        """
        #
        if type( self.__algorithm ) is dict:
            raise ValueError("No observer can be build before choosing an algorithm.")
        #
        # V�rification du nom de variable et typage
        # -----------------------------------------
        if type( VariableName ) is str:
            VariableNames = [VariableName,]
        elif type( VariableName ) is list:
            VariableNames = map( str, VariableName )
        else:
            raise ValueError("The observer requires a name or a list of names of variables.")
        #
        # Association interne de l'observer � la variable
        # -----------------------------------------------
        for n in VariableNames:
            if not self.__algorithm.has_key( n ):
                raise ValueError("An observer requires to be set on a variable named %s which does not exist."%n)
            else:
                self.__algorithm.StoredVariables[ n ].setDataObserver(
                    Scheduler      = Scheduler,
                    HookFunction   = HookFunction,
                    HookParameters = HookParameters,
                    )

    def removeDataObserver(self,
            VariableName   = None,
            HookFunction   = None,
            ):
        """
        Permet de retirer un observer � une ou des variable nomm�e.
        """
        #
        if type( self.__algorithm ) is dict:
            raise ValueError("No observer can be removed before choosing an algorithm.")
        #
        # V�rification du nom de variable et typage
        # -----------------------------------------
        if type( VariableName ) is str:
            VariableNames = [VariableName,]
        elif type( VariableName ) is list:
            VariableNames = map( str, VariableName )
        else:
            raise ValueError("The observer requires a name or a list of names of variables.")
        #
        # Association interne de l'observer � la variable
        # -----------------------------------------------
        for n in VariableNames:
            if not self.__algorithm.has_key( n ):
                raise ValueError("An observer requires to be removed on a variable named %s which does not exist."%n)
            else:
                self.__algorithm.StoredVariables[ n ].removeDataObserver(
                    HookFunction   = HookFunction,
                    )

    # -----------------------------------------------------------
    def setDebug(self, level=10):
        """
        Utiliser par exemple "import logging ; level = logging.DEBUG" avant cet
        appel pour changer le niveau de verbosit�, avec :
        NOTSET=0 < DEBUG=10 < INFO=20 < WARNING=30 < ERROR=40 < CRITICAL=50
        """
        log = logging.getLogger()
        log.setLevel( level )

    def unsetDebug(self):
        """
        Remet le logger au niveau par d�faut
        """
        log = logging.getLogger()
        log.setLevel( logging.WARNING )

    def __dir__(self):
        # return set(self.__dict__.keys() + dir(self.__class__))
        return ['get', '__doc__', '__init__', '__module__']

    def prepare_to_pickle(self):
        """
        Retire les variables non pickelisables
        """
        del self.__B
        del self.__CM # non pickelisable
        del self.__EM # non pickelisable
        del self.__HO # non pickelisable
        del self.__Parameters
        del self.__Q
        del self.__R
        del self.__U
        del self.__X
        del self.__Xb
        del self.__Y
        del self.__algorithmFile # non pickelisable
        del self.__algorithmName
        del self.__diagnosticFile # non pickelisable
        self.__class__.__doc__ = ""

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
