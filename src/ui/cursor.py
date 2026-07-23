from __future__ import annotations

from src.ui.pages.page import Page
from src.ui.widgets.widget import NavDirection, Widget


class Cursor:
    def __init__(self, start_page: Page) -> None:
        self.focused_page = start_page

    @property
    def focused_widget(self) -> Widget:
        return self.focused_page.focused_widget

    def change_page(self, page: Page) -> None:
        self.focused_page = page

    def walk(self, direction: NavDirection) -> None:
        current = self.focused_widget

        match direction:
            case NavDirection.North:
                next_widget = current.north

            case NavDirection.East:
                next_widget = current.east

            case NavDirection.South:
                next_widget = current.south

            case NavDirection.West:
                next_widget = current.west

            case NavDirection.Parent:
                if current.parent is not current:
                    current.parent.last_focused_child = current
                next_widget = current.parent

            case NavDirection.Children:
                if current.last_focused_child is not None:
                    next_widget = current.last_focused_child
                elif current.children:
                    next_widget = current.children[0]
                else:
                    next_widget = current

        if next_widget is not current:
            self.focused_page.focused_widget = next_widget
