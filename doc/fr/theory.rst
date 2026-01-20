..
   Copyright (C) 2008-2026 EDF R&D

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
.. index:: single: Assimilation de données
.. index:: single: Etat vrai
.. index:: single: Observation
.. index:: single: a priori
.. index:: single: EstimationOf
.. index:: single: Analyse

**L'assimilation de données** est un cadre général bien établi pour le calcul
de l'estimation optimale de l'état réel d'un système, au cours du temps si
nécessaire. Il utilise les valeurs obtenues en combinant des observations et
des modèles *a priori*, incluant de plus des informations sur leurs erreurs
tout en respectant simultanément des contraintes. Cela tient donc compte des
lois du comportement ou de la dynamique du système à travers les équations du
modèle, et de la façon dont les mesures sont physiquement liées aux variables
simulées.

En d'autres termes, l'assimilation de données est un moyen de fusionner les
données mesurées d'un système, qui sont les observations, avec des
connaissances physique et mathématique *a priori* du système, intégrées dans
les modèles numériques. L'objectif est d'obtenir la meilleure estimation
possible, appelée "*analyse*", de l'état réel du système et de ses propriétés
stochastiques. On note que cet état réel (ou "*état vrai*") ne peut être
habituellement atteint, mais peut seulement être estimé. De plus, malgré le
fait que les informations utilisées sont stochastiques par nature,
l'assimilation de données fournit des techniques déterministes afin de réaliser
l'estimation de manière très efficace.

Comme l'assimilation de données cherche l'estimation la **meilleure possible**,
la démarche technique sous-jacente intègre toujours de l'optimisation afin de
trouver cette estimation : des méthodes d'optimisation choisies sont toujours
intégrées dans les algorithmes d'assimilation de données. Par ailleurs, les
méthodes d'optimisation peuvent être vues dans ADAO comme un moyen d'étendre
les applications d'assimilation de données. Elles seront présentées de cette
façon dans la section pour :ref:`section_theory_optimization`, mais elles sont
beaucoup plus générales et peuvent être utilisées sans les concepts
d'assimilation de données.

Deux types principaux d'applications existent en assimilation de données, qui
sont couverts par le même formalisme : la **reconstruction de champs** (voir
`Reconstruction de champs ou interpolation de données`_) et **l'identification
de paramètres** (voir `Identification de paramètres, ajustement de modèles, ou
calage`_). On parle aussi respectivement **d'estimation d'état** et
**d'estimation de paramètres**, et l'on peut aussi estimer les deux de manière
conjointe si nécessaire (voir `Estimation conjointe d'états et de
paramètres`_). Dans ADAO, certains algorithmes peuvent être utilisés soit en
estimation d'état, soit en estimation de paramètres. Cela se fait simplement en
changeant l'option requise "*EstimationOf*" dans les paramètres des
algorithmes. Avant d'introduire la :ref:`section_theory_da_framework` dans une
prochaine section, on décrit brièvement ces deux types d'applications. A la fin
de ce chapitre, quelques informations permettent d'aller plus loin pour
:ref:`section_theory_more_assimilation` et :ref:`section_theory_optimization`,
ainsi que pour :ref:`section_theory_dynamic` et avoir
:ref:`section_theory_reduction`.

Reconstruction de champs ou interpolation de données
----------------------------------------------------

.. index:: single: Reconstruction de champs
.. index:: single: Interpolation de données
.. index:: single: Interpolation de champs
.. index:: single: Estimation d'état
.. index:: single: Ebauche

La **reconstruction (ou l'interpolation) de champs** consiste à trouver, à
partir d'un nombre restreint de mesures réelles, le (ou les) champ(s)
physique(s) qui est (sont) le(s) plus *cohérent(s)* avec ces mesures.

La *cohérence* est à comprendre en termes d'interpolation, c'est-à-dire que le
champ que l'on cherche à reconstruire, en utilisant de l'assimilation de
données sur les mesures, doit s'adapter au mieux aux mesures, tout en restant
contraint par la simulation globale du champ. Le champ calculé est donc une
estimation *a priori* du champ que l'on cherche à identifier. On parle aussi
**d'estimation d'état** dans ce cas.

Si le système évolue dans le temps, la reconstruction du champ dans son
ensemble doit être établie à chaque pas de temps, en tenant compte des
informations sur une fenêtre temporelle. Le processus d'interpolation est plus
compliqué dans ce cas car il est temporel, et plus seulement en termes de
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

Identification de paramètres, ajustement de modèles, ou calage
--------------------------------------------------------------

.. index:: single: Identification de paramètres
.. index:: single: Ajustement de paramètres
.. index:: single: Ajustement de modèles
.. index:: single: Recalage
.. index:: single: Calage
.. index:: single: Ebauche
.. index:: single: Régularisation
.. index:: single: Problèmes inverses
.. index:: single: Estimation de paramètres

**L'identification (ou l'ajustement) de paramètres** par assimilation de
données est une forme de calage d'état qui utilise simultanément les mesures
physiques et une estimation *a priori* des paramètres (appelée "*l'ébauche*")
d'état que l'on cherche à identifier, ainsi qu'une caractérisation de leurs
erreurs. De ce point de vue, cette démarche utilise toutes les informations
disponibles sur le système physique, avec des hypothèses restrictives mais
réalistes sur les erreurs, pour trouver "*l'estimation optimale*" de l'état
vrai. On peut noter, en termes d'optimisation, que l'ébauche réalise la
"*régularisation*", au sens mathématique de Tikhonov [Tikhonov77]_
[WikipediaTI]_, du problème principal d'identification de paramètres. On peut
aussi désigner cette démarche comme une résolution de type "*problème
inverse*".

