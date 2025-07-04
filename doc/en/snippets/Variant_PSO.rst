.. index::
    single: Variant
    pair: Variant ; CanonicalPSO
    pair: Variant ; OGCR
    pair: Variant ; SPSO-2011

Variant
  *Predefined name*. This key allows to choose one of the possible variants for
  the main algorithm. The default variant is the original "CanonicalPSO", and
  the possible choices are
  "CanonicalPSO" (Canonical Particle Swarm Optimization),
  "OGCR" (Simple Particle Swarm Optimization),
  "SPSO-2011" (Standard Standard Particle Swarm Optimization 2011)
  identical to
  "SPSO-2011-AIS" (Standard Standard Particle Swarm Optimisation 2011 with Asynchronous Iteration Strategy),
  "SPSO-2011-SIS" (Standard Particle Swarm Optimisation 2011 with Synchronous Iteration Strategy),
  "SPSO-2011-PSIS" (Standard Particle Swarm Optimisation 2011 with Parallel Synchronous Iteration Strategy).
  The local accelerated "VLS" (Variational Local Search) versions are obtained
  by adding the suffix "-VLS" to each method:
  "CanonicalPSO-VLS",
  "OGCR-VLS",
  "SPSO-2011-AIS-VLS",
  "SPSO-2011-SIS-VLS",
  "SPSO-2011-PSIS-VLS".

  It is recommended to try the "CanonicalPSO" variant with about 100 particles
  for robust performance, and to reduce the number of particles to about 40
  for all variants other than the original "CanonicalPSO" formulation.

  Example :
  ``{"Variant":"CanonicalPSO"}``
