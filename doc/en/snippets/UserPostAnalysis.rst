.. index:: single: UserPostAnalysis
.. index:: single: UserPostAnalysis Template

UserPostAnalysis
  *Multiline string*. This variable allows to process some parameters or data
  automatically after data assimilation or optimization algorithm processing.
  Its value is defined either as a predefined pattern name, or as a script file
  name, or as a string, allowing to put post-processing code directly inside
  the ADAO case. Common templates are provided to help the user to start or to
  quickly make his case. We refer to the description of
  :ref:`section_ref_userpostanalysis_requirements` for the list of templates
  and their format. Important note: this processing is only performed when the
  case is executed in TUI or exported to YACS.
