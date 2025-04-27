.. index::
    single: Variant
    pair: Variant ; CanonicalPSO
    pair: Variant ; OGCR
    pair: Variant ; SPSO-2011

Variant
  *Nom prédéfini*. Cette clé permet de choisir l'une des variantes possibles
  pour l'algorithme principal. La variante par défaut est la formulation
  "CanonicalPSO" d'origine, et les choix possibles sont
  "CanonicalPSO" (Canonical Particle Swarm Optimization),
  "OGCR" (Simple Particle Swarm Optimization),
  "SPSO-2011" (Standard Standard Particle Swarm Optimization 2011)
  ou
  "SPSO-2011-AIS" (Standard Standard Particle Swarm Optimisation 2011 with Asynchronous Iteration Strategy),
  "SPSO-2011-SIS" (Standard Particle Swarm Optimisation 2011 with Synchronous Iteration Strategy),
  "SPSO-2011-PSIS" (Standard Particle Swarm Optimisation 2011 with Parallel Synchronous Iteration Strategy).

  Il est conseillé d'essayer la variante "CanonicalPSO" avec une centaine de
  particules pour une performance robuste, et de réduire le nombre de
  particules à une quarantaine pour toutes les variantes autres que la
  formulation "CanonicalPSO" originale.

  Exemple :
  ``{"Variant":"CanonicalPSO"}``
