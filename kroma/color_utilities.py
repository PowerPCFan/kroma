import secrets
from .enums import HTMLColors, RGB, HSL
from .utils import (
    _convert_hex_code_to_rgb,
    _convert_rgb_to_hex_code,
    _clamp,
    _convert_hex_to_hsl,
    _convert_hsl_to_hex
)


def lighten(color: str | HTMLColors, amount: int) -> str:
    hsl = _convert_hex_to_hsl(color.value if isinstance(color, HTMLColors) else color)
    new_l = _clamp((hsl.l + amount), 0, 100)

    return _convert_hsl_to_hex(HSL(h=hsl.h, s=hsl.s, l=new_l))


def darken(color: str | HTMLColors, amount: int) -> str:
    return lighten(color, -amount)


def saturate(color: str | HTMLColors, amount: int) -> str:
    hex_color = (color.value if isinstance(color, HTMLColors) else color)
    hsl = _convert_hex_to_hsl(hex_color)

    new_s = _clamp((hsl.s + amount), 0, 100)

    return _convert_hsl_to_hex(HSL(h=hsl.h, s=new_s, l=hsl.l))


def desaturate(color: str | HTMLColors, amount: int) -> str:
    return saturate(color, -amount)


def mix(color1: str | HTMLColors, color2: str | HTMLColors, ratio: float = 50.0) -> str:
    ratio = ratio / 100.0

    rgb1 = _convert_hex_code_to_rgb((color1.value if isinstance(color1, HTMLColors) else color1))
    rgb2 = _convert_hex_code_to_rgb((color2.value if isinstance(color2, HTMLColors) else color2))

    new_r = _clamp(rgb1.r * (1 - ratio) + rgb2.r * ratio)
    new_g = _clamp(rgb1.g * (1 - ratio) + rgb2.g * ratio)
    new_b = _clamp(rgb1.b * (1 - ratio) + rgb2.b * ratio)

    return _convert_rgb_to_hex_code(RGB(r=new_r, g=new_g, b=new_b))


def invert(color: str | HTMLColors) -> str:
    color = (color.value if isinstance(color, HTMLColors) else color)
    rgb = _convert_hex_code_to_rgb(color)

    new_r = 255 - rgb.r
    new_g = 255 - rgb.g
    new_b = 255 - rgb.b

    return _convert_rgb_to_hex_code(RGB(r=new_r, g=new_g, b=new_b))


def convert_to_grayscale(color: str | HTMLColors) -> str:
    color = (color.value if isinstance(color, HTMLColors) else color)
    rgb = _convert_hex_code_to_rgb(color)

    grayscale = _clamp((0.299 * rgb.r) + (0.587 * rgb.g) + (0.114 * rgb.b))

    return _convert_rgb_to_hex_code(RGB(r=grayscale, g=grayscale, b=grayscale))


def random_color() -> str:
    def _rdm() -> int:
        # return random.randint(0, 255)
        return secrets.randbelow(256)

    return _convert_rgb_to_hex_code(RGB(r=_rdm(), g=_rdm(), b=_rdm()))
