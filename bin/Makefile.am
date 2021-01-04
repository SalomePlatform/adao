# Copyright (C) 2008-2021 EDF R&D
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

bin_SCRIPTS = AdaoYacsSchemaCreator.py gui_Adao_QT_Eficas.py # AdaoCatalogGenerator.py module_version.py

EXTRA_DIST = AdaoYacsSchemaCreator.py gui_Adao_QT_Eficas.py # AdaoCatalogGenerator.py module_version.py

ADAODIR = $(DESTDIR)$(salomepythondir)/adao

install-data-hook:
	@export PYTHONPATH="$(DESTDIR)${salomepythondir}:${PYTHONPATH}" && python${PYTHON_VERSION} $(top_srcdir)/bin/AdaoCatalogGenerator.py $(ADAODIR)/daEficas ADAO_Cata_V0.py
	@chmod 755 $(top_srcdir)/bin/gui_Adao_QT_Eficas.py

uninstall-hook:
	@rm $(ADAODIR)/daEficas/ADAO_Cata_V0.py
