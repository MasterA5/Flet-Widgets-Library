from typing import Union, List
from flet import (
    TextOverflow,
    FontWeight,
    Container,
    Control,
    Colors,
    Text
)
import asyncio


class TypeWriter(Container):
    """
    A typewriter-style text animation widget for Flet.

    This widget types out one or multiple texts character by character,
    with optional pause and looping.

    Features:
        - Animate text letter by letter.
        - Support for single or multiple texts.
        - Adjustable typing speed and pause duration.
        - Optional infinite looping.
        - Text customization: size, color, bold.
    """

    def __init__(
        self,
        texts: Union[str, List[str]],
        speed: int = 10,
        pause: float = 1.0,
        loop: bool = False,
        size: int = 24,
        color: Colors = Colors.WHITE,
        bold: bool = False
    ):
        """
        Initialize the TypeWriter widget.

        Args:
            texts (str | List[str]): Text or list of texts to animate.
            speed (int): Typing speed in characters per second (default=10).
            pause (float): Pause duration (in seconds) between texts (default=1.0).
            loop (bool): If True, the text animation loops indefinitely (default=False).
            size (int): Font size of the text (default=24).
            color (Colors): Text color (default=Colors.WHITE).
            bold (bool): Whether the text is bold (default=False).
        """
        super().__init__()
        self.texts: Union[str, List[str]] = texts if isinstance(texts, list) else [texts]
        self.speed: float = speed
        self.pause: float = pause
        self.value: str = ""
        self.content: Control = Text(
            value=self.value,
            size=size,
            overflow=TextOverflow.ELLIPSIS,
            color=color,
            weight=FontWeight.BOLD if bold else None
        )
        self.running: bool = False
        self.loop: bool = loop
        self.padding: int = 0
        self.margin: int = 0

    def did_mount(self):
        """
        Called when the widget is mounted to the page.
        Starts the typing animation loop.
        """
        self.running = True
        self.page.run_task(self._type_loop)

    def will_unmount(self):
        """
        Called when the widget is unmounted from the page.
        Stops the typing animation loop.
        """
        self.running = False

    async def _type_text(self, text: str):
        """
        Animate typing a single text string character by character.

        Args:
            text (str): The text to animate.
        """
        self.value = ""
        self.content.value = self.value
        self.update()

        for letter in text:
            self.value += letter
            self.content.value = self.value
            self.update()
            await asyncio.sleep(1 / self.speed)

    async def _type_loop(self):
        """
        Main typing loop.
        Iterates through all texts and animates them sequentially.
        """
        while self.running:
            for text in self.texts:
                await self._type_text(text)
                await asyncio.sleep(self.pause)
            if not self.loop:  # Exit if looping is disabled
                break
