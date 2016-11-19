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

.. index:: single: SamplingTest
.. _section_ref_algorithm_SamplingTest:

Algorithme de v�rification "*SamplingTest*"
-------------------------------------------

Description
+++++++++++

Cet algorithme permet d'�tablir les valeurs, li�es � un �tat :math:`\mathbf{x}`,
d'une fonctionnelle d'erreur :math:`J` quelconque de type :math:`L^1`,
:math:`L^2` ou :math:`L^{\infty}`, avec ou sans pond�rations, et de l'op�rateur
d'observation, pour un �chantillon d'�tats donn� a priori. La fonctionnelle
d'erreur par d�faut est celle de moindres carr�s pond�r�s augment�s,
classiquement utilis�e en assimilation de donn�es.

Il est utile pour tester la sensibilit�, de la fonctionnelle :math:`J`, en
particulier, aux variations de l'�tat :math:`\mathbf{x}`. Lorsque un �tat n'est
pas observable, une valeur *"NaN"* est retourn�e.

L'�chantillon des �tats :math:`\mathbf{x}` peut �tre fourni explicitement ou
sous la forme d'hyper-cubes, explicites ou �chantillonn�s selon des lois
courantes. Attention � la taille de l'hyper-cube (et donc au nombre de calculs)
qu'il est possible d'atteindre, elle peut rapidement devenir importante.

Pour appara�tre pour l'utilisateur, les r�sultats de l'�chantillonnage doivent
�tre demand�s explicitement. On utilise pour cela, sur la variable d�sir�e, la
sauvegarde finale � l'aide du mot-cl� "*UserPostAnalysis*" ou le traitement en
cours de calcul � l'aide des "*observer*" adapt�s.

Pour effectuer un �chantillonnage distribu� ou plus complexe, voir d'autres
modules disponibles dans SALOME : PARAMETRIC ou OPENTURNS.

Commandes requises et optionnelles
++++++++++++++++++++++++++++++++++

.. index:: single: AlgorithmParameters
.. index:: single: CheckingPoint
.. index:: single: BackgroundError
.. index:: single: Observation
.. index:: single: ObservationError
.. index:: single: ObservationOperator
.. index:: single: SampleAsnUplet
.. index:: single: SampleAsExplicitHyperCube
.. index:: single: SampleAsMinMaxStepHyperCube
.. index:: single: SampleAsIndependantRandomVariables
.. index:: single: QualityCriterion
.. index:: single: SetDebug
.. index:: single: SetSeed
.. index:: single: StoreSupplementaryCalculations

Les commandes requises g�n�rales, disponibles dans l'interface en �dition, sont
les suivantes:

  CheckingPoint
    *Commande obligatoire*. Elle d�finit le vecteur utilis� comme l'�tat autour
    duquel r�aliser le test requis, not� :math:`\mathbf{x}` et similaire �
    l'�bauche :math:`\mathbf{x}^b`. Sa valeur est d�finie comme un objet de type
    "*Vector*".

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
    *Commande obligatoire*. Elle indique l'op�rateur d'observation, not�e
    pr�c�demment :math:`H`, qui transforme les param�tres d'entr�e
    :math:`\mathbf{x}` en r�sultats :math:`\mathbf{y}` qui sont � comparer aux
    observations :math:`\mathbf{y}^o`.  Sa valeur est d�finie comme un objet de
    type "*Function*". Diff�rentes formes fonctionnelles peuvent �tre
    utilis�es, comme d�crit dans la section
    :ref:`section_ref_operator_requirements`. Si un contr�le :math:`U` est
    inclus dans le mod�le d'observation, l'op�rateur doit �tre appliqu� � une
    paire :math:`(X,U)`.

