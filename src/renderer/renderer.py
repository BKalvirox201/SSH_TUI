from rich.console import Console
from rich.layout import Layout
from rich.theme import Theme

from src.core.io.writer import SSHChannelWriter
from src.renderer.render_context import RenderContext


class Renderer:
    def __init__(self, writer: SSHChannelWriter):
        self.writer = writer
        self.current_theme: Theme
        self.console = Console(
            force_terminal=True,
            color_system="truecolor",
            record=True,
        )

    def render_page(self, page_layout: Layout):
        self.writer.clear_screen()
        self.console.print(page_layout, soft_wrap=False, end="")
        recorded_tui = self.console.export_text(clear=True, styles=True)[:-2]
        self.writer.write_tui(recorded_tui)

    def resize_console(self, width: int, height: int):
        self.console.width = width
        self.console.height = height

    def create_render_context(self) -> RenderContext:
        return RenderContext(
            self.console.width, self.console.height, self.current_theme
        )

    def set_theme(self, new_theme: Theme):
        self.current_theme = new_theme
        self.console.push_theme(new_theme)
