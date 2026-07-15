from dataclasses import dataclass

from ui.widgets.widget import NavDirection


# TODO: based on https://docs.python.org/3/library/stdtypes.html#types-union
# Rewrite to be like : https://stackoverflow.com/questions/68183495/union-vs-inheritance-in-python-implementation
class PageEvent:
    pass


@dataclass
class NavEvent(PageEvent):
    """Navigation Events are unique to the cursor on each page"""

    direction: NavDirection
