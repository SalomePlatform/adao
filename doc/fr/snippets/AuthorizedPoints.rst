.. index:: single: AuthorizedPoints

AuthorizedPoints
  *Liste de série d'entiers*. Chaque élément est une série, contenant les
  indices des points autorisés de la recherche optimale, selon l'ordre des
  variables d'un vecteur d'état considéré arbitrairement sous forme
  unidimensionnelle. Dans un cas par défaut où tous les points sont
  implicitement autorisés, la série est vide.

  Exemple :
  ``ep = ADD.get("AuthorizedPoints")[-1]``
