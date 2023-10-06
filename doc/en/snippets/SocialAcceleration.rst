.. index:: single: SocialAcceleration

SocialAcceleration
  *Real value*. This key indicates the recall rate at the best swarm insect in
  the neighbourhood of the current insect, which is by default the whole swarm.
  It is a floating point positive value. The default value is about
  :math:`1/2+ln(2)=1.19315` and it is recommended to adapt it, rather by
  reducing it, to the physical case that is being treated.

  Example :
  ``{"SocialAcceleration":1.19315}``
