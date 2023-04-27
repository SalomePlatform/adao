.. index::
    single: Variant
    pair: Variant ; CanonicalPSO
    pair: Variant ; OGCR
    pair: Variant ; SPSO-2011

Variant
  *Predefined name*.  This key allows to choose one of the possible variants
  for the main algorithm. The default variant is the original "CanonicalPSO",
  and the possible choices are
  "CanonicalPSO" (Canonical Particule Swarm Optimisation),
  "OGCR" (Simple Particule Swarm Optimisation),
  "SPSO-2011" (Standard Standard Particle Swarm Optimisation 2011).

  It is recommended to try the "CanonicalPSO" variant with about 100 particles
  for robust performance, and to reduce the number of particules to about 40
  for all variants other than the original "CanonicalPSO" formulation.

  Example :
  ``{"Variant":"CanonicalPSO"}``
