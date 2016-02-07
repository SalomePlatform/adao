..
   Copyright (C) 2008-2016 EDF R&D

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

.. index:: single: ExtendedBlue
.. _section_ref_algorithm_ExtendedBlue:

Algorithme de calcul "*ExtendedBlue*"
-------------------------------------

Description
+++++++++++

Cet algorithme r�alise une estimation de type BLUE �tendu (Best Linear Unbiased
Estimator, �tendu) de l'�tat d'un syst�me.

Cet algorithme est une g�n�ralisation partiellement non-lin�aire de
l':ref:`section_ref_algorithm_Blue`. Il lui est �quivalent pour un op�rateur
d'observation lin�aire. On peut v�rifier la lin�arit� de l'op�rateur
d'observation � l'aide de l':ref:`section_ref_algorithm_LinearityTest`.

En non-lin�aire, il se rapproche de l':ref:`section_ref_algorithm_3DVAR`, sans
lui �tre enti�rement �quivalent.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: StoreSupplementaryCalculations
.. index:: single: Quantiles
.. index:: single: SetSeed
.. index:: single: NumberOfSamplesForQuantiles
.. index:: single: SimulationForQuantiles

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

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["CurrentState", "Innovation",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"].

    Exemple : ``{"StoreSupplementaryCalculations":["CurrentState", "Innovation"]}``

  Quantiles
    Cette liste indique les valeurs de quantile, entre 0 et 1, � estimer par
    simulation autour de l'�tat optimal. L'�chantillonnage utilise des tirages
    al�atoires gaussiens multivari�s, dirig�s par la matrice de covariance a
    posteriori. Cette option n'est utile que si le calcul suppl�mentaire
    "SimulationQuantiles" a �t� choisi. La valeur par d�faut est une liste vide.

    Exemple : ``{"Quantiles":[0.1,0.9]}``

  SetSeed
    Cette cl� permet de donner un nombre entier pour fixer la graine du
    g�n�rateur al�atoire utilis� pour g�n�rer l'ensemble. Un valeur pratique est
    par exemple 1000. Par d�faut, la graine est laiss�e non initialis�e, et elle
    utilise ainsi l'initialisation par d�faut de l'ordinateur.

    Exemple : ``{"SetSeed":1000}``

  NumberOfSamplesForQuantiles
    Cette cl� indique le nombre de simulations effectu�es pour estimer les
    quantiles. Cette option n'est utile que si le calcul suppl�mentaire
    "SimulationQuantiles" a �t� choisi. Le d�faut est 100, ce qui suffit souvent
    pour une estimation correcte de quantiles courants � 5%, 10%, 90% ou 95%.

    Exemple : ``{"NumberOfSamplesForQuantiles":100}``

  SimulationForQuantiles
    Cette cl� indique le type de simulation, lin�aire (avec l'op�rateur
    d'observation tangent appliqu� sur des incr�ments de perturbations autour de
    l'�tat optimal) ou non-lin�aire (avec l'op�rateur d'observation standard
    appliqu� aux �tats perturb�s), que l'on veut faire pour chaque perturbation.
    Cela change essentiellement le temps de chaque simulation �l�mentaire,
    usuellement plus long en non-lin�aire qu'en lin�aire. Cette option n'est
    utile que si le calcul suppl�mentaire "SimulationQuantiles" a �t� choisi. La
    valeur par d�faut est "Linear", et les choix possibles sont "Linear" et
    "NonLinear".

    Exemple : ``{"SimulationForQuantiles":"Linear"}``

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

Les sorties conditionnelles de l'algorithme sont les suivantes:

  APosterioriCorrelations
    *Liste de matrices*. Chaque �l�ment est une matrice de corr�lation des
    erreurs *a posteriori* de l'�tat optimal.

    Exemple : ``C = ADD.get("APosterioriCorrelations")[-1]``

  APosterioriCovariance
    *Liste de matrices*. Chaque �l�ment est une matrice :math:`\mathbf{A}*` de
    covariances des erreurs *a posteriori* de l'�tat optimal.

    Exemple : ``A = ADD.get("APosterioriCovariance")[-1]``

  APosterioriStandardDeviations
    *Liste de matrices*. Chaque �l�ment est une matrice d'�cart-types des
    erreurs *a posteriori* de l'�tat optimal.

    Exemple : ``E = ADD.get("APosterioriStandardDeviations")[-1]``

  APosterioriVariances
    *Liste de matrices*. Chaque �l�ment est une matrice de variances des erreurs
    *a posteriori* de l'�tat optimal.

    Exemple : ``V = ADD.get("APosterioriVariances")[-1]``

  BMA
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'�bauche et l'�tat optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

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

  Innovation
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'innovation, qui est
    en statique l'�cart de l'optimum � l'�bauche, et en dynamique l'incr�ment
    d'�volution.

    Exemple : ``d = ADD.get("Innovation")[-1]``

  MahalanobisConsistency
    *Liste de valeurs*. Chaque �l�ment est une valeur de l'indicateur de
    qualit� de Mahalanobis.

    Exemple : ``m = ADD.get("MahalanobisConsistency")[-1]``

  OMA
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'observation et l'�tat optimal dans l'espace des observations.

    Exemple : ``oma = ADD.get("OMA")[-1]``

  OMB
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'observation et l'�tat d'�bauche dans l'espace des observations.

    Exemple : ``omb = ADD.get("OMB")[-1]``

  SigmaBck2
    *Liste de valeurs*. Chaque �l�ment est une valeur de l'indicateur de
    qualit� :math:`(\sigma^b)^2` de la partie �bauche.

    Exemple : ``sb2 = ADD.get("SigmaBck")[-1]``

  SigmaObs2
    *Liste de valeurs*. Chaque �l�ment est une valeur de l'indicateur de
    qualit� :math:`(\sigma^o)^2` de la partie observation.

    Exemple : ``so2 = ADD.get("SigmaObs")[-1]``

  SimulatedObservationAtBackground
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�bauche :math:`\mathbf{x}^b`.

    Exemple : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtOptimum
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'analyse ou de l'�tat optimal :math:`\mathbf{x}^a`.

    Exemple : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

  SimulationQuantiles
    *Liste de vecteurs*. Chaque �l�ment est un vecteur correspondant � l'�tat
    observ� qui r�alise le quantile demand�, dans le m�me ordre que les
    quantiles requis par l'utilisateur.

    Exemple : ``sQuantiles = ADD.get("SimulationQuantiles")[:]``

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_Blue`
  - :ref:`section_ref_algorithm_3DVAR`
  - :ref:`section_ref_algorithm_LinearityTest`
