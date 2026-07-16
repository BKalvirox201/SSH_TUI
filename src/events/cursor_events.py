from dataclasses import dataclass

from ui.widgets.widget import NavDirection


@dataclass
class CursorEvent:
    pass


@dataclass
class NavEvent(CursorEvent):
    """Navigation Events are unique to the cursor on each page"""

    direction: NavDirection


@dataclass
class ClickEvent(CursorEvent):
    pass
