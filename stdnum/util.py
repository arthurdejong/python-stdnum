# util.py - common utility functions
#
# Copyright (C) 2012, 2013 Arthur de Jong
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
import pydoc
import re
import sys

from stdnum.exceptions import *


_strip_doctest_re = re.compile('^>>> .*\Z', re.DOTALL | re.MULTILINE)


def clean(number, deletechars):
    """Remove the specified characters from the supplied number.

    >>> clean('123-456:78 9', ' -:')
    '123456789'
    """
    try:
        return ''.join(x for x in number if x not in deletechars)
    except:
        raise InvalidFormat()


def get_number_modules(base='stdnum'):
    """Yield all the module and package names under the specified module."""
    __import__(base)
    module = sys.modules[base]
    for loader, name, is_pkg in pkgutil.walk_packages(
                    module.__path__, module.__name__ + '.',
                    onerror=lambda x: None
                ):
        __import__(name)
        module = sys.modules[name]
        if hasattr(module, 'validate'):
            yield module


def get_module_name(module):
    """Return the short description of the number."""
    return pydoc.splitdoc(pydoc.getdoc(module))[0].strip('.')


def get_module_description(module):
    """Return a description of the number."""
    doc = pydoc.splitdoc(pydoc.getdoc(module))[1]
    # remove the doctests
    return _strip_doctest_re.sub('', doc[1]).strip(),


def get_module_list():
    for module in get_number_modules():
        yield ' * %s: %s' % (
            module.__name__.replace('stdnum.', ''),
            get_module_name(module),
        )
