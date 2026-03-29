class InputEvent:
    """Wraps raw input data as an event."""

    def __init__(self, data: str):
        self.data = data
