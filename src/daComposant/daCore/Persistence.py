# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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
    Définit des outils de persistance et d'enregistrement de séries de valeurs
    pour analyse ultérieure ou utilisation de calcul.
"""
__author__ = "Jean-Philippe ARGAUD"
__all__ = []

import os
import copy
import math
import gzip
import bz2
import pickle
import numpy

from daCore.PlatformInfo import PathManagement, PlatformInfo

PathManagement()
lpi = PlatformInfo()
mfp = lpi.MaximumPrecision()

if lpi.has_gnuplot:
    import Gnuplot


# ==============================================================================
class Persistence(object):
    """
    Classe générale de persistance définissant les accesseurs nécessaires
    (Template)
    """

    __slots__ = (
        "__name",
        "__unit",
        "__basetype",
        "__values",
        "__tags",
        "__dynamic",
        "__g",
        "__title",
        "__ltitle",
        "__pause",
        "__dataobservers",
    )

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
        self.__values = []
        self.__tags = []
        #
        self.__dynamic = False
        self.__g = None
        self.__title = None
        self.__ltitle = None
        self.__pause = None
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
        if value is None:
            raise ValueError("Value argument required")
        #
        self.__values.append(copy.copy(self.__basetype(value)))
        self.__tags.append(kwargs)
        #
        if self.__dynamic:
            self.__replots()
        __step = len(self.__values) - 1
        for hook, parameters, scheduler, order, osync, dovar in self.__dataobservers:
            if __step in scheduler:
                if order is None or dovar is None:
                    hook(self, parameters)
                else:
                    if not isinstance(order, (list, tuple)):
                        continue
                    if not isinstance(dovar, dict):
                        continue
                    if not bool(osync):  # Async observation
                        hook(self, parameters, order, dovar)
                    else:  # Sync observations
                        for v in order:
                            if len(dovar[v]) != len(self):
                                break
                        else:
                            hook(self, parameters, order, dovar)

    def pop(self, item=None):
        """
        Retire une valeur enregistrée par son index de stockage. Sans argument,
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
            if self.__basetype in [
                numpy.matrix,
                numpy.ndarray,
                numpy.array,
                numpy.ravel,
            ]:
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
        msg = "   Index        Value   Tags\n"
        for iv, vv in enumerate(self.__values):
            msg += "  i=%05i  %10s   %s\n" % (iv, vv, self.__tags[iv])
        return msg

    def __len__(self):
        "x.__len__() <==> len(x)"
        return len(self.__values)

    def name(self):
        return self.__name

    def __getitem__(self, index=None):
        "x.__getitem__(y) <==> x[y]"
        return copy.copy(self.__values[index])

    def count(self, value):
        "L.count(value) -> integer -- return number of occurrences of value"
        return self.__values.count(value)

    def index(self, value, start=0, stop=None):
        "L.index(value, [start, [stop]]) -> integer -- return first index of value."
        if stop is None:
            stop = len(self.__values)
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
                            __tmp.append(i)
                        elif (
                            isinstance(kwargs[tagKey], (list, tuple))
                            and self.__tags[i][tagKey] in kwargs[tagKey]
                        ):
                            __tmp.append(i)
                __indexOfFilteredItems = __tmp
                if len(__indexOfFilteredItems) == 0:
                    break
        return __indexOfFilteredItems

    # ---------------------------------------------------------
    def values(self, **kwargs):
        "D.values() -> list of D's values"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return [self.__values[i] for i in __indexOfFilteredItems]

    def keys(self, keyword=None, **kwargs):
        "D.keys() -> list of D's keys"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        __keys = []
        for i in __indexOfFilteredItems:
            if keyword in self.__tags[i]:
                __keys.append(self.__tags[i][keyword])
            else:
                __keys.append(None)
        return __keys

    def items(self, keyword=None, **kwargs):
        "D.items() -> list of D's (key, value) pairs, as 2-tuples"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        __pairs = []
        for i in __indexOfFilteredItems:
            if keyword in self.__tags[i]:
                __pairs.append((self.__tags[i][keyword], self.__values[i]))
            else:
                __pairs.append((None, self.__values[i]))
        return __pairs

    def tagkeys(self):
        "D.tagkeys() -> list of D's tag keys"
        __allKeys = []
        for dicotags in self.__tags:
            __allKeys.extend(list(dicotags.keys()))
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
            __indexOfFilteredItems = [
                item,
            ]
        #
        # Dans le cas où la sortie donne les valeurs d'un "outputTag"
        if outputTag is not None and isinstance(outputTag, str):
            outputValues = []
            for index in __indexOfFilteredItems:
                if outputTag in self.__tags[index].keys():
                    outputValues.append(self.__tags[index][outputTag])
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
                    allTags.update(self.__tags[index])
                allKeys = sorted(allTags.keys())
                return allKeys

    # ---------------------------------------------------------
    # Pour compatibilité
    def stepnumber(self):
        "Nombre de pas"
        return len(self.__values)

    # Pour compatibilité
    def stepserie(self, **kwargs):
        "Nombre de pas filtrés"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return __indexOfFilteredItems

    # Pour compatibilité
    def steplist(self, **kwargs):
        "Nombre de pas filtrés"
        __indexOfFilteredItems = self.__filteredIndexes(**kwargs)
        return list(__indexOfFilteredItems)

    # ---------------------------------------------------------
    def means(self):
        """
        Renvoie la série contenant, à chaque pas, la valeur moyenne des données
        au pas. Il faut que le type de base soit compatible avec les types
        élémentaires numpy.
        """
        try:
            __sr = [
                numpy.mean(item, dtype=mfp).astype("float") for item in self.__values
            ]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def stds(self, ddof=0):
        """
        Renvoie la série contenant, à chaque pas, l'écart-type des données
        au pas. Il faut que le type de base soit compatible avec les types
        élémentaires numpy.

        ddof : c'est le nombre de degrés de liberté pour le calcul de
               l'écart-type, qui est dans le diviseur. Inutile avant Numpy 1.1
        """
        try:
            if numpy.version.version >= "1.1.0":
                __sr = [
                    numpy.array(item).std(ddof=ddof, dtype=mfp).astype("float")
                    for item in self.__values
                ]
            else:
                return [
                    numpy.array(item).std(dtype=mfp).astype("float")
                    for item in self.__values
                ]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def sums(self):
        """
        Renvoie la série contenant, à chaque pas, la somme des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            __sr = [numpy.array(item).sum() for item in self.__values]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def mins(self):
        """
        Renvoie la série contenant, à chaque pas, le minimum des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            __sr = [numpy.array(item).min() for item in self.__values]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def maxs(self):
        """
        Renvoie la série contenant, à chaque pas, la maximum des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            __sr = [numpy.array(item).max() for item in self.__values]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def powers(self, x2):
        """
        Renvoie la série contenant, à chaque pas, la puissance "**x2" au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            __sr = [numpy.power(item, x2) for item in self.__values]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def norms(self, _ord=None):
        """
        Norm (_ord : voir numpy.linalg.norm)

        Renvoie la série contenant, à chaque pas, la norme des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy.
        """
        try:
            __sr = [numpy.linalg.norm(item, _ord) for item in self.__values]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def traces(self, offset=0):
        """
        Trace (offset : voir numpy.trace)

        Renvoie la série contenant, à chaque pas, la trace (avec l'offset) des
        données au pas. Il faut que le type de base soit compatible avec les
        types élémentaires numpy.
        """
        try:
            __sr = [
                numpy.trace(item, offset, dtype=mfp).astype("float")
                for item in self.__values
            ]
        except Exception:
            raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def maes(self, predictor=None):
        """
        Mean Absolute Error (MAE)
        mae(dX) = 1/n sum(dX_i)

        Renvoie la série contenant, à chaque pas, la MAE des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy. C'est réservé aux variables d'écarts ou d'incréments si le
        prédicteur est None, sinon c'est appliqué à l'écart entre les données
        au pas et le prédicteur au même pas.
        """
        if predictor is None:
            try:
                __sr = [numpy.mean(numpy.abs(item)) for item in self.__values]
            except Exception:
                raise TypeError("Base type is incompatible with numpy")
        else:
            if len(predictor) != len(self.__values):
                raise ValueError(
                    "Predictor number of steps is incompatible with the values"
                )
            for i, item in enumerate(self.__values):
                if numpy.asarray(predictor[i]).size != numpy.asarray(item).size:
                    raise ValueError(
                        "Predictor size at step %i is incompatible with the values" % i
                    )
            try:
                __sr = [
                    numpy.mean(numpy.abs(numpy.ravel(item) - numpy.ravel(predictor[i])))
                    for i, item in enumerate(self.__values)
                ]
            except Exception:
                raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    def mses(self, predictor=None):
        """
        Mean-Square Error (MSE) ou Mean-Square Deviation (MSD)
        mse(dX) = 1/n sum(dX_i**2) = 1/n ||X||^2

        Renvoie la série contenant, à chaque pas, la MSE des données au pas. Il
        faut que le type de base soit compatible avec les types élémentaires
        numpy. C'est réservé aux variables d'écarts ou d'incréments si le
        prédicteur est None, sinon c'est appliqué à l'écart entre les données
        au pas et le prédicteur au même pas.
        """
        if predictor is None:
            try:
                __n = self.shape()[0]
                __sr = [(numpy.linalg.norm(item) ** 2 / __n) for item in self.__values]
            except Exception:
                raise TypeError("Base type is incompatible with numpy")
        else:
            if len(predictor) != len(self.__values):
                raise ValueError(
                    "Predictor number of steps is incompatible with the values"
                )
            for i, item in enumerate(self.__values):
                if numpy.asarray(predictor[i]).size != numpy.asarray(item).size:
                    raise ValueError(
                        "Predictor size at step %i is incompatible with the values" % i
                    )
            try:
                __n = self.shape()[0]
                __sr = [
                    (
                        numpy.linalg.norm(numpy.ravel(item) - numpy.ravel(predictor[i]))
                        ** 2
                        / __n
                    )
                    for i, item in enumerate(self.__values)
                ]
            except Exception:
                raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    msds = mses  # Mean-Square Deviation (MSD=MSE)

    def rmses(self, predictor=None):
        """
        Root-Mean-Square Error (RMSE) ou Root-Mean-Square Deviation (RMSD)
        rmse(dX) = sqrt( 1/n sum(dX_i**2) ) = sqrt( mse(dX) )

        Renvoie la série contenant, à chaque pas, la RMSE des données au pas.
        Il faut que le type de base soit compatible avec les types élémentaires
        numpy. C'est réservé aux variables d'écarts ou d'incréments si le
        prédicteur est None (c'est donc une RMS), sinon c'est appliqué à
        l'écart entre les données au pas et le prédicteur au même pas.
        """
        if predictor is None:
            try:
                __n = self.shape()[0]
                __sr = [
                    (numpy.linalg.norm(item) / math.sqrt(__n)) for item in self.__values
                ]
            except Exception:
                raise TypeError("Base type is incompatible with numpy")
        else:
            if len(predictor) != len(self.__values):
                raise ValueError(
                    "Predictor number of steps is incompatible with the values"
                )
            for i, item in enumerate(self.__values):
                if numpy.asarray(predictor[i]).size != numpy.asarray(item).size:
                    raise ValueError(
                        "Predictor size at step %i is incompatible with the values" % i
                    )
            try:
                __n = self.shape()[0]
                __sr = [
                    (
                        numpy.linalg.norm(numpy.ravel(item) - numpy.ravel(predictor[i]))
                        / math.sqrt(__n)
                    )
                    for i, item in enumerate(self.__values)
                ]
            except Exception:
                raise TypeError("Base type is incompatible with numpy")
        return numpy.array(__sr).tolist()

    rmsds = rmses  # Root-Mean-Square Deviation (RMSD=RMSE)

    def __preplots(
        self,
        title="",
        xlabel="",
        ylabel="",
        ltitle=None,
        geometry="600x400",
        persist=False,
        pause=True,
    ):
        "Préparation des plots"
        #
        # Vérification de la disponibilité du module Gnuplot
        if not lpi.has_gnuplot:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # Vérification et compléments sur les paramètres d'entrée
        if ltitle is None:
            ltitle = ""
        __geometry = str(geometry)
        __sizespec = (__geometry.split("+")[0]).replace("x", ",")
        #
        if persist:
            Gnuplot.GnuplotOpts.gnuplot_command = "gnuplot -persist "
        #
        self.__g = Gnuplot.Gnuplot()  # persist=1
        self.__g(
            "set terminal " + Gnuplot.GnuplotOpts.default_term + " size " + __sizespec
        )
        self.__g("set style data lines")
        self.__g("set grid")
        self.__g("set autoscale")
        self.__g('set xlabel "' + str(xlabel) + '"')
        self.__g('set ylabel "' + str(ylabel) + '"')
        self.__title = title
        self.__ltitle = ltitle
        self.__pause = pause

    def plots(
        self,
        item=None,
        step=None,
        steps=None,
        title="",
        xlabel="",
        ylabel="",
        ltitle=None,
        geometry="600x400",
        filename="",
        dynamic=False,
        persist=False,
        pause=True,
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
            self.__preplots(title, xlabel, ylabel, ltitle, geometry, persist, pause)
            if dynamic:
                self.__dynamic = True
                if len(self.__values) == 0:
                    return 0
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
            self.__g('set title  "' + str(title) + " (pas " + str(index) + ')"')
            if isinstance(steps, (list, numpy.ndarray)):
                Steps = list(steps)
            else:
                Steps = list(range(len(self.__values[index])))
            #
            self.__g.plot(Gnuplot.Data(Steps, self.__values[index], title=ltitle))
            #
            if filename != "":
                i += 1
                stepfilename = "%s_%03i.ps" % (filename, i)
                if os.path.isfile(stepfilename):
                    raise ValueError(
                        'Error: a file with this name "%s" already exists.'
                        % stepfilename
                    )
                self.__g.hardcopy(filename=stepfilename, color=1)
            if self.__pause:
                eval(input("Please press return to continue...\n"))

    def __replots(self):
        """
        Affichage dans le cas du suivi dynamique de la variable
        """
        if self.__dynamic and len(self.__values) < 2:
            return 0
        #
        self.__g('set title  "' + str(self.__title))
        Steps = list(range(len(self.__values)))
        self.__g.plot(Gnuplot.Data(Steps, self.__values, title=self.__ltitle))
        #
        if self.__pause:
            eval(input("Please press return to continue...\n"))

    # ---------------------------------------------------------
    # On pourrait aussi utiliser d'autres attributs d'un "array" comme "tofile"
    def mean(self):
        """
        Renvoie la moyenne sur toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.mean(self.__values, axis=0, dtype=mfp).astype("float")
        except Exception:
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
            if numpy.version.version >= "1.1.0":
                return (
                    numpy.asarray(self.__values).std(ddof=ddof, axis=0).astype("float")
                )
            else:
                return numpy.asarray(self.__values).std(axis=0).astype("float")
        except Exception:
            raise TypeError("Base type is incompatible with numpy")

    def sum(self):
        """
        Renvoie la somme de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.asarray(self.__values).sum(axis=0)
        except Exception:
            raise TypeError("Base type is incompatible with numpy")

    def min(self):
        """
        Renvoie le minimum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.asarray(self.__values).min(axis=0)
        except Exception:
            raise TypeError("Base type is incompatible with numpy")

    def max(self):
        """
        Renvoie le maximum de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.asarray(self.__values).max(axis=0)
        except Exception:
            raise TypeError("Base type is incompatible with numpy")

    def cumsum(self):
        """
        Renvoie la somme cumulée de toutes les valeurs sans tenir compte de la
        longueur des pas. Il faut que le type de base soit compatible avec
        les types élémentaires numpy.
        """
        try:
            return numpy.asarray(self.__values).cumsum(axis=0)
        except Exception:
            raise TypeError("Base type is incompatible with numpy")

    def plot(
        self,
        steps=None,
        title="",
        xlabel="",
        ylabel="",
        ltitle=None,
        geometry="600x400",
        filename="",
        persist=False,
        pause=True,
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
        if not lpi.has_gnuplot:
            raise ImportError("The Gnuplot module is required to plot the object.")
        #
        # Vérification et compléments sur les paramètres d'entrée
        if ltitle is None:
            ltitle = ""
        if isinstance(steps, (list, numpy.ndarray)):
            Steps = list(steps)
        else:
            Steps = list(range(len(self.__values[0])))
        __geometry = str(geometry)
        __sizespec = (__geometry.split("+")[0]).replace("x", ",")
        #
        if persist:
            Gnuplot.GnuplotOpts.gnuplot_command = "gnuplot -persist "
        #
        self.__g = Gnuplot.Gnuplot()  # persist=1
        self.__g(
            "set terminal " + Gnuplot.GnuplotOpts.default_term + " size " + __sizespec
        )
        self.__g("set style data lines")
        self.__g("set grid")
        self.__g("set autoscale")
        self.__g('set title  "' + str(title) + '"')
        self.__g('set xlabel "' + str(xlabel) + '"')
        self.__g('set ylabel "' + str(ylabel) + '"')
        #
        # Tracé du ou des vecteurs demandés
        indexes = list(range(len(self.__values)))
        self.__g.plot(
            Gnuplot.Data(
                Steps, self.__values[indexes.pop(0)], title=ltitle + " (pas 0)"
            )
        )
        for index in indexes:
            self.__g.replot(
                Gnuplot.Data(
                    Steps, self.__values[index], title=ltitle + " (pas %i)" % index
                )
            )
        #
        if filename != "":
            self.__g.hardcopy(filename=filename, color=1)
        if pause:
            eval(input("Please press return to continue...\n"))

    # ---------------------------------------------------------
    def s2mvr(self):
        """
        Renvoie la série sous la forme d'une unique matrice avec les données au
        pas rangées par ligne
        """
        try:
            return numpy.asarray(self.__values)
        except Exception:
            raise TypeError("Base type is incompatible with numpy")

    def s2mvc(self):
        """
        Renvoie la série sous la forme d'une unique matrice avec les données au
        pas rangées par colonne
        """
        try:
            return numpy.asarray(self.__values).transpose()
            # Eqvlt: return numpy.stack([numpy.ravel(sv) for sv in self.__values], axis=1)
        except Exception:
            raise TypeError("Base type is incompatible with numpy")

    # ---------------------------------------------------------
    def setDataObserver(
        self,
        HookFunction=None,
        HookParameters=None,
        Scheduler=None,
        Order=None,
        OSync=True,
        DOVar=None,
    ):
        """
        Association à la variable d'un triplet définissant un observer.

        Les variables Order et DOVar sont utilisées pour un observer
        multi-variable. Le Scheduler attendu est une fréquence, une simple
        liste d'index ou un range des index.
        """
        #
        # Vérification du Scheduler
        # -------------------------
        maxiter = int(1e9)
        if isinstance(Scheduler, int):  # Considéré comme une fréquence à partir de 0
            Schedulers = range(0, maxiter, int(Scheduler))
        elif isinstance(Scheduler, range):  # Considéré comme un itérateur
            Schedulers = Scheduler
        elif isinstance(
            Scheduler, (list, tuple)
        ):  # Considéré comme des index explicites
            Schedulers = [
                int(i) for i in Scheduler
            ]  # Similaire à map( int, Scheduler )
        else:  # Dans tous les autres cas, activé par défaut
            Schedulers = range(0, maxiter)
        #
        # Stockage interne de l'observer dans la variable
        # -----------------------------------------------
        self.__dataobservers.append(
            [HookFunction, HookParameters, Schedulers, Order, OSync, DOVar]
        )

    def removeDataObserver(self, HookFunction=None, AllObservers=False):
        """
        Suppression d'un observer nommé sur la variable.

        On peut donner dans HookFunction la même fonction que lors de la
        définition, ou un simple string qui est le nom de la fonction. Si
        AllObservers est vrai, supprime tous les observers enregistrés.
        """
        if hasattr(HookFunction, "func_name"):
            name = str(HookFunction.func_name)
        elif hasattr(HookFunction, "__name__"):
            name = str(HookFunction.__name__)
        elif isinstance(HookFunction, str):
            name = str(HookFunction)
        else:
            name = None
        #
        ih = -1
        index_to_remove = []
        for [hf, _, _, _, _, _] in self.__dataobservers:
            ih = ih + 1
            if name is hf.__name__ or AllObservers:
                index_to_remove.append(ih)
        index_to_remove.reverse()
        for ih in index_to_remove:
            self.__dataobservers.pop(ih)
        return len(index_to_remove)

    def hasDataObserver(self):
        return bool(len(self.__dataobservers) > 0)


# ==============================================================================
class SchedulerTrigger(object):
    """
    Classe générale d'interface de type Scheduler/Trigger
    """

    __slots__ = ()

    def __init__(
        self,
        simplifiedCombo=None,
        startTime=0,
        endTime=int(1e9),
        timeDelay=1,
        timeUnit=1,
        frequency=None,
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

    __slots__ = ()

    def __init__(self, name="", unit="", basetype=float):
        Persistence.__init__(self, name, unit, basetype)


class OneIndex(Persistence):
    """
    Classe définissant le stockage d'une valeur unique entière (int) par pas.
    """

    __slots__ = ()

    def __init__(self, name="", unit="", basetype=int):
        Persistence.__init__(self, name, unit, basetype)


class OneVector(Persistence):
    """
    Classe de stockage d'une liste de valeurs numériques homogènes par pas. Ne
    pas utiliser cette classe pour des données hétérogènes, mais "OneList".
    """

    __slots__ = ()

    def __init__(self, name="", unit="", basetype=numpy.ravel):
        Persistence.__init__(self, name, unit, basetype)


class OneMatrice(Persistence):
    """
    Classe de stockage d'une matrice de valeurs homogènes par pas.
    """

    __slots__ = ()

    def __init__(self, name="", unit="", basetype=numpy.array):
        Persistence.__init__(self, name, unit, basetype)


class OneMatrix(Persistence):
    """
    Classe de stockage d'une matrice de valeurs homogènes par pas (obsolète).
    """

    __slots__ = ()

    def __init__(self, name="", unit="", basetype=numpy.matrix):
        Persistence.__init__(self, name, unit, basetype)


class OneList(Persistence):
    """
    Classe de stockage d'une liste de valeurs hétérogènes (list) par pas. Ne
    pas utiliser cette classe pour des données numériques homogènes, mais
    "OneVector".
    """

    __slots__ = ()

    def __init__(self, name="", unit="", basetype=list):
        Persistence.__init__(self, name, unit, basetype)


def NoType(value):
    "Fonction transparente, sans effet sur son argument"
    return value


class OneNoType(Persistence):
    """
    Classe de stockage d'un objet sans modification (cast) de type. Attention,
    selon le véritable type de l'objet stocké à chaque pas, les opérations
    arithmétiques à base de numpy peuvent être invalides ou donner des
    résultats inattendus. Cette classe n'est donc à utiliser qu'à bon escient
    volontairement, et pas du tout par défaut.
    """

    __slots__ = ()

    def __init__(self, name="", unit="", basetype=NoType):
        Persistence.__init__(self, name, unit, basetype)


# ==============================================================================
class CompositePersistence(object):
    """
    Structure de stockage permettant de rassembler plusieurs objets de
    persistence.

    Des objets par défaut sont prévus, et des objets supplémentaires peuvent
    être ajoutés.
    """

    __slots__ = ("__name", "__StoredObjects")

    def __init__(self, name="", defaults=True):
        """
        name : nom courant

        La gestion interne des données est exclusivement basée sur les
        variables initialisées ici (qui ne sont pas accessibles depuis
        l'extérieur des objets comme des attributs) :
        __StoredObjects : objets de type persistence collectés dans cet objet
        """
        self.__name = str(name)
        #
        self.__StoredObjects = {}
        #
        # Definition des objets par defaut
        # --------------------------------
        if defaults:
            self.__StoredObjects["Informations"] = OneNoType("Informations")
            self.__StoredObjects["Background"] = OneVector(
                "Background", basetype=numpy.array
            )
            self.__StoredObjects["BackgroundError"] = OneMatrix("BackgroundError")
            self.__StoredObjects["Observation"] = OneVector(
                "Observation", basetype=numpy.array
            )
            self.__StoredObjects["ObservationError"] = OneMatrix("ObservationError")
            self.__StoredObjects["Analysis"] = OneVector(
                "Analysis", basetype=numpy.array
            )
            self.__StoredObjects["AnalysisError"] = OneMatrix("AnalysisError")
            self.__StoredObjects["Innovation"] = OneVector(
                "Innovation", basetype=numpy.array
            )
            self.__StoredObjects["KalmanGainK"] = OneMatrix("KalmanGainK")
            self.__StoredObjects["OperatorH"] = OneMatrix("OperatorH")
            self.__StoredObjects["RmsOMA"] = OneScalar("RmsOMA")
            self.__StoredObjects["RmsOMB"] = OneScalar("RmsOMB")
            self.__StoredObjects["RmsBMA"] = OneScalar("RmsBMA")
        #

    def store(self, name=None, value=None, **kwargs):
        """
        Stockage d'une valeur "value" pour le "step" dans la variable "name".
        """
        if name is None:
            raise ValueError("Storable object name is required for storage.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in storable objects." % name)
        self.__StoredObjects[name].store(value=value, **kwargs)

    def add_object(self, name=None, persistenceType=Persistence, basetype=None):
        """
        Ajoute dans les objets stockables un nouvel objet défini par son nom,
        son type de Persistence et son type de base à chaque pas.
        """
        if name is None:
            raise ValueError("Object name is required for adding an object.")
        if name in self.__StoredObjects.keys():
            raise ValueError(
                "An object with the same name '%s' already exists in storable objects. Choose another one."
                % name
            )
        if basetype is None:
            self.__StoredObjects[name] = persistenceType(name=str(name))
        else:
            self.__StoredObjects[name] = persistenceType(
                name=str(name), basetype=basetype
            )

    def get_object(self, name=None):
        """
        Renvoie l'objet de type Persistence qui porte le nom demandé.
        """
        if name is None:
            raise ValueError("Object name is required for retrieving an object.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in stored objects." % name)
        return self.__StoredObjects[name]

    def set_object(self, name=None, objet=None):
        """
        Affecte directement un 'objet' qui porte le nom 'name' demandé.
        Attention, il n'est pas effectué de vérification sur le type, qui doit
        comporter les méthodes habituelles de Persistence pour que cela
        fonctionne.
        """
        if name is None:
            raise ValueError("Object name is required for setting an object.")
        if name in self.__StoredObjects.keys():
            raise ValueError(
                "An object with the same name '%s' already exists in storable objects. Choose another one."
                % name
            )
        self.__StoredObjects[name] = objet

    def del_object(self, name=None):
        """
        Supprime un objet de la liste des objets stockables.
        """
        if name is None:
            raise ValueError("Object name is required for retrieving an object.")
        if name not in self.__StoredObjects.keys():
            raise ValueError("No such name '%s' exists in stored objects." % name)
        del self.__StoredObjects[name]

    # ---------------------------------------------------------
    # Méthodes d'accès de type dictionnaire
    def __getitem__(self, name=None):
        "x.__getitem__(y) <==> x[y]"
        return self.get_object(name)

    def __setitem__(self, name=None, objet=None):
        "x.__setitem__(i, y) <==> x[i]=y"
        self.set_object(name, objet)

    def keys(self):
        "D.keys() -> list of D's keys"
        return self.get_stored_objects(hideVoidObjects=False)

    def values(self):
        "D.values() -> list of D's values"
        return self.__StoredObjects.values()

    def items(self):
        "D.items() -> list of D's (key, value) pairs, as 2-tuples"
        return self.__StoredObjects.items()

    # ---------------------------------------------------------
    def get_stored_objects(self, hideVoidObjects=False):
        "Renvoie la liste des objets présents"
        objs = self.__StoredObjects.keys()
        if hideVoidObjects:
            usedObjs = []
            for k in objs:
                try:
                    if len(self.__StoredObjects[k]) > 0:
                        usedObjs.append(k)
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
                filename = os.tempnam(os.getcwd(), "dacp") + ".pkl.gz"
            elif compress == "bzip2":
                filename = os.tempnam(os.getcwd(), "dacp") + ".pkl.bz2"
            else:
                filename = os.tempnam(os.getcwd(), "dacp") + ".pkl"
        else:
            filename = os.path.abspath(filename)
        #
        if mode == "pickle":
            if compress == "gzip":
                output = gzip.open(filename, "wb")
            elif compress == "bzip2":
                output = bz2.BZ2File(filename, "wb")
            else:
                output = open(filename, "wb")
            pickle.dump(self, output)
            output.close()
        else:
            raise ValueError("Save mode '%s' unknown. Choose another one." % mode)
        #
        return filename

    def load_composite(self, filename=None, mode="pickle", compress="gzip"):
        """
        Recharge un objet composite sauvé en fichier
        """
        if filename is None:
            raise ValueError("A file name if requested to load a composite.")
        else:
            filename = os.path.abspath(filename)
        #
        if mode == "pickle":
            if compress == "gzip":
                pkl_file = gzip.open(filename, "rb")
            elif compress == "bzip2":
                pkl_file = bz2.BZ2File(filename, "rb")
            else:
                pkl_file = open(filename, "rb")
            output = pickle.load(pkl_file)
            for k in output.keys():
                self[k] = output[k]
        else:
            raise ValueError("Load mode '%s' unknown. Choose another one." % mode)
        #
        return filename


# ==============================================================================
if __name__ == "__main__":
    print("\n AUTODIAGNOSTIC\n")
