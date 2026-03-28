from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.session import SSHServerSession

from src.core.logging import session_logger


async def session_stop(session: SSHServerSession):
    session.session_main.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await session.session_main

    try:
        session.writer.set_cursor_visibility(True)
        session.writer.set_alt_screen(False)
    except Exception as e:
        session_logger.exception(f"shutdown: failed to restore terminal: {e}")

    if hasattr(session, "_chan") and not session._chan.is_closing():
        session._chan.exit(0)
