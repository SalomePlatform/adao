include $(top_srcdir)/adm_local/make_common_starter.am

EXTRA_DIST = daCore

DIR = $(top_srcdir)/src/daComposant/

install-data-local:
	${mkinstalldirs} $(DESTDIR)$(salomepythondir)
	cp -R $(DIR)daCore $(DESTDIR)$(salomepythondir)

uninstall-local:
	chmod -R +w $(DESTDIR)$(salomepythondir)/daCore
	rm -rf $(DESTDIR)$(salomepythondir)/daCore
