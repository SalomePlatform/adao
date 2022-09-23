.. index:: single: ReducedBasis

ReducedBasis
  *Liste de matrices*. Chaque élément est une matrice, contenant dans chaque
  colonne un vecteur de la base réduite obtenue par la recherche optimale,
  rangés par ordre de préférence décroissante et dans le même ordre que les
  points idéaux trouvés itérativement.

  Exemple :
  ``rb = ADD.get("ReducedBasis")[-1]``
