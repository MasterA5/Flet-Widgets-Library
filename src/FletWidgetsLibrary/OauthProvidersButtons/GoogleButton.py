from flet import Colors, Image, Row, Text, ButtonStyle
from .OauthProviderButton import OauthProviderButton
from ..Resources.IconsBase64 import GoogleIcon

class GoogleButton(OauthProviderButton):
    def __init__(
        self, 
        text: str = "Google Account", 
        on_click: callable = None, 
        on_hover: callable = None, 
        bgcolor: Colors = None, 
        text_color = Colors.WHITE
    ):
        super().__init__(text, on_click, on_hover, bgcolor, text_color) 
        self.content = Row(
            controls=[
                Image(
                    src_base64=GoogleIcon,
                    width=20,
                    height=20,
                    border_radius=100
                ),
                Text(
                    value=text,
                    color=self.text_color
                )
            ],
            tight=True
        )
        self.style = ButtonStyle(
            padding=5,
            animation_duration=300
        )