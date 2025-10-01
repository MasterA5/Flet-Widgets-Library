from flet import (
    MainAxisAlignment,
    AnimationCurve,
    FontWeight,
    TextStyle,
    Container,
    Animation,
    padding,
    Colors,
    Text,
    Page,
    Column,
    Row,
    app,
)
import asyncio
from typing import Union


class HighlightRotatingText(Row):
    """
    A composite widget that displays a fixed static text followed by
    an animated text inside a colored box. The animated text rotates
    through a list of phrases, animating letter by letter with smooth
    entry transitions.

    Features:
        - Static text (optional) combined with animated rotating text.
        - Animated appearance of letters with configurable speed/direction.
        - Auto-resizing box width based on the text length.
        - Supports looping or stopping at the last phrase.
        - Fade-out + letter-by-letter animation when switching phrases.

    Args:
        static_text (str): Text displayed before the animated box.
        phrases (list[str] | str): List of phrases or a single phrase to animate.
        interval (float): Seconds to wait before switching to the next phrase.
        size (int): Font size of the animated text.
        color (str): Color of the animated text.
        bold (bool): Whether animated text is bold.
        box_color (str): Background color of the box around animated text.
        loop (bool): Whether to loop phrases indefinitely.
        direction (str): Entry direction of the letters ("bottom", "top", "left", "right").
        speed (float): Delay in seconds between showing each letter.
        width_factor (int): Approximate pixels per character to calculate box width.
        static_style (TextStyle | None): Custom style for static text.
    """

    def __init__(
        self,
        static_text: str,
        phrases: Union[list[str], str],
        interval: float = 2.0,
        size: int = 28,
        color: str = Colors.WHITE,
        bold: bool = True,
        box_color: str = Colors.INDIGO,
        loop: bool = True,
        direction: str = "bottom",  # "bottom", "top", "left", "right"
        speed: float = 0.05,
        width_factor: int = 20,
        static_style: TextStyle | None = None,
    ):
        super().__init__()
        self.interval = interval
        self.size = size
        self.color = color
        self.bold = bold
        self.box_color = box_color
        self.loop = loop
        self.direction = direction
        self.speed = speed
        self.width_factor = width_factor

        # Normalize phrases to list
        self.phrases = phrases if isinstance(phrases, list) else [phrases]
        if not self.phrases:
            self.phrases = [""]

        self.index = 0
        self.running = False

        # Static text
        self.static = Text(
            static_text,
            style=static_style
            or TextStyle(size=28, weight=FontWeight.BOLD, color=Colors.GREY_200),
        )

        # Animated box (Container + Row of letters)
        self.row = Row(spacing=2, alignment="center")
        self.animated_box = Container(
            content=self.row,
            bgcolor=self.box_color,
            padding=padding.symmetric(horizontal=10, vertical=4),
            border_radius=8,
            animate=Animation(300, AnimationCurve.DECELERATE),
        )

        self.controls = [self.static, self.animated_box]

    # ------------------------------
    # Animation helpers
    # ------------------------------
    def _get_offset(self):
        """Return entry offset based on direction."""
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
        """Animate letters of a single phrase into the box."""
        self.row.controls.clear()

        # Adapt width dynamically
        self.animated_box.width = len(text) * self.width_factor
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

    async def _rotate(self):
        """Rotate through phrases continuously (or until stopped)."""
        while self.running:
            phrase = self.phrases[self.index]
            await self._animate_text(phrase)
            await asyncio.sleep(self.interval)

            self.index += 1
            if self.index >= len(self.phrases):
                if self.loop:
                    self.index = 0
                else:
                    self.running = False
                    break

    # ------------------------------
    # Lifecycle management
    # ------------------------------
    def start(self, e=None):
        """Start the rotation animation."""
        if not self.running:
            self.running = True
            self.page.run_task(self._rotate)

    def stop(self):
        """Stop the rotation animation."""
        self.running = False

    def did_mount(self):
        """Called when widget is mounted on the page."""
        self.start()

    def will_unmount(self):
        """Called when widget is removed from the page."""
        self.stop()


# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    def main(page: Page):
        page.bgcolor = Colors.BLACK
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"

        rot_1 = HighlightRotatingText(
            static_text="Creative",
            phrases="thinking",
            interval=1.5,
            box_color=Colors.DEEP_PURPLE,
            size=30,
            direction="top",
            speed=0.08,
            width_factor=22,
        )

        rot_2 = HighlightRotatingText(
            static_text="",
            phrases=["welcome", "to", "flet", "and", "python"],
            interval=1.5,
            box_color=Colors.DEEP_PURPLE,
            size=30,
            direction="top",
            speed=0.08,
            width_factor=25,
        )

        page.add(Column(controls=[rot_1, rot_2]))


    app(target=main)
