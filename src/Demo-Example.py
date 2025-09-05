from FletWidgetsLibrary import TextFader, TypeWriter, AnimatedTextBubble
from flet import *

# <-------EXAMPLE DEMO------->
def main(page:Page):
    page.horizontal_alignment="center"
    page.vertical_alignment="center"
    page.window.width = 1200
    page.window.height = 800
    page.scroll = "auto"

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


    page.add(
        Text(
            value="This Is A Fade Text With Out Loop Animation And Permanent Opacity",
            color=Colors.AMBER
        ),
        TextFader(
            text="Hello World And Hello Flet",
            loop=False,
            color=Colors.AMBER,
            permanent=True
        ),
        Divider(
            color=Colors.AMBER,
            height=10
        ),
        Text(
            value="This Is A Fade Text With Loop Animation And Not Permanent Opacity",
            color=Colors.RED
        ),
        TextFader(
            text="Hello World And Hello Flet",
            loop=True,
            color=Colors.RED,
            permanent=False
        ),
        Divider(
            color=Colors.RED,
            height=10
        ),
        Text(
            value="This Is A Type Writer Text Animated",
            color=Colors.BLUE
        ),
        TypeWriter(
            texts=[
                "Hello Welcome To Flet This Is A Type Writer Animated", 
                "This Is A Second Part For The Type Writer Content"
            ],
            speed=30,
            size=40,
            color=Colors.BLUE
        ),
        Divider(
            color=Colors.BLUE,
            height=10
        ),
        Text(
            value="This Is A Bubbble Text Animated",
            color=Colors.PURPLE,
        ),
        Row(
            controls=[
                AnimatedTextBubble(texts=demo_text, speed=60, bgcolor=Colors.PURPLE) # <- Bassed in TypeWriter Component
            ],
            alignment=MainAxisAlignment.START,
            
            width=400 # <- Adjust this value for the width of the bubble
        )
    )
app(target=main)