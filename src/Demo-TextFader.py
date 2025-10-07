from FletWidgetsLibrary import TextFader
from flet import (
    Page,
    app,
    Row,
    Colors
)

# Demo Example
def main(page:Page):
    page.vertical_alignment = "center"

    TextFaderWithLoop = TextFader(
        text="Hello Python",
        loop=True,
        color=Colors.WHITE,
        permanent=False,
        speed=0.05,
        size=30,
    )

    TextFaderWithOutLoop = TextFader(
        text="Hello Flet",
        loop=False,
        color=Colors.WHITE,
        permanent=True,
        speed=0.05,
        size=30,
    )

    TextFaderWithOutPermanent = TextFader(
        text="Hello World",
        loop=False,
        color=Colors.WHITE,
        permanent=False,
        speed=0.05,
        size=30,
    )

    page.add(
        Row(
            controls=[
                TextFaderWithLoop
            ],
            alignment="center"
        ),
        Row(
            controls=[
                TextFaderWithOutLoop
            ],
            alignment="center"
        ),
        Row(
            controls=[
                TextFaderWithOutPermanent
            ],
            alignment="center"
        )
    )

app(target=main)