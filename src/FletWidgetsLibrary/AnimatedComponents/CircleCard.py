from typing import Union, Callable
from flet import (
    CrossAxisAlignment,
    AnimationCurve,
    Container,
    alignment,
    Animation,
    Control,
    Divider,
    Column,
    border,
    Colors,
    Icons,
    Icon,
    Row,
)


class CircleCard(Container):
    """
    A circular expandable card widget that transitions smoothly between a collapsed
    circular icon button and an expanded card displaying a title and additional content.

    This component is ideal for dashboards, menus, toolboxes, quick actions,
    or any UI element requiring collapsible/expandable behavior.

    Parameters
    ----------
    title : Control, optional
        A Flet control displayed as the title when the card is expanded.
    icon : Union[Icon, Icons], optional
        Main icon shown in both collapsed and expanded modes.
        Defaults to a random icon.
    icon_color : Colors, optional
        Color applied to the icon.
    content : Control, optional
        Additional content displayed when the card expands.
    expanded_width : int, optional
        Width of the card when expanded.
    expanded_height : int, optional
        Height of the card when expanded.
    collapsed_width : int, optional
        Width when the card is collapsed.
    bgcolor : Colors, optional
        Background color of the card.
    padding : int, optional
        Internal padding of the card container.
    on_click : Callable, optional
        External callback executed when the card is clicked/toggled.
    animation_duration : int, optional
        Duration of the expand/collapse animation in milliseconds.
    border_color : Colors, optional
        Color of the border around the card.
    divider_color : Colors, optional
        Color of the divider shown when expanded.
    animation_curve : AnimationCurve, optional
        Animation curve controlling the smoothness of transitions.
    """

    def __init__(
        self,
        title: Control = None,
        icon: Union[Icon, Icons] = Icons.random(),
        icon_color: Colors = Colors.WHITE,
        content: Control = None,
        expanded_width: int = 500,
        expanded_height: int = 200,
        collapsed_width: int = 60,
        bgcolor: Colors = Colors.GREY_900,
        padding: int = 16,
        on_click: Callable = None,
        animation_duration: int = 300,
        border_color: Colors = Colors.WHITE,
        divider_color: Colors = Colors.WHITE,
        animation_curve: AnimationCurve = AnimationCurve.DECELERATE
    ):
        super().__init__()

        # --- Parameters ---
        self.expanded_width = expanded_width
        self.expanded_height = expanded_height
        self.collapsed_width = collapsed_width
        self.on_click_callback = on_click
        self.is_open = False

        # --- Expandable content ---
        self.card_content = content
        self.card_content.visible = False
        self.alignment = alignment.center
        self.border_color = border_color

        # --- Title ---
        self.title = title
        self.title.visible = False

        # --- Icon ---
        self.icon = Icon(name=icon, size=28, color=icon_color)

        # --- Header row ---
        if self.title is not None:
            self.header = Row(
                controls=[self.icon, self.title]
            )
        else:
            self.header = Row(controls=[self.icon])

        # --- Divider ---
        self.divider = Divider(height=5, visible=self.is_open, color=divider_color)

        # --- Layout ---
        self.column = Column(
            controls=[
                self.header,
                self.divider,
                self.card_content
            ],
            spacing=10,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        # --- Card appearance ---
        self.content = self.column
        self.width = self.collapsed_width
        self.bgcolor = bgcolor
        self.padding = padding
        self.height = 60
        self.border_radius = 100
        self.animation_curve = animation_curve
        self.animate = Animation(animation_duration, self.animation_curve)
        self.border = border.all(0.5, self.border_color)
        self.on_click = self._handle_click

    def _handle_click(self, e):
        """
        Internal click handler that toggles the card's open/closed state,
        triggers UI updates, and executes the external callback (if provided).

        Parameters
        ----------
        e : Event
            The click event information.
        """
        self.is_open = not self.is_open

        if self.is_open:
            # Expanded state
            self.width = self.expanded_width
            self.card_content.visible = True
            self.border_radius = 20
            self.height = self.expanded_height
            self.border = border.all(1, self.border_color)
            self.divider.visible = True
            self.title.visible = True
        else:
            # Collapsed state
            self.width = self.collapsed_width
            self.card_content.visible = False
            self.border_radius = 100
            self.height = 60
            self.border = border.all(0.5, self.border_color)
            self.divider.visible = False
            self.title.visible = False

        self.update()

        # External callback
        if self.on_click_callback:
            self.on_click_callback(e)