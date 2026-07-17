import asyncio
from typing import TYPE_CHECKING

from src.core.server_logging import server_logger
from src.events import SessionClose

if TYPE_CHECKING:
    from src.core.session.session import SSHServerSession


class SSHSessionManager:
    """Tracks all active SSH sessions safely."""

    def __init__(self):
        self.sessions: list[SSHServerSession] = []

    def add(self, session: SSHServerSession):
        self.sessions.append(session)
        server_logger.info(
            f"""Session {session.session_id} created, Active sessions: {len(self.sessions)}"""
        )

    def remove(self, session: SSHServerSession):
        self.sessions.remove(session)
        server_logger.info(
            f"""Session {session.session_id} closed, Active sessions: {len(self.sessions)}"""
        )

    async def close_all_sessions(self, timeout: float = 5.0):
        """Signal all sessions to close, wait up to `timeout` seconds."""
        # TODO: Create a stand-alone broadcast function and then have this one as well which calls it
        for session in self.sessions:
            session.event_queue.put_nowait(
                SessionClose(exit_code=0, exit_message="Session closed by server")
            )

        try:
            await asyncio.wait_for(self.__wait_sessions_empty(), timeout=timeout)
        except TimeoutError:
            print(f"Timeout reached: {len(self.sessions)} session(s) still open")

    async def __wait_sessions_empty(self):
        """Poll until sessions set is empty without blocking the loop."""
        while self.sessions:
            await asyncio.sleep(0.1)
