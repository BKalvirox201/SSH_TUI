from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum

from rich.console import RenderableType

from src.renderer.render_context import RenderContext


class NavDirection(Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    Parent = 4
    Children = 5


class Widget(ABC):
    def __init__(self, name: str = "") -> None:
        self.name = name

        # Navigation graph
        self.parent: Widget = self
        self.north: Widget = self
        self.east: Widget = self
        self.south: Widget = self
        self.west: Widget = self

        self.children: list[Widget] = []
        self.last_focused_child: Widget | None = None

    def connect(self, target: Widget, direction: NavDirection) -> None:
        assert target is not self

        match direction:
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
        assert target is not self

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
            target.parent = target
            self.children.remove(target)

            if self.last_focused_child is target:
                self.last_focused_child = None

    @abstractmethod
    def render(self, ctx: RenderContext) -> RenderableType: ...


class ClickableWidget(Widget):
    def __init__(self, name: str = "", callback: Callable = lambda: None) -> None:
        super().__init__(name)
        self.callback = callback

    def clicked(self) -> None:
        self.callback()
