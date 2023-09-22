.. index:: single: ReducedBasis

ReducedBasis
  *Liste de matrices*. Chaque élément est une matrice, contenant dans chaque
  colonne un vecteur de la base réduite obtenue par la recherche optimale,
  rangés par ordre de préférence décroissante, et dans le même ordre que les
  points idéaux trouvés itérativement.

  Lorsque c'est une donnée d'entrée, elle est identique à une sortie unique
  d'un :ref:`section_ref_algorithm_MeasurementsOptimalPositioningTask`.

  Exemple :
  ``rb = ADD.get("ReducedBasis")[-1]``
