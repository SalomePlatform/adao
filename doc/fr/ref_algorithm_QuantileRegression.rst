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
des paramètres d'état, exprimés à l'aide d'un modèle des variables observées. Ce
sont donc les quantiles sur les variables observées qui vont permettre de
déterminer les paramètres de modèles satisfaisant aux conditions de quantiles.

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

Les commandes requises générales, disponibles dans l'interface en édition, sont
les suivantes:

  Background
    *Commande obligatoire*. Elle définit le vecteur d'ébauche ou
    d'initialisation, noté précédemment :math:`\mathbf{x}^b`. Sa valeur est
    définie comme un objet de type "*Vector*" ou de type "*VectorSerie*".

  Observation
    *Commande obligatoire*. Elle définit le vecteur d'observation utilisé en
    assimilation de données ou en optimisation, et noté précédemment
    :math:`\mathbf{y}^o`. Sa valeur est définie comme un objet de type "*Vector*"
    ou de type "*VectorSerie*".

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

Les commandes optionnelles générales, disponibles dans l'interface en édition,
sont indiquées dans la :ref:`section_ref_assimilation_keywords`. En particulier,
la commande optionnelle "*AlgorithmParameters*" permet d'indiquer les options
particulières, décrites ci-après, de l'algorithme. On se reportera à la
:ref:`section_ref_options_AlgorithmParameters` pour le bon usage de cette
commande.

Les options de l'algorithme sont les suivantes:

  Quantile
    Cette clé permet de définir la valeur réelle du quantile recherché, entre 0
    et 1. La valeur par défaut est 0.5, correspondant à la médiane.

    Exemple : ``{"Quantile":0.5}``

  MaximumNumberOfSteps
    Cette clé indique le nombre maximum d'itérations possibles en optimisation
    itérative. Le défaut est 15000, qui est très similaire à une absence de
    limite sur les itérations. Il est ainsi recommandé d'adapter ce paramètre
    aux besoins pour des problèmes réels.

    Exemple : ``{"MaximumNumberOfSteps":100}``

  CostDecrementTolerance
    Cette clé indique une valeur limite, conduisant à arrêter le processus
    itératif d'optimisation lorsque la fonction coût décroît moins que cette
    tolérance au dernier pas. Le défaut est de 1.e-6, et il est recommandé de
    l'adapter aux besoins pour des problèmes réels.

    Exemple : ``{"CostDecrementTolerance":1.e-7}``

  StoreSupplementaryCalculations
    Cette liste indique les noms des variables supplémentaires qui peuvent être
    disponibles à la fin de l'algorithme. Cela implique potentiellement des
    calculs ou du stockage coûteux. La valeur par défaut est une liste vide,
    aucune de ces variables n'étant calculée et stockée par défaut. Les noms
    possibles sont dans la liste suivante : ["BMA", "CostFunctionJ",
    "CurrentState", "OMA", "OMB", "Innovation",
    "SimulatedObservationAtBackground", "SimulatedObservationAtCurrentState",
    "SimulatedObservationAtOptimum"]. 

    Exemple : ``{"StoreSupplementaryCalculations":["BMA","Innovation"]}``

*Astuce pour cet algorithme :*

    Comme les commandes *"BackgroundError"* et *"ObservationError"* sont
    requises pour TOUS les algorithmes de calcul dans l'interface, vous devez
    fournir une valeur, malgré le fait que ces commandes ne sont pas requises
    pour cet algorithme, et ne seront pas utilisées. La manière la plus simple
    est de donner "1" comme un STRING pour les deux.

Informations et variables disponibles à la fin de l'algorithme
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En sortie, après exécution de l'algorithme, on dispose d'informations et de
variables issues du calcul. La description des
:ref:`section_ref_output_variables` indique la manière de les obtenir par la
méthode nommée ``get`` de la variable "*ADD*" du post-processing. Les variables
d'entrée, mises à disposition de l'utilisateur en sortie pour faciliter
l'écriture des procédures de post-processing, sont décrites dans
l':ref:`subsection_r_o_v_Inventaire`.

Les sorties non conditionnelles de l'algorithme sont les suivantes:

  Analysis
    *Liste de vecteurs*. Chaque élément est un état optimal :math:`\mathbf{x}*`
    en optimisation ou une analyse :math:`\mathbf{x}^a` en assimilation de
    données.

    Exemple : ``Xa = ADD.get("Analysis")[-1]``

  CostFunctionJ
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J`.

    Exemple : ``J = ADD.get("CostFunctionJ")[:]``

  CostFunctionJb
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^b`, c'est-à-dire de la partie écart à l'ébauche.

    Exemple : ``Jb = ADD.get("CostFunctionJb")[:]``

  CostFunctionJo
    *Liste de valeurs*. Chaque élément est une valeur de fonctionnelle d'écart
    :math:`J^o`, c'est-à-dire de la partie écart à l'observation.

    Exemple : ``Jo = ADD.get("CostFunctionJo")[:]``

Les sorties conditionnelles de l'algorithme sont les suivantes:

  BMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'ébauche et l'état optimal.

    Exemple : ``bma = ADD.get("BMA")[-1]``

  CurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur d'état courant utilisé
    au cours du déroulement de l'algorithme d'optimisation.

    Exemple : ``Xs = ADD.get("CurrentState")[:]``

  Innovation
    *Liste de vecteurs*. Chaque élément est un vecteur d'innovation, qui est
    en statique l'écart de l'optimum à l'ébauche, et en dynamique l'incrément
    d'évolution.

    Exemple : ``d = ADD.get("Innovation")[-1]``

  OMA
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état optimal dans l'espace des observations.

    Exemple : ``oma = ADD.get("OMA")[-1]``

  OMB
    *Liste de vecteurs*. Chaque élément est un vecteur d'écart entre
    l'observation et l'état d'ébauche dans l'espace des observations.

    Exemple : ``omb = ADD.get("OMB")[-1]``

  SimulatedObservationAtBackground
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'ébauche :math:`\mathbf{x}^b`.

    Exemple : ``hxb = ADD.get("SimulatedObservationAtBackground")[-1]``

  SimulatedObservationAtCurrentState
    *Liste de vecteurs*. Chaque élément est un vecteur observé à l'état courant,
    c'est-à-dire dans l'espace des observations.

    Exemple : ``Ys = ADD.get("SimulatedObservationAtCurrentState")[-1]``

  SimulatedObservationAtOptimum
    *Liste de vecteurs*. Chaque élément est un vecteur d'observation simulé à
    partir de l'analyse ou de l'état optimal :math:`\mathbf{x}^a`.

    Exemple : ``hxa = ADD.get("SimulatedObservationAtOptimum")[-1]``

Voir aussi
++++++++++

Références bibliographiques :
  - [Buchinsky98]_
  - [Cade03]_
  - [Koenker00]_
  - [Koenker01]_
  - [WikipediaQR]_
