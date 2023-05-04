.. index:: single: SwarmTopology

SwarmTopology
  *Nom prédéfini*. Cette clé indique la manière dont les particules (ou
  insectes) se communiquent des informations lors de l'évolution de l'essaim
  particulaire. La méthode la plus classique consiste à échanger des
  informations entre toutes les particules (nommée "gbest" ou
  "FullyConnectedNeighborhood"). Mais il est souvent plus efficace d'échanger
  des informations sur un voisinage réduit, comme dans la méthode classique
  "lbest" (ou "RingNeighborhoodWithRadius1") échangeant des informations avec
  les deux particules voisines dans l'ordre de numérotation (la précédente et
  la suivante), ou la méthode "RingNeighborhoodWithRadius2" échangeant avec les
  4 voisins (les deux précédents et les deux suivants). Une variante de
  voisinage réduit consiste à échanger avec 3 voisins (méthode
  "AdaptativeRandomWith3Neighbors") ou 5 voisins (méthode
  "AdaptativeRandomWith5Neighbors") choisis aléatoirement (la particule pouvant
  être tirée plusieurs fois). La valeur par défaut est
  "FullyConnectedNeighborhood", et il est conseillé de la changer avec prudence
  en fonction des propriétés du système physique simulé. La topologie de
  communication possible est à choisir dans la liste suivante, dans laquelle
  les noms équivalents sont indiqués par un signe "<=>" :
  ["FullyConnectedNeighborhood" <=> "FullyConnectedNeighbourhood" <=> "gbest",
  "RingNeighborhoodWithRadius1" <=> "RingNeighbourhoodWithRadius1" <=> "lbest",
  "RingNeighborhoodWithRadius2" <=> "RingNeighbourhoodWithRadius2",
  "AdaptativeRandomWith3Neighbors" <=> "AdaptativeRandomWith3Neighbours" <=> "abest",
  "AdaptativeRandomWith5Neighbors" <=> "AdaptativeRandomWith5Neighbours"].

  Exemple :
  ``{"SwarmTopology":"FullyConnectedNeighborhood"}``
