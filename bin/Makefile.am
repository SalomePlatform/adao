# Copyright (C) 2010-2012 EDF R&D
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

bin_SCRIPTS = AdaoYacsSchemaCreator.py qtEficas_adao_study.py AdaoCatalogGenerator.py

EXTRA_DIST = AdaoYacsSchemaCreator.py qtEficas_adao_study.py.in AdaoCatalogGenerator.py

install-data-hook:
	@export PYTHONPATH=$(DESTDIR)${salomepythondir}:${PYTHONPATH} && python $(top_srcdir)/bin/AdaoCatalogGenerator.py $(DESTDIR)${salomepythondir}/daEficas ADAO_Cata_V0.py

uninstall-hook:
	@rm  $(DESTDIR)${salomepythondir}/daEficas/ADAO_Cata_V0.py
