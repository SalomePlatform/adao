#-*-coding:iso-8859-1-*-
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
    Classe pour tracer simplement un vecteur à chaque pas
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
        Trace en gnuplot le vecteur Vector, avec une légende générale, en X et
        en Y
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
        self.__g('set title  "'+title +'"')
        self.__g('set xlabel "'+xlabel+'"')
        self.__g('set ylabel "'+ylabel+'"')
        self.__g.plot( self.__gnuplot.Data( Steps, Vector, title=ltitle ) )
        if filename != "":
            self.__g.hardcopy(filename=filename, color=1)
        if pause:
            raw_input('Please press return to continue...\n')
        #
        return 1

    def calculate(self, vector = None, steps = None,
                        title = "", xlabel = "", ylabel = "", ltitle = "",
                        geometry = "600x400",
                        filename = "",
                        persist  = False,
                        pause    = True ):
        """
        Arguments :
            - vector   : le vecteur à tracer, en liste ou en numpy.array
            - steps    : liste unique des pas de l'axe des X, ou None si c'est
                         la numérotation par défaut
            - title    : titre général du dessin
            - xlabel   : label de l'axe des X
            - ylabel   : label de l'axe des Y
            - ltitle   : titre associé au vecteur tracé
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
        Vector = numpy.array(vector)
        if Vector.size < 1:
            raise ValueError("The given vector must not be empty")
        if steps is None:
            Steps = range(len( vector ))
        elif not ( type(steps) is type([]) or type(steps) is not type(numpy.array([])) ):
            raise ValueError("The steps must be given as a list/tuple.")
        else:
            Steps = list(steps)
        if os.path.isfile(filename):
            raise ValueError("Error: a file with this name \"%s\" already exists."%filename)
        #
        value = self._formula(
            Vector   = Vector,
            Steps    = Steps,
            title    = str(title).encode('ascii','replace'),
            xlabel   = str(xlabel).encode('ascii','replace'),
            ylabel   = str(ylabel).encode('ascii','replace'),
            ltitle   = str(ltitle),
            geometry = str(geometry),
            filename = str(filename),
            persist  = bool(persist),
            pause    = bool(pause) )

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'

    D = ElementaryDiagnostic("Mon Plot")

    vect = [1, 2, 1, 2, 1]
    D.calculate(vect, title = "Vecteur 1", xlabel = "Axe X", ylabel = "Axe Y" )
    vect = [1, 3, 1, 3, 1]
    D.calculate(vect, title = "Vecteur 2", filename = "vecteur.ps")
    vect = [1, 1, 1, 1, 1]
    D.calculate(vect, title = "Vecteur 3")
    vect = [0.29, 0.97, 0.73, 0.01, 0.20]
    D.calculate(vect, title = "Vecteur 4")
    vect = [-0.23262176, 1.36065207,  0.32988102, 0.24400551, -0.66765848, -0.19088483, -0.31082575,  0.56849814,  1.21453443,  0.99657516]
    D.calculate(vect, title = "Vecteur 5")
    vect = [0.29, 0.97, 0.73, 0.01, 0.20]
    D.calculate(vect, title = "Vecteur 6 affiche avec une autre geometrie et position", geometry="800x200+50+50")
    vect = 100*[0.29, 0.97, 0.73, 0.01, 0.20]
    D.calculate(vect, title = "Vecteur 7 : long construit par repetition")
    vect = [0.29, 0.97, 0.73, 0.01, 0.20]
    D.calculate(vect, title = "Vecteur 8", ltitle = "Vecteur 8")
    temps = [0.1,0.2,0.3,0.4,0.5]
    D.calculate(vect, temps, title = "Vecteur 8 avec axe du temps modifie")
    print
