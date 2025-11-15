from typing import Callable, Any
from .enums import HTMLColors, ANSIColors, StyleType, RGB, HSL, TextFormat
from .gv import RESET, ANSI, ansi_supported


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


# def _clamp(value: float) -> int:
#     new_value = round(value)

#     if new_value < 0:
#         return 0
#     elif new_value > 255:
#         return 255
#     else:
#         return new_value


# this new one SHOULD work the same
def _clamp(value: float, min_val: float = 0.0, max_val: float = 255.0) -> int:
    return int(max(min_val, min(max_val, round(value))))


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


# this function is AI-generated since i don't even know where to BEGIN when converting rgb to hsl lmao
def _convert_rgb_to_hsl(rgb: RGB) -> HSL:
    # Normalize R, G, B components to range [0, 1]
    r_norm = rgb.r / 255.0
    g_norm = rgb.g / 255.0
    b_norm = rgb.b / 255.0

    c_max = max(r_norm, g_norm, b_norm)
    c_min = min(r_norm, g_norm, b_norm)
    delta = c_max - c_min

    # Calculate Lightness (L)
    l_val = (c_max + c_min) / 2.0

    if delta == 0:
        # Grayscale: H=0, S=0
        h_val = 0.0
        s_val = 0.0
    else:
        # Calculate Saturation (S)
        s_val = delta / (1.0 - abs(2.0 * l_val - 1.0))

        # Calculate Hue (H)
        if c_max == r_norm:
            h_val = 60.0 * (((g_norm - b_norm) / delta) % 6)
        elif c_max == g_norm:
            h_val = 60.0 * ((b_norm - r_norm) / delta + 2.0)
        else:  # c_max == b_norm
            h_val = 60.0 * ((r_norm - g_norm) / delta + 4.0)

        # Ensure hue is positive
        if h_val < 0:
            h_val += 360.0

    # Scale S and L back to percentage [0, 100]
    s_percent = s_val * 100.0
    l_percent = l_val * 100.0

    return HSL(h=h_val, s=_clamp(s_percent, 0.0, 100.0), l=_clamp(l_percent, 0.0, 100.0))


# this function is also AI-generated
def _convert_hsl_to_rgb(hsl: HSL) -> RGB:
    h = hsl.h
    # Normalize S and L to range [0, 1]
    s = hsl.s / 100.0
    l = hsl.l / 100.0  # noqa: E741

    if s == 0.0:
        # Grayscale: R, G, B are all equal to L
        r_val = g_val = b_val = l
    else:
        # Calculate Chroma (C), Intermediate Value (X), and Matcher (M)
        c = (1.0 - abs(2.0 * l - 1.0)) * s
        h_prime = h / 60.0
        x = c * (1.0 - abs(h_prime % 2.0 - 1.0))
        m = l - c / 2.0

        # Determine R1, G1, B1 based on Hue sector
        if 0.0 <= h_prime < 1.0:
            r1, g1, b1 = c, x, 0.0
        elif 1.0 <= h_prime < 2.0:
            r1, g1, b1 = x, c, 0.0
        elif 2.0 <= h_prime < 3.0:
            r1, g1, b1 = 0.0, c, x
        elif 3.0 <= h_prime < 4.0:
            r1, g1, b1 = 0.0, x, c
        elif 4.0 <= h_prime < 5.0:
            r1, g1, b1 = x, 0.0, c
        else:  # 5.0 <= h_prime < 6.0
            r1, g1, b1 = c, 0.0, x

        # Final RGB values (scaled and shifted)
        r_val = r1 + m
        g_val = g1 + m
        b_val = b1 + m

    # Scale RGB components to range [0, 255]
    r = r_val * 255.0
    g = g_val * 255.0
    b = b_val * 255.0

    return RGB(r=_clamp(r), g=_clamp(g), b=_clamp(b))


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
