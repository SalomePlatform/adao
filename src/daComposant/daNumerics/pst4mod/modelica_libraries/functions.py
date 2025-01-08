# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2025 EDF R&D
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

###############################################################################
#                            LIBRARIES IMPORT                                 #
###############################################################################
from time import localtime
import os
from subprocess import Popen

###############################################################################
#                            USEFUL FUNCTIONS                                 #
###############################################################################

def get_cur_time():
    """
    Return a string in the format : year/month/day hour:min:sec
    """
    real_time = localtime()
    str_real_time = \
        '{0:04d}'.format(real_time.tm_year) + '/' + \
        '{0:02d}'.format(real_time.tm_mon) + '/' + \
        '{0:02d}'.format(real_time.tm_mday) + ' ' + \
        '{0:02d}'.format(real_time.tm_hour) + ':' + \
        '{0:02d}'.format(real_time.tm_min) + ':' + \
        '{0:02d}'.format(real_time.tm_sec)

    return str_real_time


def tol_equality(vars, tol=1.e-4):
    """
    Check whether two numbers (vars[0] and vars[1]) are approximately equal (with 'tol' tollerance)
    """
    try:
        return abs(float(vars[1]) / float(vars[0]) - 1.) < tol
    except ZeroDivisionError:
        return abs(vars[1] - vars[0]) < tol


def Edit_File(filename):
    if os.name == 'nt':  # Windows
        editor = ['Notepad']
    else:
        editor = ['gedit', '-s']
    file_display = Popen(editor + [f'{filename}'])
    file_display.wait()


if __name__ == '__main__':
    print('\n  AUTODIAGNOSTIC\n  ==============\n')
