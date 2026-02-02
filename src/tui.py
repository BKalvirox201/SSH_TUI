from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.box import MINIMAL
from rich.console import Console
from time import sleep
from rich.live import Live


class Tui:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layout = self._build_layout()

    def _build_layout(self) -> Layout:
        layout = Layout(name="root")

        layout.split_column(
            Layout(name="top_padding", size=1),
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=1),
        )

        # Top padding: empty
        # layout["top_padding"].update(
        #    Panel("", box=MINIMAL, padding=0, style="on black")
        # )

        # Header: borderless, fill width
        header_text = Text("HEADER", style="bold white on blue", justify="center")
        layout["header"].update(
            Panel(header_text, box=MINIMAL, padding=(0, 0), style="on blue")
        )

        # Main panel: keep border if you want
        layout["main"].update(
            Panel("Main content area", style="white on black", padding=(0, 1))
        )

        # Footer: borderless, two texts justified left and right
        left_text = Text("Left info", style="bold white on dark_green")
        right_text = Text("Right info", style="bold white on dark_green")

        # Combine left and right in a single line using Align
        footer_content = Text.assemble(
            left_text,
            Text(" " * (self.width - len(left_text.plain) - len(right_text.plain))),
            right_text,
        )

        layout["footer"].update(
            Panel(
                renderable="",
                title=footer_content,
                box=MINIMAL,
                padding=(0, 0),
                style="on dark_green",
            )
        )

        return layout

    def resize(self, width: int, height: int):
        """Call this on terminal resize."""
        self.width = width
        self.height = height
        self.layout = self._build_layout()

    def renderable(self):
        """What Live displays."""
        return self.layout


def main():
    console = Console()
    tui = Tui(width=console.width, height=console.height)

    try:
        # Use Live to render the layout in-place
        with Live(tui.renderable(), console=console, refresh_per_second=5, screen=True):
            while True:
                width, height = console.size.width, console.size.height
                tui.resize(width, height)
                sleep(0.2)
    except KeyboardInterrupt:
        console.clear()
        console.show_cursor()
        print("Exited TUI.")


if __name__ == "__main__":
    main()
