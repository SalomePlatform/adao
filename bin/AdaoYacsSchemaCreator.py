# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2024 EDF R&D
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

import os, sys, logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)-8s %(message)s')

logging.debug("-- Starting AdaoYacsSchemaCreator --")

# Check some basics variables
if "ADAO_ENGINE_ROOT_DIR" not in os.environ:
    logging.fatal("You have to define ADAO_ENGINE_ROOT_DIR")
    sys.exit(1)

try:
    import adao
    from daYacsSchemaCreator import run
except ImportError as e:
    logging.fatal("\n  Import of YACS schema creator module failed, the error message is:\n" +
                  "\n  %s\n"%(e,) +
                  "\n  Add its installation directory in your PYTHONPATH.\n")
    sys.exit(1)

# Parse arguments
from argparse import ArgumentParser
usage = "usage: %(prog)s [options] config_file yacs_schema_filename"
my_parser = ArgumentParser(usage=usage)
my_parser.add_argument('config_file')
my_parser.add_argument('yacs_schema_filename')
args = my_parser.parse_args()

if os.path.dirname(args.config_file) != '':
    # Ajout dans le sys.path pour permettre l'import des fichiers inclus
    sys.path.insert(0, os.path.dirname(args.config_file))

run.create_schema_from_file(args.config_file, args.yacs_schema_filename)
