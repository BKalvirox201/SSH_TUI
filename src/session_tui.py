from rich.layout import Layout
from rich.panel import Panel


class Tui:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layout = self._build_layout()

    def _build_layout(self) -> Layout:
        layout = Layout(name="root")

        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=1),
        )

        layout["header"].update(Panel("HEADER", style="bold white on blue"))
        layout["main"].update(Panel("Main content area", style="white on black"))
        layout["footer"].update(Panel("FOOTER", style="bold white on dark_green"))

        return layout

    def resize(self, width: int, height: int):
        """Call this on terminal resize."""
        self.width = width
        self.height = height
        self.layout = self._build_layout()

    def renderable(self):
        """What Live displays."""
        return self.layout
