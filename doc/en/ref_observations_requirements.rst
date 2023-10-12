..
   Copyright (C) 2008-2023 EDF R&D

   This file is part of SALOME ADAO module.

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with this library; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

   See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com

   Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D

.. _section_ref_observations_requirements:

Requirements for observation or experimental measurements description
---------------------------------------------------------------------

.. index:: single: setObservation
.. index:: single: setObservationError

The whole set of measurements of the physical system we are considering are
called "*observations*", or even simply "*an observation*". As already
mentioned in :ref:`section_theory`, this observation is noted in the most
generic way by:

.. math:: \mathbf{y}^o

It can depend in general of the space and the time, and even of parametric
variables, and this in a more or less complex way. We usually particularize the
time dependence by considering that, at each instant, the quantity
:math:`\mathbf{y}^o` is a vector of :math:`\mbox{I\hspace{-.15em}R}^d` (with
the dimension :math:`d` of the space being able to possibly vary in time). In
other words, **an observation is a (temporal) series of (varied)
measurements**. One will thus speak in an equivalent way of an observation
(vector), of a series or a vector of observations, and of a set of
observations. In its greatest generality, the sequential aspect of the series
of observations is related jointly to space, and/or to time, and/or to a
parametric dependence.

We can classify the ways of representing the observation according to the uses
that we have afterwards and the links with the algorithmic methods. The
classification that we propose is the following, each category being detailed
below:

#. `Use of a single spatial observation`_
#. `Use of a time series of spatial observations`_
#. `Use of a single spatio-temporal observation`_
#. `Use of a parameterized series of spatial observations`_

The numerical representations of the observations use all the possibilities
described in the :ref:`section_ref_entry_types`. We specialize their uses here
to indicate different possible ways of writing this information.

Use of a single spatial observation
+++++++++++++++++++++++++++++++++++

.. index:: single: Vector
.. index:: single: DataFile

This refers to the use of a vector series dependent only on space. This
observation is moreover used at once, i.e. being completely known at the
beginning of the algorithmic analysis. This can for example be a spatial field
of measurements, or several fields physically homogeneous or not.

- The mathematical representation is :math:`\mathbf{y}^o\,\in\,\mbox{I\hspace{-.15em}R}^d`.

- The canonical numerical representation is **a vector**.

- The numerical representation in ADAO is done with the keyword "*Vector*". All
  the information, declared in one of the following representations, is
  transformed into a single vector (note: lists and tuples are equivalent):

    - "*numpy.array*" variable : ``numpy.array([1, 2, 3])``
    - "*list*" variable        : ``[1, 2, 3]``
    - string variable          : ``'1 2 3'``
    - string variable          : ``'1,2,3'``
    - string variable          : ``'1;2;3'``
    - string variable          : ``'[1,2,3]'``
    - Python data file, with variable "*Observation*" in the namespace, indicated by the keyword "*Script*" with the condition ``Vector=True``
    - data text file (TXT, CSV, TSV, DAT), with variable pointer by name in column or row, indicated by the keyword "*DataFile*" with the condition ``Vector=True``
    - binary data file (NPY, NPZ), with variable pointer by name, indicated by the keyword "*DataFile*" with the condition ``Vector=True``

