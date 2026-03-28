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
from src.events.global_events import (
    QuitEvent,
    RenderEvent,
    ResizeEvent,
)


class SSHServerSession(asyncssh.SSHServerSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_id = str(uuid.uuid4())

    def connection_made(self, chan: asyncssh.SSHServerChannel):
        self._chan = cast(asyncssh.SSHLineEditorChannel, chan)
        self.writer = SSHChannelWriter(self._chan)
        self.logger = logging.LoggerAdapter(
            session_logger,
            {"session_id": self.session_id},
        )

    def connection_lost(self, exc):
        _ = exc
        asyncio.create_task(session_stop(self))

    def pty_requested(self, term_type, term_size, term_modes):
        _, _ = term_type, term_modes
        self._width, self._height, _, _ = term_size
        return True

    def shell_requested(self) -> bool:
        return True

    def session_started(self):
        self.state = session_start(self)
        self.state.event_queue.put_nowait(RenderEvent(self._width, self._height))
        self.session_main = asyncio.create_task(session_main(self))

    def data_received(self, data: str, datatype):
        _ = datatype
        self.logger.debug(f"[SSH] Data received: {data!r}")
        if data and data.strip() in ("q", "\x03"):
            self.state.event_queue.put_nowait(QuitEvent())

        # Add input handler

    def terminal_size_changed(self, width, height, pixwidth, pixheight):
        """Handle terminal resize by updating the renderer and notifying the current page."""
        _, _ = pixwidth, pixheight
        self._width = width
        self._height = height
        self.state.event_queue.put_nowait(ResizeEvent(width=width, height=height))