En pratique, les deux écarts (ou incréments) observés "*calculs-mesures*" et
"*calculs-ébauche*" sont combinés pour construire la correction de calage des
paramètres ou des conditions initiales. L'ajout de ces deux incréments requiert
une pondération relative, qui est choisie pour refléter la confiance que l'on
donne à chaque information utilisée. Cette confiance est représentée par la
covariance des erreurs sur l'ébauche et sur les observations. Ainsi l'aspect
stochastique des informations est essentiel pour construire une fonction
d'erreur pour le calage.

Un exemple simple d'identification de paramètres provient de tout type de
simulation physique impliquant un modèle paramétré. Par exemple, une simulation
de mécanique statique d'une poutre contrainte par des forces est décrite par les
paramètres de la poutre, comme un coefficient de Young, ou par l'intensité des
forces appliquées. Le problème d'estimation de paramètres consiste à chercher
par exemple la bonne valeur du coefficient de Young de telle manière à ce que la
simulation de la poutre corresponde aux mesures, en y incluant la connaissance
des erreurs.

Toutes les grandeurs représentant la description de la physique dans un modèle
sont susceptibles d'être calibrées dans une démarche d'assimilation de données,
que ce soient des paramètres de modèles, des conditions initiales ou des
conditions aux limites. Leur prise en compte simultanée est largement facilitée
par la démarche d'assimilation de données, permettant de traiter objectivement
un ensemble hétérogène d'informations à disposition.

Estimation conjointe d'états et de paramètres
---------------------------------------------

