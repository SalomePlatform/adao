..
   Copyright (C) 2008-2015 EDF R&D

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

.. index:: single: QuantileRegression
.. _section_ref_algorithm_QuantileRegression:

Algorithme de calcul "*QuantileRegression*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet d'estimer les quantiles conditionnels de la distribution
des param�tres d'�tat, exprim�s � l'aide d'un mod�le des variables observ�es. Ce
sont donc les quantiles sur les variables observ�es qui vont permettre de
d�terminer les param�tres de mod�les satisfaisant aux conditions de quantiles.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: Background
.. index:: single: Observation
.. index:: single: ObservationOperator
.. index:: single: Quantile
.. index:: single: Minimizer
.. index:: single: MaximumNumberOfSteps
.. index:: single: CostDecrementTolerance
.. index:: single: StoreSupplementaryCalculations

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

  Background
    *Commande obligatoire*. Elle d�finit le vecteur d'�bauche ou
    d'initialisation, not� pr�c�demment :math:`\mathbf{x}^b`. Sa valeur est
    d�finie comme un objet de type "*Vector*" ou de type "*VectorSerie*".

  Observation
    *Commande obligatoire*. Elle d�finit le vecteur d'observation utilis� en
    assimilation de donn�es ou en optimisation, et not� pr�c�demment
    :math:`\mathbf{y}^o`. Sa valeur est d�finie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*".

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

  Quantile
    Cette cl� permet de d�finir la valeur r�elle du quantile recherch�, entre 0
    et 1. La valeur par d�faut est 0.5, correspondant � la m�diane.

    Exemple : ``{"Quantile":0.5}``

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 15000, qui est tr�s similaire � une absence de
    limite sur les it�rations. Il est ainsi recommand� d'adapter ce param�tre
    aux besoins pour des probl�mes r�els.

    Exemple : ``{"MaximumNumberOfSteps":100}``

  CostDecrementTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la fonction co�t d�cro�t moins que cette
    tol�rance au dernier pas. Le d�faut est de 1.e-6, et il est recommand� de
    l'adapter aux besoins pour des probl�mes r�els.

    Exemple : ``{"CostDecrementTolerance":1.e-7}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["BMA", "CostFunctionJ",
    "CurrentState", "OMA", "OMB", "Innovation",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"]. 

    Exemple : ``{"StoreSupplementaryCalculations":["BMA","Innovation"]}``

*Astuce pour cet algorithme :*

    Comme les commandes *"BackgroundError"* et *"ObservationError"* sont
    requises pour TOUS les algorithmes de calcul dans l'interface, vous devez
    fournir une valeur, malgr� le fait que ces commandes ne sont pas requises
    pour cet algorithme, et ne seront pas utilis�es. La mani�re la plus simple
    est de donner "1" comme un STRING pour les deux.

Informations et variables disponibles � la fin de l'algorithme
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En sortie, apr�s ex�cution de l'algorithme, on dispose d'informations et de
variables issues du calcul. La description des
:ref:`section_ref_output_variables` indique la mani�re de les obtenir par la
m�thode nomm�e ``get`` de la variable "*ADD*" du post-processing. Les variables
d'entr�e, mises � disposition de l'utilisateur en sortie pour faciliter
l'�criture des proc�dures de post-processing, sont d�crites dans
l':ref:`subsection_r_o_v_Inventaire`.

Les sorties non conditionnelles de l'algorithme sont les suivantes:

  Analysis
    *Liste de vecteurs*. Chaque �l�ment est un �tat optimal :math:`\mathbf{x}*`
    en optimisation ou une analyse :math:`\mathbf{x}^a` en assimilation de
    donn�es.

    Exemple : ``Xa = ADD.get("Analysis")[-1]``

  CostFunctionJ
    *Liste de valeurs*. Chaque �l�ment est une valeur de fonctionnelle d'�cart
    :math:`J`.

    Exemple : ``J = ADD.get("CostFunctionJ")[:]``

  CostFunctionJb
    *Liste de valeurs*. Chaque �l�ment est une valeur de fonctionnelle d'�cart
    :math:`J^b`, c'est-�-dire de la partie �cart � l'�bauche.

    Exemple : ``Jb = ADD.get("CostFunctionJb")[:]``

  CostFunctionJo
    *Liste de valeurs*. Chaque �l�ment est une valeur de fonctionnelle d'�cart
    :math:`J^o`, c'est-�-dire de la partie �cart � l'observation.

    Exemple : ``Jo = ADD.get("CostFunctionJo")[:]``

Les sorties conditionnelles de l'algorithme sont les suivantes:

  BMA
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'�bauche et l'�tat optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

  CurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�tat courant utilis�
    au cours du d�roulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  Innovation
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'innovation, qui est
    en statique l'�cart de l'optimum � l'�bauche, et en dynamique l'incr�ment
    d'�volution.

    Exemple : ``d = ADD.get("Innovation")[-1]``

  OMA
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'observation et l'�tat optimal dans l'espace des observations.

    Exemple : ``oma = ADD.get("OMA")[-1]``

  OMB
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'observation et l'�tat d'�bauche dans l'espace des observations.

    Exemple : ``omb = ADD.get("OMB")[-1]``

  SimulatedObservationAtBackground
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�bauche :math:`\mathbf{x}^b`.

    Exemple : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur observ� � l'�tat courant,
    c'est-�-dire dans l'espace des observations.

    Exemple : ``Ys = ADD.get("SimulatedObservationAtCurrentState")[-1]``

  SimulatedObservationAtOptimum
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'analyse ou de l'�tat optimal :math:`\mathbf{x}^a`.

    Exemple : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

Voir aussi
++++++++++

R�f�rences bibliographiques :
  - [Buchinsky98]_
  - [Cade03]_
  - [Koenker00]_
  - [Koenker01]_
  - [WikipediaQR]_
