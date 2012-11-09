.. _section_using:

================================================================================
Using the ADAO module
================================================================================

.. |eficas_new| image:: images/eficas_new.png
   :align: middle
.. |eficas_save| image:: images/eficas_save.png
   :align: middle
.. |eficas_yacs| image:: images/eficas_yacs.png
   :align: middle

This section presents the usage of the ADAO module in SALOME. It is complemented
by advanced usage procedures in the section :ref:`section_advanced`, and by
examples in the section :ref:`section_examples`.

Logical procedure to build an ADAO test case
--------------------------------------------

The construction of an ADAO case follows a simple approach to define the set of
input data, and then generates a complete executable block diagram used in YACS.
Many variations exist for the definition of input data, but the logical sequence
remains unchanged.

First of all, the user is considered to know its personnal input data needed to
set up the data assimilation study. These data can already be available in
SALOME or not.

**Basically, the procedure of using ADAO involves the following steps:**

#.  **Activate the ADAO module and use the editor GUI,**
#.  **Build and/or modify the ADAO case and save it,**
#.  **Export the ADAO case as a YACS scheme,**
#.  **Modify and supplement the YACS scheme and save it,**
#.  **Execute the YACS case and obtain the results.**

Each step will be detailed in the next section.

Detailed procedure to build an ADAO test case
---------------------------------------------

Activate the ADAO module and use the editor GUI
+++++++++++++++++++++++++++++++++++++++++++++++

As always for a module, it has to be activated by choosing the appropriate
module button (or menu) in the toolbar of SALOME. If there is no SALOME study
loaded, a popup appears, allowing to choose between creating a new study, or
opening an already existing one:

  .. _adao_activate1:
  .. image:: images/adao_activate.png
    :align: center
  .. centered::
    **Activating the module ADAO in SALOME**

