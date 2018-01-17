..
   Copyright (C) 2008-2018 EDF R&D

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

.. _section_methodology:

===========================================================================================
**[DocT]** Méthodologie pour élaborer une étude d'Assimilation de Données ou d'Optimisation
===========================================================================================

Cette section présente un méthodologie générique pour construire une étude
d'Assimilation de Données ou d'Optimisation. Elle décrit les étapes
conceptuelles pour établir de manière indépendante cette étude. Elle est
indépendante de tout outil, mais le module ADAO permet de mettre en oeuvre
efficacement une telle étude.

Procédure logique pour une étude
--------------------------------

Pour une étude générique d'Assimilation de Données ou d'Optimisation, les
principales étapes méthodologiques peuvent être les suivantes:

    - :ref:`section_m_step1`
    - :ref:`section_m_step2`
    - :ref:`section_m_step3`
    - :ref:`section_m_step4`
    - :ref:`section_m_step5`
    - :ref:`section_m_step6`
    - :ref:`section_m_step7`

Chaque étape est détaillée dans la section suivante.

Procédure détaillée pour une étude
----------------------------------

.. _section_m_step1:

ÉTAPE 1: Spécifier la résolution du système physique et les paramètres à ajuster
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Une source essentielle de connaissance du système physique étudié est la
simulation numérique. Elle est souvent disponible à travers un ou des cas de
calcul, et elle est symbolisée par un **opérateur de simulation** (précédemment
inclus dans :math:`H`). Un cas de calcul standard rassemble des hypothèses de
modèles, une implémentation numérique, des capacités de calcul, etc. de manière
à représenter le comportement du système physique. De plus, un cas de calcul est
caractérisé par exemple par ses besoins en temps de calcul et en mémoire, par la
taille de ses données et de ses résultats, etc. La connaissance de tous ces
éléments est primordiale dans la mise au point d'une étude d'assimilation de
données ou d'optimisation.

Pour établir correctement une étude, il faut aussi choisir les inconnues
d'optimisation incluses dans la simulation. Fréquemment, cela peut être à l'aide
de modèles physiques dont les paramètres peuvent être ajustés. De plus, il est
toujours utile d'ajouter une connaissance de type sensibilité, comme par exemple
celle de la simulation par rapport aux paramètres qui peuvent être ajustés. Des
éléments plus généraux, comme la stabilité ou la régularité de la simulation par
rapport aux inconnues en entrée, sont aussi d'un grand intérêt.

En pratique, les méthodes d'optimisation peuvent requérir une information de
type gradient de la simulation par rapport aux inconnues. Dans ce cas, le
gradient explicite du code doit être donné, ou le gradient numérique doit être
établi. Sa qualité est en relation avec la stabilité ou la régularité du code de
simulation, et elle doit être vérifiée avec soin avant de mettre en oeuvre les
calculs d'optimisation. Des conditions spécifiques doivent être utilisées pour
ces vérifications.

Un **opérateur d'observation** est toujours requis, en complément à l'opérateur
de simulation. Cet opérateur d'observation, noté :math:`H` ou inclus dedans,
doit convertir les sorties de la simulation numérique en quelque-chose qui est
directement comparable aux observations. C'est un opérateur essentiel, car il
est le moyen pratique de comparer les simulations et les observations. C'est
usuellement réalisé par échantillonnage, projection ou intégration, des sorties
de simulation, mais cela peut être plus compliqué. Souvent, du fait que
l'opérateur d'observation fasse directement suite à celui de simulation dans un
schéma simple d'assimilation de données, cet opérateur d'observation utilise
fortement les capacités de post-traitement et d'extraction du code de
simulation.

.. _section_m_step2:

ÉTAPE 2: Spécifier les critères de qualification des résultats physiques
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Comme les systèmes étudiés ont une réalité physique, il est important d'exprimer
les **information physiques qui peuvent aider à qualifier un état simulé du
système**. Il y a deux grand types d'informations qui conduisent à des critères
permettant la qualification et la quantification de résultats d'optimisation.

Premièrement, provenant d'une connaissance mathématique ou numérique, un grand
nombre d'indicateurs standards permettent de qualifier, en relatif ou en absolu,
l'intérêt d'un état optimal. Par exemple, des équations d'équilibre ou des
conditions de fermeture sont des mesures complémentaires de la qualité d'un état
du système. Des critères bien choisis comme des RMS, des RMSE, des extrema de
champs, des intégrales, etc. permettent d'évaluer la qualité d'un état optimisé.

Deuxièmement, provenant d'une connaissance physique ou expérimentale, des
informations utiles peuvent être obtenus à partir de l'interprétation des
résultats d'optimisation. En particulier, la validité physique ou l'intérêt
technique permettent d'évaluer l'intérêt de résultats des résultats numériques
de l'optimisation.

Pour obtenir une information signifiante de ces deux types de connaissances, il
est recommandé, si possible, de construire des critères numériques pour
faciliter l'évaluation de la qualité globale des résultats numériques

.. _section_m_step3:

ÉTAPE 3: Identifier et décrire les observations disponibles
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

En tant que seconde source d'information principale à propos du système physique
à étudier, les **observations, ou mesures,** notées :math:`\mathbf{y}^o`,
doivent être décrites avec soin. La qualité des mesures, leur erreurs
intrinsèques, leur particularités, sont importantes à connaître, pour pouvoir
introduire ces informations dans les calculs d'assimilation de données ou
d'optimisation.

