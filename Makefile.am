include $(top_srcdir)/adm_local/make_common_starter.am

SUBDIRS =

if SALOME_MODULE
SUBDIRS += idl
endif

SUBDIRS += src

if SALOME_MODULE
SUBDIRS += resources bin samples
endif

if SPHINX_IS_OK
SUBDIRS += doc
endif

ACLOCAL_AMFLAGS = -I adm_local
