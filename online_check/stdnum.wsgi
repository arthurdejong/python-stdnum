# stdnum.wsgi - simple WSGI application to check numbers
#
# Copyright (C) 2017-2020 Arthur de Jong.
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

"""Simple WSGI application to check numbers."""

import cgi
import inspect
import json
import os
import re
import sys


sys.stdout = sys.stderr
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-stdnum'))

from stdnum.util import (
    get_module_description, get_module_name, get_number_modules, to_unicode)


_template = None


def get_conversions(module, number):
    """Return the possible conversions for the number."""
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if name.startswith('to_'):
            args, varargs, varkw, defaults = inspect.getargspec(func)
            if defaults:
                args = args[:-len(defaults)]
            if args == ['number'] and not name.endswith('binary'):
                try:
                    conversion = func(number)
                    if conversion != number:
                        yield (name[3:], to_unicode(conversion))
                except Exception:
                    pass


def info(module, number):
    """Return information about the number."""
    compactfn = getattr(module, 'compact', lambda x: x)
    formatfn = getattr(module, 'format', compactfn)
    return dict(
        number=formatfn(number),
        compact=compactfn(number),
        valid=module.is_valid(number),
        module=module.__name__.split('.', 1)[1],
        name=to_unicode(get_module_name(module)),
        description=to_unicode(get_module_description(module)),
        conversions=dict(get_conversions(module, number)))


def format(data):
    """Return an HTML snippet describing the number."""
    description = cgi.escape(data['description']).replace('\n\n', '<br/>\n')
    description = re.sub(
        r'^[*] (.*)$', r'<ul><li>\1</li></ul>',
        description, flags=re.MULTILINE)
    description = re.sub(
        r'\b((https?|ftp)://[^\s<]*[-\w+&@#/%=~_|])',
        r'<a href="\1">\1</a>',
        description, flags=re.IGNORECASE + re.UNICODE)
    for name, conversion in data.get('conversions', {}).items():
        description += '\n<br/><b><i>%s</i></b>: %s' % (
            cgi.escape(name), cgi.escape(conversion))
    return '<li>%s: <b>%s</b><p>%s</p></li>' % (
        cgi.escape(data['number']),
        cgi.escape(data['name']),
        description)


def application(environ, start_response):
    """WSGI application."""
    # read template if needed
    global _template
    if not _template:
        basedir = os.path.join(
            environ['DOCUMENT_ROOT'],
            os.path.dirname(environ['SCRIPT_NAME']).strip('/'))
        _template = to_unicode(open(os.path.join(basedir, 'template.html'), 'rt').read())
    is_ajax = environ.get(
        'HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest'
    parameters = cgi.parse_qs(environ.get('QUERY_STRING', ''))
    results = []
    number = ''
    if 'number' in parameters:
        number = to_unicode(parameters['number'][0])
        results = [
            info(module, number)
            for module in get_number_modules()
            if module.is_valid(number)]
    if is_ajax:
        start_response('200 OK', [
            ('Content-Type', 'application/json'),
            ('Vary', 'X-Requested-With')])
        return [json.dumps(results, indent=2, sort_keys=True).encode('utf-8')]
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Vary', 'X-Requested-With')])
    return [(_template % dict(
        value=cgi.escape(number, True),
        results=u'\n'.join(format(data) for data in results))).encode('utf-8')]
