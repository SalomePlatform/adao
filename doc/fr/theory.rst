..
   Copyright (C) 2008-2020 EDF R&D

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

.. _section_theory:

=================================================================================
**[DocT]** Une brève introduction à l'Assimilation de Données et à l'Optimisation
=================================================================================

.. index:: single: Data Assimilation
.. index:: single: assimilation de données
.. index:: single: état vrai
.. index:: single: observation
.. index:: single: a priori

L'**assimilation de données** est un cadre général bien établi pour le calcul de
l'estimation optimale de l'état réel d'un système, au cours du temps si
nécessaire. Il utilise les valeurs obtenues en combinant des observations et des
modèles *a priori*, incluant de plus des informations sur leurs erreurs.

En d'autres termes, l'assimilation de données est un moyen de fusionner les
données mesurées d'un système, qui sont les observations, avec des
connaissances physique et mathématique *a priori* du système, intégrées dans
les modèles numériques. L'objectif est d'obtenir la meilleure estimation possible
de l'état réel du système et de ses propriétés stochastiques. On note que cet
état réel (ou "*état vrai*") ne peut être atteint, mais peut seulement être
estimé. De plus, malgré le fait que les informations utilisées sont
stochastiques par nature, l'assimilation de données fournit des techniques
déterministes afin de réaliser l'estimation de manière très efficace.

Comme l'assimilation de données cherche l'estimation la **meilleure possible**,
la démarche technique sous-jacente intègre toujours de l'optimisation afin de
trouver cette estimation : des méthodes d'optimisation choisies sont toujours
intégrées dans les algorithmes d'assimilation de données. Par ailleurs, les
méthodes d'optimisation peuvent être vues dans ADAO comme un moyen d'étendre
les applications d'assimilation de données. Elles seront présentées de cette
façon dans la section pour `Approfondir l'estimation d'état par des méthodes
d'optimisation`_, mais elles sont beaucoup plus générales et peuvent être
utilisés sans les concepts d'assimilation de données.

Deux types principaux d'applications existent en assimilation de données, qui
sont couverts par le même formalisme : l'**identification de paramètres** et la
**reconstruction de champs**. Avant d'introduire la `Description simple du cadre
méthodologique de l'assimilation de données`_ dans une prochaine section, nous
décrivons brièvement ces deux types d'applications. A la fin de ce chapitre,
quelques références permettent d'`Approfondir le cadre méthodologique de
l'assimilation de données`_ et d'`Approfondir l'estimation d'état par des
méthodes d'optimisation`_.

Reconstruction de champs ou interpolation de données
----------------------------------------------------

.. index:: single: reconstruction de champs
.. index:: single: interpolation de données
.. index:: single: interpolation de champs

