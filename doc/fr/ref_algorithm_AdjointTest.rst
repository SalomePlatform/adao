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

Description
+++++++++++

Cet algorithme permet de vérifier la qualité de l'opérateur adjoint, en
calculant un résidu dont les propriétés théoriques sont connues.

On observe le résidu suivant, qui est la différence de deux produits scalaires :

.. math:: R(\alpha) = | < TangentF_x(\mathbf{dx}) , \mathbf{y} > - < \mathbf{dx} , AdjointF_x(\mathbf{y}) > |

qui doit rester constamment égal à zéro à la précision du calcul. On prend
:math:`\mathbf{dx}_0=Normal(0,\mathbf{x})` et
:math:`\mathbf{dx}=\alpha*\mathbf{dx}_0`. :math:`F` est le code de calcul.
:math:`\mathbf{y}` doit être dans l'image de :math:`F`. S'il n'est pas donné, on
prend :math:`\mathbf{y} = F(\mathbf{x})`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  .. include:: snippets/CheckingPoint.rst

  .. include:: snippets/ObservationOperator.rst

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_checking_keywords`. De plus, les
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

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
    possibles sont dans la liste suivante : ["CurrentState", "Residu",
    "SimulatedObservationAtCurrentState"].

    Exemple :
    ``{"StoreSupplementaryCalculations":["CurrentState"]}``

Informations et variables disponibles à la fin de l'algorithme
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En sortie, après exécution de l'algorithme, on dispose d'informations et de
variables issues du calcul. La description des
:ref:`section_ref_output_variables` indique la manière de les obtenir par la
méthode nommée ``get`` de la variable "*ADD*" du post-processing. Les variables
d'entrée, mises à disposition de l'utilisateur en sortie pour faciliter
l'écriture des procédures de post-processing, sont décrites dans
l':ref:`subsection_r_o_v_Inventaire`.

Les sorties non conditionnelles de l'algorithme sont les suivantes:

  .. include:: snippets/Residu.rst

Les sorties conditionnelles de l'algorithme sont les suivantes:

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/SimulatedObservationAtCurrentState.rst

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`
  - :ref:`section_ref_algorithm_LinearityTest`
  - :ref:`section_ref_algorithm_TangentTest`
  - :ref:`section_ref_algorithm_GradientTest`
