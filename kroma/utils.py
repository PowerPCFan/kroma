from .ansi_tools import ansi_supported as _ansi_supported
from .enums import HTMLColors, ANSIColors, StyleType, RGB
from .gv import RESET, ANSI


ansi_supported = _ansi_supported()


def _get_color_if_supported(color: str) -> str:
    if ansi_supported:
        return color
    return ''


def _convert_html_hex_to_ansi(text: str, color: HTMLColors | str, type: StyleType) -> str:
    if isinstance(color, str):
        # color is a HEX code
        if "#" in color:
            color = color.replace("#", "")
        color = color.lower().strip()
    else:
        # color is a HTMLColor enum, get the corresponding hex code
        color = color.value.lower().strip()

    color_chars = [char for char in color]

    rgb = RGB(
        int(color_chars[0] + color_chars[1], 16),
        int(color_chars[2] + color_chars[3], 16),
        int(color_chars[4] + color_chars[5], 16)
    )

    ansi_color = (
        (ANSI + ("38" if type == StyleType.FOREGROUND else "48") + ";2;[r];[g];[b]m")
        .replace("[r]", str(rgb.r))
        .replace("[g]", str(rgb.g))
        .replace("[b]", str(rgb.b))
    )

    return _get_color_if_supported(ansi_color) + text + _get_color_if_supported(RESET)


def _get_ansi_color_code(text: str, color: ANSIColors, type: StyleType) -> str:
    return _get_color_if_supported(color.value) + text + _get_color_if_supported(RESET)
