from typing import override

from rich import box
from rich.align import Align
from rich.panel import Panel

from src.renderer.render_context import RenderContext
from src.ui.widgets.widget import ClickableWidget


class TestBody(ClickableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: Make widget render_context
    @override
    def render(self, ctx: RenderContext):
        size_text = f"{ctx.width} x {ctx.height}"
        return Panel(
            Align.center(size_text, vertical="middle"),
            title=f"{{ {self.name} }}" if ctx.focused else f"  {self.name}  ",
            box=box.ROUNDED,
            padding=(0, 0),
            border_style="primary",
            expand=True,
            highlight=False,
        )
