class PageEvent:
    pass


class NavEvent(PageEvent):
    def __init__(self, direction):
        self.direction = direction


class ActionEvent(PageEvent):
    def __init__(self, action):
        self.action = action
