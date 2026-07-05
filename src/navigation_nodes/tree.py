from enum import Enum


class NodeLinkDirection(Enum):
    North = 1
    East = 2
    South = 3
    West = 4


class TreeNode:
    def __init__(self) -> None:
        self.parent_container: NodeContainer | None = None
        self.north: TreeNode | None = None
        self.east: TreeNode | None = None
        self.south: TreeNode | None = None
        self.west: TreeNode | None = None

    def connect(
        self,
        target: TreeNode,
        link_direction: NodeLinkDirection | None,
    ) -> None:
        if self == target:
            raise ValueError("Can't Link a Node to itself")

        if link_direction:
            match link_direction:
                case NodeLinkDirection.North:
                    self.north = target
                case NodeLinkDirection.East:
                    self.east = target
                case NodeLinkDirection.South:
                    self.south = target
                case NodeLinkDirection.West:
                    self.west = target

    def disconnect(self, target: TreeNode) -> None:
        if self.north is target:
            self.north = None
        elif self.east is target:
            self.east = None
        elif self.south is target:
            self.south = None
        elif self.west is target:
            self.west = None

    def exit_parent_container(self) -> NodeContainer | None:
        if self.parent_container:
            self.parent_container.last_selected_child = self
        return self.parent_container

    def walk(self, direction: NodeLinkDirection) -> TreeNode:
        match direction:
            case NodeLinkDirection.North:
                return self.north or self
            case NodeLinkDirection.East:
                return self.east or self
            case NodeLinkDirection.South:
                return self.south or self
            case NodeLinkDirection.West:
                return self.west or self


class NodeContainer(TreeNode):
    def __init__(self) -> None:
        super().__init__()
        self.last_selected_child: TreeNode | None = None
        self.children: list[TreeNode] = []

    def add(self, node: TreeNode):
        node.parent = self
        self.children.append(node)

    def remove(self, node: TreeNode):
        node.parent = None
        self.children.remove(node)

    def enter(self) -> TreeNode:
        return self.last_selected_child or self.children[0]


# TestWidget
class Widget(TreeNode):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def print_descending(self) -> None:
        padding = "  "
        pairs: set[tuple[Widget, Widget]] = set()
        depth = 0

        def __print_descending(
            pairs: set[tuple[Widget, Widget]], depth: int, new_root: Widget
        ):
            print(depth * padding + new_root.value)
            depth += 1

            if new_root.north and (new_root, new_root.north) not in pairs:
                pairs.add((new_root, new_root.north))
                if (new_root.north, new_root) in pairs:
                    print(depth * padding + new_root.north.value)
                    return pairs
                pairs = __print_descending(pairs, depth, new_root.north)
            if new_root.east and (new_root, new_root.east) not in pairs:
                pairs.add((new_root, new_root.east))
                if (new_root.east, new_root) in pairs:
                    print(depth * padding + new_root.east.value)
                    return pairs
                pairs = __print_descending(pairs, depth, new_root.east)
            if new_root.south and (new_root, new_root.south) not in pairs:
                pairs.add((new_root, new_root.south))
                if (new_root.south, new_root) in pairs:
                    print(depth * padding + new_root.south.value)
                    return pairs
                pairs = __print_descending(pairs, depth, new_root.south)
            if new_root.west and (new_root, new_root.west) not in pairs:
                pairs.add((new_root, new_root.west))
                if (new_root.west, new_root) in pairs:
                    print(depth * padding + new_root.west.value)
                    return pairs
                pairs = __print_descending(pairs, depth, new_root.west)

            return pairs

        _ = __print_descending(pairs, depth, self)


if __name__ == "__main__":
    a = Widget("a")
    b = Widget("b")
    c = Widget("c")
    d = Widget("d")
    e = Widget("e")
    f = Widget("f")

    a.connect(b, NodeLinkDirection.South)
    b.connect(c, NodeLinkDirection.South)
    c.connect(d, NodeLinkDirection.East)
    d.connect(c, NodeLinkDirection.West)
    c.connect(e, NodeLinkDirection.South)
    b.connect(f, NodeLinkDirection.West)
    f.connect(b, NodeLinkDirection.East)
    a.print_descending()

    print("Walking the tree\n")

    current_node = a
    current_node = current_node.walk(NodeLinkDirection.South)
    current_node = current_node.walk(NodeLinkDirection.South)
    current_node = current_node.walk(NodeLinkDirection.East)
    current_node = current_node.walk(NodeLinkDirection.West)
    print(current_node.value)
