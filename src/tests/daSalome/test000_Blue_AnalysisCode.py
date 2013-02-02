#-*-coding:iso-8859-1-*-
# Copyright (C) 2010-2012 EDF R&D
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

import numpy
precision = 1.e-13

Xa = ADD.get("Analysis")
print
print "    Nombre d'analyses  :",Xa.stepnumber()
print "    Analyse r�sultante :",Xa[0]
#
# V�rification du r�sultat
# ------------------------
if max(numpy.array(Xa[0])-numpy.array([0.25, 1.25, 2.25])) > precision:
  raise ValueError("R�sultat du test erron�")
else:
  print "    Test correct, erreur maximale inf�rieure � %s"%precision
  print

