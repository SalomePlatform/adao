..
   Copyright (C) 2008-2022 EDF R&D

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

.. _section_ref_observations_requirements:

Conditions requises pour la description d'observations ou de mesures expérimentales
-----------------------------------------------------------------------------------

.. index:: single: setObservation
.. index:: single: setObservationError

L'ensemble des mesures du système physique que l'on considère sont appelées
"*des observations*", ou même simplement "*une observation*". Comme cela a déjà
été mentionné dans :ref:`section_theory`, cette observation est notée de
manière la plus générique par :

.. math:: \mathbf{y}^o

Elle peut dépendre en général de l'espace et du temps, voire de variables
paramétriques, et cela de manière plus ou moins complexe. On particularise
usuellement la dépendance en temps en considérant que, à chaque instant, la
quantité :math:`\mathbf{y}^o` est un vecteur de
:math:`\mbox{I\hspace{-.15em}R}^d` (avec la dimension :math:`d` de l'espace
pouvant éventuellement varier en temps). Autrement dit, **une observation est
une série (temporelle) de mesures (variées)**. On parlera donc de manière
équivalente d'une observation (vectorielle), d'une série ou d'un vecteur
d'observations, et d'un ensemble d'observations. Dans sa plus grande
généralité, l'aspect séquentiel de la série d'observations est relatif
conjointement à l'espace, et/ou au temps, et/ou à une dépendance paramétrique.

On peut classer les manières de représenter l'observation en fonction des
usages que l'on en a ensuite et des liens avec les méthodes algorithmiques. Le
classement que l'on propose est le suivant, dont chaque catégorie est détaillée
ensuite :

#. `Utilisation d'une unique observation spatiale`_
#. `Utilisation d'une série temporelle d'observations spatiales`_
#. `Utilisation d'une unique observation spatio-temporelle`_
#. `Utilisation d'une série paramétrée d'observations spatiales`_

Les représentations numériques des observations utilisent toutes les
possibilités décrites dans la :ref:`section_ref_entry_types`. On spécialise ici
leurs usages pour indiquer différentes manières possible d'écrire cette
information.

Utilisation d'une unique observation spatiale
+++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Vector
.. index:: single: DataFile

Cela fait référence à l'usage d'une série vectorielle dépendante uniquement de
l'espace. Cette observation est de plus utilisée en une seule fois,
c'est-à-dire en étant entièrement connue au début de l'analyse algorithmique.
Cela peut par exemple être un champ spatial de mesures, ou de plusieurs champs
physiquement homogènes ou pas.

- La représentation mathématique est :math:`\mathbf{y}^o\,\in\,\mbox{I\hspace{-.15em}R}^d`.

- La représentation numérique canonique est **un vecteur**.

- La représentation numérique dans ADAO se fait avec le mot-clé "*Vector*". La
  totalité de l'information, déclarée dans l'une des représentations suivantes,
  est transformée en un unique vecteur (remarque : listes et tuples sont
  équivalents) :

    - variable "*numpy.array*" : ``numpy.array([1, 2, 3])``
    - variable "*liste*"       : ``[1, 2, 3]``
    - chaîne de caractères     : ``'1 2 3'``
    - chaîne de caractères     : ``'1,2,3'``
    - chaîne de caractères     : ``'1;2;3'``
    - chaîne de caractères     : ``'[1,2,3]'``
    - fichier Python de données, avec variable "*Observation*" dans l'espace de nommage, indiqué par le mot-clé "*Script*" avec la condition ``Vector=True``
    - fichier texte de données (TXT, CSV, TSV, DAT), avec pointeur de variable par nom en colonne ou en ligne, indiqué par le mot-clé "*DataFile*" avec la condition ``Vector=True``
    - fichier binaire de données (NPY, NPZ), avec pointeur de variable par nom, indiqué par le mot-clé "*DataFile*" avec la condition ``Vector=True``

