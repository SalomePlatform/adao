
================================================================================
ADAO module documentation
================================================================================

The ADAO module provides **data assimilation** features in SALOME context. It is
based on usage on other SALOME modules, namely YACS and EFICAS, and on an
extensible generic underlying data assimilation library.

Briefly stated, Data Assimilation is a methodological framework to compute the
optimal estimate of the inaccessible true value of a system state over time. It
uses information coming from experimental measurements or observations, and from
numerical *a priori* models, including information about their errors. Parts of
the framework are also known as *parameter estimation*, *inverse problems*,
*bayesian estimation*, *optimal interpolation*, etc. More details can be found
in the section :ref:`section_theory`.

The documentation of this module is divided in 5 parts, the first one being an
introduction. The second part briefly introduces data assimilation and concepts.
The third part describes how to use the module ADAO. The fourth part gives
examples on ADAO usage. Users interested in quick use of the module can jump to
this section :ref:`section_examples`, but a valuable use of the module requires
to read and come back regularly to the section :ref:`section_using`. The last
part focuses on advanced usages of the module, how to get more information, or
how to use it without the graphical user interface (GUI). 

In all this documentation, we use standard notations of data assimilation, as
described in [Ide97]. Moreover, vectors are written horizontally or vertically
without making difference. Matrices are written either normally, or with a
condensed notation, consisting in the use of a space to separate values and a
"``;``" to separate the rows, in a continuous line.

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   examples
   advanced

Indices and tables
================================================================================

* :ref:`genindex`
* :ref:`search`

.. [Argaud09] Argaud J.-P., Bouriquet B., Hunt J., *Data Assimilation from Operational and Industrial Applications to Complex Systems*, Mathematics Today, pp.150-152, October 2009

.. [Bouttier99] Bouttier B., Courtier P., *Data assimilation concepts and methods*, Meteorological Training Course Lecture Series, ECMWF, 1999, http://www.ecmwf.int/newsevents/training/rcourse_notes/pdf_files/Assim_concepts.pdf

.. [Bocquet04] Bocquet M., *Introduction aux principes et méthodes de l'assimilation de données en géophysique*, Lecture Notes, 2004-2008, http://cerea.enpc.fr/HomePages/bocquet/assim.pdf

.. [Byrd95] Byrd R. H., Lu P., Nocedal J., *A Limited Memory Algorithm for Bound Constrained Optimization*, SIAM Journal on Scientific and Statistical Computing, 16(5), pp.1190-1208, 1995

.. [Ide97] Ide K., Courtier P., Ghil M., Lorenc A. C., *Unified notation for data assimilation: operational, sequential and variational*, Journal of the Meteorological Society of Japan, 75(1B), pp.181-189, 1997

.. [Kalnay03] Kalnay E., *Atmospheric Modeling, Data Assimilation and Predictability*, Cambridge University Press, 2003

.. [Tarantola87] Tarantola A., *Inverse Problem: Theory Methods for Data Fitting and Parameter Estimation*, Elsevier, 1987

.. [Talagrand97] Talagrand O., *Assimilation of Observations, an Introduction*, Journal of the Meteorological Society of Japan, 75(1B), pp.191-209, 1997

.. [WikipediaDA] Wikipedia/Data_assimilation: http://en.wikipedia.org/wiki/Data_assimilation

.. [Zhu97] Zhu C., Byrd R. H., Nocedal J., *L-BFGS-B: Algorithm 778: L-BFGS-B, FORTRAN routines for large scale bound constrained optimization*, ACM Transactions on Mathematical Software, Vol 23(4), pp.550-560, 1997
