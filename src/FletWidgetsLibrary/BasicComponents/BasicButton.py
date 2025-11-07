from typing import Optional, Union, Callable
from flet import (
    RoundedRectangleBorder,
    AnimationCurve,
    ElevatedButton,
    ControlState,
    ButtonStyle,
    MouseCursor,
    HoverEvent,
    Animation,
    Colors,
)
import asyncio


class BasicButton(ElevatedButton):
    """
    A customizable and interactive button component for Flet.

    This class extends Flet's `ElevatedButton` to include:
    - Smooth hover and click animations.
    - Dynamic updates to text, icon, and colors.
    - Visual glow effects.
    - Simplified style configuration.

    Attributes
    ----------
    text : str
        The text displayed on the button.
    icon : Optional[str]
        Optional icon to display beside the text.
    bgcolor : str | Colors
        Background color of the button.
    text_color : str | Colors
        Text color of the button.
    click_action : Optional[Callable]
        Function called when the button is clicked.
    hover_scale : float
        Scale applied on hover (default: 1.08).
    click_scale : float
        Scale applied when clicked (default: 0.9).
    animation_duration : int
        Duration of animations in milliseconds (default: 200).
    """

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable] = None,
        bgcolor: Union[str, Colors] = Colors.BLUE,
        text_color: Union[str, Colors] = Colors.WHITE,
        icon: Optional[str] = None,
        hover_scale: float = 1.08,
        click_scale: float = 0.9,
        animation_duration: int = 200,
    ):
        super().__init__()

        # Core properties
        self.text = text
        self.icon = icon
        self.bgcolor = bgcolor
        self.text_color = text_color
        self.click_action = on_click

        # Animation parameters
        self.hover_scale = hover_scale
        self.click_scale = click_scale
        self.animation_duration = animation_duration

        # Button visual style
        self.style = ButtonStyle(
            bgcolor={ControlState.DEFAULT: bgcolor},
            color={ControlState.DEFAULT: text_color},
            overlay_color=Colors.with_opacity(0.15, text_color),
            shape={ControlState.DEFAULT: RoundedRectangleBorder(radius=12)},
            mouse_cursor={ControlState.HOVERED: MouseCursor.CLICK},
        )

        # Animation configuration
        self.animate_scale = Animation(self.animation_duration, AnimationCurve.EASE_OUT)

        # Event bindings
        self.on_hover = self._on_hover
        self.on_click = self._on_click

    # -------------------------------
    # Internal Event Handlers
    # -------------------------------
    def _on_click(self, e):
        """Handles button click events with animation."""
        if self.click_action:
            self.click_action(e)
        self.__animate__(e, "click")

    def _on_hover(self, e: HoverEvent):
        """Handles hover enter/leave events with scale animation."""
        self.__animate__(e, "hover")

    def __animate__(self, e, data: str):
        """Internal animation logic for click and hover effects."""
        if data == "click":
            self.scale = self.click_scale
            self.update()
            asyncio.run(asyncio.sleep(0.1))
            self.scale = 1
            self.update()
        elif data == "hover":
            self.scale = self.hover_scale if e.data == "true" else 1
            self.update()

    # -------------------------------
    # Dynamic Update Methods
    # -------------------------------
    def set_button_text(self, text: str):
        """
        Change the button's text dynamically.

        Parameters
        ----------
        text : str
            The new text to display on the button.
        """
        if text:
            self.text = text
            self.update()

    def set_icon(self, icon: Optional[str] = None, color: Optional[Union[str, Colors]] = None):
        """
        Change the button's icon and optionally its color.

        Parameters
        ----------
        icon : str, optional
            The new icon name.
        color : str | Colors, optional
            The new icon color.
        """
        self.icon = icon
        if color:
            self.icon_color = color
        self.update()

    def toggle_icon(self, icon1: str, icon2: str):
        """
        Toggle between two icons.

        Parameters
        ----------
        icon1 : str
            The first icon.
        icon2 : str
            The second icon to toggle to.
        """
        self.icon = icon2 if self.icon == icon1 else icon1
        self.update()

    def toggle_color(self, color1: str, color2: str):
        """
        Toggle the background color between two options.

        Parameters
        ----------
        color1 : str
            The first background color.
        color2 : str
            The second background color.
        """
        self.bgcolor = color2 if self.bgcolor == color1 else color1
        self.style.bgcolor = {ControlState.DEFAULT: self.bgcolor}
        self.update()

    def toggle_text_color(self, color1: str, color2: str):
        """
        Toggle the text color between two options.

        Parameters
        ----------
        color1 : str
            The first text color.
        color2 : str
            The second text color.
        """
        self.text_color = color2 if self.text_color == color1 else color1
        self.style.color = {ControlState.DEFAULT: self.text_color}
        self.update()

    def glow(self, color: str = Colors.YELLOW, duration: float = 0.3):
        """
        Create a temporary glowing overlay effect.

        Parameters
        ----------
        color : str, optional
            The glow color (default: Colors.YELLOW).
        duration : float, optional
            Duration of the glow effect in seconds (default: 0.3).
        """
        async def animate_glow():
            old_color = self.style.overlay_color
            self.style.overlay_color = Colors.with_opacity(0.5, color)
            self.update()
            await asyncio.sleep(duration)
            self.style.overlay_color = old_color
            self.update()

        asyncio.run(animate_glow())