- Exemples de déclaration en interface TUI :

    - ``case.setObservation( Vector = [1, 2, 3] )``
    - ``case.setObservation( Vector = numpy.array([1, 2, 3]) )``
    - ``case.setObservation( Vector = '1 2 3' )``
    - ``case.setObservation( Vector=True, Script = 'script.py' )```
    - ``case.setObservation( Vector=True, DataFile = 'data.csv' )```
    - ``case.setObservation( Vector=True, DataFile = 'data.npy' )```

Remarque d'utilisation : dans une étude donnée, seul le dernier enregistrement
(que ce soit un vecteur unique ou une série de vecteurs) est utilisable, car un
seul concept d'observation existe par étude ADAO.

Utilisation d'une série temporelle d'observations spatiales
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: VectorSerie
.. index:: single: DataFile

Cela fait référence une série ordonnée vectorielle d'observations, dépendantes
de l'espace et du temps. A un instant donné, on suppose que l'on ne connaît que
les observations des instants courant et précédents. Les observations
successives en temps sont indexées par :math:`n`, leur instant d'existence ou
de référence. Cela peut par exemple être un champs spatial de mesures,
physiquement homogènes ou pas, dont on considère un historique.

- La représentation mathématique est :math:`\forall\,n\in\{0...N\},\,\mathbf{y}^o_n\,\in\mbox{I\hspace{-.15em}R}^d`.

- La représentation numérique canonique est **une série ordonnée de vecteurs**.

- La représentation numérique dans ADAO se fait avec le mot-clé
  "*VectorSerie*". L'indexation courante de l'information est utilisée pour
  représenter l'index temporel lors de la déclaration dans l'une des
  représentations suivantes, et l'information est transformée en une série
  ordonnée de vecteurs (remarque : listes et tuples sont équivalents) :

    - "*liste*" de "*numpy.array*"      : ``[numpy.array([1,2,3]), numpy.array([1,2,3])]``
    - "*numpy.array*" de "*liste*"      : ``numpy.array([[1,2,3], [1,2,3]])``
    - "*liste*" de "*liste*"            : ``[[1,2,3], [1,2,3]]``
    - "*liste*" de chaîne de caractères : ``['1 2 3', '1 2 3']``
    - "*liste*" de chaîne de caractères : ``['1;2;3', '1;2;3']``
    - "*liste*" de chaîne de caractères : ``['[1,2,3]', '[1,2,3]']``
    - chaîne de "*liste*"               : ``'[[1,2,3], [1,2,3]]'``
    - chaîne de "*liste*"               : ``'1 2 3 ; 1 2 3'``
    - fichier Python de données, avec variable "*Observation*" dans l'espace de nommage, indiqué par le mot-clé "*Script*" avec la condition ``VectorSerie=True``
    - fichier texte de données (TXT, CSV, TSV, DAT), avec pointeur de variable par nom en colonne ou en ligne, indiqué par le mot-clé "*DataFile*" avec la condition ``VectorSerie=True``
    - fichier binaire de données (NPY, NPZ), avec pointeur de variable par nom, indiqué par le mot-clé "*DataFile*" avec la condition ``VectorSerie=True``

- Exemples de déclaration en interface TUI :

    - ``case.setObservation( VectorSerie = [[1,2,3], [1,2,3]] )``
    - ``case.setObservation( VectorSerie = [numpy.array([1,2,3]), numpy.array([1,2,3])] )``
    - ``case.setObservation( VectorSerie =  ['1 2 3', '1 2 3'] )``
    - ``case.setObservation( VectorSerie =  '[[1,2,3], [1,2,3]]' )``
    - ``case.setObservation( VectorSerie =  '1 2 3 ; 1 2 3' )``
    - ``case.setObservation( VectorSerie=True, Script = 'script.py' )```
    - ``case.setObservation( VectorSerie=True, DataFile = 'data.csv' )```
    - ``case.setObservation( VectorSerie=True, DataFile = 'data.npy' )```

Remarque d'utilisation : dans une étude donnée, seul le dernier enregistrement
(que ce soit un vecteur unique ou une série de vecteurs) est utilisable, car un
seul concept d'observation existe par étude ADAO.

Utilisation d'une unique observation spatio-temporelle
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Cette unique observation spatio-temporelle est similaire à la précédente dans
sa représentation de série vectorielle, mais elle impose qu'elle doit être
utilisée en une seule fois, c'est-à-dire en étant entièrement connue au début
de l'analyse algorithmique. Elle est donc représentable comme une série
indexée, de la même manière que pour une `Utilisation d'une série temporelle
d'observations spatiales`_.

Utilisation d'une série paramétrée d'observations spatiales
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

On représente cette fois une collection d'observations paramétrées par un
indice ou un paramètre discret. Cette forme est encore similaire à la
précédente. Elle est donc représentable comme une série indexée, de la même
manière que pour une `Utilisation d'une série temporelle d'observations
spatiales`_.

Remarques générales sur les observations
++++++++++++++++++++++++++++++++++++++++

.. warning::

  Lorsque l'assimilation établit explicitement un **processus itératif
  temporel**, comme dans l'assimilation de données d'états, **la première
  observation est non utilisée mais elle doit être présente dans la description
  des données d'un cas ADAO**. Par convention, elle est donc considérée comme
  disponible au même instant que la valeur temporelle d'ébauche, et ne conduit
  pas à une correction à cet instant là. La numérotation des observations
  commençant à 0 par convention, ce n'est donc qu'à partir du numéro 1 que les
  valeurs d'observations sont utilisées dans les algorithmes itératifs
  temporels.

Les observations peuvent être fournies par pas de temps uniques ou par fenêtres
successives pour les algorithmes itératifs. Dans ce cas, on doit fournir à
chaque itération algorithmique relative à une fenêtre temporelle une série
d'observations. Dans la pratique, pour chaque fenêtre, on fournit une série
comme lors d'une `Utilisation d'une série temporelle d'observations
spatiales`_.

Les options d'acquisition d'observations sont plus riches en interface
textuelle TUI, toutes les options n'étant pas obligatoirement disponibles dans
l'interface graphique GUI.

Pour l'entrée de données par fichiers, on se reportera à la description des
possibilités autour du mot-clé "*DataFile*" dans les
:ref:`section_ref_entry_types_info`.
