from typing import override

from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from src.events.page_events import NavEvent, NavDirectionEnum
from src.ui.widget import Widget
from src.pages.page import Page

class TestPage(Page):
    def __init__(self) -> None:
        super().__init__()

        self.layout = Layout(name="root")

        self.widget_one = Widget(Text("Widget 1"))
        self.widget_two = Widget(Text("Widget 2"))
        self.widget_three = Widget(Text("Widget 3"))

        self.widget_one.set_neighbouring_widgets(north_panel=self.widget_three, south_panel=self.widget_two)
        self.widget_two.set_neighbouring_widgets(north_panel=self.widget_one, south_panel=self.widget_three)
        self.widget_three.set_neighbouring_widgets(north_panel=self.widget_two, south_panel=self.widget_one)

        self.active_widget = self.widget_one

    @override
    def render(self, ctx: RenderContext) -> Layout:
        return self.layout
    
    @override
    def handle_event(self, event, state_data: dict):
        if isinstance(event, NavEvent):
            neighbour = self.active_widget.get_neighbouring_widget(event.direction)
            if neighbour:
                self.active_widget.style = "white"
                self.active_widget = neighbour
                self.active_widget.style = "bold white"
                
