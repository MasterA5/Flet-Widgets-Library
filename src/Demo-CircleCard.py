from FletWidgetsLibrary import CircleCard
from flet import *

def main(page: Page):
    page.bgcolor = Colors.BLACK

    page.add(
        Container(
            content=Row(
                controls=[
                    CircleCard(
                        title=Text(i),
                        content=Text(i),
                        icon=Icons.random(),
                        expanded_width=200,
                        expanded_height=120,
                        bgcolor=Colors.random()
                    ) for i in range(3)
                ],
                expand=True,
                scroll="auto",
                wrap=True
            ),
            expand=True,
            alignment=alignment.center,
        )
    )


app(target=main)
