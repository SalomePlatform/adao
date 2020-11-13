.. index:: single: Blue (exemple)

Cet exemple décrit l'interpolation entre deux états physiques. Ces deux champs
vectoriels, de discrétisation identique, sont l'observation
:math:`\mathbf{y}^o` et l'état d'ébauche a priori :math:`\mathbf{x}^b`. Les
confiances dans les erreurs sur les deux informations sont considérées comme
identiques. Le modèle :math:`H` observe complètement le champ disponible, c'est
un opérateur de sélection matriciel.

Le champ interpolé résultant est simplement le "milieu" entre les deux champs,
avec une confiance améliorée sur les erreurs.
