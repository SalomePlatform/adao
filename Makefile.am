include $(top_srcdir)/adm_local/make_common_starter.am

SUBDIRS = src

if SALOME_MODULE
SUBDIRS += idl resources bin
endif

if SPHINX_IS_OK
SUBDIRS += doc
endif

ACLOCAL_AMFLAGS = -I adm_local
