# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2026 EDF R&D
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
import scipy
import math


# ==============================================================================
class OneDimensionalLinearDiffusionEquation:
    """
    One-dimensional linear diffusion equation of parameter α:

        ð_t u(x,t) = α ð²_x u(x,t)       for (x,t) ∈ [0,Lx] x [0,Tf]
        u(x,0) = u_0(x)                  for x ∈ [0,Lx]
        u(0,t) = u(Lx,t) = 0             for t ∈ [0,Tf]

    whose solution is denoted u(x,t)=u(x,t,α,σ) to emphasize the dependency
    with one diffusion parameter α and one parameter σ embedded in initial
    conditions u_0(x)=u_0(x,σ). Possible initial conditions are:

        "CenteredSin"   : u_0(x,σ) = π² * sin(σ * π * x)
        "CenteredGauss" : u_0(x,σ) = exp(-100 * σ * (x - Lx/2)²)
        "CenteredHat"   : u_0(x,σ) = 2. * σ * (Lx/2 - |x - Lx/2|)
        "CenteredPeak"  : u_0(x,σ) = 0 for x ∈ [0,Lx] but u_0(Lx/2) = σ

    By default : α = Lx = Tf = σ = 1, u[0] = u[Lx] = 0
    """

    def __init__(
        self,
        alpha: float = 1,
        ndt: int = 10,
        Tf: float = 1,
        ndx: int = 100,
        Lx: float = 1,
        stationary: bool = True,
        IC: str = "CenteredSin",
        sigma: float = 1,
    ):
        # Set domain parameters
        self.ndt = max(0, ndt)
        self.Tf = Tf
        self.ndx = max(1, ndx)
        self.Lx = Lx
        self.t = numpy.linspace(0, self.Tf, self.ndt, dtype=float)
        self.x = numpy.linspace(0, self.Lx, self.ndx, dtype=float)
        self.dt = self.Tf / (self.ndt - 1)
        self.dx = self.Lx / (self.ndx - 1)
        #
        self.stationary = stationary
        #
        self.setDiffusionCoefficientAndMatrix(alpha)
        self.setInitialCondition(IC, sigma)

    def setDiffusionCoefficientAndMatrix(self, alpha: float = 1):
        self.alpha = alpha
        self.A = numpy.zeros((3, self.ndx))  # Tri-diagonal banded matrix
        if self.stationary:
            asdx2 = self.alpha / self.dx**2
            self.A[0, 2:-1] = -asdx2
            self.A[1, :] = 2 * asdx2
            self.A[2, 1:-2] = -asdx2
        else:
            adtsdx2 = self.alpha * self.dt / self.dx**2
            self.A[0, 2:-1] = -adtsdx2
            self.A[1, :] = 1 + 2 * adtsdx2
            self.A[2, 1:-2] = -adtsdx2

    def setInitialCondition(self, IC: str = "CenteredSin", sigma: float = 1):
        self.IC = IC
        self.sigma = sigma
        if self.IC == "CenteredSin":
            self.u0 = math.pi**2 * numpy.sin(self.sigma * math.pi * self.x)
        elif self.IC == "CenteredGauss":
            self.u0 = numpy.exp(-100 * self.sigma * (self.x - self.Lx / 2) ** 2)
        elif self.IC == "CenteredHat":
            self.u0 = 2.0 * self.sigma * (self.Lx / 2 - numpy.abs(self.x - self.Lx / 2))
        elif self.IC == "CenteredPeak":
            self.u0 = numpy.zeros(self.x.shape)
            self.u0[self.ndx // 2] = self.sigma
        else:
            raise ValueError("Initial Condition '%s' is not allowed" % str(IC))

    def FieldUFromDiffusionCoefficient(self, alpha: float = 1):
        "Here, the parameter is the diffusion coefficient"
        alpha = float(numpy.ravel(alpha)[0])
        self.setDiffusionCoefficientAndMatrix(alpha)
        return scipy.linalg.solve_banded((1, 1), self.A, self.u0)

    def FieldUFromInitialConditionCoefficient(self, sigma: float = 1):
        "Here, the parameter is the initial condition coefficient"
        raise ValueError("Warning: function to be implemented")

    def EvolutionUFromDiffusionCoefficient(self, XX):
        "Here, the parameter is the diffusion coefficient"
        raise ValueError("Warning: function to be implemented")

    def EvolutionUFromInitialConditionCoefficient(self, XX):
        "Here, the parameter is the initial condition coefficient"
        raise ValueError("Warning: function to be implemented")

    def get_t(self):
        return self.t

    def get_x(self):
        return self.x

    def get_u0(self):
        return self.u0

    def get_sample_of_mu(self, ns: int = 1):
        raise ValueError("Warning: function to be implemented")

    OneRealisation = FieldUFromDiffusionCoefficient


# ==============================================================================
class LocalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nAUTODIAGNOSTIC\n==============\n")
        print("    " + OneDimensionalLinearDiffusionEquation().__doc__.strip())

    def test001(self, Figure=False):
        numpy.set_printoptions(precision=5)
        Equation = OneDimensionalLinearDiffusionEquation()  # Default parameters
        #
        alpha = 0.2
        state = Equation.OneRealisation(alpha)
        u0 = Equation.get_u0()
        print("\n    Initial condition u_0:\n", u0)
        print("\n    Solution for α=%.2f:" % alpha, "\n", state)
        self.assertTrue(-1.0e-15 < state[0] < 1.0e-15)  # Null left condition
        self.assertTrue(-1.0e-15 < state[-1] < 1.0e-15)  # Null right condition
        self.assertTrue(4.999 < state[50] < 5.0)  # Value at middle
        #
        print("\n    Tests 001 OK")
        if Figure:
            import matplotlib.pyplot as plt

            x = Equation.get_x()
            plt.plot(x, u0, label="Initial condition")
            plt.plot(x, state, "--", label="Solution for α=%.2f" % alpha)
            plt.xlabel("x")
            plt.ylabel("u(x)")
            plt.title("Simulation of the static linear diffusion equation in 1D")
            plt.legend()
            plt.grid(True)
            plt.show()

    def tearDown(cls):
        print("\n    Tests OK\n")


# ==============================================================================
if __name__ == "__main__":
    sys.stderr = sys.stdout
    unittest.main(verbosity=0)
