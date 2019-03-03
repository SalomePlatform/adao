.. index:: single: NoiseHalfRange

NoiseHalfRange
  Cette clé indique, uniquement dans le cas d'une distribution de type
  "Uniform" demandée par le mot-clé "*NoiseDistribution*", la demi-amplitude
  des perturbations uniformes centrées d'état pour chaque composante de l'état.
  Le défaut est une liste vide, cette clé doit donc obligatoirement être
  renseignée dans le cas d'une distribution "Uniform". Une manière simple de le
  faire est de donner une liste de la longueur de l'état recherché et de
  demi-amplitudes identiques, comme dans l'exemple ci-dessous avec des
  demi-amplitudes de 3%. Il est conseillé de prendre des demi-amplitudes de
  quelques pourcents au maximum.

  Exemple :
  ``{"NoiseHalfRange":<longueur de l'état>*[0.03]}``
