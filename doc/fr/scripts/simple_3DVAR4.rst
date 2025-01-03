.. index:: single: 3DVAR (exemple)
.. index:: single: Lorenz63
.. _section_usecase_3DVAR4_L63a:

Correction de l'état d'un système dynamique de Lorenz par 3DVAR
...............................................................

Cet exemple prolonge les cas simples d'usage de l'algorithme 3DVAR (voir la
partie :ref:`Exemples avec l'algorithme de
"3DVAR"<section_ref_algorithm_3DVAR_examples>`, ou un exemple similaire dans
[Asch16]_). Il décrit l'effet d'une assimilation de données sur la prévision
temporelle d'un système dynamique. C'est un cas très simplifié qui illustre une
démarche classique en météorologie (prévision du temps à court terme, en-deçà
de la quinzaine de jours) ou en prévision saisonnière (prévision du temps à
plus long terme, au-delà de la quinzaine de jours).

On utilise ici un modèle simple classique de système dynamique, nommé *système
de Lorenz*, *oscillateur de Lorenz*, *Lorenz3D* ou *Lorenz63* d'après le nom de
son auteur, le mathématicien et météorologue Edward Lorenz ([Lorenz63]_,
[WikipediaL63]_). Il est disponible dans les modèles de tests intégrés d'ADAO
sous le nom ``Lorenz1963``.

Ce système dynamique tridimensionnel non-linéaire est un modèle extrêmement
simplifié des équations de Navier-Stokes, en vue d'étudier le couplage de
l'atmosphère et de l'océan, dans une configuration physique particulière de
convection (convection de Rayleigh-Bénard). Il présente un comportement de
chaos déterministe, ce qui signifie que le système dynamique est déterministe
(du point de vue continu ou discret), mais que sa sensibilité aux conditions
initiales ou aux paramètres permet d'obtenir au bout d'un temps fini une
trajectoire arbitrairement différente pour de petites variations de ses
conditions initiales. Ce système est connu pour être à l'origine de la notion
d'effet papillon [Butterfly72]_ et pour l'illustration qu'il en donne.

Ce système est dépendant de ses conditions initiales et de 3 paramètres
physiques :math:`(\sigma,\rho,\beta)`. Les équations classiques pour l'état
:math:`u=(x,y,z)` le décrivant sont :

