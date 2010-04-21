
include $(top_srcdir)/adm_local/make_common_starter.am

BUILT_SOURCES = DATASSIMSK.cc 
IDL_FILES=DATASSIM.idl

lib_LTLIBRARIES = libDATASSIM.la
salomeidl_DATA = $(IDL_FILES) 
salomepython_DATA = DATASSIM_idl.py 
libDATASSIM_la_SOURCES      =
nodist_libDATASSIM_la_SOURCES = DATASSIMSK.cc
nodist_salomeinclude_HEADERS= DATASSIM.hh 
libDATASSIM_la_CXXFLAGS     = -I.  $(KERNEL_INCLUDES)
libDATASSIM_la_LIBADD     = $(KERNEL_LIBS)
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
	rm -rf DATASSIM DATASSIM__POA

install-data-local:
	${mkinstalldirs} $(DESTDIR)$(salomepythondir)
	cp -R DATASSIM DATASSIM__POA $(DESTDIR)$(salomepythondir)

uninstall-local:
	rm -rf $(DESTDIR)$(salomepythondir)/DATASSIM
	rm -rf $(DESTDIR)$(salomepythondir)/DATASSIM__POA
