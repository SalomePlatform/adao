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

AC_DEFUN([CHECK_EFICAS],[

AC_CHECKING(for Eficas)

eficas_ok=no

AC_ARG_WITH(eficas,
            [  --with-eficas=DIR               root directory path of Eficas installation],
               EFICAS_DIR=$withval,EFICAS_DIR="")

if test "x$EFICAS_DIR" = "x" ; then

  # no --with-eficas option used

  if test "x$EFICAS_ROOT" != "x" ; then

  #EFICAS_ROOT environment variable defined
  EFICAS_DIR=$EFICAS_ROOT

  else
    AC_MSG_WARN("EFICAS_ROOT is not defined")
  fi
fi

if test "x$EFICAS_DIR" != "x" ; then
  eficas_ok=yes
  AC_SUBST(EFICAS_DIR)
fi

AC_MSG_RESULT(for Eficas: $eficas_ok)

])dnl

