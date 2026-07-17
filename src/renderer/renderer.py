from typing import TYPE_CHECKING

from render_context import RenderContext
from rich.console import Console
from rich.theme import Theme

if TYPE_CHECKING:
    from core.session.session import SSHServerSession


class Renderer:
    def __init__(self, session: SSHServerSession):
        self.session = session
        self.console = Console(
            file=session.writer,
            force_terminal=True,
            color_system="truecolor",
            record=True,
        )

    # NOTE: Console should be private variable
    def set_console_width_height(self, width: int, height: int):
        self.console.width = width
        self.console.height = height

    def render_current_page(self):
        self.session.writer.clear_screen()
        current_page_layout = self.session.current_page.render(
            self.create_render_context()
        )
        self.console.print(current_page_layout, soft_wrap=False, end="")
        recorded_tui = self.console.export_text(clear=True, styles=True)[:-2]
        self.session.writer.write_tui(recorded_tui)

    def create_render_context(self) -> RenderContext:
        return RenderContext(
            self.console.width,
            self.console.height,
            False,  # NOTE: Maybe we need two types  of render context, page and widget
        )

    def set_theme(self, new_theme: Theme):
        self.console.push_theme(new_theme)
        # Render directly or queue event or rerender in the main function... We need to decide on 1 place to call render
