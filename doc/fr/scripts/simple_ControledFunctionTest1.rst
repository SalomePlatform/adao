.. index:: single: ControledFunctionTest (exemple)

Premier exemple
...............

Cet exemple décrit le test du bon fonctionnement d'un opérateur quelconque, et
que son appel se déroule de manière compatible avec son usage courant dans les
algorithmes d'ADAO. Les informations nécessaires sont minimales, à savoir ici
un opérateur (décrit pour le test par la commande d'observation
"*ObservationOperator*"), un état particulier :math:`\mathbf{x}` sur lequel le
tester (décrit pour le test par la commande "*CheckingPoint*") et un contrôle
:math:`\mathbf{u}` (décrit pour le test par la commande "*ControlInput*"), les
deux n'étant pas nécessairement de la même taille.

Le test est répété un nombre paramétrable de fois, et une statistique finale
permet de vérifier rapidement le bon comportement de l'opérateur. Le diagnostic
le plus simple consiste à vérifier, à la toute fin de l'affichage, l'ordre de
grandeur des variations des valeurs indiquées comme la moyenne des différences
entre les sorties répétées et leur moyenne, sous la partie titrée
"*Characteristics of the mean of the differences between the outputs Y and
their mean Ym*". Pour un opérateur satisfaisant, ces valeurs doivent être
proches du zéro numérique.
