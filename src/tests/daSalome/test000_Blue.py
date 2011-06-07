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

study_config = {}
study_config["Name"] = "test000_Blue"
study_config["Algorithm"] = "Blue"

Background_config = {}
Background_config["Data"] = "0,1,2"
Background_config["Type"] = "Vector"
Background_config["From"] = "String"
study_config["Background"] = Background_config

BackgroundError_config = {}
BackgroundError_config["Data"] = "1 0 0;0 1 0;0 0 1"
BackgroundError_config["Type"] = "Matrix"
BackgroundError_config["From"] = "String"
study_config["BackgroundError"] = BackgroundError_config

Observation_config = {}
Observation_config["Data"] = "0.5,1.5,2.5"
Observation_config["Type"] = "Vector"
Observation_config["From"] = "String"
study_config["Observation"] = Observation_config

ObservationError_config = {}
ObservationError_config["Data"] = "1 0 0;0 1 0;0 0 1"
ObservationError_config["Type"] = "Matrix"
ObservationError_config["From"] = "String"
study_config["ObservationError"] = ObservationError_config

ObservationOperator_config = {}
ObservationOperator_config["Data"] = "1 0 0;0 1 0;0 0 1"
ObservationOperator_config["Type"] = "Matrix"
ObservationOperator_config["From"] = "String"
study_config["ObservationOperator"] = ObservationOperator_config

Analysis_config = {}
Analysis_config["Data"] = """
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
"""
Analysis_config["From"] = "String"
study_config["Analysis"] = Analysis_config
