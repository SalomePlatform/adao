#!/bin/sh
# Copyright (C) 2008-2019 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
# Author: André Ribes, andre.ribes@edf.fr, EDF R&D

rm -rf autom4te.cache
rm -f aclocal.m4 adm_local/ltmain.sh

########################################################################
# Test if the KERNEL_ROOT_DIR is set correctly

if test ! -d "${KERNEL_ROOT_DIR}"; then
    echo "failed : KERNEL_ROOT_DIR variable is not correct !"
    exit 1
fi

echo "Running aclocal..."    ;
aclocal --force -I adm_local \
                -I ${KERNEL_ROOT_DIR}/salome_adm/unix/config_files || exit 1
echo "Running autoheader..." ; autoheader --force                  || exit 1
echo "Running autoconf..."   ; autoconf --force                    || exit 1
echo "Running libtoolize..." ; libtoolize --copy --force           || exit 1
echo "Running automake..."   ; automake --add-missing --copy       || exit 1
