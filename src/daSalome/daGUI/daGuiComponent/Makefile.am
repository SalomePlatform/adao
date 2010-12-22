
include $(top_srcdir)/adm_local/make_common_starter.am

AM_CFLAGS=$(SALOME_INCLUDES) -fexceptions

lib_LTLIBRARIES= libADAOEngine.la
salomeinclude_HEADERS= adaogui_component.hxx

libADAOEngine_la_SOURCES        = adaogui_component.cxx
nodist_libADAOEngine_la_SOURCES =
libADAOEngine_la_CXXFLAGS       = -I$(top_builddir)/idl  $(KERNEL_INCLUDES) -I/usr/include
libADAOEngine_la_LIBADD         = -L$(top_builddir)/idl -lADAO ${KERNEL_LIBS}
libADAOEngine_la_LDFLAGS        =

