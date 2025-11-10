# flake8: noqa


# test_style.py
import kroma

print("\n" + "="*20 + " HTML Colors and HEX Codes " + "="*20 + "\n")

# Using Named HTML Colors
print(kroma.style(
    "This is black text on a spring green background.",
    background=kroma.HTMLColors.SPRINGGREEN,
    foreground=kroma.HTMLColors.BLACK
))

# Partial Color Styling
print(kroma.style(
    "This is normal text with a maroon background.",
    background=kroma.HTMLColors.MAROON
))
print(kroma.style(
    "This is goldenrod text on a normal background.",
    foreground=kroma.HTMLColors.GOLDENROD
))

# Custom HEX Colors
print(kroma.style(
    "This is text with a custom background and foreground.",
    background="#000094",
    foreground="#8CFF7F"
))

print("\n" + "="*20 + " ANSI Colors " + "="*20 + "\n")

# ANSI Colors
print(kroma.style(
    "This is bright blue text on a red background.",
    background=kroma.ANSIColors.RED,
    foreground=kroma.ANSIColors.BRIGHT_BLUE
))

print("\n" + "="*20 + " Custom Styles " + "="*20 + "\n")

# HTML CustomStyle
reusable_style = kroma.CustomStyle(
    foreground=kroma.HTMLColors.DARKKHAKI,
    background=kroma.HTMLColors.NAVY,
    bold=True
)
print(reusable_style("This is some text styled with a CustomStyle!"))
print(reusable_style("Here's another line with the same styling."))
print(reusable_style("Yet another styled line."))

# ANSI CustomStyle
warning_style = kroma.CustomStyle(
    foreground=kroma.ANSIColors.BRIGHT_YELLOW,
    background=kroma.ANSIColors.RED,
    bold=True
)
print(warning_style("Warning: This is important!"))
print(warning_style("Another warning message."))

print("\n" + "="*20 + " Palettes " + "="*20 + "\n")

# Palettes
palette = kroma.palettes.Solarized
kroma.palettes.Solarized.enable()
print(palette.debug("This is a debug message in the Solarized palette"))
print(kroma.palettes.Solarized.error("This is an error message in the Solarized palette"))
print(kroma.palettes.Solarized.info(kroma.style(
    "This is an underlined and bold info message in the Solarized palette",
    bold=True,
    underline=True
)))

print("\n" + "="*20 + " Color Manipulation " + "="*20 + "\n")

# Swapping Colors
print(kroma.style(
    "This is text with a bisque background and a blue violet foreground.\n",
    foreground=kroma.HTMLColors.BLUEVIOLET,
    background=kroma.HTMLColors.BISQUE,
))
print(kroma.style(
    "This is the same text with the foreground and background swapped.",
    foreground=kroma.HTMLColors.BLUEVIOLET,
    background=kroma.HTMLColors.BISQUE,
    swap_foreground_background=True
))

# Lightening and Darkening Colors
print(kroma.style(
    "This is text with colors manipulated at runtime.",
    foreground=kroma.lighten(kroma.HTMLColors.GAINSBORO, 10),
    background=kroma.darken("#2F4F4F", 20)
))

print("\n" + "="*20 + " Text Formatting " + "="*20 + "\n")

# All formatting options combined
print(kroma.style(
    "This is bold, italic, underlined, and strikethrough text.",
    bold=True,
    italic=True,
    underline=True,
    strikethrough=True
))

# Individual formatting
print(kroma.style("This is bold text.", bold=True))
print(kroma.style("This is underlined text.", underline=True))
print(kroma.style(
    "This is italic and strikethrough text.",
    italic=True,
    strikethrough=True
))

# Combining colors and formatting
print(kroma.style(
    "This is bold and italic text with colors.",
    foreground=kroma.ANSIColors.MAGENTA,
    bold=True,
    italic=True
))
