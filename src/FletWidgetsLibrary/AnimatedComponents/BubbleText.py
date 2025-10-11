from typing import List, Union
from flet import (
    MarkdownExtensionSet,
    MarkdownCodeTheme,
    Container,
    Markdown,
    SnackBar,
    Colors,
    Column,
    border,
    Text,
)
import asyncio


class AnimatedTextBubble(Container):
    """Animated message bubble with Markdown support, typewriter animation, and a Copy button."""

    def __init__(
        self,
        texts: Union[str, List[str]],
        speed: int = 10,
        pause: float = 0,
        bgcolor: Colors = Colors.GREY_900,
        border_radius: int = 20,
        MarkdownCodeTheme: MarkdownCodeTheme = MarkdownCodeTheme.ATOM_ONE_DARK,
        ExtensionSet: MarkdownExtensionSet = MarkdownExtensionSet.GITHUB_WEB
    ):
        super().__init__()
        self.texts = texts if isinstance(texts, list) else [texts]
        self.speed = speed
        self.pause = pause
        self.running = False
        self.MarkdownTheme = MarkdownCodeTheme
        self.ExtensionSet = ExtensionSet

        self.bgcolor = bgcolor
        self.adaptive = True
        self.expand = True
        self.expand_loose = True
        self.padding = 10
        self.border_radius = border_radius
        self.border = border.all(3, Colors.with_opacity(0.4, Colors.WHITE))
        self.on_long_press = self._copy_to_clipboard
        self.ink = True

        self.message_column = Column(spacing=2, tight=False)
        self.content = self.message_column

    def _copy_to_clipboard(self, e):
        full_text = "\n".join(self.texts)
        clean_text = (
            full_text.replace("#", "")
            .replace("*", "")
            .replace("`", "")
            .strip()
        )
        self.page.set_clipboard(clean_text)

        # Mostrar notificación
        self.page.overlay.append(
            SnackBar(
                content=Text("✅ Copied to clipboard", color=Colors.WHITE),
                bgcolor=Colors.BLACK,
                open=True,
                action="Close",
                action_color=Colors.WHITE,
            )
        )
        self.page.update()

    def did_mount(self):
        self.running = True
        self.page.run_task(self._type_loop)

    def will_unmount(self):
        self.running = False

    async def _type_text(self, full_text: str):
        self.message_column.controls.clear()
        self.update()

        # Animación de aparición progresiva del markdown con soporte de links
        partial_text = ""
        md = Markdown(
            value="",
            selectable=True,
            extension_set=self.ExtensionSet,
            code_theme=self.MarkdownTheme,
            on_tap_link=lambda e: self.page.launch_url(e.data),  # 🚀 abre el link
        )
        self.message_column.controls.append(md)

        for ch in full_text:
            partial_text += ch
            md.value = partial_text
            self.update()
            await asyncio.sleep(1 / self.speed)
        self.update()

        if self.pause > 0:
            await asyncio.sleep(self.pause)

    async def _type_loop(self):
        for text in self.texts:
            if not self.running:
                break
            await self._type_text(text)