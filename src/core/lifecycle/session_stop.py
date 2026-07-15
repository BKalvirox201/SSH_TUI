from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.session.session import SSHServerSession


async def session_stop(session: SSHServerSession) -> None:
    if session.writer._chan and not session.writer._chan.is_closing():
        session.writer.set_cursor_visibility(True)
        session.writer.set_alt_screen(False)

    assert session.session_main
    session.session_main.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await session.session_main

    if session.writer._chan and not session.writer._chan.is_closing():
        try:
            session.writer._chan.exit(0)
        except Exception:
            session.logger.debug("shutdown: channel exit failed (already closed)")

    session.session_manager.remove(session)
