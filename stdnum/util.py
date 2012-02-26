# util.py - common utility functions
#
# Copyright (C) 2012 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""Common utility functions for other stdnum modules.

This module is meant for internal use by stdnum modules and is not
guaranteed to remain stable and as such not part of the public API of
stdnum.
"""

import pkgutil


def clean(number, deletechars):
    """Remove the specified characters from the supplied number.

    >>> clean('123-456:78 9', ' -:')
    '123456789'
    """
    return ''.join(x for x in number if x not in deletechars)


def get_number_modules(base='stdnum'):
    """Yield all the module and package names under the specified module."""
    module = __import__(base, globals(), locals(), [base])
    for loader, name, is_pkg in pkgutil.walk_packages(
                    module.__path__, module.__name__ + '.',
                    onerror=lambda x: None
                ):
        module = __import__(name, globals(), locals(), [name])
        if hasattr(module, 'is_valid'):
            yield module
