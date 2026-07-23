# ico.py - functions for handling Slovak organisation identifiers
# coding: utf-8
#
# Copyright (C) 2026 Devashish Moghe
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
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

"""IČO (Identifikačné číslo organizácie, Slovak organisation identifier).

The IČO (Identifikačné číslo organizácie) is an 8-digit number (including a
trailing check digit) that identifies an organisation or sole trader
registered in Slovakia. It is listed in the Slovak business register (ORSR)
and the Register of Legal Entities (RPO).

This number is identical to the Czech counterpart (until 1993 the Czech
Republic and Slovakia were one country) and uses the same format and check
digit.

>>> validate('31322832')
'31322832'
>>> validate('31 322 832')
'31322832'
>>> validate('31322833')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('313228')  # too short
Traceback (most recent call last):
    ...
InvalidLength: ...
"""

# since this number is essentially the same as the Czech counterpart
# (until 1993 the Czech Republic and Slovakia were one country)

from __future__ import annotations

from stdnum.cz.ico import calc_check_digit, compact, is_valid, validate


__all__ = ['compact', 'calc_check_digit', 'validate', 'is_valid']
