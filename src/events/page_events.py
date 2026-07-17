from dataclasses import dataclass

from src.events.session_events import SessionEvent


@dataclass
class PageEvent(SessionEvent):
    pass
