from .enums import HTMLColors, RGB
from .utils import _convert_html_hex_to_ansi, _convert_html_hex_to_ansi_with_formatting, _style_base, _convert_hex_code_to_rgb, _convert_rgb_to_hex_code, _clamp


class CustomStyle:
    def __init__(self,
            foreground: str | HTMLColors | None = None,
            background: str | HTMLColors | None = None,
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
    foreground: str | HTMLColors | None = None,
    background: str | HTMLColors | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    strikethrough: bool = False,
    swap_foreground_background: bool = False
) -> str:
    return _style_base(
        text=text,
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


def lighten(color: HTMLColors | str, percentage: float) -> str:
    p = percentage / 100.0
    hex_color = (color.value if isinstance(color, HTMLColors) else color)

    rgb = _convert_hex_code_to_rgb(hex_color)

    new_r = _clamp(rgb.r + (255 - rgb.r) * p)
    new_g = _clamp(rgb.g + (255 - rgb.g) * p)
    new_b = _clamp(rgb.b + (255 - rgb.b) * p)

    return _convert_rgb_to_hex_code(RGB(r=new_r, g=new_g, b=new_b))


def darken(color: HTMLColors | str, percentage: float) -> str:
    p = percentage / 100.0
    hex_color = (color.value if isinstance(color, HTMLColors) else color)

    rgb = _convert_hex_code_to_rgb(hex_color)

    new_r = _clamp(rgb.r * (1 - p))
    new_g = _clamp(rgb.g * (1 - p))
    new_b = _clamp(rgb.b * (1 - p))

    return _convert_rgb_to_hex_code(RGB(r=new_r, g=new_g, b=new_b))
