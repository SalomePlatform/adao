# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2017 EDF R&D
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

import numpy
from daCore import BasicObjects
import os.path

# ==============================================================================
class ElementaryDiagnostic(BasicObjects.Diagnostic):
    """
    Classe pour tracer simplement une liste de vecteurs à chaque pas
    """
    def __init__(self, name = "", unit = "", basetype = None, parameters = {}):
        BasicObjects.Diagnostic.__init__(self, name, parameters)
        try:
            import Gnuplot
            self.__gnuplot = Gnuplot
        except:
            raise ImportError("The Gnuplot module is required to plot the vector")

    def _formula(self,
            Vector, Steps,
            title, xlabel, ylabel, ltitle,
            geometry,
            filename,
            persist,
            pause ):
        """
        Trace en gnuplot chaque vecteur de la liste Vector, avec une légende
        générale, en X et en Y
        """
        if persist:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -persist -geometry '+geometry
        else:
            self.__gnuplot.GnuplotOpts.gnuplot_command = 'gnuplot -geometry '+geometry
        #
        self.__g = self.__gnuplot.Gnuplot() # persist=1
        self.__g('set terminal '+self.__gnuplot.GnuplotOpts.default_term)
        self.__g('set style data lines')
        self.__g('set grid')
        self.__g('set autoscale')
        self.__g('set title  "'+title.decode() +'"')
        self.__g('set xlabel "'+xlabel.decode()+'"')
        self.__g('set ylabel "'+ylabel.decode()+'"')
        self.__g.plot( self.__gnuplot.Data( Steps, Vector.pop(0), title=ltitle.pop(0) ) )
        for vector in Vector:
            self.__g.replot( self.__gnuplot.Data( Steps, vector, title=ltitle.pop(0) ) )
        if filename != "":
            self.__g.hardcopy(filename=filename, color=1)
        if pause:
            eval(input('Please press return to continue...\n'))
        #
        return 1

    def calculate(self, vector = None, steps = None,
                        title = "", xlabel = "", ylabel = "", ltitle = None,
                        geometry = "600x400",
                        filename = "",
                        persist  = False,
                        pause    = True ):
        """
        Arguments :
            - vector   : liste des vecteurs à tracer, chacun étant en liste ou
                         en numpy.array
            - steps    : liste unique des pas, ou None si c'est la numérotation
                         par défaut
            - title    : titre général du dessin
            - xlabel   : label de l'axe des X
            - ylabel   : label de l'axe des Y
            - ltitle   : liste des titres associés à chaque vecteur, dans le
                         même ordre que les vecteurs eux-mêmes
            - geometry : taille en pixels de la fenêtre et position du coin haut
                         gauche, au format X11 : LxH+X+Y (défaut : 600x400)
            - filename : nom de fichier Postscript pour une sauvegarde à 1 pas
                         Attention, il faut changer le nom à l'appel pour
                         plusieurs pas de sauvegarde
            - persist  : booléen indiquant que la fenêtre affichée sera
                         conservée lors du passage au dessin suivant
                         Par défaut, persist = False
            - pause    : booléen indiquant une pause après chaque tracé, et
                         attendant un Return
                         Par défaut, pause = True
        """
        if vector is None:
            raise ValueError("One vector must be given to plot it.")
        if not isinstance(vector, (list, tuple)):
            raise ValueError("The vector(s) must be given as a list/tuple.")
        if ltitle is None or len(ltitle) != len(vector):
            ltitle = ["" for i in range(len(vector))]
        VectorList = []
        for onevector in vector:
            VectorList.append( numpy.array( onevector ) )
            if VectorList[-1].size < 1:
                raise ValueError("Each given vector must not be empty.")
        if steps is None:
            Steps = list(range(len(vector[0])))
        elif not ( isinstance(steps, type([])) or not isinstance(steps, type(numpy.array([]))) ):
            raise ValueError("The steps must be given as a list/tuple.")
        else:
            Steps = list(steps)
        if os.path.isfile(filename):
            raise ValueError("Error: a file with this name \"%s\" already exists."%filename)
        #
        value = self._formula(
            Vector   = VectorList,
            Steps    = Steps,
            title    = str(title).encode('ascii','replace'),
            xlabel   = str(xlabel).encode('ascii','replace'),
            ylabel   = str(ylabel).encode('ascii','replace'),
            ltitle   = [str(lt) for lt in ltitle],
            geometry = str(geometry),
            filename = str(filename),
            persist  = bool(persist),
            pause    = bool(pause),
            )

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC \n')

    D = ElementaryDiagnostic("Mon Plot")

    vect1 = [1, 2, 1, 2, 1]
    D.calculate([vect1,], title = "Vecteur 1", xlabel = "Axe X", ylabel = "Axe Y" )
    vect2 = [1, 3, 1, 3, 1]
    D.calculate([vect1,vect2], title = "Vecteurs 1 et 2", filename = "liste_de_vecteurs.ps")
    vect3 = [-1, 1, -1, 1, -1]
    D.calculate((vect1,vect2,vect3), title = "Vecteurs 1 a 3")
    vect4 = 100*[0.29, 0.97, 0.73, 0.01, 0.20]
    D.calculate([vect4,], title = "Vecteur 4 : long construit par repetition")
    D.calculate(
        (vect1,vect2,vect3),
        [0.1,0.2,0.3,0.4,0.5],
        title = "Vecteurs 1 a 3, temps modifie",
        ltitle = ["Vecteur 1","Vecteur 2","Vecteur 3"])
    print("")
