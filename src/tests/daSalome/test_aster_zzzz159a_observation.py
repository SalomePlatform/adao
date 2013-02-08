#-*-coding:iso-8859-1-*-
# Copyright (C) 2010-2013 EDF R&D
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
debug = init_data["debug"]
experience = init_data["experience"]

nbmesures = 11 # De 0 à 1 par pas de 0.1
instants = numpy.array([0.1*i for i in range(nbmesures)])
yo = []
for reponse in experience:
    for t,v in list(reponse):
        if min(abs(t - instants)) < 1.e-8:
            yo.append(v)
            # print t,'===>',v
if debug:
    print "Observations = ",yo
    print

Observation = yo
