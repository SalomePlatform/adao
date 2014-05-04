#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2014 EDF R&D
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

import logging
from daCore import BasicObjects
import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "OBSERVERTEST")

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run()
        print "Results of observer check on all potential variables or commands,"
        print "         only activated on selected ones by explicit association."
        print
        #
        # Paramètres de pilotage
        # ----------------------
        self.setParameters(Parameters)
        #
        __Xa = 1.+numpy.arange(3.)
        __Xb = numpy.zeros(3)
        __YY = 1.+numpy.arange(5.)
        #
        # Activation des observers sur toutes les variables stockables
        # ------------------------------------------------------------
        self.StoredVariables["Analysis"].store( __Xa )
        self.StoredVariables["CurrentState"].store( __Xa )
        self.StoredVariables["CostFunctionJb"].store( 1. )
        self.StoredVariables["CostFunctionJo"].store( 2. )
        self.StoredVariables["CostFunctionJ" ].store( 3. )
        #
        self.StoredVariables["APosterioriCovariance"].store( numpy.diag(__Xa) )
        self.StoredVariables["BMA"].store( __Xb - __Xa )
        self.StoredVariables["OMA"].store( __YY )
        self.StoredVariables["OMB"].store( __YY )
        self.StoredVariables["Innovation"].store( __YY )
        self.StoredVariables["SigmaObs2"].store( 1. )
        self.StoredVariables["SigmaBck2"].store( 1. )
        self.StoredVariables["MahalanobisConsistency"].store( 1. )
        self.StoredVariables["SimulationQuantiles"].store( numpy.matrix((__YY,__YY,__YY)) )
        #
        print
        self._post_run()
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
