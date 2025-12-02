from flet import ElevatedButton, Colors, Text, Row, Animation, AnimationCurve

class OauthProviderButton(ElevatedButton):
    def __init__(
        self, 
        text: str, 
        on_click: callable = None, 
        on_hover: callable = None,
        bgcolor: Colors = None,
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
        self.on_hover_event = on_hover
        self.animate_scale = Animation(300, AnimationCurve.DECELERATE)
        self.on_hover = self._handle_hover
        self.bgcolor = bgcolor

    def _handle_hover(self, e):
        if self.on_hover_event:
            self.on_hover_event(e)
        
        if e.data == "true":
            self.scale = 1.1
        else:
            self.scale = 1
        self.update()