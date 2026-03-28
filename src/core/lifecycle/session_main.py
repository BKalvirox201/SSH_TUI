from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from src.core.lifecycle.session_stop import session_stop
from src.events.global_event_handler import GlobalEventHandler
from src.events.global_events import GlobalEvent, QuitEvent
from src.events.page_events import PageEvent

if TYPE_CHECKING:
    from src.core.session import SSHServerSession


async def session_main(session: SSHServerSession):
    try:
        while True:
            event = await session.state.event_queue.get()
            if isinstance(event, QuitEvent):
                a = asyncio.create_task(session_stop(session))
                _ = a
            elif isinstance(event, GlobalEvent):
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
