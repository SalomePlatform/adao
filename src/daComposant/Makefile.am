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
