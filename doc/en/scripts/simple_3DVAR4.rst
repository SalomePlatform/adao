.. index:: single: 3DVAR (example)
.. index:: single: Lorenz63
.. _section_usecase_3DVAR4_L63a:

Correction by 3DVAR of the state of a Lorenz dynamic system
...........................................................

This example extends the simple use cases of the 3DVAR algorithm (see
:ref:`Examples with the "3DVAR"<section_ref_algorithm_3DVAR_examples>`, or a
similar example in [Asch16]_). It describes the effect of data assimilation on
the time forecast of a dynamic system. It is a highly simplified case that
illustrates a classical approach in meteorology (short-term weather
forecasting, below a two-week period) or in seasonal forecasting (longer-term
weather forecasting, beyond a two-week period).

Here, we use a simple classical model of a dynamic system, named *Lorenz
system*, *Lorenz oscillator*, *Lorenz3D* or *Lorenz63* after its author, the
mathematician and meteorologist Edward Lorenz ([Lorenz63]_, [WikipediaL63]_).
It is available in integrated test models of ADAO under the name
``Lorenz1963``.

This three-dimensional nonlinear dynamical system is a highly simplified model
of the Navier-Stokes equations, designed to study the coupling of atmosphere
and ocean, in a particular physical convection configuration (Rayleigh-Bénard
convection). It exhibits deterministic chaotic behavior, which means that the
dynamical system is deterministic (from a continuous or discrete point of
view), but its sensitivity to initial conditions or parameters enables an
arbitrarily different trajectory to be obtained after a finite time for small
variations in its initial conditions. This system is known as the origin of the
concept of the butterfly effect [Butterfly72]_ and for its illustrative value.

This system depends on its initial conditions and on 3 physical parameters
:math:`(\sigma,\rho,\beta)`. The classical equations for state
:math:`u=(x,y,z)` describing it are:

.. math:: \left\{
    \begin{array}{lcl}
    \displaystyle\frac{dx}{dt} & = & \sigma (y - x)\\~\\
    \displaystyle\frac{dy}{dt} & = & \rho\, x - y - x\, z\\~\\
    \displaystyle\frac{dz}{dt} & = & x\, y - \beta\, z
    \end{array}
    \right.

with time :math:`t\in{I\!R}^+`, and with :math:`\sigma=10`, :math:`\rho=28`,
:math:`\beta=8/3` current values of parameters characterizing a chaotic state.
The initial condition is arbitrary.

The following figure illustrates the Lorenz attractor by direct simulation of
this dynamic system, shown here for :math:`t\in[0,40]` and with initial
condition :math:`(0,1,0)`. The attractor is the structure corresponding to the
long-term behavior of the Lorenz oscillator, which here appears as two
"*butterfly wings*". The figure shows that the state variable :math:`u=(x,y,z)`
of this dynamical system evolves on a deterministic, non-periodic trajectory,
which wraps around one wing of the butterfly and then "*jumps*" to the other
wing, and so on in a seemingly erratic fashion. The figure below shows a single
trajectory, colored differently for its first and second halves to illustrate
the successive windings and jumps.

.. _simple_3DVAR4Plus01:
.. image:: scripts/simple_3DVAR4Plus01.png
  :align: center
  :width: 90%

If we observe the same trajectory by plotting the 3 components of the system
state separately, with the same simulation parameters, we obtain the following
figure:

.. _simple_3DVAR4Plus02:
.. image:: scripts/simple_3DVAR4Plus02.png
  :align: center
  :width: 90%

Noting that the amplitudes and temporal behaviors of the first two components
:math:`x` and :math:`y` are indeed not identical, despite their similarity,
this figure illustrates the property of chaos through an absence of spatial and
temporal regularity.

**To illustrate the analysis approach, we'll be using twin experiments** (see
section :ref:`section_methodology_twin`).

We choose here to **perturb only the initial state of the simulation**, using
the background value :math:`u^b=[2,3,4]`, whose effects are to be compared with
those of the initial state, said to be *ideal* or *true*, unperturbed, equal to
:math:`u^t=[1,1,1]`.

The model is considered to be perfect, and is observed over the time interval
[0,2]. Pseudo-observations :math:`\mathbf{y}^o` are of 10 in number,
constructed by sampling at time step :math:`\delta t=0.2` over this time
interval, based on a simulation from the initial unperturbed state
:math:`u^t=[1,1,1]`. To these exact sampled values is then added, on each
component, a Gaussian noise of amplitude :math:`\sigma_m=0.15` to obtain a
pseudo-observation. The order of magnitude of the noise is that of the
experimental noise of real variable measurements corresponding to the
simplified Lorenz model.

