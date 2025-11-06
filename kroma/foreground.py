from .colors.ansi import AnsiCodes_Foreground, LightAnsiCodes_Foreground, ANSI
from .colors.html import HTMLColorName, RGB
from .utils import _get_color_if_supported


# Colors #

def red(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Foreground.RED) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)


def yellow(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Foreground.YELLOW) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)


def green(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Foreground.GREEN) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)


def cyan(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Foreground.CYAN) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)


def blue(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Foreground.BLUE) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)


def purple(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Foreground.PURPLE) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)


def white(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Foreground.WHITE) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)

# End Colors #


# Light Colors #

def light_cyan(text: str) -> str:
    return _get_color_if_supported(LightAnsiCodes_Foreground.LIGHT_CYAN) + text + _get_color_if_supported(LightAnsiCodes_Foreground.RESET)

# End Light Colors #


# HTML Colors #

def html_color(text: str, color_name: str) -> str | None:
    color = HTMLColorName[color_name.upper()].value
    color_chars = [char for char in color]

    rgb = RGB(
        int(color_chars[0] + color_chars[1], 16),
        int(color_chars[2] + color_chars[3], 16),
        int(color_chars[4] + color_chars[5], 16)
    )

    ansi_color = (
        (ANSI + "38;2;[r];[g];[b]m")
        .replace("[r]", str(rgb.r))
        .replace("[g]", str(rgb.g))
        .replace("[b]", str(rgb.b))
    )

    return _get_color_if_supported(ansi_color) + text + _get_color_if_supported(AnsiCodes_Foreground.RESET)

# End HTML Colors #
