from FletWidgetsLibrary import SplitText
from flet import (
    Page,
    app,
    Row
)

# Demo Example
def main(page:Page):
    page.vertical_alignment = "center"

    SplitTextWithLoop = SplitText(
        texts=["Hello", "Python", "Flet", "World"],
        loop=True,
        size=30,
        direction="bottom", # <- "top" "left" "right"
        bold=True,
        speed=0.01 # <- The closer it is to zero, the faster it moves.
    )

    SplitTextWithOutLoop = SplitText(
        texts="Hello", # <- Not needed pass a list you can pass a simple string
        loop=False,
        size=30,
        direction="bottom", # <- "top" "left" "right"
        bold=True,
        speed=0.01 # <- The closer it is to zero, the faster it moves.
    )

    page.add(
        Row(
            controls=[
                SplitTextWithLoop
            ],
            alignment="center"
        ),
        Row(
            controls=[
                SplitTextWithOutLoop
            ],
            alignment="center"
        )
    )

app(target=main)