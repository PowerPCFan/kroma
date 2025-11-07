from .enums import ANSIColors
from .utils import _get_ansi_color_code, _get_ansi_color_code_with_formatting, _style_base


def style(
    text: str,
    foreground: ANSIColors | None = None,
    background: ANSIColors | None = None,
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
        color_func=_get_ansi_color_code,
        color_func_with_formatting=_get_ansi_color_code_with_formatting
    )
