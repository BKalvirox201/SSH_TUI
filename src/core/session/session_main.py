from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from events import CursorEvent, PageEvent, RenderEvent, SessionClose

if TYPE_CHECKING:
    from core.session.session import SSHServerSession


async def session_main(session: SSHServerSession):
    try:
        while True:
            event = await session.event_queue.get()
            if isinstance(event, SessionClose):
                session.logger.info(
                    f"Exiting with code: {SessionClose.exit_code}, with message: {SessionClose.exit_message}"
                )
                await session.__deinitialise_session()
                break

            if isinstance(event, RenderEvent):
                session.renderer.resize_pagewidth(event.width)
                session.renderer.resize_pageheight(event.height)
                ctx = session.renderer.create_render_context()
                current_page = session.pages[session.current_page]
                layout = current_page.render(ctx)
                session.renderer.render_page(layout)

            elif isinstance(event, PageEvent):
                current_page = session.pages[session.current_page]
                current_page.handle_event(event, session.pages[session.current_page])
                session.event_queue.put_nowait(
                    RenderEvent(session.width, session.height)
                )

            elif isinstance(event, CursorEvent):
                current_page = session.pages[session.current_page]
                if not hasattr(current_page, "cursor"):
                    continue
                current_page.cursor.handle_event(CursorEvent)
                session.event_queue.put_nowait(
                    RenderEvent(session.width, session.height)
                )

    except asyncio.CancelledError:
        pass
