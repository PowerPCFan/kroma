from .styles import style, lighten, darken, CustomStyle
from .exceptions import MixedColorTypesError
from .utils import ansi_supported
from .enums import ANSIColors, HTMLColors
from . import palettes

__name__ = "kroma"
__all__ = [
    "style",
    "lighten",
    "darken",
    "CustomStyle",
    "MixedColorTypesError",
    "ansi_supported",
    "ANSIColors",
    "HTMLColors",
    "palettes"
]
