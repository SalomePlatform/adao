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

#
# Check availability of Aster binary distribution
#

AC_DEFUN([AC_CHECK_ASTER],[

AC_CHECKING(for Aster)

Aster_ok=no

AC_ARG_WITH(aster,
      [AC_HELP_STRING([--with-aster=DIR],[root directory path of Aster installation])],
      [ASTER_DIR="$withval"],[ASTER_DIR=""])

if test -f ${ASTER_DIR}/asteru ; then
   Aster_ok=yes
   AC_MSG_RESULT(Using Aster distribution in ${ASTER_DIR})

   ASTER_INCLUDES=-I$ASTER_DIR/bibc/include

   AC_SUBST(ASTER_DIR)
   AC_SUBST(ASTER_INCLUDES)

else
   AC_MSG_WARN("Cannot find Aster distribution")
fi

AC_MSG_RESULT(for Aster: $Aster_ok)

])dnl
