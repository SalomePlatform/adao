.. index:: single: HybridNumberOfLocalHunters

HybridNumberOfLocalHunters
  *Integer value*. This key indicates the number of insects on which the local
  search will be conducted. Insects are chosen as the best from the current
  iteration of the global search. With a default value of 1, the local search
  is performed on the best insect only. It is then recommended to adapt this
  parameter to the needs on real problems.

  Example :
  ``{"HybridNumberOfLocalHunters":1}``
