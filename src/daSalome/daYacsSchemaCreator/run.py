#-*- coding: utf-8 -*-
#
# Copyright (C) 2008-2020 EDF R&D
#
# This file is part of SALOME ADAO module
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
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

import sys
import os
import traceback
import logging
import tempfile
from daYacsSchemaCreator.methods import *
from daYacsSchemaCreator.help_methods import *

def create_schema(config_file, config_content, yacs_schema_filename):

    if config_file is not None and config_content is None:
      # Import config_file
      try:
        (fd, filename) = tempfile.mkstemp()
        exec(compile(open(config_file).read(), filename, 'exec'))
      except Exception as e:
        if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
        else: msg = ""
        raise ValueError("\n\nexception in loading %s\n\nThe following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal.\n"%(config_file,str(e),msg))
    elif config_file is None and config_content is not None:
      # Import config_content
      try:
        (fd, filename) = tempfile.mkstemp()
        exec(compile(config_content, filename, 'exec'))
      except Exception as e:
        if isinstance(e, SyntaxError): msg = "at %s: %s"%(e.offset, e.text)
        else: msg = ""
        raise ValueError("\n\nexception in loading the config content\n\nThe following error occurs:\n\n%s %s\n\nSee also the potential messages, which can show the origin of the above error, in the launching terminal.\n"%(str(e),msg))
    else:
        raise ValueError("Error in schema creation, file or content has to be given")

    if "study_config" not in locals():
        raise ValueError("\n\n Cannot find study_config in %s\n"%str(config_file))
    else:
        globals()['study_config'] = locals()['study_config']

    check_study(study_config)
    proc = create_yacs_proc(study_config)
    write_yacs_proc(proc, yacs_schema_filename)

def create_schema_from_file(config_file, yacs_schema_filename):
    create_schema(config_file, None, yacs_schema_filename)

def create_schema_from_content(config_content, yacs_schema_filename):
    create_schema(None, config_content, yacs_schema_filename)
