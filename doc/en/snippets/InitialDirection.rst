.. index:: single: InitialDirection

InitialDirection
  This key indicates the vector direction used for the directional derivative
  around the nominal checking point. It has to be a vector. If not specified,
  this direction defaults to a random perturbation around zero of the same
  vector size than the checking point.

  Example :
  ``{"InitialDirection":[0.1,0.1,100.,3}``
