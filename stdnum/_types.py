# _types.py - module for defining custom types
#
# Copyright (C) 2025 David Salvisberg
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

"""Module containing custom types.

This module is designed to be accessed through `stdnum._typing` so
you only have the overhead and runtime requirement of Python 3.9
and `typing_extensions`, when that type is introspected at runtime.

As such this module should never be accessed directly.
"""

from __future__ import annotations

from typing import Protocol
from typing_extensions import Required, TypedDict


class NumberValidationModule(Protocol):
    """Minimal interface for a number validation module."""

    def compact(self, number: str) -> str:
        """Convert the number to the minimal representation."""

    def validate(self, number: str) -> str:
        """Check if the number provided is a valid number of its type."""

    def is_valid(self, number: str) -> bool:
        """Check if the number provided is a valid number of its type."""


class IMSIInfo(TypedDict, total=False):
    """Info `dict` returned by `stdnum.imsi.info`."""

    number: Required[str]
    mcc: Required[str]
    mnc: Required[str]
    msin: Required[str]
    country: str
    cc: str
    brand: str
    operator: str
    status: str
    bands: str


class GSTINInfo(TypedDict):
    """Info `dict` returned by `stdnum.in_.gstin.info`."""

    state: str | None
    pan: str
    holder_type: str
    initial: str
    registration_count: int


class PANInfo(TypedDict):
    """Info `dict` returned by `stdnum.in_.pan.info`."""

    holder_type: str
    initial: str
