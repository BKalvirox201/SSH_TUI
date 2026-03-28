from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel

from src.pages.page import Page
from src.renderer.render_context import RenderContext


class MainMenu(Page):
    """Main menu page with header, footer, and dynamic center panel."""

    def __init__(self) -> None:
        super().__init__()
        self.layout = Layout(name="root")

    def render(self, ctx: RenderContext) -> Layout:
        size_text = f"{ctx.width} x {ctx.height}"
        panel_content = Align.center(size_text, vertical="middle")
        center_panel = Panel(
            panel_content,
            title="MainMenu",
            border_style="primary",
            padding=(0, 0),
        )
        self.layout["root"].update(center_panel)

        return self.layout

    def handle_event(self, event, state_data: dict):
        pass
