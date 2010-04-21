include $(top_srcdir)/adm_local/make_common_starter.am

EXTRA_DIST = daYacsSchemaCreator

DIR = $(top_srcdir)/src/daSalome/

install-data-local:
	${mkinstalldirs} $(DESTDIR)$(salomepythondir)
	cp -R $(DIR)daYacsSchemaCreator $(DESTDIR)$(salomepythondir)

uninstall-local:
	chmod -R +w $(DESTDIR)$(salomepythondir)
	rm -rf $(DESTDIR)$(salomepythondir)/daYacsSchemaCreator

