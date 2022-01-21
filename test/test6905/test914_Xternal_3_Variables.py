# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2022 EDF R&D
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

dimension = 5

Background = [-1. for i in range(dimension)]

Observation = [1. for i in range(dimension)]

sigmaB2 = 1.
BackgroundError = [[0. for i in range(dimension)] for i in range(dimension)]
for i in range(dimension):
    BackgroundError[i][i] = sigmaB2

sigmaO2 = 1.
ObservationError = [[0. for i in range(dimension)] for i in range(dimension)]
for i in range(dimension):
    ObservationError[i][i] = sigmaO2

ObservationOperator = [[0. for i in range(dimension)] for i in range(dimension)]
# dimension * [ dimension * [0.] ]
for i in range(dimension):
    ObservationOperator[i][i] = 2.
for i in range(dimension-1):
    ObservationOperator[i+1][i] = -1.
    ObservationOperator[i][i+1] = -1.

AlgorithmParameters = {
    "SetSeed" : 1000,
    "Minimizer" : "LBFGSB",
    "MaximumNumberOfSteps" : 15,
    }
