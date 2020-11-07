.. index:: single: StandardDeviation

StandardDeviation
  *Liste de valeurs réelles*. Cette clé indique, uniquement dans le cas d'une
  distribution de type "Gaussian" demandée par le mot-clé
  "*NoiseDistribution*", l'écart-type des perturbations gaussiennes d'état pour
  chaque composante de l'état. Le défaut est une liste vide, cette clé doit
  donc obligatoirement être renseignée dans le cas d'une distribution
  "Gaussian". Une manière simple de le faire est de donner une liste de la
  longueur de l'état recherché avec des écart-types identiques, comme dans
  l'exemple ci-dessous avec des demi-amplitudes de 5%. Il est conseillé de
  prendre des écart-types de quelques pourcents au maximum.

  Exemple :
  ``{"StandardDeviation":<longueur de l'état>*[0.05]}``
