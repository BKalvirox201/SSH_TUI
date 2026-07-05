from typing import TYPE_CHECKING

from src.core.logging import server_logger
from src.events.exit_events import SessionCloseEvent

if TYPE_CHECKING:
    from src.core.session.session import SSHServerSession

import asyncio


class SSHSessionManager:
    """Tracks all active SSH sessions safely."""

    def __init__(self):
        self.sessions: set[SSHServerSession] = set()

    def add(self, session: SSHServerSession):
        self.sessions.add(session)
        server_logger.info(f"Active sessions: {len(self.sessions)}")

    def remove(self, session: SSHServerSession):
        self.sessions.discard(session)
        server_logger.info(f"Active sessions: {len(self.sessions)}")

    async def close_all_sessions(self, timeout: float = 5.0):
        """Signal all sessions to close, wait up to `timeout` seconds."""
        # Broadcast event
        for session in self.sessions:
            session.state.event_queue.put_nowait(SessionCloseEvent())

        try:
            await asyncio.wait_for(self._wait_sessions_empty(), timeout=timeout)
        except TimeoutError:
            print(f"Timeout reached: {len(self.sessions)} session(s) still open")

    async def _wait_sessions_empty(self):
        """Poll until sessions set is empty without blocking the loop."""
        while self.sessions:
            await asyncio.sleep(0.1)
