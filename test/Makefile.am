# Copyright (C) 2008-2016 EDF R&D
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

include $(top_srcdir)/adm_local/make_common_starter.am

EXTRA_DIST = test1001 test1002 CTestTestfileInstall.cmake.in

DIR = $(top_srcdir)/test/

SALOMETESTDIR=$(DESTDIR)$(bindir)/test

install-data-local:
	${mkinstalldirs} $(SALOMETESTDIR)
	cp -R $(DIR)test1001 $(SALOMETESTDIR)
	cp -R $(DIR)test1002 $(SALOMETESTDIR)
	cp    $(DIR)CTestTestfileInstall.cmake.in $(SALOMETESTDIR)/CTestTestfile.cmake

uninstall-local:
	chmod -R +w $(SALOMETESTDIR)
	rm -rf $(SALOMETESTDIR)/test1001
	rm -rf $(SALOMETESTDIR)/test1002
	rm     $(SALOMETESTDIR)/CTestTestfile.cmake