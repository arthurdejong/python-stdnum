# __init__.py - collection of Austrian numbers
# coding: utf-8
#
# Copyright (C) 2012-2018 Arthur de Jong
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

"""Collection of Austrian numbers."""
from __future__ import annotations

# provide aliases
from stdnum.at import postleitzahl as postal_code  # noqa: F401
from stdnum.at import uid as vat  # noqa: F401
from stdnum.at import vnr as personalid  # noqa: F401
