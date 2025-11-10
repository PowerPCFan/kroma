from .styles import CustomStyle


def _set_global_terminal_colors(*, bg: str, fg: str):
    print(f"\033]11;{bg}\007", end="", flush=True)  # set global background color
    print(f"\033]10;{fg}\007", end="", flush=True)  # set global foreground color


class Gruvbox:
    @staticmethod
    def enable():
        _set_global_terminal_colors(bg="#282828", fg="#fbf1c7")

    @staticmethod
    def info(text: str):
        return CustomStyle(foreground="#458588")(text)

    @staticmethod
    def debug(text: str):
        return CustomStyle(foreground="#689d6a")(text)

    @staticmethod
    def warning(text: str):
        return CustomStyle(foreground="#d79921")(text)

    @staticmethod
    def error(text: str):
        return CustomStyle(foreground="#cc241d")(text)

    @staticmethod
    def critical(text: str):
        return CustomStyle(foreground="#b16286")(text)

    @staticmethod
    def success(text: str):
        return CustomStyle(foreground="#98971a")(text)


class Bootstrap:
    @staticmethod
    def enable():
        pass  # no need to set bg/fg for bootstrap since they are really close to most terminal defaults

    @staticmethod
    def info(text: str):
        return CustomStyle(foreground="#0d6efd")(text)

    @staticmethod
    def debug(text: str):
        return CustomStyle(foreground="#6c757d")(text)

    @staticmethod
    def warning(text: str):
        return CustomStyle(foreground="#ffc107")(text)

    @staticmethod
    def error(text: str):
        return CustomStyle(foreground="#dc3545")(text)

    @staticmethod
    def critical(text: str):
        return CustomStyle(foreground="#6f42c1")(text)

    @staticmethod
    def success(text: str):
        return CustomStyle(foreground="#198754")(text)


class Solarized:
    @staticmethod
    def enable():
        _set_global_terminal_colors(bg="#002b36", fg="#fdf6e3")

    @staticmethod
    def info(text: str):
        return CustomStyle(foreground="#268bd2")(text)

    @staticmethod
    def debug(text: str):
        return CustomStyle(foreground="#2aa198")(text)

    @staticmethod
    def warning(text: str):
        return CustomStyle(foreground="#b58900")(text)

    @staticmethod
    def error(text: str):
        return CustomStyle(foreground="#dc322f")(text)

    @staticmethod
    def critical(text: str):
        return CustomStyle(foreground="#d33682")(text)

    @staticmethod
    def success(text: str):
        return CustomStyle(foreground="#859900")(text)
