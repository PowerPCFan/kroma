from .enums import HTMLColors
from .utils import _convert_html_hex_to_ansi, _convert_html_hex_to_ansi_with_formatting, _style_base


def style(
    text: str,
    foreground: str | HTMLColors | None = None,
    background: str | HTMLColors | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    strikethrough: bool = False
) -> str:
    return _style_base(
        text=text,
        foreground=foreground,
        background=background,
        bold=bold,
        italic=italic,
        underline=underline,
        strikethrough=strikethrough,
        color_func=_convert_html_hex_to_ansi,
        color_func_with_formatting=_convert_html_hex_to_ansi_with_formatting
    )
