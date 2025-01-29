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

import sys
import unittest
import math
import numpy


# ==============================================================================
class TwoDimensionalRosenbrockFunctionR1960:
    """
    Two-dimensional spatial function of µ=(a,b):

        f(x,y) = (a - x)² + b (y -x²)²

        with (x,y) ∈ [-2,2]x[-1,3]² and a=1, b=100 the commonly used parameter
        values. There exists a global minimum at (x,y) = (a,a²) for which
        f(x,y) = 0.

    This is the non-linear non-convex parametric function of the reference:
        Rosenbrock, H. H. (1960). "An Automatic Method for Finding the Greatest
        or Least Value of a Function", The Computer Journal, vol.3 (3),
        pp.175–184.
    """

    def __init__(self, nx: int = 40, ny: int = 40):
        "Définition du maillage spatial"
        self.nx = max(1, nx)
        self.ny = max(1, ny)
        self.x = numpy.linspace(-2, 2, self.nx, dtype=float)
        self.y = numpy.linspace(-1, 3, self.ny, dtype=float)

    def FieldZ(self, mu):
        "Fonction simulation pour un paramètre donné"
        a, b = numpy.ravel(mu)
        #
        x, y = numpy.meshgrid(self.x, self.y)
        sxymu = (a - x) ** 2 + b * (y - x**2) ** 2
        #
        return sxymu

    def FunctionH(self, xy, a=1, b=100):
        "Construit la fonction de Rosenbrock en L2 (Scipy 1.8.1 p.1322)"
        xy = numpy.ravel(xy).reshape((-1, 2))  # Deux colonnes
        x = xy[:, 0]
        y = xy[:, 1]
        return numpy.array([(a - x), math.sqrt(b) * (y - x**2)])

    def get_x(self):
        "Renvoie le maillage spatial"
        return self.x, self.y

    def get_sample_of_mu(self, ns1: int = 20, ns2: int = 20):
        "Renvoie l'échantillonnage paramétrique régulier"
        sa = numpy.linspace(0, 2, ns1, dtype=float)
        sb = numpy.linspace(1, 200, ns2, dtype=float)
        smu = numpy.array([(a, b) for a in sa for b in sb])
        return smu

    def get_random_sample_of_mu(self, ns1: int = 1, ns2: int = 1):
        "Renvoie l'échantillonnage paramétrique aléatoire"
        smu = []
        for i in range(ns1 * ns2):
            smu1 = numpy.random.uniform(0, 2)
            smu2 = numpy.random.uniform(1, 200)
            smu.append((smu1, smu2))
        smu = numpy.array(smu)
        return smu

    def get_bounds_on_space(self):
        "Renvoie les bornes sur le maillage spatial"
        return [[min(self.x), max(self.x)], [min(self.y), max(self.y)]]

    def get_bounds_on_parameter(self):
        "Renvoie les bornes sur le maillage paramétrique"
        return [[0, 2], [1, 200]]

    OneRealisation = FieldZ


# ==============================================================================
class LocalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nAUTODIAGNOSTIC\n==============\n")
        print("    " + TwoDimensionalRosenbrockFunctionR1960().__doc__.strip())

    def test001(self):
        numpy.random.seed(123456789)
        Equation = TwoDimensionalRosenbrockFunctionR1960()

        optimum = Equation.FunctionH([1, 1])
        self.assertTrue(max(optimum.flat) <= 0.0)

        optimum = Equation.FunctionH([0.5, 0.25], a=0.5)
        self.assertTrue(max(optimum.flat) <= 0.0)

    def tearDown(cls):
        print("\n    Tests OK\n")


# ==============================================================================
if __name__ == "__main__":
    sys.stderr = sys.stdout
    unittest.main(verbosity=0)
