from collections.abc import Callable

from widget import Widget


class Button(Widget):
    def __init__(self, *args, callback: Callable, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def activate(self):
        self.callback()
