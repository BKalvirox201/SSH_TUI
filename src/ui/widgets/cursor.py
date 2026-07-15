from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widget import NavDirection, Widget


class Cursor:
    def __init__(self, start: Widget) -> None:
        # Make this optional and assign later?
        self.focused: Widget = start
        # NOTE:
        # This is a bit silly being here, since there is only ever 1 cursor made by the user
        # The history for which child to travel down can live on the node instead.
        # This implementation is only required if you want multiple cursors
        # (atleast you don't have to manually manage the memory for this yourself)
        self.last_selected_child_history: dict[Widget, Widget] = {}

    def walk(self, direction: NavDirection) -> None:
        next: Widget
        match direction:
            case NavDirection.North:
                next = self.focused.north
            case NavDirection.East:
                next = self.focused.east
            case NavDirection.South:
                next = self.focused.south
            case NavDirection.West:
                next = self.focused.west
            case NavDirection.Parent:
                if self.focused.next.parent.owner is not self.focused:
                    self.last_selected_child_history[self.focused.next.parent] = (
                        self.focused.next
                    )
                next = self.focused.parent
            case NavDirection.Children:
                if self.focused.next in self.last_selected_child_history:
                    next = self.last_selected_child_history[self.focused]
                elif len(self.focused.next.children) > 0:
                    next = self.focused.children[0]
                else:
                    next = self.focused

        if self.focused is not next:
            self.focused.deselect()
            self.focused = next
            self.focused.select()
