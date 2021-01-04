# Copyright (C) 2008-2021 EDF R&D
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

BUILT_SOURCES = ADAO_COMPONENTSK.cc
IDL_FILES=ADAO_COMPONENT.idl

lib_LTLIBRARIES = libADAO_COMPONENT.la
salomeidl_DATA = $(IDL_FILES)
salomepython_DATA = ADAO_COMPONENT_idl.py
libADAO_COMPONENT_la_SOURCES      =
nodist_libADAO_COMPONENT_la_SOURCES = ADAO_COMPONENTSK.cc
nodist_salomeinclude_HEADERS= ADAO_COMPONENT.hh
libADAO_COMPONENT_la_CXXFLAGS     = -I.  $(KERNEL_INCLUDES)
libADAO_COMPONENT_la_LIBADD     = $(KERNEL_LIBS)
##########################################################
%SK.cc %.hh : %.idl
	$(OMNIORB_IDL) -bcxx $(IDLCXXFLAGS) $(OMNIORB_IDLCXXFLAGS) $(IDL_INCLUDES) $<
%_idl.py : %.idl
	$(OMNIORB_IDL) -bpython $(IDL_INCLUDES)  $<
%PaCO.hxx %PaCO.cxx : %.idl %.xml
	$(OMNIORB_IDL) -I@KERNEL_ROOT_DIR@/idl/salome -p@PACOPATH@/lib/python -bpaco -Wb$(top_srcdir)/idl/$*.xml,$(srcdir):@PACOPATH@/idl:@KERNEL_ROOT_DIR@/idl/salome $(top_srcdir)/idl/$*.idl

CLEANFILES = *.hh *SK.cc *.py *.hxx *.cxx

EXTRA_DIST = $(IDL_FILES)

clean-local:
	rm -rf ADAO_COMPONENT ADAO_COMPONENT__POA

install-data-local:
	${mkinstalldirs} $(DESTDIR)$(salomepythondir)
	cp -R ADAO_COMPONENT ADAO_COMPONENT__POA $(DESTDIR)$(salomepythondir)

uninstall-local:
	rm -rf $(DESTDIR)$(salomepythondir)/ADAO_COMPONENT
	rm -rf $(DESTDIR)$(salomepythondir)/ADAO_COMPONENT__POA
