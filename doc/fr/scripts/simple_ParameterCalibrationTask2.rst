.. index:: single: ParameterCalibrationTask (exemple)

Second exemple
..............

Comme il est aisé de changer de méthode d'optimisation, l'objet de ce second
exemple est de réaliser la calibration de paramètres à l'aide d'une
optimisation sans dérivées. Elle est indiquée à cet algorithme par la variante
"DerivativeFreeOptimization" (accompagnée d'un changement de l'optimiseur par
le mot-clé "Minimizer"). Seuls les valeurs de ces deux mot-clés "Variant" et
"Minimizer" changent donc entre les deux approches.

Dans ce cas extrêmement simple de petite dimension et sans difficulté, les
paramètres de contrôle restent les mêmes. Les résultats sont de la même qualité
que pour l'optimisation variationnelle de référence.