La **reconstruction (ou l'interpolation) de champs** consiste à trouver, à
partir d'un nombre restreint de mesures réelles, le (ou les) champ(s)
physique(s) qui est (sont) le(s) plus *cohérent(s)* avec ces mesures.

La *cohérence* est à comprendre en termes d'interpolation, c'est-à-dire que le
champ que l'on cherche à reconstruire, en utilisant de l'assimilation de données
sur les mesures, doit s'adapter au mieux aux mesures, tout en restant contraint
par la simulation globale du champ. Le champ calculé est donc une estimation *a
priori* du champ que l'on cherche à identifier.

Si le système évolue dans le temps, la reconstruction doit être établie à chaque
pas de temps, du champ dans son ensemble. Le processus d'interpolation est dans
ce cas plus compliqué car il est temporel, et plus seulement en termes de
valeurs instantanées du champ.

Un exemple simple de reconstruction de champs provient de la météorologie, dans
laquelle on recherche les valeurs de variables comme la température ou la
pression en tout point du domaine spatial. On dispose de mesures instantanées de
ces quantités en certains points, mais aussi d'un historique de ces mesures. De
plus, ces variables sont contraintes par les équations d'évolution de
l'atmosphère, qui indiquent par exemple que la pression en un point ne peut pas
prendre une valeur quelconque indépendamment de la valeur au même point à un
temps précédent. On doit donc faire la reconstruction d'un champ en tout point
de l'espace, de manière "cohérente" avec les équations d'évolution et avec les
mesures aux précédents pas de temps.

Identification de paramètres, ajustement de modèles, calibration
----------------------------------------------------------------

.. index:: single: identification de paramètres
.. index:: single: ajustement de paramètres
.. index:: single: ajustement de modèles
.. index:: single: calibration
.. index:: single: ébauche
.. index:: single: régularisation
.. index:: single: problèmes inverses

L'**identification (ou l'ajustement) de paramètres** par assimilation de données
est une forme de calibration d'état qui utilise simultanément les mesures
physiques et une estimation *a priori* des paramètres (appelée l'"*ébauche*")
d'état que l'on cherche à identifier, ainsi qu'une caractérisation de leurs
erreurs. De ce point de vue, cette démarche utilise toutes les informations
disponibles sur le système physique, avec des hypothèses restrictives mais
réalistes sur les erreurs, pour trouver l'"*estimation optimale*" de l'état
vrai. On peut noter, en termes d'optimisation, que l'ébauche réalise la
"*régularisation*", au sens mathématique de Tikhonov [Tikhonov77]_
[WikipediaTI]_, du problème principal d'identification de paramètres. On peut
aussi désigner cette démarche comme une résolution de type "*problème inverse*".

En pratique, les deux écarts (ou incréments) observés "*calculs-mesures*" et
"*calculs-ébauche*" sont combinés pour construire la correction de calibration
des paramètres ou des conditions initiales. L'ajout de ces deux incréments
requiert une pondération relative, qui est choisie pour refléter la confiance
que l'on donne à chaque information utilisée. Cette confiance est représentée
par la covariance des erreurs sur l'ébauche et sur les observations. Ainsi
l'aspect stochastique des informations est essentiel pour construire une
fonction d'erreur pour la calibration.

Un exemple simple d'identification de paramètres provient de tout type de
simulation physique impliquant un modèle paramétré. Par exemple, une simulation
de mécanique statique d'une poutre contrainte par des forces est décrite par les
paramètres de la poutre, comme un coefficient de Young, ou par l'intensité des
forces appliquées. Le problème d'estimation de paramètres consiste à chercher
par exemple la bonne valeur du coefficient de Young de telle manière à ce que la
simulation de la poutre corresponde aux mesures, en y incluant la connaissance
des erreurs.

Toutes les grandeurs représentant la description de la physique dans un modèle
sont susceptibles d'être calibrés dans une démarche d'assimilation de données,
que ce soient des paramètres de modèles, des conditions initiales ou des
conditions aux limites. Leur prise en compte simultanée est largement facilitée
par la démarche d'assimilation de données, permettant de traiter objectivement
un ensemble hétérogène d'informations à disposition.

Description simple du cadre méthodologique de l'assimilation de données
-----------------------------------------------------------------------

.. index:: single: ébauche
.. index:: single: covariances d'erreurs d'ébauche
.. index:: single: covariances d'erreurs d'observation
.. index:: single: covariances
.. index:: single: 3DVAR
.. index:: single: Blue

On peut décrire ces démarches de manière simple. Par défaut, toutes les
variables sont des vecteurs, puisqu'il y a plusieurs paramètres à ajuster, ou
un champ discrétisé à reconstruire.

Selon les notations standards en assimilation de données, on note
:math:`\mathbf{x}^a` les paramètres optimaux qui doivent être déterminés par
calibration, :math:`\mathbf{y}^o` les observations (ou les mesures
expérimentales) auxquelles on doit comparer les sorties de simulation,
:math:`\mathbf{x}^b` l'ébauche (valeurs *a priori*, ou valeurs de
régularisation) des paramètres cherchés, :math:`\mathbf{x}^t` les paramètres
inconnus idéaux qui donneraient exactement les observations (en supposant que
toutes les erreurs soient nulles et que le modèle soit exact) en sortie.

Dans le cas le plus simple, qui est statique, les étapes de simulation et
d'observation peuvent être combinées en un unique opérateur d'observation noté
:math:`H` (linéaire ou non-linéaire). Il transforme formellement les paramètres
:math:`\mathbf{x}` en entrée en résultats :math:`\mathbf{y}`, qui peuvent être
directement comparés aux observations :math:`\mathbf{y}^o` :

.. math:: \mathbf{y} = H(\mathbf{x})

