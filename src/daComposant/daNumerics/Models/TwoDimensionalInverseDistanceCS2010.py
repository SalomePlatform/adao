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
import numpy


# ==============================================================================
class TwoDimensionalInverseDistanceCS2010:
    """
    Two-dimensional inverse distance function of parameter µ=(µ1,µ2):

        s(x,y,µ) = 1 / sqrt( (x-µ1)² + (y-µ2)² + 0.1² )

        with (x,y) ∈ [0.1,0.9]² and µ=(µ1,µ2) ∈ [-1,-0.01]².

    This is the non-linear parametric function (3.38) of the reference:
        Chaturantabut, S., Sorensen, D. C. (2010). "Nonlinear Model Reduction
        via Discrete Empirical Interpolation", SIAM Journal on Scientific
        Computing, vol.32 (5), pp. 2737-2764.
    """

    def __init__(self, nx: int = 20, ny: int = 20):
        "Définition du maillage spatial"
        self.nx = max(1, nx)
        self.ny = max(1, ny)
        self.x = numpy.linspace(0.1, 0.9, self.nx, dtype=float)
        self.y = numpy.linspace(0.1, 0.9, self.ny, dtype=float)

    def FieldG(self, mu):
        "Fonction simulation pour un paramètre donné"
        mu1, mu2 = numpy.ravel(mu)
        #
        x, y = numpy.meshgrid(self.x, self.y)
        sxymu = 1.0 / numpy.sqrt((x - mu1) ** 2 + (y - mu2) ** 2 + 0.1**2)
        #
        return sxymu

    def get_x(self):
        "Renvoie le maillage spatial"
        return self.x, self.y

    def get_sample_of_mu(self, ns1: int = 20, ns2: int = 20):
        "Renvoie l'échantillonnage paramétrique régulier"
        smu1 = numpy.linspace(-1, -0.01, ns1, dtype=float)
        smu2 = numpy.linspace(-1, -0.01, ns2, dtype=float)
        smu = numpy.array([(mu1, mu2) for mu1 in smu1 for mu2 in smu2])
        return smu

    def get_random_sample_of_mu(self, ns1: int = 1, ns2: int = 1):
        "Renvoie l'échantillonnage paramétrique aléatoire"
        smu = []
        for i in range(ns1 * ns2):
            smu1 = numpy.random.uniform(-1, -0.01)
            smu2 = numpy.random.uniform(-1, -0.01)
            smu.append((smu1, smu2))
        smu = numpy.array(smu)
        return smu

    def get_bounds_on_space(self):
        "Renvoie les bornes sur le maillage spatial"
        return [[min(self.x), max(self.x)], [min(self.y), max(self.y)]]

    def get_bounds_on_parameter(self):
        "Renvoie les bornes sur le maillage paramétrique"
        return [[-1, -0.01]] * 2

    OneRealisation = FieldG


# ==============================================================================
class LocalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nAUTODIAGNOSTIC\n==============\n")
        print("    " + TwoDimensionalInverseDistanceCS2010().__doc__.strip())

    def test001(self):
        numpy.random.seed(123456789)
        Equation = TwoDimensionalInverseDistanceCS2010()
        for mu in Equation.get_sample_of_mu(5, 5):
            solution = Equation.OneRealisation(mu)
            # Nappe maximale au coin (0,0)
            self.assertTrue(numpy.max(solution.flat) <= solution[0, 0])
            # Nappe minimale au coin [-1,-1]
            self.assertTrue(numpy.min(solution.flat) >= solution[-1, -1])

    def tearDown(cls):
        print("\n    Tests OK\n")


# ==============================================================================
if __name__ == "__main__":
    sys.stderr = sys.stdout
    unittest.main(verbosity=0)
