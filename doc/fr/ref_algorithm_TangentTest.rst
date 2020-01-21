..
   Copyright (C) 2008-2020 EDF R&D

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

.. index:: single: TangentTest
.. _section_ref_algorithm_TangentTest:

Algorithme de vérification "*TangentTest*"
------------------------------------------

.. ------------------------------------ ..
.. include:: snippets/Header2Algo01.rst

Cet algorithme permet de vérifier la qualité de l'opérateur tangent, en
calculant un résidu dont les propriétés théoriques sont connues.

On observe le résidu suivant, provenant du rapport d'incréments utilisant
l'opérateur linéaire tangent :

.. math:: R(\alpha) = \frac{|| F(\mathbf{x}+\alpha*\mathbf{dx}) - F(\mathbf{x}) ||}{|| \alpha * TangentF_x * \mathbf{dx} ||}

qui doit rester stable en :math:`1+O(\alpha)` jusqu'à ce que l'on atteigne la
précision du calcul.

Lorsque :math:`|R-1|/\alpha` est inférieur ou égal à une valeur stable lorsque
:math:`\alpha` varie, le tangent est valide, jusqu'à ce que l'on atteigne la
précision du calcul.

Si :math:`|R-1|/\alpha` est très faible, le code de calcul :math:`F` est
vraisemblablement linéaire ou quasi-linéaire (ce que l'on peut vérifier par
l':ref:`section_ref_algorithm_LinearityTest`), et le tangent est valide jusqu'à
ce que l'on atteigne la précision du calcul.

On prend :math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.

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
  disponibles à la fin de l'algorithme, si elles sont initialement demandées par
  l'utilisateur. Cela implique potentiellement des calculs ou du stockage
  coûteux. La valeur par défaut est une liste vide, aucune de ces variables
  n'étant calculée et stockée par défaut sauf les variables inconditionnelles.
  Les noms possibles sont dans la liste suivante : [
  "CurrentState",
  "Residu",
  "SimulatedObservationAtCurrentState",
  ].

  Exemple :
  ``{"StoreSupplementaryCalculations":["BMA", "CurrentState"]}``

.. ------------------------------------ ..
.. include:: snippets/Header2Algo04.rst

.. include:: snippets/Residu.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo05.rst

.. include:: snippets/CurrentState.rst

.. include:: snippets/Residu.rst

.. include:: snippets/SimulatedObservationAtCurrentState.rst

.. ------------------------------------ ..
.. include:: snippets/Header2Algo06.rst

- :ref:`section_ref_algorithm_FunctionTest`
- :ref:`section_ref_algorithm_LinearityTest`
- :ref:`section_ref_algorithm_AdjointTest`
- :ref:`section_ref_algorithm_GradientTest`
- :ref:`section_ref_algorithm_LocalSensitivityTest`
