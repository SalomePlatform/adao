# Copyright (C) 2008-2024 EDF R&D
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

include $(top_srcdir)/adm_local/make_common_starter.am

SUBDIRS =

if SALOME_MODULE
SUBDIRS += idl
endif

SUBDIRS += src

if SALOME_MODULE
SUBDIRS += resources bin examples test i18n
endif

if SPHINX_IS_OK
SUBDIRS += doc
endif

ACLOCAL_AMFLAGS = -I adm_local -I ${KERNEL_ROOT_DIR}/salome_adm/unix/config_files

EXTRA_DIST = autogen.sh
