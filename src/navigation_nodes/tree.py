from enum import Enum


class NavDirection(Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    Parent = 4
    Children = 5


class NavNode:
    def __init__(self, owner: Widget) -> None:
        # Nodes link to themselves if they don't link to other nodes
        self.parent: NavNode = self
        self.north: NavNode = self
        self.east: NavNode = self
        self.south: NavNode = self
        self.west: NavNode = self
        self.children: list[
            NavNode
        ] = []  # every node is also a container, layout nesting has to be done at another level

        self.owner: Widget = owner

    def connect(
        self,
        target: NavNode,
        link_direction: NavDirection,
    ) -> None:
        assert target != self  # cannot manually connect a node to itself
        match link_direction:
            case NavDirection.North:
                self.north = target
            case NavDirection.East:
                self.east = target
            case NavDirection.South:
                self.south = target
            case NavDirection.West:
                self.west = target
            case NavDirection.Parent:
                self.parent = target
                target.children.append(self)
            case NavDirection.Children:
                target.parent = self
                self.children.append(target)

    def disconnect(self, target: NavNode) -> None:
        assert target != self  # cannot manually disconnect a node from itself
        if self.north is target:
            self.north = self
        elif self.east is target:
            self.east = self
        elif self.south is target:
            self.south = self
        elif self.west is target:
            self.west = self
        elif self.parent is target:
            self.parent = self
            target.children.remove(self)
        elif target in self.children:
            target.parent = self
            self.children.remove(target)


class Widget:
    def __init__(self, value) -> None:
        super().__init__()
        self.node = NavNode(self)
        self.value = value

    def connect(
        self,
        target: Widget,
        link_direction: NavDirection,
    ) -> None:
        """Convenience Function for connecting widgets"""
        self.node.connect(target.node, link_direction)

    def disconnect(
        self,
        target: Widget,
    ) -> None:
        """Convenience Function for disconnecting widgets"""
        self.node.disconnect(target.node)

    def __str__(self) -> str:
        # How do printing multiline strings work?
        return f"""
        Widget: {self.value}
            Parent: {self.node.parent.owner.value if self.node.parent else None}
            North: {self.node.north.owner.value if self.node.north else None}
            East: {self.node.east.owner.value if self.node.east else None}
            South: {self.node.south.owner.value if self.node.south else None}
            West: {self.node.west.owner.value if self.node.west else None}
            Children: {[child.owner.value for child in self.node.children]}
        """

    def __repr__(self) -> str:
        return str(self.value)


class Cursor:
    def __init__(self, start: Widget) -> None:
        self.focused: Widget = start
        # self.history: list[]  # Could be cool, make it using a ring buffer

        # This is a bit silly being here, since there is only ever 1 cursor made by the user
        # The history for which child to travel down can live on the node instead.
        # This implementation is only required if you want multiple cursors
        # (atleast you don't have to manually manage the memory for this yourself)
        self.last_selected_child_history: dict[NavNode, NavNode] = {}

    def walk(self, direction: NavDirection) -> None:
        """
        If walking from a node in a direction with no connection
        it will return itself as in "stay here" instead of throwing an error.
        """
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
        self.focused = node.owner

    def print_selected(self) -> None:
        print(self.focused)

    def print_descending(self) -> None:
        widgets: set[Widget] = set()

        def __collect(starting_widget: Widget):
            widgets.add(starting_widget)
            cursor = Cursor(starting_widget)

            # Hopefully, there is a world where this doesn't consume RAM
            fnode = cursor.focused.node

            if fnode.parent and fnode.parent.owner not in widgets:
                widgets.add(fnode.parent.owner)
            if fnode.north and fnode.north.owner not in widgets:
                widgets.add(fnode.north.owner)
                __collect(fnode.north.owner)
            if fnode.east and fnode.east.owner not in widgets:
                widgets.add(fnode.east.owner)
                __collect(fnode.east.owner)
            if fnode.south and fnode.south.owner not in widgets:
                widgets.add(fnode.south.owner)
                __collect(fnode.south.owner)
            if fnode.west and fnode.west.owner not in widgets:
                widgets.add(fnode.west.owner)
                __collect(fnode.west.owner)
            for child in fnode.children:
                if child not in widgets:
                    widgets.add(child.owner)
                    __collect(child.owner)

        __collect(self.focused)

        for widget in sorted(widgets, key=lambda w: w.value):
            print(widget)


if __name__ == "__main__":
    a = Widget("a")
    b = Widget("b")
    c = Widget("c")
    d = Widget("d")
    e = Widget("e")
    f = Widget("f")
    g = Widget("g")
    h = Widget("h")

    a.connect(b, NavDirection.South)
    b.connect(c, NavDirection.South)
    c.connect(d, NavDirection.East)
    d.connect(c, NavDirection.West)
    c.connect(e, NavDirection.West)
    e.connect(c, NavDirection.East)
    e.connect(f, NavDirection.Children)
    e.connect(g, NavDirection.Children)
    e.connect(h, NavDirection.Children)
    f.connect(g, NavDirection.West)
    g.connect(f, NavDirection.East)
    f.connect(h, NavDirection.North)
    g.connect(h, NavDirection.North)
    h.connect(f, NavDirection.South)

    cursor = Cursor(a)
    # cursor.print_descending()

    # walk a->e visiting all nodes, then into e, f->g->h->f, then exit e
    cursor.walk(NavDirection.South)
    cursor.walk(NavDirection.South)
    cursor.walk(NavDirection.East)
    cursor.walk(NavDirection.West)
    cursor.walk(NavDirection.West)
    assert cursor.focused.value == "e"

    # Shouldn't be able to go anywhere it's not linked to
    cursor.walk(NavDirection.North)
    cursor.walk(NavDirection.South)
    cursor.walk(NavDirection.West)
    cursor.walk(NavDirection.Parent)
    assert cursor.focused.value == "e"
    assert len(cursor.last_selected_child_history) == 0, print(
        cursor.last_selected_child_history
    )

    # Walk down to children
    cursor.walk(NavDirection.Children)
    assert cursor.focused.value == "f"

    # Walk around and then back up
    cursor.walk(NavDirection.West)
    cursor.walk(NavDirection.North)
    cursor.walk(NavDirection.Parent)
    assert cursor.focused.value == "e"

    # Walk down again and we should land on the one we came up on
    cursor.walk(NavDirection.Children)
    assert cursor.focused.value == "h"

    # Once more for luck
    cursor.walk(NavDirection.South)
    cursor.walk(NavDirection.Parent)
    cursor.walk(NavDirection.Children)
    assert cursor.focused.value == "f"
    cursor.print_descending()
