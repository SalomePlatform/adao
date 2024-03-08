.. index:: single: DataFile
.. index:: single: ColNames
.. index:: single: ColMajor

**DataFile**, **ColNames**, **ColMajor**
    This indicates data given in an external file. It can be described by a
    full absolute path name or only by the file name without path. If the file
    is given only by a file name without path, and if a study directory is also
    indicated, the file is searched in the given study directory. The content
    of the file can be:

    - in text format (simple text in a file with a ".txt" or ".dat" extension,
      text with comma delimiter in a file with a ".csv" extension, text with
      tabulation delimiter in a file with a ".tsv" extension), named here TXT,
      CSV, TSV or DAT.
    - in binary format (single-variable in a Numpy file with a ".npy"
      extension, multi-variables in a NumpyZ file with a ".npz" extension),
      named here NPY or NPZ.

    By default, the values of a variable has to be ordered in rows to be
    acquired record line by record line ("ColMajor=False"), but they can also
    be ordered in lines to be acquired record row by record row
    ("ColMajor=True").

    Without information or with a void list for the variable names, all the
    values of all the variables are used, but one can also select only the ones
    of the variables that are indicated in the name list "ColNames". The
    variable names are always as header of columns.

    Example of CSV file for "*Observation*" variable in "*DataFile*" ::

        # CSV file with delimiter ";" or ","
        # ==================================
        # Comment line beginning with #
        # The next line is dedicated to variable naming
        Alpha1;Observation;Alpha2
        0.1234;5.6789;9.0123
        1.2345;2.3456;3.
        2.3456;3.4567;4.56
        3.;4.;5.
        4;5;6
        5.123;6.789;7.8

    Example of TXT file for "*Observation*" variable in "*DataFile*" ::

        # Fichier TXT à séparateur espace
        # TXT file with space delimiter
        # =============================
        # Ligne de commentaires quelconques débutant par #
        # Ligne suivante réservée au nommage des variables
        Alpha1 Observation Alpha2
        0.1234 5.6789 9.0123
        1.2345 2.3456 3.
        2.3456 3.4567 4.56
        3.     4.     5.
        4      5      6
        5.123  6.789  7.8

.. warning::

    It is recommended, before using them as an input of this type, to carefully
    check text or binary files. Various checks are carried out on loading, but
    the variety of potential errors is great. In practice, by respecting the
    requirements for naming variables and for comments, text files from
    classical programs or spreadsheets are (most of the time) compatible.
