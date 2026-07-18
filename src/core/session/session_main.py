from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from src.events import ChangePage, PageEvent, RenderEvent, SessionClose

if TYPE_CHECKING:
    from src.core.session.session import SSHServerSession


async def session_main(session: SSHServerSession):
    try:
        session.logger.debug("Session Main Started")
        while True:
            event = await session.event_queue.get()
            if isinstance(event, SessionClose):
                session.logger.info(
                    f"Exiting with code: {event.exit_code}, with message: {event.exit_message}"
                )
                await session._deinitialise_session()
                # TODO: Does this break ever get called?
                break

            if isinstance(event, RenderEvent):
                # TODO: Make the rendering a separate function that can be repeatedly called
                # Maybe it should live on the renderer and we pass the session to it
                session.renderer.render_current_page()

            elif isinstance(event, PageEvent):
                session.current_page.handle_event(event)
                session.event_queue.put_nowait(RenderEvent())

            elif isinstance(event, ChangePage):
                if event.page_name not in session.pages:
                    # TODO: Throw Error
                    continue
                session.current_page = session.pages[event.page_name]
                session.event_queue.put_nowait(RenderEvent())

    except asyncio.CancelledError:
        pass
