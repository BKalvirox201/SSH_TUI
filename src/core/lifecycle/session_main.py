from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from src.core.lifecycle.session_stop import session_stop
from src.events.exit_events import QuitEvent, SessionCloseEvent
from src.events.global_events import RenderEvent, ResizeEvent, ChangeCurrentPageEvent
from src.events.page_events import NavEvent

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

            elif isinstance(event, ResizeEvent):
                session.state.event_queue.put_nowait(RenderEvent(event.width, event.height))

            elif isinstance(event, RenderEvent):
                if event.width:
                    session.state.renderer.resize_pagewidth(event.width)
                if event.height:
                    session.state.renderer.resize_pageheight(event.height)

                ctx = session.state.renderer.create_render_context()
                current_page = session.state.pages[session.state.current_page]
                layout = current_page.render(ctx)
                session.state.renderer.render_page(layout)

            elif isinstance(event, ChangeCurrentPageEvent):
                assert event.new_page_name in session.state.page_data
                session.state.current_page = event.new_page_name

            elif isinstance(event, NavEvent):
                current_page = session.state.pages[session.state.current_page]
                current_page.handle_event(
                    event, session.state.page_data[session.state.current_page]
                )

            session.state.event_queue.put_nowait(
                RenderEvent(session.width, session.height)
                )
                
                

    except asyncio.CancelledError:
        pass
    except Exception as e:
        session.state.logger.exception(f"Event loop exception: {e}")
