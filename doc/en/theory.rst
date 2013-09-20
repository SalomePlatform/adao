.. _section_theory:

================================================================================
A brief introduction to Data Assimilation and Optimization
================================================================================

.. index:: single: Data Assimilation
.. index:: single: true state
.. index:: single: observation
.. index:: single: a priori

**Data Assimilation** is a general framework for computing the optimal estimate
of the true state of a system, over time if necessary. It uses values obtained
by combining both observations and *a priori* models, including information
about their errors.

In other words, data assimilation merges measurement data of a system, that are
the observations, with *a priori* system physical and mathematical knowledge,
embedded in numerical models, to obtain the best possible estimate of the system
true state and of its stochastic properties. Note that this true state can not
be reached, but can only be estimated. Moreover, despite the fact that the used
information are stochastic by nature, data assimilation provides deterministic
techniques in order to realize the estimation.

Because data assimilation look for the **best possible** estimate, its
underlying procedure always integrates optimization in order to find this
estimate: particular optimization methods are always embedded in data
assimilation algorithms. Optimization methods can be seen here as a way to
extend data assimilation applications. They will be introduced this way in the
section `Going further in the state estimation by optimization methods`_, but
they are far more general and can be used without data assimilation concepts.

Two main types of applications exist in data assimilation, being covered by the
same formalism: **parameters identification** and **fields reconstruction**.
Before introducing the `Simple description of the data assimilation framework`_
in a next section, we describe briefly these two types. At the end, some
references allow `Going further in the data assimilation framework`_.

Fields reconstruction or measures interpolation
-----------------------------------------------

.. index:: single: fields reconstruction

Fields reconstruction consists in finding, from a restricted set of real
measures, the physical field which is the most *consistent* with these measures.

This consistency is to understand in terms of interpolation, that is to say that
the field we want to reconstruct, using data assimilation on measures, has to
fit at best the measures, while remaining constrained by the overall
calculation. The calculation is thus an *a priori* estimation of the field that
we seek to identify.

If the system evolves in time, the reconstruction has to be established on every
time step, as a whole. The interpolation process in this case is more
complicated since it is temporal, not only in terms of instantaneous values of
the field.

A simple example of fields reconstruction comes from meteorology, in which one
look for value of variables such as temperature or pressure in all points of the
spatial domain. One have instantaneous measurements of these quantities at
certain points, but also a history set of these measures. Moreover, these
variables are constrained by evolution equations for the state of the
atmosphere, which indicates for example that the pressure at a point can not
take any value independently of the value at this same point in previous time.
One must therefore make the reconstruction of a field at any point in space, in
a "consistent" manner with the evolution equations and with the measures of the
previous time steps.

Parameters identification or calibration
----------------------------------------

.. index:: single: parameters identification

The identification of parameters by data assimilation is a form of calibration
which uses both the measurement and an *a priori* estimation (called the
"*background*") of the state that one seeks to identify, as well as a
characterization of their errors. From this point of view, it uses all available
information on the physical system (even if assumptions about errors are
relatively restrictive) to find the "*optimal*" estimation from the true state.
We note, in terms of optimization, that the background realizes a mathematical
regularization of the main problem of parameters identification.

In practice, the two observed gaps "*calculation-background*" and
"*calculation-measures*" are added to build the calibration correction of
parameters or initial conditions. The addition of these two gaps requires a
relative weight, which is chosen to reflect the trust we give to each piece of
information. This confidence is measured by the covariance of the errors on the
background and on the observations. Thus the stochastic aspect of information,
measured or *a priori*, is essential for building the calibration error
function.

A simple example of parameters identification comes from any kind of physical
simulation process involving a parametrized model. For example, a static
mechanical simulation of a beam constrained by some forces is described by beam
parameters, such as a Young coefficient, or by the intensity of the force. The
parameter estimation problem consists in finding for example the right Young
coefficient in order that the simulation of the beam corresponds to
measurements, including the knowledge of errors.

Simple description of the data assimilation framework
-----------------------------------------------------

.. index:: single: background
.. index:: single: background error covariances
.. index:: single: observation error covariances
.. index:: single: covariances

We can write these features in a simple manner. By default, all variables are
vectors, as there are several parameters to readjust.