De plus, on utilise l'opérateur linéarisé (ou tangent) :math:`\mathbf{H}` pour
représenter l'effet de l'opérateur complet :math:`H` autour d'un point de
linéarisation (et on omettra ensuite de mentionner :math:`H` même si l'on peut
le conserver). En réalité, on a déjà indiqué que la nature stochastique des
variables est essentielle, provenant du fait que le modèle, l'ébauche et les
observations sont tous incorrects. On introduit donc des erreurs d'observations
additives, sous la forme d'un vecteur aléatoire :math:`\mathbf{\epsilon}^o` tel
que :

.. math:: \mathbf{y}^o = \mathbf{H} \mathbf{x}^t + \mathbf{\epsilon}^o

Les erreurs représentées ici ne sont pas uniquement celles des observations, ce
sont aussi celles de la simulation. On peut toujours considérer que ces erreurs
sont de moyenne nulle. En notant :math:`E[.]` l'espérance mathématique
classique, on peut alors définir une matrice :math:`\mathbf{R}` des covariances
d'erreurs d'observation par l'expression :

.. math:: \mathbf{R} = E[\mathbf{\epsilon}^o.{\mathbf{\epsilon}^o}^T]

L'ébauche peut être écrite formellement comme une fonction de la valeur vraie,
en introduisant le vecteur d'erreurs :math:`\mathbf{\epsilon}^b` tel que :

.. math:: \mathbf{x}^b = \mathbf{x}^t + \mathbf{\epsilon}^b

Les erreurs d'ébauche :math:`\mathbf{\epsilon}^b` sont aussi supposées de
moyenne nulle, de la même manière que pour les observations. On définit la
matrice :math:`\mathbf{B}` des covariances d'erreurs d'ébauche par :

.. math:: \mathbf{B} = E[\mathbf{\epsilon}^b.{\mathbf{\epsilon}^b}^T]

L'estimation optimale des paramètres vrais :math:`\mathbf{x}^t`, étant donné
l'ébauche :math:`\mathbf{x}^b` et les observations :math:`\mathbf{y}^o`, est
ainsi "l'*analyse*" :math:`\mathbf{x}^a` et provient de la minimisation d'une
fonction d'erreur, explicite en assimilation variationnelle, ou d'une correction
de filtrage en assimilation par filtrage.

En **assimilation variationnelle**, dans un cas statique, on cherche
classiquement à minimiser la fonction :math:`J` suivante :

.. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

:math:`J` est classiquement désignée comme la fonctionnelle "*3D-VAR*" en
assimilation de données (voir par exemple [Talagrand97]_) ou comme la
fonctionnelle de régularisation de Tikhonov généralisée en optimisation (voir
par exemple [WikipediaTI]_). Comme les matrices de covariance :math:`\mathbf{B}`
et :math:`\mathbf{R}` sont proportionnelles aux variances d'erreurs, leur
présence dans les deux termes de la fonctionnelle :math:`J` permet effectivement
de pondérer les termes d'écarts par la confiance dans les erreurs d'ébauche ou
d'observations. Le vecteur :math:`\mathbf{x}` des paramètres réalisant le
minimum de cette fonction constitue ainsi l'analyse :math:`\mathbf{x}^a`. C'est
à ce niveau que l'on doit utiliser toute la panoplie des méthodes de
minimisation de fonctions connues par ailleurs en optimisation (voir aussi la
section `Approfondir l'estimation d'état par des méthodes d'optimisation`_).
Selon la taille du vecteur :math:`\mathbf{x}` des paramètres à identifier, et la
disponibilité du gradient ou de la hessienne de :math:`J`, il est judicieux
d'adapter la méthode d'optimisation choisie (gradient, Newton, quasi-Newton...).

En **assimilation par filtrage**, dans ce cas simple usuellement dénommé
"*BLUE*" (pour "*Best Linear Unbiased Estimator*"), l'analyse
:math:`\mathbf{x}^a` est donnée comme une correction de l'ébauche
:math:`\mathbf{x}^b` par un terme proportionnel à la différence entre les
observations :math:`\mathbf{y}^o` et les calculs :math:`\mathbf{H}\mathbf{x}^b` :

.. math:: \mathbf{x}^a = \mathbf{x}^b + \mathbf{K}(\mathbf{y}^o - \mathbf{H}\mathbf{x}^b)

où :math:`\mathbf{K}` est la matrice de gain de Kalman, qui s'exprime à l'aide
des matrices de covariance sous la forme suivante :

.. math:: \mathbf{K} = \mathbf{B}\mathbf{H}^T(\mathbf{H}\mathbf{B}\mathbf{H}^T+\mathbf{R})^{-1}

