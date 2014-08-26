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

.. index:: single: LinearLeastSquares
.. _section_ref_algorithm_LinearLeastSquares:

Algorithme de calcul "*LinearLeastSquares*"
-------------------------------------------

Description
+++++++++++

Cet algorithme r�alise une estimation lin�aire de type "Moindres Carr�s"
pond�r�s. Il est similaire � l':ref:`section_ref_algorithm_Blue`
amput� de sa partie �bauche.

Cet algorithme est toujours le plus rapide de l'ensemble des algorithmes
d'optimisation d'ADAO. Il est th�oriquement r�serv� aux cas d'op�rateurs
d'observation lin�aires, m�me s'il fonctionne parfois dans les cas "faiblement"
non-lin�aire. On peut v�rifier la lin�arit� de l'op�rateur d'observation �
l'aide de l':ref:`section_ref_algorithm_LinearityTest`.

Dans tous les cas, il est recommand� de lui pr�f�rer au minimum
l':ref:`section_ref_algorithm_Blue`, voire
l':ref:`section_ref_algorithm_ExtendedBlue` ou
l':ref:`section_ref_algorithm_3DVAR`.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: StoreInternalVariables
.. index:: single: StoreSupplementaryCalculations

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

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

Les commandes optionnelles g�n�rales, disponibles dans l'interface en �dition,
sont indiqu�es dans la :ref:`section_ref_assimilation_keywords`. En particulier,
la commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  StoreInternalVariables
    Cette cl� bool�enne permet de stocker les variables internes par d�faut,
    principalement l'�tat courant lors d'un processus it�ratif. Attention, cela
    peut �tre un choix num�riquement co�teux dans certains cas de calculs. La
    valeur par d�faut est "False".

    Exemple : ``{"StoreInternalVariables":True}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["OMA"].

    Exemple : ``{"StoreSupplementaryCalculations":["OMA"]}``

*Astuce pour cet algorithme :*

    Comme les commandes *"Background"* et *"BackgroundError"* sont requises pour
    TOUS les algorithmes de calcul dans l'interface, vous devez fournir une
    valeur, malgr� le fait que ces commandes ne sont pas requises pour
    cet algorithme, et ne seront pas utilis�es. La mani�re la plus simple est
    de donner "1" comme un STRING pour les deux.

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_Blue`
  - :ref:`section_ref_algorithm_ExtendedBlue`
  - :ref:`section_ref_algorithm_3DVAR`
  - :ref:`section_ref_algorithm_LinearityTest`