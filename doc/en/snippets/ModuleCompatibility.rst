The compatibility of the module is furthermore checked against various versions
of Python and support modules like Numpy and Scipy. The range of versions
reached in the tests depends on their availability, and the tests are not
systematically performed on all intermediate versions. For all tested versions,
the ADAO module behaves identically (to the extent of modifications depending
on the support tools). It is strongly discouraged (or impossible) to use ADAO
with a version lower than the minimum version, and there is no limitation to
the use of the ADAO module beyond the reached version (but this remains without
guarantee).

.. csv-table:: Support tool verification intervals for ADAO
   :header: "Tool", "Minimal version", "Reached version"
   :widths: 20, 10, 10

   Python,     3.6.5,    3.10.9
   Numpy,      1.14.3,    1.24.2
   Scipy,      1.1.0,    1.10.0
   MatplotLib, 2.2.2,    3.6.3
   GnuplotPy,  1.8,    1.8
   NLopt,      2.4.2,    2.7.1