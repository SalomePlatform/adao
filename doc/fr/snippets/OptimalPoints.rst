.. index:: single: OptimalPoints

OptimalPoints
  *Liste de série d'entiers*. Chaque élément est une série, contenant les
  indices des positions idéales ou points optimaux auxquels une mesure est
  requise, déterminés par la recherche optimale, rangés par ordre de préférence
  décroissante et dans le même ordre que les vecteurs trouvés itérativement
  pour constituer la base réduite.

  Exemple :
  ``op = ADD.get("OptimalPoints")[-1]``
