.. _section_theory:

================================================================================
A brief introduction to Data Assimilation
================================================================================

**Data Assimilation** is a general framework for computing the optimal estimate
of the true state of a system, over time if necessary. It uses values obtained
both from observations and *a priori* models, including information about their
errors.

In other words, data assimilation merges measurement data, the observations,
with *a priori* physical and mathematical knowledge, embedded in numerical
models, to obtain the best possible estimate of the true state and of its
stochastic properties. Note that this true state can not be reached, but can
only be estimated. Moreover, despite the fact that used information are
stochastic by nature, data assimilation provides deterministic techniques in
order to realize the estimation.

Two main types of applications exist in data assimilation being covered by the
same formalism: **parameters identification** and **fields reconstruction**.
Before introducing the `Simple description of the data assimilation framework`_
in a next section, we describe briefly these two types. At the end, some
references allow `Going further in the data assimilation framework`_.

Fields reconstruction or measures interpolation
-----------------------------------------------

Fields reconstruction consists in finding, from a restricted set of real
measures, the physical field which is the most *consistent* with these measures.

This consistency is to understand in terms of interpolation, that is to say that
the field, we want to reconstruct using data assimilation on measures, has to
fit at best the measures, while remaining constrained by the overall
calculation. The calculation is thus an *a priori* estimation of the field that
we seek to identify.

If the system evolves in time, the reconstruction has to be established on every
time step, as a whole. The interpolation process in this case is more
complicated since it is temporal, not only in terms of instantaneous values of
the field.

A simple example of fields reconstruction comes from of meteorology, in which we
look for value of variables such as temperature or pressure in all points of the
spatial domain. We have instantaneous measurements of these quantities at
certain points, but also a history set of these measures. Moreover, these
variables are constrained by evolution equations for the state of the
atmosphere, which indicates for example that the pressure at a point can not
take any value independently of the value at this same point in previous time.
We must therefore make the reconstruction of a field at any point in space, in
order "consistent" with the evolution equations and measures of the previous
time steps.

Parameters identification or calibration
----------------------------------------

The identification of parameters by data assimilation is a form of calibration
which uses both the measurement and an *a priori* estimation (called the
"*background*") of the state that one seeks to identify, as well as a
characterization of their errors. From this point of view, it uses all available
information on the physical system (even if assumptions about errors are
relatively restrictive) to find the "*optimal*" estimation from the true state.
We note, in terms of optimization, that the background realizes a mathematical
regularization of the main problem of identification.

In practice, the two gaps "*calculation-background*" and
"*calculation-measures*" are added to build the calibration correction of
parameters or initial conditions. The addition of these two gaps requires a
relative weight, which is chosen to reflect the trust we give to each piece of
information. This confidence is measured by the covariance of the errors on the
background and on the observations. Thus the stochastic aspect of information,
measured or *a priori*, is essential for building the calibration error
function.

Simple description of the data assimilation framework
-----------------------------------------------------

We can write these features in a simple manner. By default, all variables are
vectors, as there are several parameters to readjust.

According to standard notations in data assimilation, we note
:math:`\mathbf{x}^a` the optimal unknown parameters that is to be determined by
calibration, :math:`\mathbf{y}^o` the observations (or experimental
measurements) that we must compare the simulation outputs, :math:`\mathbf{x}^b`
the background (*a priori* values, or regularization values) of searched
parameters, :math:`\mathbf{x}^t` unknown ideals parameters that would give as
output exactly the observations (assuming that the errors are zero and the model
exact).

In the simplest case, static, the steps of simulation and of observation can be
combined into a single operator noted :math:`H` (linear or nonlinear), which
transforms the input parameters :math:`\mathbf{x}` to results :math:`\mathbf{y}`
to be compared to observations :math:`\mathbf{y}^o`. Moreover, we use the
linearized operator :math:`\mathbf{H}` to represent the effect of the full
operator :math:`H` around a linearization point (and we omit thereafter to
mention :math:`H` even if it is possible to keep it). In reality, we have already
indicated that the stochastic nature of variables is essential, coming from the
fact that model, background and observations are incorrect. We therefore
introduce errors of observations additively, in the form of a random vector
:math:`\mathbf{\epsilon}^o` such that:

.. math:: \mathbf{y}^o = \mathbf{H} \mathbf{x}^t + \mathbf{\epsilon}^o

The errors represented here are not only those from observation, but also from
the simulation. We can always consider that these errors are of zero mean. We
can then define a matrix :math:`\mathbf{R}` of the observation error covariance
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

In **variational assimilation**, one classically attempts to minimize the
following function :math:`J`:

.. math:: J(\mathbf{x})=(\mathbf{x}-\mathbf{x}^b)^T.\mathbf{B}^{-1}.(\mathbf{x}-\mathbf{x}^b)+(\mathbf{y}^o-\mathbf{H}.\mathbf{x})^T.\mathbf{R}^{-1}.(\mathbf{y}^o-\mathbf{H}.\mathbf{x})

which is usually designed as the "*3D-VAR*" function. Since covariance matrices
are proportional to the variances of errors, their presence in both terms of the
function :math:`J` can effectively weight the differences by confidence in the
background or observations. The parameters :math:`\mathbf{x}` realizing the
minimum of this function therefore constitute the analysis :math:`\mathbf{x}^a`.
It is at this level that we have to use the full panoply of function
minimization methods otherwise known in optimization. Depending on the size of
the parameters vector :math:`\mathbf{x}` to identify and ot the availability of
gradient and Hessian of :math:`J`, it is appropriate to adapt the chosen
optimization method (gradient, Newton, quasi-Newton ...).

In **assimilation by filtering**, in this simple case usually referred to as
"*BLUE*"(for "*Best Linear Unbiased Estimator*"), the :math:`\mathbf{x}^a`
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
filter*". They can take account of the evolution operator to establish an
analysis at the right time steps of the gap between observations and simulations,
and to have, at every moment, the propagation of the background through the
evolution model. Many other variants have been developed to improve the
numerical quality or to take into account computer requirements such as
calculation size and time.

Going further in the data assimilation framework
++++++++++++++++++++++++++++++++++++++++++++++++

To get more information about all the data assimilation techniques, the reader
can consult introductory documents like [Argaud09], on-line training courses or
lectures like [Bouttier99] and [Bocquet04] (along with other materials coming
from geosciences applications), or general documents like [Talagrand97],
[Tarantola87], [Kalnay03] and [WikipediaDA].

Note that data assimilation is not restricted to meteorology or geo-sciences, but
is widely used in other scientific domains. There are several fields in science
and technology where the effective use of observed but incomplete data is
crucial.

Some aspects of data assimilation are also known as *parameter estimation*,
*inverse problems*, *bayesian estimation*, *optimal interpolation*,
*mathematical regularisation*, *data smoothing*, etc. These terms can be used in
bibliographical searches.

.. [Argaud09] Argaud J.-P., Bouriquet B., Hunt J., *Data Assimilation from Operational and Industrial Applications to Complex Systems*, Mathematics Today, pp.150-152, October 2009

.. [Bouttier99] Bouttier B., Courtier P., *Data assimilation concepts and methods*, Meteorological Training Course Lecture Series, ECMWF, 1999, http://www.ecmwf.int/newsevents/training/rcourse_notes/pdf_files/Assim_concepts.pdf

.. [Bocquet04] Bocquet M., *Introduction aux principes et méthodes de l'assimilation de données en géophysique*, Lecture Notes, 2004-2008, http://cerea.enpc.fr/HomePages/bocquet/assim.pdf

.. [Tarantola87] Tarantola A., *Inverse Problem: Theory Methods for Data Fitting and Parameter Estimation*, Elsevier, 1987

.. [Talagrand97] Talagrand O., *Assimilation of Observations, an Introduction*, Journal of the Meteorological Society of Japan, 75(1B), pp. 191-209, 1997

.. [Kalnay03] Kalnay E., *Atmospheric Modeling, Data Assimilation and Predictability*, Cambridge University Press, 2003

.. [WikipediaDA] Wikipedia/Data_assimilation: http://en.wikipedia.org/wiki/Data_assimilation
