================================================================================
Using the module ADAO
================================================================================

This section presents the usage of the ADAO module in SALOME.

Logical procedure to build an ADAO test case
--------------------------------------------------------------------------------

The construction of an ADAO case follows a simple approach to define the set of
input data, either static or dynamic data, and then generates a complete block
diagram used in Y. Many variations exist for the definition of input data, but
the logical sequence remains unchanged.

First of all, the user is considered to know the input data needed to set up the
data assimilation study. These data can be in SALOME or not.

**Basically, the procedure involves the following steps:**

#.      **Activate the ADAO module and use the editor GUI,**
#.      **Build and modify the ADAO case and save it,**
#.      **Export the ADAO case as a YACS scheme,**
#.      **Modify and supplement the YACS scheme and save it,**
#.      **Execute the YACS case and obtain the results.**

Each step will be detailed later in the next section.

Detailed procedure to build an ADAO test case
--------------------------------------------------------------------------------

Activate the ADAO module and use the editor GUI
++++++++++++++++++++++++++++++++++++++++

As always for a module, it has to be activated by choosing the appropriate
module button (or menu) in the toolbar of SALOME. A popup appears, allowing to
choose between creating a new study, or opening an already existing one:

  .. _adao_activate:
  .. image:: images/adao_activate.png
    :align: center
  .. centered::
    **Activating the module ADAO in SALOME**

.. |eficas_new| image:: images/eficas_new.png
   :align: middle
.. |eficas_save| image:: images/eficas_save.png
   :align: middle

Choosing the "*New*" button, an embedded case editor EFICAS [#]_ will be opened,
along with the standard "*Object browser*". You can then click on the "*New*"
button |eficas_new| (or choose the "*New*" entry in the "*File*" menu) to create
a new ADAO case, and you will see:

  .. _adao_viewer:
  .. image:: images/adao_viewer.png
    :align: center
    :width: 100%
  .. centered::
    **The EFICAS editor for cases definition in module ADAO**

It is a good habit to save the ADAO case now, by pushing the "*Save*" button
|eficas_save| or by choosing the "*Save/Save as*" entry in the "*File*" menu.
You will be prompted for a location in your file tree and a name, that will be
completed by a "*.comm*" extension used for JDC EFICAS files.

Build and modify the ADAO case and save it
++++++++++++++++++++++++++++++++++++++++

To build a case using EFICAS, you have to go through a series of steps for
selecting a keyword and then filling in its value. The structured editor
indicates hierarchical types, values or keywords allowed. Incomplete or
incorrect keywords are identified by a visual error red flag.






At the end, you have to save your ADAO case.

Export the ADAO case as a YACS scheme
++++++++++++++++++++++++++++++++++++++++



Modify and supplement the YACS scheme and save it
++++++++++++++++++++++++++++++++++++++++


Execute the YACS case and obtain the results
++++++++++++++++++++++++++++++++++++++++






Reference description of the commands and keywords available throught the GUI
--------------------------------------------------------------------------------

--TODO--


ASSIM_STUDY

String

Script

Vector

Matrix

Function

Dict

Background

BackgroundError

Observation

ObservationError

ObservationOperator

AlgorithmParameters

Algorithm : "ThreeDVAR", "Blue", "EnsembleBlue", "Kalman"...

.. [#] For more information on EFICAS, see the the *EFICAS User Guide* available in the main "*Help*" menu of SALOME GUI.

