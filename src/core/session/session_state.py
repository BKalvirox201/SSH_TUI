import asyncio
from dataclasses import dataclass
import logging

from renderer.renderer import Renderer
from ui.pages.page import Page


@dataclass
class SessionState:
    """stores persistant data across pages"""

    current_page: str
    pages: dict[str, Page]
    renderer: Renderer
    event_queue: asyncio.Queue
    logger: logging.LoggerAdapter
