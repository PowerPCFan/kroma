from . import html_color
from . import ansi_color
from .utils import ansi_supported
from .enums import ANSIColors, HTMLColors
from . import palettes

__name__ = "kroma"
__all__ = [
    "html_color",
    "ansi_color",
    "ansi_supported",
    "ANSIColors",
    "HTMLColors",
    "palettes"
]