- Examples of statements in TUI interface:

    - ``case.setObservation( Vector = [1, 2, 3] )``
    - ``case.setObservation( Vector = numpy.array([1, 2, 3]) )``
    - ``case.setObservation( Vector = '1 2 3' )``
    - ``case.setObservation( Vector=True, Script = 'script.py' )```
    - ``case.setObservation( Vector=True, DataFile = 'data.csv' )```
    - ``case.setObservation( Vector=True, DataFile = 'data.npy' )```

Use note: in a given study, only the last record (whether a single vector or a
series of vectors) can be used, as only one observation concept exists per ADAO
study.

Use of a time series of spatial observations
++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: VectorSerie
.. index:: single: DataFile

This refers to a vector ordered series of observations, dependent on space and
time. At a given instant, it is assumed that only the observations of the
current and previous instants are known. The successive observations in time
are indexed by :math:`n`, their instant of existence or of reference. This can
for example be a spatial field of measurements, physically homogeneous or not,
of which we consider a history.

- The mathematical representation is :math:`\forall\,n\in\{0...N\},\,\mathbf{y}^o_n\,\in\mbox{I\hspace{-.15em}R}^d`.

- The canonical numerical representation is **an ordered series of vectors**.

- The numerical representation in ADAO is done with the keyword
  "*VectorSeries*". The current indexing of the information is used to
  represent the time index when declaring in one of the following
  representations, and the information is transformed into an ordered series of
  vectors (note: lists and tuples are equivalent):

    - "*list*" of "*numpy.array*"       : ``[numpy.array([1,2,3]), numpy.array([1,2,3])]``
    - "*numpy.array*" of "*list*"       : ``numpy.array([[1,2,3], [1,2,3]])``
    - "*list*" of "*list*"              : ``[[1,2,3], [1,2,3]]``
    - "*list*" of string variables      : ``['1 2 3', '1 2 3']``
    - "*list*" of string variables      : ``['1;2;3', '1;2;3']``
    - "*list*" of string variables      : ``['[1,2,3]', '[1,2,3]']``
    - string of "*list*"                : ``'[[1,2,3], [1,2,3]]'``
    - string of "*list*"                : ``'1 2 3 ; 1 2 3'``
    - Python data file, with variable "*Observation*" in the namespace, indicated by the keyword "*Script*" with the condition ``VectorSerie=True``
    - data text file (TXT, CSV, TSV), with variable pointer by name in column or row, indicated by the keyword "*DataFile*" with the condition ``VectorSerie=True``
    - binary data file (NPY, NPZ), with variable pointer by name, indicated by the keyword "*DataFile*" with the condition ``VectorSerie=True``

- Examples of statements in TUI interface:

    - ``case.setObservation( VectorSerie = [[1,2,3], [1,2,3]] )``
    - ``case.setObservation( VectorSerie = [numpy.array([1,2,3]), numpy.array([1,2,3])] )``
    - ``case.setObservation( VectorSerie =  ['1 2 3', '1 2 3'] )``
    - ``case.setObservation( VectorSerie =  '[[1,2,3], [1,2,3]]' )``
    - ``case.setObservation( VectorSerie =  '1 2 3 ; 1 2 3' )``
    - ``case.setObservation( VectorSerie=True, Script = 'script.py' )```
    - ``case.setObservation( VectorSerie=True, DataFile = 'data.csv' )```
    - ``case.setObservation( VectorSerie=True, DataFile = 'data.npy' )```

Use note: in a given study, only the last record (whether a single vector or a
series of vectors) can be used, as only one observation concept exists per ADAO
study.

Use of a single spatio-temporal observation
+++++++++++++++++++++++++++++++++++++++++++

This single spatio-temporal observation is similar to the previous one in its
representation as a vector series, but it imposes that it must be used in a
single run, i.e. by being fully known at the beginning of the algorithmic
analysis. It can therefore be represented as an indexed series, in the same way
as for a `Use of a time series of spatial observations`_.

Use of a parameterized series of spatial observations
+++++++++++++++++++++++++++++++++++++++++++++++++++++

One represents now a collection of observations parameterized by an index or a
discrete parameter. This form is still similar to the previous one. It is
therefore representable as an indexed series, in the same way as for a `Use of
a time series of spatial observations`_.

General comments on the observations
++++++++++++++++++++++++++++++++++++

.. warning::

  When the assimilation explicitly establishes a **temporal iterative
  process**, as in state data assimilation, **the first observation is not used
  but must be present in the data description of a ADAO case**. By convention,
  it is therefore considered to be available at the same time as the draft time
  value, and does not lead to a correction at that time. The numbering of the
  observations starts at 0 by convention, so it is only from number 1 that the
  observation values are used in the temporal iterative algorithms.

Observations can be provided by single time steps or by successive windows for
iterative algorithms. In this case, a series of observations must be provided
for each algorithmic iteration relative to a time window. In practice, for each
window, we provide a series as in a `Use of a time series of spatial
observations`_.

The observation acquisition options are richer in the TUI textual interface, as
not all options are necessarily available in the GUI.

For data entry via files, please refer to the description of the possibilities
around the keyword "*DataFile*" in the :ref:`section_ref_entry_types_info`.
