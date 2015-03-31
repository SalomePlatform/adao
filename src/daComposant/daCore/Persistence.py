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
    D�finit des outils de persistence et d'enregistrement de s�ries de valeurs
    pour analyse ult�rieure ou utilisation de calcul.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import numpy, copy

from PlatformInfo import PathManagement ; PathManagement()

# ==============================================================================
class Persistence:
    """
    Classe g�n�rale de persistence d�finissant les accesseurs n�cessaires
    (Template)
    """
    def __init__(self, name="", unit="", basetype=str):
        """
        name : nom courant
        unit : unit�
        basetype : type de base de l'objet stock� � chaque pas
        
        La gestion interne des donn�es est exclusivement bas�e sur les variables
        initialis�es ici (qui ne sont pas accessibles depuis l'ext�rieur des
        objets comme des attributs) :
        __basetype : le type de base de chaque valeur, sous la forme d'un type
                     permettant l'instanciation ou le casting Python 
        __values : les valeurs de stockage. Par d�faut, c'est None
        """
        self.__name = str(name)
        self.__unit = str(unit)
        #
        self.__basetype = basetype
        #
        self.__values = []
        self.__tags   = []
        #
        self.__dynamic  = False
        #
        self.__dataobservers = []
    
    def basetype(self, basetype=None):
        """
        Renvoie ou met en place le type de base des objets stock�s
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
        Renvoie la taille sous forme numpy du dernier objet stock�. Si c'est un
        objet numpy, renvoie le shape. Si c'est un entier, un flottant, un
        complexe, renvoie 1. Si c'est une liste ou un dictionnaire, renvoie la
        longueur. Par d�faut, renvoie 1.
        """
        if len(self.__values) > 0:
            if self.__basetype in [numpy.matrix, numpy.array, numpy.ravel]:
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
        msg  = "   Index        Value   Tags\n"
        for i,v in enumerate(self.__values):
            msg += "  i=%05i  %10s   %s\n"%(i,v,self.__tags[i])
        return msg
    
    def __len__(self):
        return len(self.__values)
    
    def __getitem__(self, index=None ):
        return copy.copy(self.__values[index])
    
    def count(self, value):
        return self.__values.count(value)
    
    def index(self, value, start=0, stop=None):
        if stop is None : stop = len(self.__values)
        return self.__values.index(value, start, stop)

    # ---------------------------------------------------------
    def __filteredIndexes(self, **kwargs):
        __indexOfFilteredItems = range(len(self.__tags))
        __filteringKwTags = kwargs.keys()
        if len(__filteringKwTags) > 0:
            for tagKey in __filteringKwTags:
                __tmp = []
                for i in __indexOfFilteredItems:
                    if self.__tags[i].has_key(tagKey):
                        if self.__tags[i][tagKey] == kwargs[tagKey]:
                            __tmp.append( i )
                        elif isinstance(kwargs[tagKey],(list,tuple)) and self.__tags[i][tagKey] in kwargs[tagKey]:
                            __tmp.append( i )
                __indexOfFilteredItems = __tmp
                if len(__indexOfFilteredItems) == 0: break
        return __indexOfFilteredItems

    # ---------------------------------------------------------
    def values(self, **kwargs):
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return [self.__values[i] for i in __indexOfFilteredItems]

    def keys(self, keyword=None , **kwargs):
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        __keys = []
        for i in __indexOfFilteredItems:
            if self.__tags[i].has_key( keyword ):
                __keys.append( self.__tags[i][keyword] )
            else:
                __keys.append( None )
        return __keys

    def items(self, keyword=None , **kwargs):
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        __pairs = []
        for i in __indexOfFilteredItems:
            if self.__tags[i].has_key( keyword ):
                __pairs.append( [self.__tags[i][keyword], self.__values[i]] )
            else:
                __pairs.append( [None, self.__values[i]] )
        return __pairs

    def tagkeys(self):
        __allKeys = []
        for dicotags in self.__tags:
            __allKeys.extend( dicotags.keys() )
        __allKeys = list(set(__allKeys))
        __allKeys.sort()
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
        if item is None:
            __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        else:
            __indexOfFilteredItems = [item,]
        #
        # Dans le cas o� la sortie donne les valeurs d'un "outputTag"
        if outputTag is not None and type(outputTag) is str :
            outputValues = []
            for index in __indexOfFilteredItems:
                if outputTag in self.__tags[index].keys():
                    outputValues.append( self.__tags[index][outputTag] )
            outputValues = list(set(outputValues))
            outputValues.sort()
            return outputValues
        #
        # Dans le cas o� la sortie donne les tags satisfaisants aux conditions
        else:
            if withValues:
                return [self.__tags[index] for index in __indexOfFilteredItems]
            else:
                allTags = {}
                for index in __indexOfFilteredItems:
                    allTags.update( self.__tags[index] )
                allKeys = allTags.keys()
                allKeys.sort()
                return allKeys

    # ---------------------------------------------------------
    # Pour compatibilite
    def stepnumber(self):
        return len(self.__values)

    # Pour compatibilite
    def stepserie(self, **kwargs):
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return __indexOfFilteredItems

    # ---------------------------------------------------------
    def means(self):
        """
        Renvoie la s�rie, contenant � chaque pas, la valeur moyenne des donn�es
        au pas. Il faut que le type de base soit compatible avec les types
        �l�mentaires numpy.
        """
        try:
            return [numpy.matrix(item).mean() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stds(self, ddof=0):
        """
        Renvoie la s�rie, contenant � chaque pas, l'�cart-type des donn�es
        au pas. Il faut que le type de base soit compatible avec les types
        �l�mentaires numpy.
        
        ddof : c'est le nombre de degr�s de libert� pour le calcul de
               l'�cart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
        """
        try:
            if numpy.version.version >= '1.1.0':
                return [numpy.matrix(item).std(ddof=ddof) for item in self.__values]
            else:
                return [numpy.matrix(item).std() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def sums(self):
        """
        Renvoie la s�rie, contenant � chaque pas, la somme des donn�es au pas.
        Il faut que le type de base soit compatible avec les types �l�mentaires
        numpy.
        """
        try:
            return [numpy.matrix(item).sum() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def mins(self):
        """
        Renvoie la s�rie, contenant � chaque pas, le minimum des donn�es au pas.
        Il faut que le type de base soit compatible avec les types �l�mentaires
        numpy.
        """
        try:
            return [numpy.matrix(item).min() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def maxs(self):
        """
        Renvoie la s�rie, contenant � chaque pas, la maximum des donn�es au pas.
        Il faut que le type de base soit compatible avec les types �l�mentaires
        numpy.
        """
        try:
            return [numpy.matrix(item).max() for item in self.__values]
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
        #
        # V�rification de la disponibilit� du module Gnuplot
        try:
            import Gnuplot
            self.__gnuplot = Gnuplot
        except:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # V�rification et compl�ments sur les param�tres d'entr�e
        if persist:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -persist -geometry '+geometry
        else:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -geometry '+geometry
        if ltitle is None:
            ltitle = ""
        self.__g = self.__gnuplot.Gnuplot() # persist=1
        self.__g('set terminal '+self.__gnuplot.GnuplotOpts.default_term)
        self.__g('set style data lines')
        self.__g('set grid')
        self.__g('set autoscale')
        self.__g('set xlabel "'+str(xlabel).encode('ascii','replace')+'"')
        self.__g('set ylabel "'+str(ylabel).encode('ascii','replace')+'"')
        self.__title  = title
        self.__ltitle = ltitle
        self.__pause  = pause

    def plots(self, item=None, step=None,
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
        Renvoie un affichage de la valeur � chaque pas, si elle est compatible
        avec un affichage Gnuplot (donc essentiellement un vecteur). Si
        l'argument "step" existe dans la liste des pas de stockage effectu�s,
        renvoie l'affichage de la valeur stock�e � ce pas "step". Si l'argument
        "item" est correct, renvoie l'affichage de la valeur stock�e au num�ro
        "item". Par d�faut ou en l'absence de "step" ou "item", renvoie un
        affichage successif de tous les pas.

        Arguments :
            - step     : valeur du pas � afficher
            - item     : index de la valeur � afficher
            - steps    : liste unique des pas de l'axe des X, ou None si c'est
                         la num�rotation par d�faut
            - title    : base du titre g�n�ral, qui sera automatiquement
                         compl�t�e par la mention du pas
            - xlabel   : label de l'axe des X
            - ylabel   : label de l'axe des Y
            - ltitle   : titre associ� au vecteur trac�
            - geometry : taille en pixels de la fen�tre et position du coin haut
                         gauche, au format X11 : LxH+X+Y (d�faut : 600x400)
            - filename : base de nom de fichier Postscript pour une sauvegarde,
                         qui est automatiquement compl�t�e par le num�ro du
                         fichier calcul� par incr�ment simple de compteur
            - dynamic  : effectue un affichage des valeurs � chaque stockage
                         (au-del� du second). La m�thode "plots" permet de
                         d�clarer l'affichage dynamique, et c'est la m�thode
                         "__replots" qui est utilis�e pour l'effectuer
            - persist  : bool�en indiquant que la fen�tre affich�e sera
                         conserv�e lors du passage au dessin suivant
                         Par d�faut, persist = False
            - pause    : bool�en indiquant une pause apr�s chaque trac�, et
                         attendant un Return
                         Par d�faut, pause = True
        """
        import os
        if not self.__dynamic:
            self.__preplots(title, xlabel, ylabel, ltitle, geometry, persist, pause )
            if dynamic:
                self.__dynamic = True
                if len(self.__values) == 0: return 0
        #
        # Trac� du ou des vecteurs demand�s
        indexes = []
        if step is not None and step < len(self.__values):
            indexes.append(step)
        elif item is not None and item < len(self.__values):
            indexes.append(item)
        else:
            indexes = indexes + range(len(self.__values))
        #
        i = -1
        for index in indexes:
            self.__g('set title  "'+str(title).encode('ascii','replace')+' (pas '+str(index)+')"')
            if ( type(steps) is list ) or ( type(steps) is type(numpy.array([])) ):
                Steps = list(steps)
            else:
                Steps = range(len(self.__values[index]))
            #
            self.__g.plot( self.__gnuplot.Data( Steps, self.__values[index], title=ltitle ) )
            #
            if filename != "":
                i += 1
                stepfilename = "%s_%03i.ps"%(filename,i)
                if os.path.isfile(stepfilename):
                    raise ValueError("Error: a file with this name \"%s\" already exists."%stepfilename)
                self.__g.hardcopy(filename=stepfilename, color=1)
            if self.__pause:
                raw_input('Please press return to continue...\n')

    def __replots(self):
        """
        Affichage dans le cas du suivi dynamique de la variable
        """
        if self.__dynamic and len(self.__values) < 2: return 0
        #
        self.__g('set title  "'+str(self.__title).encode('ascii','replace'))
        Steps = range(len(self.__values))
        self.__g.plot( self.__gnuplot.Data( Steps, self.__values, title=self.__ltitle ) )
        #
        if self.__pause:
            raw_input('Please press return to continue...\n')

    # ---------------------------------------------------------
    def mean(self):
        """
        Renvoie la moyenne sur toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        """
        try:
            if self.__basetype in [int, float]:
                return float( numpy.array(self.__values).mean() )
            else:
                return numpy.array(self.__values).mean(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def std(self, ddof=0):
        """
        Renvoie l'�cart-type de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        
        ddof : c'est le nombre de degr�s de libert� pour le calcul de
               l'�cart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
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
        les types �l�mentaires numpy.
        """
        try:
            return numpy.array(self.__values).sum(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def min(self):
        """
        Renvoie le minimum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        """
        try:
            return numpy.array(self.__values).min(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def max(self):
        """
        Renvoie le maximum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        """
        try:
            return numpy.array(self.__values).max(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    def cumsum(self):
        """
        Renvoie la somme cumul�e de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        """
        try:
            return numpy.array(self.__values).cumsum(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    # On pourrait aussi utiliser les autres attributs d'une "matrix", comme
    # "tofile", "min"...

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
        Renvoie un affichage unique pour l'ensemble des valeurs � chaque pas, si
        elles sont compatibles avec un affichage Gnuplot (donc essentiellement
        un vecteur). Si l'argument "step" existe dans la liste des pas de
        stockage effectu�s, renvoie l'affichage de la valeur stock�e � ce pas
        "step". Si l'argument "item" est correct, renvoie l'affichage de la
        valeur stock�e au num�ro "item".

        Arguments :
            - steps    : liste unique des pas de l'axe des X, ou None si c'est
                         la num�rotation par d�faut
            - title    : base du titre g�n�ral, qui sera automatiquement
                         compl�t�e par la mention du pas
            - xlabel   : label de l'axe des X
            - ylabel   : label de l'axe des Y
            - ltitle   : titre associ� au vecteur trac�
            - geometry : taille en pixels de la fen�tre et position du coin haut
                         gauche, au format X11 : LxH+X+Y (d�faut : 600x400)
            - filename : nom de fichier Postscript pour une sauvegarde
            - persist  : bool�en indiquant que la fen�tre affich�e sera
                         conserv�e lors du passage au dessin suivant
                         Par d�faut, persist = False
            - pause    : bool�en indiquant une pause apr�s chaque trac�, et
                         attendant un Return
                         Par d�faut, pause = True
        """
        #
        # V�rification de la disponibilit� du module Gnuplot
        try:
            import Gnuplot
            self.__gnuplot = Gnuplot
        except:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # V�rification et compl�ments sur les param�tres d'entr�e
        if persist:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -persist -geometry '+geometry
        else:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -geometry '+geometry
        if ltitle is None:
            ltitle = ""
        if ( type(steps) is list ) or ( type(steps) is type(numpy.array([])) ):
            Steps = list(steps)
        else:
            Steps = range(len(self.__values[0]))
        self.__g = self.__gnuplot.Gnuplot() # persist=1
        self.__g('set terminal '+self.__gnuplot.GnuplotOpts.default_term)
        self.__g('set style data lines')
        self.__g('set grid')
        self.__g('set autoscale')
        self.__g('set title  "'+str(title).encode('ascii','replace') +'"')
        self.__g('set xlabel "'+str(xlabel).encode('ascii','replace')+'"')
        self.__g('set ylabel "'+str(ylabel).encode('ascii','replace')+'"')
        #
        # Trac� du ou des vecteurs demand�s
        indexes = range(len(self.__values))
        self.__g.plot( self.__gnuplot.Data( Steps, self.__values[indexes.pop(0)], title=ltitle+" (pas 0)" ) )
        for index in indexes:
            self.__g.replot( self.__gnuplot.Data( Steps, self.__values[index], title=ltitle+" (pas %i)"%index ) )
        #
        if filename != "":
            self.__g.hardcopy(filename=filename, color=1)
        if pause:
            raw_input('Please press return to continue...\n')

    # ---------------------------------------------------------
    def setDataObserver(self,
        HookFunction   = None,
        HookParameters = None,
        Scheduler      = None,
        ):
        """
        Association � la variable d'un triplet d�finissant un observer
        
        Le Scheduler attendu est une fr�quence, une simple liste d'index ou un
        xrange des index.
        """
        #
        # V�rification du Scheduler
        # -------------------------
        maxiter = int( 1e9 )
        if type(Scheduler) is int:    # Consid�r� comme une fr�quence � partir de 0
            Schedulers = xrange( 0, maxiter, int(Scheduler) )
        elif type(Scheduler) is xrange: # Consid�r� comme un it�rateur
            Schedulers = Scheduler
        elif type(Scheduler) is list: # Consid�r� comme des index explicites
            Schedulers = map( long, Scheduler )
        else:                         # Dans tous les autres cas, activ� par d�faut
            Schedulers = xrange( 0, maxiter )
        #
        # Stockage interne de l'observer dans la variable
        # -----------------------------------------------
        self.__dataobservers.append( [HookFunction, HookParameters, Schedulers] )

    def removeDataObserver(self,
        HookFunction   = None,
        ):
        """
        Suppression d'un observer nomm� sur la variable.
        
        On peut donner dans HookFunction la meme fonction que lors de la
        d�finition, ou un simple string qui est le nom de la fonction.
        
        """
        if hasattr(HookFunction,"func_name"):
            name = str( HookFunction.func_name )
        elif type(HookFunction) is str:
            name = str( HookFunction )
        else:
            name = None
        #
        i = -1
        index_to_remove = []
        for [hf, hp, hs] in self.__dataobservers:
            i = i + 1
            if name is hf.func_name: index_to_remove.append( i )
        index_to_remove.reverse()
        for i in index_to_remove:
                self.__dataobservers.pop( i )

# ==============================================================================
class OneScalar(Persistence):
    """
    Classe d�finissant le stockage d'une valeur unique r�elle (float) par pas.

    Le type de base peut �tre chang� par la m�thode "basetype", mais il faut que
    le nouveau type de base soit compatible avec les types par �l�ments de
    numpy. On peut m�me utiliser cette classe pour stocker des vecteurs/listes
    ou des matrices comme dans les classes suivantes, mais c'est d�conseill�
    pour conserver une signification claire des noms.
    """
    def __init__(self, name="", unit="", basetype = float):
        Persistence.__init__(self, name, unit, basetype)

class OneVector(Persistence):
    """
    Classe de stockage d'une liste de valeurs num�riques homog�nes par pas. Ne
    pas utiliser cette classe pour des donn�es h�t�rog�nes, mais "OneList".
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
    Classe de stockage d'une liste de valeurs h�t�rog�nes (list) par pas. Ne pas
    utiliser cette classe pour des donn�es num�riques homog�nes, mais
    "OneVector".
    """
    def __init__(self, name="", unit="", basetype = list):
        Persistence.__init__(self, name, unit, basetype)

def NoType( value ): return value

class OneNoType(Persistence):
    """
    Classe de stockage d'un objet sans modification (cast) de type. Attention,
    selon le v�ritable type de l'objet stock� � chaque pas, les op�rations
    arithm�tiques � base de numpy peuvent �tre invalides ou donner des r�sultats
    inattendus. Cette classe n'est donc � utiliser qu'� bon escient
    volontairement, et pas du tout par d�faut.
    """
    def __init__(self, name="", unit="", basetype = NoType):
        Persistence.__init__(self, name, unit, basetype)

# ==============================================================================
class CompositePersistence:
    """
    Structure de stockage permettant de rassembler plusieurs objets de
    persistence.
    
    Des objets par d�faut sont pr�vus, et des objets suppl�mentaires peuvent
    �tre ajout�s.
    """
    def __init__(self, name="", defaults=True):
        """
        name : nom courant
        
        La gestion interne des donn�es est exclusivement bas�e sur les variables
        initialis�es ici (qui ne sont pas accessibles depuis l'ext�rieur des
        objets comme des attributs) :
        __StoredObjects : objets de type persistence collect�s dans cet objet
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
        Ajoute dans les objets stockables un nouvel objet d�fini par son nom, son
        type de Persistence et son type de base � chaque pas.
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
        Renvoie l'objet de type Persistence qui porte le nom demand�.
        """
        if name is None: raise ValueError("Object name is required for retrieving an object.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in stored objects."%name)
        return self.__StoredObjects[name]

    def set_object(self, name=None, objet=None ):
        """
        Affecte directement un 'objet' qui porte le nom 'name' demand�.
        Attention, il n'est pas effectu� de v�rification sur le type, qui doit
        comporter les m�thodes habituelles de Persistence pour que cela
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
    # M�thodes d'acc�s de type dictionnaire
    def __getitem__(self, name=None ):
        return self.get_object( name )

    def __setitem__(self, name=None, objet=None ):
        self.set_object( name, objet )

    def keys(self):
        return self.get_stored_objects(hideVoidObjects = False)

    def values(self):
        return self.__StoredObjects.values()

    def items(self):
        return self.__StoredObjects.items()

    # ---------------------------------------------------------
    def get_stored_objects(self, hideVoidObjects = False):
        objs = self.__StoredObjects.keys()
        if hideVoidObjects:
            usedObjs = []
            for k in objs:
                try:
                    if len(self.__StoredObjects[k]) > 0: usedObjs.append( k )
                except:
                    pass
            objs = usedObjs
        objs.sort()
        return objs

    # ---------------------------------------------------------
    def save_composite(self, filename=None, mode="pickle", compress="gzip"):
        """
        Enregistre l'objet dans le fichier indiqu� selon le "mode" demand�,
        et renvoi le nom du fichier
        """
        import os
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
        import cPickle
        if mode == "pickle":
            if compress == "gzip":
                import gzip
                output = gzip.open( filename, 'wb')
            elif compress == "bzip2":
                import bz2
                output = bz2.BZ2File( filename, 'wb')
            else:
                output = open( filename, 'wb')
            cPickle.dump(self, output)
            output.close()
        else:
            raise ValueError("Save mode '%s' unknown. Choose another one."%mode)
        #
        return filename

    def load_composite(self, filename=None, mode="pickle", compress="gzip"):
        """
        Recharge un objet composite sauv� en fichier
        """
        import os
        if filename is None:
            raise ValueError("A file name if requested to load a composite.")
        else:
            filename = os.path.abspath( filename )
        #
        import cPickle
        if mode == "pickle":
            if compress == "gzip":
                import gzip
                pkl_file = gzip.open( filename, 'rb')
            elif compress == "bzip2":
                import bz2
                pkl_file = bz2.BZ2File( filename, 'rb')
            else:
                pkl_file = open(filename, 'rb')
            output = cPickle.load(pkl_file)
            for k in output.keys():
                self[k] = output[k]
        else:
            raise ValueError("Load mode '%s' unknown. Choose another one."%mode)
        #
        return filename

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
