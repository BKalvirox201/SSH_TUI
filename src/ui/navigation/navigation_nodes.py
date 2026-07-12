from enum import Enum
from typing import Any


class NavDirection(Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    Parent = 4
    Children = 5


class NavNode:
    def __init__(self, owner: Any) -> None:
        # NOTE: Nodes link to themselves if they don't link to other nodes
        self.parent: NavNode = self
        self.north: NavNode = self
        self.east: NavNode = self
        self.south: NavNode = self
        self.west: NavNode = self
        self.children: list[NavNode] = []

        # NOTE: The type for this is Any because I don't know how this is going to be used yet
        self.owner: Any = owner

    def connect(self, target: NavNode, link_direction: NavDirection) -> None:
        assert target != self  # NOTE: # cannot manually connect a node to itself
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
        assert target != self  # NOTE: # cannot manually disconnect a node from itself
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
