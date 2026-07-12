from rich.text import Text


class Footer:
    def __init__(self, left: str, right: str, style: str = "bold"):
        self.left = left
        self.right = right
        self.style = style

    def render(self, width: int) -> Text:
        text = Text()
        available = max(0, width - len(self.left) - len(self.right))

        if available == 0:
            half = width // 2
            left = self.left[:half]
            right = self.right[: width - len(left)]
        else:
            left = self.left
            right = self.right

        text.append(left, style=self.style)
        text.append(" " * max(1, width - len(left) - len(right)))
        text.append(right, style=self.style)

        return text
