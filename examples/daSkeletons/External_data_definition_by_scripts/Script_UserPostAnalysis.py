# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2019 EDF R&D
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

    Script defining the UserPostAnalysis
    """
__author__ = "Jean-Philippe ARGAUD"
#
# ==============================================================================
#
from Physical_data_and_covariance_matrices import True_state
import numpy
numpy.set_printoptions(precision=4)
#
xt, names   = True_state()
xa          = ADD.get("Analysis")[-1]
x_series    = ADD.get("CurrentState")[:]
J           = ADD.get("CostFunctionJ")[:]
#
# Verifying the results by printing
# ---------------------------------
print("")
print("obs = [%s]"%(", ".join(["%.4f"%v for v in ADD.get("Observation").A1])))
print("")
print("xb  = [%s]"%(", ".join(["%.4f"%v for v in ADD.get("Background").A1])))
print("xt  = [%s]"%(", ".join(["%.4f"%v for v in numpy.array(xt)])))
print("xa  = [%s]"%(", ".join(["%.4f"%v for v in numpy.array(xa)])))
print("")
for i in range( len(x_series) ):
    print("Step %2i : J = %.4e     X = [%s]"%(i, J[i], ", ".join(["%.4f"%v for v in x_series[i]])))
print("")
#
# ==============================================================================
