.. index:: single: ResiduFormula

ResiduFormula
  *Nom prédéfini*. Cette clé indique la formule de résidu qui doit être
  utilisée pour le test. Le choix par défaut est "Taylor", et les choix
  possibles sont "Taylor" (résidu du développement de Taylor normalisé de
  l'opérateur, qui doit décroître comme le carré de la perturbation),
  "TaylorOnNorm" (résidu du développement de Taylor rapporté à la perturbation
  de l'opérateur, qui doit rester constant) et "Norm" (résidu obtenu en prenant
  la norme du développement de Taylor à l'ordre 0, qui approxime le gradient,
  et qui doit rester constant).

  Exemple :
  ``{"ResiduFormula":"Taylor"}``
