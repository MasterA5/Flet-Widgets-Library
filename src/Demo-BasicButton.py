from FletWidgetsLibrary import BasicButton
from flet import *

def main(page:Page):

    button1 = BasicButton(
        text="Click Me",
        bgcolor=Colors.BLUE_ACCENT_400,
        animation_duration=200,
        icon=Icons.TOUCH_APP,
        text_color=Colors.WHITE,
        on_click=lambda e: (
            page.controls.insert(1, Text("Button 1 Clicked")),
            page.update()
        )
    )

    button2 = BasicButton(
        text="Click Me",
        bgcolor=Colors.GREEN_ACCENT_700,
        animation_duration=200,
        icon=Icons.TOUCH_APP,
        text_color=Colors.WHITE,
        on_click=lambda e: (
            page.controls.insert(3, Text("Button 2 Clicked")),
            page.update()
        )
    )

    button3 = BasicButton(
        text="Click Me",
        bgcolor=Colors.PURPLE_ACCENT_700,
        animation_duration=200,
        icon=Icons.TOUCH_APP,
        text_color=Colors.WHITE,
        on_click=lambda e: (
            page.controls.insert(5, Text("Button 3 Clicked")),
            page.update()
        )
    )

    page.add(button1, button2, button3)

app(target=main)