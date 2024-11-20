import re
from typing import Optional

from rigour.ids.common import IdentifierFormat

OGRN_RE = re.compile(r"\b(\d{13}|\d{15})\b")
VALID_FEDERAL_SUBJECT_CODES = set(range(1, 80)) | {83, 86, 87, 89, 91, 92, 99}


class OGRN(IdentifierFormat):
    """Primary State Registration Number (Russian company registration)."""

    TITLE: str = "OGRN"

    # cf. https://docs.trellix.com/de-DE/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-945B4343-861E-4A57-8E60-8B6028871BA1.html

    @classmethod
    def is_valid(cls, text: str) -> bool:
        """Determine if the given string is a valid OGRN."""
        if OGRN_RE.match(text) is None:
            return False

        # Validate registration type
        if text[0] == "0":
            return False

        # Validate federal subject code
        federal_subject_code = int(text[3:5])
        if federal_subject_code not in VALID_FEDERAL_SUBJECT_CODES:
            return False

        # Validate control digit logic
        control_digit = int(text[-1])
        return control_digit == cls.calculate_control_digit(text)

    @classmethod
    def normalize(cls, text: str) -> Optional[str]:
        """Normalize the given string to a valid OGRN."""
        match = OGRN_RE.search(text)
        if match is None:
            return None
        return match.group(1)

    @classmethod
    def calculate_control_digit(cls, grn: str) -> Optional[int]:
        if len(grn) == 13:
            number = int(grn[:12])
            mod_result = number % 11
            calculated_digit = mod_result if mod_result != 10 else 0
            return calculated_digit
        elif len(grn) == 15:
            number = int(grn[:14])
            mod_result = number % 13
            calculated_digit = mod_result if mod_result != 10 else 0
            return calculated_digit
        return None