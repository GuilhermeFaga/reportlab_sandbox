from enum import Enum
from typing import Final


icons_path: Final[str] = "./assets/icons"


class SvgPath(Enum):
    Check: Final = f"{icons_path}/check.svg"
    Warning: Final = f"{icons_path}/warning.svg"
    Error: Final = f"{icons_path}/error.svg"
