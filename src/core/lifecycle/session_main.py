from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from src.core.lifecycle.session_stop import session_stop
from src.events.exit_events import QuitEvent, SessionCloseEvent
from src.events.global_event_handler import GlobalEventHandler
from src.events.global_events import GlobalEvent
from src.events.page_events import PageEvent

if TYPE_CHECKING:
    from src.core.session.session import SSHServerSession


async def session_main(session: SSHServerSession):
    try:
        while True:
            event = await session.state.event_queue.get()
            if isinstance(event, SessionCloseEvent):
                if isinstance(event, QuitEvent):
                    session.logger.info("Session Closed By User")
                await session_stop(session)
                break

            if isinstance(event, GlobalEvent):
                GlobalEventHandler.handle_event(event, session.state)
            elif isinstance(event, PageEvent):
                current_page = session.state.pages[session.state.current_page]
                current_page.handle_event(
                    event, session.state.page_data[session.state.current_page]
                )

    except asyncio.CancelledError:
        pass
    except Exception as e:
        session.state.logger.exception(f"Event loop exception: {e}")
