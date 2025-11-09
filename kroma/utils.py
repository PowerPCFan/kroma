from typing import Callable, Any
from .ansi_tools import ansi_supported as _ansi_supported
from .enums import HTMLColors, ANSIColors, StyleType, RGB, TextFormat
from .gv import RESET, ANSI


ansi_supported = _ansi_supported()


def _get_color_if_supported(color: str) -> str:
    if ansi_supported:
        return color
    return ''


def _fix_text(text: str) -> str:
    # i forget what i was gonna do here lol
    return text


def _convert_hex_code_to_rgb(hex_code: str) -> RGB:
    hex_code = hex_code.lstrip("#").lower().strip()
    color_chars = [char for char in hex_code]
    return RGB(
        int(color_chars[0] + color_chars[1], 16),
        int(color_chars[2] + color_chars[3], 16),
        int(color_chars[4] + color_chars[5], 16)
    )


def _convert_rgb_to_hex_code(rgb: RGB) -> str:
    return f"#{rgb.r:02X}{rgb.g:02X}{rgb.b:02X}"


def _clamp(value: float) -> int:
    new_value = round(value)

    if new_value < 0:
        return 0
    elif new_value > 255:
        return 255
    else:
        return new_value


def _convert_rgb_to_ansi_sequence(rgb: RGB, type: StyleType) -> str:
    r = str(rgb.r)
    g = str(rgb.g)
    b = str(rgb.b)
    rgb_sequence = f";2;{r};{g};{b}m"
    color_type = ("38" if type == StyleType.FOREGROUND else "48")

    return ANSI + color_type + rgb_sequence


def _convert_html_hex_to_ansi(text: str, color: HTMLColors | str, type: StyleType) -> str:
    color = (color.replace("#", "") if isinstance(color, str) else color.value).lower().strip()

    rgb = _convert_hex_code_to_rgb(color)
    ansi_color = _convert_rgb_to_ansi_sequence(rgb, type)

    return _get_color_if_supported(ansi_color) + _fix_text(text) + _get_color_if_supported(RESET)


def _get_ansi_color_code(text: str, color: ANSIColors, type: StyleType) -> str:
    color_code = _get_color_if_supported(color.value)
    if type == StyleType.BACKGROUND:
        color_code = color_code.replace("3", "4").replace("9", "10")
    return color_code + _fix_text(text) + _get_color_if_supported(RESET)


def _get_ansi_color_code_with_formatting(text: str, color: ANSIColors, type: StyleType, formats: list[TextFormat] | None = None) -> str:
    color_code = _get_color_if_supported(color.value)
    if type == StyleType.BACKGROUND:
        color_code = color_code.replace("3", "4").replace("9", "10")
    format_codes = "".join([_get_color_if_supported(fmt.value) for fmt in formats]) if formats else ""
    reset_code = _get_color_if_supported(RESET)
    return color_code + format_codes + _fix_text(text) + reset_code


def _convert_html_hex_to_ansi_with_formatting(text: str, color: HTMLColors | str, type: StyleType, formats: list[TextFormat] | None = None) -> str:
    if not formats:
        return _convert_html_hex_to_ansi(text, color, type)

    colored_text = _convert_html_hex_to_ansi("", color, type)
    reset_code = _get_color_if_supported(RESET)

    if reset_code and colored_text.endswith(reset_code):
        color_code = colored_text[:-len(reset_code)]
    else:
        color_code = colored_text

    format_codes = "".join([_get_color_if_supported(fmt.value) for fmt in formats])
    return color_code + format_codes + _fix_text(text) + reset_code


def _apply_text_formatting(text: str, formats: list[TextFormat] | None = None) -> str:
    if not formats:
        return text

    format_codes = "".join([_get_color_if_supported(fmt.value) for fmt in formats])
    return format_codes + _fix_text(text) + _get_color_if_supported(RESET)


def _style_base(
    text: str,
    *,  # Enforce keyword arguments from here on
    foreground: HTMLColors | ANSIColors | str | None,
    background: HTMLColors | ANSIColors | str | None,
    bold: bool,
    italic: bool,
    underline: bool,
    strikethrough: bool,
    swap_foreground_background: bool,
    color_func: Callable[[str, Any, StyleType], str],
    color_func_with_formatting: Callable[[str, Any, StyleType, list[TextFormat] | None], str]
) -> str:
    formats = []
    if bold:
        formats.append(TextFormat.BOLD)
    if italic:
        formats.append(TextFormat.ITALIC)
    if underline:
        formats.append(TextFormat.UNDERLINE)
    if strikethrough:
        formats.append(TextFormat.STRIKETHROUGH)
    if swap_foreground_background:
        formats.append(TextFormat.SWAP_FOREGROUND_BACKGROUND)

    if foreground is None and background is None:
        if formats:
            return _apply_text_formatting(text, formats)
        else:
            return text
    elif foreground is not None and background is None:
        if formats:
            return color_func_with_formatting(text, foreground, StyleType.FOREGROUND, formats)
        else:
            return color_func(text, foreground, StyleType.FOREGROUND)
    elif foreground is None and background is not None:
        if formats:
            return color_func_with_formatting(text, background, StyleType.BACKGROUND, formats)
        else:
            return color_func(text, background, StyleType.BACKGROUND)
    else:
        assert foreground is not None and background is not None
        if formats:
            fg_formatted = color_func_with_formatting(text, foreground, StyleType.FOREGROUND, formats)
            return color_func_with_formatting(fg_formatted, background, StyleType.BACKGROUND, None)
        else:
            return color_func(color_func(text, foreground, StyleType.FOREGROUND), background, StyleType.BACKGROUND)
