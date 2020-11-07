.. index:: single: ShowInformationOnlyFor

ShowInformationOnlyFor
  *Liste de noms prédéfinis*. Cette clé indique la liste des noms de vecteurs
  dont les informations synthétiques (taille, min/max...) sont à imprimer, la
  valeur par défaut étant l'ensemble des vecteurs. Si le vecteur nommé n'est
  pas une entrée fournie, le nom est simplement ignoré. Cela permet de
  restreindre les impressions synthétiques. Les noms possibles sont dans la
  liste suivante : [
  "Background",
  "CheckingPoint",
  "Observation",
  ].

  Exemple :
  ``{"ShowInformationOnlyFor":["Background"]}``
