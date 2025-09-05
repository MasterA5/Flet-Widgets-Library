from flet import (
    Container,
    Control,
    Colors,
    Text
)
import asyncio


class TextFader(Container):
    """
    A text fading widget for Flet.

    This widget gradually fades in and out a text element.
    Can optionally loop or remain permanently visible.

    Features:
        - Fade-in and fade-out animation.
        - Adjustable speed and pause duration.
        - Optional looping of the fade animation.
        - Permanent display option (skip fade-out).
    """

    def __init__(
        self,
        text: str,
        color: Colors = Colors.WHITE,
        size: int = 24,
        speed: float = 0.05,
        pause: float = 1.0,
        loop: bool = False,
        permanent: bool = False
    ):
        """
        Initialize the TextFader widget.

        Args:
            text (str): The text to display.
            color (Colors): Text color (default=WHITE).
            size (int): Font size of the text (default=24).
            speed (float): Animation speed for fade in/out (default=0.05).
            pause (float): Pause duration between fade-in and fade-out (default=1.0).
            loop (bool): If True, the fade animation repeats (default=False).
            permanent (bool): If True, text stays visible after fading in (default=False).
        """
        super().__init__()
        self.text: str = text
        self.color: Colors = color
        self.size: int = size
        self.speed: float = speed
        self.pause: float = pause
        self.opacity: float = 0.0
        self.running: bool = False
        self.content: Control = Text(self.text, color=self.color, size=self.size)
        self.loop: bool = loop
        self.permanent: bool = permanent

    def did_mount(self):
        """
        Called when the widget is mounted to the page.
        Starts the fade animation loop.
        """
        self.running = True
        self.page.run_task(self._fade_loop)

    def will_unmount(self):
        """
        Called when the widget is unmounted from the page.
        Stops the fade animation loop.
        """
        self.running = False

    async def _fade_in(self):
        """
        Gradually increases the text opacity until fully visible.
        """
        try:
            while self.opacity < 1.0 and self.running:
                self.opacity += 0.05
                self.update()
                await asyncio.sleep(self.speed)
        except AssertionError as e:
            return e

    async def _fade_out(self):
        """
        Gradually decreases the text opacity until fully transparent.
        """
        try:
            while self.opacity > 0.0 and self.running:
                self.opacity -= 0.05
                self.update()
                await asyncio.sleep(self.speed)
        except AssertionError as e:
            return e

    async def _fade_loop(self):
        """
        Main loop controlling the fade-in and fade-out animation.
        Handles pause, looping, and permanent display options.
        """
        while self.running:
            await self._fade_in()
            await asyncio.sleep(self.pause)
            if not self.permanent:
                await self._fade_out()
            if self.loop:
                await asyncio.sleep(self.pause)
            else:
                break