L'avantage du filtrage est le calcul explicite du gain, pour produire ensuite la
matrice *a posteriori* de covariance d'analyse.

Dans ce cas statique simple, on peut montrer, sous une hypothèse de
distributions gaussiennes d'erreurs (très peu restrictive en pratique) et de
linéarité de :math:`H`, que les deux approches *variationnelle* et *de
filtrage* donnent la même solution.

On indique que ces méthodes de "*3D-VAR*" et de "*BLUE*" peuvent être étendues
à des problèmes dynamiques, sous les noms respectifs de "*4D-VAR*" et de
"*filtre de Kalman*". Elles doivent alors prendre en compte l'opérateur
d'évolution pour établir aux bons pas de temps une analyse de l'écart entre les
observations et les simulations et pour avoir, à chaque instant, la propagation
de l'ébauche à travers le modèle d'évolution. De la même manière, ces méthodes
peuvent aussi être utilisées dans le cas d'opérateurs d'observation ou
d'évolution non linéaires. Un grand nombre de variantes ont été développées
pour accroître la qualité numérique des méthodes ou pour prendre en compte des
contraintes informatiques comme la taille ou la durée des calculs.

Approfondir le cadre méthodologique de l'assimilation de données
----------------------------------------------------------------

.. index:: single: apprentissage
.. index:: single: calibration
.. index:: single: data-driven
.. index:: single: estimation bayésienne
.. index:: single: estimation d'état
.. index:: single: estimation de paramètres
.. index:: single: intelligence artificielle
.. index:: single: interpolation de champs
.. index:: single: interpolation optimale
.. index:: single: inversion
.. index:: single: lissage de données
.. index:: single: machine learning
.. index:: single: méta-heuristiques
.. index:: single: méthodes de régularisation
.. index:: single: optimisation quadratique
.. index:: single: optimisation variationnelle
.. index:: single: problèmes inverses
.. index:: single: recalage
.. index:: single: réduction de modèles
.. index:: single: régularisation mathématique

Pour obtenir de plus amples informations sur les techniques d'assimilation de
données, le lecteur peut consulter les documents introductifs comme
[Talagrand97]_ ou [Argaud09]_, des supports de formations ou de cours comme
[Bouttier99]_ et [Bocquet04]_ (ainsi que d'autres documents issus des
applications des géosciences), ou des documents généraux comme [Talagrand97]_,
[Tarantola87]_, [Asch16]_, [Kalnay03]_, [Ide97]_, [Tikhonov77]_ et
[WikipediaDA]_.

On note que l'assimilation de données n'est pas limitée à la météorologie ou aux
géo-sciences, mais est largement utilisée dans d'autres domaines scientifiques.
Il y a de nombreux champs d'applications scientifiques et technologiques dans
lesquels l'utilisation efficace des données observées, mais incomplètes, est
cruciale.

Certains aspects de l'assimilation de données sont aussi connus sous d'autres
noms. Sans être exhaustif, on peut mentionner les noms de *calage* ou de
*recalage*, de *calibration*, d'*estimation d'état*, d'*estimation de
paramètres*, de *problèmes inverses* ou d'*inversion*, d'*estimation
bayésienne*, d'*interpolation de champs* ou d'*interpolation optimale*,
d'*optimisation variationnelle*, d'*optimisation quadratique*, de
*régularisation mathématique*, de *méta-heuristiques* d'optimisation, de
*réduction de modèles*, de *lissage de données*, de pilotage des modèles par
les données (« *data-driven* »), d’*apprentissage* de modèles et de données
(*Machine Learning* et Intelligence Artificielle), etc. Ces termes peuvent être
utilisés dans les recherches bibliographiques.

Approfondir l'estimation d'état par des méthodes d'optimisation
---------------------------------------------------------------

.. index:: single: estimation d'état
.. index:: single: méthodes d'optimisation
.. index:: single: DerivativeFreeOptimization
.. index:: single: ParticleSwarmOptimization
.. index:: single: DifferentialEvolution
.. index:: single: QuantileRegression

Comme vu précédemment, dans un cas de simulation statique, l'assimilation
variationnelle de données nécessite de minimiser la fonction objectif :math:`J`:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

