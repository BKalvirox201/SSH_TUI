from dataclasses import dataclass

from events.session_events import SessionEvent


@dataclass
class PageEvent(SessionEvent):
    pass
