from abc import abstractmethod

from navigation_nodes import NavDirection, NavNode
from rich.panel import Panel


class Widget(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.node: NavNode = NavNode(self)

    def on_select(self):
        self.highlight = True

    def on_deselect(self):
        self.highlight = False

    def connect(self, widget: Widget, direction: NavDirection):
        self.node.connect(widget.node, direction)

    def disconnect(self, widget: Widget):
        self.node.disconnect(widget.node)

    @abstractmethod
    def activate(self):
        # TODO: This is probably going to want to take some page/session data as an arg
        pass
