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

__doc__ = """
    ADAO skeleton case, for wide script usage in case definition
    ------------------------------------------------------------

    Script defining the Background
    """
__author__ = "Jean-Philippe ARGAUD"
#
# ==============================================================================
#
import sys, os ; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from Physical_data_and_covariance_matrices import True_state
import numpy
numpy.random.seed(1000)
#
xt, names = True_state()
#
Standard_deviation = 0.2*xt # 20% for each variable
#
xb = xt + abs(numpy.random.normal(0.,Standard_deviation,size=(len(xt),)))
#
# Creating the required ADAO variable
# -----------------------------------
Background = list(xb)
#
# ==============================================================================
