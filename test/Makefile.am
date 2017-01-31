# Copyright (C) 2008-2017 EDF R&D
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

include $(top_srcdir)/adm_local/make_common_starter.am

EXTRA_DIST = test1001 test1002 test6701 test6702 test6703 test6901 test6902 CTestTestfileInstall.cmake.in

DIR = $(top_srcdir)/test/

SALOMETESTDIR=$(DESTDIR)$(bindir)/test

install-data-local:
	${mkinstalldirs} $(SALOMETESTDIR)
	cp -R $(DIR)test1001 $(SALOMETESTDIR)
	cp -R $(DIR)test1002 $(SALOMETESTDIR)
	cp -R $(DIR)test6701 $(SALOMETESTDIR)
	cp -R $(DIR)test6702 $(SALOMETESTDIR)
	cp -R $(DIR)test6703 $(SALOMETESTDIR)
	cp -R $(DIR)test6901 $(SALOMETESTDIR)
	cp -R $(DIR)test6902 $(SALOMETESTDIR)
	cp    $(DIR)CTestTestfileInstall.cmake.in $(SALOMETESTDIR)/CTestTestfile.cmake

uninstall-local:
	chmod -R +w $(SALOMETESTDIR)
	rm -rf $(SALOMETESTDIR)/test1001
	rm -rf $(SALOMETESTDIR)/test1002
	rm -rf $(SALOMETESTDIR)/test6701
	rm -rf $(SALOMETESTDIR)/test6702
	rm -rf $(SALOMETESTDIR)/test6703
	rm -rf $(SALOMETESTDIR)/test6901
	rm -rf $(SALOMETESTDIR)/test6902
	rm     $(SALOMETESTDIR)/CTestTestfile.cmake
