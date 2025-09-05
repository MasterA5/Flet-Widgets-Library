from flet import (
    Container, Colors, Divider, Text, BorderRadius, Page,
    Column, MainAxisAlignment, TextSpan, TextStyle,
    FontWeight, Row, SnackBar, TextDecoration, border
)
import asyncio
import re
from typing import List, Union, Optional


# ---------- TEXT FORMATTER ----------
class TextFormatter:
    """Formatea texto estilo markdown y links clicables."""
    def __init__(self, color=Colors.WHITE):
        self.color = color
        self.markdown_link_pattern = r"\[(.*?)\]\((https?://[^\s]+)\)"
        self.link_pattern = r"https?://[^\s]+"
        self.bold_pattern = r"\*\*(.*?)\*\*"
        self.italic_pattern = r"_(.*?)_"
        self.code_pattern = r"`(.*?)`"

    def format(self, text: str) -> Text:
        s = text.strip()
        if s.startswith("### "):
            return Text(s[4:], size=16, weight=FontWeight.W_700, color=Colors.AMBER)
        if s.startswith("## "):
            return Text(s[3:], size=18, weight=FontWeight.W_700, color=Colors.AMBER)
        if s.startswith("# "):
            return Text(s[2:], size=20, weight=FontWeight.W_700, color=Colors.AMBER)
        if s.startswith("- "):
            return Text("• " + s[2:], color=self.color)
        return Text(spans=self._format_spans(text))

    def _format_spans(self, text: str) -> List[TextSpan]:
        spans: List[TextSpan] = []
        idx = 0
        while idx < len(text):
            md_link = re.search(self.markdown_link_pattern, text[idx:])
            link = re.search(self.link_pattern, text[idx:])
            code = re.search(self.code_pattern, text[idx:])
            bold = re.search(self.bold_pattern, text[idx:])
            italic = re.search(self.italic_pattern, text[idx:])

            matches = [m for m in [md_link, link, code, bold, italic] if m]
            if not matches:
                spans.append(TextSpan(text=text[idx:], style=TextStyle(color=self.color)))
                break

            first = min(matches, key=lambda m: m.start())
            start, end = first.span()
            start += idx
            end += idx

            if start > idx:
                spans.append(TextSpan(text=text[idx:start], style=TextStyle(color=self.color)))

            if first == md_link:  # [Texto](url)
                content, url = first.groups()
                spans.append(TextSpan(text=content, url=url,
                                      style=TextStyle(color=Colors.BLUE_200,
                                                      decoration=TextDecoration.UNDERLINE)))
            elif first == link:  # URL directa
                content = first.group(0)
                spans.append(TextSpan(text=content, url=content,
                                      style=TextStyle(color=Colors.BLUE_200,
                                                      decoration=TextDecoration.UNDERLINE)))
            elif first == code:  # `inline code`
                content = first.group(1)
                spans.append(TextSpan(text=content,
                                      style=TextStyle(color=Colors.AMBER_200,
                                                      font_family="monospace",
                                                      bgcolor=Colors.GREY_800)))
            elif first == bold:  # **bold**
                content = first.group(1)
                spans.append(TextSpan(text=content,
                                      style=TextStyle(color=self.color,
                                                      weight=FontWeight.BOLD)))
            elif first == italic:  # _italic_
                content = first.group(1)
                spans.append(TextSpan(text=content,
                                      style=TextStyle(color=self.color,
                                                      italic=True)))

            idx = end

        return spans


# ---------- TEXT BUBBLE ----------
class AnimatedTextBubble(Container):
    """Burbuja animada con soporte de markdown, links y bloques de código."""
    def __init__(
        self,
        texts: Union[str, List[str]],
        speed: int = 20,
        pause: float = 0,
        bgcolor: Colors = Colors.GREY_800,
        on_copied: Optional[callable] = None,
    ):
        super().__init__()
        self.texts = texts if isinstance(texts, list) else [texts]
        self.speed = speed
        self.pause = pause
        self.running = False
        self.on_copied = on_copied

        # Apariencia
        self.bgcolor = bgcolor
        self.border_radius = 15
        self.Text_content = "\n".join(self.texts)
        self.adaptive = True
        self.expand = True
        self.padding = 10
        self.ink = True

        # Contenido
        self.Text_column = Column(spacing=4, tight=False)
        self.content = self.Text_column
        self.formatter = TextFormatter(color=Colors.WHITE)
        self.border = border.all(color=Colors.with_opacity(0.5, self.bgcolor), width=2)

        # Acción
        self.on_long_press = self.copy_to_clipboard

    def copy_to_clipboard(self, e=None):
        clean = re.sub(r"[*#`]", "", self.Text_content)
        self.page.set_clipboard(clean)
        self.page.overlay.append(SnackBar(content=Text("📋 Copied to clipboard"), open=True))
        if self.on_copied:
            self.on_copied(clean)
        self.page.update()

    def did_mount(self):
        self.running = True
        self.page.run_task(self._type_loop)

    def will_unmount(self):
        self.running = False

    async def _type_text(self, full_text: str):
        self.Text_column.controls.clear()
        self.update()

        in_code_block = False
        code_accum = ""

        for line in full_text.splitlines():
            stripped = line.strip()

            # Separador
            if not in_code_block and stripped == "---":
                self.Text_column.controls.append(
                    Divider(height=1, color=Colors.GREY_600, opacity=0.5)
                )
                self.update()
                continue

            # Bloques de código
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                if in_code_block:
                    code_accum = ""
                    self.Text_column.controls.append(
                        Container(
                            content=Text(""), 
                            padding=10,
                            bgcolor=Colors.with_opacity(
                                color=Colors.LIGHT_BLUE_500,
                                opacity=0.5, 
                            ),
                            border_radius=10
                        )
                    )
                    self.update()
                continue

            if in_code_block:
                for ch in line + "\n":
                    code_accum += ch
                    self.Text_column.controls[-1] = Container(
                        Text(code_accum, style=TextStyle(font_family="monospace", color=Colors.WHITE)),
                        padding=10,
                        bgcolor=Colors.with_opacity(0.5, Colors.LIGHT_BLUE_500),
                        border_radius=10,
                        on_click=lambda e, c=code_accum: self.copy_to_clipboard(),
                        ink=True
                    )
                    self.update()
                    await asyncio.sleep(1 / self.speed)
                continue

            # Texto normal
            partial_text = ""
            self.Text_column.controls.append(Text(""))
            for ch in line:
                partial_text += ch
                self.Text_column.controls[-1] = self.formatter.format(partial_text)
                self.update()
                await asyncio.sleep(1 / self.speed)

        if self.pause > 0:
            await asyncio.sleep(self.pause)

    async def _type_loop(self):
        for text in self.texts:
            if not self.running:
                break
            await self._type_text(text)