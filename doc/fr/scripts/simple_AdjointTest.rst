.. index:: single: AdjointTest (exemple)

Cet exemple décrit le test de la qualité de l'adjoint d'un opérateur
quelconque, dont la formulation directe est donnée et dont la formulation
adjointe est ici approximée par défaut. Les informations nécessaires sont
minimales, à savoir ici un opérateur :math:`F` (décrit pour le test par la
commande d'observation "*ObservationOperator*"), et un état
:math:`\mathbf{x}^b` sur lequel le tester (décrit pour le test par la commande
"*CheckingPoint*"). Une observation :math:`\mathbf{y}^o` peut être donnée comme
ici (décrit pour le test par la commande "*Observation*"). On a paramétré la
sortie pour fixer l'impression, par exemple pour faciliter la comparaison
automatique.

La vérification pratique consiste à observer si le résidu est constamment égal
à zéro à la précision du calcul.
