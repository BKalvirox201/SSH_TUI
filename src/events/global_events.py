from rich.theme import Theme


class GlobalEvent:
    pass


class ChangeCurrentPageEvent(GlobalEvent):
    def __init__(self, new_page_name: str) -> None:
        self.new_page_name = new_page_name


class TickEvent(GlobalEvent):
    pass


class UpdateThemeEvent(GlobalEvent):
    def __init__(self, theme: Theme):
        self.theme = theme


class RenderEvent(GlobalEvent):
    def __init__(self, width: int | None, height: int | None):
        self.width = width
        self.height = height


class ResizeEvent(GlobalEvent):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
