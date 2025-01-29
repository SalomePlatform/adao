.. index:: single: SwarmInitialization

SwarmInitialization
  *Nom prédéfini*. Le nom défini le mode d'initialisation de l'essaim de
  particules pour l'algorithme "*ParticleSwarmOptimization*". La série des
  particules est initialisée en spécifiant la distribution par composante, qui
  peut être identique pour toutes les composantes (c'est le cas des valeurs
  "UniformByComponents" ou "LogUniformByComponents"), ou spécifique par
  composante avec "DistributionByComponents". Dans ce dernier cas, il faut par
  ailleurs spécifier le contenu du mot-clé "DistributionByComponents". La
  valeur par défaut est "UniformByComponents".

  Le nom possible est donc dans la liste suivante :
  ["UniformByComponents",
  "LogUniformByComponents",
  "DistributionByComponents"].

  Exemple :
  ``{"SwarmInitialization":"UniformByComponents"}``
