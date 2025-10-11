from FletWidgetsLibrary import AnimatedTextBubble
from flet import (
    MarkdownExtensionSet,
    MarkdownCodeTheme,
    Colors,
    Page,
    Row,
    app,
)

# Demo Example
def main(page:Page):
    
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
        "Official link: [flet.dev](https://flet.dev)\n"
        "Github Repo: [flet-dev](https://github.com/flet-dev/flet)"
    )

    BubbleText = AnimatedTextBubble(
        texts=demo_text,
        bgcolor=Colors.GREY_700,
        speed=60,
        MarkdownCodeTheme=MarkdownCodeTheme.DRAGULA,
        ExtensionSet=MarkdownExtensionSet.GITHUB_WEB,
    )

    page.add(
        Row(
            controls=[BubbleText],
            width=300, # Adjust this value for asing the width to the bubble text
        )
    )
app(target=main)