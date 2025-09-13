from flet import (
    Container, Colors, Divider, Text, BorderRadius, Page,
    Column, MainAxisAlignment, TextSpan, TextStyle,
    FontWeight, Row, SnackBar, TextDecoration, border
)
import asyncio
import re
from typing import List, Union, Optional


# ============================================================
# 📌 TEXT FORMATTER
# ============================================================
class TextFormatter:
    """
    Formats text with Markdown-like syntax and clickable links for Flet.

    Supported features:
        - Headings: "#", "##", "###"
        - Lists: "- "
        - Bold: **text**
        - Italic: _text_
        - Inline code: `code`
        - Markdown-style links: [Text](https://url)
        - Direct URLs: https://example.com
    """

    def __init__(self, color=Colors.WHITE):
        """
        Initialize the text formatter.

        Args:
            color (Colors): Default color for normal text.
        """
        self.color = color
        self.markdown_link_pattern = r"\[(.*?)\]\((https?://[^\s]+)\)"
        self.link_pattern = r"https?://[^\s]+"
        self.bold_pattern = r"\*\*(.*?)\*\*"
        self.italic_pattern = r"_(.*?)_"
        self.code_pattern = r"`(.*?)`"

    def format(self, text: str) -> Text:
        """
        Convert a raw string into a styled Flet `Text` object.

        Args:
            text (str): Input string.

        Returns:
            Text: Flet text object with styles applied.
        """
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
        """
        Parse inline Markdown patterns and return a list of text spans.

        Args:
            text (str): Input text to parse.

        Returns:
            List[TextSpan]: A list of styled text spans.
        """
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

            if first == md_link:  # <- [Text](url)
                content, url = first.groups()
                spans.append(TextSpan(text=content, url=url,
                                      style=TextStyle(color=Colors.BLUE_200,
                                                      decoration=TextDecoration.UNDERLINE)))
            elif first == link:  # <- Direct URL
                content = first.group(0)
                spans.append(TextSpan(text=content, url=content,
                                      style=TextStyle(color=Colors.BLUE_200,
                                                      decoration=TextDecoration.UNDERLINE)))
            elif first == code:  # <- `inline code`
                content = first.group(1)
                spans.append(TextSpan(text=content,
                                      style=TextStyle(color=Colors.AMBER_200,
                                                      font_family="monospace",
                                                      bgcolor=Colors.GREY_800)))
            elif first == bold:  # <- **bold**
                content = first.group(1)
                spans.append(TextSpan(text=content,
                                      style=TextStyle(color=self.color,
                                                      weight=FontWeight.BOLD)))
            elif first == italic:  # <- _italic_
                content = first.group(1)
                spans.append(TextSpan(text=content,
                                      style=TextStyle(color=self.color,
                                                      italic=True)))

            idx = end

        return spans


# ============================================================
# 📌 ANIMATED TEXT BUBBLE
# ============================================================
class AnimatedTextBubble(Container):
    """
    Animated text bubble with Markdown-like formatting,
    clickable links, and inline code block support.
    """

    def __init__(
        self,
        texts: Union[str, List[str]],
        speed: int = 20,
        pause: float = 0,
        bgcolor: Colors = Colors.GREY_800,
        on_copied: Optional[callable] = None,
    ):
        """
        Initialize the animated text bubble.

        Args:
            texts (str | List[str]): Text or list of texts to display.
            speed (int): Typing speed (characters per second).
            pause (float): Optional pause (in seconds) after finishing typing.
            bgcolor (Colors): Background color of the bubble.
            on_copied (callable, optional): Callback triggered when text is copied.
        """
        super().__init__()
        self.texts = texts if isinstance(texts, list) else [texts]
        self.speed = speed
        self.pause = pause
        self.running = False
        self.on_copied = on_copied

        # Appearance
        self.bgcolor = bgcolor
        self.border_radius = 15
        self.Text_content = "\n".join(self.texts)
        self.adaptive = True
        self.expand = True
        self.padding = 10
        self.ink = True

        # Content
        self.Text_column = Column(spacing=4, tight=False)
        self.content = self.Text_column
        self.formatter = TextFormatter(color=Colors.WHITE)
        self.border = border.all(color=Colors.with_opacity(0.5, self.bgcolor), width=2)

        # Copy to clipboard on long press
        self.on_long_press = self.copy_to_clipboard

    def copy_to_clipboard(self, e=None):
        """
        Copy the bubble's content to clipboard and show a snackbar.

        Args:
            e: Flet event (optional).
        """
        clean = re.sub(r"[*#`]", "", self.Text_content)
        self.page.set_clipboard(clean)
        self.page.overlay.append(SnackBar(content=Text("📋 Copied to clipboard"), open=True))
        if self.on_copied:
            self.on_copied(clean)
        self.page.update()

    def did_mount(self):
        """
        Start the typing animation when the widget is mounted.
        """
        self.running = True
        self.page.run_task(self._type_loop)

    def will_unmount(self):
        """
        Stop the typing animation when the widget is unmounted.
        """
        self.running = False

    async def _type_text(self, full_text: str):
        """
        Animate the typing effect for a single text block.

        Args:
            full_text (str): Full text to animate.
        """
        self.Text_column.controls.clear()
        self.update()

        in_code_block = False
        code_accum = ""

        for line in full_text.splitlines():
            stripped = line.strip()

            # Separator line ("---")
            if not in_code_block and stripped == "---":
                self.Text_column.controls.append(
                    Divider(height=1, color=Colors.GREY_600, opacity=0.5)
                )
                self.update()
                continue

            # Code block toggle
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

            # Inside code block
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

            # Normal text typing
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
        """
        Main loop to type multiple texts sequentially.
        """
        for text in self.texts:
            if not self.running:
                break
            await self._type_text(text)
