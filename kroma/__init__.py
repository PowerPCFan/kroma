from .styles import style, lighten, darken, CustomStyle
from .exceptions import MixedColorTypesError
from .utils import ansi_supported
from .enums import ANSIColors, HTMLColors, StyleType
from .gradients import gradient, CustomGradient
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
    "palettes",
    "gradient",
    "CustomGradient",
    "StyleType"
]
