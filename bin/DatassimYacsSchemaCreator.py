#!/usr/bin/python
#-*-coding:iso-8859-1-*-
#  Copyright (C) 2008-2009  EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# --
# Author : André RIBES (EDF R&D)
# --

import sys
import os
import traceback
import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

print "-- Starting DatassimYacsSchemaCreator --"

# Check some basics variables
if "DATASSIM_ROOT_DIR" not in os.environ:
  logging.fatal("You have to define DATASSIM_ROOT_DIR")
  sys.exit(1)

try:
  from daYacsSchemaCreator.run import *
  from daYacsSchemaCreator.help_methods import *
except:
  logging.fatal("Import of DATASSIM python modules failed !" +
                "\n add DATASSIM python installation directory in your PYTHONPATH")
  traceback.print_exc()
  sys.exit(1)

# Parse arguments
from optparse import OptionParser
usage = "usage: %prog [options] config_file yacs_schema_filename"
version="%prog 0.1"
my_parser = OptionParser(usage=usage, version=version)
(options, args) = my_parser.parse_args()
check_args(args)

config_file =  args[0]
yacs_schema_filename =  args[1]
create_schema(config_file, yacs_schema_filename)
