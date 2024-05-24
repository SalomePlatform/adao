..
   Copyright (C) 2008-2024 EDF R&D

   This file is part of SALOME ADAO module.

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with this library; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

   See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com

   Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

.. index:: single: InterpolationByReducedModelTest
.. _section_ref_algorithm_InterpolationByReducedModelTest:

Algorithme de vérification "*InterpolationByReducedModelTest*"
--------------------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet d'analyser de manière simple la qualité de
l'interpolation empirique des états obtenue par une base réduite, en utilisant
des mesures en des points précis.

Les résultats affichés par défaut sont des statistiques simples liées aux
erreurs normalisées de l'interpolation avec une base réduite. Le test utilise
une base réduite et un ensemble de positions de mesures optimales, et utilise
des pseudo-mesures provenant de chaque état complet ("*snapshot*") inclus dans
l'ensemble de test donné.

Attention : pour être cohérent, ce test doit utiliser la même norme
mathématique que celle utilisée pour construire la base réduite. La norme étant
choisie par l'utilisateur lors de la définition du test, il faut vérifier la
norme de construction de la base réduite.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo12.rst

.. include:: snippets/FeaturePropDerivativeFree.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/EnsembleOfSnapshots.rst

.. include:: snippets/MeasurementLocations.rst

.. include:: snippets/ReducedBasis.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/ErrorNorm.rst

.. include:: snippets/NumberOfPrintedDigits.rst

.. include:: snippets/ShowElementarySummary.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/NoUnconditionalOutput.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/NoConditionalOutput.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_InterpolationByReducedModelTest_examples:

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_InterpolationByReducedModelTask`
- :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`
- :ref:`section_ref_algorithm_ReducedModelingTest`