The following figure illustrates this information for the first variable (the
others are similar), spread over the time interval [0,2] of measurement:

.. _simple_3DVAR4Plus03:
.. image:: scripts/simple_3DVAR4Plus03.png
  :align: center
  :width: 90%

.. note::

    It is strongly emphasized that successive observations are not available
    simultaneously, at the initial time for example, but are available each
    time the simulation reaches one of the measurement instants. It is also
    recalled that the blue dashed simulation curve, obtained from the ideal or
    true state :math:`u^t=[1,1,1]`, is unknown outside twin experiments. Only
    trajectories plotted as continuous are known by simulation.

In numerical form, saved in a file named ``simple_3DVAR4Observations.csv`` to
be read, the observation values are as follows:

.. literalinclude:: scripts/simple_3DVAR4Observations.csv

Data assimilation is then used to correct the initial background trajectory of
the system with each new observation acquired. At each step :math:`n`, the
current predicted state :math:`\mathbf{u}^f_n` is modified to produce a new
**analyzed state** :math:`\mathbf{u}^a_n`, taking into account this new
information :math:`\mathbf{y}^o_n`, then the simulation continues from this new
state. Assimilation of the observations is performed using the simple ADAO
script below. For better readability, the script explicitly presents the time
loop on the observations:

.. literalinclude:: scripts/simple_3DVAR4.py

.. include:: snippets/Header2Algo10.rst

.. literalinclude:: scripts/simple_3DVAR4.res
    :language: none

The following figure illustrates, on the first variable, the **forecasted,
measured and analyzed states** at each observation step, as well as the states
simulated by the model between two observations. The temporal breaks in the
trajectory are, by their very nature, the result of each assimilation operation
with new observed information.

.. _simple_3DVAR4Plus06:
.. image:: scripts/simple_3DVAR4Plus06.png
  :align: center
  :width: 90%

We can clearly see that the predicted state :math:`\mathbf{u}^f_n` is more and
more consistent with each pseudo-observation :math:`\mathbf{y}^o_n`, and that
each portion of the predicted trajectory is closer and closer to the unknown
ideal trajectory resulting from the true state :math:`\mathbf{u}^t`. In the
following figure, the classical RMSE (*Root-Mean-Square Error*) measure of
deviations similarly describes this iterative improvement of forecasts and
analyses incorporating the information of observations.

.. _simple_3DVAR4Plus09:
.. image:: scripts/simple_3DVAR4Plus09.png
  :align: center
  :width: 90%

It is also possible to compare the state forecasts obtained over the time
interval [2,10], which lies beyond the observation window concerned by the data
assimilation approach. There are three ways of establishing this temporal
simulation after the instant :math:`t=2`:

- we can calculate the forecast from the state at :math:`t=2`, itself obtained
  by simulation from the disturbed initial background state :math:`u^b=[2,3,4]`
  at time :math:`t=0`, in which only the background information is used;
- we can calculate the forecast from the state at :math:`t=2`, itself obtained
  by simulation from the unperturbed initial state (*ideal state* or *true
  state*) :math:`u^t=[1,1,1]`, which is considered the reference but known only
  through the observations obtained from sampling with noise ;
- we can calculate the forecast resulting from data assimilation analysis,
  which comes from state correction by observations.

These three approaches are illustrated in the following figure, where the
assimilation window is recalled over the time interval [0,2] and where
forecasts are made over the time interval [2,10]:

.. _simple_3DVAR4Plus12:
.. image:: scripts/simple_3DVAR4Plus12.png
  :align: center
  :width: 90%

It is apparent that the forecast resulting from the :math:`\mathbf{u}^a`
analysis, obtained by data assimilation at time :math:`t=2`, is much more in
line with the ideal :math:`\mathbf{u}^t` simulation chosen for the twin
experiment, than the forecast resulting from the :math:`\mathbf{u}^b` draft
simulated at :math:`t=2`. Even if the time extension of the simulation
necessarily leads to an increasing deviation from the true state, due to the
chaotic property of the Lorenz system, the correction by data assimilation
makes it possible to obtain an acceptable forecast over a much longer period of
time than the absence of correction intrinsically present in the background
simulation.
