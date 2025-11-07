# flake8: noqa

#! kroma demonstration


# HTML colors and HEX codes
from kroma import html_color, HTMLColors

# example for blue-violet text with a maroon background
print(html_color.style("This is blue-violet text on a maroon background.", background=HTMLColors.MAROON, foreground=HTMLColors.BLUEVIOLET))

# you can leave out either the background or foreground argument to only set one of them, for example:
print(html_color.style("This is normal text with a chartreuse background.", background=HTMLColors.CHARTREUSE))

# and for only foreground color:
print(html_color.style("This is aquamarine text on a normal background.", foreground=HTMLColors.AQUAMARINE))

# the html_color.style function also accepts HEX color codes, for example:                    ↓ note: the leading '#' is optional but recommended for clarity
print(html_color.style("This is text with a custom background and foreground.\n", background="#000094", foreground="#8CFF7F"))


# ANSI colors
# you may want to use these if you want support on terminals that do not support True Color.
# True Color is a newer standard that allows for millions of colors instead of a limited palette of 16 or 256 colors.

from kroma import ansi_color, ANSIColors

# example for bright blue text with a red background
print(ansi_color.style("This is bright blue text on a red background.", background=ANSIColors.RED, foreground=ANSIColors.BRIGHT_BLUE))

# this function works the same way as html_color.style, except it uses ANSI colors instead of HTML colors.
# so, that means you can also leave out either the background or foreground argument to only set one of them, for example:
print(ansi_color.style("This is normal text with a cyan background.", background=ANSIColors.CYAN))

# or:
print(ansi_color.style("This is bright yellow text on a normal background.", foreground=ANSIColors.BRIGHT_YELLOW))
