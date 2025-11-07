import os
import sys
import ctypes
import functools


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
