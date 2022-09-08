.. index:: single: FunctionTest (exemple)

Cet exemple décrit le test du bon fonctionnement d'un opérateur quelconque, et
que son appel se déroule de manière compatible avec son usage courant en
parallèle dans les algorithmes d'ADAO. Les information nécessaires sont
minimales, à savoir ici un opérateur :math:`F` (décrit pour le test par la
commande d'observation "*ObservationOperator*"), et un état
:math:`\mathbf{x}^b` sur lequel le tester (décrit pour le test par la commande
"*CheckingPoint*").

Le test est répété un nombre paramétrable de fois, et une statistique finale
permet de vérifier rapidement le bon comportement de l'opérateur. Le diagnostic
le plus simple consiste à vérifier, à la toute fin de l'affichage, l'ordre de
grandeur des valeurs indiquées comme la moyenne des différences entre les
sorties répétées et leur moyenne, sous la partie titrée "*Characteristics of
the mean of the differences between the outputs Y and their mean Ym*". Pour un
opérateur satisfaisant, ces valeurs doivent être proches du zéro numérique.

.. note::

    .. index:: single: EnableMultiProcessingInEvaluation

    Il peut être utile de s'assurer que l'évaluation de l'opérateur est
    réalisée réellement en parallèle, et par exemple qu'il n'y a pas
    d'utilisation forcée d'une accélération du parallélisme, qui éviterait
    ainsi un véritable test parallèle. Pour cela, il est recommandé d'utiliser
    systématiquement le paramètre booléen spécial
    "*EnableMultiProcessingInEvaluation*", exclusivement réservé à cet usage,
    de la commande de déclaration de l'opérateur. L'usage de ce paramètre est
    illustré dans l'exemple présent. Il n'est à utiliser dans aucun autre cas.
