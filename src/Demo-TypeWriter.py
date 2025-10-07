from FletWidgetsLibrary import TypeWriter
from flet import (
    Page,
    app,
    Row,
    Colors
)

# Demo Example
def main(page:Page):
    page.vertical_alignment = "center"

    TypeWriterTextWithLoop = TypeWriter(
        texts=["Hello", "Flet", "Python"],
        bold=True,
        color=Colors.WHITE,
        size=30,
        speed=30
    )

    TypeWriterTextWithOutLoop = TypeWriter(
        texts="Hello Flet and Python",
        bold=True,
        color=Colors.WHITE,
        size=30,
        speed=50
    )

    page.add(
        Row(
            controls=[
                TypeWriterTextWithLoop
            ],
            alignment="center"
        ),
        Row(
            controls=[
                TypeWriterTextWithOutLoop
            ],
            alignment="center"
        )
    )

app(target=main)