.. math:: \left\{
    \begin{array}{lcl}
    \displaystyle\frac{dx}{dt} & = & \sigma (y - x)\\~\\
    \displaystyle\frac{dy}{dt} & = & \rho\, x - y - x\, z\\~\\
    \displaystyle\frac{dz}{dt} & = & x\, y - \beta\, z
    \end{array}
    \right.

avec le temps :math:`t\in{I\!R}^+`, et avec :math:`\sigma=10`, :math:`\rho=28`,
:math:`\beta=8/3` des valeurs courantes de paramètres caractérisant un état
chaotique. La condition initiale est quelconque.

La figure suivante illustre l'attracteur de Lorenz par la simulation directe de
ce système dynamique, que l'on représente ici pour :math:`t\in[0,40]` et avec
la condition initiale :math:`(0,1,0)`. L'attracteur est la structure qui
correspond au comportement long terme de l'oscillateur de Lorenz, qui se
présente donc ici comme deux "*ailes de papillon*". La figure montre que la
variable d'état :math:`u=(x,y,z)` de ce système dynamique évolue sur une
trajectoire déterministe non périodique, qui s'enroule sur une aile du papillon
pour ensuite "*sauter*" sur l'autre aile, et ainsi de suite de façon en
apparence erratique. La figure ci-dessous présente une unique trajectoire,
colorée de manière différente pour sa première moitié et sa seconde moitié pour
illustrer les enroulements et sauts successifs.

.. _simple_3DVAR4Plus01:
.. image:: scripts/simple_3DVAR4Plus01.png
  :align: center
  :width: 90%

Si on observe la même trajectoire en traçant séparément les 3 composantes de
l'état du système, avec les mêmes paramètres de simulation, on obtient la
figure suivante :

.. _simple_3DVAR4Plus02:
.. image:: scripts/simple_3DVAR4Plus02.png
  :align: center
  :width: 90%

En remarquant bien que les amplitudes et temporalités des deux premières
composantes :math:`x` et :math:`y` ne sont effectivement pas identiques, malgré
leur ressemblance, cette figure illustre la propriété de chaos par une absence
de régularité spatiale et temporelle.

**Pour illustrer la démarche d'analyse, on se place pour la suite en
expériences jumelles** (voir la partie :ref:`section_methodology_twin`).

On choisit ici de **perturber uniquement l'état initial de la simulation**, en
utilisant la valeur d'ébauche :math:`u^b=[2,3,4]`, dont les effets sont à
comparer à ceux de l'état initial, dit *idéal* ou *vrai*, non perturbé, valant
:math:`u^t=[1,1,1]`.

Le modèle est considéré comme parfait, et il est observé sur l'intervalle
temporel [0,2]. Les pseudo-observations :math:`\mathbf{y}^o` sont au nombre de
10, construites par échantillonnage au pas de temps :math:`\delta t=0.2` sur
cet intervalle temporel, sur la base d'une simulation depuis l'état initial non
perturbé :math:`u^t=[1,1,1]`. A ces valeurs exactes échantillonnées est ensuite
ajouté, sur chaque composante, un bruit gaussien d'amplitude
:math:`\sigma_m=0.15` pour obtenir une pseudo-observation. L'ordre de grandeur
du bruit est celui du bruit expérimental de mesure de variables réelles
correspondant au modèle simplifié de Lorenz.

La figure suivante illustre sur la première variable (les autres sont
similaires) ces différentes informations réparties sur l'intervalle temporel
[0,2] de mesure :

.. _simple_3DVAR4Plus03:
.. image:: scripts/simple_3DVAR4Plus03.png
  :align: center
  :width: 90%

.. note::

    On insiste fortement sur le fait que les observations successives ne sont
    pas disponibles simultanément, à l'instant initial par exemple, mais
    qu'elles sont disponibles à chaque fois que la simulation atteint l'un des
    instants de mesure. On rappelle de plus que la courbe de simulation bleue
    en pointillés, obtenue à partir de l'état idéal ou vrai
    :math:`u^t=[1,1,1]`, est inconnue en dehors d'expériences jumelles. Seules
    les trajectoires tracées comme continues sont connues par simulation.

Sous forme numérique, les valeurs d'observations sont les suivantes :

.. literalinclude:: scripts/simple_3DVAR4Observations.csv

L'assimilation de données est ensuite utilisée pour corriger la trajectoire
initiale d'ébauche du système à chaque nouvelle observation acquise. A chaque
étape :math:`n`, l'état courant prévu :math:`\mathbf{u}^f_n` est modifié pour
produire un nouvel **état analysé** :math:`\mathbf{u}^a_n`, tenant compte de
cette nouvelle information :math:`\mathbf{y}^o_n`, puis la simulation se
poursuit à partir de ce nouvel état. L'assimilation des observations se produit
grâce au simple script ADAO ci-dessous. Pour une meilleure lisibilité, le
script présente de manière explicite la boucle temporelle sur les observations
:

.. literalinclude:: scripts/simple_3DVAR4.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_3DVAR4.res
    :language: none

La figure suivante illustre alors, sur la première variable, les **états
prévus, mesurés et analysés** à chaque pas d'observation, ainsi que les états
simulés par le modèle entre deux observations. Les ruptures temporelles de la
trajectoire proviennent par nature de chaque opération d'assimilation avec une
nouvelle information observée.

.. _simple_3DVAR4Plus06:
.. image:: scripts/simple_3DVAR4Plus06.png
  :align: center
  :width: 90%

On constate clairement que l'état prévu :math:`\mathbf{u}^f_n` est de plus en
plus conforme à chaque pseudo-observation :math:`\mathbf{y}^o_n`, et que chaque
portion de trajectoire prévue est de plus en plus proche de la trajectoire
idéale inconnue issue de l'état vrai :math:`\mathbf{u}^t`. Dans la figure
suivante, la mesure classique des écarts par RMSE (*Root-Mean-Square Error*)
décrit de manière similaire cette amélioration itérative des prévisions et des
analyses intégrant l'information d'observations.

.. _simple_3DVAR4Plus09:
.. image:: scripts/simple_3DVAR4Plus09.png
  :align: center
  :width: 90%

On peut aussi comparer les prévisions d'état obtenues sur l'intervalle temporel
[2,10], qui se situe au-delà de la fenêtre d'observation concernée
par la démarche d'assimilation de données. On dispose de trois manières
d'établir cette simulation temporelle après l'instant :math:`t=2` :

- on peut calculer la prévision issue de l'état à :math:`t=2` obtenu lui-même
  par simulation à partir de l'état initial perturbé d'ébauche
  :math:`u^b=[2,3,4]` à l'instant :math:`t=0`, prévision dans laquelle on
  n'utilise que l'information d'ébauche ;
- on peut calculer la prévision issue de l'état à :math:`t=2` obtenu lui-même
  par simulation à partir de l'état initial non perturbé (*état idéal* ou *état
  vrai*) :math:`u^t=[1,1,1]`, qui est considéré comme la référence mais connue
  uniquement à travers les observations issues de l'échantillonnage avec bruit
  ;
- on peut calculer la prévision issue de l'analyse par assimilation de données,
  qui provient de la correction d'état par les observations.

Ces trois manières de faire sont illustrées sur la figure suivante, où l'on a
rappelé la fenêtre d'assimilation sur l'intervalle temporel [0,2] et où
les prévisions sont établies sur l'intervalle temporel [2,10] :

.. _simple_3DVAR4Plus12:
.. image:: scripts/simple_3DVAR4Plus12.png
  :align: center
  :width: 90%

Il est manifeste que la prévision issue de l'analyse :math:`\mathbf{u}^a`,
obtenue par assimilation de données à l'instant :math:`t=2`, est beaucoup plus
conforme à la simulation :math:`\mathbf{u}^t` idéale choisie pour l'expérience
jumelle, que la prévision issue de l'ébauche :math:`\mathbf{u}^b` simulée à
:math:`t=2`. Même si la prolongation temporelle de la simulation conduit
obligatoirement à un écart avec l'état vrai qui s'accroît, à cause de la
propriété chaotique du système de Lorenz, la correction par assimilation de
données permet d'obtenir une prévision acceptable sur une durée beaucoup plus
longue que l'absence de correction intrinsèquement présente dans la simulation
issue de l'ébauche.