qui est dénommée la fonctionnelle du "*3D-VAR*". Elle peut être vue comme la
forme étendue d'une *minimisation moindres carrés*, obtenue en ajoutant un terme
de régularisation utilisant :math:`\mathbf{x}-\mathbf{x}^b`, et en pondérant les
différences par les deux matrices de covariances :math:`\mathbf{B}` et
:math:`\mathbf{R}`. La minimisation de la fonctionnelle :math:`J` conduit à la
*meilleure* estimation de l'état :math:`\mathbf{x}`. Pour obtenir plus
d'informations sur ces notions, on se reportera aux ouvrages généraux de
référence comme [Tarantola87]_.

Les possibilités d'extension de cette estimation d'état, en utilisant de manière
plus explicite des méthodes d'optimisation et leurs propriétés, peuvent être
imaginées de deux manières.

En premier lieu, les méthodes classiques d'optimisation impliquent l'usage de
méthodes de minimisation variées souvent basées sur un gradient. Elles sont
extrêmement efficaces pour rechercher un minimum local isolé. Mais elles
nécessitent que la fonctionnelle :math:`J` soit suffisamment régulière et
différentiable, et elles ne sont pas en mesure de saisir des propriétés
globales du problème de minimisation, comme par exemple : minimum global,
ensemble de solutions équivalentes dues à une sur-paramétrisation, multiples
minima locaux, etc. **Une méthode pour étendre les possibilités d'estimation
consiste donc à utiliser l'ensemble des méthodes d'optimisation existantes,
permettant la minimisation globale, diverses propriétés de robustesse de la
recherche, etc**. Il existe de nombreuses méthodes de minimisation, comme les
méthodes stochastiques, évolutionnaires, les heuristiques et méta-heuristiques
pour les problèmes à valeurs réelles, etc. Elles peuvent traiter des
fonctionnelles :math:`J` en partie irrégulières ou bruitées, peuvent
caractériser des minima locaux, etc. Les principaux désavantages de ces
méthodes sont un coût numérique souvent bien supérieur pour trouver les
estimations d'états, et fréquemment aucune garantie de convergence en temps
fini. Ici, on ne mentionne que quelques méthodes disponibles dans ADAO :

- l'*optimisation sans dérivées (Derivative Free Optimization ou DFO)* (voir :ref:`section_ref_algorithm_DerivativeFreeOptimization`),
- l'*optimisation par essaim de particules (Particle Swarm Optimization ou PSO)* (voir :ref:`section_ref_algorithm_ParticleSwarmOptimization`),
- l'*évolution différentielle (Differential Evolution ou DE)* (voir :ref:`section_ref_algorithm_DifferentialEvolution`),
- la *régression de quantile (Quantile Regression ou QR)* (voir :ref:`section_ref_algorithm_QuantileRegression`).

En second lieu, les méthodes d'optimisation cherchent usuellement à minimiser
des mesures quadratiques d'erreurs, car les propriétés naturelles de ces
fonctions objectifs sont bien adaptées à l'optimisation classique par gradient.
Mais d'autres mesures d'erreurs peuvent être mieux adaptées aux problèmes de
simulation de la physique réelle. Ainsi, **une autre manière d'étendre les
possibilités d'estimation consiste à utiliser d'autres mesures d'erreurs à
réduire**. Par exemple, on peut citer une **erreur absolue**, une **erreur
maximale**, etc. Ces mesures d'erreurs ne sont pas différentiables, mais
certaines méthodes d'optimisation peuvent les traiter: heuristiques et
méta-heuristiques pour les problèmes à valeurs réelles, etc. Comme
précédemment, les principaux désavantages de ces méthodes sont un coût
numérique souvent bien supérieur pour trouver les estimations d'états, et pas
de garantie de convergence en temps fini. Ici encore, on ne mentionne que
quelques méthodes qui sont disponibles dans ADAO :

- l'*optimisation sans dérivées (Derivative Free Optimization ou DFO)* (voir :ref:`section_ref_algorithm_DerivativeFreeOptimization`),
- l'*optimisation par essaim de particules (Particle Swarm Optimization ou PSO)* (voir :ref:`section_ref_algorithm_ParticleSwarmOptimization`),
- l'*évolution différentielle (Differential Evolution ou DE)* (voir :ref:`section_ref_algorithm_DifferentialEvolution`).

Le lecteur intéressé par le sujet de l'optimisation pourra utilement commencer
sa recherche grâce au point d'entrée [WikipediaMO]_.
