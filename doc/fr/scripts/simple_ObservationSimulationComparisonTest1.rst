.. index:: single: ObservationSimulationComparisonTest (exemple)

Cet exemple permet d'analyser le lancement (répété) d'un opérateur de
simulation :math:`\mathbf{F}` explicitement donné sous forme matricielle
(décrit pour le test par la commande d'observation "*ObservationOperator*"),
appliqué à un état particulier :math:`\mathbf{x}` sur lequel le tester (décrit
pour le test par la commande "*CheckingPoint*"), comparé à des mesures
:math:`\mathbf{y}` (décrit pour le test par la commande "*Observation*") par la
différence OMB = y - F(x) (Observation minus evaluation at Background) et la
fonction de coût standard d'assimilation des données J.

Le test est répété un nombre paramétrable de fois, et une statistique finale
permet de vérifier rapidement le bon comportement de l'opérateur. Le diagnostic
le plus simple consiste à vérifier, à la toute fin de l'affichage, l'ordre de
grandeur des variations des valeurs indiquées comme la moyenne des différences
entre les sorties répétées et leur moyenne, sous la partie titrée "*Launching
statistical summary calculation for 5 states*". Pour un opérateur satisfaisant,
les valeurs de différences à la moyenne et les écarts-types doivent être
proches du zéro numérique.
