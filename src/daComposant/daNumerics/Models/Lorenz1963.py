# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2024 EDF R&D
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
from daCore.BasicObjects import DynamicalSimulator


# ==============================================================================
class Lorenz1963(DynamicalSimulator):
    """
    Three-dimensional parametrized nonlinear ODE system depending on µ=(σ,ρ,β):

        ∂x/∂t = σ (y − x)
        ∂y/∂t = ρ x − y − x z
        ∂z/∂t = x y − β z

        with t ∈ [0, 40] the time interval, x(t), y(t), z(t) the dependent
        variables, and with σ=10, ρ=28, and β=8/3 the commonly used parameter
        values. The initial conditions for (x, y, z) at t=0 for the reference
        case are (0, 1, 0).

    This is the well known parametrized coupled system of three nonlinear
    ordinary differential equations:
        Lorenz, E. N. (1963). Deterministic nonperiodic flow. Journal of the
        Atmospheric Sciences, 20, 130–141.
        doi:10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2
    """

    def set_canonical_description(self):
        self.set_mu((10.0, 28.0, 8.0 / 3.0))  # µ = (σ, ρ, β)
        self.set_integrator("rk4")
        self.set_dt(0.01)
        self.set_t0(0.0)
        self.set_tf(40)
        self.set_y0((0.0, 1.0, 0.0))
        self.set_autonomous(True)
        return True

    def ODEModel(self, t, Y):
        "ODE dY/dt = F(Y,t)"
        sigma, rho, beta = self.set_mu()
        x, y, z = map(float, Y)
        #
        rx = sigma * (y - x)
        ry = x * rho - y - x * z
        rz = x * y - beta * z
        #
        return numpy.array([rx, ry, rz])


# ==============================================================================
class LocalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nAUTODIAGNOSTIC\n==============\n")
        print("    " + Lorenz1963().__doc__.strip())

    def test001(self):
        numpy.random.seed(123456789)
        ODE = Lorenz1963()  # Default parameters
        trajectory = ODE.ForecastedPath()
        #
        print()
        self.assertTrue(trajectory.shape[0] == 1 + int(ODE.set_tf() / ODE.set_dt()))
        self.assertTrue(
            abs(
                max(
                    trajectory[-1]
                    - numpy.array([16.48799962, 14.01693428, 40.30448848])
                )
            )
            <= 1.0e-8,
            msg="    Last value is not equal to the reference one",
        )
        print("    Last value is equal to the reference one")

    def tearDown(cls):
        print("\n    Tests are finished\n")


# ==============================================================================
if __name__ == "__main__":
    sys.stderr = sys.stdout
    unittest.main(verbosity=0)
