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

"""
    Définit des outils de persistence et d'enregistrement de séries de valeurs
    pour analyse ultérieure ou utilisation de calcul.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os, sys, numpy, copy
import gzip, bz2

from daCore.PlatformInfo import PathManagement ; PathManagement()
from daCore.PlatformInfo import has_gnuplot, PlatformInfo
mfp = PlatformInfo().MaximumPrecision()
if has_gnuplot:
    import Gnuplot

if sys.version_info.major < 3:
    range = xrange
    iLong = long
    import cPickle as pickle
else:
    iLong = int
    import pickle

# ==============================================================================
class Persistence(object):
    """
    Classe générale de persistence définissant les accesseurs nécessaires
    (Template)
    """
    def __init__(self, name="", unit="", basetype=str):
        """
        name : nom courant
        unit : unité
        basetype : type de base de l'objet stocké à chaque pas

        La gestion interne des données est exclusivement basée sur les variables
        initialisées ici (qui ne sont pas accessibles depuis l'extérieur des
        objets comme des attributs) :
        __basetype : le type de base de chaque valeur, sous la forme d'un type
                     permettant l'instanciation ou le casting Python
        __values : les valeurs de stockage. Par défaut, c'est None
        """
        self.__name = str(name)
        self.__unit = str(unit)
        #
        self.__basetype = basetype
        #
        self.__values   = []
        self.__tags     = []
        #
        self.__dynamic  = False
        self.__g        = None
        self.__title    = None
        self.__ltitle   = None
        self.__pause    = None
        #
        self.__dataobservers = []

    def basetype(self, basetype=None):
        """
        Renvoie ou met en place le type de base des objets stockés
        """
        if basetype is None:
            return self.__basetype
        else:
            self.__basetype = basetype

    def store(self, value=None, **kwargs):
        """
        Stocke une valeur avec ses informations de filtrage.
        """
        if value is None: raise ValueError("Value argument required")
        #
        self.__values.append(copy.copy(self.__basetype(value)))
        self.__tags.append(kwargs)
        #
        if self.__dynamic: self.__replots()
        __step = len(self.__values) - 1
        for hook, parameters, scheduler in self.__dataobservers:
            if __step in scheduler:
                hook( self, parameters )

    def pop(self, item=None):
        """
        Retire une valeur enregistree par son index de stockage. Sans argument,
        retire le dernier objet enregistre.
        """
        if item is not None:
            __index = int(item)
            self.__values.pop(__index)
            self.__tags.pop(__index)
        else:
            self.__values.pop()
            self.__tags.pop()

    def shape(self):
        """
        Renvoie la taille sous forme numpy du dernier objet stocké. Si c'est un
        objet numpy, renvoie le shape. Si c'est un entier, un flottant, un
        complexe, renvoie 1. Si c'est une liste ou un dictionnaire, renvoie la
        longueur. Par défaut, renvoie 1.
        """
        if len(self.__values) > 0:
            if self.__basetype in [numpy.matrix, numpy.ndarray, numpy.array, numpy.ravel]:
                return self.__values[-1].shape
            elif self.__basetype in [int, float]:
                return (1,)
            elif self.__basetype in [list, dict]:
                return (len(self.__values[-1]),)
            else:
                return (1,)
        else:
            raise ValueError("Object has no shape before its first storage")

    # ---------------------------------------------------------
    def __str__(self):
        "x.__str__() <==> str(x)"
        msg  = "   Index        Value   Tags\n"
        for i,v in enumerate(self.__values):
            msg += "  i=%05i  %10s   %s\n"%(i,v,self.__tags[i])
        return msg

    def __len__(self):
        "x.__len__() <==> len(x)"
        return len(self.__values)

    def name(self):
        return self.__name

    def __getitem__(self, index=None ):
        "x.__getitem__(y) <==> x[y]"
        return copy.copy(self.__values[index])

    def count(self, value):
        "L.count(value) -> integer -- return number of occurrences of value"
        return self.__values.count(value)

    def index(self, value, start=0, stop=None):
        "L.index(value, [start, [stop]]) -> integer -- return first index of value."
        if stop is None : stop = len(self.__values)
        return self.__values.index(value, start, stop)

    # ---------------------------------------------------------
    def __filteredIndexes(self, **kwargs):
        "Function interne filtrant les index"
        __indexOfFilteredItems = range(len(self.__tags))
        __filteringKwTags = kwargs.keys()
        if len(__filteringKwTags) > 0:
            for tagKey in __filteringKwTags:
                __tmp = []
                for i in __indexOfFilteredItems:
                    if tagKey in self.__tags[i]:
                        if self.__tags[i][tagKey] == kwargs[tagKey]:
                            __tmp.append( i )
                        elif isinstance(kwargs[tagKey],(list,tuple)) and self.__tags[i][tagKey] in kwargs[tagKey]:
                            __tmp.append( i )
                __indexOfFilteredItems = __tmp
                if len(__indexOfFilteredItems) == 0: break
        return __indexOfFilteredItems

    # ---------------------------------------------------------
    def values(self, **kwargs):
        "D.values() -> list of D's values"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return [self.__values[i] for i in __indexOfFilteredItems]

    def keys(self, keyword=None , **kwargs):
        "D.keys() -> list of D's keys"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        __keys = []
        for i in __indexOfFilteredItems:
            if keyword in self.__tags[i]:
                __keys.append( self.__tags[i][keyword] )
            else:
                __keys.append( None )
        return __keys

    def items(self, keyword=None , **kwargs):
        "D.items() -> list of D's (key, value) pairs, as 2-tuples"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        __pairs = []
        for i in __indexOfFilteredItems:
            if keyword in self.__tags[i]:
                __pairs.append( (self.__tags[i][keyword], self.__values[i]) )
            else:
                __pairs.append( (None, self.__values[i]) )
        return __pairs

    def tagkeys(self):
        "D.tagkeys() -> list of D's tag keys"
        __allKeys = []
        for dicotags in self.__tags:
            __allKeys.extend( list(dicotags.keys()) )
        __allKeys = sorted(set(__allKeys))
        return __allKeys

    # def valueserie(self, item=None, allSteps=True, **kwargs):
    #     if item is not None:
    #         return self.__values[item]
    #     else:
    #         __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
    #         if not allSteps and len(__indexOfFilteredItems) > 0:
    #             return self.__values[__indexOfFilteredItems[0]]
    #         else:
    #             return [self.__values[i] for i in __indexOfFilteredItems]

    def tagserie(self, item=None, withValues=False, outputTag=None, **kwargs):
        "D.tagserie() -> list of D's tag serie"
        if item is None:
            __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        else:
            __indexOfFilteredItems = [item,]
        #
        # Dans le cas où la sortie donne les valeurs d'un "outputTag"
        if outputTag is not None and isinstance(outputTag,str) :
            outputValues = []
            for index in __indexOfFilteredItems:
                if outputTag in self.__tags[index].keys():
                    outputValues.append( self.__tags[index][outputTag] )
            outputValues = sorted(set(outputValues))
            return outputValues
        #
        # Dans le cas où la sortie donne les tags satisfaisants aux conditions
        else:
            if withValues:
                return [self.__tags[index] for index in __indexOfFilteredItems]
            else:
                allTags = {}
                for index in __indexOfFilteredItems:
                    allTags.update( self.__tags[index] )
                allKeys = sorted(allTags.keys())
                return allKeys

    # ---------------------------------------------------------
    # Pour compatibilite
    def stepnumber(self):
        "Nombre de pas"
        return len(self.__values)

    # Pour compatibilite
    def stepserie(self, **kwargs):
        "Nombre de pas filtrés"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return __indexOfFilteredItems

    # Pour compatibilite
    def steplist(self, **kwargs):
        "Nombre de pas filtrés"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return list(__indexOfFilteredItems)

    # ---------------------------------------------------------
    def means(self):
        """
        Renvoie la série, contenant à chaque pas, la valeur moyenne des données
        au pas. Il faut que le type de base soit compatible avec les types
        élémentaires numpy.
        """
        try:
            return [numpy.mean(item, dtype=mfp) for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stds(self, ddof=0):
        """
        Renvoie la série, contenant à chaque pas, l'écart-type des données
        au pas. Il faut que le type de base soit compatible avec les types
        élémentaires numpy.

        ddof : c'est le nombre de degrés de liberté pour le calcul de
               l'écart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
        """
        try:
            if numpy.version.version >= '1.1.0':
                return [numpy.array(item).std(ddof=ddof) for item in self.__values]
            else:
                return [numpy.array(item).std() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def sums(self):
        """
        Renvoie la série, contenant à chaque pas, la somme des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            return [numpy.array(item).sum() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def mins(self):
        """
        Renvoie la série, contenant à chaque pas, le minimum des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            return [numpy.array(item).min() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def maxs(self):
        """
        Renvoie la série, contenant à chaque pas, la maximum des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            return [numpy.array(item).max() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def __preplots(self,
                   title    = "",
                   xlabel   = "",
                   ylabel   = "",
                   ltitle   = None,
                   geometry = "600x400",
                   persist  = False,
                   pause    = True,
                  ):
        "Préparation des plots"
        #
        # Vérification de la disponibilité du module Gnuplot
        if not has_gnuplot:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # Vérification et compléments sur les paramètres d'entrée
        if persist:
            Gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -persist -geometry '+geometry
        else:
            Gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -geometry '+geometry
        if ltitle is None:
            ltitle = ""
        self.__g = Gnuplot.Gnuplot() # persist=1
        self.__g('set terminal '+Gnuplot.GnuplotOpts.default_term)
        self.__g('set style data lines')
        self.__g('set grid')
        self.__g('set autoscale')
        self.__g('set xlabel "'+str(xlabel)+'"')
        self.__g('set ylabel "'+str(ylabel)+'"')
        self.__title  = title
        self.__ltitle = ltitle
        self.__pause  = pause

    def plots(self,
              item     = None,
              step     = None,
              steps    = None,
              title    = "",
              xlabel   = "",
              ylabel   = "",
              ltitle   = None,
              geometry = "600x400",
              filename = "",
              dynamic  = False,
              persist  = False,
              pause    = True,
             ):
        """
        Renvoie un affichage de la valeur à chaque pas, si elle est compatible
        avec un affichage Gnuplot (donc essentiellement un vecteur). Si
        l'argument "step" existe dans la liste des pas de stockage effectués,
        renvoie l'affichage de la valeur stockée à ce pas "step". Si l'argument
        "item" est correct, renvoie l'affichage de la valeur stockée au numéro
        "item". Par défaut ou en l'absence de "step" ou "item", renvoie un
        affichage successif de tous les pas.

        Arguments :
            - step     : valeur du pas à afficher
            - item     : index de la valeur à afficher
            - steps    : liste unique des pas de l'axe des X, ou None si c'est
                         la numérotation par défaut
            - title    : base du titre général, qui sera automatiquement
                         complétée par la mention du pas
            - xlabel   : label de l'axe des X
            - ylabel   : label de l'axe des Y
            - ltitle   : titre associé au vecteur tracé
            - geometry : taille en pixels de la fenêtre et position du coin haut
                         gauche, au format X11 : LxH+X+Y (défaut : 600x400)
            - filename : base de nom de fichier Postscript pour une sauvegarde,
                         qui est automatiquement complétée par le numéro du
                         fichier calculé par incrément simple de compteur
            - dynamic  : effectue un affichage des valeurs à chaque stockage
                         (au-delà du second). La méthode "plots" permet de
                         déclarer l'affichage dynamique, et c'est la méthode
                         "__replots" qui est utilisée pour l'effectuer
            - persist  : booléen indiquant que la fenêtre affichée sera
                         conservée lors du passage au dessin suivant
                         Par défaut, persist = False
            - pause    : booléen indiquant une pause après chaque tracé, et
                         attendant un Return
                         Par défaut, pause = True
        """
        if not self.__dynamic:
            self.__preplots(title, xlabel, ylabel, ltitle, geometry, persist, pause )
            if dynamic:
                self.__dynamic = True
                if len(self.__values) == 0: return 0
        #
        # Tracé du ou des vecteurs demandés
        indexes = []
        if step is not None and step < len(self.__values):
            indexes.append(step)
        elif item is not None and item < len(self.__values):
            indexes.append(item)
        else:
            indexes = indexes + list(range(len(self.__values)))
        #
        i = -1
        for index in indexes:
            self.__g('set title  "'+str(title)+' (pas '+str(index)+')"')
            if isinstance(steps,list) or isinstance(steps,numpy.ndarray):
                Steps = list(steps)
            else:
                Steps = list(range(len(self.__values[index])))
            #
            self.__g.plot( Gnuplot.Data( Steps, self.__values[index], title=ltitle ) )
            #
            if filename != "":
                i += 1
                stepfilename = "%s_%03i.ps"%(filename,i)
                if os.path.isfile(stepfilename):
                    raise ValueError("Error: a file with this name \"%s\" already exists."%stepfilename)
                self.__g.hardcopy(filename=stepfilename, color=1)
            if self.__pause:
                eval(input('Please press return to continue...\n'))

    def __replots(self):
        """
        Affichage dans le cas du suivi dynamique de la variable
        """
        if self.__dynamic and len(self.__values) < 2: return 0
        #
        self.__g('set title  "'+str(self.__title))
        Steps = list(range(len(self.__values)))
        self.__g.plot( Gnuplot.Data( Steps, self.__values, title=self.__ltitle ) )
        #
        if self.__pause:
            eval(input('Please press return to continue...\n'))

    # ---------------------------------------------------------
    # On pourrait aussi utiliser d'autres attributs d'un "array" comme "tofile"
    def mean(self):
        """
        Renvoie la moyenne sur toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            if self.__basetype in [int, float]:
                return float( numpy.mean(self.__values, dtype=mfp) )
            else:
                return numpy.mean(self.__values, axis=0, dtype=mfp)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def std(self, ddof=0):
        """
        Renvoie l'écart-type de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.

        ddof : c'est le nombre de degrés de liberté pour le calcul de
               l'écart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
        """
        try:
            if numpy.version.version >= '1.1.0':
                return numpy.array(self.__values).std(ddof=ddof,axis=0)
            else:
                return numpy.array(self.__values).std(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def sum(self):
        """
        Renvoie la somme de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.array(self.__values).sum(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def min(self):
        """
        Renvoie le minimum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.array(self.__values).min(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def max(self):
        """
        Renvoie le maximum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.array(self.__values).max(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def cumsum(self):
        """
        Renvoie la somme cumulée de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.array(self.__values).cumsum(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def plot(self,
             steps    = None,
             title    = "",
             xlabel   = "",
             ylabel   = "",
             ltitle   = None,
             geometry = "600x400",
             filename = "",
             persist  = False,
             pause    = True,
            ):
        """
        Renvoie un affichage unique pour l'ensemble des valeurs à chaque pas, si
        elles sont compatibles avec un affichage Gnuplot (donc essentiellement
        un vecteur). Si l'argument "step" existe dans la liste des pas de
        stockage effectués, renvoie l'affichage de la valeur stockée à ce pas
        "step". Si l'argument "item" est correct, renvoie l'affichage de la
        valeur stockée au numéro "item".

        Arguments :
            - steps    : liste unique des pas de l'axe des X, ou None si c'est
                         la numérotation par défaut
            - title    : base du titre général, qui sera automatiquement
                         complétée par la mention du pas
            - xlabel   : label de l'axe des X
            - ylabel   : label de l'axe des Y
            - ltitle   : titre associé au vecteur tracé
            - geometry : taille en pixels de la fenêtre et position du coin haut
                         gauche, au format X11 : LxH+X+Y (défaut : 600x400)
            - filename : nom de fichier Postscript pour une sauvegarde
            - persist  : booléen indiquant que la fenêtre affichée sera
                         conservée lors du passage au dessin suivant
                         Par défaut, persist = False
            - pause    : booléen indiquant une pause après chaque tracé, et
                         attendant un Return
                         Par défaut, pause = True
        """
        #
        # Vérification de la disponibilité du module Gnuplot
        if not has_gnuplot:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # Vérification et compléments sur les paramètres d'entrée
        if persist:
            Gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -persist -geometry '+geometry
        else:
            Gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -geometry '+geometry
        if ltitle is None:
            ltitle = ""
        if isinstance(steps,list) or isinstance(steps, numpy.ndarray):
            Steps = list(steps)
        else:
            Steps = list(range(len(self.__values[0])))
        self.__g = Gnuplot.Gnuplot() # persist=1
        self.__g('set terminal '+Gnuplot.GnuplotOpts.default_term)
        self.__g('set style data lines')
        self.__g('set grid')
        self.__g('set autoscale')
        self.__g('set title  "'+str(title) +'"')
        self.__g('set xlabel "'+str(xlabel)+'"')
        self.__g('set ylabel "'+str(ylabel)+'"')
        #
        # Tracé du ou des vecteurs demandés
        indexes = list(range(len(self.__values)))
        self.__g.plot( Gnuplot.Data( Steps, self.__values[indexes.pop(0)], title=ltitle+" (pas 0)" ) )
        for index in indexes:
            self.__g.replot( Gnuplot.Data( Steps, self.__values[index], title=ltitle+" (pas %i)"%index ) )
        #
        if filename != "":
            self.__g.hardcopy(filename=filename, color=1)
        if pause:
            eval(input('Please press return to continue...\n'))

    # ---------------------------------------------------------
    def setDataObserver(self, HookFunction = None, HookParameters = None, Scheduler = None):
        """
        Association à la variable d'un triplet définissant un observer

        Le Scheduler attendu est une fréquence, une simple liste d'index ou un
        range des index.
        """
        #
        # Vérification du Scheduler
        # -------------------------
        maxiter = int( 1e9 )
        if isinstance(Scheduler,int):      # Considéré comme une fréquence à partir de 0
            Schedulers = range( 0, maxiter, int(Scheduler) )
        elif isinstance(Scheduler,range):  # Considéré comme un itérateur
            Schedulers = Scheduler
        elif isinstance(Scheduler,(list,tuple)):   # Considéré comme des index explicites
            Schedulers = [iLong(i) for i in Scheduler] # map( long, Scheduler )
        else:                              # Dans tous les autres cas, activé par défaut
            Schedulers = range( 0, maxiter )
        #
        # Stockage interne de l'observer dans la variable
        # -----------------------------------------------
        self.__dataobservers.append( [HookFunction, HookParameters, Schedulers] )

    def removeDataObserver(self, HookFunction = None, AllObservers = False):
        """
        Suppression d'un observer nommé sur la variable.

        On peut donner dans HookFunction la meme fonction que lors de la
        définition, ou un simple string qui est le nom de la fonction. Si
        AllObservers est vrai, supprime tous les observers enregistrés.
        """
        if hasattr(HookFunction,"func_name"):
            name = str( HookFunction.func_name )
        elif hasattr(HookFunction,"__name__"):
            name = str( HookFunction.__name__ )
        elif isinstance(HookFunction,str):
            name = str( HookFunction )
        else:
            name = None
        #
        i = -1
        index_to_remove = []
        for [hf, hp, hs] in self.__dataobservers:
            i = i + 1
            if name is hf.__name__ or AllObservers: index_to_remove.append( i )
        index_to_remove.reverse()
        for i in index_to_remove:
            self.__dataobservers.pop( i )
        return len(index_to_remove)

    def hasDataObserver(self):
        return bool(len(self.__dataobservers) > 0)

# ==============================================================================
class SchedulerTrigger(object):
    """
    Classe générale d'interface de type Scheduler/Trigger
    """
    def __init__(self,
                 simplifiedCombo = None,
                 startTime       = 0,
                 endTime         = int( 1e9 ),
                 timeDelay       = 1,
                 timeUnit        = 1,
                 frequency       = None,
                ):
        pass

# ==============================================================================
class OneScalar(Persistence):
    """
    Classe définissant le stockage d'une valeur unique réelle (float) par pas.

    Le type de base peut être changé par la méthode "basetype", mais il faut que
    le nouveau type de base soit compatible avec les types par éléments de
    numpy. On peut même utiliser cette classe pour stocker des vecteurs/listes
    ou des matrices comme dans les classes suivantes, mais c'est déconseillé
    pour conserver une signification claire des noms.
    """
    def __init__(self, name="", unit="", basetype = float):
        Persistence.__init__(self, name, unit, basetype)

class OneIndex(Persistence):
    """
    Classe définissant le stockage d'une valeur unique entière (int) par pas.
    """
    def __init__(self, name="", unit="", basetype = int):
        Persistence.__init__(self, name, unit, basetype)

class OneVector(Persistence):
    """
    Classe de stockage d'une liste de valeurs numériques homogènes par pas. Ne
    pas utiliser cette classe pour des données hétérogènes, mais "OneList".
    """
    def __init__(self, name="", unit="", basetype = numpy.ravel):
        Persistence.__init__(self, name, unit, basetype)

class OneMatrix(Persistence):
    """
    Classe de stockage d'une matrice de valeurs (numpy.matrix) par pas.
    """
    def __init__(self, name="", unit="", basetype = numpy.matrix):
        Persistence.__init__(self, name, unit, basetype)

class OneList(Persistence):
    """
    Classe de stockage d'une liste de valeurs hétérogènes (list) par pas. Ne pas
    utiliser cette classe pour des données numériques homogènes, mais
    "OneVector".
    """
    def __init__(self, name="", unit="", basetype = list):
        Persistence.__init__(self, name, unit, basetype)

def NoType( value ):
    "Fonction transparente, sans effet sur son argument"
    return value

class OneNoType(Persistence):
    """
    Classe de stockage d'un objet sans modification (cast) de type. Attention,
    selon le véritable type de l'objet stocké à chaque pas, les opérations
    arithmétiques à base de numpy peuvent être invalides ou donner des résultats
    inattendus. Cette classe n'est donc à utiliser qu'à bon escient
    volontairement, et pas du tout par défaut.
    """
    def __init__(self, name="", unit="", basetype = NoType):
        Persistence.__init__(self, name, unit, basetype)

# ==============================================================================
class CompositePersistence(object):
    """
    Structure de stockage permettant de rassembler plusieurs objets de
    persistence.

    Des objets par défaut sont prévus, et des objets supplémentaires peuvent
    être ajoutés.
    """
    def __init__(self, name="", defaults=True):
        """
        name : nom courant

        La gestion interne des données est exclusivement basée sur les variables
        initialisées ici (qui ne sont pas accessibles depuis l'extérieur des
        objets comme des attributs) :
        __StoredObjects : objets de type persistence collectés dans cet objet
        """
        self.__name = str(name)
        #
        self.__StoredObjects = {}
        #
        # Definition des objets par defaut
        # --------------------------------
        if defaults:
            self.__StoredObjects["Informations"]     = OneNoType("Informations")
            self.__StoredObjects["Background"]       = OneVector("Background", basetype=numpy.array)
            self.__StoredObjects["BackgroundError"]  = OneMatrix("BackgroundError")
            self.__StoredObjects["Observation"]      = OneVector("Observation", basetype=numpy.array)
            self.__StoredObjects["ObservationError"] = OneMatrix("ObservationError")
            self.__StoredObjects["Analysis"]         = OneVector("Analysis", basetype=numpy.array)
            self.__StoredObjects["AnalysisError"]    = OneMatrix("AnalysisError")
            self.__StoredObjects["Innovation"]       = OneVector("Innovation", basetype=numpy.array)
            self.__StoredObjects["KalmanGainK"]      = OneMatrix("KalmanGainK")
            self.__StoredObjects["OperatorH"]        = OneMatrix("OperatorH")
            self.__StoredObjects["RmsOMA"]           = OneScalar("RmsOMA")
            self.__StoredObjects["RmsOMB"]           = OneScalar("RmsOMB")
            self.__StoredObjects["RmsBMA"]           = OneScalar("RmsBMA")
        #

    def store(self, name=None, value=None, **kwargs):
        """
        Stockage d'une valeur "value" pour le "step" dans la variable "name".
        """
        if name is None: raise ValueError("Storable object name is required for storage.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in storable objects."%name)
        self.__StoredObjects[name].store( value=value, **kwargs )

    def add_object(self, name=None, persistenceType=Persistence, basetype=None ):
        """
        Ajoute dans les objets stockables un nouvel objet défini par son nom, son
        type de Persistence et son type de base à chaque pas.
        """
        if name is None: raise ValueError("Object name is required for adding an object.")
        if name in self.__StoredObjects.keys():
            raise ValueError("An object with the same name '%s' already exists in storable objects. Choose another one."%name)
        if basetype is None:
            self.__StoredObjects[name] = persistenceType( name=str(name) )
        else:
            self.__StoredObjects[name] = persistenceType( name=str(name), basetype=basetype )

    def get_object(self, name=None ):
        """
        Renvoie l'objet de type Persistence qui porte le nom demandé.
        """
        if name is None: raise ValueError("Object name is required for retrieving an object.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in stored objects."%name)
        return self.__StoredObjects[name]

    def set_object(self, name=None, objet=None ):
        """
        Affecte directement un 'objet' qui porte le nom 'name' demandé.
        Attention, il n'est pas effectué de vérification sur le type, qui doit
        comporter les méthodes habituelles de Persistence pour que cela
        fonctionne.
        """
        if name is None: raise ValueError("Object name is required for setting an object.")
        if name in self.__StoredObjects.keys():
            raise ValueError("An object with the same name '%s' already exists in storable objects. Choose another one."%name)
        self.__StoredObjects[name] = objet

    def del_object(self, name=None ):
        """
        Supprime un objet de la liste des objets stockables.
        """
        if name is None: raise ValueError("Object name is required for retrieving an object.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in stored objects."%name)
        del self.__StoredObjects[name]

    # ---------------------------------------------------------
    # Méthodes d'accès de type dictionnaire
    def __getitem__(self, name=None ):
        "x.__getitem__(y) <==> x[y]"
        return self.get_object( name )

    def __setitem__(self, name=None, objet=None ):
        "x.__setitem__(i, y) <==> x[i]=y"
        self.set_object( name, objet )

    def keys(self):
        "D.keys() -> list of D's keys"
        return self.get_stored_objects(hideVoidObjects = False)

    def values(self):
        "D.values() -> list of D's values"
        return self.__StoredObjects.values()

    def items(self):
        "D.items() -> list of D's (key, value) pairs, as 2-tuples"
        return self.__StoredObjects.items()

    # ---------------------------------------------------------
    def get_stored_objects(self, hideVoidObjects = False):
        "Renvoie la liste des objets présents"
        objs = self.__StoredObjects.keys()
        if hideVoidObjects:
            usedObjs = []
            for k in objs:
                try:
                    if len(self.__StoredObjects[k]) > 0: usedObjs.append( k )
                finally:
                    pass
            objs = usedObjs
        objs = sorted(objs)
        return objs

    # ---------------------------------------------------------
    def save_composite(self, filename=None, mode="pickle", compress="gzip"):
        """
        Enregistre l'objet dans le fichier indiqué selon le "mode" demandé,
        et renvoi le nom du fichier
        """
        if filename is None:
            if compress == "gzip":
                filename = os.tempnam( os.getcwd(), 'dacp' ) + ".pkl.gz"
            elif compress == "bzip2":
                filename = os.tempnam( os.getcwd(), 'dacp' ) + ".pkl.bz2"
            else:
                filename = os.tempnam( os.getcwd(), 'dacp' ) + ".pkl"
        else:
            filename = os.path.abspath( filename )
        #
        if mode == "pickle":
            if compress == "gzip":
                output = gzip.open( filename, 'wb')
            elif compress == "bzip2":
                output = bz2.BZ2File( filename, 'wb')
            else:
                output = open( filename, 'wb')
            pickle.dump(self, output)
            output.close()
        else:
            raise ValueError("Save mode '%s' unknown. Choose another one."%mode)
        #
        return filename

    def load_composite(self, filename=None, mode="pickle", compress="gzip"):
        """
        Recharge un objet composite sauvé en fichier
        """
        if filename is None:
            raise ValueError("A file name if requested to load a composite.")
        else:
            filename = os.path.abspath( filename )
        #
        if mode == "pickle":
            if compress == "gzip":
                pkl_file = gzip.open( filename, 'rb')
            elif compress == "bzip2":
                pkl_file = bz2.BZ2File( filename, 'rb')
            else:
                pkl_file = open(filename, 'rb')
            output = pickle.load(pkl_file)
            for k in output.keys():
                self[k] = output[k]
        else:
            raise ValueError("Load mode '%s' unknown. Choose another one."%mode)
        #
        return filename

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
