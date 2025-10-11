from FletWidgetsLibrary import (
    HighlightRotatingText,
    AnimatedTextBubble,
    ImagesSlider,
    TypeWriter,
    TextFader,
    SplitText,
)
from flet import *


def section(title: str, color: str, *controls: Control):
    """Crea una sección con título, contenido y divisor."""
    return Column(
        controls=[
            Text(value=title, color=color, size=30, weight="bold"),
            *controls,
            Divider(color=color, height=15),
        ],
        spacing=10,
    )


def main(page: Page):
    # --- Configuración general ---
    page.title = "Flet Widgets Demo"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window.width = 1200
    page.window.height = 800
    page.scroll = ScrollMode.AUTO
    page.padding = 20
    page.bgcolor = Colors.BLACK87

    # --- Datos de ejemplo ---
    demo_text = (
        "### 🌟 What is Flet?\n\n"
        "**Flet** is a framework in Python for building web, desktop, and mobile apps.\n\n"
        "---\n\n"
        "### Features\n"
        "- Cross-platform\n"
        "- Easy to use\n"
        "- Based on Flutter\n\n"
        "```python\n"
        "import flet as ft\n"
        "def main(page: ft.Page):\n"
        "    page.bgcolor = ft.colors.BLACK\n"
        "    page.add(ft.Text('Hello Flet'))\n"
        "ft.app(target=main)\n"
        "```\n\n"
        "Official link: [flet.dev](https://flet.dev)"
    )

    images_1 = [
        Image(src=f"https://picsum.photos/800/450?{i}", fit=ImageFit.COVER)
        for i in range(10)
    ]

    images_2 = [
        Image(src=f"https://picsum.photos/800/450?{i*2}", fit=ImageFit.COVER)
        for i in range(10)
    ]

    # --- Construcción de la interfaz ---
    content = Column(
        spacing=30,
        scroll=ScrollMode.ADAPTIVE,
        controls=[
            section(
                "SplitText Without Loop",
                Colors.CYAN,
                SplitText(
                    texts=["Hello World", "Offset Animation"],
                    speed=0.1,
                    pause=1.5,
                    loop=False,
                    size=32,
                    color=Colors.CYAN,
                    bold=True,
                    direction="bottom",
                ),
            ),
            section(
                "SplitText With Loop",
                Colors.BROWN,
                SplitText(
                    texts=["Hello World", "Offset Animation With Loop"],
                    speed=0.1,
                    pause=1.5,
                    loop=True,
                    size=32,
                    color=Colors.BROWN,
                    bold=True,
                    direction="bottom",
                ),
            ),
            section(
                "Fade Text Without Loop (Permanent)",
                Colors.AMBER,
                TextFader(
                    text="Hello World And Hello Flet",
                    loop=False,
                    color=Colors.AMBER,
                    permanent=True,
                ),
            ),
            section(
                "Fade Text With Loop (Not Permanent)",
                Colors.RED,
                TextFader(
                    text="Hello World And Hello Flet",
                    loop=True,
                    color=Colors.RED,
                    permanent=False,
                ),
            ),
            section(
                "TypeWriter Text Animation",
                Colors.BLUE,
                TypeWriter(
                    texts=[
                        "Hello Welcome To Flet This Is A Type Writer Animated",
                        "This Is A Second Part For The Type Writer Content",
                    ],
                    speed=30,
                    size=40,
                    color=Colors.BLUE,
                ),
            ),
            section(
                "TypeWriter Text Animation With Loop",
                Colors.GREEN,
                TypeWriter(
                    texts=[
                        "Hello Welcome To Flet This Is A Type Writer Animated",
                        "But This Is A Second Part For The Type Writer Content With Loop",
                    ],
                    speed=30,
                    size=40,
                    color=Colors.GREEN,
                    loop=True,
                ),
            ),
            section(
                "Bubble Text Animation",
                Colors.PURPLE,
                Row(
                    controls=[
                        AnimatedTextBubble(
                            texts=demo_text,
                            bgcolor=Colors.GREY_700,
                            speed=60,
                            MarkdownCodeTheme=MarkdownCodeTheme.DRAGULA,
                            ExtensionSet=MarkdownExtensionSet.GITHUB_WEB,
                        )
                    ],
                    alignment=MainAxisAlignment.START,
                    width=600,
                ),
            ),
            section(
                "Highlight Rotating Text",
                Colors.DEEP_PURPLE,
                HighlightRotatingText(
                    static_text="Creative",
                    phrases=["thinking", "building", "coding"],
                    interval=1.5,
                    box_color=Colors.DEEP_PURPLE,
                    size=30,
                    direction="top",
                    speed=0.08,
                    width_factor=22,
                ),
            ),
            section(
                "Images Slider Without AutoPlay",
                Colors.TEAL,
                ImagesSlider(
                    images=images_2,
                    animation_type="SCALE",
                    auto_play=False,
                ),
            ),
            section(
                "Images Slider With AutoPlay",
                Colors.DEEP_PURPLE,
                ImagesSlider(
                    images=images_1,
                    auto_play=True,
                    interval=1.5,
                    animation_type="FADE",
                ),
            ),
        ],
    )

    page.add(content)


app(target=main)
