from FletWidgetsLibrary import HighlightRotatingText
from flet import (
    TextStyle,
    Colors,
    Page,
    app,
    Row,
)

# Demo Example
def main(page:Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    RotatingTextWithLoop = HighlightRotatingText(
        static_text="Hello",
        phrases=["Flet", "Python", "World"],
        bold=True,
        box_color=Colors.PURPLE,
        color=Colors.WHITE,
        direction="bottom",
        loop=True,
        static_style=TextStyle(
            color=Colors.WHITE,
            size=30,
            weight="bold"
        ),
        width_factor=22,
        interval=1
    )

    RotatingTextWithOutLoop = HighlightRotatingText(
        static_text="Hello",
        phrases=["Flet", "Python", "World"],
        bold=True,
        box_color=Colors.PURPLE,
        color=Colors.WHITE,
        direction="bottom",
        loop=False,
        static_style=TextStyle(
            color=Colors.WHITE,
            size=30,
            weight="bold"
        ),
        width_factor=22,
        interval=1
    )

    page.add(
        # With Loop
        Row(
            controls=[
                RotatingTextWithLoop
            ],
            alignment="center"
        ),
        # With Out Loop
        Row(
            controls=[
                RotatingTextWithOutLoop
            ],
            alignment="center"
        )
    )
app(target=main)