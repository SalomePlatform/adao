.. index::
    single: Variant
    pair: Variant ; 3DVAR
    pair: Variant ; ExtendedBlue
    pair: Variant ; DerivativeFreeOptimization
    pair: Variant ; CanonicalPSO
    pair: Variant ; SPSO-2011-AIS-VLS
    pair: Variant ; 3DVARGradientOptimization
    pair: Variant ; ExtendedBlueOptimization
    pair: Variant ; DerivativeFreeOptimization
    pair: Variant ; CanonicalParticuleSwarmOptimization
    pair: Variant ; VariationalParticuleSwarmOptimization

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal de calage de paramètres. La variante par défaut
  est le "3DVAR" d'origine, et les choix possibles sont
  "3DVARGradientOptimization" ou "3DVAR" (analyse variationnelle de type 3DVAR),
  "ExtendedBlueOptimization" ou "ExtendedBlue" (estimation semi-linéaire de type BLUE),
  "DerivativeFreeOptimization" ou "DFO" (optimisation sans dérivées par approximation de type simplexe ou autres),
  "CanonicalParticuleSwarmOptimization" ou "CanonicalPSO" ou "PSO" (optimisation canonique par essaim particulaire),
  "VariationalParticuleSwarmOptimization" ou "SPSO-2011-AIS-VLS" (optimisation standard 2011 par essaim particulaire, avec accélération par recherche variationnelle locale),
  Il est fortement recommandé de conserver la valeur par défaut.

  Exemple :
  ``{"Variant":"3DVAR"}``
