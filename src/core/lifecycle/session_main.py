from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from core.lifecycle.session_stop import session_stop
from events import CursorEvent, PageEvent, RenderEvent, SessionClose

if TYPE_CHECKING:
    from core.session.session import SSHServerSession


async def session_main(session: SSHServerSession):
    try:
        while True:
            event = await session.state.event_queue.get()
            if isinstance(event, SessionClose):
                session.logger.info(
                    f"Exiting with code: {SessionClose.exit_code}, with message: {SessionClose.exit_message}"
                )
                await session_stop(session)
                break

            if isinstance(event, RenderEvent):
                session.state.renderer.resize_pagewidth(event.width)
                session.state.renderer.resize_pageheight(event.height)
                ctx = session.state.renderer.create_render_context()
                current_page = session.state.pages[session.state.current_page]
                layout = current_page.render(ctx)
                session.state.renderer.render_page(layout)

            elif isinstance(event, PageEvent):
                current_page = session.state.pages[session.state.current_page]
                current_page.handle_event(
                    event, session.state.pages[session.state.current_page]
                )
                session.state.event_queue.put_nowait(
                    RenderEvent(session.width, session.height)
                )

            elif isinstance(event, CursorEvent):
                current_page = session.state.pages[session.state.current_page]
                if not hasattr(current_page, "cursor"):
                    current_page.cursor.


    # TODO: Do we still need this?
    except asyncio.CancelledError:
        pass
    except Exception as e:
        session.state.logger.exception(f"Event loop exception: {e}")
