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
        super().__init__()
        # Asegurar que texts sea lista
        self.texts: Union[str, List[str]] = texts if isinstance(texts, list) else [texts]
        self.speed: float = speed  # chars per second
        self.pause: float = pause  # second for pause on the texts
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
        self.running = True
        self.page.run_task(self._type_loop)

    def will_unmount(self):
        self.running = False

    async def _type_text(self, text: str):
        """Escribe un texto letra por letra."""
        self.value = ""
        self.content.value = self.value
        self.update()

        for letter in text:
            self.value += letter
            self.content.value = self.value
            self.update()
            await asyncio.sleep(1 / self.speed)

    async def _type_loop(self):
        """Bucle principal del typewriter."""
        while self.running:
            for text in self.texts:
                await self._type_text(text)
                await asyncio.sleep(self.pause)

            if not self.loop:  # if no loop ends
                break