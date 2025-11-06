from .colors.ansi import AnsiCodes_Foreground, LightAnsiCodes_Foreground, AnsiCodes_Background, LightAnsiCodes_Background, ansi_supported as _ansi_supported

ansi_supported = _ansi_supported()


def _get_color_if_supported(color: AnsiCodes_Foreground | LightAnsiCodes_Foreground | AnsiCodes_Background | LightAnsiCodes_Background | str) -> str:
    if ansi_supported:
        if isinstance(color, str):
            return color
        else:
            return color.value
    return ''
