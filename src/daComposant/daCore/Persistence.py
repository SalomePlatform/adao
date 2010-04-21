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
    Définit des outils de persistence et d'enregistrement de séries de valeurs
    pour analyse ultérieure ou utilisation de calcul.
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

import numpy

from PlatformInfo import PathManagement ; PathManagement()

# ==============================================================================
class Persistence:
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
        __step   : numérotation par défaut du pas courant
        __basetype : le type de base de chaque valeur, sous la forme d'un type
                     permettant l'instanciation ou le casting Python 
        __steps  : les pas de stockage. Par défaut, c'est __step
        __values : les valeurs de stockage. Par défaut, c'est None
        """
        self.__name = str(name)
        self.__unit = str(unit)
        #
        self.__step     = -1
        self.__basetype = basetype
        #
        self.__steps    = []
        self.__values   = []
    
    def basetype(self, basetype=None):
        """
        Renvoie ou met en place le type de base des objets stockés
        """
        if basetype is None:
            return self.__basetype
        else:
            self.__basetype = basetype

    def store(self, value=None, step=None):
        """
        Stocke une valeur à un pas. Une instanciation est faite avec le type de
        base pour stocker l'objet. Si le pas n'est pas fournit, on utilise
        l'étape de stockage comme valeur de pas.
        """
        if value is None: raise ValueError("Value argument required")
        self.__step += 1
        if step is not None:
            self.__steps.append(step)
        else:
            self.__steps.append(self.__step)
        #
        self.__values.append(self.__basetype(value))

    def shape(self):
        """
        Renvoie la taille sous forme numpy du dernier objet stocké. Si c'est un
        objet numpy, renvoie le shape. Si c'est un entier, un flottant, un
        complexe, renvoie 1. Si c'est une liste ou un dictionnaire, renvoie la
        longueur. Par défaut, renvoie 1.
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
        Renvoie le nombre d'éléments dans un séquence ou la plus grande
        dimension d'une matrice
        """
        return max( self.shape() )

    # ---------------------------------------------------------
    def stepserie(self, item=None, step=None):
        """
        Renvoie par défaut toute la liste des pas de temps. Si l'argument "step"
        existe dans la liste des pas de stockage effectués, renvoie ce pas
        "step". Si l'argument "item" est correct, renvoie le pas stockée au
        numéro "item".
        """
        if step is not None and step in self.__steps:
            return step
        elif item is not None and item < len(self.__steps):
            return self.__steps[item]
        else:
            return self.__steps

    def valueserie(self, item=None, step=None):
        """
        Renvoie par défaut toute la liste des valeurs/objets. Si l'argument
        "step" existe dans la liste des pas de stockage effectués, renvoie la
        valeur stockée à ce pas "step". Si l'argument "item" est correct,
        renvoie la valeur stockée au numéro "item".
        """
        if step is not None and step in self.__steps:
            index = self.__steps.index(step)
            return self.__values[index]
        elif item is not None and item < len(self.__values):
            return self.__values[item]
        else:
            return self.__values
    
    def stepnumber(self):
        """
        Renvoie le nombre de pas de stockage.
        """
        return len(self.__steps)

    # ---------------------------------------------------------
    def mean(self):
        """
        Renvoie la valeur moyenne des données à chaque pas. Il faut que le type
        de base soit compatible avec les types élémentaires numpy.
        """
        try:
            return [numpy.matrix(item).mean() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def std(self, ddof=0):
        """
        Renvoie l'écart-type des données à chaque pas. Il faut que le type de
        base soit compatible avec les types élémentaires numpy.
        
        ddof : c'est le nombre de degrés de liberté pour le calcul de
               l'écart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
        """
        try:
            if numpy.version.version >= '1.1.0':
                return [numpy.matrix(item).std(ddof=ddof) for item in self.__values]
            else:
                return [numpy.matrix(item).std() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def sum(self):
        """
        Renvoie la somme des données à chaque pas. Il faut que le type de
        base soit compatible avec les types élémentaires numpy.
        """
        try:
            return [numpy.matrix(item).sum() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def min(self):
        """
        Renvoie le minimum des données à chaque pas. Il faut que le type de
        base soit compatible avec les types élémentaires numpy.
        """
        try:
            return [numpy.matrix(item).min() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def max(self):
        """
        Renvoie le maximum des données à chaque pas. Il faut que le type de
        base soit compatible avec les types élémentaires numpy.
        """
        try:
            return [numpy.matrix(item).max() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def plot(self, item=None, step=None,
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
            - persist  : booléen indiquant que la fenêtre affichée sera
                         conservée lors du passage au dessin suivant
                         Par défaut, persist = False
            - pause    : booléen indiquant une pause après chaque tracé, et
                         attendant un Return
                         Par défaut, pause = True
        """
        import os
        #
        # Vérification de la disponibilité du module Gnuplot
        try:
            import Gnuplot
            self.__gnuplot = Gnuplot
        except:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # Vérification et compléments sur les paramètres d'entrée
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
        #
        # Tracé du ou des vecteurs demandés
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
            if ( type(steps) is type([]) ) or ( type(steps) is type(numpy.array([])) ):
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
            if pause:
                raw_input('Please press return to continue...\n')

    # ---------------------------------------------------------
    def stepmean(self):
        """
        Renvoie la moyenne sur toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).mean()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stepstd(self, ddof=0):
        """
        Renvoie l'écart-type de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        
        ddof : c'est le nombre de degrés de liberté pour le calcul de
               l'écart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
        """
        try:
            if numpy.version.version >= '1.1.0':
                return numpy.matrix(self.__values).std(ddof=ddof)
            else:
                return numpy.matrix(self.__values).std()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stepsum(self):
        """
        Renvoie la somme de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).sum()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stepmin(self):
        """
        Renvoie le minimum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).min()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stepmax(self):
        """
        Renvoie le maximum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).max()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def cumsum(self):
        """
        Renvoie la somme cumulée de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).cumsum(axis=0)
        except:
            raise TypeError("Base type is incompatible with numpy")

    # On pourrait aussi utiliser les autres attributs d'une "matrix", comme
    # "tofile", "min"...

    def stepplot(self,
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
            - filename : nom de fichier Postscript pour une sauvegarde,
            - persist  : booléen indiquant que la fenêtre affichée sera
                         conservée lors du passage au dessin suivant
                         Par défaut, persist = False
            - pause    : booléen indiquant une pause après chaque tracé, et
                         attendant un Return
                         Par défaut, pause = True
        """
        import os
        #
        # Vérification de la disponibilité du module Gnuplot
        try:
            import Gnuplot
            self.__gnuplot = Gnuplot
        except:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # Vérification et compléments sur les paramètres d'entrée
        if persist:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -persist -geometry '+geometry
        else:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -geometry '+geometry
        if ltitle is None:
            ltitle = ""
        if ( type(steps) is type([]) ) or ( type(steps) is type(numpy.array([])) ):
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
        # Tracé du ou des vecteurs demandés
        indexes = range(len(self.__values))
        self.__g.plot( self.__gnuplot.Data( Steps, self.__values[indexes.pop(0)], title=ltitle+" (pas 0)" ) )
        for index in indexes:
            self.__g.replot( self.__gnuplot.Data( Steps, self.__values[index], title=ltitle+" (pas %i)"%index ) )
        #
        if filename != "":
            self.__g.hardcopy(filename=filename, color=1)
        if pause:
            raw_input('Please press return to continue...\n')

