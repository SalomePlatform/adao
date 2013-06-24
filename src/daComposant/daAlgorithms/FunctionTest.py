#-*-coding:iso-8859-1-*-
#
#  Copyright (C) 2008-2013 EDF R&D
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
from daCore import BasicObjects, PlatformInfo
m = PlatformInfo.SystemUsage()

import numpy

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "FUNCTIONTEST")
        self.defineRequiredParameter(
            name     = "ResultTitle",
            default  = "",
            typecast = str,
            message  = "Titre du tableau et de la figure",
            )
        self.defineRequiredParameter(
            name     = "SetDebug",
            default  = True,
            typecast = bool,
            message  = "Activation du mode debug lors de l'exécution",
            )

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        logging.debug("%s Lancement"%self._name)
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        #
        self.setParameters(Parameters)
        #
        Hm = HO["Direct"].appliedTo
        #
        Xn = numpy.asmatrix(numpy.ravel( Xb )).T
        #
        # ----------
        if len(self._parameters["ResultTitle"]) > 0:
            msg  = "     ====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
            msg += "        " + self._parameters["ResultTitle"] + "\n"
            msg += "     ====" + "="*len(self._parameters["ResultTitle"]) + "====\n"
            print("%s"%msg)
        #
        msg  = "===> Information before launching:\n"
        msg += "     -----------------------------\n"
        msg += "     Characteristics of input parameter X, internally converted:\n"
        msg += "       Type...............: %s\n"%type( Xn )
        msg += "       Lenght of vector...: %i\n"%max(numpy.matrix( Xn ).shape)
        msg += "       Minimum value......: %.5e\n"%numpy.min( Xn )
        msg += "       Maximum value......: %.5e\n"%numpy.max( Xn )
        msg += "       Mean of vector.....: %.5e\n"%numpy.mean( Xn )
        msg += "       Standard error.....: %.5e\n"%numpy.std( Xn )
        msg += "       L2 norm of vector..: %.5e\n"%numpy.linalg.norm( Xn )
        print(msg)
        #
        if self._parameters["SetDebug"]:
            CUR_LEVEL = logging.getLogger().getEffectiveLevel()
            logging.getLogger().setLevel(logging.DEBUG)
            print("===> Beginning of evaluation, activating debug\n")
        else:
            print("===> Beginning of evaluation, without activating debug\n")
        print("     %s\n"%("-"*75,))
        #
        print("===> Launching direct operator evaluation\n")
        Y = Hm( Xn )
        print("\n===> End of direct operator evaluation\n")
        #
        msg  = "===> Information after launching:\n"
        msg += "     ----------------------------\n"
        msg += "     Characteristics of output parameter Y, to compare to observation:\n"
        msg += "       Type...............: %s\n"%type( Y )
        msg += "       Lenght of vector...: %i\n"%max(numpy.matrix( Y ).shape)
        msg += "       Minimum value......: %.5e\n"%numpy.min( Y )
        msg += "       Maximum value......: %.5e\n"%numpy.max( Y )
        msg += "       Mean of vector.....: %.5e\n"%numpy.mean( Y )
        msg += "       Standard error.....: %.5e\n"%numpy.std( Y )
        msg += "       L2 norm of vector..: %.5e\n"%numpy.linalg.norm( Y )
        print(msg)
        #
        print("     %s\n"%("-"*75,))
        if self._parameters["SetDebug"]:
            print("===> End evaluation, deactivating debug if necessary\n")
            logging.getLogger().setLevel(CUR_LEVEL)
        #
        logging.debug("%s Taille mémoire utilisée de %.1f Mo"%(self._name, m.getUsedMemory("M")))
        logging.debug("%s Terminé"%self._name)
        #
        return 0

# ==============================================================================
if __name__ == "__main__":
    print '\n AUTODIAGNOSTIC \n'
