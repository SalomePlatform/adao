.. index:: single: ExcludeLocations

ExcludeLocations
  *Liste d'entiers ou de noms*. Cette clé indique la liste des points du
  vecteur d'état exclus de la recherche optimale. La valeur par défaut est une
  liste vide. La liste peut contenir soit des **indices de points** (dans
  l'ordre interne implicite d'un vecteur d'état), soit des **noms des points**
  (qui doivent exister dans la liste des noms de positions indiquées par le
  mot-clé "*NameOfLocations*" pour pouvoir être exclus). Par défaut, si les
  éléments de la liste sont des chaînes de caractères assimilables à des
  indices, alors ces chaînes sont bien considérées comme des indices et pas des
  noms.

  Rappel important : la numérotation de ces points exclus doit être identique à
  celle qui est adoptée, implicitement et impérativement, par les variables
  constituant un état considéré arbitrairement sous forme unidimensionnelle.

  Exemple :
  ``{"ExcludeLocations":[3, 125, 286]}`` ou ``{"ExcludeLocations":["Point3", "XgTaC"]}``
