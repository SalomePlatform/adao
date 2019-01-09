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

.. index:: single: EnsembleBlue
.. _section_ref_algorithm_EnsembleBlue:

Algorithme de calcul "*EnsembleBlue*"
-------------------------------------

Description
+++++++++++

Cet algorithme réalise une estimation de type BLUE (Best Linear Unbiased
Estimator, qui est ici un estimateur d'Aitken) de l'état d'un système, par
méthode d'ensemble. Pour fonctionner, il faut fournir un ensemble d'ébauches,
dont le nombre déterminera la taille de l'ensemble pour l'estimation.

Il est théoriquement réservé aux cas d'opérateurs d'observation linéaires, mais
doit fonctionner aussi dans les cas "faiblement" non-linéaire. On peut vérifier
la linéarité de l'opérateur d'observation à l'aide de
l':ref:`section_ref_algorithm_LinearityTest`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  .. include:: snippets/Background.rst

  .. include:: snippets/BackgroundError.rst

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

  .. include:: snippets/ObservationOperator.rst

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_assimilation_keywords`. De plus, les
paramètres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  .. include:: snippets/SetSeed.rst

  StoreSupplementaryCalculations
    .. index:: single: StoreSupplementaryCalculations

    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["CurrentState", "Innovation",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"].

    Exemple :
    ``{"StoreSupplementaryCalculations":["CurrentState", "Innovation"]}``

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

  .. include:: snippets/Analysis.rst

  .. include:: snippets/CurrentState.rst

  .. include:: snippets/Innovation.rst

Voir aussi
++++++++++

Références vers d'autres sections :
  - :ref:`section_ref_algorithm_Blue`
