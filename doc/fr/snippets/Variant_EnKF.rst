.. index::
    single: Variant
    pair: Variant ; EnKF
    pair: Variant ; ETKF
    pair: Variant ; ETKF-N
    pair: Variant ; MLEF
    pair: Variant ; IEnKF
    pair: Variant ; E3DVAR
    pair: Variant ; EnKS

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est la formulation "EnKF"
  d'origine, et les choix possibles sont
  "EnKF" (Ensemble Kalman Filter),
  "ETKF" (Ensemble-Transform Kalman Filter),
  "ETKF-N" (Ensemble-Transform Kalman Filter),
  "MLEF" (Maximum Likelihood Kalman Filter),
  "IEnKF" (Iterative_EnKF),
  "E3DVAR" (EnKF 3DVAR),
  "EnKS" (Ensemble Kalman Smoother).

  Il est conseillé d'essayer les variantes "ETKF-N" ou "IEnKF" pour une
  performance robuste, et de réduire le nombre de membres à une dizaine ou
  moins pour toutes les variantes autres que la formulation "EnKF" originale.

  Exemple :
  ``{"Variant":"EnKF"}``
