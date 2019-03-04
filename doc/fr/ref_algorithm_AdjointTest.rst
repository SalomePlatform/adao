..
   Copyright (C) 2008-2019 EDF R&D

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

.. index:: single: AdjointTest
.. _section_ref_algorithm_AdjointTest:

Algorithme de vérification "*AdjointTest*"
------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de vérifier la qualité de l'opérateur adjoint, en
calculant un résidu dont les propriétés théoriques sont connues.

On observe le résidu suivant, qui est la différence de deux produits scalaires :

.. math:: R(\alpha) = | < TangentF_x(\mathbf{dx}) , \mathbf{y} > - < \mathbf{dx} , AdjointF_x(\mathbf{y}) > |

qui doit rester constamment égal à zéro à la précision du calcul. On prend
:math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.
:math:`\mathbf{y}` doit être dans l'image de :math:`F`. S'il n'est pas donné,
on prend :math:`\mathbf{y} = F(\mathbf{x})`.

.. ------------------------------------ ..
.. include:: snippets/Header2Algo02.rst

.. include:: snippets/CheckingPoint.rst

.. include:: snippets/ObservationOperator.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo03Chck.rst

.. include:: snippets/AmplitudeOfInitialDirection.rst

.. include:: snippets/EpsilonMinimumExponent.rst

.. include:: snippets/InitialDirection.rst

.. include:: snippets/SetSeed.rst

StoreSupplementaryCalculations
  .. index:: single: StoreSupplementaryCalculations

  Cette liste indique les noms des variables supplémentaires qui peuvent être
  disponibles à la fin de l'algorithme. Cela implique potentiellement des
  calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
  aucune de ces variables n'étant calculée et stockée par défaut. Les noms
  possibles sont dans la liste suivante : [
  "CurrentState",
  "Residu",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["CurrentState"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Residu.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LinearityTest`
- :ref:`section_ref_algorithm_TangentTest`
- :ref:`section_ref_algorithm_GradientTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`
