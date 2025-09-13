import asyncio
from typing import Union, List
from flet import (
    Container,
    Row,
    Text,
    Colors,
    Animation,
    FontWeight,
    Control,
    alignment,
    TextOverflow
)


class SplitText(Container):
    """
    A split-text animation widget for Flet.

    This widget splits text into characters and animates them
    with offset-based transitions.

    Features:
        - Animate letters entering with Offset().
        - Support for single or multiple texts.
        - Adjustable speed and pause duration.
        - Optional infinite looping.
        - Text customization: size, color, bold.
    """

    def __init__(
        self,
        texts: Union[str, List[str]],
        speed: float = 0.05,
        pause: float = 1.0,
        loop: bool = False,
        size: int = 24,
        color: Colors = Colors.WHITE,
        bold: bool = False,
        direction: str = "bottom"  # "bottom", "top", "left", "right"
    ):
        super().__init__()
        self.texts: List[str] = texts if isinstance(texts, list) else [texts]
        self.speed: float = speed / 0.1 if speed != 0.1 else speed
        self.pause: float = pause
        self.loop: bool = loop
        self.running: bool = False
        self.direction: str = direction

        self.size: int = size
        self.color: Colors = color
        self.bold: bool = bold

        self.row = Row(alignment="center", spacing=2)
        self.content: Control = self.row
        self.alignment = alignment.center

    def did_mount(self):
        self.running = True
        self.page.run_task(self._animate_loop)

    def will_unmount(self):
        self.running = False

    def _get_offset(self):
        """
        Return initial offset depending on direction.
        """
        if self.direction == "bottom":
            return (0, 1)
        elif self.direction == "top":
            return (0, -1)
        elif self.direction == "left":
            return (-1, 0)
        elif self.direction == "right":
            return (1, 0)
        return (0, 1)

    async def _animate_text(self, text: str):
        """
        Animate a text by revealing each character with offset.
        """
        self.row.controls.clear()
        self.update()

        offset = self._get_offset()

        letters = [
            Text(
                value=ch,
                size=self.size,
                color=self.color,
                weight=FontWeight.BOLD if self.bold else None,
                offset=offset,
                animate_offset=Animation(400, "easeOut"),
                opacity=0,
                animate_opacity=Animation(400, "easeOut"),
                overflow=TextOverflow.ELLIPSIS
            )
            for ch in text
        ]

        self.row.controls.extend(letters)
        self.update()

        # Animate letters one by one
        for letter in letters:
            letter.offset = (0, 0)
            letter.opacity = 1
            self.update()
            await asyncio.sleep(self.speed)

    async def _animate_loop(self):
        """
        Main loop to animate all texts.
        """
        while self.running:
            for text in self.texts:
                await self._animate_text(text)
                await asyncio.sleep(self.pause)
            if not self.loop:
                break