.. index:: single: Jointe (estimation d'états et de paramètres)
.. index:: single: Estimation conjointe d'états et de paramètres

Il parfois nécessaire, en considérant les deux types d'applications
précédentes, d'avoir besoin d'estimer en même temps des états (champs) et des
paramètres caractérisant un phénomène physique. On parle alors **d'estimation
conjointe d'états et de paramètres**.

Sans rentrer ici dans les méthodes avancées pour résoudre ce problème, on peut
mentionner la démarche conceptuellement très simple consistant à considérer le
vecteur des états à interpoler comme *augmenté* par le vecteur des paramètres à
caler. On note que l'on est globalement en *estimation d'état* ou
*reconstruction de champs*, et que dans le cas temporel de l'identification de
paramètres, l'évolution des paramètres à estimer est simplement l'identité. Les
algorithmes d'assimilation ou d'optimisation peuvent ensuite être appliqués au
vecteur augmenté. Valable dans le cas de non-linéarités modérées dans la
simulation, cette méthode simple étend l'espace d'optimisation, et conduit donc
à des problèmes plus gros, mais il est souvent possible de réduire la
représentation pour revenir à des cas numériquement calculables. Sans
exhaustivité, l'optimisation à variables séparées, le filtrage de rang réduit,
ou le traitement spécifique des matrices de covariances, sont des techniques
courantes pour éviter ce problème de dimension. Dans le cas temporel, on verra
ci-après des indications pour une `Estimation conjointe d'état et de paramètres
en dynamique`_.

Pour aller plus loin, on se référera aux méthodes mathématiques d'optimisation
et d'augmentation développées dans de nombreux ouvrages ou articles
spécialisés, trouvant leur origine par exemple dans [Lions68]_, [Jazwinski70]_
ou [Dautray85]_. En particulier dans le cas de non-linéarités plus marquées
lors de la simulation numérique des états, il convient de traiter de manière
plus complète mais aussi plus complexe le problème d'estimation conjointe
d'états et de paramètres.

.. _section_theory_da_framework:

Description simple du cadre méthodologique de l'assimilation de données
-----------------------------------------------------------------------

.. index:: single: Analyse
.. index:: single: Ebauche
.. index:: single: Covariances d'erreurs d'ébauche
.. index:: single: Covariances d'erreurs d'observation
.. index:: single: Covariances
.. index:: single: 3DVAR
.. index:: single: Blue

On peut décrire ces démarches de manière simple. Par défaut, toutes les
variables sont des vecteurs, puisqu'il y a plusieurs paramètres à ajuster, ou
un champ discrétisé à reconstruire.

Selon les notations standards en assimilation de données, on note
:math:`\mathbf{x}^a` les paramètres optimaux qui doivent être déterminés par
calage, :math:`\mathbf{y}^o` les observations (ou les mesures expérimentales)
auxquelles on doit comparer les sorties de simulation, :math:`\mathbf{x}^b`
l'ébauche (valeurs *a priori*, ou valeurs de régularisation) des paramètres
cherchés, :math:`\mathbf{x}^t` les paramètres inconnus idéaux qui donneraient
exactement les observations (en supposant que toutes les erreurs soient nulles
et que le modèle soit exact) en sortie.

Dans le cas le plus simple, qui est statique, les étapes de simulation et
d'observation peuvent être combinées en un unique opérateur d'observation noté
:math:`\mathcal{H}` (linéaire ou non-linéaire). Il transforme formellement les
paramètres :math:`\mathbf{x}` en entrée en résultats :math:`\mathbf{y}`, qui
peuvent être directement comparés aux observations :math:`\mathbf{y}^o` :

.. math:: \mathbf{y} = \mathcal{H}(\mathbf{x})

De plus, on utilise l'opérateur linéarisé (ou tangent) :math:`\mathbf{H}` pour
représenter l'effet de l'opérateur complet :math:`\mathcal{H}` autour d'un
point de linéarisation (et on omettra usuellement ensuite de mentionner
:math:`\mathcal{H}`, même si l'on peut le conserver, pour ne mentionner que
:math:`\mathbf{H}`). En réalité, on a déjà indiqué que la nature stochastique
des variables est essentielle, provenant du fait que le modèle, l'ébauche et
les observations sont tous incorrects. On introduit donc des erreurs
d'observations additives, sous la forme d'un vecteur aléatoire
:math:`\mathbf{\epsilon}^o` tel que :

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
ainsi appelée une "*analyse*", notée :math:`\mathbf{x}^a`, et provient de la
minimisation d'une fonction d'erreur, explicite en assimilation variationnelle,
ou d'une correction de filtrage en assimilation par filtrage.

En **assimilation variationnelle**, dans un cas statique, on cherche
classiquement à minimiser la fonction :math:`J` suivante :

.. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

:math:`J` est classiquement désignée comme la fonctionnelle "*3D-Var*" en
assimilation de données (voir par exemple [Talagrand97]_) ou comme la
fonctionnelle de régularisation de Tikhonov généralisée en optimisation (voir
par exemple [WikipediaTI]_). Comme les matrices de covariance
:math:`\mathbf{B}` et :math:`\mathbf{R}` sont proportionnelles aux variances
d'erreurs, leur présence dans les deux termes de la fonctionnelle :math:`J`
permet effectivement de pondérer les termes d'écarts par la confiance dans les
erreurs d'ébauche ou d'observations. Le vecteur :math:`\mathbf{x}` des
paramètres réalisant le minimum de cette fonction constitue ainsi l'analyse
:math:`\mathbf{x}^a`. C'est à ce niveau que l'on doit utiliser toute la
panoplie des méthodes de minimisation de fonctions connues par ailleurs en
optimisation (voir aussi la section :ref:`section_theory_optimization`). Selon
la taille du vecteur :math:`\mathbf{x}` des paramètres à identifier, et la
disponibilité du gradient ou de la hessienne de :math:`J`, il est judicieux
d'adapter la méthode d'optimisation choisie (gradient, Newton,
quasi-Newton...).

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
linéarité de :math:`\mathcal{H}`, que les deux approches *variationnelle* et
*de filtrage* donnent la même solution.

On indique que ces méthodes de "*3D-Var*" et de "*BLUE*" peuvent être étendues
à des problèmes dynamiques ou temporels, sous les noms respectifs de "*4D-Var*"
et de "*Filtre de Kalman (KF)*" et leurs dérivés. Elles doivent alors prendre
en compte un opérateur d'évolution pour établir aux bons pas de temps une
analyse de l'écart entre les observations et les simulations et pour avoir, à
chaque instant, la propagation de l'ébauche à travers le modèle d'évolution. On
se reportera à la section suivante pour :ref:`section_theory_dynamic`. De
la même manière, ces méthodes peuvent aussi être utilisées dans le cas
d'opérateurs d'observation ou d'évolution non linéaires. Un grand nombre de
variantes ont été développées pour accroître la qualité numérique des méthodes
ou pour prendre en compte des contraintes informatiques comme la taille ou la
durée des calculs.

Une vue schématique des approches d'Assimilation de Données et d'Optimisation
-----------------------------------------------------------------------------

Pour aider le lecteur à se faire un idée des approches utilisables avec ADAO en
Assimilation de Données et en Optimisation, on propose ici un schéma simplifié
décrivant une classification arbitraire des méthodes. Il est partiellement et
librement inspiré de [Asch16]_ (Figure 1.5).

  .. _meth_steps_in_study:
  .. image:: images/meth_ad_and_opt.png
    :align: center
    :width: 75%
  .. centered::
    **Une classification simplifiée de méthodes utilisables avec ADAO en Assimilation de Données et en Optimisation (les acronymes et les liens descriptifs internes sont énumérés ci-dessous)**

Il est volontairement simple pour rester lisible, les lignes tiretées montrant
certaines des simplifications ou extensions. Ce schéma omet par exemple de
citer spécifiquement les méthodes avec réductions (dont il est donné ci-après
:ref:`section_theory_reduction`), dont une partie sont des variantes de
méthodes de base indiquées ici, ou de citer les extensions les plus détaillées.
Il omet de même les méthodes de tests disponibles dans ADAO et utiles pour la
mise en étude.

Chaque méthode citée dans ce schéma fait l'objet d'une partie descriptive
spécifique dans le chapitre des :ref:`section_reference_assimilation`. Les
acronymes cités dans le schéma ont la signification indiquée dans les pointeurs
associés :

- 3D-Var : :ref:`section_ref_algorithm_3DVAR`,
- 4D-Var : :ref:`section_ref_algorithm_4DVAR`,
- Blue : :ref:`section_ref_algorithm_Blue`,
- DiffEvol : :ref:`section_ref_algorithm_DifferentialEvolution`,
- EKF : :ref:`section_ref_algorithm_ExtendedKalmanFilter`,
- EnKF : :ref:`section_ref_algorithm_EnsembleKalmanFilter`,
- DFO : :ref:`section_ref_algorithm_DerivativeFreeOptimization`,
- Incr-Var : Incremental version Variational optimisation,
- KF : :ref:`section_ref_algorithm_KalmanFilter`,
- LLS : :ref:`section_ref_algorithm_LinearLeastSquares`,
- NLLS : :ref:`section_ref_algorithm_NonLinearLeastSquares`,
- QR : :ref:`section_ref_algorithm_QuantileRegression`,
- Swarm : :ref:`section_ref_algorithm_ParticleSwarmOptimization`,
- Tabu : :ref:`section_ref_algorithm_TabuSearch`,
- UKF : :ref:`section_ref_algorithm_UnscentedKalmanFilter`.

.. _section_theory_reduction:

Un aperçu des méthodes de réduction et de l'optimisation réduite
----------------------------------------------------------------

.. index:: single: Réduction
.. index:: single: Méthodes de réduction
.. index:: single: Méthodes réduites
.. index:: single: Espace réduit
.. index:: single: Sous-espace neutre
.. index:: single: SVD
.. index:: single: POD
.. index:: single: PCA
.. index:: single: Kahrunen-Loeve
.. index:: single: RBM
.. index:: single: ROM
.. index:: single: EIM
.. index:: single: Fourier
.. index:: single: Ondelettes
.. index:: single: EOF
.. index:: single: Sparse

Les démarches d'assimilation de données et d'optimisation impliquent toujours
une certaine réitération d'une simulation numérique unitaire représentant la
physique que l'on veut traiter. Pour traiter au mieux cette physique, cette
simulation numérique unitaire est souvent de taille importante voire imposante,
et conduit à un coût calcul extrêmement important dès lors qu'il est répété. La
simulation physique complète est souvent appelée "*simulation haute fidélité*"
(ou "*high fidelity simulation*" ou "*full scale simulation*").

Pour éviter cette difficulté pratique, **différentes stratégies de réduction du
coût du calcul d'optimisation existent, et certaines permettent également de
contrôler au mieux l'erreur numérique impliquée par cette réduction**. Ces
stratégies sont intégrées de manière transparente à certaines des méthodes
d'ADAO ou font l'objet d'algorithmes particuliers.

Pour établir une telle démarche, on cherche à réduire au moins l'un des
ingrédients qui composent le problème d'assimilation de données ou
d'optimisation. On peut ainsi classer les méthodes de réduction selon
l'ingrédient sur lequel elles opèrent, en sachant que certaines méthodes
portent sur plusieurs d'entre eux. On indique ici une classification grossière,
que le lecteur peut compléter par la lecture d'ouvrages ou d'articles généraux
en mathématiques ou spécialisés pour sa physique.

Réduction des algorithmes d'assimilation de données ou d'optimisation :
    les algorithmes d'optimisation eux-mêmes peuvent engendrer des coûts de
    calculs importants pour traiter les informations numériques. Diverses
    méthodes permettent de réduire leur coût algorithmique, par exemple en
    travaillant dans l'espace réduit le plus adéquat pour l'optimisation, ou en
    utilisant des techniques d'optimisation multi-niveaux. ADAO dispose de
    telles techniques qui sont incluses dans les variantes d'algorithmes
    classiques, conduisant à des résolutions exactes ou approximées mais
    numériquement plus efficaces. Par défaut, les options algorithmiques
    choisies par défaut dans ADAO sont toujours les plus performantes
    lorsqu'elles n'impactent pas la qualité de l'optimisation.

Réduction de la représentation des covariances :
    dans les algorithmes d'assimilation de données, ce sont les covariances qui
    sont les grandeurs les plus coûteuses à manipuler ou à stocker, devenant
    souvent les quantités limitantes du point de vue du coût de calcul. De
    nombreuses méthodes cherchent donc à utiliser une représentation réduite de
    ces matrices (conduisant parfois mais pas obligatoirement à réduire aussi
    la dimension l'espace d'optimisation). On utilise classiquement des
    techniques de factorisation, de décomposition (spectrale, Fourier,
    ondelettes...) ou d'estimation d'ensemble (EOF...), ou des combinaisons,
    pour réduire la charge numérique de ces covariances dans les calculs. ADAO
    utilise certaines de ces techniques, en combinaison avec des techniques de
    calcul creux ("*sparse*"), pour rendre plus efficace la manipulation des
    matrices de covariance.

Réduction du modèle physique :
    la manière la plus simple de réduire le coût du calcul unitaire consiste à
    réduire le modèle de simulation lui-même, en le représentant de manière
    numériquement plus économique. De nombreuses méthodes permettent cette
    réduction de modèles en assurant un contrôle plus ou moins strict de
    l'erreur d'approximation engendrée par la réduction. L'usage de modèles
    simplifiés de la physique permet une réduction mais sans toujours produire
    un contrôle d'erreur. Au contraire, toutes les méthodes de décomposition
    (Fourier, ondelettes, SVD, POD, PCA, Kahrunen-Loeve, RBM, EIM, etc.) visent
    ainsi une réduction de l'espace de représentation avec un contrôle d'erreur
    explicite. Très fréquemment utilisées, elles doivent néanmoins être
    complétées par une analyse fine de l'interaction avec l'algorithme
    d'optimisation dans lequel le calcul réduit est inséré, pour éviter des
    instabilités, incohérences ou inconsistances notoirement préjudiciables.
    ADAO supporte complètement l'usage de ce type de méthode de réduction, même
    s'il est souvent nécessaire d'établir cette réduction indépendante
    générique préalablement à l'optimisation.

Réduction de l'espace d'assimilation de données ou d'optimisation :
    la taille de l'espace d'optimisation dépend grandement du type de problème
    traité (estimation d'états ou de paramètres) mais aussi du nombre
    d'observations dont on dispose pour conduire l'assimilation de données. Il
    est donc parfois possible de conduire l'optimisation dans l'espace le plus
    petit par une adaptation de la formulation interne des algorithmes
    d'optimisation. Lorsque c'est possible et judicieux, ADAO intègre ce genre
    de formulation réduite pour améliorer la performance numérique sans
    amoindrir la qualité de l'optimisation.

Combinaison de plusieurs réductions :
    de nombreux algorithmes avancés cherchent à combiner simultanément
    plusieurs techniques de réduction. Néanmoins, il est difficile de disposer
    à la fois de méthodes génériques et robustes, et d'utiliser en même temps
    de plusieurs techniques très performantes de réduction. ADAO intègre
    certaines méthodes parmi les plus robustes, mais cet aspect fait toujours
    largement l'objet de recherches et d'évolutions.

On peut terminer ce rapide tour d'horizon des méthodes de réduction en
soulignant que leur usage est omniprésent dans les applications réelles et dans
les outils numériques, et qu'ADAO permet d'utiliser des méthodes éprouvées sans
même le savoir.

.. _section_theory_more_assimilation:

Approfondir le cadre méthodologique de l'assimilation de données
----------------------------------------------------------------

.. index:: single: Ajustement de paramètres
.. index:: single: Apprentissage
.. index:: single: Calage
.. index:: single: Calibration
.. index:: single: Data-driven
.. index:: single: Estimation bayésienne
.. index:: single: Estimation d'état
.. index:: single: Estimation de paramètres
.. index:: single: Intelligence artificielle
.. index:: single: Interpolation de champs
.. index:: single: Interpolation optimale
.. index:: single: Inversion
.. index:: single: Lissage de données
.. index:: single: Machine learning
.. index:: single: Méta-heuristiques
.. index:: single: Méthodes de régularisation
.. index:: single: Optimisation quadratique
.. index:: single: Optimisation variationnelle
.. index:: single: Problèmes inverses
.. index:: single: Recalage
.. index:: single: Réduction de modèles
.. index:: single: Régularisation mathématique

Pour obtenir de plus amples informations sur les techniques d'assimilation de
données, le lecteur peut consulter les documents introductifs comme
[Talagrand97]_ ou [Argaud09]_, des supports de formations ou de cours comme
[Bouttier99]_ et [Bocquet04]_ (ainsi que d'autres documents issus des
applications des géosciences), ou des documents généraux comme [Talagrand97]_,
[Tarantola87]_, [Asch16]_, [Kalnay03]_, [Ide97]_, [Tikhonov77]_ et
[WikipediaDA]_. De manière plus mathématique, on pourra aussi consulter
[Lions68]_, [Jazwinski70]_.

On note que l'assimilation de données n'est pas limitée à la météorologie ou aux
géo-sciences, mais est largement utilisée dans d'autres domaines scientifiques.
Il y a de nombreux champs d'applications scientifiques et technologiques dans
lesquels l'utilisation efficace des données observées, mais incomplètes, est
cruciale.

Certains aspects de l'assimilation de données sont aussi connus sous d'autres
noms. Sans être exhaustif, on peut mentionner les noms de *calage* ou de
*recalage*, de *calibration*, *d'estimation d'état*, *d'estimation de
paramètres*, *d'ajustement de paramètres*, de *problèmes inverses* ou
*d'inversion*, *d'estimation bayésienne*, *d'interpolation de champs* ou
*d'interpolation optimale*, *d'optimisation variationnelle*, *d'optimisation
quadratique*, de *régularisation mathématique*, de *méta-heuristiques*
d'optimisation, de *réduction de modèles*, de *lissage de données*, de pilotage
des modèles par les données (« *data-driven* »), *d'apprentissage* de modèles
et de données (*Machine Learning* et Intelligence Artificielle), etc. Ces
termes peuvent être utilisés dans les recherches bibliographiques.

.. _section_theory_optimization:

Approfondir l'estimation d'état par des méthodes d'optimisation
---------------------------------------------------------------

.. index:: single: Estimation d'état
.. index:: single: Méthodes d'optimisation
.. index:: single: Optimisation locale
.. index:: single: Locale (optimisation)
.. index:: single: Optimisation globale
.. index:: single: Globale (optimisation)
.. index:: single: DerivativeFreeOptimization
.. index:: single: ParticleSwarmOptimization
.. index:: single: DifferentialEvolution
.. index:: single: QuantileRegression
.. index:: single: QualityCriterion

Comme vu précédemment, dans un cas de simulation statique, l'assimilation
variationnelle de données nécessite de minimiser la fonction objectif :math:`J`:

.. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

qui est dénommée la fonctionnelle du "*3D-Var*". Elle peut être vue comme la
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
minima locaux, etc. **Une démarche pour étendre les possibilités d'estimation
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

- *Optimisation sans dérivées (Derivative Free Optimization ou DFO)* (voir :ref:`section_ref_algorithm_DerivativeFreeOptimization`),
- *Optimisation par essaim de particules (Particle Swarm Optimization ou PSO)* (voir :ref:`section_ref_algorithm_ParticleSwarmOptimization`),
- *Évolution différentielle (Differential Evolution ou DE)* (voir :ref:`section_ref_algorithm_DifferentialEvolution`),
- *Régression de quantile (Quantile Regression ou QR)* (voir :ref:`section_ref_algorithm_QuantileRegression`).

En second lieu, les méthodes d'optimisation cherchent usuellement à minimiser
des mesures quadratiques d'erreurs, car les propriétés naturelles de ces
fonctions objectifs sont bien adaptées à l'optimisation classique par gradient.
Mais d'autres mesures d'erreurs peuvent être mieux adaptées aux problèmes de
simulation de la physique réelle. Ainsi, **une autre manière d'étendre les
possibilités d'estimation consiste à utiliser d'autres mesures d'erreurs à
réduire**. Par exemple, on peut citer une *erreur en valeur absolue*, une
*erreur maximale*, etc. On donne précisément ci-dessous les cas les plus
classiques de mesures d'erreurs, en indiquant leur identifiant dans ADAO pour
la sélection éventuelle d'un critère de qualité :

- la fonction objectif pour la mesure d'erreur par moindres carrés pondérés et augmentés (qui est la fonctionnelle de base par défaut de tous les algorithmes en assimilation de données, souvent nommée la fonctionnelle du "*3D-Var*", et qui est connue dans les critères de qualité pour ADAO sous les noms de "*AugmentedWeightedLeastSquares*", "*AWLS*" ou "*DA*") est :

    .. index:: single: AugmentedWeightedLeastSquares (QualityCriterion)
    .. index:: single: AWLS (QualityCriterion)
    .. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

- la fonction objectif pour la mesure d'erreur par moindres carrés pondérés (qui est le carré de la norme pondérée :math:`L^2` de l'innovation, avec un coefficient :math:`1/2` pour être homogène à la précédente, et qui est connue dans les critères de qualité pour ADAO sous les noms de "*WeightedLeastSquares*" ou "*WLS*") est :

    .. index:: single: WeightedLeastSquares (QualityCriterion)
    .. index:: single: WLS (QualityCriterion)
    .. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

- la fonction objectif pour la mesure d'erreur par moindres carrés (qui est le carré de la norme :math:`L^2` de l'innovation, avec un coefficient :math:`1/2` pour être homogène aux précédentes, et qui est connue dans les critères de qualité pour ADAO sous les noms de "*LeastSquares*", "*LS*" ou "*L2*") est :

    .. index:: single: LeastSquares (QualityCriterion)
    .. index:: single: LS (QualityCriterion)
    .. index:: single: L2 (QualityCriterion)
    .. math:: J(\mathbf{x})=\frac{1}{2}(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})=\frac{1}{2}||\mathbf{y}^o-\mathbf{H}.\mathbf{x}||_{L^2}^2

