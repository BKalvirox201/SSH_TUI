from __future__ import annotations

from abc import ABC, abstractmethod

from rich.layout import Layout

from src.renderer.render_context import RenderContext
from src.ui.widgets.widget import Widget


class PageData:
    pass


class Page(ABC):
    def __init__(self, start_widget: Widget) -> None:
        self.focused_widget: Widget = start_widget

    @abstractmethod
    def render(self, ctx: RenderContext) -> Layout: ...

    @property
    def name(self) -> str:
        return self.__class__.__name__
