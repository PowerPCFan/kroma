from enum import Enum
import os
import sys
import ctypes
import functools


ANSI = "\033["


class AnsiCodes_Foreground(Enum):
    RESET = f"{ANSI}0m"

    RED = f"{ANSI}31m"
    YELLOW = f"{ANSI}33m"
    GREEN = f"{ANSI}32m"
    CYAN = f"{ANSI}36m"
    BLUE = f"{ANSI}34m"
    PURPLE = f"{ANSI}35m"
    WHITE = f"{ANSI}37m"


class AnsiCodes_Background(Enum):
    RESET = f"{ANSI}0m"

    RED = f"{ANSI}41m"
    YELLOW = f"{ANSI}43m"
    GREEN = f"{ANSI}42m"
    CYAN = f"{ANSI}46m"
    BLUE = f"{ANSI}44m"
    PURPLE = f"{ANSI}45m"
    WHITE = f"{ANSI}47m"


class LightAnsiCodes_Foreground(Enum):
    RESET = f"{ANSI}0m"

    LIGHT_CYAN = f"{ANSI}96m"
    # todo: expand with more colors than just light cyan


class LightAnsiCodes_Background(Enum):
    RESET = f"{ANSI}0m"

    LIGHT_CYAN = f"{ANSI}106m"
    # todo: expand with more colors than just light cyan


def enable_ansi() -> bool:
    """
    (Windows-only)

    Returns a boolean value indicating if ANSI sequences were enabled or not
    """
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        new_mode = mode.value | 0x0004
        return kernel32.SetConsoleMode(handle, new_mode) != 0
    except Exception:
        return False


def supports_ansi(vt_enabled: bool) -> bool:
    if vt_enabled:
        return True

    if os.name.lower() != 'nt':
        return sys.stdout.isatty()

    return (
        sys.stdout.isatty() and (                                               # is a TTY and not redirected
            ('ANSICON' in os.environ) or                                        # Terminal uses ANSICON
            ('WT_SESSION' in os.environ) or                                     # Is using Windows Terminal
            ((os.getenv('TERM_PROGRAM') or 'unknown').lower() == 'vscode') or   # Is using VSCode terminal
            (('TERM' in os.environ) and ('xterm' in os.environ['TERM']))        # xterm-compatible terminal
        )
    )


@functools.lru_cache(maxsize=None)
def ansi_supported() -> bool:
    vt_enabled = False
    if os.name == 'nt':
        vt_enabled = enable_ansi()

    return supports_ansi(vt_enabled)
