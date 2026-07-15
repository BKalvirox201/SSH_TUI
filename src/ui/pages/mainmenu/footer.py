from typing import override

from rich.text import Text

from renderer.render_context import RenderContext
from ui.widgets.widget import Widget


class Footer(Widget):
    def __init__(self, left: str, right: str, style: str = "bold"):
        super().__init__()
        self.left = left
        self.right = right
        self.style = style

    @override
    def render(self, ctx: RenderContext) -> Text:
        text = Text()
        available = max(0, ctx.width - len(self.left) - len(self.right))

        if available == 0:
            half = ctx.width // 2
            left = self.left[:half]
            right = self.right[: ctx.width - len(left)]
        else:
            left = self.left
            right = self.right

        text.append(left, style=self.style)
        text.append(" " * max(1, ctx.width - len(left) - len(right)))
        text.append(right, style=self.style)

        return text
