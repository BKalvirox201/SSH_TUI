import asyncio
from dataclasses import dataclass
import logging

from src.pages.page import Page
from src.renderer.renderer import Renderer


@dataclass
class SessionState:
    """stores persistant data across pages"""

    def __init__(
        self,
        current_page: str,
        pages: dict[str, Page],
        page_data: dict[str, dict],
        # Input Handler,
        renderer: Renderer,
        event_queue: asyncio.Queue,
        logger: logging.LoggerAdapter,
    ):
        self.current_page: str = current_page
        self.pages: dict[str, Page] = pages
        self.page_data: dict[str, dict] = page_data
        self.renderer: Renderer = renderer
        self.event_queue: asyncio.Queue = event_queue
        self.logger: logging.LoggerAdapter = logger
