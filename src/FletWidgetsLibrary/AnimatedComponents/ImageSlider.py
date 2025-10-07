from flet import (
    AnimatedSwitcherTransition,
    CrossAxisAlignment,
    MainAxisAlignment,
    AnimatedSwitcher,
    ClipBehavior,
    ControlEvent,
    ButtonStyle,
    HoverEvent,
    IconButton,
    Container,
    alignment,
    BoxShadow,
    Colors,
    Image,
    Icons,
    Stack,
    Row,
)
import asyncio

class ImagesSlider(Container):
    def __init__(
        self,
        images: list[Image],
        auto_play: bool = False,
        interval: float = 3.0,
        buttons_color: str = Colors.GREY_900,
        selected_buttons_color: str = Colors.WHITE,
        animation_type: str = "FADE",
    ):
        super().__init__()

        # Validación
        if not images:
            raise ValueError("Debe proporcionar al menos una imagen.")

        # Propiedades
        self.images = images
        self.auto_play = auto_play
        self.interval = interval
        self.current_index = 0
        self.auto_task = None
        self.is_running = False

        # Estilo general
        self.width = 768
        self.height = 432
        self.border_radius = 12
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.shadow = BoxShadow(blur_radius=25, spread_radius=2, color=Colors.BLACK26)
        self.buttons_color = buttons_color
        self.selected_buttons_color = selected_buttons_color
        self.animation_type = {
            "FADE": AnimatedSwitcherTransition.FADE, 
            "SCALE": AnimatedSwitcherTransition.SCALE, 
            "ROTATION": AnimatedSwitcherTransition.ROTATION
        }

        # Contenedor animado de la imagen actual
        self.switcher = AnimatedSwitcher(
            content=self.images[0],
            duration=400,
            reverse_duration=400,
            transition=self.animation_type.get(animation_type, AnimatedSwitcherTransition.FADE),
        )

        # Botones indicadores inferiores
        self.buttons = self._create_buttons()

        # Botones laterales de navegación
        self.prev_btn = self._create_nav_button(Icons.ARROW_BACK, self._on_prev_click)
        self.next_btn = self._create_nav_button(Icons.ARROW_FORWARD, self._on_next_click)

        # Layout principal
        self.content = Stack(
            controls=[
                self.switcher,
                # Botones laterales
                Row(
                    controls=[self.prev_btn, Container(expand=True), self.next_btn],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                # Indicadores inferiores
                Row(
                    controls=self.buttons,
                    alignment=MainAxisAlignment.CENTER,
                    bottom=20,
                ),
            ],
            alignment=alignment.center,
        )

    # --- Inicialización ---
    def did_mount(self):
        self.set_current(0)
        self.is_running = True
        if self.auto_play:
            self.auto_task = self.page.run_task(self._auto_switch)

    def will_unmount(self):
        """Se ejecuta al desmontar el control, detiene el autoplay."""
        self.is_running = False

    # --- Cambio de imagen manual ---
    def set_current(self, index: int):
        if not self.images:
            return

        self.current_index = index % len(self.images)
        self.switcher.content = self.images[self.current_index]
        self.switcher.update()

        for i, btn in enumerate(self.buttons):
            btn.bgcolor = (
                self.selected_buttons_color
                if i == self.current_index
                else self.buttons_color
            )
            btn.opacity = 1.0 if i == self.current_index else 0.4
        self.update()

    def _on_next_click(self, e: ControlEvent):
        self.set_current(self.current_index + 1)

    def _on_prev_click(self, e: ControlEvent):
        self.set_current(self.current_index - 1)

    # --- Creación de botones inferiores ---
    def _create_buttons(self):
        return [
            Container(
                width=14,
                height=14,
                border_radius=360,
                bgcolor=self.buttons_color,
                opacity=0.4,
                data=i,
                on_click=self._on_button_click,
                on_hover=self._on_hover_indicator,
                ink=True,
            )
            for i in range(len(self.images))
        ]

    def _on_hover_indicator(self, e: HoverEvent):
        e.control.scale = 1.25 if e.data == "true" else 1.0
        e.control.update()

    def _on_button_click(self, e: ControlEvent):
        self.set_current(e.control.data)

    # --- Botones laterales ---
    def _create_nav_button(self, icon_name, handler):
        return Container(
            content=IconButton(
                icon=icon_name,
                icon_size=26,
                icon_color=Colors.WHITE,
                on_click=handler,
                style=ButtonStyle(overlay_color=Colors.TRANSPARENT),
            ),
            bgcolor=Colors.with_opacity(0.25, Colors.BLACK),
            border_radius=360,
            padding=6,
            opacity=0.7,
            on_hover=self._on_hover_nav,
        )

    def _on_hover_nav(self, e: HoverEvent):
        e.control.opacity = 1.0 if e.data == "true" else 0.7
        e.control.update()

    # --- Cambio automático ---
    async def _auto_switch(self):
        while self.is_running:
            await asyncio.sleep(self.interval)
            if not self.page or not self.is_running:
                break
            self.set_current(self.current_index + 1)
