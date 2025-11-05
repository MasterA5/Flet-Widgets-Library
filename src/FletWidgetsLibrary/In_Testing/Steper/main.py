from typing import List, Any, Optional, Union
from dataclasses import dataclass
from flet import *

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

# === Componente de cada paso ===
class StepperStepCard(Container):
    def __init__(
        self,
        title: str,
        subtitle: str = "",
        description: str = "",
        icon: Union[Control, Icons] = Icons.CIRCLE,
        icon_color: Colors = Colors.WHITE,
        icon_size: int = 30,
        content: Control = None,
        color: str = Colors.BLUE_400,
        active_color: str = None,
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

        self.inner_content = content or Text(f"Contenido del paso: {title}", size=14)

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
        on_event=None,  # único manejador central de eventos
        active_color=Colors.BLUE,
        inactive_color=Colors.GREY_700,
        completed_color=Colors.GREEN,
    ):
        super().__init__()

        self.steps = steps
        self.current_step = 0
        self.on_event = on_event
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.completed_color = completed_color
        self.completed = False

        self.padding = padding.all(25)
        self.border_radius = 12
        self.bgcolor = Colors.with_opacity(0.15, Colors.GREY_900)
        self.expand = True

        # Estructura visual
        self.step_indicators = self._build_indicators()
        self.step_content = self.steps[self.current_step]
        self.navigation = self._build_navigation()

        self.content = Column(
            spacing=25,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.step_indicators,
                Divider(height=5, color=Colors.with_opacity(0.2, Colors.WHITE)),
                AnimatedSwitcher(
                    self.step_content,
                    transition=AnimatedSwitcherTransition.FADE,
                    duration=400,
                    expand=True,
                ),
                self.navigation,
            ],
        )

        # Dispara evento inicial
        self._dispatch_event("change")

    # === Crear los indicadores ===
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
            controls=[
                OutlinedButton(
                    text="Anterior",
                    on_click=self.prev_step,
                    disabled=self.current_step == 0,
                ),
                ElevatedButton(
                    text="Siguiente" if self.current_step < len(self.steps) - 1 else "Finalizar",
                    on_click=self.next_step,
                ),
            ],
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

    # === Evento final ===
    def _on_complete(self):
        self.completed = True
        self._dispatch_event("complete")
        self.content.controls = [
            Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    Icon(name=Icons.CHECK_CIRCLE, color=Colors.GREEN, size=90),
                    Text("¡Proceso completado!", size=22, weight="bold"),
                    Text("Gracias por completar todos los pasos.", size=14, color=Colors.GREY_300),
                    FilledButton("Cerrar", on_click=lambda e: self._close_stepper()),
                ],
            )
        ]
        self.update()

    # === Despachar eventos ===
    def _dispatch_event(self, event_type: str):
        """Envía un StepperEvent con todos los datos actuales."""
        if callable(self.on_event):
            event = StepperEvent(
                type=event_type,
                current_step=self.current_step,
                total_steps=len(self.steps),
                step=self.steps[self.current_step],
                is_first=self.current_step == 0,
                is_last=self.current_step == len(self.steps) - 1,
                completed=self.completed,
            )
            self.on_event(event)

    # === Cerrar ===
    def _close_stepper(self):
        if self.page and self in self.page.controls:
            self.page.controls.remove(self)
        else:
            self.page.controls.remove(self.parent)
        self.page.update()


# === Ejemplo de uso ===
def main(page: Page):
    page.title = "Stepper con eventos"
    page.bgcolor = Colors.BLACK
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # === Manejo de eventos centralizado ===
    def handle_stepper_event(ev: StepperEvent):
        print(f"📢 Evento: {ev.type.upper()} | Paso {ev.current_step + 1}/{ev.total_steps}")
        if ev.type == "complete":
            print("Complete")

    steps = [
        StepperStepCard(
            title="Usuario",
            description="Ingrese nombre y correo.",
            subtitle="Ingrese su usuario",
            icon=Icons.PERSON,
            content=Column([
                TextField(label="Nombre"),
                TextField(label="Correo"),
            ]),
        ),
        StepperStepCard(
            title="Dirección",
            description="Complete los datos de envío.",
            icon=Icons.HOME,
            content=Column([
                TextField(label="Ciudad"),
                TextField(label="Calle"),
            ]),
        ),
        StepperStepCard(
            title="Confirmación",
            description="Verifique y confirme.",
            icon=Icons.CHECKLIST,
            content=Checkbox(label="Confirmo mis datos"),
        ),
    ]

    stepper = Stepper(steps=steps, on_event=handle_stepper_event)
    page.add(Container(width=500, content=stepper))


if __name__ == "__main__":
    app(target=main)
