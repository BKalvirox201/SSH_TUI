from dataclasses import dataclass

from ui.widgets.widget import NavDirection


class PageEvent:
    pass


@dataclass
class NavEvent(PageEvent):
    """Navigation Events are unique to the cursor on each page"""

    direction: NavDirection


@dataclass
class ClickEvent(PageEvent):
    pass
