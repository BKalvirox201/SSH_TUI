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
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=1),
        )

        # HEADER
        header_text = Text(
            "HEADER",
            style="bold white on blue",
            justify="center",
        )

        layout["header"].update(
            Panel(
                renderable=header_text,
                box=MINIMAL,
                padding=(0, 0),
                style="on blue",
            )
        )

        # MAIN
        layout["main"].update(
            Panel(
                "Main content area",
                style="white on rgb(10,25,60)",
                border_style="bright_blue",
                padding=(0, 1),
            )
        )

        # FOOTER
        left_text = Text("Left info", style="bold white on blue")
        right_text = Text("Right info", style="bold white on blue")

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
                style="on blue",
            )
        )

        return layout

    def resize(self, width: int, height: int):
        """Call this on terminal resize."""
        self.width = width
        self.height = height
        self.layout = self._build_layout()

    def render(self):
        return self.layout


def main():
    print("Exited TUI.")


if __name__ == "__main__":
    main()
