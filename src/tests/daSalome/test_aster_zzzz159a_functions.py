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
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

import numpy
import sys

sys.path.insert(0, init_data['SOURCES_ROOT'])
import test_aster_zzzz159a_aster_functions as Code_Aster

# Configuration du module
Code_Aster.debug = init_data["debug"]
Code_Aster.ASTER_ROOT = init_data["ASTER_ROOT"]
Code_Aster.SOURCES_ROOT = init_data['SOURCES_ROOT']
Code_Aster.export = init_data["export"]
Code_Aster.calcul = init_data["calcul"]
Code_Aster.parametres = init_data["parametres"]
Code_Aster.python_version = init_data["python_version"]

print computation
method = ""
for param in computation["specificParameters"]:
  if param["name"] == "method":
    method = param["value"]

# Extraction des données et remise en forme (normalement à faire
# dans le code
# On sait qu'on a trois variables
input_data = []
for i in range(3):
  input_data.append(computation["inputValues"][0][0][i][0])

if method == "Adjoint":
  input_data = (input_data, [])
  for i in range(22):
    if i < 11:
      input_data[1].append(computation["inputValues"][0][0][3][i])
    else:
      input_data[1].append(computation["inputValues"][0][0][4][i-11])

result = {}
result["specificOutputInfos"] = []
result["returnCode"] = 0
result["errorMessage"] = ""

outputValues = [[[[]]]]
if method == "Direct":
  output_data = Code_Aster.Calcul_Aster_Ponctuel(input_data)
  outputValues[0][0] = [[],[]]
  for i in range(22):
    if i < 11:
      outputValues[0][0][0].append(output_data[i])
    else:
      outputValues[0][0][1].append(output_data[i])

if method == "Tangent":
  output_data = Code_Aster.Calcul_Aster_Ponctuel(input_data)
  outputValues[0][0] = [[],[]]
  for i in range(22):
    if i < 11:
      outputValues[0][0][0].append(output_data[i])
    else:
      outputValues[0][0][1].append(output_data[i])

if method == "Adjoint":
  output_data = Code_Aster.Calcul_Aster_Adjoint(input_data)
  outputValues[0][0] = [[],[],[]]
  outputValues[0][0][0].append(output_data[0])
  outputValues[0][0][1].append(output_data[1])
  outputValues[0][0][2].append(output_data[2])

result["outputValues"] = outputValues

print "Computation end"
