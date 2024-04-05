.. index:: single: AmplitudeOfInitialDirection

AmplitudeOfInitialDirection
  *Real value*. This key indicates the scaling of the initial perturbation
  build as a vector used for the directional derivative around the nominal
  checking point. The default is 1, that means no scaling. It's useful to
  modify this value, and in particular to decrease it when the biggest
  perturbations are going out of the allowed domain for the function.

  Example:
  ``{"AmplitudeOfInitialDirection":0.5}``
