from typing import override

from rich import box
from rich.align import Align
from rich.panel import Panel

from renderer.render_context import RenderContext
from ui.widgets.widget import Widget


class TestBody(Widget):
    def __init__(self):
        super().__init__()

    @override
    def render(self, ctx: RenderContext):
        size_text = f"{ctx.width} x {ctx.height}"
        return Panel(
            Align.center(size_text, vertical="middle"),
            box=box.ROUNDED,
            padding=(0, 0),
            border_style="primary",
            expand=True,
            highlight=ctx.highlight,
        )
