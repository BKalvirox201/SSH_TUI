from dataclasses import dataclass

from rich.theme import Theme


@dataclass
class RenderContext:
    width: int
    height: int
    focused: bool
    theme: Theme

    def child(
        self,
        *,
        width: int | None = None,
        height: int | None = None,
        focused: bool = False,
    ) -> RenderContext:
        return RenderContext(
            width=width if width is not None else self.width,
            height=height if height is not None else self.height,
            focused=focused,
            theme=self.theme,
        )
