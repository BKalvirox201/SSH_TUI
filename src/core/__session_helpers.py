import asyncio
import re

# OSC templates
OSC_BATCH_TEMPLATE = "\033]4;{indices};?\007"  # e.g. "4;0;?;1;?;2;?"
OSC_FG_QUERY = "\033]10;?\007"
OSC_BG_QUERY = "\033]11;?\007"

# Regex to match rgb responses
RGB_RE = re.compile(r'rgb:([0-9a-fA-F]+)/([0-9a-fA-F]+)/([0-9a-fA-F]+)')

async def _read_osc_response(process, timeout=0.5):
    """Read an OSC response from the terminal."""
    buffer = ""
    try:
        while True:
            chunk = await asyncio.wait_for(process.stdin.read(1), timeout)
            if not chunk:
                break
            buffer += chunk
            if "\x07" in buffer or buffer.endswith("\033\\"):
                return buffer
    except asyncio.TimeoutError:
        return None
    return None

def _parse_rgb(resp):
    """Parse OSC rgb:RRRR/GGGG/BBBB → (r,g,b) 0–255."""
    if not resp:
        return None
    match = RGB_RE.search(resp)
    if not match:
        return None
    r, g, b = match.groups()
    return tuple(int(x, 16) >> 8 for x in (r, g, b))

async def _query_color(process, seq):
    process.stdout.write(seq)
    await process.stdout.drain()
    resp = await _read_osc_response(process)
    return resp

async def get_terminal_palette(process, max_colors=256, batch_size=16):
    """
    Query the full terminal palette in batches + foreground/background.
    Returns a dict:
      {
        "palette": {index: (r,g,b)},
        "foreground": (r,g,b),
        "background": (r,g,b)
      }
    """
    palette = {}

    for start in range(0, max_colors, batch_size):
        indices = ";".join(f"{i};?" for i in range(start, min(start+batch_size, max_colors)))
        seq = f"\033]4;{indices}\007"
        resp = await _query_color(process, seq)

        if not resp:
            continue

        # parse all rgb responses in order
        matches = RGB_RE.findall(resp)
        for i, rgb in enumerate(matches):
            idx = start + i
            r, g, b = rgb
            palette[idx] = (int(r,16)>>8, int(g,16)>>8, int(b,16)>>8)

    # foreground/background
    fg_resp = await _query_color(process, OSC_FG_QUERY)
    bg_resp = await _query_color(process, OSC_BG_QUERY)

    fg = _parse_rgb(fg_resp)
    bg = _parse_rgb(bg_resp)

    return {"palette": palette, "foreground": fg, "background": bg}
