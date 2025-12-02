from flet import Colors, Image, Row, Text, ButtonStyle
from .OauthProviderButton import OauthProviderButton
from ..Resources.IconsBase64 import LinkedinIcon

class LinkedinButton(OauthProviderButton):
    def __init__(
        self, 
        text: str = "Linkedin Account", 
        on_click: callable = None, 
        on_hover: callable = None, 
        bgcolor: Colors = None, 
        text_color = Colors.WHITE
    ):
        super().__init__(text, on_click, on_hover, bgcolor, text_color) 
        self.content = Row(
            controls=[
                Image(
                    src_base64=LinkedinIcon,
                    width=20,
                    height=20,
                ),
                Text(
                    value=text,
                    color=self.text_color
                )
            ],
            tight=True
        )
        self.style = ButtonStyle(
            padding=10,
            animation_duration=300
        )