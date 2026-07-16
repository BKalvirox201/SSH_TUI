from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from rich.theme import Theme

from core.session.session_state import SessionState
from renderer.renderer import Renderer
from ui.pages.mainmenu.mainmenu import MainMenu
from ui.pages.page import Page

if TYPE_CHECKING:
    from core.session.session import SSHServerSession


def session_start(session: SSHServerSession) -> SessionState:
    """
    Factory function to create a fully initialized SessionState.
    """
    # Terminal setup
    session.writer.clear_input()
    session.writer.set_line_mode(False)
    session.writer.set_echo(False)
    session.writer.set_alt_screen(True)
    session.writer.set_window_title("Nigel's Amazing TUI")
    session.writer.set_cursor_visibility(False)

    # Pages
    pages: dict[str, Page] = {
        "MainMenu": MainMenu(),
        # Add more pages here as needed
    }

    # Renderer and theme
    renderer = Renderer(session.writer)
    client_theme = Theme(
        {
            "primary": "yellow",
            "secondary": "cyan",
            "error": "red",
            "highlight": "bright_red",
            "background": "black",
            "foreground": "white",
            "heading": "blue",
        }
    )
    renderer.set_theme(client_theme)

    # Event queue
    event_queue: asyncio.Queue = asyncio.Queue()

    # Initialize SessionState
    return SessionState(
        current_page=next(iter(pages)),
        pages=pages,
        renderer=renderer,
        event_queue=event_queue,
        logger=session.logger,
    )
