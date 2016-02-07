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

EXTRA_DIST = daCore daAlgorithms daDiagnostics  daExternals  daMatrices  daNumerics

DIR = $(top_srcdir)/src/daComposant/

install-data-local:
	${mkinstalldirs} $(DESTDIR)$(salomepythondir)
	cp -R $(DIR)daCore $(DESTDIR)$(salomepythondir)
	cp -R $(DIR)daAlgorithms $(DESTDIR)$(salomepythondir)
	cp -R $(DIR)daDiagnostics $(DESTDIR)$(salomepythondir)
	cp -R $(DIR)daNumerics $(DESTDIR)$(salomepythondir)

uninstall-local:
	chmod -R +w $(DESTDIR)$(salomepythondir)
	rm -rf $(DESTDIR)$(salomepythondir)/daCore
	rm -rf $(DESTDIR)$(salomepythondir)/daAlgorithms
	rm -rf $(DESTDIR)$(salomepythondir)/daDiagnostics
	rm -rf $(DESTDIR)$(salomepythondir)/daNumerics
