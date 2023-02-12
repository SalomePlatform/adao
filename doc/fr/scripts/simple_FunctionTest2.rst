Deuxième exemple
................

Ce nouvel exemple décrit le test du bon fonctionnement d'un opérateur
quelconque nommé ``QuadFunction``, disponible sous forme fonctionnelle. Il est
définit par la commande "*ObservationOperator*" selon la
:ref:`section_ref_operator_one`. Par la commande "*CheckingPoint*", on ajoute
aussi un état particulier :math:`\mathbf{x}` sur lequel tester l'opérateur.

Ce test est répété ici 15 fois, et une statistique finale permet de vérifier
rapidement le bon comportement de l'opérateur. Le diagnostic le plus simple
consiste à vérifier, à la toute fin de l'affichage, l'ordre de grandeur des
variations des valeurs indiquées comme la moyenne des différences entre les
sorties répétées et leur moyenne, sous la partie titrée "*Characteristics of
the mean of the differences between the outputs Y and their mean Ym*". Pour
qu'un opérateur soit satisfaisant, ces valeurs doivent être proches du zéro
numérique.
