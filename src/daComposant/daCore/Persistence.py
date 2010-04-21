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
    D�finit des outils de persistence et d'enregistrement de s�ries de valeurs
    pour analyse ult�rieure ou utilisation de calcul.
"""
__author__ = "Jean-Philippe ARGAUD - Mars 2008"

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
    
    def basetype(self, basetype=None):
        """
        Renvoie ou met en place le type de base des objets stock�s
        """
        if basetype is None:
            return self.__basetype
        else:
            self.__basetype = basetype

    def store(self, value=None, step=None):
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
    def stepserie(self, item=None, step=None):
        """
        Renvoie par d�faut toute la liste des pas de temps. Si l'argument "step"
        existe dans la liste des pas de stockage effectu�s, renvoie ce pas
        "step". Si l'argument "item" est correct, renvoie le pas stock�e au
        num�ro "item".
        """
        if step is not None and step in self.__steps:
            return step
        elif item is not None and item < len(self.__steps):
            return self.__steps[item]
        else:
            return self.__steps

    def valueserie(self, item=None, step=None):
        """
        Renvoie par d�faut toute la liste des valeurs/objets. Si l'argument
        "step" existe dans la liste des pas de stockage effectu�s, renvoie la
        valeur stock�e � ce pas "step". Si l'argument "item" est correct,
        renvoie la valeur stock�e au num�ro "item".
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
        Renvoie la valeur moyenne des donn�es � chaque pas. Il faut que le type
        de base soit compatible avec les types �l�mentaires numpy.
        """
        try:
            return [numpy.matrix(item).mean() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def std(self, ddof=0):
        """
        Renvoie l'�cart-type des donn�es � chaque pas. Il faut que le type de
        base soit compatible avec les types �l�mentaires numpy.
        
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

    def sum(self):
        """
        Renvoie la somme des donn�es � chaque pas. Il faut que le type de
        base soit compatible avec les types �l�mentaires numpy.
        """
        try:
            return [numpy.matrix(item).sum() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def min(self):
        """
        Renvoie le minimum des donn�es � chaque pas. Il faut que le type de
        base soit compatible avec les types �l�mentaires numpy.
        """
        try:
            return [numpy.matrix(item).min() for item in self.__values]
        except:
            raise TypeError("Base type is incompatible with numpy")

    def max(self):
        """
        Renvoie le maximum des donn�es � chaque pas. Il faut que le type de
        base soit compatible avec les types �l�mentaires numpy.
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
            - persist  : bool�en indiquant que la fen�tre affich�e sera
                         conserv�e lors du passage au dessin suivant
                         Par d�faut, persist = False
            - pause    : bool�en indiquant une pause apr�s chaque trac�, et
                         attendant un Return
                         Par d�faut, pause = True
        """
        import os
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
        les types �l�mentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).mean()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stepstd(self, ddof=0):
        """
        Renvoie l'�cart-type de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        
        ddof : c'est le nombre de degr�s de libert� pour le calcul de
               l'�cart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
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
        les types �l�mentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).sum()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stepmin(self):
        """
        Renvoie le minimum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).min()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def stepmax(self):
        """
        Renvoie le maximum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
        """
        try:
            return numpy.matrix(self.__values).max()
        except:
            raise TypeError("Base type is incompatible with numpy")

    def cumsum(self):
        """
        Renvoie la somme cumul�e de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types �l�mentaires numpy.
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
            - filename : nom de fichier Postscript pour une sauvegarde,
            - persist  : bool�en indiquant que la fen�tre affich�e sera
                         conserv�e lors du passage au dessin suivant
                         Par d�faut, persist = False
            - pause    : bool�en indiquant une pause apr�s chaque trac�, et
                         attendant un Return
                         Par d�faut, pause = True
        """
        import os
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
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'�cart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
    print "  La somme cumul�e  :", OBJET_DE_TEST.cumsum()
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
    print "La 2�me valeur      :", OBJET_DE_TEST.valueserie(1)
    print "La derni�re valeur  :", OBJET_DE_TEST.valueserie(-1)
    print "Valeurs par pas :"
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'�cart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
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
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales :"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'�cart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
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
    print "  La moyenne        :", OBJET_DE_TEST.mean()
    print "  L'�cart-type      :", OBJET_DE_TEST.std()
    print "  La somme          :", OBJET_DE_TEST.sum()
    print "  Le minimum        :", OBJET_DE_TEST.min()
    print "  Le maximum        :", OBJET_DE_TEST.max()
    print "Valeurs globales : attention, on peut les calculer car True=1, False=0, mais cela n'a pas de sens"
    print "  La moyenne        :", OBJET_DE_TEST.stepmean()
    print "  L'�cart-type      :", OBJET_DE_TEST.stepstd()
    print "  La somme          :", OBJET_DE_TEST.stepsum()
    print "  Le minimum        :", OBJET_DE_TEST.stepmin()
    print "  Le maximum        :", OBJET_DE_TEST.stepmax()
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

    print "======> Affichage d'objets stock�s"
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
    print "Affichage de l'ensemble du stockage sur une m�me image"
    D.stepplot(
        title = "Tous les vecteurs",
        filename="vecteurs.ps",
        xlabel = "Axe X",
        ylabel = "Axe Y",
        pause = False )
    print "Stockage d'un quatri�me vecteur de longueur diff�rente"
    D.store(vect4)
    print "Affichage s�par� du dernier stockage"
    D.plot(
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
