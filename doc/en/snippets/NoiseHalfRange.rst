.. index:: single: NoiseHalfRange

NoiseHalfRange
  *List of real values*. This key indicates,, only in the case of a "Uniform"
  distribution type asked through the keyword "*NoiseDistribution*", the
  half-amplitude of the uniform state centred perturbations for each component
  of the state. The default is an empty list, this key must therefore be filled
  in in the case of a "Uniform" distribution. A simple way to do this is to
  give a list of the length of the desired state with identical
  half-amplitudes, as in the example below with half-amplitudes of 3%. It is
  recommended to take half-amplitudes of a few percent maximum.

  Example :
  ``{"NoiseHalfRange":<state length>*[0.03]}``
