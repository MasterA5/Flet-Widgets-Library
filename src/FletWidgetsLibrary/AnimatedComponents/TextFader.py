from flet import (
    Container,
    Control,
    Colors,
    Text
)
import asyncio

class TextFader(Container):
    def __init__(
        self, 
        text: str, 
        color: Colors = Colors.WHITE, 
        size: int = 24, 
        speed: float = 0.05, 
        pause: float = 1.0, 
        loop: bool = False,
        permanent: bool = False   # <- Nueva propiedad
    ):
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
        self.permanent: bool = permanent  # <- Se guarda el valor

    def did_mount(self):
        self.running = True
        self.page.run_task(self._fade_loop)

    def will_unmount(self):
        self.running = False

    async def _fade_in(self):
        try:
            while self.opacity < 1.0 and self.running:
                self.opacity += 0.05
                self.update()
                await asyncio.sleep(self.speed)
        except AssertionError as e:
            return e

    async def _fade_out(self):
        try:
            while self.opacity > 0.0 and self.running:
                self.opacity -= 0.05
                self.update()
                await asyncio.sleep(self.speed)
        except AssertionError as e:
            return e

    async def _fade_loop(self):
        while self.running:
            await self._fade_in()
            await asyncio.sleep(self.pause)
            if not self.permanent:
                await self._fade_out()
            if self.loop:
                await asyncio.sleep(self.pause)
            else:
                break
