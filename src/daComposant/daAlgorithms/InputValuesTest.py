# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
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

import sys, logging
import numpy
from daCore import BasicObjects

# ==============================================================================
class ElementaryAlgorithm(BasicObjects.Algorithm):
    def __init__(self):
        BasicObjects.Algorithm.__init__(self, "INPUTVALUESTEST")
        self.defineRequiredParameter(
            name     = "NumberOfPrintedDigits",
            default  = 5,
            typecast = int,
            message  = "Nombre de chiffres affichés pour les impressions de réels",
            minval   = 0,
            )
        self.defineRequiredParameter(
            name     = "PrintAllValuesFor",
            default  = [],
            typecast = tuple,
            message  = "Liste de noms de vecteurs dont les valeurs détaillées sont à imprimer",
            listval  = [
                "Background",
                "CheckingPoint",
                "Observation",
                ]
            )
        self.defineRequiredParameter(
            name     = "ShowInformationOnlyFor",
            default  = ["Background", "CheckingPoint", "Observation"],
            typecast = tuple,
            message  = "Liste de noms de vecteurs dont les informations synthétiques sont à imprimer",
            listval  = [
                "Background",
                "CheckingPoint",
                "Observation",
                ]
            )
        self.defineRequiredParameter(
            name     = "SetDebug",
            default  = False,
            typecast = bool,
            message  = "Activation du mode debug lors de l'exécution",
            )
        self.requireInputArguments(
            mandatory= (),
            )
        self.setAttributes(tags=(
            "Checking",
            ))

    def run(self, Xb=None, Y=None, U=None, HO=None, EM=None, CM=None, R=None, B=None, Q=None, Parameters=None):
        self._pre_run(Parameters, Xb, Y, R, B, Q)
        #
        _p = self._parameters["NumberOfPrintedDigits"]
        numpy.set_printoptions(precision=_p)
        #
        def __buildPrintableVectorProperties( __name, __vector ):
            if __vector is None:                                         return ""
            if len(__vector) == 0:                                       return ""
            if hasattr(__vector,"name") and __name != __vector.name():   return ""
            if __name not in self._parameters["ShowInformationOnlyFor"]: return ""
            #
            if hasattr(__vector,"mins"):
                __title = "Information for %svector series:"%(str(__name)+" ",)
            else:
                __title = "Information for %svector:"%(str(__name)+" ",)
            msgs = "\n"
            msgs += ("===> "+__title+"\n")
            msgs += ("     "+("-"*len(__title))+"\n")
            msgs += ("     Main characteristics of the vector:\n")
            if hasattr(__vector,"basetype"):
                msgs += ("       Python base type..........: %s\n")%( __vector.basetype(), )
                msgs += ("       Shape of data.............: %s\n")%( __vector.shape(), )
            else:
                msgs += ("       Python base type..........: %s\n")%type( __vector )
                msgs += ("       Shape of serie of vectors.: %s\n")%( __vector.shape, )
            try:
                msgs += ("       Number of data............: %s\n")%( len(__vector), )
            except: pass
            if hasattr(__vector,"mins"):
                msgs += ("       Serie of minimum values...: %s\n")%numpy.array(__vector.mins())
            else:
                msgs += ("       Minimum of vector.........: %12."+str(_p)+"e\n")%__vector.min()
            if hasattr(__vector,"means"):
                msgs += ("       Serie of mean values......: %s\n")%numpy.array(__vector.means())
            else:
                msgs += ("       Mean of vector............: %12."+str(_p)+"e\n")%__vector.mean()
            if hasattr(__vector,"maxs"):
                msgs += ("       Serie of maximum values...: %s\n")%numpy.array(__vector.maxs())
            else:
                msgs += ("       Maximum of vector.........: %12."+str(_p)+"e\n")%__vector.max()
            if self._parameters["SetDebug"] or __name in self._parameters["PrintAllValuesFor"]:
                msgs += ("\n")
                msgs += ("     Printing all values :\n")
                msgs += ("%s"%(__vector,))
            print(msgs)
            return msgs
        #----------
        __buildPrintableVectorProperties( "Background",    Xb )
        __buildPrintableVectorProperties( "CheckingPoint", Xb )
        __buildPrintableVectorProperties( "Observation",    Y )
        #
        self._post_run(HO)
        return 0

# ==============================================================================
if __name__ == "__main__":
    print('\n AUTODIAGNOSTIC\n')
