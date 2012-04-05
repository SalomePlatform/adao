#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2011  EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
#  Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

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
#
xt, names   = True_state()
xa          = ADD.get("Analysis").valueserie(-1)
x_series    = ADD.get("CurrentState").valueserie()
J           = ADD.get("CostFunctionJ").valueserie()
#
# Verifying the results by printing
# ---------------------------------
print
print "xt = %s"%xt
print "xa = %s"%numpy.array(xa)
print
for i in range( len(x_series) ):
    print "Step %2i : J = %.5e  et  X = %s"%(i, J[i], x_series[i])
print
#
# ==============================================================================