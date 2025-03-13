# _typing.py - module for typing shims with reduced runtime overhead
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

"""Compatibility shims for the Python typing module.

This module is designed in a way, such, that runtime use of
annotations is possible starting with Python 3.9, but it still
supports Python 3.6 - 3.8 if the package is used normally without
introspecting the annotations of the API.

You should never import *from* this module, you should always import
the entire module and then access the members via attribute access.

I.e. use the module like this:
```python
from stdnum import _typing as t

foo: t.Any = ...
```

Instead of like this:
```python
from stdnum._typing import Any

foo: Any = ...
```

The exception to that rule are `TYPE_CHECKING` `cast` and `deprecated`
which can be used at runtime.
"""

from __future__ import annotations


TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Generator as Generator
    from collections.abc import Iterable as Iterable
    from collections.abc import Mapping as Mapping
    from collections.abc import Sequence as Sequence
    from typing import Any as Any
    from typing import IO as IO
    from typing import Literal as Literal
    from typing import cast as cast
    from typing_extensions import TypeAlias as TypeAlias
    from typing_extensions import deprecated as deprecated

    from stdnum._types import GSTINInfo as GSTINInfo
    from stdnum._types import IMSIInfo as IMSIInfo
    from stdnum._types import NumberValidationModule as NumberValidationModule
    from stdnum._types import PANInfo as PANInfo
else:
    def cast(typ, val):
        """Cast a value to a type."""
        return val

    class deprecated:  # noqa: N801
        """Simplified backport of `warnings.deprecated`.

        This backport doesn't handle classes or async functions.
        """

        def __init__(self, message, category=DeprecationWarning, stacklevel=1):  # noqa: D107
            self.message = message
            self.category = category
            self.stacklevel = stacklevel

        def __call__(self, func):  # noqa: D102
            func.__deprecated__ = self.message

            if self.category is None:
                return func

            import functools
            import warnings

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warnings.warn(self.message, category=self.category, stacklevel=self.stacklevel + 1)
                return func(*args, **kwargs)

            wrapper.__deprecated__ = self.message
            return wrapper

    def __getattr__(name):
        if name in {'Generator', 'Iterable', 'Mapping', 'Sequence'}:
            import collections.abc
            return getattr(collections.abc, name)
        elif name in {'Any', 'IO', 'Literal'}:
            import typing
            return getattr(typing, name)
        elif name == 'TypeAlias':
            import sys
            if sys.version_info >= (3, 10):
                import typing
            else:
                import typing_extensions as typing
            return getattr(typing, name)
        elif name in {'GSTINInfo', 'IMSIInfo', 'NumberValidationModule', 'PANInfo'}:
            import stdnum._types
            return getattr(stdnum._types, name)
        else:
            raise AttributeError(name)