Les observations doivent non seulement être disponibles, mais aussi doivent
pouvoir être introduites efficacement dans l'environnement numérique de calcul
ou d'optimisation. Ainsi l'environnement d'accès numérique aux observations est
fondamental pour faciliter l'usage effectif de mesures variées et de sources
diverses, et pour encourager des essais extensifs utilisant des mesures.
L'environnement d'accès numérique intègre la disponibilité de bases de données
ou pas, les formats de données, les interfaces d'accès, etc.

.. _section_m_step4:

ÉTAPE 4: Spécifier les éléments de modélisation de l'AD/Optimisation (covariances, ébauche...)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Des éléments supplémentaires de modélisation en Assimilation de Données ou en
Optimisation permettent d'améliorer l'information à propos de la représentation
détaillée du système physique étudié.

La connaissance *a-priori* de l'état du système peut être représentée en
utilisant l'**ébauche**, notée :math:`\mathbf{x}^b`, et la **matrice de
covariance des erreurs d'ébauche**, notée :math:`\mathbf{B}`. Ces informations
sont extrêmement importantes à compléter, en particulier pour obtenir des
résultats signifiants en Assimilation de Données.

Par ailleurs, des informations sur les erreurs d'observation peuvent être
utilisées pour compléter la **matrice de covariance des erreurs d'observation**,
notée :math:`\mathbf{R}`. Comme pour :math:`\mathbf{B}`, il est recommandé
d'utiliser des informations soigneusement vérifiées pour renseigner ces matrices
de covariances.

Dans le cas de simulations dynamiques, il est de plus nécessaire de définir un
**opérateur d'évolution** et la **matrice de covariance des erreurs
d'évolution** associée.

.. _section_m_step5:

ÉTAPE 5: Choisir l'algorithme d'optimisation et ses paramètres
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

L'Assimilation de Données ou l'Optimisation demandent de résoudre un problème
d'optimisation, le plus souvent sous la forme d'un problème de minimisation.
Selon la disponibilité du gradient de la fonction coût en fonction des
paramètres d'optimisation, la classe recommandée de méthodes sera différente.
Les méthodes d'optimisation variationnelles ou avec linéarisation locale
nécessitent ce gradient. A l'opposé, les méthodes sans dérivées ne nécessitent
pas ce gradient, mais présentent souvent un coût de calcul notablement
supérieur.

A l'intérieur même d'une classe de méthodes d'optimisation, pour chaque méthode,
il y a usuellement un compromis à faire entre les *"capacités génériques de la
méthode"* et ses *"performances particulières sur un problème spécifique"*. Les
méthodes les plus génériques, comme par exemple la minimisation variationnelle
utilisant l':ref:`section_ref_algorithm_3DVAR`, présentent de remarquables
propriétés numériques d'efficacité, de robustesse et de fiabilité, ce qui
conduit à les recommander indépendamment du problème à résoudre. De plus, il est
souvent difficile de régler les paramètres d'une méthode d'optimisation, donc la
méthodes la plus robuste est souvent celle qui présente le moins de paramètres.
Au final, au moins au début, il est recommandé d'utiliser les méthodes les plus
génériques et de changer le moins possible les paramètres par défaut connus.

.. _section_m_step6:

ÉTAPE 6: Conduire les calculs d'optimisation et obtenir les résultats
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Après avoir mis au point une étude d'Assimilation de Données ou d'Optimisation,
les calculs doivent être conduits de manière efficace.

Comme l'optimisation requiert usuellement un grand nombre de simulations
physiques élémentaires du système, les calculs sont souvent effectués dans un
environnement de calculs hautes performances (HPC, ou Hight Performance
Computing) pour réduire le temps complet d'utilisateur. Même si le problème
d'optimisation est petit, le temps de simulation du système physique peut être
long, nécessitant des ressources de calcul conséquentes. Ces besoins doivent
être pris en compte suffisamment tôt dans la procédure d'étude pour être
satisfaits sans nécessiter un effort trop important.

Pour la même raison de besoins de calculs importants, il est aussi important de
préparer soigneusement les sorties de la procédure d'optimisation. L'état
optimal est la principale information requise, mais un grand nombre d'autres
informations spéciales peuvent être obtenues au cours du calcul d'optimisation
ou à la fin: évaluation des erreurs, états intermédiaires, indicateurs de
qualité, etc. Toutes ces informations, nécessitant parfois des calculs
additionnels, doivent être connues et demandées au début du processus
d'optimisation.

.. _section_m_step7:

ÉTAPE 7: Exploiter les résultats et qualifier leur pertinence physique
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Une fois les résultats obtenus, ils doivent être interprétés en termes de
significations physique et numérique. Même si la démarche d'optimisation donne
toujours un nouvel état optimal qui est au moins aussi bon que l'état *a
priori*, et le plus souvent meilleur, cet état optimal doit par exemple être
vérifié par rapport aux critères de qualité identifiés au moment de
:ref:`section_m_step2`. Cela peut conduire à des études statistiques ou
numériques de manière à évaluer l'intérêt d'un état optimal pour représenter la
système physique.

Au-delà de cette analyse qui doit être réalisée pour chaque étude d'Assimilation
de Données ou d'Optimisation, il est très utile d'exploiter les résultats
d'optimisation comme une partie intégrée dans une étude plus complète du système
physique d'intérêt.
