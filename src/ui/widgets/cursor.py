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
        # Not even sure I want this feature
        self.last_selected_child_history: dict[Widget, Widget] = {}

    def walk(self, direction: NavDirection) -> None:
        next_widget: Widget
        match direction:
            case NavDirection.North:
                next_widget = self.focused.north
            case NavDirection.East:
                next_widget = self.focused.east
            case NavDirection.South:
                next_widget = self.focused.south
            case NavDirection.West:
                next_widget = self.focused.west
            case NavDirection.Parent:
                if self.focused.parent is not self.focused:
                    self.last_selected_child_history[self.focused.parent] = self.focused
                next_widget = self.focused.parent
            case NavDirection.Children:
                if self.focused in self.last_selected_child_history:
                    next_widget = self.last_selected_child_history[self.focused]
                elif len(self.focused.children) > 0:
                    next_widget = self.focused.children[0]
                else:
                    next_widget = self.focused

        if self.focused is not next_widget:
            self.focused = next_widget
