from enum import Enum

class NavDirectionEnum(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    

class PageEvent:
    pass


class NavEvent(PageEvent):
    def __init__(self, direction: NavDirectionEnum):
        self.direction = direction


class ActionEvent(PageEvent):
    def __init__(self, action):
        self.action = action
