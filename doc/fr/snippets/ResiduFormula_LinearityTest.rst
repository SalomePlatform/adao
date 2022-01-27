.. index:: single: ResiduFormula

ResiduFormula
  *Nom prédéfini*. Cette clé indique la formule de résidu qui doit être
  utilisée pour le test. Le choix par défaut est "CenteredDL", et les choix
  possibles sont "CenteredDL" (résidu de la différence entre la fonction au
  point nominal et ses valeurs avec des incréments positif et négatif, qui doit
  rester très faible), "Taylor" (résidu du développement de Taylor de
  l'opérateur normalisé par sa valeur nominal, qui doit rester très faible),
  "NominalTaylor" (résidu de l'approximation à l'ordre 1 de l'opérateur,
  normalisé au point nominal, qui doit rester proche de 1), et
  "NominalTaylorRMS" (résidu de l'approximation à l'ordre 1 de l'opérateur,
  normalisé par l'écart quadratique moyen (RMS) au point nominal, qui doit
  rester proche de 0).

  Exemple :
  ``{"ResiduFormula":"CenteredDL"}``
