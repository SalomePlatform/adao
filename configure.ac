dnl  Copyright (C) 2010-2011  EDF R&D
dnl
dnl  This library is free software; you can redistribute it and/or
dnl  modify it under the terms of the GNU Lesser General Public
dnl  License as published by the Free Software Foundation; either
dnl  version 2.1 of the License.
dnl
dnl  This library is distributed in the hope that it will be useful,
dnl  but WITHOUT ANY WARRANTY; without even the implied warranty of
dnl  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
dnl  Lesser General Public License for more details.
dnl
dnl  You should have received a copy of the GNU Lesser General Public
dnl  License along with this library; if not, write to the Free Software
dnl  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
dnl
dnl  See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
dnl
dnl  Author: André Ribes, andre.ribes@edf.fr, EDF R&D

AC_INIT(ADAO_SRC, [6.4.0])
AC_CONFIG_AUX_DIR(adm_local)
AM_INIT_AUTOMAKE
AM_CONFIG_HEADER(adao_config.h)
MODULE_NAME=adao
AC_SUBST(MODULE_NAME)

AC_ENABLE_DEBUG(yes)
AC_DISABLE_PRODUCTION

AC_PROG_LIBTOOL
AC_PROG_CC
AC_PROG_CXX

CHECK_KERNEL
CHECK_OMNIORB
CHECK_EFICAS
CHECK_MODULE_EFICAS
CHECK_SCIPY
CHECK_SPHINX

echo
echo
echo
echo "------------------------------------------------------------------------"
echo "$PACKAGE $VERSION"
echo "------------------------------------------------------------------------"
echo
echo "Configuration Options Summary:"
echo
echo "Mandatory products:"
echo "  Threads ................ : $threads_ok"
echo "  Python ................. : $python_ok"
echo "  Scipy .................. : $scipy_ok"
echo
echo "SALOME Integration mandatory products:"
echo "  OmniOrb (CORBA) ........ : $omniORB_ok"
echo "  OmniOrbpy (CORBA) ...... : $omniORBpy_ok"
echo "  SALOME KERNEL .......... : $Kernel_ok"
echo "  Eficas ................. : $eficas_ok"
echo "  Module Eficas .......... : $module_eficas_ok"
echo
echo "Optional products:"
echo "  Sphinx (for doc)........ : $threads_ok"
echo "------------------------------------------------------------------------"
echo

if test "x$threads_ok" = "xno"; then
  AC_MSG_ERROR([Thread is required],1)
fi
if test "x$python_ok" = "xno"; then
  AC_MSG_ERROR([Python is required],1)
fi
if test "x$scipy_ok" = "xno"; then
  AC_MSG_ERROR([Scipy is required],1)
fi

salome_module_ok=yes

if test "x$omniORB_ok" = "xno"; then
  AC_MSG_WARN([OmniOrb is required for SALOME Module part])
  salome_module_ok=no
fi
if test "x$omniORBpy_ok" = "xno"; then
  AC_MSG_WARN([OmniOrbpy is required for SALOME Module part])
  salome_module_ok=no
fi
if test "x$Kernel_ok" = "xno"; then
  AC_MSG_WARN([SALOME KERNEL is required for SALOME Module part - 
               You could define a correct KERNEL_ROOT_DIR or use the --with-kernel= configure option])
  salome_module_ok=no
fi
if test "x$eficas_ok" = "xno"; then
  AC_MSG_WARN([Eficas is required for SALOME Module part])
  salome_module_ok=no
fi
if test "x$module_eficas_ok" = "xno"; then
  AC_MSG_WARN([Module Eficas is required for SALOME Module part])
  salome_module_ok=no
fi

AM_CONDITIONAL(SALOME_MODULE, test x$salome_module_ok = xyes)

if test "x$sphinx_ok" = "xno"; then
  AC_MSG_WARN([Sphinx is required for ADAO documentation])
fi

if test -f a.out; then
  rm a.out
fi

AC_CONFIG_FILES([
        Makefile
        idl/Makefile
        resources/Makefile
        src/Makefile
        src/daComposant/Makefile
        src/daEficas/Makefile
        src/daEficas/prefs_ADAO.py
        src/daSalome/Makefile
        src/daSalome/daGUI/Makefile
        src/daSalome/daGUI/daUtils/Makefile
        src/daSalome/daGUI/daGuiImpl/Makefile
        src/daSalome/daGUI/daEficasWrapper/Makefile
        examples/Makefile
        examples/daSalome/Makefile
        examples/daSalome/test003_ADAO_JDC_using_scripts.comm
        examples/daSalome/test004_ADAO_JDC_using_scripts.comm
        examples/daSalome/test005_ADAO_Operators.comm
        examples/daSkeletons/Makefile
        examples/daSkeletons/External_data_definition_by_scripts/Makefile
        examples/daSkeletons/External_data_definition_by_scripts/ADAO_Case.comm
        bin/Makefile
        bin/qtEficas_adao_study.py
        doc/Makefile
        ])
AC_OUTPUT
