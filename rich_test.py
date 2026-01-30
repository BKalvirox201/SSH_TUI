import asyncio
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live

class SimpleTui:
    def __init__(self):
        self.console = Console()
        self.layout = Layout(name="root")

        # Build the layout
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=1)
        )

    def build_layout(self):
        # Update the sections with some content
        self.layout["header"].update(Panel("HEADER", style="bold white on blue"))
        self.layout["main"].update(Panel("Main content area", style="white on black"))
        self.layout["footer"].update(Panel("FOOTER", style="bold white on dark_green"))

    async def run(self):
        self.build_layout()
        # Use Live to render layout dynamically
        with Live(self.layout, console=self.console, refresh_per_second=4, screen=True):
            while True:
                # Example of dynamic content update
                self.layout["main"].update(
                    Panel(f"Main content area\nCounter: {asyncio.get_running_loop().time():.1f}",
                          style="white on black")
                )
                await asyncio.sleep(0.5)

if __name__ == "__main__":
    tui = SimpleTui()
    asyncio.run(tui.run())

