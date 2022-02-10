.. index:: single: Observation

Observation
  *List of vectors*. The variable indicates the observation vector used for
  data assimilation or optimization, and usually noted :math:`\mathbf{y}^o`.
  Its value is defined as an object of type "*Vector*" if it is a single
  observation (temporal or not) or "*VectorSeries*" if it is a succession of
  observations. Its availability in output is conditioned by the boolean
  "*Stored*" associated in input.