According to standard notations in data assimilation, we note
:math:`\mathbf{x}^a` the optimal parameters that is to be determined by
calibration, :math:`\mathbf{y}^o` the observations (or experimental
measurements) that we must compare to the simulation outputs,
:math:`\mathbf{x}^b` the background (*a priori* values, or regularization
values) of searched parameters, :math:`\mathbf{x}^t` the unknown ideals
parameters that would give exactly the observations (assuming that the errors
are zero and the model is exact) as output.

In the simplest case, which is static, the steps of simulation and of
observation can be combined into a single observation operator noted :math:`H`
(linear or nonlinear), which transforms the input parameters :math:`\mathbf{x}`
to results :math:`\mathbf{y}` to be compared to observations
:math:`\mathbf{y}^o`. Moreover, we use the linearized operator
:math:`\mathbf{H}` to represent the effect of the full operator :math:`H` around
a linearization point (and we omit thereafter to mention :math:`H` even if it is
possible to keep it). In reality, we have already indicated that the stochastic
nature of variables is essential, coming from the fact that model, background
and observations are incorrect. We therefore introduce errors of observations
additively, in the form of a random vector :math:`\mathbf{\epsilon}^o` such
that:

.. math:: \mathbf{y}^o = \mathbf{H} \mathbf{x}^t + \mathbf{\epsilon}^o

The errors represented here are not only those from observation, but also from
the simulation. We can always consider that these errors are of zero mean. We
can then define a matrix :math:`\mathbf{R}` of the observation error covariances
by:

.. math:: \mathbf{R} = E[\mathbf{\epsilon}^o.{\mathbf{\epsilon}^o}^T]

The background can also be written as a function of the true value, by
introducing the error vector :math:`\mathbf{\epsilon}^b`:

.. math:: \mathbf{x}^b = \mathbf{x}^t + \mathbf{\epsilon}^b

where errors are also assumed of zero mean, in the same manner as for
observations. We define the :math:`\mathbf{B}` matrix of background error
covariances by:

.. math:: \mathbf{B} = E[\mathbf{\epsilon}^b.{\mathbf{\epsilon}^b}^T]

The optimal estimation of the true parameters :math:`\mathbf{x}^t`, given the
background :math:`\mathbf{x}^b` and the observations :math:`\mathbf{y}^o`, is
then the "*analysis*" :math:`\mathbf{x}^a` and comes from the minimisation of an
error function (in variational assimilation) or from the filtering correction (in
assimilation by filtering).

In **variational assimilation**, in a static case, one classically attempts to
minimize the following function :math:`J`:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

which is usually designed as the "*3D-VAR*" function. Since :math:`\mathbf{B}`
and :math:`\mathbf{R}` covariance matrices are proportional to the variances of
errors, their presence in both terms of the function :math:`J` can effectively
weight the differences by confidence in the background or observations. The
parameters vector :math:`\mathbf{x}` realizing the minimum of this function
therefore constitute the analysis :math:`\mathbf{x}^a`. It is at this level that
we have to use the full panoply of function minimization methods otherwise known
in optimization (see also section `Going further in the state estimation by
optimization methods`_). Depending on the size of the parameters vector
:math:`\mathbf{x}` to identify and of the availability of gradient and Hessian
of :math:`J`, it is appropriate to adapt the chosen optimization method
(gradient, Newton, quasi-Newton...).

In **assimilation by filtering**, in this simple case usually referred to as
"*BLUE*" (for "*Best Linear Unbiased Estimator*"), the :math:`\mathbf{x}^a`
analysis is given as a correction of the background :math:`\mathbf{x}^b` by a
term proportional to the difference between observations :math:`\mathbf{y}^o`
and calculations :math:`\mathbf{H}\mathbf{x}^b`:

.. math:: \mathbf{x}^a = \mathbf{x}^b + \mathbf{K}(\mathbf{y}^o - \mathbf{H}\mathbf{x}^b)

where :math:`\mathbf{K}` is the Kalman gain matrix, which is expressed using
covariance matrices in the following form:

.. math:: \mathbf{K} = \mathbf{B}\mathbf{H}^T(\mathbf{H}\mathbf{B}\mathbf{H}^T+\mathbf{R})^{-1}

