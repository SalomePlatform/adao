Deuxième exemple
................

Ce nouvel exemple décrit le test du bon fonctionnement d'un opérateur
quelconque nommé ``ControledQuadFunction``, disponible sous forme
fonctionnelle. Il est défini par la commande "*ObservationOperator*" selon la
:ref:`section_ref_operator_funcs` (ici, même avec cette forme fonctionnelle, on
peut exceptionnellement ne pas définir les formes tangente et adjointe de
l'opérateur car elles ne sont pas utiles dans ce test). Par la commande
"*CheckingPoint*", on ajoute aussi un état particulier :math:`\mathbf{x}` sur
lequel tester l'opérateur, et par la commande "*ControlInput*" on ajoute un
contrôle fixe :math:`\mathbf{u}`.

Ce test est arbitrairement répété ici 15 fois, et une statistique finale permet
de vérifier rapidement le bon comportement de l'opérateur. Le diagnostic le
plus simple consiste à vérifier, à la toute fin de l'affichage, l'ordre de
grandeur des variations des valeurs indiquées comme la moyenne des différences
entre les sorties répétées et leur moyenne, sous la partie titrée
"*Characteristics of the mean of the differences between the outputs Y and
their mean Ym*". Pour qu'un opérateur soit satisfaisant, ces valeurs doivent
être proches du zéro numérique.
