from .colors.ansi import AnsiCodes_Background, LightAnsiCodes_Background, ANSI
from .colors.html import HTMLColorName, RGB
from .utils import _get_color_if_supported


# Colors #

def red(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Background.RED) + text + _get_color_if_supported(AnsiCodes_Background.RESET)


def yellow(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Background.YELLOW) + text + _get_color_if_supported(AnsiCodes_Background.RESET)


def green(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Background.GREEN) + text + _get_color_if_supported(AnsiCodes_Background.RESET)


def cyan(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Background.CYAN) + text + _get_color_if_supported(AnsiCodes_Background.RESET)


def blue(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Background.BLUE) + text + _get_color_if_supported(AnsiCodes_Background.RESET)


def purple(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Background.PURPLE) + text + _get_color_if_supported(AnsiCodes_Background.RESET)


def white(text: str) -> str:
    return _get_color_if_supported(AnsiCodes_Background.WHITE) + text + _get_color_if_supported(AnsiCodes_Background.RESET)

# End Colors #


# Light Colors #

def light_cyan(text: str) -> str:
    return _get_color_if_supported(LightAnsiCodes_Background.LIGHT_CYAN) + text + _get_color_if_supported(LightAnsiCodes_Background.RESET)

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
        (ANSI + "48;2;[r];[g];[b]m")
        .replace("[r]", str(rgb.r))
        .replace("[g]", str(rgb.g))
        .replace("[b]", str(rgb.b))
    )

    return _get_color_if_supported(ansi_color) + text + _get_color_if_supported(AnsiCodes_Background.RESET)

# End HTML Colors #
