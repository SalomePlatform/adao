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

.. index:: single: LocalSensitivityTest
.. _section_ref_algorithm_LocalSensitivityTest:

Algorithme de vérification "*LocalSensitivityTest*"
---------------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet d'établir la valeur de la Jacobienne de l'opérateur
d'observation :math:`\mathcal{H}` par rapport aux variables d'entrée
:math:`\mathbf{x}`. Cet opérateur intervient dans la relation :

.. math:: \mathbf{y} = \mathcal{H}(\mathbf{x})

(voir :ref:`section_theory` pour de plus amples explications). Cette jacobienne
est l'opérateur linéarisé (ou opérateur tangent) :math:`\mathbf{H}` de
:math:`\mathcal{H}` autour du point de vérification choisi.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/Observation.rst

*Remarque : l'observation n'étant utilisé que pour renforcer la vérification
des dimensions, elle peut donc être fournie comme un vecteur non réaliste de
la bonne taille.
Exemple :* ``numpy.ones(<nombre d'observations>)``

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/SetDebug.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  *Liste de noms*. Cette liste indique les noms des variables supplémentaires,
  qui peuvent être disponibles au cours du déroulement ou à la fin de
  l'algorithme, si elles sont initialement demandées par l'utilisateur. Leur
  disponibilité implique, potentiellement, des calculs ou du stockage coûteux.
  La valeur par défaut est donc une liste vide, aucune de ces variables n'étant
  calculée et stockée par défaut (sauf les variables inconditionnelles). Les
  noms possibles pour les variables supplémentaires sont dans la liste suivante
  (la description détaillée de chaque variable nommée est donnée dans la suite
  de cette documentation par algorithme spécifique, dans la sous-partie
  "*Informations et variables disponibles à la fin de l'algorithme*") : [
  "CurrentState",
  "JacobianMatrixAtCurrentState",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState", "Residu"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/JacobianMatrixAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/JacobianMatrixAtCurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. _section_ref_algorithm_LocalSensitivityTest_examples:

.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_GradientTest`
