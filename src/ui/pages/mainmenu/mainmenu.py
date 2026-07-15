from typing import override

from rich.layout import Layout

from renderer.render_context import RenderContext
from ui.pages.mainmenu.body import TestBody as Body
from ui.pages.mainmenu.footer import Footer
from ui.pages.page import Page
from ui.widgets.cursor import Cursor
from ui.widgets.widget import NavDirection

# from src.ui.pages.panels.header import Header


class MainMenu(Page):
    def __init__(self) -> None:
        # Geometry
        self.layout = Layout(name="root")
        self.inner_layout = Layout(name="inner_layout")

        self.inner_layout.split_column(
            Layout(name="upper"),
            Layout(name="lower"),
        )
        self.inner_layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )

        self.layout.split_column(
            # Layout(name="header", size=6),
            self.inner_layout,
            Layout(name="footer", size=1),
        )

        # Widgets
        self.body_1 = Body()
        self.body_2 = Body()
        self.body_3 = Body()
        self.footer = Footer(
            left=" Navigate: h/j/k/l or a/s/w/d, q to quit",
            right="Trademark: SaltyCorp 2026 ",
        )

        # Connect the Widgets
        self.body_1.connect(self.body_2, NavDirection.South)

        # Cursor
        self.cursor = Cursor(self.body_1)

    @override
    def render(self, ctx: RenderContext) -> Layout:
        height_excl_footer = ctx.height - 1
        half_height = height_excl_footer / 2
        half_width = ctx.width / 2

        body_1_ctx = ctx.child(
            height=half_height,
            focused=self.body_1 is self.cursor.focused,
        )
        body_2_ctx = ctx.child(
            width=half_width,
            height=height_excl_footer - half_height,
            focused=self.body_2 is self.cursor.focused,
        )
        body_3_ctx = ctx.child(
            width=ctx.width - half_width,
            height=height_excl_footer - half_height,
            focused=self.body_3 is self.cursor.focused,
        )
        footer_ctx = ctx.child(height=1)

        self.layout["inner_layout"]["upper"].update(self.body_1.render(body_1_ctx))
        self.layout["inner_layout"]["lower"]["left"].update(
            self.body_2.render(body_2_ctx)
        )
        self.layout["inner_layout"]["lower"]["right"].update(
            self.body_3.render(body_3_ctx)
        )
        self.layout["footer"].update(self.footer.render(footer_ctx))

        return self.layout

    @override
    def handle_event(self, event, state_data: dict):
        pass
