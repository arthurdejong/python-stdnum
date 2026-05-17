"""СНИЛС (Страховой номер индивидуального лицевого счёта, Russian Individual insurance account number)

More information:

* https://en.wikipedia.org/wiki/SNILS_(Russia)
* https://ru.wikipedia.org/wiki/Страховой_номер_индивидуального_лицевого_счёта

>>> validate('11223344595')
'112-233-445 95'
>>> validate('010-242-368 77')
'010-242-368 77'
>>> validate('010-242-368 00')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from __future__ import annotations

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, " -").strip()


def calc_check_digit(number: str) -> str:
    """Calculate the expected SNILS checksum digits"""
    calculated_checksum: int = sum([int(c) * (9 - i) for i, c in enumerate(number[:9])])
    if calculated_checksum > 101:
        calculated_checksum %= 101
    if calculated_checksum in [100, 101]:
        calculated_checksum = 0
    return f"{calculated_checksum:02d}"


def _is_valid_checksum(number: str) -> bool:
    """Determine if checksum is correct"""
    checksum_digits: str = number[9:11]
    if calc_check_digit(number) != checksum_digits:
        return False
    return True


def validate(number: str) -> str:
    """Determine if the given number is a valid SNILS."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if not len(number) == 11:
        raise InvalidLength()
    if not _is_valid_checksum(number):
        raise InvalidChecksum()
    return number


def is_valid(number: str) -> bool:
    """Check if the number is a valid SNILS."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number: str) -> str:
    """Format the number provided for output."""
    number = validate(number)
    return f"{number[0:3]}-{number[3:6]}-{number[6:9]} {number[9:11]}"


if __name__ == "__main__":
    print(format("148-481-255 85"))