- la fonction objectif pour la mesure d'erreur en valeur absolue (qui est la norme :math:`L^1` de l'innovation, et qui est connue dans les critères de qualité pour ADAO sous les noms de "*AbsoluteValue*" ou "*L1*") est :

    .. index:: single: AbsoluteValue (QualityCriterion)
    .. index:: single: L1 (QualityCriterion)
    .. math:: J(\mathbf{x})=||\mathbf{y}^o-\mathbf{H}.\mathbf{x}||_{L^1}

- la fonction objectif pour la mesure d'erreur maximale (qui est la norme :math:`L^{\infty}` de l'innovation, et qui est connue dans les critères de qualité pour ADAO sous les noms de "*MaximumError*", "*ME*" ou "*Linf*") est :

    .. index:: single: MaximumError (QualityCriterion)
    .. index:: single: ME (QualityCriterion)
    .. index:: single: Linf (QualityCriterion)
    .. math:: J(\mathbf{x})=||\mathbf{y}^o-\mathbf{H}.\mathbf{x}||_{L^{\infty}}

Ces mesures d'erreurs peuvent ne pas être différentiables comme pour les deux
dernières, mais certaines méthodes d'optimisation peuvent quand même les
traiter : heuristiques et méta-heuristiques pour les problèmes à valeurs
réelles, etc. Comme précédemment, les principaux désavantages de ces méthodes
sont un coût numérique souvent bien supérieur pour trouver les estimations
d'états, et pas de garantie de convergence en temps fini. Ici encore, on ne
mentionne que quelques méthodes qui sont disponibles dans ADAO :

