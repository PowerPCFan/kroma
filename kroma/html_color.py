from .enums import HTMLColors, StyleType
from .utils import _convert_html_hex_to_ansi


def style(text: str, foreground: str | HTMLColors | None = None, background: str | HTMLColors | None = None) -> str:
    if foreground is None and background is None:
        return text
    elif foreground is not None and background is None:
        return _convert_html_hex_to_ansi(text, foreground, StyleType.FOREGROUND)
    elif foreground is None and background is not None:
        return _convert_html_hex_to_ansi(text, background, StyleType.BACKGROUND)
    elif foreground is not None and background is not None:
        return _convert_html_hex_to_ansi(_convert_html_hex_to_ansi(text, foreground, StyleType.FOREGROUND), background, StyleType.BACKGROUND)

    return text
