================================================================================
ADAO module documentation
================================================================================

.. image:: images/ADAO_logo.png
   :align: center
   :scale: 10%

The ADAO module provides **data assimilation** features in SALOME context. It is
based on usage of other SALOME modules, namely YACS and EFICAS, and on usage of
a generic underlying data assimilation library.

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

Table of contents
-----------------

.. toctree::
   :maxdepth: 2

   intro
   theory
   using
   examples
   advanced
   bibliography

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
* :ref:`section_glossary`