- *Optimisation sans dérivées (Derivative Free Optimization ou DFO)* (voir :ref:`section_ref_algorithm_DerivativeFreeOptimization`),
- *Optimisation par essaim de particules (Particle Swarm Optimization ou PSO)* (voir :ref:`section_ref_algorithm_ParticleSwarmOptimization`),
- *Évolution différentielle (Differential Evolution ou DE)* (voir :ref:`section_ref_algorithm_DifferentialEvolution`).

Le lecteur intéressé par le sujet de l'optimisation pourra utilement commencer
sa recherche grâce au point d'entrée [WikipediaMO]_.

.. _section_theory_dynamic:

Approfondir l'assimilation de données pour la dynamique
-------------------------------------------------------

.. index:: single: Dynamique (système)
.. index:: single: Système dynamique
.. index:: single: Evolution temporelle
.. index:: single: EDO (Équation Différentielle Ordinaire)
.. index:: single: ODE (Ordinary Differential Equation)
.. index:: single: EstimationOf

On peut analyser un système en évolution temporelle (dynamique) à l'aide de
l'assimilation de données, pour tenir compte explicitement de l'écoulement du
temps dans l'estimation d'état ou de paramètres. On introduit ici brièvement la
problématique, et certains outils théoriques ou pratiques, pour faciliter le
traitement utilisateur de telles situations. On indique néanmoins que la
variété des problématiques physiques et utilisateur est grande, et qu'il est
donc recommandé d'adapter le traitement aux contraintes, qu'elles soient
physiques, numériques ou informatiques.

