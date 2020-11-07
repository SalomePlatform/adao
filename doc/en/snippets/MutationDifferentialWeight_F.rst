.. index:: single: MutationDifferentialWeight_F

MutationDifferentialWeight_F
  *Pair of real values*. This key is used to define the differential weight in
  the mutation step. This variable is usually noted as ``F`` in the literature.
  It can be constant if it is in the form of a single value, or randomly
  variable in the two given bounds in the pair. The default value is (0.5, 1).

  Example:
  ``{"MutationDifferentialWeight_F":(0.5, 1)}``
