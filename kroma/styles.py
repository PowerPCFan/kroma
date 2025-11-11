from enum import Enum
from .enums import ANSIColors, HTMLColors, RGB
from .utils import (
    _get_ansi_color_code,
    _get_ansi_color_code_with_formatting,
    _convert_html_hex_to_ansi,
    _convert_html_hex_to_ansi_with_formatting,
    _style_base,
    _convert_hex_code_to_rgb,
    _convert_rgb_to_hex_code,
    _clamp
)
from .exceptions import MixedColorTypesError


class ColorMode(Enum):
    ANSI = "ansi"
    HTML = "html"


def _get_color_type(color) -> str:
    """Get the string representation of a color's type."""
    if isinstance(color, ANSIColors):
        return "ANSIColors"
    elif isinstance(color, HTMLColors):
        return "HTMLColors"
    elif isinstance(color, str):
        return "hex string"
    return "None"


def _determine_color_mode(foreground, background) -> ColorMode:
    fg_is_ansi = isinstance(foreground, ANSIColors)
    bg_is_ansi = isinstance(background, ANSIColors)

    fg_is_html = isinstance(foreground, (str, HTMLColors))
    bg_is_html = isinstance(background, (str, HTMLColors))

    if (fg_is_ansi and bg_is_html) or (fg_is_html and bg_is_ansi):
        fg_type = _get_color_type(foreground)
        bg_type = _get_color_type(background)
        raise MixedColorTypesError(fg_type, bg_type)

    if fg_is_html or bg_is_html:
        return ColorMode.HTML

    return ColorMode.ANSI


class CustomStyle:
    def __init__(
        self,
        *,  # Enforce keyword arguments from here on
        foreground: str | ANSIColors | HTMLColors | None = None,
        background: str | ANSIColors | HTMLColors | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
        swap_foreground_background: bool = False
    ):

        self.kwargs = {
            "foreground": foreground,
            "background": background,
            "bold": bold,
            "italic": italic,
            "underline": underline,
            "strikethrough": strikethrough,
            "swap_foreground_background": swap_foreground_background
        }

    def __call__(self, text: str) -> str:
        return style(text, **self.kwargs)


def style(
    text: str,
    *,  # Enforce keyword arguments from here on
    foreground: str | ANSIColors | HTMLColors | None = None,
    background: str | ANSIColors | HTMLColors | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    strikethrough: bool = False,
    swap_foreground_background: bool = False
) -> str:
    color_mode = _determine_color_mode(foreground, background)

    if color_mode == ColorMode.HTML:
        return _style_base(
            text,
            foreground=foreground,
            background=background,
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            swap_foreground_background=swap_foreground_background,
            color_func=_convert_html_hex_to_ansi,
            color_func_with_formatting=_convert_html_hex_to_ansi_with_formatting
        )
    elif color_mode == ColorMode.ANSI:
        return _style_base(
            text,
            foreground=foreground,
            background=background,
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            swap_foreground_background=swap_foreground_background,
            color_func=_get_ansi_color_code,
            color_func_with_formatting=_get_ansi_color_code_with_formatting
        )
    else:
        raise Exception("An unknown error has occurred.")


def lighten(color: str | HTMLColors, percentage: float) -> str:
    p = percentage / 100.0
    hex_color = (color.value if isinstance(color, HTMLColors) else color)

    rgb = _convert_hex_code_to_rgb(hex_color)

    new_r = _clamp(rgb.r + (255 - rgb.r) * p)
    new_g = _clamp(rgb.g + (255 - rgb.g) * p)
    new_b = _clamp(rgb.b + (255 - rgb.b) * p)

    return _convert_rgb_to_hex_code(RGB(r=new_r, g=new_g, b=new_b))


def darken(color: str | HTMLColors, percentage: float) -> str:
    p = percentage / 100.0
    hex_color = (color.value if isinstance(color, HTMLColors) else color)

    rgb = _convert_hex_code_to_rgb(hex_color)

    new_r = _clamp(rgb.r * (1 - p))
    new_g = _clamp(rgb.g * (1 - p))
    new_b = _clamp(rgb.b * (1 - p))

    return _convert_rgb_to_hex_code(RGB(r=new_r, g=new_g, b=new_b))
