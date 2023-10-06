.. index:: single: SingularValues

SingularValues
  *Liste de série de valeurs réelles*. Chaque élément est une série, contenant
  les valeurs singulières obtenues par une décomposition SVD d'un ensemble de
  vecteurs d'états complets. Le nombre de valeurs singulières retenues n'est
  pas limité par la taille de la base réduite demandée.

  Exemple :
  ``sv = ADD.get("SingularValues")[-1]``
