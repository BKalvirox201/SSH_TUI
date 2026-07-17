from dataclasses import dataclass


@dataclass
class RenderContext:
    width: int
    height: int
    focused: bool

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
        )
