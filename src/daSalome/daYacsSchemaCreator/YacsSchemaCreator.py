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
from optparse import OptionParser
from daYacsSchemaCreator.methods import *
from daYacsSchemaCreator.help_methods import *

# Variables globales
global my_parser

# Init part
def init():

  logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
  usage = "usage: %prog [options] config_file yacs_schema_filename"
  version="%prog 0.1"
  global my_parser
  my_parser = OptionParser(usage=usage, version=version)

# Start application
def main():

  print "-- Starting YacsSchemaCreator --"
  (options, args) = my_parser.parse_args()
  check_args(args)
  config_file =  args[0]
  yacs_schema_filename =  args[1]

  # Import config_file
  try:
    execfile(config_file)
  except:
    logging.fatal("Exception in loading " + config_file)
    traceback.print_exc()
    sys.exit(1)

  if "study_config" not in locals():
    logging.fatal("Cannot found study_config in " + str(config_file))
    sys.exit(1)
  else:
    globals()['study_config'] = locals()['study_config']

  if "DATASSIM_ROOT_DIR" not in os.environ:
    logging.fatal("You have to define DATASSIM_ROOT_DIR")
    sys.exit(1)

  check_study(study_config)
  proc = create_yacs_proc(study_config)
  write_yacs_proc(proc, yacs_schema_filename)

init()
main()