# ==============================================================================
class OneScalar(Persistence):
    """
    Classe définissant le stockage d'une valeur unique réelle (float) par pas
    
    Le type de base peut être changé par la méthode "basetype", mais il faut que
    le nouveau type de base soit compatible avec les types par éléments de 
    numpy. On peut même utiliser cette classe pour stocker des vecteurs/listes
    ou des matrices comme dans les classes suivantes, mais c'est déconseillé
    pour conserver une signification claire des noms.
    """
    def __init__(self, name="", unit="", basetype = float):
        Persistence.__init__(self, name, unit, basetype)

class OneVector(Persistence):
    """
    Classe définissant le stockage d'une liste (list) de valeurs homogènes par
    hypothèse par pas. Pour éviter les confusions, ne pas utiliser la classe
    "OneVector" pour des données hétérogènes, mais bien "OneList".
    """
    def __init__(self, name="", unit="", basetype = list):
        Persistence.__init__(self, name, unit, basetype)

class OneMatrix(Persistence):
    """
    Classe définissant le stockage d'une matrice de valeurs (numpy.matrix) par
    pas
    """
    def __init__(self, name="", unit="", basetype = numpy.matrix):
        Persistence.__init__(self, name, unit, basetype)

class OneList(Persistence):
    """
    Classe définissant le stockage d'une liste de valeurs potentiellement
    hétérogènes (list) par pas. Pour éviter les confusions, ne pas utiliser la
    classe "OneVector" pour des données hétérogènes, mais bien "OneList".
    """
    def __init__(self, name="", unit="", basetype = list):
        Persistence.__init__(self, name, unit, basetype)

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
    print "La 2ème valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La dernière valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas :"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'écart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'écart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
    print "  La somme cumulée  :", OBJET_DE_TEST.cumsum()
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Un entier"
    OBJET_DE_TEST = OneScalar("My int", unit="cm", basetype=int)
    OBJET_DE_TEST.store( 5 )
    OBJET_DE_TEST.store(-5 )
    OBJET_DE_TEST.store( 1.)
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2ème valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La dernière valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas :"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'écart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'écart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
    print "  La somme cumulée  :", OBJET_DE_TEST.cumsum()
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Un booléen"
    OBJET_DE_TEST = OneScalar("My bool", unit="", basetype=bool)
    OBJET_DE_TEST.store( True  )
    OBJET_DE_TEST.store( False )
    OBJET_DE_TEST.store( True  )
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2ème valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La dernière valeur  :", OBJET_DE_TEST.valueserie(-1)
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
    print "La 2ème valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La dernière valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas :"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'écart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'écart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
    print "  La somme cumulée  :", OBJET_DE_TEST.cumsum()
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Une liste hétérogène"
    OBJET_DE_TEST = OneList("My list", unit="bool/cm")
    OBJET_DE_TEST.store( (True , -5) )
    OBJET_DE_TEST.store( (False,  5 ) )
    OBJET_DE_TEST.store( (True ,  1.) )
    print "Les pas de stockage :", OBJET_DE_TEST.stepserie()
    print "Les valeurs         :", OBJET_DE_TEST.valueserie()
    print "La 2ème valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La dernière valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas : attention, on peut les calculer car True=1, False=0, mais cela n'a pas de sens"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'écart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales : attention, on peut les calculer car True=1, False=0, mais cela n'a pas de sens"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'écart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
    print "  La somme cumulée  :", OBJET_DE_TEST.cumsum()
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
    print "La 2ème valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La dernière valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Taille \"shape\"      :", OBJET_DE_TEST.shape()
    print "Taille \"len\"        :", len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print

    print "======> Affichage d'objets stockés"
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
    print "Affichage de l'ensemble du stockage sur une même image"
    D.stepplot(
        title = "Tous les vecteurs",
        filename="vecteurs.ps",
        xlabel = "Axe X",
        ylabel = "Axe Y",
        pause = False )
    print "Stockage d'un quatrième vecteur de longueur différente"
    D.store(vect4)
    print "Affichage séparé du dernier stockage"
    D.plot(
        item  = 3,
        title = "Vecteurs",
        filename = "vecteur",
        xlabel = "Axe X",
        ylabel = "Axe Y",
        pause = False )
    print "Les images ont été stockées en fichiers Postscript"
    print "Taille \"shape\" du dernier objet stocké",OBJET_DE_TEST.shape()
    print "Taille \"len\" du dernier objet stocké",len(OBJET_DE_TEST)
    del OBJET_DE_TEST
    print
