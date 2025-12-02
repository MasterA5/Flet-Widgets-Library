from flet import Colors, CupertinoColors, Row, Text, CupertinoButton
from typing import Union

class CupertinoOauthProviderButton(CupertinoButton):
    def __init__(
        self, 
        text: str, 
        on_click: callable = None,
        bgcolor: Union[Colors, CupertinoColors] = Colors.GREY_800,
        text_color: Colors = Colors.WHITE
    ):
        super().__init__()
        self.text_color = text_color
        self.provider_icon = None
        self.content = Row(
            controls=[
                Text(
                    value=text,
                    color=self.text_color
                )
            ],
            tight=True
        )
        self.on_click = on_click
        self.bgcolor = bgcolor
        self.padding = 10