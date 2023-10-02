.. index:: single: InterpolationByReducedModelTask (example)

First example
.............

This example describes the implementation of a reconstruction by interpolation,
following the building of a reduced representation by an **optimal measurement
positioning** search task.

To illustrate, we use the very simple artificial fields (generated in such a
way as to exist in a vector space of dimension 2) that for the :ref:`study
examples with
"MeasurementsOptimalPositioningTask"<section_ref_algorithm_MeasurementsOptimalPositioningTask_examples>`.
The preliminary ADAO search yields 2 optimal positions for the measurements,
which are then used to establish a physical field interpolation based on
measurements at the optimum locations.
