from src.core.session_state import SessionState
from src.events.global_events import (
    ChangeCurrentPageEvent,
    GlobalEvent,
    RenderEvent,
    ResizeEvent,
)


class GlobalEventHandler:
    @staticmethod
    def handle_event(event: GlobalEvent, session_state: SessionState):
        if isinstance(event, ResizeEvent):
            session_state.event_queue.put_nowait(RenderEvent(event.width, event.height))

        elif isinstance(event, RenderEvent):
            if event.width:
                session_state.renderer.resize_page_width(event.width)
            if event.height:
                session_state.renderer.resize_page_height(event.height)
            ctx = session_state.renderer.create_render_context()

            current_page = session_state.pages[session_state.current_page]
            layout = current_page.render(ctx)
            session_state.renderer.render_page(layout)

        elif isinstance(event, ChangeCurrentPageEvent):
            assert event.new_page_name in session_state.page_data
            session_state.current_page = event.new_page_name
            session_state.event_queue.put_nowait(RenderEvent(None, None))
