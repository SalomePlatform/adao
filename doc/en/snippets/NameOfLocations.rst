.. index:: single: NameOfLocations

NameOfLocations
  *List of names*. This key indicates an explicit list of variable names or
  positions, positioned as in a state vector considered arbitrarily in
  one-dimensional form. The default value is an empty list. To be used, this
  list must have the same length as that of a physical state.

  Important notice: the order of the names is, implicitly and imperatively, the
  same as that of the variables constituting a state considered arbitrarily in
  one-dimensional form.

  Example :
  ``{"NameOfLocations":["Point3", "Location42", "Position125", "XgTaC"]}``
