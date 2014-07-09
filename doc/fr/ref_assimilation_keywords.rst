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

Liste des commandes et mots-cl�s pour un cas d'assimilation de donn�es ou d'optimisation
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

Ce jeu de commandes est li� � la description d'un cas de calcul, qui est une
proc�dure d'*Assimilation de Donn�es* ou d'*Optimisation*. Les termes sont
class�s par ordre alphab�tique, sauf le premier, qui d�crit le choix entre le
calcul ou la v�rification.

Les diff�rentes commandes sont les suivantes:

  **ASSIMILATION_STUDY**
    *Commande obligatoire*. C'est la commande g�n�rale qui d�crit le cas
    d'assimilation de donn�es ou d'optimisation. Elle contient hi�rarchiquement
    toutes les autres commandes.

  Algorithm
    *Commande obligatoire*. C'est une cha�ne de caract�re qui indique
    l'algorithme d'assimilation de donn�es ou d'optimisation choisi. Les choix
    sont limit�s et disponibles � travers l'interface graphique. Il existe par
    exemple le "3DVAR", le "Blue"... Voir plus loin la liste des algorithmes et
    des param�tres associ�s, chacun d�crit par une sous-section.

  AlgorithmParameters
    *Commande optionnelle*. Elle permet d'ajouter des param�tres optionnels pour
    contr�ler l'algorithme d'assimilation de donn�es ou d'optimisation. Sa
    valeur est d�finie comme un objet de type "*Dict*". Voir la
    :ref:`section_ref_options_AlgorithmParameters` pour l'usage correct de cette
    commande.

  Background
    *Commande obligatoire*. Elle d�finit le vecteur d'�bauche ou
    d'initialisation, not� pr�c�demment :math:`\mathbf{x}^b`. Sa valeur est
    d�finie comme un objet de type "*Vector*".

  BackgroundError
    *Commande obligatoire*. Elle d�finit la matrice de covariance des erreurs
    d'�bauche, not�e pr�c�demment :math:`\mathbf{B}`. Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  ControlInput
    *Commande optionnelle*. Elle indique le vecteur de contr�le utilis� pour
    forcer le mod�le d'�volution � chaque pas, usuellement not�
    :math:`\mathbf{U}`. Sa valeur est d�finie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*". Lorsqu'il n'y a pas de contr�le, sa valeur doit
    �tre une cha�ne vide ''.

  Debug
    *Commande optionnelle*. Elle d�finit le niveau de sorties et d'informations
    interm�diaires de d�bogage. Les choix sont limit�s entre 0 (pour False) et
    1 (pour True).

  EvolutionError
    *Commande optionnelle*. Elle d�finit la matrice de covariance des erreurs
    d'�volution, usuellement not�e :math:`\mathbf{Q}`.  Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  EvolutionModel
    *Commande optionnelle*. Elle indique l'op�rateur d'�volution du mod�le,
    usuellement not� :math:`M`, qui d�crit un pas �l�mentaire d'�volution. Sa
    valeur est d�finie comme un objet de type "*Function*" ou de type
    "*Matrix*". Dans le cas du type "*Function*", diff�rentes formes
    fonctionnelles peuvent �tre utilis�es, comme d�crit dans la section
    :ref:`section_ref_operator_requirements`. Si un contr�le :math:`U` est
    inclus dans le mod�le d'�volution, l'op�rateur doit �tre appliqu� � une
    paire :math:`(X,U)`.

  InputVariables
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des
    variables physiques qui sont rassembl�es dans le vecteur d'�tat. Cette
    information est destin�e � �tre utilis�e dans le traitement algorithmique
    interne des donn�es.

  Observation
    *Commande obligatoire*. Elle d�finit le vecteur d'observation utilis� en
    assimilation de donn�es ou en optimisation, et not� pr�c�demment
    :math:`\mathbf{y}^o`. Sa valeur est d�finie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*".

  ObservationError
    *Commande obligatoire*. Elle d�finit la matrice de covariance des erreurs
    d'�bauche, not�e pr�c�demment :math:`\mathbf{R}`. Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

  ObservationOperator
    *Commande obligatoire*. Elle indique l'op�rateur d'observation, not�
    pr�c�demment :math:`H`, qui transforme les param�tres d'entr�e
    :math:`\mathbf{x}` en r�sultats :math:`\mathbf{y}` qui sont � comparer aux
    observations :math:`\mathbf{y}^o`. Sa valeur est d�finie comme un objet de
    type "*Function*" ou de type "*Matrix*". Dans le cas du type "*Function*",
    diff�rentes formes fonctionnelles peuvent �tre utilis�es, comme d�crit dans
    la section :ref:`section_ref_operator_requirements`. Si un contr�le
    :math:`U` est inclus dans le mod�le d'observation, l'op�rateur doit �tre
    appliqu� � une paire :math:`(X,U)`.

  Observers
    *Commande optionnelle*. Elle permet de d�finir des observateurs internes,
    qui sont des fonctions li�es � une variable particuli�re, qui sont ex�cut�es
    chaque fois que cette variable est modifi�e. C'est une mani�re pratique de
    suivre des variables d'int�r�t durant le processus d'assimilation de donn�es
    ou d'optimisation, en l'affichant ou en la tra�ant, etc. Des exemples
    courants (squelettes) sont fournis pour aider l'utilisateur ou pour
    faciliter l'�laboration d'un cas.

  OutputVariables
    *Commande optionnelle*. Elle permet d'indiquer le nom et la taille des 
    variables physiques qui sont rassembl�es dans le vecteur d'observation.
    Cette information est destin�e � �tre utilis�e dans le traitement
    algorithmique interne des donn�es.

  Study_name
    *Commande obligatoire*. C'est une cha�ne de caract�res quelconque pour
    d�crire l'�tude ADAO par un nom ou une d�claration.

  Study_repertory
    *Commande optionnelle*. S'il existe, ce r�pertoire est utilis� comme base
    pour les calculs, et il est utilis� pour trouver les fichiers de script,
    donn�s par nom sans r�pertoire, qui peuvent �tre utilis�s pour d�finir
    certaines variables.

  UserDataInit
    *Commande optionnelle*. Elle permet d'initialiser certains param�tres ou
    certaines donn�es automatiquement avant le traitement de donn�es d'entr�e
    pour l'assimilation de donn�es ou l'optimisation. Pour cela, elle indique un
    nom de fichier de script � ex�cuter avant d'entrer dans l'initialisation des
    variables choisies.

  UserPostAnalysis
    *Commande optionnelle*. Elle permet de traiter des param�tres ou des
    r�sultats apr�s le d�roulement de l'algorithme d'assimilation de donn�es ou
    d'optimisation. Sa valeur est d�finie comme un fichier script ou une cha�ne
    de caract�res, permettant de produire directement du code de post-processing
    dans un cas ADAO. Des exemples courants (squelettes) sont fournis pour aider
    l'utilisateur ou pour faciliter l'�laboration d'un cas.