The advantage of filtering is to explicitly calculate the gain, to produce then
the *a posteriori* covariance analysis matrix.

In this simple static case, we can show, under the assumption of Gaussian error
distributions, that the two *variational* and *filtering* approaches are
equivalent.

It is indicated here that these methods of "*3D-VAR*" and "*BLUE*" may be
extended to dynamic problems, called respectively "*4D-VAR*" and "*Kalman
filter*". They can take into account the evolution operator to establish an
analysis at the right time steps of the gap between observations and simulations,
and to have, at every moment, the propagation of the background through the
evolution model. Many other variants have been developed to improve the
numerical quality or to take into account computer requirements such as
calculation size and time.

Going further in the data assimilation framework
------------------------------------------------

.. index:: single: state estimation
.. index:: single: parameter estimation
.. index:: single: inverse problems
.. index:: single: Bayesian estimation
.. index:: single: optimal interpolation
.. index:: single: mathematical regularization
.. index:: single: data smoothing

To get more information about all the data assimilation techniques, the reader
can consult introductory documents like [Argaud09]_, on-line training courses or
lectures like [Bouttier99]_ and [Bocquet04]_ (along with other materials coming
from geosciences applications), or general documents like [Talagrand97]_,
[Tarantola87]_, [Kalnay03]_, [Ide97]_ and [WikipediaDA]_.

Note that data assimilation is not restricted to meteorology or geo-sciences, but
is widely used in other scientific domains. There are several fields in science
and technology where the effective use of observed but incomplete data is
crucial.

Some aspects of data assimilation are also known as *state estimation*,
*parameter estimation*, *inverse problems*, *Bayesian estimation*, *optimal
interpolation*, *mathematical regularization*, *data smoothing*, etc. These
terms can be used in bibliographical searches.

Going further in the state estimation by optimization methods
-------------------------------------------------------------

.. index:: single: state estimation
.. index:: single: optimization methods

As seen before, in a static simulation case, the variational data assimilation
requires to minimize the goal function :math:`J`:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

which is named the "*3D-VAR*" function. It can be seen as a *least squares
minimization* extented form, obtained by adding a regularizing term using
:math:`\mathbf{x}-\mathbf{x}^b`, and by weighting the differences using
:math:`\mathbf{B}` and :math:`\mathbf{R}` the two covariance matrices. The
minimization of the :math:`J` function leads to the *best* state estimation.

State estimation possibilities extension, by using more explicitly optimization
methods and their properties, can be imagined in two ways.

First, classical optimization methods involves using various gradient-based
minimizing procedures. They are extremely efficient to look for a single local
minimum. But they require the goal function :math:`J` to be sufficiently regular
and differentiable, and are not able to capture global properties of the
minimization problem, for example: global minimum, set of equivalent solutions
due to over-parametrization, multiple local minima, etc. **A way to extend
estimation possibilities is then to use a whole range of optimizers, allowing
global minimization, various robust search properties, etc**. There is a lot of
minimizing methods, such as stochastic ones, evolutionary ones, heuristics and
meta-heuristics for real-valued problems, etc. They can treat partially irregular
or noisy function :math:`J`, can characterize local minima, etc. The main
drawback is a greater numerical cost to find state estimates, and no guarantee
of convergence in finite time. Here, we only point the following
topics, as the methods are available in the ADAO module: *Quantile regression*
[WikipediaQR]_ and *Particle swarm optimization* [WikipediaPSO]_.

Secondly, optimization methods try usually to minimize quadratic measures of
errors, as the natural properties of such goal functions are well suited for
classical gradient optimization. But other measures of errors can be more
adapted to real physical simulation problems. Then, **an another way to extend
estimation possibilities is to use other measures of errors to be reduced**. For
example, we can cite *absolute error value*, *maximum error value*, etc. These
error measures are not differentiables, but some optimization methods can deal
with:  heuristics and meta-heuristics for real-valued problem, etc. As
previously, the main drawback remain a greater numerical cost to find state
estimates, and no guarantee of convergence in finite time. Here, we point also
the following methods as it is available in the ADAO module: *Particle swarm
optimization* [WikipediaPSO]_.

The reader interested in the subject of optimization can look at [WikipediaMO]_
as a general entry point.