Forme générale de systèmes dynamiques
+++++++++++++++++++++++++++++++++++++

Les systèmes en évolution temporelle peuvent être étudiés ou représentés à
l'aide de systèmes dynamiques. Dans ce cas, il est aisé de concevoir l'analyse
de leur comportement à l'aide de l'assimilation de données (c'est même dans ce
cas précis que la démarche d'assimilation de données a initialement été
largement développée).

On formalise de manière simple le cadre de simulation numérique. Un système
dynamique simple sur l'état :math:`\mathbf{x}` peut être décrit en temps
continu sous la forme :

.. math:: \forall t \in \mathbb{R}^{+}, \frac{d\mathbf{x}}{dt} = \mathcal{D}(\mathbf{x},\mathbf{u},t)

où :math:`\mathbf{x}` est le vecteur d'état inconnu, :math:`\mathbf{u}` est un
vecteur de contrôle externe connu, et :math:`\mathcal{D}` l'opérateur
(éventuellement non linéaire) de la dynamique du système. C'est une Équation
Différentielle Ordinaire (EDO, ou ODE en anglais), du premier ordre, sur
l'état. En temps discret, ce système dynamique peut être écrit sous la forme
suivante :

.. math:: \forall n \in \mathbb{N}, \mathbf{x}_{n+1} = M(\mathbf{x}_{n},\mathbf{u}_{n},t_n\rightarrow t_{n+1})

