
================================================================================
ADAO module documentation
================================================================================

The ADAO module provides **data assimilation** features [#]_ in SALOME context.
It is based on an extensible generic underlying data assimilation library, and
on usage on other SALOME modules, namely YACS and EFICAS.

Briefly stated, Data Assimilation is a methodological framework to compute the
optimal estimate of the inaccesible true value of a system state over time. It
uses information coming from experimental measurements or observations, and from
numerical *a priori* models, including information about their errors. Parts of
the framework are also known as *parameter estimation*, *inverse problems*,
*bayesian estimation*, *optimal interpolation*, etc.

The documentation of this module is divided in 4 parts, the first one being an
introduction. The second part describes how to use the module ADAO. The third
part focuses on advanced usages of the module, how to get more information, or
how to use it without the graphical user interface (GUI). The last part gives
examples on ADAO usage.

Users interested in quick use of the module can jump to the last part, but a
valuable use of the module requires to read and come back regularly the second
part.

In all this documentation, we use standard notations of data assimilation.
Vectors are written horizontally or vertically without difference. Matrices are
written either normally, either with a condensed notation, consisting in the
use of a "``;``" to separate the rows in a continuous line.

.. toctree::
   :maxdepth: 2

   intro
   using
   advanced
   examples

Indices and tables
================================================================================

* :ref:`genindex`
* :ref:`search`

.. _ECMWF: http://www.ecmwf.int/newsevents/training/rcourse_notes/DATA_ASSIMILATION/ASSIM_CONCEPTS/Assim_concepts.html
.. _Wikipedia/Data_assimilation: http://en.wikipedia.org/wiki/Data_assimilation

.. [#] If you are not familiar with data assimilation concepts in general, an introductory on-line training course can be found at ECMWF_, along with other materials coming from geosciences applications. See also for example `Wikipedia/Data_assimilation`_. Note that data assimilation is not restricted to meteorology or geosciences, but is widely used in other scientific domains.