Choosing the "*New*" button, an embedded case editor EFICAS [#]_ will be opened,
along with the standard "*Object browser*". You can then click on the "*New*"
button |eficas_new| (or choose the "*New*" entry in the "*ADAO*" main menu) to
create a new ADAO case, and you will see:

  .. _adao_viewer:
  .. image:: images/adao_viewer.png
    :align: center
    :width: 100%
  .. centered::
    **The EFICAS editor for cases definition in module ADAO**

It is a good habit to save the ADAO case now, by pushing the "*Save*" button
|eficas_save| or by choosing the "*Save/Save as*" entry in the "*ADAO*" menu.
You will be prompted for a location in your file tree and a name, that will be
completed by a "*.comm*" extension used for JDC EFICAS files.

Build and modify the ADAO case and save it
++++++++++++++++++++++++++++++++++++++++++

To build a case using EFICAS, you have to go through a series of steps, by
selecting a keyword and then filling in its value.

The structured editor indicates hierarchical types, values or keywords allowed.
Incomplete or incorrect keywords are identified by a visual error red flag.
Possible values are indicated for keywords defined with a limited list of
values, and adapted entries are given for the other keywords. All the mandatory
command or keyword are already present, and optionnal commands can be added.

A new case is set up with the minimal list of commands. No mandatory command can
be suppressed, but others can be added as allowed keywords for an
"*ASSIMILATION_STUDY*" command. As an example, one can add an
"*AlgorithmParameters*" keyword, as described in the last part of the section
:ref:`section_examples`.

At the end, when all fields or keywords have been correctly defined, each line
of the commands tree must have a green flag. This indicates that the whole case
is valid and completed.

  .. _adao_jdcexample00:
  .. image:: images/adao_jdcexample01.png
    :align: center
    :width: 50%
  .. centered::
    **Example of a valid ADAO case**

Finally, you have to save your ADAO case by pushing the "*Save*" button
|eficas_save| or by choosing the "*Save/Save as*" entry in the "*ADAO*" menu.

Export the ADAO case as a YACS scheme
+++++++++++++++++++++++++++++++++++++

When the ADAO case is completed, you have to export it as a YACS scheme [#]_ in
order to execute the data assimilation calculation. This can be easily done by
using the "*Export to YACS*" button |eficas_yacs|, or equivalently choose the
"*Export to YACS*" entry in the "*ADAO*" main menu, or in the contextual case
menu in the object browser.

  .. _adao_exporttoyacs01:
  .. image:: images/adao_exporttoyacs.png
    :align: center
    :scale: 75%
  .. centered::
    **"Export to YACS" sub-menu to generate the YACS scheme from the ADAO case**

This will lead to automatically generate an XML file for the YACS scheme, and
open YACS module on this file. The YACS file will be stored in the same
directory and with the same name as the ADAO saved case, only changing its
extension from "*.comm*" to "*.xml*". *Be careful, if the name already exist, it
will overwrite it without prompting for replacing the file*. In the same time,
an intermediary python file is also stored in the same place, with a "*.py*"
extension replacing the "*.comm*" one [#]_.

Modify and supplement the YACS scheme and save it
+++++++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Analysis

When the YACS scheme is generated and opened in SALOME through the YACS module
GUI, you can modify or supplement the scheme like any YACS scheme. It is
recommended to save the modified scheme with a new name, in order to preserve in
the case you re-export to YACS the ADAO case.

The main supplement needed in the YACS scheme is a postprocessing step. The
evaluation of the results has to be done in the physical context of the
simulation used by the data assimilation procedure.

The YACS scheme has an "*algoResults*" output port of the computation bloc,
which gives access to a "*pyobj*" containing all the results. These results can
be obtained by retrieving the named variables stored along the calculation. The
main is the "*Analysis*" one, that can be obtained by the python command (for
example in an in-line script node)::

    Analysis = results.ADD.get("Analysis").valueserie(-1)

This is a complex object, similar to a list of values calculated at each step of
data assimilation calculation. In order to get the last data assimilation
analysis, one can use::

    Xa = results.ADD.get("Analysis").valueserie(-1)

This ``Xa`` is a vector of values, that represents the solution of the data
assimilation evaluation problem, noted as :math:`\mathbf{x}^a` in the section
:ref:`section_theory`.

Such command can be used to print results, or to convert these ones to
structures that can be used in the native or external SALOME postprocessing. A
simple example is given in the section :ref:`section_examples`.

Execute the YACS case and obtain the results
++++++++++++++++++++++++++++++++++++++++++++

.. index:: single: Analysis
.. index:: single: Innovation
.. index:: single: APosterioriCovariance
.. index:: single: OMB (Observation minus Background)
.. index:: single: BMA (Background minus Analysis)
.. index:: single: OMA (Observation minus Analysis)
.. index:: single: CostFunctionJ
.. index:: single: CostFunctionJo
.. index:: single: CostFunctionJb

The YACS scheme is now complete and can be executed. Parametrisation and
execution of a YACS case is fully compliant with the standard way to deal with a
YACS scheme, and is described in the *YACS module User's Guide*.

Results can be obtained, through the "*algoResults*" output port, using YACS
nodes to retrieve all the informations in the "*pyobj*" object, to transform
them, to convert them, to save part of them, etc.

The data assimilation results and complementary calculations can be retrieved
using the "*get*" method af the "*algoResults.ADD*" object. This method pick the
different output variables identified by their name. Indicating in parenthesis
their availability as automatic (for every algorithm) or optional (depending on
the algorithm), and their notation coming from section :ref:`section_theory`,
the main available output variables are the following:

#.  "Analysis" (automatic): the control state evaluated by the data assimilation
    procedure, noted as :math:`\mathbf{x}^a`.
#.  "Innovation" (automatic): the difference between the observations and the
    control state transformed by the observation operator, noted as
    :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^b`.
#.  "APosterioriCovariance" (optional): the covariance matrix of the *a
    posteriori* analysis errors, noted as :math:`\mathbf{A}`.
#.  "OMB" (optional): the difference between the observations and the
    background, similar to the innovation.
#.  "BMA" (optional): the difference between the background and the analysis,
    noted as :math:`\mathbf{x}^b - \mathbf{x}^a`.
#.  "OMA" (optional): the difference between the observations and the analysis,
    noted as :math:`\mathbf{y}^o - \mathbf{H}\mathbf{x}^a`.
#.  "CostFunctionJ" (optional): the minimisation function, noted as :math:`J`.
#.  "CostFunctionJo" (optional): the observation part of the minimisation
    function, noted as :math:`J^o`.
#.  "CostFunctionJb" (optional): the background part of the minimisation
    function, noted as :math:`J^b`.

Input variables are also available as output in order to gather all the
information at the end of the procedure.

All the variables are list of typed values, each item of the list
corresponding to the value of the variable at a time step or an iteration step
in the data assimilation optimization procedure. The variable value at a given
"*i*" step can be obtained by the method "*valueserie(i)*". The last one
(consisting in the solution of the evaluation problem) can be obtained using the
step "*-1*" as in a standard list.

.. [#] For more information on EFICAS, see the *EFICAS module* available in SALOME GUI.

.. [#] For more information on YACS, see the *YACS module User's Guide* available in the main "*Help*" menu of SALOME GUI.

.. [#] This intermediary python file can be safely removed after YACS export, but can also be used as described in the section :ref:`section_advanced`.
