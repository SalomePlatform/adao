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
precision = 1.e-13

Xa = ADD.get("Analysis")
print
print "    Nombre d'analyses  :",Xa.stepnumber()
print "    Analyse résultante :",Xa.valueserie(0)
#
# Vérification du résultat
# ------------------------
if max(numpy.array(Xa.valueserie(0))-numpy.array([0.25, 1.25, 2.25])) > precision:
  raise ValueError("Résultat du test erroné")
else:
  print "    Test correct, erreur maximale inférieure à %s"%precision
  print

