include $(top_srcdir)/adm_local/make_common_starter.am

bin_SCRIPTS = AdaoYacsSchemaCreator.py qtEficas_adao_study.py AdaoCatalogGenerator.py

EXTRA_DIST = AdaoYacsSchemaCreator.py qtEficas_adao_study.py.in AdaoCatalogGenerator.py

install-data-hook:
	@export PYTHONPATH=$(DESTDIR)${salomepythondir}:${PYTHONPATH} && python $(top_srcdir)/bin/AdaoCatalogGenerator.py $(DESTDIR)${salomepythondir}/daEficas ADAO_Cata_V0.py

uninstall-hook:
	@rm  $(DESTDIR)${salomepythondir}/daEficas/ADAO_Cata_V0.py
