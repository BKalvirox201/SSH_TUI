from typing import override

from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel

from src.renderer.render_context import RenderContext
from src.ui.pages.page import Page
from src.ui.pages.panels.footer import Footer
from src.ui.pages.panels.header import Header


class MainMenu(Page):
    def __init__(self) -> None:
        super().__init__()

        self.layout = Layout(name="root")
        self.layout.split_column(
            Layout(name="header", size=6),
            Layout(name="body"),
            Layout(name="footer", size=1),
        )

    @override
    def render(self, ctx: RenderContext) -> Layout:

        header = Header(title="Coffee", font="ansi_shadow")
        self.layout["header"].update(header.render(ctx))

        size_text = f"{ctx.width} x {ctx.height}"

        body_panel = Panel(
            Align.center(size_text, vertical="middle"),
            box=box.ROUNDED,
            padding=(0, 0),
            border_style="primary",
            expand=True,
        )
        self.layout["body"].update(body_panel)

        footer = Footer(
            left=" Navigate: h/j/k/l or a/s/w/d, q to quit",
            right="Trademark: SaltyCorp 2026 ",
        )
        self.layout["footer"].update(footer.render(ctx.width))
        return self.layout

    @override
    def handle_event(self, event, state_data: dict):
        pass
