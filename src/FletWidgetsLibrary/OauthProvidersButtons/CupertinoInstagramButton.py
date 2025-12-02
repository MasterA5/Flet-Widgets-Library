from .CupertinoOauthProviderButton import CupertinoOauthProviderButton
from flet import Colors, CupertinoColors, Row, Image, Text
from ..Resources.IconsBase64 import InstagramIcon
from typing import Union

class CupertinoInstagramButton(CupertinoOauthProviderButton):
    def __init__(
        self, 
        text: str = "Instagram Account", 
        on_click: callable = None, 
        bgcolor: Union[Colors, CupertinoColors] = Colors.GREY_900, 
        text_color: Union[Colors, CupertinoColors] = Colors.WHITE,
    ):
        super().__init__(text, on_click, bgcolor, text_color)
        self.content = Row(
            controls=[
                Image(
                    src_base64=InstagramIcon,
                    width=20,
                    height=20,
                ),
                Text(text, color=text_color)
            ],
            tight=True
        )