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

.. index:: single: 3DVAR
.. _section_ref_algorithm_3DVAR:

Algorithme de calcul "*3DVAR*"
------------------------------

Description
+++++++++++

Cet algorithme r�alise une estimation d'�tat par minimisation variationnelle de
la fonctionnelle :math:`J` d'�cart classique en assimilation de donn�es
statique:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-H(\mathbf{x}))^T.\mathbf{R}^{-1}.(\mathbf{y}^o-H(\mathbf{x}))

qui est usuellement d�sign�e comme la fonctionnelle "*3D-VAR*" (voir par exemple
[Talagrand97]_).

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: Background
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: Minimizer
.. index:: single: Bounds
.. index:: single: MaximumNumberOfSteps
.. index:: single: CostDecrementTolerance
.. index:: single: ProjectedGradientTolerance
.. index:: single: GradientNormTolerance
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

  Minimizer
    Cette cl� permet de changer le minimiseur pour l'optimiseur. Le choix par
    d�faut est "LBFGSB", et les choix possibles sont "LBFGSB" (minimisation non
    lin�aire sous contraintes, voir [Byrd95]_, [Morales11]_ et [Zhu97]_), "TNC"
    (minimisation non lin�aire sous contraintes), "CG" (minimisation non
    lin�aire sans contraintes), "BFGS" (minimisation non lin�aire sans
    contraintes), "NCG" (minimisation de type gradient conjugu� de Newton). Il
    est fortement conseill� de conserver la valeur par d�faut.

    Exemple : ``{"Minimizer":"LBFGSB"}``

  Bounds
    Cette cl� permet de d�finir des bornes sup�rieure et inf�rieure pour chaque
    variable d'�tat optimis�e. Les bornes doivent �tre donn�es par une liste de
    liste de paires de bornes inf�rieure/sup�rieure pour chaque variable, avec
    une valeur ``None`` chaque fois qu'il n'y a pas de borne. Les bornes peuvent
    toujours �tre sp�cifi�es, mais seuls les optimiseurs sous contraintes les
    prennent en compte.

    Exemple : ``{"Bounds":[[2.,5.],[1.e-2,10.],[-30.,None],[None,None]]}``

  MaximumNumberOfSteps
    Cette cl� indique le nombre maximum d'it�rations possibles en optimisation
    it�rative. Le d�faut est 15000, qui est tr�s similaire � une absence de
    limite sur les it�rations. Il est ainsi recommand� d'adapter ce param�tre
    aux besoins pour des probl�mes r�els. Pour certains optimiseurs, le nombre
    de pas effectif d'arr�t peut �tre l�g�rement diff�rent de la limite � cause
    d'exigences de contr�le interne de l'algorithme.

    Exemple : ``{"MaximumNumberOfSteps":100}``

  CostDecrementTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la fonction co�t d�cro�t moins que cette
    tol�rance au dernier pas. Le d�faut est de 1.e-7, et il est recommand�
    de l'adapter aux besoins pour des probl�mes r�els.

    Exemple : ``{"CostDecrementTolerance":1.e-7}``

  ProjectedGradientTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque toutes les composantes du gradient projet�
    sont en-dessous de cette limite. C'est utilis� uniquement par les
    optimiseurs sous contraintes. Le d�faut est -1, qui d�signe le d�faut
    interne de chaque optimiseur (usuellement 1.e-5), et il n'est pas recommand�
    de le changer.

    Exemple : ``{"ProjectedGradientTolerance":-1}``

  GradientNormTolerance
    Cette cl� indique une valeur limite, conduisant � arr�ter le processus
    it�ratif d'optimisation lorsque la norme du gradient est en dessous de cette
    limite. C'est utilis� uniquement par les optimiseurs sans contraintes. Le
    d�faut est 1.e-5 et il n'est pas recommand� de le changer.

    Exemple : ``{"GradientNormTolerance":1.e-5}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables suppl�mentaires qui peuvent �tre
    disponibles � la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage co�teux. La valeur par d�faut est une liste vide,
    aucune de ces variables n'�tant calcul�e et stock�e par d�faut. Les noms
    possibles sont dans la liste suivante : ["APosterioriCorrelations",
    "APosterioriCovariance", "APosterioriStandardDeviations",
    "APosterioriVariances", "BMA", "CostFunctionJ", "CurrentOptimum",
    "CurrentState", "IndexOfOptimum", "Innovation", "InnovationAtCurrentState",
    "MahalanobisConsistency", "OMA", "OMB", "SigmaObs2",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentOptimum",
    "SimulatedObservationAtCurrentState", "SimulatedObservationAtOptimum",
    "SimulationQuantiles"].

    Exemple : ``{"StoreSupplementaryCalculations":["BMA", "Innovation"]}``

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

  APosterioriCorrelations
    *Liste de matrices*. Chaque �l�ment est une matrice de corr�lations des
    erreurs *a posteriori* de l'�tat optimal, issue de la matrice
    :math:`\mathbf{A}*` des covariances.

    Exemple : ``C = ADD.get("APosterioriCorrelations")[-1]``

  APosterioriCovariance
    *Liste de matrices*. Chaque �l�ment est une matrice :math:`\mathbf{A}*` de
    covariances des erreurs *a posteriori* de l'�tat optimal.

    Exemple : ``A = ADD.get("APosterioriCovariance")[-1]``

  APosterioriStandardDeviations
    *Liste de matrices*. Chaque �l�ment est une matrice diagonale d'�carts-types
    des erreurs *a posteriori* de l'�tat optimal, issue de la matrice
    :math:`\mathbf{A}*` des covariances.

    Exemple : ``S = ADD.get("APosterioriStandardDeviations")[-1]``

  APosterioriVariances
    *Liste de matrices*. Chaque �l�ment est une matrice diagonale de variances
    des erreurs *a posteriori* de l'�tat optimal, issue de la matrice
    :math:`\mathbf{A}*` des covariances.

    Exemple : ``V = ADD.get("APosterioriVariances")[-1]``

  BMA
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�cart entre
    l'�bauche et l'�tat optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

  CurrentOptimum
    *Liste de vecteurs*. Chaque �l�ment est le vecteur d'�tat optimal au pas de
    temps courant au cours du d�roulement de l'algorithme d'optimisation. Ce
    n'est pas n�cessairement le dernier �tat.

    Exemple : ``Xo = ADD.get("CurrentOptimum")[:]``

  CurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�tat courant utilis�
    au cours du d�roulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  IndexOfOptimum
    *Liste d'entiers*. Chaque �l�ment est l'index d'it�ration de l'optimum
    obtenu au cours du d�roulement de l'algorithme d'optimisation. Ce n'est pas
    n�cessairement le num�ro de la derni�re it�ration.

    Exemple : ``i = ADD.get("IndexOfOptimum")[-1]``

  Innovation
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'innovation, qui est
    en statique l'�cart de l'optimum � l'�bauche, et en dynamique l'incr�ment
    d'�volution.

    Exemple : ``d = ADD.get("Innovation")[-1]``

  InnovationAtCurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'innovation � l'�tat
    courant.

    Exemple : ``ds = ADD.get("InnovationAtCurrentState")[-1]``

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

  SigmaObs2
    *Liste de valeurs*. Chaque �l�ment est une valeur de l'indicateur de
    qualit� :math:`(\sigma^o)^2` de la partie observation.

    Exemple : ``so2 = ADD.get("SigmaObs")[-1]``

  SimulatedObservationAtBackground
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�bauche :math:`\mathbf{x}^b`.

    Exemple : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtCurrentOptimum
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�tat optimal au pas de temps courant au cours du d�roulement de
    l'algorithme d'optimisation, c'est-�-dire dans l'espace des observations.

    Exemple : ``hxo = ADD.get("SimulatedObservationAtCurrentOptimum")[-1]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�tat courant, c'est-�-dire dans l'espace des observations.

    Exemple : ``hxs = ADD.get("SimulatedObservationAtCurrentState")[-1]``

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
  - :ref:`section_ref_algorithm_ExtendedBlue`
  - :ref:`section_ref_algorithm_LinearityTest`

R�f�rences bibliographiques :
  - [Byrd95]_
  - [Morales11]_
  - [Talagrand97]_
