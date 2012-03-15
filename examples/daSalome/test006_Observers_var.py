#-*-coding:iso-8859-1-*-
# Copyright (C) 2010-2011 EDF R&D
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
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

import numpy
#
# Definition of the Background as a vector
# ----------------------------------------
Background = init_data["Background"]
#
# Definition of the Observation as a vector
# -----------------------------------------
Observation = init_data["Observation"]
#
# Definition of the Background Error covariance as a matrix
# ---------------------------------------------------------
BackgroundError = init_data["BackgroundError"]
#
# Definition of the Observation Error covariance as a matrix
# ----------------------------------------------------------
ObservationError = init_data["ObservationError"]
#
# Definition of the Observation Operator as a matrix
# --------------------------------------------------
AlgorithmParameters = init_data["AlgorithmParameters"]
