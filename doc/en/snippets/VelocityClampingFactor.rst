.. index:: single: VelocityClampingFactor

VelocityClampingFactor
  *Real value*. This key indicates the rate of group velocity attenuation in
  the update for each insect, useful to avoid swarm explosion, i.e.
  uncontrolled growth of insect velocity. It is a floating point value between
  0+ and 1. The default value is 0.3.

  Example :
  ``{"VelocityClampingFactor":0.3}``
