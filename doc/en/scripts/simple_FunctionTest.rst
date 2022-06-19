.. index:: single: FunctionTest (exemple)

Cet exemple décrit le test du bon fonctionnement d'un opérateur et que son
appel se déroule de manière compatible avec son usage dans les algorithmes
d'ADAO. Les information nécessaires sont minimales, à savoir ici un opérateur
de type observation :math:`H` et un état :math:`\mathbf{x}^b` sur lequel le
tester (nommé "*CheckingPoint*" pour le test).

Le test est répété un nombre paramétrable de fois, et une statistique finale
permet de vérifier rapidement le bon comportement de l'opérateur. Le diagnostic
le plus simple consiste à vérifier, à la fin, l'ordre de grandeur des valeurs
indiquées comme la moyenne des différences entre les sorties répétées et leur
moyenne ("*mean of the differences between the outputs Y and their mean Ym*").
Pour un opérateur normal, ces valeurs doivent être proches du zéro numérique.


