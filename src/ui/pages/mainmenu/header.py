import pyfiglet
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from src.renderer.render_context import RenderContext


class Header:
    def __init__(self, *, title: str, font: str):
        self.title = title
        self.font = font

        self.layout = Layout()
        self.layout.split_row(
            Layout(name="left"),
            Layout(name="center", ratio=1),
            Layout(name="right"),
        )

    def _render_logo(self):
        ascii_art = pyfiglet.figlet_format(self.title, font=self.font)
        lines = ascii_art.splitlines()

        width = max(len(line) for line in lines) if lines else 0
        text = Text("\n".join(lines))

        return Align.left(text), width

    def _render_center(self):
        return Text("")

    def _render_login(self):
        panel = Panel(
            "Login\n[username]\n[password]",
            title="User",
            border_style="green",
        )
        contentwidth = max(12, max(len("Login"), len("[username]"), len("[password]")))
        width = contentwidth + 4

        return panel, width

    def render(self, ctx: RenderContext) -> Layout:
        logo_renderable, logowidth = self._render_logo()
        self.layout["left"].size = logowidth
        self.layout["left"].update(logo_renderable)

        login_renderable, loginwidth = self._render_login()
        self.layout["right"].size = loginwidth
        self.layout["right"].update(login_renderable)

        self.layout["center"].update(self._render_center())

        return self.layout
