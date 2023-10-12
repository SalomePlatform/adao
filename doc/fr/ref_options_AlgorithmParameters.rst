..
   Copyright (C) 2008-2023 EDF R&D

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

Il existe plusieurs méthodes pratiques pour fournir ces options, que ce soit en
utilisant l'interface graphique EFICAS d'ADAO (GUI) ou l'interface textuelle
(TUI). La méthode est déterminée de la manière suivante :

#. Soit en interface graphique (GUI), à l'aide du mot-clé "*Parameters*" dans
   la commande "*AlgorithmParameters*", qui permet de choisir entre
   "*Defaults*" (utilisation de mots-clés explicites pré-remplis par les
   valeurs par défaut des paramètres) et "*Dict*" (utilisation d'un
   dictionnaire pour renseigner les mots-clés nécessaires),
#. Soit en interface graphique (GUI), uniquement dans le cas "*Dict*" de
   "*Parameters*", par le mot-clé "*FROM*" inclus qui permet de choisir entre une
   entrée par chaîne de caractères ou une entrée par fichier de script Python.
#. Soit en interface textuelle (TUI), à l'aide du mot-clé "*Parameters*" dans
   la commande "*AlgorithmParameters*", de manière semblable à l'interface
   graphique, en renseignant les mots-clés explicites décrits dans la
   documentation de chaque algorithme.
#. Soit en interface textuelle (TUI), à l'aide du mot-clé "*Parameters*" dans
   la commande "*AlgorithmParameters*", en fournissant un script contenant un
   dictionnaire similaire aux méthodes deux et trois et compatibles avec ces
   entrées en GUI.

Ces deux dernières options sont celles que l'on peut utiliser dans l'interface
textuelle (TUI) de manière similaire et compatible aux deux précédentes basées
sur l'interface graphique (GUI).

Si une option ou un paramètre est spécifié par l'utilisateur pour un algorithme
qui ne la supporte pas, cette option est simplement ignorée (laissée
inutilisée) et ne bloque pas le traitement. La signification des acronymes ou
des noms particuliers peut être trouvée dans l'index ou dans le
:ref:`section_glossary`.

Première méthode (GUI) : utiliser les mots-clés explicites pré-remplis
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

Deuxième méthode (GUI) : utiliser une chaîne de caractères dans l'interface graphique
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

Dans le champ de saisie, il faut utiliser des guillemets simples pour une
définition standard de dictionnaire, comme par exemple::

    '{"MaximumNumberOfIterations":25,"SetSeed":1000}'

C'est la manière recommandée pour définir des paramètres algorithmiques. Cette
méthode permet en particulier de conserver des options ou des paramètres pour
d'autres algorithmes que celui que l'on utilise au moment présent. Cela
facilite le changement d'algorithme ou la conservation de valeurs par défaut
différentes des défauts standards.

Troisième méthode (GUI) : utiliser un fichier externe de script Python
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

Ce fichier script Python externe, nommé par exemple ici ``myParameters.py``,
doit définir une variable de type dictionnaire au nom imposé "*Parameters*" ou
"*AlgorithmParameters*", à la manière de l'exemple qui suit :

.. code-block:: python
    :caption: myParameters.py : fichier de paramètres

    AlgorithmParameters = {
        "MaximumNumberOfIterations" : 25,
        "StoreSupplementaryCalculations" : [
            "CurrentState",
            "APosterioriCovariance",
            "OMA",
            ],
        }

De plus, le fichier peut contenir d'autres commandes Python. Cette méthode
permet aussi, comme la précédente, de conserver de manière externe des options
ou des paramètres pour d'autres algorithmes que celui que l'on utilise.

Quatrième méthode (TUI) : utiliser les mots-clés explicites documentés
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Dans l'interface textuelle (TUI), le contrôle des algorithmes se fait en
utilisant la commande "*setAlgorithmParameters*". Elle permet de renseigner ou
de définir les mots-clés décrits dans la documentation de chaque cas de calcul
ADAO. Pour mémoire, ces mots-clés sont les mêmes que ceux qui sont présentés
dans l'interface graphique.

Pour cela, un dictionnaire des couples "mot-clé/valeurs" peut être donné comme
argument du mot-clé "*Parameters*" de la commande. Pour un  cas de calcul TUI
nommé par exemple ``case``, la syntaxe ressemble au code suivant :

.. code-block:: python

    [...]
    case.setAlgorithmParameters(
        Algorithm='3DVAR',
        Parameters={
            "MaximumNumberOfIterations" : 25,
            "StoreSupplementaryCalculations" : [
                "CurrentState",
                "APosterioriCovariance",
                "OMA",
                ],
            },
        )
    [...]

Les valeurs des arguments peuvent évidemment provenir d'évaluations Python ou
de variables précédemment définies, facilitant l'insertion des commandes ADAO
dans le flot du scripting Python d'une étude.

Cinquième méthode (TUI) : utiliser un fichier externe de script Python
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Dans l'interface textuelle (TUI), un fichier peut être donné comme argument de
manière identique et compatible avec la troisième méthode dédiée à l'interface
graphique (GUI). Un fichier externe de script Python nommé ``myParameters.py``,
et contenant par exemple les informations déjà mentionnées pour la troisième
méthode, est le suivant :

.. code-block:: python
    :caption: Version simple de myParameters.py

    AlgorithmParameters = {
        "MaximumNumberOfIterations" : 25,
        "StoreSupplementaryCalculations" : [
            "CurrentState",
            "APosterioriCovariance",
            "OMA",
            ],
        }

Pour un  cas de calcul TUI nommé par exemple ``case``, qui doit lire ce
fichier, la commande en interface textuelle utilise l'argument "*Script*" sous
la forme suivante :

.. code-block:: python

    [...]
    case.setAlgorithmParameters( Algorithm = "3DVAR", Script = "myParameters.py" )
    [...]

De manière alternative et complètement équivalente, pour être conforme à la
définition requise par la commande "*setAlgorithmParameters*", on peut utiliser
dans le script Python externe ``myParameters.py`` la dénomination
"*Parameters*" à la place de "*AlgorithmParameters*" sous la forme :

.. code-block:: python
    :caption: Version simple de myParameters.py

    Parameters = {
        "MaximumNumberOfIterations" : 25,
        "StoreSupplementaryCalculations" : [
            "CurrentState",
            "APosterioriCovariance",
            "OMA",
            ],
        }

La commande de chargement en interface textuelle reste identique. On peut aussi
rajouter dans le script externe le nom de l'algorithme avec son propre mot-clé
"*Algorithm*" (qui dans ce cas est requis, et qui ne peut pas être inclus comme
une option dans "*AlgorithmParameters*") :

.. code-block:: python
    :caption: Version complète de myParameters.py
    :name: myParameters.py

    Algorithm='3DVAR'
    Parameters = {
        "MaximumNumberOfIterations" : 25,
        "StoreSupplementaryCalculations" : [
            "CurrentState",
            "APosterioriCovariance",
            "OMA",
            ],
        }

La commande de chargement en interface textuelle se simplifie alors pour ne
plus comporter qu'un seul argument :

.. code-block:: python

    [...]
    case.setAlgorithmParameters(Script = "myParameters.py")
    [...]

Cette dernière forme est la plus simple pour paramétrer entièrement les entrées
d'algorithmes dans un script Python externe, qui peut ainsi être contrôlé ou
généré par un processus plus vaste de construction d'étude incluant les
commandes ADAO.
