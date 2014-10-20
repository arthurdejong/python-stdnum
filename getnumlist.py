#!/usr/bin/env python

# getnumlist.py - script to get a list of number formats in stdnum
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

"""This script uses introspection to present a list of number formats
suitable to be included in the README and stdnum package description."""

import pydoc

from stdnum import util


# these are excluded
algortihms = ('stdnum.verhoeff', 'stdnum.luhn', 'stdnum.iso7064')


def get_number_modules():
    """Provides the number modules that are not algorithms."""
    for module in util.get_number_modules():
        if module.__name__ not in algortihms and \
           not module.__name__.startswith('stdnum.iso7064'):
             yield module

if __name__ == '__main__':
    print 'For README:'
    print ''
    for module in get_number_modules():
        print ' * %s' % util.get_module_name(module)
    print ''
    print 'For stdnum/__init__.py:'
    print ''
    for module in get_number_modules():
        print '* %s: %s' % (
            module.__name__.replace('stdnum.', ''),
            util.get_module_name(module),
        )
    print ''
    print 'For docs/index.rst:'
    print ''
    for module in get_number_modules():
        print '   %s' % module.__name__.replace('stdnum.', '')
    print ''
    print 'For index.xml:'
    print ''
    for module in get_number_modules():
        print '  <li>%s</li>' % util.get_module_name(module)
