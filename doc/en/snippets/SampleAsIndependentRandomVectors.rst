.. index:: single: SampleAsIndependentRandomVectors

SampleAsIndependentRandomVectors
  *List of pairs [Name, Parameters], plus [Dimension, Number]*. This key
  describes the calculation points in the form of particular distributions
  defined for each dimension, resulting in random vectors whose individual
  components follow the required distribution. Unlike the sampling described by
  the keyword "*SampleAsIndependentRandomVariables*", the points are not
  distributed over a regular hypercube. The distribution on each axis variable
  is specified by its name and parameters, in the form of a list *[Name,
  Parameters]* for each axis. This list of pairs, whose number is identical to
  the size of the state space, is completed by a pair of integers *[Dimension,
  Number]* containing the dimension of the state space and the desired number
  of sampling points. Possible distribution names are 'normal' with parameters
  (mean,std), 'lognormal' with parameters (mean,sigma), 'uniform' with
  parameters (low,high), 'loguniform' with parameters (low,high), or 'weibull'
  with parameters (shape). By their very nature, points are included in the
  unbounded or bounded domain, depending on the characteristics of the
  distributions chosen for each variable. Distributions can be different for
  each axis.

  Example :
  ``{"SampleAsIndependentRandomVectors":[['normal',[0.,1.]], ['uniform',[-2,2]]]}`` for a state space of dimension 2.
