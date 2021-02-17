..
   Copyright (C) 2008-2021 EDF R&D

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

.. index:: single: AlgorithmParameters
.. index:: single: Parameters
.. index:: single: Defaults
.. index:: single: setAlgorithmParameters
.. _section_ref_options_Algorithm_Parameters:

Description des options d'un algorithme par "*AlgorithmParameters*"
-------------------------------------------------------------------

Chaque algorithme peut être contrôlé en utilisant des options ou des paramètres
particuliers. Ils sont donnés à travers la commande optionnelle "*Parameters*"
incluse dans la commande obligatoire "*AlgorithmParameters*".

Il y a 3 méthodes pratiques pour l'utilisateur de l'interface graphique EFICAS
d'ADAO (GUI) pour fournir ces options. La méthode est déterminée de la manière
suivante dans l'interface graphique EFICAS d'ADAO :

#. premièrement à l'aide du mot-clé "*Parameters*" dans la commande
   "*AlgorithmParameters*", qui permet de choisir entre "*Defaults*"
   (utilisation de mots-clés explicites pré-remplis par les valeurs par défaut
   des paramètres) et "*Dict*" (utilisation d'un dictionnaire pour renseigner
   les mots-clés nécessaires),
#. puis deuxièmement ou troisièmement, uniquement dans le cas "*Dict*" de
   "*Parameters*", par le mot-clé "*FROM*" inclus qui permet de choisir entre
   une entrée par chaîne de caractères ou une entrée par fichier de script
   Python.

Ces deux dernières options sont celles que l'on peut aussi utiliser dans
l'interface textuelle d'ADAO (TUI), par les mot-clés "*Parameters*" et
"*Script*" dans la commande correspondante "*AlgorithmParameters*" (voir la
partie :ref:`section_tui` pour une description détaillée).

Si une option ou un paramètre est spécifié par l'utilisateur pour un algorithme
qui ne la supporte pas, cette option est simplement ignorée (laissée
inutilisée) et ne bloque pas le traitement. La signification des acronymes ou
des noms particuliers peut être trouvée dans l'index ou dans le
:ref:`section_glossary`.

Première méthode : utiliser les mots-clés explicites pré-remplis
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs des paramètres par les mots-clés explicites pré-remplis,
directement dans l'interface graphique, l'utilisateur sélectionne le type
"*Defaults*" dans le mot-clé "*Parameters*", puis les mots-clés dans la liste
prévue "*Parameters[Algo]*" qui apparaît, associée à l'algorithme choisi, comme
montré dans la figure qui suit :

  .. adao_algopar_defaults:
  .. image:: images/adao_algopar_defaults.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser les mots-clés explicites pré-remplis pour les paramètres algorithmiques**

Chaque paramètre est optionnel, et il présente sa valeur par défaut lorsqu'il
est sélectionné par l'utilisateur. On peut alors modifier sa valeur, ou la
renseigner dans le cas de listes par exemple.

C'est la manière recommandée pour modifier uniquement une partie des paramètres
algorithmiques de manière sûre. Cette méthode ne permet de définir que les
paramètres autorisés pour un algorithme donné, et les valeurs définies ne sont
pas conservées si l'utilisateur change d'algorithme.

Cette méthode n'est naturellement pas utilisable en interface TUI.

Seconde méthode : utiliser une chaîne de caractères dans l'interface graphique
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs des paramètres par une chaîne de caractères, directement
dans l'interface graphique, l'utilisateur sélectionne le type "*Dict*" dans le
mot-clé "*Parameters*", puis le type "*String*" dans le mot-clé "*FROM*" de la
commande "*Dict*" qui apparaît, comme montré dans la figure qui suit :

  .. adao_algopar_string:
  .. image:: images/adao_algopar_string.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser une chaîne de caractères pour les paramètres algorithmiques**

Dans le champs de saisie, il faut utiliser des guillemets simples pour une
définition standard de dictionnaire, comme par exemple::

    '{"MaximumNumberOfSteps":25,"SetSeed":1000}'

C'est la manière recommandée pour définir des paramètres algorithmiques. Cette
méthode permet en particulier de conserver des options ou des paramètres pour
d'autres algorithmes que celui que l'on utilise au moment présent. Cela
facilite le changement d'algorithme ou la conservation de valeurs par défaut
différentes des défauts standards.

Dans l'interface textuelle TUI, le dictionnaire peut être simplement donné
comme argument du mot-clé "*Parameters*".

Troisième méthode : utiliser un fichier de script Python externe
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour donner les valeurs des paramètres par un fichier de script Python externe,
l'utilisateur sélectionne dans l'interface graphique le type "*Dict*" dans le
mot-clé "*Parameters*", puis le type "*Script*" dans le mot-clé "*FROM*" de la
commande "*Dict*" qui apparaît, comme montré dans la figure qui suit :

  .. :adao_algopar_script
  .. image:: images/adao_algopar_script.png
    :align: center
    :width: 100%
  .. centered::
    **Utiliser un fichier externe pour les paramètres algorithmiques**

Ce fichier script Python externe doit définir alors une variable au nom imposé
"*AlgorithmParameters*", à la manière de l'exemple qui suit::

    AlgorithmParameters = {
        "MaximumNumberOfSteps" : 25,
        "StoreSupplementaryCalculations" : ["APosterioriCovariance","OMA"],
        }

Le fichier peut aussi contenir d'autres commandes Python. Cette méthode permet
aussi, comme la précédente, de conserver des options ou des paramètres pour
d'autres algorithmes que celui que l'on utilise.

Dans l'interface textuelle TUI, le fichier peut être donné comme argument du
mot-clé "*Script*".
