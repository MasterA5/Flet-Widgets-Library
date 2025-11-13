from typing import Optional, Union
from dataclasses import dataclass
from flet import (
    AnimatedSwitcherTransition,
    CrossAxisAlignment,
    MainAxisAlignment,
    AnimatedSwitcher,
    OutlinedButton,
    ElevatedButton,
    FilledButton,
    Container,
    TextAlign,
    alignment,
    padding,
    Divider,
    Control,
    Column,
    Colors,
    Icons,
    Icon,
    Text,
    Row,
)


# === DataClass para eventos del Stepper ===
@dataclass
class StepperEvent:
    type: str                   # "next", "prev", "change", "complete"
    current_step: int            # índice del paso actual
    total_steps: int             # cantidad total de pasos
    step: Control                # referencia al Step actual
    is_first: bool               # True si es el primer paso
    is_last: bool                # True si es el último paso
    completed: bool              # True si el Stepper se completó
    parent: Control

# === Componente de cada paso ===
class StepperStepCard(Container):
    def __init__(
        self,
        title: str,
        subtitle: str = "",
        description: str = "",
        icon: Union[Control, Icons] = Icons.CIRCLE,
        icon_color: str = Colors.WHITE,
        icon_size: int = 30,
        content: Optional[Control] = None,
        color: str = Colors.BLUE_400,
        active_color: Optional[str] = None,
    ):
        super().__init__()

        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.icon_color = icon_color
        self.icon_size = icon_size
        self.icon = Icon(name=icon, color=self.icon_color, size=self.icon_size) if not isinstance(icon, Control) else icon 
        self.color = color
        self.active_color = active_color or color

        self.inner_content = content or Text(f"Step Content: {title}", size=14)

        self.bgcolor = Colors.with_opacity(0.1, Colors.BLUE_GREY_900)
        self.border_radius = 10
        self.padding = 15
        self.expand = True

        self.content = Column(
            spacing=10,
            controls=[
                Row(
                    spacing=10,
                    controls=[
                        self.icon,
                        Column(
                            spacing=1,
                            controls=[
                                Text(self.title, size=18, weight="bold", color=Colors.WHITE),
                                Text(self.subtitle if self.subtitle else self.description, size=13, color=Colors.GREY_400),
                            ],
                        ),
                    ],
                ),
                Divider(color=Colors.with_opacity(0.15, Colors.WHITE)),
                Text(self.description, color=Colors.GREY_300, size=13),
                self.inner_content,
            ],
        )

# === Stepper principal ===
class Stepper(Container):
    def __init__(
        self,
        steps: list[StepperStepCard],
        on_event=None,               # manejador global de eventos
        on_complete=None,            # manejador solo del evento final
        active_color=Colors.BLUE,
        inactive_color=Colors.GREY_700,
        completed_color=Colors.GREEN,
    ):
        super().__init__()

        self.steps = steps
        self.current_step = 0
        self.on_event = on_event
        self.on_complete = on_complete   # callback de finalización
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.completed_color = completed_color
        self.completed = False

        self.prev_btn = OutlinedButton(
            text="Previous",
            on_click=self.prev_step,
            disabled=self.current_step == 0,
        )

        self.next_btn = ElevatedButton(
            text="Next" if self.current_step < len(self.steps) - 1 else "Finish",
            on_click=self.next_step
        )

        self.padding = padding.all(25)
        self.border_radius = 12
        self.bgcolor = Colors.with_opacity(0.15, Colors.GREY_900)
        self.expand = True

        # Estructura visual
        self.step_indicators = self._build_indicators()
        self.step_content = self.steps[self.current_step]
        self.navigation = self._build_navigation()

        self.content_switcher = AnimatedSwitcher(
            self.step_content,
            transition=AnimatedSwitcherTransition.FADE,
            duration=400,
            expand=True,
        )

        self.content = Column(
            spacing=25,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.step_indicators,
                Divider(height=5, color=Colors.with_opacity(0.2, Colors.WHITE)),
                self.content_switcher,
                self.navigation,
            ],
        )

        # Evento inicial
        self._dispatch_event("change")

    # === Crear indicadores ===
    def _build_indicators(self):
        dots = []
        for i, step in enumerate(self.steps):
            is_active = i == self.current_step
            is_completed = i < self.current_step
            color = (
                self.completed_color if is_completed
                else self.active_color if is_active
                else self.inactive_color
            )

            dots.append(
                Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            width=36,
                            height=36,
                            alignment=alignment.center,
                            bgcolor=color,
                            border_radius=50,
                            content=Text(str(i + 1), color=Colors.WHITE, size=16, weight="bold"),
                        ),
                        Text(
                            step.title,
                            color=Colors.WHITE if is_active or is_completed else Colors.with_opacity(0.6, Colors.WHITE),
                            size=12,
                            weight="bold",
                            text_align=TextAlign.CENTER,
                        ),
                    ],
                )
            )

        return Row(
            alignment=MainAxisAlignment.SPACE_AROUND,
            expand=True,
            controls=dots,
        )

    # === Navegación ===
    def _build_navigation(self):
        return Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[self.prev_btn, self.next_btn],
        )

    # === Actualizar UI ===
    def _update_ui(self):
        self.step_indicators.controls = self._build_indicators().controls
        self.step_content = self.steps[self.current_step]
        self.navigation.controls = self._build_navigation().controls

        self.content.controls[2] = AnimatedSwitcher(
            self.step_content,
            transition=AnimatedSwitcherTransition.FADE,
            duration=400,
            expand=True,
        )
        self.update()

    # === Lógica de navegación ===
    def prev_step(self, e):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_ui()
            self._dispatch_event("prev")
            self._dispatch_event("change")

    def next_step(self, e):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._update_ui()
            self._dispatch_event("next")
            self._dispatch_event("change")
        else:
            self._on_complete()

    # === Finalización ===
    def _on_complete(self):
        self.completed = True
        self._dispatch_event("complete")

        # Ejecutar callback personalizado si existe
        if callable(self.on_complete):
            event = StepperEvent(
                type="complete",
                current_step=self.current_step,
                total_steps=len(self.steps),
                step=self.steps[self.current_step],
                is_first=False,
                is_last=True,
                completed=True,
                parent=self.parent
            )
            self.on_complete(event)

        # UI final por defecto (si no hay callback personalizado)
        if not callable(self.on_complete):
            self.content.controls = [
                Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        Icon(name=Icons.CHECK_CIRCLE, color=Colors.GREEN, size=90),
                        Text("¡Proccess Completed!", size=22, weight="bold"),
                        Text("Thanks For Complete All Steps", size=14, color=Colors.GREY_300),
                        FilledButton("Close", on_click=lambda e: self._close_stepper()),
                    ],
                )
            ]
            self.update()

    # === Despachar eventos ===
    def _dispatch_event(self, event_type: str):
        if callable(self.on_event):
            event = StepperEvent(
                type=event_type,
                current_step=self.current_step,
                total_steps=len(self.steps),
                step=self.steps[self.current_step],
                is_first=self.current_step == 0,
                is_last=self.current_step == len(self.steps) - 1,
                completed=self.completed,
                parent=self.parent
            )
            self.on_event(event)

    # === Cerrar ===
    def _close_stepper(self):
        if self.page and self in self.page.controls:
            self.page.controls.remove(self)
        else:
            self.page.controls.remove(self.parent)
        self.page.update()