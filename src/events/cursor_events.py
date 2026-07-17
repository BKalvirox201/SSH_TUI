from dataclasses import dataclass

from src.events.page_events import PageEvent
from src.ui.widgets.widget import NavDirection


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
