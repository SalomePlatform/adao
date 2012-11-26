#-*-coding:iso-8859-1-*-
#
# Copyright (C) 2008-2012 EDF R&D
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
    D�finit des outils de persistence et d'enregistrement de s�ries de valeurs
    pour analyse ult�rieure ou utilisation de calcul.
"""
__author__ = "Jean-Philippe ARGAUD"

import numpy

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
        __step   : num�rotation par d�faut du pas courant
        __basetype : le type de base de chaque valeur, sous la forme d'un type
                     permettant l'instanciation ou le casting Python 
        __steps  : les pas de stockage. Par d�faut, c'est __step
        __values : les valeurs de stockage. Par d�faut, c'est None
        """
        self.__name = str(name)
        self.__unit = str(unit)
        #
        self.__step     = -1
        self.__basetype = basetype
        #
        self.__steps    = []
        self.__values   = []
        self.__tags     = []
        self.__tagkeys  = {}
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

    def store(self, value=None, step=None, tags={}):
        """
        Stocke une valeur � un pas. Une instanciation est faite avec le type de
        base pour stocker l'objet. Si le pas n'est pas fournit, on utilise
        l'�tape de stockage comme valeur de pas.
        """
        if value is None: raise ValueError("Value argument required")
        self.__step += 1
        if step is not None:
            self.__steps.append(step)
        else:
            self.__steps.append(self.__step)
        #
        self.__values.append(self.__basetype(value))
        #
        self.__tags.append(   dict(tags))
        self.__tagkeys.update(dict(tags))
        #
        if self.__dynamic: self.__replots()
        for hook, parameters, scheduler in self.__dataobservers:
            if self.__step in scheduler:
                hook( self, parameters )

    def pop(self, item=None, step=None):
        """
        Retire une valeur enregistree. Par defaut, retire par le numero d'item,
        sinon cherche le step demande et le retire s'il existe. Sans argument,
        retire le dernier objet enregistre.
        Attention, la liste des cles "tagkeys" n'est pas mise a jour.
        """
        if item is not None:
            index = int(item)
            self.__steps.pop(index)
            self.__values.pop(index)
            self.__tags.pop(index)
        elif step is not None:
            index = int(self.__steps.index(int(step)))
            self.__steps.pop(index)
            self.__values.pop(index)
            self.__tags.pop(index)
        else:
            self.__steps.pop()
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
            if self.__basetype in [numpy.matrix, numpy.array]:
                return self.__values[-1].shape
            elif self.__basetype in [int, float]:
                return (1,)
            elif self.__basetype in [list, dict]:
                return (len(self.__values[-1]),)
            else:
                return (1,)
        else:
            raise ValueError("Object has no shape before its first storage")

    def __len__(self):
        """
        Renvoie le nombre d'�l�ments dans un s�quence ou la plus grande
        dimension d'une matrice
        """
        return max( self.shape() )

    # ---------------------------------------------------------
    def itemserie(self, item=None, step=None, tags=None,
                        allSteps=False):
        """
        Les "item" sont les index de la liste des pas de "step". Ils sont
        renvoy�s par cette fonction selon les filtres d�finis par les mots-cl�s.
        
        Les comportements sont les suivants :
            - Renvoie par d�faut toute la liste des index.
            - Si l'argument "item" est valide, renvoie uniquement cet index.
            - Si l'argument "step" existe dans la liste des pas de stockage,
              renvoie le premier index (si allSteps=False) ou tous les index
              (si allSteps=True) de ce "step" dans les pas de stockage.
            - Si l'argument "tags" est un dictionnaire correct, renvoie les
              index des pas caract�ris�s par toutes les paires "tag/valeur" des
              tags indiqu�s, ou rien sinon.
        
        Cette m�thode est � vocation interne pour simplifier les acc�s aux pas
        par la m�thode "stepserie", aux attributs par la m�thode "tagserie" et
        aux valeurs par la m�thode "valueserie".
        """
        #
        # Cherche l'item demand�
        if item is not None and item < len(self.__steps):
            return [item,]
        #
        # Cherche le ou les items dont le "step" est demand�
        elif step is not None and step in self.__steps:
            if allSteps:
                allIndexes = []
                searchFrom = 0
                try:
                    while self.__steps.index(step,searchFrom) >= 0:
                        searchFrom = self.__steps.index(step,searchFrom)
                        allIndexes.append( searchFrom )
                        searchFrom +=1
                except ValueError, e:
                    pass
                return allIndexes
            else:
                return [self.__steps.index(step),]
        #
        # Cherche le ou les items dont les "tags" sont demand�s
        elif tags is not None and type(tags) is dict :
            allIndexes = []
            for i, attributs in enumerate(self.__tags):           # Boucle sur les attributs de chaque pas
                selection = True                                  # Booleen permettant de traiter la combinaison "ET" des tags
                for key in tags.keys():                           # Boucle sur tous les tags de filtrage
                    if key not in self.__tagkeys.keys(): continue # Passe au suivant s'il n'existe nulle part
                    if not( key in attributs.keys() and attributs[key] == tags[key] ):
                        selection = False
                if selection:
                    allIndexes.append(i)
            allIndexes = list(set(allIndexes))
            allIndexes.sort()
            return allIndexes
        #
        # Renvoie par d�faut tous les items valides
        else:
            return range(len(self.__steps))

    def stepserie(self, item=None, step=None, tags=None):
        """
        Les "step" sont les pas nomm�s de stockage. Par d�faut, s'il ne sont pas
        d�finis explicitement, ils sont identiques aux index de stockage. Ils
        sont renvoy�s par cette fonction selon les filtres d�finis par les
        mots-cl�s.
        
        Les comportements sont les suivants :
            - Renvoie par d�faut toute la liste des pas.
            - Si l'argument "item" est valide, renvoie le pas � cet index.
            - Si l'argument "step" existe dans la liste des pas, le renvoie.
            - Si l'argument "tags" est un dictionnaire correct, renvoie les pas
              caract�ris�s par toutes les paires "tag/valeur" des tags indiqu�s,
              ou rien sinon.
        """
        if item is not None and item < len(self.__steps):
            return self.__steps[item]
        elif step is not None and step in self.__steps:
            return step
        elif tags is not None:
            allIndexes = self.itemserie(tags = tags)
            return [self.__steps[index] for index in allIndexes]
        else:
            return self.__steps

    def valueserie(self, item=None, step=None, tags=None,
                         allSteps=False):
        """
        Les valeurs stock�es sont renvoy�es par cette fonction selon les filtres
        d�finis par les mots-cl�s.
        
        Les comportements sont les suivants :
            - Renvoie par d�faut toute la liste des valeurs.
            - Si l'argument "item" est valide, renvoie la valeur � cet index.
            - Si l'argument "step" existe dans la liste des pas de stockage,
              renvoie la premi�re valeur (si allSteps=False) ou toutes les
              valeurs (si allSteps=True).
            - Si l'argument "tags" est un dictionnaire correct, renvoie les
              valeurs aux pas caract�ris�s par toutes les paires "tag/valeur"
              des tags indiqu�s, ou rien sinon.
        """
        if item is not None and item < len(self.__values):
            return self.__values[item]
        elif step is not None:
            allIndexes = self.itemserie(step = step, allSteps = allSteps)
            if allSteps:
                return [self.__values[index] for index in allIndexes]
            else:
                return self.__values[allIndexes[0]]
        elif tags is not None:
            allIndexes = self.itemserie(tags = tags)
            return [self.__values[index] for index in allIndexes]
        else:
            return self.__values
    
    def tagserie(self, item=None, step=None, tags=None,
                       allSteps=False, withValues=False,
                       outputTag=None):
        """
        Les "tag" sont les attributs nomm�s, sous forme de paires "cl�/valeur",
        qu'il est possible d'associer avec chaque pas de stockage. Par d�faut,
        s'il ne sont pas d�finis explicitement, il n'y en a pas. Ils sont
        renvoy�s par cette fonction selon les filtres d�finis par les mots-cl�s.
        On obtient uniquement la liste des cl�s de tags avec "withValues=False"
        ou la liste des paires "cl�/valeurs" avec "withValues=True".
        
        On peut aussi obtenir les valeurs d'un tag satisfaisant aux conditions
        de filtrage en "item/step/tags" en donnant le nom du tag dans
        "outputTag".

        Les comportements sont les suivants :
            - Renvoie par d�faut toute la liste des tags.
            - Si l'argument "item" est valide, renvoie le tag � cet index.
            - Si l'argument "step" existe dans la liste des pas de stockage,
              renvoie les tags du premier pas (si allSteps=False) ou la liste
              des tags de tous les pas (si allSteps=True).
            - Si l'argument "tags" est un dictionnaire correct, renvoie les
              valeurs aux pas caract�ris�s par toutes les paires "tag/valeur"
              des tags indiqu�s, ou rien sinon.
        """
        #
        # Cherche tous les index satisfaisant les conditions
        allIndexes = self.itemserie(item = item, step = step, tags = tags, allSteps = allSteps)
        #
        # Dans le cas o� la sortie donne les valeurs d'un "outputTag"
        if outputTag is not None and type(outputTag) is str :
            outputValues = []
            for index in allIndexes:
                if outputTag in self.__tags[index].keys():
                    outputValues.append( self.__tags[index][outputTag] )
            outputValues = list(set(outputValues))
            outputValues.sort()
            return outputValues
        #
        # Dans le cas o� la sortie donne les tags satisfaisants aux conditions
        else:
            if withValues:
                return [self.__tags[index] for index in allIndexes]
            else:
                allTags = {}
                for index in allIndexes:
                    allTags.update( self.__tags[index] )
                allKeys = allTags.keys()
                allKeys.sort()
                return allKeys

    def stepnumber(self):
        """
        Renvoie le nombre de pas de stockage.
        """
        return len(self.__steps)

    # ---------------------------------------------------------
    # M�thodes d'acc�s de type dictionnaire
    def keys(self):
        return self.stepserie()

    def values(self):
        return self.valueserie()

    def items(self):
        pairs = []
        for i in xrange(self.stepnumber()):
            pairs.append( (self.stepserie(item=i), self.valueserie(item=i)) )
        return pairs

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
        if step is not None and step in self.__steps:
            indexes.append(self.__steps.index(step))
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
    Classe d�finissant le stockage d'une valeur unique r�elle (float) par pas
    
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
    Classe d�finissant le stockage d'une liste (list) de valeurs homog�nes par
    hypoth�se par pas. Pour �viter les confusions, ne pas utiliser la classe
    "OneVector" pour des donn�es h�t�rog�nes, mais bien "OneList".
    """
    def __init__(self, name="", unit="", basetype = list):
        Persistence.__init__(self, name, unit, basetype)

class OneMatrix(Persistence):
    """
    Classe d�finissant le stockage d'une matrice de valeurs (numpy.matrix) par
    pas
    """
    def __init__(self, name="", unit="", basetype = numpy.matrix):
        Persistence.__init__(self, name, unit, basetype)

class OneList(Persistence):
    """
    Classe d�finissant le stockage d'une liste de valeurs potentiellement
    h�t�rog�nes (list) par pas. Pour �viter les confusions, ne pas utiliser la
    classe "OneVector" pour des donn�es h�t�rog�nes, mais bien "OneList".
    """
    def __init__(self, name="", unit="", basetype = list):
        Persistence.__init__(self, name, unit, basetype)

def NoType( value ): return value

class OneNoType(Persistence):
    """
    Classe d�finissant le stockage d'un objet sans modification (cast) de type.
    Attention, selon le v�ritable type de l'objet stock� � chaque pas, les
    op�rations arithm�tiques � base de numpy peuvent �tre invalides ou donner
    des r�sultats inatendus. Cette classe n'est donc � utiliser qu'� bon escient
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

    def store(self, name=None, value=None, step=None, tags={}):
        """
        Stockage d'une valeur "value" pour le "step" dans la variable "name".
        """
        if name is None: raise ValueError("Storable object name is required for storage.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in storable objects."%name)
        self.__StoredObjects[name].store( value=value, step=step, tags=tags )

    def add_object(self, name=None, persistenceType=Persistence, basetype=numpy.array ):
        """
        Ajoute dans les objets stockables un nouvel objet d�fini par son nom, son
        type de Persistence et son type de base � chaque pas.
        """
        if name is None: raise ValueError("Object name is required for adding an object.")
        if name in self.__StoredObjects.keys():
            raise ValueError("An object with the same name '%s' already exists in storable objects. Choose another one."%name)
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

    print "======> Un flottant"
    OBJET_DE_TEST = OneScalar("My float", unit="cm")
    OBJET_DE_TEST.store( 5.)
    OBJET_DE_TEST.store(-5.)
    OBJET_DE_TEST.store( 1.)
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas :"
    print "  La moyenne        :", OBJET_DE_TEST.means()
    print "  L'�cart-type      :", OBJET_DE_TEST.stds()
    print "  La somme          :", OBJET_DE_TEST.sums()
    print "  Le minimum        :", OBJET_DE_TEST.mins()
    print "  Le maximum        :", OBJET_DE_TEST.maxs()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "  La somme cumul�e  :", OBJET_DE_TEST.cumsum()
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Un flottant"
    OBJET_DE_TEST = OneScalar("My float", unit="cm")
    OBJET_DE_TEST.store( 5., step="azerty")
    OBJET_DE_TEST.store(-5., step="poiuyt")
    OBJET_DE_TEST.store( 1., step="azerty")
    OBJET_DE_TEST.store( 0., step="xxxxxx")
    OBJET_DE_TEST.store( 5., step="poiuyt")
    OBJET_DE_TEST.store(-5., step="azerty")
    OBJET_DE_TEST.store( 1., step="poiuyt")
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Premier index       :", OBJET_DE_TEST.valueserie( step = "azerty", allSteps = False )
    print "Valeurs identiques  :", OBJET_DE_TEST.valueserie( step = "azerty", allSteps = True )
    print "Premier index       :", OBJET_DE_TEST.valueserie( step = "poiuyt", allSteps = False )
    print "Valeurs identiques  :", OBJET_DE_TEST.valueserie( step = "poiuyt", allSteps = True )
    del OBJET_DE_TEST
    print

    print "======> Un entier"
    OBJET_DE_TEST = OneScalar("My int", unit="cm", basetype=int)
    OBJET_DE_TEST.store( 5 )
    OBJET_DE_TEST.store(-5 )
    OBJET_DE_TEST.store( 1.)
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas :"
    print "  La moyenne        :", OBJET_DE_TEST.means()
    print "  L'�cart-type      :", OBJET_DE_TEST.stds()
    print "  La somme          :", OBJET_DE_TEST.sums()
    print "  Le minimum        :", OBJET_DE_TEST.mins()
    print "  Le maximum        :", OBJET_DE_TEST.maxs()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "  La somme cumul�e  :", OBJET_DE_TEST.cumsum()
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Un bool�en"
    OBJET_DE_TEST = OneScalar("My bool", unit="", basetype=bool)
    OBJET_DE_TEST.store( True  )
    OBJET_DE_TEST.store( False )
    OBJET_DE_TEST.store( True  )
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Un vecteur de flottants"
    OBJET_DE_TEST = OneVector("My float vector", unit="cm")
    OBJET_DE_TEST.store( (5 , -5) )
    OBJET_DE_TEST.store( (-5, 5 ) )
    OBJET_DE_TEST.store( (1., 1.) )
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas :"
    print "  La moyenne        :", OBJET_DE_TEST.means()
    print "  L'�cart-type      :", OBJET_DE_TEST.stds()
    print "  La somme          :", OBJET_DE_TEST.sums()
    print "  Le minimum        :", OBJET_DE_TEST.mins()
    print "  Le maximum        :", OBJET_DE_TEST.maxs()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "  La somme cumul�e  :", OBJET_DE_TEST.cumsum()
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Une liste h�t�rog�ne"
    OBJET_DE_TEST = OneList("My list", unit="bool/cm")
    OBJET_DE_TEST.store( (True , -5) )
    OBJET_DE_TEST.store( (False,  5 ) )
    OBJET_DE_TEST.store( (True ,  1.) )
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas : attention, on peut les calculer car True=1, False=0, mais cela n'a pas de sens"
    print "  La moyenne        :", OBJET_DE_TEST.means()
    print "  L'�cart-type      :", OBJET_DE_TEST.stds()
    print "  La somme          :", OBJET_DE_TEST.sums()
    print "  Le minimum        :", OBJET_DE_TEST.mins()
    print "  Le maximum        :", OBJET_DE_TEST.maxs()
    print "Valeurs globales : attention, on peut les calculer car True=1, False=0, mais cela n'a pas de sens"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "  La somme cumul�e  :", OBJET_DE_TEST.cumsum()
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Utilisation directe de la classe Persistence"
    OBJET_DE_TEST = Persistence("My object", unit="", basetype=int )
    OBJET_DE_TEST.store( 1  )
    OBJET_DE_TEST.store( 3 )
    OBJET_DE_TEST.store( 7  )
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Utilisation des m�thodes d'acc�s de type dictionnaire"
    OBJET_DE_TEST = OneScalar("My int", unit="cm", basetype=int)
    for i in range(5):
        OBJET_DE_TEST.store( 7+i )
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    print "Les pas de stockage :", OBJET_DE_TEST.keys()
    print "Les valeurs         :", OBJET_DE_TEST.values()
    print "Les paires          :", OBJET_DE_TEST.items()
    OBJET_DE_TEST.pop(step=1)
    print "Les valeurs sans la 1:", OBJET_DE_TEST.values()
    OBJET_DE_TEST.pop(item=2)
    print "Les valeurs sans la 2:", OBJET_DE_TEST.values()
    del OBJET_DE_TEST
    print

    print "======> Persistence composite"
    OBJET_DE_TEST = CompositePersistence("My CompositePersistence")
    print "Objets stockables :", OBJET_DE_TEST.get_stored_objects()
    print "Objets actifs     :", OBJET_DE_TEST.get_stored_objects( hideVoidObjects = True )
    print "--> Stockage d'une valeur de Background"
    OBJET_DE_TEST.store("Background",numpy.zeros(5))
    print "Objets actifs     :", OBJET_DE_TEST.get_stored_objects( hideVoidObjects = True )
    print "--> Ajout d'un objet nouveau par defaut, de type vecteur numpy par pas"
    OBJET_DE_TEST.add_object("ValeursVectorielles")
    OBJET_DE_TEST.store("ValeursVectorielles",numpy.zeros(5))
    print "Objets actifs     :", OBJET_DE_TEST.get_stored_objects( hideVoidObjects = True )
    print "--> Ajout d'un objet nouveau de type liste par pas"
    OBJET_DE_TEST.add_object("ValeursList", persistenceType=OneList )
    OBJET_DE_TEST.store("ValeursList",range(5))
    print "Objets actifs     :", OBJET_DE_TEST.get_stored_objects( hideVoidObjects = True )
    print "--> Ajout d'un objet nouveau, de type vecteur string par pas"
    OBJET_DE_TEST.add_object("ValeursStr", persistenceType=Persistence, basetype=str )
    OBJET_DE_TEST.store("ValeursStr","IGN3")
    OBJET_DE_TEST.store("ValeursStr","c021")
    print "Les valeurs       :", OBJET_DE_TEST.get_object("ValeursStr").valueserie()
    print "Acces comme dict  :", OBJET_DE_TEST["ValeursStr"].stepserie()
    print "Acces comme dict  :", OBJET_DE_TEST["ValeursStr"].valueserie()
    print "Objets actifs     :", OBJET_DE_TEST.get_stored_objects( hideVoidObjects = True )
    print "--> Suppression d'un objet"
    OBJET_DE_TEST.del_object("ValeursVectorielles")
    print "Objets actifs     :", OBJET_DE_TEST.get_stored_objects( hideVoidObjects = True )
    print "--> Enregistrement de l'objet complet de Persistence composite"
    OBJET_DE_TEST.save_composite("composite.pkl", compress="None")
    print

    print "======> Affichage graphique d'objets stock�s"
    OBJET_DE_TEST = Persistence("My object", unit="", basetype=numpy.array)
    D = OBJET_DE_TEST
    vect1 = [1, 2, 1, 2, 1]
    vect2 = [-3, -3, 0, -3, -3]
    vect3 = [-1, 1, -5, 1, -1]
    vect4 = 100*[0.29, 0.97, 0.73, 0.01, 0.20]
    print "Stockage de 3 vecteurs de longueur identique"
    D.store(vect1)
    D.store(vect2)
    D.store(vect3)
    print "Affichage graphique de l'ensemble du stockage sur une m�me image"
    D.plot(
        title = "Tous les vecteurs",
        filename="vecteurs.ps",
        xlabel = "Axe X",
        ylabel = "Axe Y",
        pause = False )
    print "Stockage d'un quatri�me vecteur de longueur diff�rente"
    D.store(vect4)
    print "Affichage graphique s�par� du dernier stockage"
    D.plots(
        item  = 3,
        title = "Vecteurs",
        filename = "vecteur",
        xlabel = "Axe X",
        ylabel = "Axe Y",
        pause = False )
    print "Les images ont �t� stock�es en fichiers Postscript"
    print "Taille \"shape\" du dernier objet stock�",OBJET_DE_TEST.shape()
    print "Taille \"len\" du dernier objet stock�",len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Affichage graphique dynamique d'objets"
    OBJET_DE_TEST = Persistence("My object", unit="", basetype=float)
    D = OBJET_DE_TEST
    D.plots(
        dynamic = True,
        title   = "Valeur suivie",
        xlabel  = "Pas",
        ylabel  = "Valeur",
        pause   = False,
        )
    for i in range(1,11):
        D.store( i*i )
    print "Taille \"shape\" du dernier objet stock�",OBJET_DE_TEST.shape()
    print "Taille \"len\" du dernier objet stock�",len(OBJET_DE_TEST)
    print "Nombre d'objets stock�s",OBJET_DE_TEST.stepnumber()
    del OBJET_DE_TEST
    print

    print "======> Affectation simple d'observateurs dynamiques"
    def obs(var=None,info=None):
        print "  ---> Mise en oeuvre de l'observer"
        print "       var  =",var.valueserie(-1)
        print "       info =",info
    OBJET_DE_TEST = Persistence("My object", unit="", basetype=list)
    D = OBJET_DE_TEST
    D.setDataObserver( HookFunction = obs )
    for i in range(5):
        #�print
        print "Action de 1 observer sur la variable observ�e, �tape :",i
        D.store( [i, i, i] )
    del OBJET_DE_TEST
    print

    print "======> Affectation multiple d'observateurs dynamiques"
    def obs(var=None,info=None):
        print "  ---> Mise en oeuvre de l'observer"
        print "       var  =",var.valueserie(-1)
        print "       info =",info
    def obs_bis(var=None,info=None):
        print "  ---> Mise en oeuvre de l'observer"
        print "       var  =",var.valueserie(-1)
        print "       info =",info
    OBJET_DE_TEST = Persistence("My object", unit="", basetype=list)
    D = OBJET_DE_TEST
    D.setDataObserver(
        HookFunction   = obs,
        Scheduler      = [2, 4],
        HookParameters = "Premier observer",
        )
    D.setDataObserver(
        HookFunction   = obs,
        Scheduler      = xrange(1,3),
        HookParameters = "Second observer",
        )
    D.setDataObserver(
        HookFunction   = obs_bis,
        Scheduler      = range(1,3)+range(7,9),
        HookParameters = "Troisi�me observer",
        )
    for i in range(5):
        print "Action de 3 observers sur la variable observ�e, �tape :",i
        D.store( [i, i, i] )
    D.removeDataObserver(
        HookFunction   = obs,
        )
    for i in range(5,10):
        print "Action d'un seul observer sur la variable observ�e, �tape :",i
        D.store( [i, i, i] )
    del OBJET_DE_TEST
    print

    print "======> Utilisation des tags/attributs et stockage puis r�cup�ration de l'ensemble"
    OBJET_DE_TEST = CompositePersistence("My CompositePersistence", defaults=False)
    OBJET_DE_TEST.add_object("My ecarts", basetype = numpy.array)

    OBJET_DE_TEST.store( "My ecarts", numpy.arange(1,5),   tags = {"Camp":"Base","Carte":"IGN3","Niveau":1024,"Palier":"Premier"} )
    OBJET_DE_TEST.store( "My ecarts", numpy.arange(1,5)+1, tags = {"Camp":"Base","Carte":"IGN4","Niveau": 210,"Palier":"Premier"} )
    OBJET_DE_TEST.store( "My ecarts", numpy.arange(1,5)+2, tags = {"Camp":"Base","Carte":"IGN1","Niveau":1024} )
    OBJET_DE_TEST.store( "My ecarts", numpy.arange(1,5)+3, tags = {"Camp":"Sommet","Carte":"IGN2","Niveau":4024,"Palier":"Second","FullMap":True} )

    print "Les pas de stockage :", OBJET_DE_TEST["My ecarts"].stepserie()
    print "Les valeurs         :", OBJET_DE_TEST["My ecarts"].valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST["My ecarts"].valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST["My ecarts"].valueserie(-1)
    print "Liste des attributs :", OBJET_DE_TEST["My ecarts"].tagserie()
    print "Taille \"shape\"      :", OBJET_DE_TEST["My ecarts"].shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST["My ecarts"])
    print

    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Palier":"Premier"} )
    print "Valeurs pour tag    :", OBJET_DE_TEST["My ecarts"].valueserie( tags={"Palier":"Premier"} )
    print
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Carte":"IGN1"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Niveau":1024} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Camp":"Base"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Camp":"TOTO"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Toto":"Premier"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Carte":"IGN1"} )
    print

    print "Combinaison 'ET' de plusieurs Tags"
    print "Attendu : [0, 1],    trouv� :",OBJET_DE_TEST["My ecarts"].stepserie( tags={"Camp":"Base", "Palier":"Premier"} )
    print "Attendu : [],        trouv� :",OBJET_DE_TEST["My ecarts"].stepserie( tags={"Camp":"Sommet", "Palier":"Premier"} )
    # Attention : {"Camp":"Sommet", "Camp":"Base"} == {"Camp":"Base"}
    print "Attendu : [0, 1, 2], trouv� :",OBJET_DE_TEST["My ecarts"].stepserie( tags={"Camp":"Sommet", "Camp":"Base"} )
    print "Attendu : [2],       trouv� :",OBJET_DE_TEST["My ecarts"].stepserie( tags={"Carte":"IGN1", "Niveau":1024} )
    print
      
    print "Liste des tags pour le pas (item) 1  :",OBJET_DE_TEST["My ecarts"].tagserie(item = 1)
    print "Liste des tags pour le pas (item) 2  :",OBJET_DE_TEST["My ecarts"].tagserie(item = 2)
    print "Comme le step et l'item sont identiques par d�faut, on doit avoir la m�me chose :"
    print "Liste des tags pour le pas (step) 1  :",OBJET_DE_TEST["My ecarts"].tagserie(step = 1)
    print "Liste des tags pour le pas (step) 2  :",OBJET_DE_TEST["My ecarts"].tagserie(step = 2)
    print
    print "Liste des tags/valeurs pour le pas 1 :",OBJET_DE_TEST["My ecarts"].tagserie(item = 1, withValues=True)
    print "Liste des tags/valeurs pour le pas 2 :",OBJET_DE_TEST["My ecarts"].tagserie(item = 2, withValues=True)
    print

    print "Liste des valeurs possibles pour 1 tag donn� 'Camp'   :",OBJET_DE_TEST["My ecarts"].tagserie(outputTag="Camp")
    print "Liste des valeurs possibles pour 1 tag donn� 'Toto'   :",OBJET_DE_TEST["My ecarts"].tagserie(outputTag="Toto")
    print "Liste des valeurs possibles pour 1 tag donn� 'Niveau' :",OBJET_DE_TEST["My ecarts"].tagserie(outputTag="Niveau")
    print

    OBJET_DE_TEST.add_object("My other ecarts", basetype = numpy.array)
    OBJET_DE_TEST.store( "My other ecarts", numpy.arange(-1,5),   tags = {"Camp":"Base","Carte":"IGN3","Niveau":1024,"Palier":"Premier"} )
    OBJET_DE_TEST.store( "My other ecarts", numpy.arange(-1,5)+1, tags = {"Camp":"Base","Carte":"IGN4","Niveau": 210,"Palier":"Premier"} )
    OBJET_DE_TEST.store( "My other ecarts", numpy.arange(-1,5)+2, tags = {"Camp":"Base","Carte":"IGN1","Niveau":1024} )
    OBJET_DE_TEST.store( "My other ecarts", numpy.arange(-1,5)+3, tags = {"Camp":"Sommet","Carte":"IGN2","Niveau":4024,"Palier":"Second"} )

    print "Objets pr�sents dans le composite :",OBJET_DE_TEST.get_stored_objects()
    fichier = "composite.pkl.gz"
    print "Sauvegarde sur \"%s\"..."%fichier
    OBJET_DE_TEST.save_composite( fichier )
    print "Effacement de l'objet en memoire"
    del OBJET_DE_TEST
    print

    print "Relecture de l'objet sur \"%s\"..."%fichier
    OBJET_DE_TEST = CompositePersistence("My CompositePersistence bis", defaults=False)
    OBJET_DE_TEST.load_composite( fichier )
    print "Objets pr�sents dans le composite :",OBJET_DE_TEST.get_stored_objects()
    print "Taille des objets contenus :"
    for name in OBJET_DE_TEST.get_stored_objects():
        print "  Objet \"%s\" : taille unitaire de %i"%(name,len(OBJET_DE_TEST[name]))

    print
    print "Les pas de stockage :", OBJET_DE_TEST["My ecarts"].stepserie()
    print "Les valeurs         :", OBJET_DE_TEST["My ecarts"].valueserie()
    print "La 2�me valeur      :", OBJET_DE_TEST["My ecarts"].valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST["My ecarts"].valueserie(-1)
    print "Liste des attributs :", OBJET_DE_TEST["My ecarts"].tagserie()
    print "Taille \"shape\"      :", OBJET_DE_TEST["My ecarts"].shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST["My ecarts"])
    print

    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Palier":"Premier"} )
    print "Valeurs pour tag    :", OBJET_DE_TEST["My ecarts"].valueserie( tags={"Palier":"Premier"} )
    print
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Carte":"IGN1"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Niveau":1024} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Camp":"Base"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Camp":"TOTO"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Toto":"Premier"} )
    print "Pas pour tag        :", OBJET_DE_TEST["My ecarts"].stepserie( tags={"Carte":"IGN1"} )
    print
    print "Attributs                 :", OBJET_DE_TEST["My ecarts"].tagserie()
    print "Attributs pour tag filtr� :", OBJET_DE_TEST["My ecarts"].tagserie( tags={"Camp":"Base"} )
    print "Attributs pour tag filtr� :", OBJET_DE_TEST["My ecarts"].tagserie( tags={"Niveau":4024} )
    print
    print "Attributs et valeurs                 :", OBJET_DE_TEST["My ecarts"].tagserie( withValues=True )
    print "Attributs et valeurs pour tag filtr� :", OBJET_DE_TEST["My ecarts"].tagserie( withValues=True, tags={"Camp":"Base"} )
    print "Attributs et valeurs pour tag filtr� :", OBJET_DE_TEST["My ecarts"].tagserie( withValues=True, tags={"Niveau":4024} )
    print
    print "Valeur d'attribut pour un tag donn� 'BU'           :", OBJET_DE_TEST["My ecarts"].tagserie( outputTag = "Niveau" )
    print "Valeur d'attribut pour un tag donn� 'BU' filtr�    :", OBJET_DE_TEST["My ecarts"].tagserie( outputTag = "Niveau", tags={"Camp":"Base"} )
    print "Valeur d'attribut pour un tag donn� 'BU' filtr�    :", OBJET_DE_TEST["My ecarts"].tagserie( outputTag = "Niveau", tags={"Palier":"Second"} )
    print "Valeur d'attribut pour un tag donn� 'Camp' filtr�  :", OBJET_DE_TEST["My ecarts"].tagserie( outputTag = "Camp", tags={"Palier":"Premier"} )
    print "Valeur d'attribut pour un tag donn� 'Carte' filtr� :", OBJET_DE_TEST["My ecarts"].tagserie( outputTag = "Carte", tags={"Palier":"Premier"} )
    print "Valeur d'attribut pour un tag donn� 'Carte' filtr� :", OBJET_DE_TEST["My ecarts"].tagserie( outputTag = "Carte", tags={"Palier":"Premier","Niveau":4024} )
    print "Valeur d'attribut pour un tag donn� 'Carte' filtr� :", OBJET_DE_TEST["My ecarts"].tagserie( outputTag = "Carte", tags={"Palier":"Premier","Niveau":210} )
    print
