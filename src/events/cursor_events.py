from dataclasses import dataclass

from events.page_events import PageEvent
from ui.widgets.widget import NavDirection


@dataclass
class CursorEvent(PageEvent):
    pass


@dataclass
class NavEvent(CursorEvent):
    """Navigation Events are unique to the cursor on each page"""

    direction: NavDirection


@dataclass
class ClickedEvent(CursorEvent):
    pass
