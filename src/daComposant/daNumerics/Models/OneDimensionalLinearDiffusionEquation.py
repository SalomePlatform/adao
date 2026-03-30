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
from daCore.BasicObjects import DynamicalSimulator

numpy.set_printoptions(precision=5)


# ==============================================================================
class OneDimensionalLinearDiffusionEquation(DynamicalSimulator):
    """
    One-dimensional linear diffusion equation of parameters α, σ_i and σ_s:

        Un-stationary version write:

            ð_t u(x,t) - α ð²_x u(x,t) = s(x,t)     for (x,t) ∈ [0,Lx] x [0,Tf]
            u(x,0) = u_0(x)                         for x ∈ [0,Lx]
            u(0,t) = u(Lx,t) = 0                    for t ∈ [0,Tf]

        Stationary version write:

            - α ð²_x u(x,t) = s(x,t)                for (x,t) ∈ [0,Lx] x [0,Tf]
            u(x,0) = u_0(x)                         for x ∈ [0,Lx]
            u(0,t) = u(Lx,t) = 0                    for t ∈ [0,Tf]

    whose solution is denoted u(x,t)=u(x,t,α,σ) to emphasize the dependencies
    with one diffusion parameter α and with one parameter σ embedded in initial
    conditions u_0(x)=u_0(x,σ). The constant source term is s(x,t,σ_s)
    depending on one parameter σ_s. Possible source terms or initial conditions
    are (a function f(x,σ) is written for one general parameter σ):

        "Null"          : f(x,σ) = 0
        "CenteredSin"   : f(x,σ) = π² * sin(σ * π * x)
        "CenteredGauss" : f(x,σ) = exp(-100 * σ * (x - Lx/2)²)
        "CenteredHat"   : f(x,σ) = 2. * σ * (Lx/2 - |x - Lx/2|)
        "CenteredPeak"  : f(x,σ) = 0 for x ∈ [0,Lx] but u_0(Lx/2) = σ
        "CenteredWall"  : a centered wall on [0,Lx]
        "SinPlusWall"   : f(x,σ) is sinusoidal on [0,Lx/2] and a centered
                          wall on [Lx/2,Lx]

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
        InitialCondition: str = "Null",
        SourceTerm: str = "CenteredSin",
        sigma_i: float = 1,
        sigma_s: float = 1,
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
        self.setInitialConditionAndSourceTerm(
            InitialCondition, sigma_i, SourceTerm, sigma_s
        )
        #
        DynamicalSimulator.__init__(self)

    def CanonicalDescription(self):
        self.Parameters = self.alpha  # µ = (α)
        self.Integrator = "solve_ivp"
        self.IntegrationStep = self.dt
        self.InitialTime = 0.0
        self.FinalTime = self.Tf
        self.InitialCondition = self.u0
        self.Autonomous = True
        return True

    def ODEModel(self, t, y):
        "ODE dy/dt = F_µ(t, y)"
        return numpy.dot(self.A, y)

    def ODETLMModel(self, t, xyz):
        "Return the tangent linear matrix"
        return self.A

    def setDiffusionCoefficientAndMatrix(self, alpha: float = 1):
        self.alpha = alpha
        if self.stationary:
            self.A = numpy.zeros((3, self.ndx))  # Tri-diagonal banded matrix
            asdx2 = self.alpha / self.dx**2
            self.A[0, 2:-1] = -asdx2
            self.A[1, :] = 2 * asdx2
            self.A[2, 1:-2] = -asdx2
        else:
            adtsdx2 = self.alpha * self.dt / self.dx**2
            self.A = -(
                numpy.diag(numpy.ones(self.ndx) * (2 * adtsdx2))
                + numpy.diag(numpy.ones(self.ndx - 1) * (-adtsdx2), 1)
                + numpy.diag(numpy.ones(self.ndx - 1) * (-adtsdx2), -1)
            )
            self.A[0, 1] = self.A[1, 0] = 0
            self.A[-1, -2] = self.A[-2, -1] = 0

    def setInitialConditionAndSourceTerm(
        self, IC: str = "Null", sigma_i: float = 1, ST: str = "Null", sigma_s: float = 1
    ):
        self.sigma_i, self.u0 = self.setInitialConditionOrSourceTerm(IC, sigma_i)
        self.sigma_s, self.st = self.setInitialConditionOrSourceTerm(ST, sigma_s)

    def setInitialConditionOrSourceTerm(
        self, Predefined: str = "Null", sigma: float = 1
    ):
        if Predefined == "Null":
            field = numpy.zeros(self.x.size)
        elif Predefined == "CenteredSin":
            field = math.pi**2 * numpy.sin(sigma * math.pi * self.x)
        elif Predefined == "CenteredGauss":
            field = numpy.exp(-100 * sigma * (self.x - self.Lx / 2) ** 2)
        elif Predefined == "CenteredHat":
            field = 2.0 * sigma * (self.Lx / 2 - numpy.abs(self.x - self.Lx / 2))
        elif Predefined == "CenteredPeak":
            field = numpy.zeros(self.x.shape)
            field[self.ndx // 2] = sigma
        elif Predefined == "CenteredWall":
            field = numpy.array(0.40 * self.Lx < self.x, dtype=int) * numpy.array(
                self.x < 0.60 * self.Lx, dtype=int
            )
        elif Predefined == "SinPlusWall":
            field = 0.5 * (
                1 + numpy.sin(4 * math.pi * self.x - 0.5 * math.pi)
            ) * numpy.array(0.0 * self.Lx < self.x, dtype=int) * numpy.array(
                self.x < 0.5 * self.Lx, dtype=int
            ) + numpy.array(
                0.70 * self.Lx < self.x, dtype=int
            ) * numpy.array(
                self.x < 0.80 * self.Lx, dtype=int
            )
        else:
            raise ValueError("Predefined choice '%s' is not allowed" % str(Predefined))
        return sigma, field

    def FieldUFromDiffusionCoefficient(self, coefficient):
        "Here, the parameter is the diffusion coefficient"
        alpha = numpy.ravel(numpy.array(coefficient, dtype=float))[0]
        self.setDiffusionCoefficientAndMatrix(alpha)
        solution = scipy.linalg.solve_banded((1, 1), self.A, self.st)
        return solution

    def FieldUFromInitialConditionCoefficient(self, coefficient):
        "Here, the parameter is the initial condition coefficient"
        sigma_i = numpy.ravel(numpy.array(coefficient, dtype=float))[0]
        raise ValueError("Warning: function to be implemented")

    def FieldUFromSourceTermCoefficient(self, coefficient):
        "Here, the parameter is the source term coefficient"
        sigma_s = numpy.ravel(numpy.array(coefficient, dtype=float))[0]
        raise ValueError("Warning: function to be implemented")

    def FieldUFromAllCoefficients(self, coefficients):
        "Here, the parameter is the source term coefficient"
        alpha, sigma_i, sigma_s = numpy.ravel(numpy.array(coefficients, dtype=float))
        raise ValueError("Warning: function to be implemented")

    def get_t(self):
        return self.t

    def get_dt(self):
        return self.dt

    def get_dx(self):
        return self.dx

    def get_x(self):
        return self.x

    def get_u0(self):
        return self.u0

    def get_st(self):
        return self.st

    def get_sample_of_mu(self, ns: int = 1):
        raise ValueError("Warning: function to be implemented")

    OneRealisation = FieldUFromAllCoefficients


# ==============================================================================
class LocalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nAUTODIAGNOSTIC\n==============\n")
        print("    " + OneDimensionalLinearDiffusionEquation().__doc__.strip())

    @unittest.skip("Debug")
    def test001(self, Figure=False):
        Equation = OneDimensionalLinearDiffusionEquation()  # Default parameters
        #
        alpha = 0.2
        state = Equation.FieldUFromDiffusionCoefficient(alpha)
        st = Equation.get_st()
        print("\n    Source term s:\n", st)
        print("\n    Solution for α=%.2f:" % alpha, "\n", state)
        self.assertTrue(-1.0e-15 < state[0] < 1.0e-15)  # Null left condition
        self.assertTrue(-1.0e-15 < state[-1] < 1.0e-15)  # Null right condition
        self.assertTrue(4.999 < state[50] < 5.0)  # Value at middle
        #
        print("\n    Tests 001 OK")
        if Figure:
            import matplotlib.pyplot as plt

            x = Equation.get_x()
            plt.plot(x, st, label="Source term")
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
