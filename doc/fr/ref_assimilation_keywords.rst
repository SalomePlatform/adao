..
   Copyright (C) 2008-2014 EDF R&D

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

.. index:: single: ASSIMILATION_STUDY
.. _section_ref_assimilation_keywords:

Liste des commandes et mots-clés pour un cas d'assimilation de données ou d'optimisation
----------------------------------------------------------------------------------------

.. index:: single: Algorithm
.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: ControlInput
.. index:: single: Debug
.. index:: single: EvolutionError
.. index:: single: EvolutionModel
.. index:: single: InputVariables
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Observer
.. index:: single: Observers
.. index:: single: Observer Template
.. index:: single: OutputVariables
.. index:: single: Study_name
.. index:: single: Study_repertory
.. index:: single: UserDataInit
.. index:: single: UserPostAnalysis
.. index:: single: UserPostAnalysis Template

Ce jeu de commandes est lié à la description d'un cas de calcul, qui est une
procédure d'*Assimilation de Données* ou d'*Optimisation*. Les termes sont
classés par ordre alphabétique, sauf le premier, qui décrit le choix entre le
calcul ou la vérification.

Les différentes commandes sont les suivantes:

  **ASSIMILATION_STUDY**
    *Commande obligatoire*. C'est la commande générale qui décrit le cas
    d'assimilation de données ou d'optimisation. Elle contient hiérarchiquement
    toutes les autres commandes.

  Algorithm
    *Commande obligatoire*. C'est une chaîne de caractère qui indique
    l'algorithme d'assimilation de données ou d'optimisation choisi. Les choix
    sont limités et disponibles à travers l'interface graphique. Il existe par
    exemple le "3DVAR", le "Blue"... Voir plus loin la liste des algorithmes et
    des paramètres associés, chacun décrit par une sous-section.

  AlgorithmParameters
    *Commande optionnelle*. Elle permet d'ajouter des paramètres optionnels pour
    contrôler l'algorithme d'assimilation de données ou d'optimisation. Sa
    valeur est définie comme un objet de type "*Dict*". Voir la
    :ref:`section_ref_options_AlgorithmParameters` pour l'usage correct de cette
    commande.

  Background
    *Commande obligatoire*. Elle définit le vecteur d'ébauche ou
    d'initialisation, noté précédemment :math:`\mathbf{x}^b`. Sa valeur est
    définie comme un objet de type "*Vector*".

  BackgroundError
    *Commande obligatoire*. Elle définit la matrice de covariance des erreurs
    d'ébauche, notée précédemment :math:`\mathbf{B}`. Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  ControlInput
    *Commande optionnelle*. Elle indique le vecteur de contrôle utilisé pour
    forcer le modèle d'évolution à chaque pas, usuellement noté
    :math:`\mathbf{U}`. Sa valeur est définie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*". Lorsqu'il n'y a pas de contrôle, sa valeur doit
    être une chaîne vide ''.

  Debug
    *Commande optionnelle*. Elle définit le niveau de sorties et d'informations
    intermédiaires de débogage. Les choix sont limités entre 0 (pour False) et
    1 (pour True).

  EvolutionError
    *Commande optionnelle*. Elle définit la matrice de covariance des erreurs
    d'évolution, usuellement notée :math:`\mathbf{Q}`.  Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  EvolutionModel
    *Commande optionnelle*. Elle indique l'opérateur d'évolution du modèle,
    usuellement noté :math:`M`, qui décrit un pas élémentaire d'évolution. Sa
    valeur est définie comme un objet de type "*Function*" ou de type
    "*Matrix*". Dans le cas du type "*Function*", différentes formes
    fonctionnelles peuvent être utilisées, comme décrit dans la section
    :ref:`section_ref_operator_requirements`. Si un contrôle :math:`U` est
    inclus dans le modèle d'évolution, l'opérateur doit être appliqué à une
    paire :math:`(X,U)`.

  InputVariables
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des
    variables physiques qui sont rassemblées dans le vecteur d'état. Cette
    information est destinée à être utilisée dans le traitement algorithmique
    interne des données.

  Observation
    *Commande obligatoire*. Elle définit le vecteur d'observation utilisé en
    assimilation de données ou en optimisation, et noté précédemment
    :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*".

  ObservationError
    *Commande obligatoire*. Elle définit la matrice de covariance des erreurs
    d'ébauche, notée précédemment :math:`\mathbf{R}`. Sa valeur est définie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  ObservationOperator
    *Commande obligatoire*. Elle indique l'opérateur d'observation, noté
    précédemment :math:`H`, qui transforme les paramètres d'entrée
    :math:`\mathbf{x}` en résultats :math:`\mathbf{y}` qui sont à comparer aux
    observations :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de
    type "*Function*" ou de type "*Matrix*". Dans le cas du type "*Function*",
    différentes formes fonctionnelles peuvent être utilisées, comme décrit dans
    la section :ref:`section_ref_operator_requirements`. Si un contrôle
    :math:`U` est inclus dans le modèle d'observation, l'opérateur doit être
    appliqué à une paire :math:`(X,U)`.

  Observers
    *Commande optionnelle*. Elle permet de définir des observateurs internes,
    qui sont des fonctions liées à une variable particulière, qui sont exécutées
    chaque fois que cette variable est modifiée. C'est une manière pratique de
    suivre des variables d'intérêt durant le processus d'assimilation de données
    ou d'optimisation, en l'affichant ou en la traçant, etc. Des exemples
    courants (squelettes) sont fournis pour aider l'utilisateur ou pour
    faciliter l'élaboration d'un cas.

  OutputVariables
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des 
    variables physiques qui sont rassemblées dans le vecteur d'observation.
    Cette information est destinée à être utilisée dans le traitement
    algorithmique interne des données.

  Study_name
    *Commande obligatoire*. C'est une chaîne de caractères quelconque pour
    décrire l'étude ADAO par un nom ou une déclaration.

  Study_repertory
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

  UserPostAnalysis
    *Commande optionnelle*. Elle permet de traiter des paramètres ou des
    résultats après le déroulement de l'algorithme d'assimilation de données ou
    d'optimisation. Sa valeur est définie comme un fichier script ou une chaîne
    de caractères, permettant de produire directement du code de post-processing
    dans un cas ADAO. Des exemples courants (squelettes) sont fournis pour aider
    l'utilisateur ou pour faciliter l'élaboration d'un cas.
