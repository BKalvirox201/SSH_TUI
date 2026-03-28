from rich.theme import Theme


class GlobalEvent:
    pass


class ResizeEvent(GlobalEvent):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class ChangeCurrentPageEvent(GlobalEvent):
    def __init__(self, new_page_name: str) -> None:
        self.new_page_name = new_page_name


class TickEvent(GlobalEvent):
    pass


class UpdateThemeEvent(GlobalEvent):
    def __init__(self, theme: Theme):
        self.theme = theme


class RenderEvent(GlobalEvent):
    pass


class InputEvent:
    """Wraps raw input data as an event."""

    def __init__(self, data: str):
        self.data = data


class QuitEvent:
    pass
