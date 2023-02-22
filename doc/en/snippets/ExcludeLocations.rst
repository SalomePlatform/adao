.. index:: single: ExcludeLocations

ExcludeLocations
  *List of integers or names*. This key specifies the list of points in the
  state vector excluded from the optimal search. The default value is an empty
  list. The list can contain either **indices of points** (in the implicit
  internal order of a state vector) or **names of points** (which must exist in
  the list of position names indicated by the keyword "*NameOfLocations*" in
  order to be excluded). By default, if the elements of the list are strings
  that can be assimilated to indices, then these strings are indeed considered
  as indices and not names.

  Important notice: the numbering of these excluded points must be identical to
  that adopted, implicitly and imperatively, by the variables constituting a
  state considered arbitrarily in one-dimensional form.

  Example :
  ``{"ExcludeLocations":[3, 125, 286]}`` or ``{"ExcludeLocations":["Point3", "XgTaC"]}``