pour une indexation :math:`t_n` des temps discrets avec :math:`n\in\mathbb{N}`.
:math:`M` est l'opérateur d'évolution discret, issu symboliquement de
:math:`\mathcal{D}` par le schéma de discrétisation. Usuellement, on omet la
notation du temps dans l'opérateur d'évolution :math:`M`. L'approximation de
l'opérateur :math:`\mathcal{D}` par :math:`M` introduit (ou ajoute, si elle
existe déjà) une erreur de modèle :math:`\epsilon`.

On peut alors caractériser deux types d'estimation en dynamique, que l'on
décrit ci-après sur le système dynamique en temps discret : `Estimation d'état
en dynamique`_ et `Estimation de paramètres en dynamique`_. Combinés, les deux
types peuvent permettre de faire une `Estimation conjointe d'état et de
paramètres en dynamique`_. Dans ADAO, nombre d'algorithmes peuvent être
utilisés soit en estimation d'état, soit en estimation de paramètres. Cela se
fait simplement en modifiant l'option requise "*EstimationOf*" dans les
paramètres des algorithmes, qui change uniquement la manière dont le contrôle
:math:`\mathbf{u}` est appliqué dans le cas où il n'est explicitement pas
inclus dans :math:`M`.

Estimation d'état en dynamique
++++++++++++++++++++++++++++++

L'estimation d'état peut être conduite par assimilation de données sur la
version en temps discret du système dynamique, écrit sous la forme suivante :

.. math:: \mathbf{x}_{n+1} = M(\mathbf{x}_{n},\mathbf{u}_{n}) + \mathbf{\epsilon}_{n}

.. math:: \mathbf{y}_{n} = H(\mathbf{x}_{n}) + \mathbf{\nu}_{n}

où :math:`\mathbf{x}` est l'état à estimer du système, :math:`\mathbf{x}_{n}`
et :math:`\mathbf{y}_{n}` sont respectivement l'état calculé (non observé) et
mesuré (observé) du système, :math:`M` et :math:`H` sont respectivement les
opérateurs d'évolution incrémentale et d'observation,
:math:`\mathbf{\epsilon}_{n}` et :math:`\mathbf{\nu}_{n}` sont respectivement
les bruits ou erreurs d'évolution et d'observation, et :math:`\mathbf{u}_{n}`
est un contrôle externe connu. Les deux opérateurs :math:`M` et :math:`H` sont
directement utilisables en assimilation de données avec ADAO.

Estimation de paramètres en dynamique
+++++++++++++++++++++++++++++++++++++

L'estimation de paramètres s'écrit un peu différemment pour être conduite par
assimilation de données. Les paramètres à estimer sont dénotés
:math:`\mathbf{a}`. Toujours sur la version en temps discret du système
dynamique, on recherche une correspondance :math:`G` ("mapping") non-linéaire,
paramétrée par :math:`\mathbf{a}`, entre des entrées :math:`\mathbf{x}_{n}` et
des mesures :math:`\mathbf{y}_{n}` à chaque pas :math:`t_n`, l'erreur à
contrôler en fonction des paramètres :math:`\mathbf{a}` étant
:math:`\mathbf{y}_{n}-G(\mathbf{x}_{n},\mathbf{a})`. On peut procéder par
optimisation sur cette erreur, avec régularisation, ou par filtrage en écrivant
le problème représenté en estimation d'état :

.. math:: \mathbf{a}_{n+1} = \mathbf{a}_{n} + \mathbf{\epsilon}_{n}

.. math:: \mathbf{y}_{n} = G(\mathbf{x}_{n},\mathbf{a}_{n}) + \mathbf{\nu}_{n}

