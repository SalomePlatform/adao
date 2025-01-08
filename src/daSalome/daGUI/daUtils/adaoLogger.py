# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2025 EDF R&D
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

from salome.kernel.logger import Logger
from salome.kernel import termcolor

adao_logger = Logger("ADAO")
adao_engine_logger = Logger("ADAO ENGINE")

def info(msg, logger = "ADAO"):

  if logger == "ADAO":
    adao_logger.setColor(termcolor.BLUE)
    adao_logger.info(msg)
  elif logger == "ENGINE":
    adao_engine_logger.setColor(termcolor.BLUE)
    adao_engine_logger.info(msg)

def debug(msg, logger = "ADAO"):

  if logger == "ADAO":
    adao_logger.setColor(termcolor.GREEN)
    adao_logger.debug(msg)
  elif logger == "ENGINE":
    adao_engine_logger.setColor(termcolor.GREEN)
    adao_engine_logger.debug(msg)

def error(msg, logger = "ADAO"):

  if logger == "ADAO":
    adao_logger.setColor(termcolor.RED)
    adao_logger.error(msg)
  elif logger == "ENGINE":
    adao_engine_logger.setColor(termcolor.RED)
    adao_engine_logger.error(msg)

def warning(msg, logger = "ADAO"):

  if logger == "ADAO":
    adao_logger.setColor(termcolor.CYAN)
    adao_logger.warning(msg)
  elif logger == "ENGINE":
    adao_engine_logger.setColor(termcolor.CYAN)
    adao_engine_logger.warning(msg)
