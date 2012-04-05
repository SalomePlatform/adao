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

    Script defining the AlgorithmParameters
    """
__author__ = "Jean-Philippe ARGAUD"
#
# ==============================================================================
#
# Creating the required ADAO variable
# -----------------------------------
AlgorithmParameters = {
    "Minimizer" : "TNC",         # Possible : "LBFGSB", "TNC", "CG", "BFGS"
    "MaximumNumberOfSteps" : 15, # Number of iterative steps
    "Bounds" : [
        [ None, None ],          # Bound on the first parameter
        [ 0., 4. ],              # Bound on the second parameter
        [ 0., None ],            # Bound on the third parameter
        ],
}
#
# ==============================================================================