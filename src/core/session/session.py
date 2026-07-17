from __future__ import annotations

import asyncio
import contextlib
import logging
from typing import cast
import uuid

import asyncssh
from rich.theme import Theme
from session_main import session_main
from session_manager import SSHSessionManager

from core.io.writer import SSHChannelWriter
from core.server_logging import session_logger
from events import (
    NavEvent,
    RenderEvent,
    SessionClose,
)
from renderer.renderer import Renderer
from ui.pages.mainmenu import MainMenu
from ui.pages.page import Page
from ui.widgets.widget import NavDirection


# TODO: Session Start and Stop should be private functions of this class and stored in this file
class SSHServerSession(asyncssh.SSHServerSession):
    def __init__(self, session_manager: SSHSessionManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_id = str(uuid.uuid4())
        self.session_manager = session_manager
        self.writer: SSHChannelWriter
        self.session_main: asyncio.Task
        self.event_queue: asyncio.Queue
        self.width: int = 0
        self.height: int = 0
        self.pages: dict[str, Page]
        self.current_page: Page
        self.renderer: Renderer
        self.logger: logging.LoggerAdapter

    def connection_made(self, chan: asyncssh.SSHServerChannel):
        channel = cast(asyncssh.SSHLineEditorChannel, chan)
        self.writer = SSHChannelWriter(channel)
        self.logger = logging.LoggerAdapter(
            session_logger,
            {"session_id": self.session_id},
        )

    def connection_lost(self, exc):
        """
        Called when the SSH channel is closed or lost.
        exc will be None if the connection was closed cleanly,
        or an exception if it was aborted.
        """
        assert self.session_main
        if exc:
            self.logger.warning(f"Connection lost: {exc}")
        else:
            self.logger.info("Connection closed cleanly")

        if not self.session_main.done():
            # TODO: Work out how to mute RUFF warnings
            # Actually understand how asyncio and the async keyword work
            asyncio.create_task(self.__deinitialise_session())

    def pty_requested(self, term_type, term_size, term_modes):
        _, _ = term_type, term_modes
        self.width, self.height, _, _ = term_size
        return True

    def shell_requested(self) -> bool:
        return True

    def session_started(self):
        self.__initialise_session()
        self.event_queue.put_nowait(RenderEvent(self.width, self.height))
        self.session_manager.add(self)
        self.session_main = asyncio.create_task(session_main(self))

    def data_received(self, data: str, datatype):
        _ = datatype
        self.logger.debug(f"[SSH] Data received: {data!r}")

        # TODO: Move to input handler

        data = data.lower()
        if data and data.strip() in ("q", "\x03"):
            self.event_queue.put_nowait(
                SessionClose(exit_code=0, exit_message="Session closed by user")
            )

        # TODO: Do inputs need to be separate events?
        if data and data.strip() in ("w", "k"):
            self.event_queue.put_nowait(NavEvent(NavDirection.North))
        if data and data.strip() in ("a", "h"):
            self.event_queue.put_nowait(NavEvent(NavDirection.East))
        if data and data.strip() in ("s", "j"):
            self.event_queue.put_nowait(NavEvent(NavDirection.South))
        if data and data.strip() in ("d", "l"):
            self.event_queue.put_nowait(NavEvent(NavDirection.West))

        # enter = select
        # TODO: we need to worry about typing in long form inputs..

    def terminal_size_changed(self, width, height, pixwidth, pixheight):
        """Handle terminal resize by updating the renderer and notifying the current page."""
        _, _ = pixwidth, pixheight
        self.width = width
        self.height = height
        self.event_queue.put_nowait(RenderEvent(self.width, self.height))

    def __initialise_session(self):
        # Terminal setup
        self.writer.clear_input()
        self.writer.set_line_mode(False)
        self.writer.set_echo(False)
        self.writer.set_alt_screen(True)
        self.writer.set_window_title("Nigel's Amazing TUI")
        self.writer.set_cursor_visibility(False)

        # Event Queue
        self.event_queue: asyncio.Queue = asyncio.Queue()

        # Pages
        self.pages: dict[str, Page] = {
            "MainMenu": MainMenu(),
        }
        self.current_page = next(iter(self.pages))

        # Renderer and theme
        self.renderer = Renderer(self.writer)
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
        self.renderer.set_theme(client_theme)

    async def __deinitialise_session(self) -> None:
        if self.writer.channel and not self.writer.channel.is_closing():
            self.writer.set_cursor_visibility(True)
            self.writer.set_alt_screen(False)

        assert self.self_main
        self.self_main.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self.self_main

        if self.writer.channel and not self.writer.channel.is_closing():
            try:
                self.writer.channel.exit(0)
            except Exception:
                self.logger.debug("shutdown: channel exit failed (already closed)")

        self.self_manager.remove(self)
