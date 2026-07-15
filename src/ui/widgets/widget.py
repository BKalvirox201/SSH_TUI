from abc import ABC, abstractmethod
from typing import Enum

from rich.render import Renderable

from src.render import RenderContext


class NavDirection(Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    Parent = 4
    Children = 5


class Widget(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # NOTE: Nodes link to themselves if they don't link to other nodes
        self.parent: Widget = self
        self.north: Widget = self
        self.east: Widget = self
        self.south: Widget = self
        self.west: Widget = self
        self.children: list[Widget] = []

    def select(self):
        self.highlight = True

    def deselect(self):
        self.highlight = False

    def connect(self, target: Widget, link_direction: NavDirection) -> None:
        assert target != self  # NOTE: cannot manually connect a node to itself
        match link_direction:
            case NavDirection.North:
                self.north = target
            case NavDirection.East:
                self.east = target
            case NavDirection.South:
                self.south = target
            case NavDirection.West:
                self.west = target
            case NavDirection.Parent:
                self.parent = target
                target.children.append(self)
            case NavDirection.Children:
                target.parent = self
                self.children.append(target)

    def disconnect(self, target: Widget) -> None:
        assert target != self  # NOTE: cannot manually disconnect a node from itself
        if self.north is target:
            self.north = self
        elif self.east is target:
            self.east = self
        elif self.south is target:
            self.south = self
        elif self.west is target:
            self.west = self
        elif self.parent is target:
            self.parent = self
            target.children.remove(self)
        elif target in self.children:
            target.parent = self
            self.children.remove(target)

    @abstractmethod
    def render(self, ctx: RenderContext) -> Renderable:
        pass
