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
from daCore.BasicObjects import DynamicalSimulator


# ==============================================================================
class EDS(DynamicalSimulator):
    """
    Three-dimensional parametrized nonlinear ODE system depending on µ=(σ,ρ,β):

        dx/dt = σ (y − x)
        dy/dt = ρ x − y − x z
        dz/dt = x y − β z

        with t ∈ [0, 40] the time interval, x(t), y(t), z(t) the dependent
        variables, and with σ=10, ρ=28, and β=8/3 the commonly used parameter
        values. The initial conditions for (x, y, z) at t=0 for the reference
        case are (0, 1, 0).

    This Lorenz3D model was described in:
        Lorenz, E. N. (1963). "Deterministic nonperiodic flow". Journal of the
        Atmospheric Sciences, 20, 130–141.
        doi:10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2
    """

    def CanonicalDescription(self):
        self.Parameters = (10.0, 28.0, 8.0 / 3.0)  # µ = (σ, ρ, β)
        self.Integrator = "rk4"
        self.IntegrationStep = 0.01
        self.InitialTime = 0.0
        self.FinalTime = 40
        self.InitialCondition = (0.0, 1.0, 0.0)
        self.Autonomous = True
        return True

    def ODEModel(self, t, xyz):
        "ODE dy/dt = F_µ(t, y)"
        sigma, rho, beta = self.Parameters
        x, y, z = numpy.ravel(numpy.array(xyz, dtype=float))  # map(float, xyz)
        #
        dxdt = sigma * (y - x)
        dydt = x * rho - y - x * z
        dzdt = x * y - beta * z
        #
        return numpy.array([dxdt, dydt, dzdt])

    def ODETLMModel(self, t, xyz):
        "Return the tangent linear matrix"
        sigma, rho, beta = self.Parameters
        x, y, z = numpy.ravel(numpy.array(xyz, dtype=float))  # map(float, xyz)
        nt = self.InitialCondition.size
        tlm = numpy.zeros((nt, nt))
        #
        tlm[0, :] = [-sigma, sigma, 0]
        tlm[1, :] = [rho - z, -1, -x]
        tlm[2, :] = [y, x, -beta]
        #
        return tlm


# ==============================================================================
class LocalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nAUTODIAGNOSTIC\n==============\n")
        print("    " + EDS().__doc__.strip())

    def test001(self):
        ODE = EDS()  # Default parameters
        ODE.ObservationStep = 0.2
        trajectory = ODE.ForecastedPath()
        lastvalue = numpy.array([16.48799962, 14.01693428, 40.30448848])
        #
        print()
        self.assertTrue(
            trajectory.shape[0] == 1 + int(ODE.FinalTime / ODE.IntegrationStep)
        )
        erreur = abs(max(trajectory[-1] - lastvalue))
        self.assertTrue(
            erreur <= 1.0e-8,
            msg="    Last value is not equal to the reference one. Error = %.2e"
            % erreur,
        )
        print("    Last value is equal to the reference one")

    def tearDown(cls):
        print("\n    Tests are finished\n")


# ==============================================================================
if __name__ == "__main__":
    sys.stderr = sys.stdout
    unittest.main(verbosity=0)
