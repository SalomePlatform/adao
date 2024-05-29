.. index:: single: MeasurementsOptimalPositioningTask (exemple)

Troisième exemple
.................

Cet exemple plus complet décrit le positionnement optimal de mesures associé à
une décomposition réduite de type DEIM sur une fonction classique paramétrique
non-linéaire, telle que proposée dans la référence [Chaturantabut10]_. Cette
fonction particulière a l'avantage notable de n'être dépendante que d'une
position :math:`x` en 2D et d'un paramètre :math:`\mu` en 2D aussi. Elle permet
donc une illustration pédagogique pour représenter les points optimaux de
mesure.

Cette fonction dépend de la position :math:`x=(x_1,x_2)\in\Omega=[0.1,0.9]^2`
dans le plan 2D, et du paramètre
:math:`\mu=(\mu_1,\mu_2)\in\mathcal{D}=[-1,-0.01]^2` de dimension 2 :

.. math:: G(x;\mu) = \frac{1}{\sqrt{(x_1 - \mu_1)^2 + (x_2 - \mu_2)^2 + 0.1^2}}

La fonction est représenté sur une grille spatiale régulière :math:`\Omega_G`
de taille 20x20 points. Elle est disponible dans les modèles de tests intégrés
pour ADAO sous le nom ``TwoDimensionalInverseDistanceCS2010``. On construit
donc ici tout d'abord un ensemble de simulations de :math:`G`, puis on cherche
les meilleurs positions de mesures pour obtenir une représentation par
interpolation DEIM des champs, en appliquant l'algorithme de décomposition de
type DEIM, et on en tire ensuite des illustrations simples. On choisit de
rechercher un nombre arbitraire ``nbmeasures`` de 15 positions de mesures.

On observe ainsi que les valeurs singulières décroissent régulièrement jusqu'au
bruit numérique, indiquant qu'il faut environ une centaine d'éléments de base
pour complètement représenter l'information contenue dans l'ensemble des
simulations de :math:`G`. Par ailleurs, les points de mesure optimaux dans le
domaine :math:`\Omega_G` sont répartis de manière inhomogène, privilégiant la
zone spatiale proche du coin :math:`(0.1,0.1)` dans laquelle la fonction
:math:`G` varie plus.
