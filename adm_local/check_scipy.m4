dnl  Copyright (C) 2008-2021 EDF R&D
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

AC_DEFUN([CHECK_SCIPY],[
AC_REQUIRE([CHECK_PYTHON])dnl

scipy_ok=no

scipydir=`$PYTHON -c "import scipy;print(scipy.get_include())" 2>/dev/null`

if test -d "$scipydir"; then
   scipy_ok=yes
fi

AC_MSG_RESULT(for scipy: $scipy_ok)

])dnl
dnl
