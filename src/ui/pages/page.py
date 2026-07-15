from abc import abstractmethod

from rich.layout import Layout

from src.events.page_events import PageEvent
from src.renderer.render_context import RenderContext


class PageData:
    pass


class Page:
    @abstractmethod
    def render(self, ctx: RenderContext) -> Layout:
        raise NotImplementedError

    @abstractmethod
    def handle_event(self, event: PageEvent, state_data: dict):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__
