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

.. _section_ref_sampling_requirements:

Conditions requises pour décrire un échantillonnage d'états
-----------------------------------------------------------

.. index:: single: SamplingTest
.. index:: single: Echantillonnage d'états
.. index:: single: Echantillonnage

De manière générale, il est utile de disposer d'un échantillonnage des états
lorsque l'on s'intéresse à des analyses qui bénéficient de la connaissance d'un
ensemble de simulations ou d'un ensemble de mesures similaires, mais chacune
obtenue pour un état différent.

C'est le cas pour la définition explicite des états simulables des
:ref:`section_ref_algorithm_SamplingTest`,
:ref:`section_ref_algorithm_EnsembleOfSimulationGenerationTask` et
:ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`.

L'ensemble de ces états peut être décrit de manière explicite ou implicite pour
en faciliter l'inventaire. On indique ci-dessous les descriptions possibles, et
on les fait suivre d'exemples très simples pour montrer les types de
répartitions obtenues dans l'espace des états.

Description explicite ou implicite de la collection d'échantillonnage des états
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

La collection d'échantillonnage des états peut être décrite à l'aide de
mots-clés dédiés dans le jeu de commandes d'un algorithme qui le nécessite.

L'échantillonnage des états :math:`\mathbf{x}` peut être fourni explicitement
ou sous la forme d'hypercubes, explicites ou échantillonnés selon des
distributions courantes, ou à l'aide d'un échantillonnage par hypercube latin
(LHS) ou par séquence de Sobol. Selon la méthode, l'échantillon sera inclus
dans le domaine décrit par ses bornes ou sera descriptif du domaine non borné
des variables d'état.

Ces mots-clés possibles sont les suivants :

.. include:: snippets/SampleAsExplicitHyperCube.rst

.. include:: snippets/SampleAsIndependantRandomVariables.rst

.. include:: snippets/SampleAsMinMaxLatinHyperCube.rst

.. include:: snippets/SampleAsMinMaxSobolSequence.rst

.. include:: snippets/SampleAsMinMaxStepHyperCube.rst

.. include:: snippets/SampleAsnUplet.rst

Attention à la taille de l'hypercube (et donc au nombre de calculs) qu'il est
possible d'atteindre, elle peut rapidement devenir importante.

Exemples très simples de répartitions dans l'espace des états
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour illustrer les commandes, on propose ici des répartitions simples obtenues
dans un espace d'état à 2 dimensions (pour être représentable), et les
commandes qui permettent de les obtenir. On choisit arbitrairement de
positionner 25 états dans chaque cas. Dans la majeure partie des commandes,
comme on décrit les états séparément selon chaque coordonnée, on demande donc 5
valeurs de coordonnées par axe.

Les trois premiers mots-clés illustrent la même répartition car ce sont
simplement des manières différentes de la décrire.

Répartition explicite d'états par le mot-clé "*SampleAsnUplet*"
...............................................................

La commande de génération explicite d'échantillons par "*SampleAsnUplet*" est
la suivante :

.. code-block:: python

    [...]
    "SampleAsnUplet":[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
                      [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
                      [2, 0], [2, 1], [2, 2], [2, 3], [2, 4],
                      [3, 0], [3, 1], [3, 2], [3, 3], [3, 4],
                      [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]
    [...]

La répartition des états ainsi décrite correspond à l'illustration  :

  .. image:: images/sampling_01_SampleAsnUplet.png
    :align: center

Répartition implicite d'états par le mot-clé "*SampleAsExplicitHyperCube*"
..........................................................................

La commande de génération implicite d'échantillons par
"*SampleAsExplicitHyperCube*" est la suivante :

.. code-block:: python

    [...]
    "SampleAsExplicitHyperCube":[[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
    # ou
    "SampleAsExplicitHyperCube":[range(0, 5), range(0, 5)]
    [...]

La répartition des états ainsi décrite correspond à l'illustration :

  .. image:: images/sampling_02_SampleAsExplicitHyperCube.png
    :align: center

Répartition implicite d'états par le mot-clé "*SampleAsMinMaxStepHyperCube*"
............................................................................

La commande de génération implicite d'échantillons par
"*SampleAsMinMaxStepHyperCube*" est la suivante :

.. code-block:: python

    [...]
    "SampleAsMinMaxStepHyperCube":[[0, 4, 1], [0, 4, 1]]
    [...]

La répartition des états ainsi décrite correspond à l'illustration :

  .. image:: images/sampling_03_SampleAsMinMaxStepHyperCube.png
    :align: center

Répartition implicite d'états par le mot-clé "*SampleAsMinMaxLatinHyperCube*"
.............................................................................

La commande de génération implicite d'échantillons par
"*SampleAsMinMaxLatinHyperCube*" est la suivante :

.. code-block:: python

    [...]
    "SampleAsMinMaxLatinHyperCube":[[0, 4], [0, 4], [2, 25]]
    [...]

La répartition des états ainsi décrite correspond à l'illustration :

  .. image:: images/sampling_04_SampleAsMinMaxLatinHyperCube.png
    :align: center

Répartition implicite d'états par le mot-clé "*SampleAsMinMaxSobolSequence*"
............................................................................

La commande de génération implicite d'échantillons par
"*SampleAsMinMaxSobolSequence*" est la suivante :

.. code-block:: python

    [...]
    "SampleAsMinMaxSobolSequence":[[0, 4, 1], [0, 4, 1], [2, 25]]
    [...]

La répartition des états (il y en a ici 32 par principe de construction de la
séquence de Sobol) ainsi décrite correspond à l'illustration :

  .. image:: images/sampling_05_SampleAsMinMaxSobolSequence.png
    :align: center

Répartition implicite d'états par le mot-clé "*SampleAsIndependantRandomVariables*" avec loi normale
....................................................................................................

La commande de génération implicite d'échantillons par
"*SampleAsIndependantRandomVariables*" est la suivante, en utilisant une loi
normale (0,1) de répartition par coordonnée :

.. code-block:: python

    [...]
    "SampleAsIndependantRandomVariables":[['normal', [0, 1], 5], ['normal', [0, 1], 5]]
    [...]

La répartition des états ainsi décrite correspond à l'illustration :

  .. image:: images/sampling_06_SampleAsIndependantRandomVariables_normal.png
    :align: center

Répartition implicite d'états par le mot-clé "*SampleAsIndependantRandomVariables*" avec loi uniforme
.....................................................................................................

La commande de génération implicite d'échantillons par
"*SampleAsIndependantRandomVariables*" est la suivante, en utilisant une loi
uniforme entre 0 et 5 de répartition par coordonnée :

.. code-block:: python

    [...]
    "SampleAsIndependantRandomVariables":[['uniform', [0, 5], 5], ['uniform', [0, 5], 5]]
    [...]

La répartition des états ainsi décrite correspond à l'illustration :

  .. image:: images/sampling_07_SampleAsIndependantRandomVariables_uniform.png
    :align: center

Répartition implicite par le mot-clé "*SampleAsIndependantRandomVariables*" avec loi de Weibull
...............................................................................................

La commande de génération implicite d'échantillons par
"*SampleAsIndependantRandomVariables*" est la suivante, en utilisant une loi de
Weibull à un paramètre de valeur 5 de répartition par coordonnée :

.. code-block:: python

    [...]
    "SampleAsIndependantRandomVariables":[['weibull', [5], 5], ['weibull', [5], 5]]
    [...]

La répartition des états ainsi décrite correspond à l'illustration :

  .. image:: images/sampling_08_SampleAsIndependantRandomVariables_weibull.png
    :align: center
