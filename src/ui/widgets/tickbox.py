from widget import Widget


class TickBox(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Add a callback here to be called when it's state changes
        self.is_ticked = False

    def activate(self):
        self.ticked = not self.ticked
