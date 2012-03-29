.. _section_glossary:

Glossary
========

.. glossary::
   :sorted:

   case
      One case is defined by a set of data and of choices, packed together
      through the user interface of the module. The data are physical
      measurements that have to be available before or during the case
      execution. The simulation code(s) and the assimilation methods and
      parameters has to be chosen, they define the execution properties of the
      case.

   iteration
      One iteration occurs when using iterative optimizers (e.g. 3DVAR), and it
      is entirely hidden in the main YACS OptimizerLoop Node named
      "compute_bloc". Nevertheless, the user can watch the iterative process
      throught the *YACS Container Log* window, which is updated during the
      process, and using *Observers* attached to calculation variables.
