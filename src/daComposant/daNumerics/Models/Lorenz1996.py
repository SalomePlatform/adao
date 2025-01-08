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
import numpy as np
from daCore.BasicObjects import DynamicalSimulator


# ==============================================================================
class EDS(DynamicalSimulator):
    """
    N-dimensional parametrized nonlinear ODE system depending on a F forcing
    term:

        dy[i]/dt = (y[i+1] − y[i-2]) * y[i-1] − y[i] + F

        with i=1,...,N and periodic conditions coming from circle-like domain
        for the N variables: y[0]=y[N], y[-1]=y[N-1], y[1]=y[N+1]. With a
        forcing term F value of 8, the dynamics of this model is chaotic.

    This Lorenz96 model was first described during a seminar at the European
    Center for Medium-Range Weather Forecasts (ECMWF) in the Autumn of 1995
    (Seminar on Predictability, 4-8 September 1995), the proceedings of which
    were published as Lorenz (1996):
        Lorenz, E.N. "Predictability: A problem partly solved". In Proceedings
        of the Seminar on Predictability, ECMWF, Reading, UK, 9–11 September
        1996, Volume 1, pp. 1-18.
    See:
    https://www.ecmwf.int/en/elibrary/75462-predictability-problem-partly-solved
    The system is chaotic and numerically very sensible, even on the order of
    numerical calculations.
    """

    def CanonicalDescription(self):
        N = 40
        self.Parameters = (N, 8.0)  # N, F
        self.Integrator = "odeint"
        self.IntegrationStep = 0.05
        self.InitialTime = 0.0
        self.FinalTime = 1.0
        self.InitialCondition = np.arange(N)
        self.Autonomous = True
        return True

    def ODEModel(self, t, Y):
        "ODE dy/dt = F_µ(t, y)"
        N, F = self.Parameters
        N = int(N)
        F = float(F)
        Y = np.ravel(Y)
        dydt = np.zeros(np.shape(Y))
        assert len(Y) == N, "%i =/= %i" % (len(Y), N)
        #
        # Boundary case equations (rank 1, 2, N):
        dydt[0] = (Y[1] - Y[N - 2]) * Y[N - 1] - Y[0]
        dydt[1] = (Y[2] - Y[N - 1]) * Y[0] - Y[1]
        dydt[-1] = (Y[0] - Y[-3]) * Y[-2] - Y[-1]
        # General indices (rank 3 to N-1)
        dydt[2:-1] = (Y[3:] - Y[:-3]) * Y[1:-2] - Y[2:-1]
        # Adding forcing
        dydt = dydt + F
        #
        return dydt


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
        lastvalue = np.array(
            [
                4.87526450e00,
                1.47956922e00,
                -3.59900230e00,
                1.04256938e00,
                3.63094386e00,
                1.88075245e01,
                -1.67896983e01,
                9.47857563e00,
                -4.10761433e01,
                -7.22094136e00,
                1.82999964e01,
                -9.50258813e00,
                1.97970038e01,
                -9.14157688e-01,
                -3.23915931e00,
                9.08515096e00,
                1.90398329e01,
                6.63360465e00,
                3.62060706e00,
                1.40450966e00,
                -4.23014939e00,
                3.12067035e00,
                -7.45630836e00,
                5.29044964e00,
                -4.95916975e00,
                1.49074059e00,
                -5.34660284e00,
                7.88846593e00,
                9.82088697e00,
                9.01760941e-01,
                7.27891147e00,
                4.66438119e00,
                -1.22290917e00,
                3.38177733e00,
                6.19234382e00,
                3.66288450e00,
                2.51247077e00,
                3.61265491e00,
                4.56523506e00,
                5.03793331e00,
            ]
        )
        #
        print()
        self.assertTrue(
            trajectory.shape[0] == 1 + int(ODE.FinalTime / ODE.IntegrationStep)
        )
        erreur = abs(max(trajectory[-1] - lastvalue))
        self.assertTrue(
            erreur <= 1.0e-7,
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
