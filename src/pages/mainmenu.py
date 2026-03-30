from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from src.pages.page import Page
from src.renderer.render_context import RenderContext


class MainMenu(Page):
    """Main menu page with header, footer, and dynamic center panel."""

    def __init__(self) -> None:
        super().__init__()

        self.layout = Layout(name="root")

        self.layout.split_column(
            Layout(name="body"),
            Layout(name="footer", size=1),  # exactly 1 row
        )

    def render(self, ctx: RenderContext) -> Layout:
        size_text = f"{ctx.width} x {ctx.height}"

        # --- Body ---
        body_panel = Panel(
            Align.center(size_text, vertical="middle"),
            box=box.ROUNDED,
            padding=(0, 0),
            border_style="primary",
            expand=True,
        )
        self.layout["body"].update(body_panel)

        footer_text = Text()
        footer_text.append("Left text", style="bold")
        footer_text.append(" " * (ctx.width - len("Left text") - len("Right text")))
        footer_text.append("Right text", style="bold")

        self.layout["footer"].update(footer_text)

        return self.layout

    def handle_event(self, event, state_data: dict):
        pass
