import asyncio
import logging
from typing import cast
import uuid

import asyncssh

from src.core.io.writer import SSHChannelWriter
from src.core.lifecycle.session_main import session_main
from src.core.lifecycle.session_start import session_start
from src.core.lifecycle.session_stop import session_stop
from src.core.logging import session_logger
from src.core.session.session_manager import SSHSessionManager
from src.events.exit_events import QuitEvent
from src.events.global_events import (
    RenderEvent,
    ResizeEvent,
)
from src.events.page_events import NavDirectionEnum as NavEnum, NavEvent


class SSHServerSession(asyncssh.SSHServerSession):
    def __init__(self, session_manager: SSHSessionManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_id = str(uuid.uuid4())
        self.session_manager = session_manager
        self._chan = None
        self.session_main = None

    def connection_made(self, chan: asyncssh.SSHServerChannel):
        self._chan = cast(asyncssh.SSHLineEditorChannel, chan)
        self.writer = SSHChannelWriter(self._chan)
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

        # Schedule session cleanup
        if hasattr(self, "session_main") and not self.session_main.done():
            # TODO: Work out how to mute RUFF warnings
            asyncio.create_task(session_stop(self))

    def pty_requested(self, term_type, term_size, term_modes):
        _, _ = term_type, term_modes
        self.width, self.height, _, _ = term_size
        return True

    def shell_requested(self) -> bool:
        return True

    def session_started(self):
        self.state = session_start(self)
        self.state.event_queue.put_nowait(RenderEvent(self.width, self.height))
        self.session_manager.add(self)
        self.session_main = asyncio.create_task(session_main(self))

    def data_received(self, data: str, datatype):
        _ = datatype
        self.logger.debug(f"[SSH] Data received: {data!r}")

        # TODO: Move to input handler

        # We need to handle capslock here maybe
        if data and data.strip() in ("q", "\x03"):
            self.state.event_queue.put_nowait(QuitEvent())

        if data and data.strip() in ("w", "k"):
            self.state.event_queue.put_nowait(NavEvent(NavEnum.NORTH))
        if data and data.strip() in ("a", "h"):
            self.state.event_queue.put_nowait(NavEvent(NavEnum.EAST))
        if data and data.strip() in ("s", "j"):
            self.state.event_queue.put_nowait(NavEvent(NavEnum.SOUTH))
        if data and data.strip() in ("d", "l"):
            self.state.event_queue.put_nowait(NavEvent(NavEnum.WEST))

        # enter = select
        # maybe we need to worry about typing in long form inputs.. #TODO

    def terminal_size_changed(self, width, height, pixwidth, pixheight):
        """Handle terminal resize by updating the renderer and notifying the current page."""
        _, _ = pixwidth, pixheight
        self.width = width
        self.height = height
        self.state.event_queue.put_nowait(ResizeEvent(width=width, height=height))
