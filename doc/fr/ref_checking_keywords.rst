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

.. index:: single: CHECKING_STUDY
.. _section_ref_checking_keywords:

Liste des commandes et mots-clés pour un cas de vérification
------------------------------------------------------------

.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Debug
.. index:: single: Observer
.. index:: single: Observers
.. index:: single: Observer Template
.. index:: single: StudyName
.. index:: single: StudyRepertory
.. index:: single: UserDataInit

Ce jeu de commandes est lié à la description d'un cas de vérification, qui est
une procédure pour vérifier les propriétés d'une information requise, utilisée
ailleurs par un cas de calcul. Les termes sont classés par ordre alphabétique,
sauf le premier, qui décrit le choix entre le calcul ou la vérification.

Les différentes commandes sont les suivantes:

  **CHECKING_STUDY**
    *Commande obligatoire*. C'est la commande générale qui décrit le cas de
    vérification. Elle contient hiérarchiquement toutes les autres commandes.

  AlgorithmParameters
    *Commande obligatoire*. Elle définit l'algorithme de test choisi par le
    mot-clé "*Algorithm*", et ses éventuels paramètres optionnels. Les choix
    d'algorithmes sont disponibles à travers l'interface graphique. Il existe
    par exemple le "FunctionTest", le "GradientTest"... Chaque algorithme est
    défini, plus loin, par une sous-section spécifique. De manière facultative,
    la commande permet aussi d'ajouter des paramètres pour contrôler
    l'algorithme. Leurs valeurs sont définies explicitement ou dans un objet de
    type "*Dict*". On se reportera à la
    :ref:`section_ref_options_Algorithm_Parameters` pour l'usage détaillé de
    cette partie de la commande.

  .. include:: snippets/CheckingPoint.rst

  .. include:: snippets/BackgroundError.rst

  Debug
    *Commande optionnelle*. Elle définit le niveau de sorties et d'informations
    intermédiaires de débogage. Les choix sont limités entre 0 (pour False) et
    1 (pour True).

  .. include:: snippets/Observation.rst

  .. include:: snippets/ObservationError.rst

  .. include:: snippets/ObservationOperator.rst

  Observers
    *Commande optionnelle*. Elle permet de définir des observateurs internes,
    qui sont des fonctions liées à une variable particulière, qui sont exécutées
    chaque fois que cette variable est modifiée. C'est une manière pratique de
    suivre des variables d'intérêt durant le processus d'assimilation de données
    ou d'optimisation, en l'affichant ou en la traçant, etc. Des exemples
    courants (squelettes) sont fournis pour aider l'utilisateur ou pour
    faciliter l'élaboration d'un cas.

  StudyName
    *Commande obligatoire*. C'est une chaîne de caractères quelconque pour
    décrire l'étude ADAO par un nom ou une déclaration.

  StudyRepertory
    *Commande optionnelle*. S'il existe, ce répertoire est utilisé comme base
    pour les calculs, et il est utilisé pour trouver les fichiers de script,
    donnés par nom sans répertoire, qui peuvent être utilisés pour définir
    certaines variables.

  UserDataInit
    *Commande optionnelle*. Elle permet d'initialiser certains paramètres ou
    certaines données automatiquement avant le traitement de données d'entrée
    pour l'assimilation de données ou l'optimisation. Pour cela, elle indique un
    nom de fichier de script à exécuter avant d'entrer dans l'initialisation des
    variables choisies.
