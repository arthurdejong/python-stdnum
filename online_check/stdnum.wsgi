# stdnum.wsgi - simple WSGI application to check numbers
#
# Copyright (C) 2017 Arthur de Jong.
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

import cgi
import json
import os
import re
import sys

sys.stdout = sys.stderr
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python-stdnum'))

from stdnum.util import (
    get_number_modules, get_module_name, get_module_description)


_template = None


def info(module, number):
    compactfn = getattr(module, 'compact', lambda x: x)
    formatfn = getattr(module, 'format', compactfn)
    return dict(
        number=formatfn(number),
        compact=compactfn(number),
        valid=module.is_valid(number),
        module=module.__name__.split('.', 1)[1],
        name=get_module_name(module),
        description=get_module_description(module))


def format(data):
    description = cgi.escape(data['description']).replace('\n\n', '<br/>\n')
    description = re.sub(
        r'^[*] (.*)$', r'<ul><li>\1</li></ul>',
        description, flags=re.MULTILINE)
    description = re.sub(
        r'\b((https?|ftp)://[^\s<]*[-\w+&@#/%=~_|])',
        r'<a href="\1">\1</a>',
        description, flags=re.IGNORECASE + re.UNICODE)
    return '<li><b>%s</b><br/>%s<p>%s</p></li>' % (
        cgi.escape(data['name']),
        cgi.escape(data['number']),
        description)


def application(environ, start_response):
    # read template if needed
    global _template
    if not _template:
        basedir = os.path.join(
            environ['DOCUMENT_ROOT'],
            os.path.dirname(environ['SCRIPT_NAME']).strip('/'))
        _template = open(os.path.join(basedir, 'template.html'), 'r').read()

    is_ajax = environ.get(
        'HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest'

    parameters = cgi.parse_qs(environ.get('QUERY_STRING', ''))
    results = []
    if 'number' in parameters:
        number = parameters['number'][0]
        results = [
            info(module, number)
            for module in get_number_modules()
            if module.is_valid(number)]
    if 'HTTP_X_REQUESTED_WITH' in environ:
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json.dumps(results, indent=2, sort_keys=True)]
    start_response('200 OK', [('Content-Type', 'text/html')])
    return _template % '\n'.join(format(data) for data in results)
