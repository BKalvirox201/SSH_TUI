from abc import ABC, abstractmethod

from rich.layout import Layout

from events.page_events import PageEvent
from renderer.render_context import RenderContext


class PageData:
    pass


class Page(ABC):
    @abstractmethod
    def render(self, ctx: RenderContext) -> Layout:
        raise NotImplementedError

    @abstractmethod
    def handle_event(self, event: PageEvent):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__
