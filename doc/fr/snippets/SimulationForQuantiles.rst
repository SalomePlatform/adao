.. index:: single: SimulationForQuantiles

SimulationForQuantiles
  Cette clé indique le type de simulation, linéaire (avec l'opérateur
  d'observation tangent appliqué sur des incréments de perturbations autour de
  l'état optimal) ou non-linéaire (avec l'opérateur d'observation standard
  appliqué aux états perturbés), que l'on veut faire pour chaque perturbation.
  Cela change essentiellement le temps de chaque simulation élémentaire,
  usuellement plus long en non-linéaire qu'en linéaire. Cette option n'est
  utile que si le calcul supplémentaire "SimulationQuantiles" a été choisi. La
  valeur par défaut est "Linear", et les choix possibles sont "Linear" et
  "NonLinear".

  Exemple :
  ``{"SimulationForQuantiles":"Linear"}``
