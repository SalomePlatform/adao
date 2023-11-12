.. index:: single: SampleAsIndependantRandomVariables

SampleAsIndependantRandomVariables
  *List of triplets [Name, Parameters, Number]*. This key describes the
  calculations points as an hyper-cube, for which the points on each axis come
  from a independent random sampling of the axis variable, under the
  specification of the distribution, its parameters and the number of points in
  the sample, as a list ``['distribution', [parameters], number]`` for each
  axis. The possible distributions are 'normal' of parameters (mean,std),
  'lognormal' of parameters (mean,sigma), 'uniform' of parameters (low,high),
  or 'weibull' of parameter (shape). That is then a list of the same size than
  the one of the state. By nature, the points are included in the unbounded or
  bounded domain, depending on the characteristics of the distributions chosen
  for each variable.

  Example :
  ``{"SampleAsIndependantRandomVariables":[['normal',[0.,1.],3], ['uniform',[-2,2],4]]}`` for a state space of dimension 2.
