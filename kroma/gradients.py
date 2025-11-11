from .enums import HTMLColors
from .enums import StyleType, RGB
from .utils import RESET, _convert_hex_code_to_rgb, _convert_rgb_to_ansi_sequence, _get_color_if_supported, _fix_text


# class CustomGradient:
#     def __init__(
#         self,
#         *,  # Enforce keyword arguments from here on
#         start_color: str | HTMLColors | None,
#         end_color: str | HTMLColors | None,
#         steps: int | None = None
#     ):

#         self.kwargs = {
#             "start_color": start_color,
#             "end_color": end_color,
#             "steps": steps
#         }

#     def __call__(self, text: str) -> str:
#         return gradient(text, **self.kwargs)


# def _apply_gradient_to_line(
#     text: str,
#     start_color: str,
#     end_color: str,
#     steps: int | None = None
# ) -> str:

#     start_rgb = _convert_hex_code_to_rgb(start_color)
#     end_rgb = _convert_hex_code_to_rgb(end_color)

#     text_len = len(text)
#     if text_len == 0:
#         return ""

#     if steps is None:
#         steps = text_len

#     gradient_chars: list[str] = []

#     if text_len == 1:
#         return (
#             _get_color_if_supported(_convert_rgb_to_ansi_sequence(start_rgb, StyleType.FOREGROUND)) +
#             _fix_text(text) +
#             _get_color_if_supported(RESET)
#         )

#     if steps <= 1:
#         delta_r, delta_g, delta_b = (0,) * 3
#     else:
#         delta_r = (end_rgb.r - start_rgb.r) / (steps - 1)
#         delta_g = (end_rgb.g - start_rgb.g) / (steps - 1)
#         delta_b = (end_rgb.b - start_rgb.b) / (steps - 1)

#     for index, char in enumerate(text):
#         color_step = min(index * (steps - 1) // (text_len - 1) if text_len > 1 else 0, steps - 1)

#         current_r = int(start_rgb.r + color_step * delta_r)
#         current_g = int(start_rgb.g + color_step * delta_g)
#         current_b = int(start_rgb.b + color_step * delta_b)

#         current_rgb = RGB(current_r, current_g, current_b)

#         colored_char = (
#             _get_color_if_supported(_convert_rgb_to_ansi_sequence(current_rgb, StyleType.FOREGROUND)) +
#             _fix_text(char) +
#             _get_color_if_supported(RESET)
#         )
#         gradient_chars.append(colored_char)

#     return "".join(gradient_chars)


# def gradient(
#     text: str,
#     *,
#     start_color: str | HTMLColors,
#     end_color: str | HTMLColors,
#     steps: int | None = None
# ) -> str:
#     if isinstance(start_color, HTMLColors):
#         start_color = start_color.value
#     if isinstance(end_color, HTMLColors):
#         end_color = end_color.value

#     splitter = "\n"
#     lines = text.split(splitter)
#     if len(lines) > 1:
#         # treat each line as a separate entity to avoid the gradient being spread across multiple lines
#         gradient_lines = []
#         for line in lines:
#             if line:
#                 gradient_lines.append(_apply_gradient_to_line(line, start_color, end_color, steps))
#             else:
#                 gradient_lines.append(line)
#         return splitter.join(gradient_lines)

#     return _apply_gradient_to_line(text, start_color, end_color, steps)


class CustomGradient:
    def __init__(
        self,
        *,  # Enforce keyword arguments from here on
        stops: tuple[str | HTMLColors, ...],
        style_type: StyleType = StyleType.FOREGROUND,
        steps: int | None = None
    ):

        self.kwargs = {
            "stops": stops,
            "style_type": style_type,
            "steps": steps
        }

    def __call__(self, text: str) -> str:
        return gradient(text, **self.kwargs)


def _apply_gradient_to_line(
    text: str,
    color_stops: list[str],
    style_type: StyleType,
    steps: int | None = None
) -> str:
    text_len = len(text)
    if text_len == 0:
        return ""

    if len(color_stops) < 2:
        if len(color_stops) == 1:
            rgb = _convert_hex_code_to_rgb(color_stops[0])
            color_sequence = _convert_rgb_to_ansi_sequence(rgb, style_type)
            return _get_color_if_supported(color_sequence) + _fix_text(text) + _get_color_if_supported(RESET)
        return text

    if steps is None:
        steps = text_len

    gradient_chars: list[str] = []

    rgb_stops = [_convert_hex_code_to_rgb(color) for color in color_stops]

    if text_len == 1:
        color_sequence = _convert_rgb_to_ansi_sequence(rgb_stops[0], style_type)
        return _get_color_if_supported(color_sequence) + _fix_text(text) + _get_color_if_supported(RESET)

    for index, char in enumerate(text):
        if text_len == 1:
            position = 0.0
        else:
            position = index / (text_len - 1)

        segment_length = 1.0 / (len(rgb_stops) - 1)
        segment_index = min(int(position / segment_length), len(rgb_stops) - 2)

        segment_position = (position - segment_index * segment_length) / segment_length

        start_rgb = rgb_stops[segment_index]
        end_rgb = rgb_stops[segment_index + 1]

        current_r = int(start_rgb.r + (end_rgb.r - start_rgb.r) * segment_position)
        current_g = int(start_rgb.g + (end_rgb.g - start_rgb.g) * segment_position)
        current_b = int(start_rgb.b + (end_rgb.b - start_rgb.b) * segment_position)

        current_rgb = RGB(current_r, current_g, current_b)

        colored_char = (
            _get_color_if_supported(_convert_rgb_to_ansi_sequence(current_rgb, style_type)) +
            _fix_text(char) +
            _get_color_if_supported(RESET)
        )
        gradient_chars.append(colored_char)

    return "".join(gradient_chars)


def gradient(
    text: str,
    *,
    stops: tuple[str | HTMLColors, ...],
    style_type: StyleType = StyleType.FOREGROUND,
    steps: int | None = None
) -> str:
    color_stops = []
    for stop in stops:
        if isinstance(stop, HTMLColors):
            color_stops.append(stop.value)
        else:
            color_stops.append(stop)

    splitter = "\n"
    lines = text.split(splitter)
    if len(lines) > 1:
        # treat each line as a separate entity to avoid the gradient being spread across multiple lines
        gradient_lines = []
        for line in lines:
            if line:
                gradient_lines.append(_apply_gradient_to_line(line, color_stops, style_type, steps))
            else:
                gradient_lines.append(line)
        return splitter.join(gradient_lines)

    return _apply_gradient_to_line(text, color_stops, style_type, steps)
