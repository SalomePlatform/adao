..
   Copyright (C) 2008-2017 EDF R&D

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

.. index:: single: ParticleSwarmOptimization
.. _section_ref_algorithm_ParticleSwarmOptimization:

Algorithme de calcul "*ParticleSwarmOptimization*"
--------------------------------------------------

Description
+++++++++++

Cet algorithme r�alise une estimation de l'�tat d'un syst�me dynamique par
minimisation d'une fonctionnelle d'�cart :math:`J` en utilisant un essaim
particulaire. C'est une m�thode qui n'utilise pas les d�riv�es de la
fonctionnelle d'�cart. Elle entre dans la m�me cat�gorie que
l':ref:`section_ref_algorithm_DerivativeFreeOptimization`.

C'est une m�thode d'optimisation permettant la recherche du minimum global d'une
fonctionnelle d'erreur :math:`J` quelconque de type :math:`L^1`, :math:`L^2` ou
:math:`L^{\infty}`, avec ou sans pond�rations. La fonctionnelle d'erreur par
d�faut est celle de moindres carr�s pond�r�s augment�s, classiquement utilis�e
en assimilation de donn�es.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: MaximumNumberOfSteps
.. index:: single: MaximumNumberOfFunctionEvaluations
.. index:: single: NumberOfInsects
.. index:: single: SwarmVelocity
.. index:: single: GroupRecallRate
.. index:: single: QualityCriterion
.. index:: single: BoxBounds
.. index:: single: SetSeed
.. index:: single: StoreSupplementaryCalculations

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

  Background
    *Commande obligatoire*. Elle d�finit le vecteur d'�bauche ou
    d'initialisation, not� pr�c�demment :math:`\mathbf{x}^b`. Sa valeur est
    d�finie comme un objet de type "*Vector*" ou de type "*VectorSerie*".

  BackgroundError
    *Commande obligatoire*. Elle d�finit la matrice de covariance des erreurs
    d'�bauche, not�e pr�c�demment :math:`\mathbf{B}`. Sa valeur est d�finie
    comme un objet de type "*Matrix*", de type "*ScalarSparseMatrix*", ou de
    type "*DiagonalSparseMatrix*".

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
sont indiqu�es dans la :ref:`section_ref_assimilation_keywords`. De plus, les
param�tres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 50, qui est une limite arbitraire. Il est ainsi
    recommand� d'adapter ce param�tre aux besoins pour des probl�mes r�els.

    Exemple : ``{"MaximumNumberOfSteps":100}``

  MaximumNumberOfFunctionEvaluations
    Cette cl� indique le nombre maximum d'�valuations possibles de la
    fonctionnelle � optimiser. Le d�faut est de 15000, qui est une limite
    arbitraire. Il est ainsi recommand� d'adapter ce param�tre aux besoins pour
    des probl�mes r�els. Pour certains optimiseurs, le nombre effectif
    d'�valuations � l'arr�t peut �tre l�g�rement diff�rent de la limite � cause
    d'exigences de d�roulement interne de l'algorithme.

    Exemple : ``{"MaximumNumberOfFunctionEvaluations":50}``

  NumberOfInsects
    Cette cl� indique le nombre d'insectes ou de particules dans l'essaim. La
    valeur par d�faut est 100, qui est une valeur par d�faut usuelle pour cet
    algorithme.

    Exemple : ``{"NumberOfInsects":100}``

  SwarmVelocity
    Cette cl� indique la part de la vitesse d'insecte qui est impos�e par
    l'essaim. C'est une valeur r�elle positive. Le d�faut est de 1.

    Exemple : ``{"SwarmVelocity":1.}``

  GroupRecallRate
    Cette cl� indique le taux de rappel vers le meilleur insecte de l'essaim.
    C'est une valeur r�elle comprise entre 0 et 1. Le d�faut est de 0.5.

    Exemple : ``{"GroupRecallRate":0.5}``

  QualityCriterion
    Cette cl� indique le crit�re de qualit�, qui est minimis� pour trouver
    l'estimation optimale de l'�tat. Le d�faut est le crit�re usuel de
    l'assimilation de donn�es nomm� "DA", qui est le crit�re de moindres carr�s
    pond�r�s augment�s. Les crit�res possibles sont dans la liste suivante, dans
    laquelle les noms �quivalents sont indiqu�s par un signe "=" :
    ["AugmentedWeightedLeastSquares"="AWLS"="DA", "WeightedLeastSquares"="WLS",
    "LeastSquares"="LS"="L2", "AbsoluteValue"="L1",  "MaximumError"="ME"].

    Exemple : ``{"QualityCriterion":"DA"}``

  BoxBounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour chaque
    incr�ment de  variable d'�tat optimis�e (et non pas chaque variable d'�tat
    elle-m�me). Les bornes doivent �tre donn�es par une liste de liste de paires
    de bornes inf�rieure/sup�rieure pour chaque incr�ment de variable, avec une
    valeur extr�me chaque fois qu'il n'y a pas de borne (``None`` n'est pas une
    valeur autoris�e lorsqu'il n'y a pas de borne). Cette cl� est requise et il
    n'y a pas de valeurs par d�faut.

    Exemple : ``{"BoxBounds":[[-0.5,0.5], [0.01,2.], [0.,1.e99], [-1.e99,1.e99]]}``

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["BMA", "CostFunctionJ",
    "CostFunctionJb", "CostFunctionJo", "CurrentState", "OMA", "OMB",
    "Innovation", "SimulatedObservationAtBackground",
    "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum"].

    Exemple : ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_DerivativeFreeOptimization`

R�f�rences bibliographiques :
  - [WikipediaPSO]_
