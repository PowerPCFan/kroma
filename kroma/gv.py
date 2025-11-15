from .ansi_tools import ansi_supported as _as

ANSI = "\033["
RESET = f"{ANSI}0m"

ansi_supported = _as()
