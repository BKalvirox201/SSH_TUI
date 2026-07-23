from typing import override

from rich.layout import Layout

from src.renderer.render_context import RenderContext
from src.ui.pages.mainmenu.body import TestBody as Body
from src.ui.pages.mainmenu.footer import Footer
from src.ui.pages.page import Page
from src.ui.widgets.widget import NavDirection


class MainMenu(Page):
    def __init__(self) -> None:
        # Widgets
        self.body_1 = Body("Body 1", lambda: print("Body 1"))
        self.body_2 = Body("Body 2", lambda: print("Body 2"))
        self.body_3 = Body("Body 3", lambda: print("Body 3"))

        super().__init__(start_widget=self.body_1)

        self.footer = Footer(
            left=" Navigate: h/j/k/l or a/s/w/d, q to quit",
            right="Trademark: SaltyCorp 2026 ",
        )

        self.layout = Layout(name="root")
        self.inner = Layout(name="inner")

        self.layout.split_column(
            self.inner,
            Layout(name="footer", size=1),
        )

        self.inner.split_column(
            Layout(name="upper"),
            Layout(name="lower"),
        )

        self.inner["lower"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )

        # Navigation graph
        self.body_1.connect(self.body_2, NavDirection.South)
        self.body_2.connect(self.body_1, NavDirection.North)

        self.body_2.connect(self.body_3, NavDirection.East)
        self.body_3.connect(self.body_2, NavDirection.West)

        self.body_3.connect(self.body_1, NavDirection.North)

    @override
    def render(self, ctx: RenderContext) -> Layout:
        height_excl_footer = ctx.height - 1
        half_height = height_excl_footer // 2
        half_width = ctx.width // 2

        self.layout["inner"]["upper"].update(
            self.body_1.render(
                ctx.child(
                    height=half_height,
                    focused=self.focused_widget is self.body_1,
                )
            )
        )

        self.layout["inner"]["lower"]["left"].update(
            self.body_2.render(
                ctx.child(
                    width=half_width,
                    height=height_excl_footer - half_height,
                    focused=self.focused_widget is self.body_2,
                )
            )
        )

        self.layout["inner"]["lower"]["right"].update(
            self.body_3.render(
                ctx.child(
                    width=ctx.width - half_width,
                    height=height_excl_footer - half_height,
                    focused=self.focused_widget is self.body_3,
                )
            )
        )

        self.layout["footer"].update(self.footer.render(ctx.child(height=1)))

        return self.layout
