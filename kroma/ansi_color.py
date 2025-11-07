from .enums import ANSIColors, StyleType
from .utils import _get_ansi_color_code


def style(text: str, foreground: ANSIColors | None = None, background: ANSIColors | None = None) -> str:
    if foreground is None and background is None:
        return text
    elif foreground is not None and background is None:
        return _get_ansi_color_code(text, foreground, StyleType.FOREGROUND)
    elif foreground is None and background is not None:
        return _get_ansi_color_code(text, background, StyleType.BACKGROUND)
    elif foreground is not None and background is not None:
        return _get_ansi_color_code(_get_ansi_color_code(text, foreground, StyleType.FOREGROUND), background, StyleType.BACKGROUND)

    return text