où, cette fois, le choix des modèles d'erreurs d'évolution et d'observation
:math:`\mathbf{\epsilon}_{n}` et :math:`\mathbf{\nu}_{n}` conditionne la
performance de la convergence et du suivi des observations (alors que les
représentations d'erreurs proviennent du comportement de la physique dans le
cas de l'estimation d'état). L'estimation des paramètres :math:`\mathbf{a}` se
fait par utilisation de paires :math:`(\mathbf{x}_{n},\mathbf{y}_{n})`
d'entrées et de sorties correspondantes. De plus, les fonctionnelles d'écart
sont posées sur la différence entre l'estimation en entrée et l'estimation en
sortie.

Dans ce cas de l'estimation de paramètres, pour appliquer les méthodes
d'assimilation de données, on impose donc l'hypothèse que l'opérateur
d'évolution est l'identité (*Remarque : il n'est donc pas utilisé, mais doit
être déclaré dans ADAO, sous la forme par exemple d'une matrice à diagonale
unité*), et l'opérateur d'observation est :math:`G`.

Estimation conjointe d'état et de paramètres en dynamique
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Un cas spécial concerne l'estimation conjointe d'état et de paramètres utilisés
dans un système dynamique. On cherche à estimer conjointement l'état
:math:`\mathbf{x}` (qui dépend du temps) et les paramètres :math:`\mathbf{a}`
(qui ici ne dépendent pas du temps). Il existe plusieurs manières de traiter ce
problème, mais la plus générale consiste à utiliser comme ci-dessous un vecteur
d'état augmenté par les paramètres, et à étendre les opérateurs en conséquence.

Pour cela, en utilisant les notations des deux sous-sections précédentes, on
définit la variable auxiliaire :math:`\mathbf{w}` telle que :

.. math:: \mathbf{w} = \left[
    \begin{array}{c}
    \mathbf{x} \\
    \mathbf{a}
    \end{array}
    \right]
    = \left[
    \begin{array}{c}
    \mathbf{w}_{|x} \\
    \mathbf{w}_{|a}
    \end{array}
    \right]

et les opérateurs d'évolution :math:`\tilde{M}` et d'observation
:math:`\tilde{H}` associés au problème augmenté :

.. math:: \tilde{M}(\mathbf{w},\mathbf{u}) = \left[
    \begin{array}{c}
    M(\mathbf{w}_{|x},\mathbf{u}) \\
    \mathbf{w}_{|a}
    \end{array}
    \right]
    = \left[
    \begin{array}{c}
    M(\mathbf{x},\mathbf{u}) \\
    \mathbf{a}
    \end{array}
    \right]

.. math:: \tilde{H}(\mathbf{w}) = \left[
    \begin{array}{c}
    H(\mathbf{w}_{|x}) \\
    G(\mathbf{w}_{|x},\mathbf{w}_{|a})
    \end{array}
    \right]
    = \left[
    \begin{array}{c}
    H(\mathbf{x}) \\
    G(\mathbf{x},\mathbf{a})
    \end{array}
    \right]

Avec ces notations, en étendant les variables de bruit
:math:`\mathbf{\epsilon}` et :math:`\mathbf{\nu}` de manière adéquate, le
problème d'estimation conjointe en temps discret d'état :math:`\mathbf{x}` et
de paramètres :math:`\mathbf{a}`, à travers la variable conjointe
:math:`\mathbf{w}`, s'écrit alors :

.. math:: \mathbf{w}_{n+1} = \tilde{M}(\mathbf{w}_{n},\mathbf{u}_{n}) + \mathbf{\epsilon}_{n}

.. math:: \mathbf{y}_{n} = \tilde{H}(\mathbf{w}_{n}) + \mathbf{\nu}_{n}

avec :math:`\mathbf{w}_{n}=[\mathbf{x}_n~~\mathbf{a}_n]^T`. Les opérateurs
d'évolution incrémentale et d'observation sont donc respectivement les
opérateurs augmentés :math:`\tilde{M}` et :math:`\tilde{H}`, et sont
directement utilisables dans les cas d'études avec ADAO.

Schéma conceptuel pour l'assimilation de données en dynamique
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Pour compléter la description, on peut représenter la démarche d'assimilation
de données de manière spécifiquement dynamique à l'aide d'un schéma temporel,
qui décrit l'action des opérateurs d'évolution (:math:`M` ou :math:`\tilde{M}`)
et d'observation (:math:`H` ou :math:`\tilde{H}`) lors de la simulation et
l'estimation récursive discrète de l'état (:math:`\mathbf{x}`). Une
représentation simple est la suivante, particulièrement adaptée aux algorithmes
itératifs de filtrage de type Kalman :

  .. _schema_d_AD_temporel:
  .. figure:: images/schema_temporel_KF.png
    :align: center
    :width: 100%

    **Schéma temporel d'action des opérateurs pour l'assimilation de données en dynamique**

avec **P** la covariance d'erreur d'état et *t* le temps itératif discret. Dans
ce schéma, l'analyse **(x,P)** est obtenue à travers la "*correction*" par
l'observation de la "*prévision*" de l'état précédent. Une autre manière de
comprendre l'assimilation de données dynamique, en observant les états dans
l'espace des mesures, consiste à représenter sous la forme suivante la même
démarche séquentielle d'assimilation que dans la figure précédente :

  .. _schema_d_AD_sequentiel:
  .. figure:: images/schema_temporel_sequentiel.png
    :align: center
    :width: 100%

    **Schéma séquentiel de l'état et des mesures pour l'assimilation de données en dynamique**

Les concepts décrits dans ce schéma peuvent directement et simplement être
utilisés dans ADAO pour comprendre et construire des cas d'études, et sont
repris dans la description et les exemples de certains algorithmes.
