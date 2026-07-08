from typing import TYPE_CHECKING

from navigation_nodes import NavDirection, NavNode

if TYPE_CHECKING:
    from widget import Widget


class Cursor:
    def __init__(self, start: Widget) -> None:
        self.focused: Widget = start

        # This is a bit silly being here, since there is only ever 1 cursor made by the user
        # The history for which child to travel down can live on the node instead.
        # This implementation is only required if you want multiple cursors
        # (atleast you don't have to manually manage the memory for this yourself)
        self.last_selected_child_history: dict[NavNode, NavNode] = {}

    def walk(self, direction: NavDirection) -> None:
        node: NavNode
        match direction:
            case NavDirection.North:
                node = self.focused.node.north
            case NavDirection.East:
                node = self.focused.node.east
            case NavDirection.South:
                node = self.focused.node.south
            case NavDirection.West:
                node = self.focused.node.west
            case NavDirection.Parent:
                if self.focused.node.parent.owner is not self.focused:
                    self.last_selected_child_history[self.focused.node.parent] = (
                        self.focused.node
                    )
                node = self.focused.node.parent
            case NavDirection.Children:
                if self.focused.node in self.last_selected_child_history:
                    node = self.last_selected_child_history[self.focused.node]
                elif len(self.focused.node.children) > 0:
                    node = self.focused.node.children[0]
                else:
                    node = self.focused.node

        if self.focused is not node.owner:
            self.focused.on_deselect()
            self.focused = node.owner
            self.focused.on_select()
