# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2025 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Author: Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D
# Author: Luis Corona Mesa-Molles, luis.corona-mesa-molles@edf.fr, EDF R&D

__doc__ = """
This module leads to easy calibration of a dynamical model from DYMOLA or
Modelica, with respect to experimental measurements, with the help of
optimization algorithms available in ADAO tool.

SYNOPSIS
--------

The most simple use of the module, using default arguments and files living in
the current directory, is the following:

    from modelica_calibration.case import Calibration
    import os
    newcase = Calibration()
    resultats = newcase.calibrate(
        DataName             = "measures.txt",
        ModelName            = os.path.join("Models","dymosim.exe"),
        MethodName           = "parameters.py",
        VariablesToCalibrate = ["COP_val","hVE_val","PEE_val","hEE_val"],
        OutputVariables      = ["proeeF.T","Ev.P","prospC.T","Sp.Q","proseF.T"],
    )
    print()
    for k,v in resultats.items():
        print("%18s = %s"%(k,v))
    print()

ARGUMENTS TO BE GIVEN AS INPUT FOR "CALIBRATE" TASK
---------------------------------------------------

The "calibrate" method is used to set and realize a calibration (optimal
estimation task) of model parameters using measures data. It can be directly
called with all the input arguments to set the full calibration problem.

The input arguments are the following named ones. They are not all required,
and can be divided in category.

Category: dynamic model description

    ModelName............: required file (or directory name that contains the
        files) for the dynamic model.
        (default None)

    ModelFormat..........: this indicates the format of the dynamic model. It
        can be given as a Dymola executable pair "dymosim.exe/dsin.txt".
        (default "GUESS", allowed "DYMOSIM", "PYSIM", "GUESS")

Category: measures description

    DataName.............: required file name for measures
        (default None)

    DataFormat...........: this indicates the format of the measures, given as
        columns of chronological series, with the same column names that are
        used for variables in the output of the model simulation.
        (default "GUESS", allowed "TXT", "CSV", "TSV", "GUESS")

Category: initial/background values description

    BackgroundName.......: file name for initial/background. If no file name is
        given, it is assumed that the initial value will come from model.
        (default None)

    BackgroundFormat.....: this indicates the source of the initial values used
        as background ones. The background values can be read in ADAO, DSIN or
        USER format. The priority is "USER", then "ADAO", then "DSIN".
        (default "GUESS", allowed "ADAO", "DSIN", "USER", "GUESS")

Category: calibration method description

    MethodName...........: file name for ADAO parameters
        (default None)

    MethodFormat.........: this indicates the format of the assimilation
        parameters, excluding background.
        (default "ADAO", allowed "ADAO")

    VariablesToCalibrate.: model names to calibrate, that have to exist as
        input variables in the model description.
        (default None)

    OutputVariables......: model names of result to compare to measures, that
        have to exist as output variables in the model description.
        (default None)

Category: results description

    ResultName...........: required file name for writing results.
        (default "results.txt")

    ResultFormat.........: this indicates the format of the result output.
        (default "GUESS", allowed "TXT", "PY", "GUESS")

    ResultLevel..........: quantity of results that will be retrieved. By
        default, it will always write at least the calibration results.
        (default None, allowed None="Final", "Final", "IntermediaryFinal")

    Verbose..............: True or False
        (default False)

ARGUMENTS OUTPUT THAT CAN BE OBTAINDED FOR "CALIBRATE" TASK
-----------------------------------------------------------

The output results are returned at the end of the calibration process, and
evantually during it. The output will be at least written in a file, and in the
same time returned in a python dictionary containing result information. The
dictionnary entries are the following ones:

    NamesOfParameters....: names of the individual parameter variables to be
        calibrated.

    InitialParameters....: initial or background parameter set, as known before
        calibration. If it is given by the user, it can differ from the initial
        model values embedded in the model.

    OptimalParameters....: optimal parameter set, as known after calibration.


    NamesOfMeasures......: names of the measures subsets used for the
        calibration.

    Measures.............: measures subsets used for calibration

    OptimalSimulation....: simulation results obtained with optimal parameter
        set, using the model. It can be directly compared to measures.

HOW TO DESCRIBE A DYNAMIC MODEL?
--------------------------------

Model can be given either by the name of the model parameter file (e.g.
"dsin.txt") with absolute or relative path, or by the directory where live the
DYMOLA compiled executable "dymosim.exe" and the parameters file "dsin.txt".

HOW TO DESCRIBE THE MEASURES?
-----------------------------

Measures can be given by colums files, with named colums, in TXT, CVS or TSV
file types (with respective delimiters "space", ";" and "tab" and respective
file extension ".txt", ".csv" and ".tsv"). Beginning lines with "#" indicates a
comment line, with the first uncommented line having to present the names of the
columns variables if available.

Example of a TXT file:
    # Measures text file
    #
    Date Heure Variable1 Variable2
    22/04/2018 8:0:0   295    0.01
    23/04/2018 8:0:0   296    0.01
    24/04/2018 8:0:0   294    0.01
    25/04/2018 8:0:0   293    0.001
    26/04/2018 8:0:0   295    0.01
    27/04/2018 8:0:0   297    0.5

Example of a CSV file:
    # Measures text file
    #
    Date,Heure,Variable1,Variable2
    22/04/2018,8:0:0,295,0.01
    23/04/2018,8:0:0,296,0.01
    24/04/2018,8:0:0,294,0.01
    25/04/2018,8:0:0,293,0.001
    26/04/2018,8:0:0,295,0.01
    27/04/2018,8:0:0,297,0.5

HOW TO SET CALIBRATION PARAMETERS?
----------------------------------

ADAO parameters can be given by Python file, with named standard variables (see
ADAO documentation for details). All parameters have wise defaults). Error
covariance matrices can be set also in this parameter file.

The variables, that can (but has not to) be set (see ADAO documentation
for details), are:
    Algorithm........: calibration algorithm (default "3DVAR")
    Parameters.......: dictionary of optimization parameters and of
                       optimization bounds (default Model ones)
    BackgroundError..: a priori errors covariance matrix (default 1.)
    ObservationError.: a priori model-observation errors covariance
                       matrix (default 1.)
    Background.......: see below.

Initial values and bounds of the variables to calibrate can be read from user
file, ADAO parameters file or model parameters file, allowing to superseed the
model initial default values. The priority is "USER", then "ADAO", then "DSIN",
and the default one correspond to "DSIN". So the background can be set using
three alternative ways:

    - by reading named parameters in a user file, with 2 (or 4) colums
      describing pairs (or quadruplets) for each variable with the Name, the
      Values (and Min/Max bounds if required). The file can be in CSV or TXT
      format.

      Choice:
          BackgroundFormat = "USER"
          BackgroundName = ...

      Example of CSV file content:
          Name,Value,Minimum,Maximum
          COP_val,1.4,0.2,1
          hVE_val,2321820,0,None
          PEE_val,8.3226E06,0,None
          hEE_val,759483,None,None

    - by reading values and bounds as series in the calibration parameters file
      with the ADAO standard syntax.

      Choice:
          BackgroundFormat = "ADAO"

      Example of subset of Python parameters calibration file:
          Parameters={
              "Bounds":[[0.2,1],[0,None],[0,None],[None,None]],
              }
          Background=[1.4,2321820,8.3226E06,759483]

    - by reading initial values in a model description file as the "dsin.txt"
      for Dymola. In this case, the only information required is the names of
      the calibrated variables as known in Dymola "dsin.txt" file.

      Choice:
          BackgroundFormat = "DSIN"

LICENSE
-------
The license for this tool and its documentation is the GNU Lesser General
Public License (Lesser GPL).

REFERENCES
----------
For more information, see:
    * DYMOLA User documentation
    * ADAO, a module for Data Assimilation and Optimization,
      http://www.salome-platform.org/

"""
__author__ = "Jean-Philippe Argaud, jean-philippe.argaud@edf.fr, EDF R&D"
__all__ = ["case"]
