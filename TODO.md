# Kroma To-do List

## New Features

### High Priority

- Color Palettes
  - Dataclass-based palettes like Gruvbox.error(), Gruvbox.warning(), etc
  - These can utilize the existing CustomStyle class

- Gradients
  - Using True Color
  - Linear foreground & background gradients
  - Controllable stops

### Medium Priority

- True Color support detection (if possible)

- 256-Color Support (8-bit)
  - Great for if you want a wider range of colors but need compatibility with older terminals / don't want to use True Color

### Color Utilities / Helpers
- Contrast / luminance checks (is_light(), contrast())
- Color blending / interpolation (blend(color1, color2, ratio))
  - Similar to the lighten() / darken() functions I have right now
- Random Color Generation (random_color())

## Improvements / Fixes
- Break up functions and improve code in general
- Possibly combine the two style() functions, since it's not really necessary to have both and it complicates things a lot
