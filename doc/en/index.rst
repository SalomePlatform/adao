================================================================================
ADAO documentation
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :width: 20%

The ADAO module provides **data assimilation and optimization** features in
SALOME context. It is based on usage of other SALOME modules, namely YACS and
EFICAS, and on usage of a generic underlying data assimilation library.

Briefly stated, Data Assimilation is a methodological framework to compute the
optimal estimate of the inaccessible true value of a system state over time. It
uses information coming from experimental measurements or observations, and from
numerical *a priori* models, including information about their errors. Parts of
the framework are also known under the names of *parameter estimation*, *inverse
problems*, *Bayesian estimation*, *optimal interpolation*, etc. More details can
be found in the section :ref:`section_theory`.

The documentation of this module is divided in parts. The first one
:ref:`section_intro` is an introduction. The second part :ref:`section_theory`
briefly introduces data assimilation, optimization and concepts. The third part
:ref:`section_using` describes how to use the module ADAO. The fourth part
:ref:`section_reference` gives a detailed description of all the ADAO commands
and keywords. The fifth part :ref:`section_examples` gives examples on ADAO
usage. Users interested in quick use of the module can jump to this section, but
a valuable use of the module requires to read and come back regularly to the
third and fourth ones. The last part :ref:`section_advanced` focuses on advanced
usages of the module, how to get more information, or how to use it by
scripting, without the graphical user interface (GUI). And be sure to read the
part :ref:`section_licence` to respect the module requirements.

In all this documentation, we use standard notations of linear algebra, data
assimilation (as described in [Ide97]_) and optimization. In particular, vectors
are written horizontally or vertically without making difference. Matrices are
written either normally, or with a condensed notation, consisting in the use of
a space to separate values and a "``;``" to separate the rows, in a continuous
line.

Table of contents
-----------------

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   reference
   examples
   advanced
   licence
   bibliography

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
* :ref:`section_glossary`
