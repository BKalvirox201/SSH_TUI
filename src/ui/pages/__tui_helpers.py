""" Helpers for the TUI """

def create_rich_styles(palette_info):
    """
    Convert raw terminal palette into semantic Rich styles.
    Returns a dict of named styles.
    """
    fg = palette_info["foreground"] or (255, 255, 255)
    bg = palette_info["background"] or (0, 0, 0)

    luminance = (0.299*bg[0] + 0.587*bg[1] + 0.114*bg[2])
    is_dark = luminance < 128
    palette = palette_info.get("palette", {})
    styles = {
        "primary": f"rgb{palette.get(33, fg)}" if 33 in palette else f"rgb{fg}",   # ANSI yellow
        "secondary": f"rgb{palette.get(36, fg)}" if 36 in palette else f"rgb{fg}", # ANSI cyan
        "error": f"rgb{palette.get(1, fg)}" if 1 in palette else f"rgb{fg}",       # ANSI red
        "highlight": f"rgb{palette.get(9, fg)}" if 9 in palette else f"rgb{fg}",   # ANSI bright red
        "background": f"rgb{bg}",
        "foreground": f"rgb{fg}",
        "heading": f"rgb{palette.get(12, fg)}" if 12 in palette else f"rgb{fg}",   # ANSI blue
    }

    return styles, is_dark