Les commandes optionnelles g�n�rales, disponibles dans l'interface en �dition,
sont indiqu�es dans la :ref:`section_ref_checking_keywords`. De plus, les
param�tres de la commande "*AlgorithmParameters*" permettent d'indiquer les
options particuli�res, d�crites ci-apr�s, de l'algorithme. On se reportera � la
:ref:`section_ref_options_Algorithm_Parameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  SampleAsnUplet
    Cette cl� d�crit les points de calcul sous la forme d'une liste de n-uplets,
    chaque n-uplet �tant un �tat.

    Exemple : ``{"SampleAsnUplet":[[0,1,2,3],[4,3,2,1],[-2,3,-4,5]]}`` pour 3 points dans un espace d'�tat de dimension 4

  SampleAsExplicitHyperCube
    Cette cl� d�crit les points de calcul sous la forme d'un hyper-cube, dont on
    donne la liste des �chantillonnages explicites de chaque variable comme une
    liste. C'est donc une liste de listes, chacune �tant de taille
    potentiellement diff�rente.

    Exemple : ``{"SampleAsExplicitHyperCube":[[0.,0.25,0.5,0.75,1.], [-2,2,1]]}`` pour un espace d'�tat de dimension 2

  SampleAsMinMaxStepHyperCube
    Cette cl� d�crit les points de calcul sous la forme d'un hyper-cube, dont on
    donne la liste des �chantillonnages implicites de chaque variable par un
    triplet *[min,max,step]*. C'est donc une liste de la m�me taille que celle
    de l'�tat. Les bornes sont incluses.

    Exemple : ``{"SampleAsMinMaxStepHyperCube":[[0.,1.,0.25],[-1,3,1]]}`` pour un espace d'�tat de dimension 2

  SampleAsIndependantRandomVariables
    Cette cl� d�crit les points de calcul sous la forme d'un hyper-cube, dont
    les points sur chaque axe proviennent de l'�chantillonnage al�atoire
    ind�pendant de la variable d'axe, selon la sp�cification de la
    distribution, de ses param�tres et du nombre de points de l'�chantillon,
    sous la forme d'une liste ``['distribution', [parametres], nombre]`` pour
    chaque axe. Les distributions possibles sont 'normal' de param�tres
    (mean,std), 'lognormal' de param�tres (mean,sigma), 'uniform' de param�tres
    (low,high), ou 'weibull' de param�tre (shape). C'est donc une liste de la
    m�me taille que celle de l'�tat.

    Exemple : ``{"SampleAsIndependantRandomVariables":[ ['normal',[0.,1.],3], ['uniform',[-2,2],4]]`` pour un espace d'�tat de dimension 2

  QualityCriterion
    Cette cl� indique le crit�re de qualit�, qui est utilis� pour trouver
    l'estimation de l'�tat. Le d�faut est le crit�re usuel de l'assimilation de
    donn�es nomm� "DA", qui est le crit�re de moindres carr�s pond�r�s
    augment�s. Les crit�res possibles sont dans la liste suivante, dans laquelle
    les noms �quivalents sont indiqu�s par un signe "=" :
    ["AugmentedWeightedLeastSquares"="AWLS"="DA", "WeightedLeastSquares"="WLS",
    "LeastSquares"="LS"="L2", "AbsoluteValue"="L1", "MaximumError"="ME"].

    Exemple : ``{"QualityCriterion":"DA"}``

  SetDebug
    Cette cl� requiert l'activation, ou pas, du mode de d�bogage durant
    l'�valuation de la fonction. La valeur par d�faut est "True", les choix sont
    "True" ou "False".

    Exemple : ``{"SetDebug":False}``

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
    possibles sont dans la liste suivante : ["CostFunctionJ", "CostFunctionJb",
    "CostFunctionJo", "CurrentState", "InnovationAtCurrentState",
    "SimulatedObservationAtCurrentState"].

    Exemple : ``{"StoreSupplementaryCalculations":["CostFunctionJ", "SimulatedObservationAtCurrentState"]}``

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

  CurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'�tat courant utilis�
    au cours du d�roulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  InnovationAtCurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'innovation � l'�tat
    courant.

    Exemple : ``ds = ADD.get("InnovationAtCurrentState")[-1]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque �l�ment est un vecteur d'observation simul� �
    partir de l'�tat courant, c'est-�-dire dans l'espace des observations.

    Exemple : ``hxs = ADD.get("SimulatedObservationAtCurrentState")[-1]``

Voir aussi
++++++++++

R�f�rences vers d'autres sections :
  - :ref:`section_ref_algorithm_FunctionTest`

R�f�rences vers d'autres modules SALOME :
  - PARAMETRIC, voir le *Guide utilisateur du module PARAMETRIC* dans le menu principal *Aide* de l'environnement SALOME
  - OPENTURNS, voir le *Guide utilisateur du module OPENTURNS* dans le menu principal *Aide* de l'environnement SALOME
