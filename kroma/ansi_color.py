from .enums import ANSIColors
from .utils import _get_ansi_color_code, _get_ansi_color_code_with_formatting, _style_base


class CustomStyle:
    def __init__(
        self,
        *,  # Enforce keyword arguments from here on
        foreground: ANSIColors | None = None,
        background: ANSIColors | None = None,
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
    foreground: ANSIColors | None = None,
    background: ANSIColors | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    strikethrough: bool = False,
    swap_foreground_background: bool = False
) -> str:
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
