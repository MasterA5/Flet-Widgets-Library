from flet import *


# === Componente para cada paso ===
class StepperStepCard(Container):
    def __init__(
        self,
        title: str,
        subtitle: str = "",
        description: str = "",
        icon: str = Icons.CIRCLE,
        content: Control = None,
        color: str = Colors.BLUE_400,
        active_color: str = None,
        border_radius: int = 12,
        padding_value: int = 15,
        show_divider: bool = True,
        compact: bool = False,
    ):
        super().__init__()

        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.icon = icon
        self.color = color
        self.active_color = active_color or color
        self.border_radius = border_radius
        self.show_divider = show_divider
        self.compact = compact

        self._inner_content = content or Text(f"Contenido del paso: {title}", size=14)

        self.bgcolor = Colors.with_opacity(0.1, Colors.BLUE_GREY_900)
        self.border_radius = border_radius
        self.padding = padding.all(padding_value)
        self.expand = True

        header = Row(
            alignment=MainAxisAlignment.START,
            spacing=10,
            controls=[
                Icon(name=self.icon, color=self.active_color, size=30),
                Column(
                    spacing=1,
                    controls=[
                        Text(self.title, size=18, weight="bold", color=Colors.WHITE),
                        *([Text(self.subtitle, size=13, color=Colors.GREY_400)] if self.subtitle else []),
                    ],
                ),
            ],
        )

        body = Column(
            spacing=10,
            controls=[
                Text(self.description, color=Colors.GREY_300, size=13),
                self._inner_content,
            ],
        )

        self.content = Column(
            spacing=10,
            controls=[
                header,
                *([Divider(color=Colors.with_opacity(0.15, Colors.WHITE))] if self.show_divider else []),
                body if not self.compact else self._inner_content,
            ],
        )


# === Stepper principal ===
class Stepper(Container):
    def __init__(
        self,
        steps: list[StepperStepCard],
        on_complete=None,
        on_step_change=None,
        active_color=Colors.BLUE,
        inactive_color=Colors.GREY_700,
        completed_color=Colors.GREEN_500,
        connector_color=Colors.with_opacity(0.3, Colors.WHITE),
        orientation: str = "horizontal",  # o "vertical"
        shadow_strength: float = 0.25,
        transition: AnimatedSwitcherTransition = AnimatedSwitcherTransition.FADE,
        transition_duration: int = 400,
        show_labels: bool = True,
    ):
        super().__init__()
        self.steps = steps
        self.current_step = 0
        self.on_complete = on_complete
        self.on_step_change = on_step_change
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.completed_color = completed_color
        self.connector_color = connector_color
        self.orientation = orientation
        self.transition = transition
        self.transition_duration = transition_duration
        self.show_labels = show_labels
        self.completed = False

        # === Estilo general ===
        self.padding = padding.all(25)
        self.border_radius = 14
        self.bgcolor = Colors.with_opacity(0.15, Colors.GREY_900)
        self.shadow = BoxShadow(blur_radius=12, color=Colors.with_opacity(shadow_strength, Colors.BLACK))
        self.expand = True

        # === Estructura inicial ===
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
                    transition=self.transition,
                    duration=self.transition_duration,
                    expand=True,
                ),
                self.navigation,
            ],
        )

    # === Indicadores de pasos ===
    def _build_indicators(self):
        controls = []
        for i, step in enumerate(self.steps):
            is_active = i == self.current_step
            is_completed = i < self.current_step

            color = (
                self.completed_color if is_completed
                else self.active_color if is_active
                else self.inactive_color
            )

            step_icon = Container(
                width=38,
                height=38,
                bgcolor=color,
                border_radius=50,
                alignment=alignment.center,
                content=Icon(
                    name=Icons.CHECK if is_completed else Icons.CIRCLE,
                    color=Colors.WHITE,
                    size=20,
                ),
            )

            label = (
                Text(
                    step.title,
                    size=12,
                    color=Colors.WHITE if is_active or is_completed else Colors.with_opacity(0.6, Colors.WHITE),
                    weight="bold",
                    text_align=TextAlign.CENTER,
                )
                if self.show_labels
                else None
            )

            step_column = Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[step_icon] + ([label] if label else []),
            )

            controls.append(step_column)

            if i < len(self.steps) - 1:
                controls.append(
                    Container(
                        width=40 if self.orientation == "horizontal" else 4,
                        height=4 if self.orientation == "horizontal" else 40,
                        bgcolor=self.connector_color,
                    )
                )

        return Row(
            alignment=MainAxisAlignment.CENTER if self.orientation == "horizontal" else MainAxisAlignment.START,
            vertical_alignment=CrossAxisAlignment.CENTER,
            wrap=False,
            controls=controls,
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

    # === Actualizar interfaz ===
    def _update_ui(self):
        if self.completed:
            return

        if callable(self.on_step_change):
            self.on_step_change(self.current_step)

        self.step_indicators.controls = self._build_indicators().controls
        self.step_content = self.steps[self.current_step]
        self.navigation.controls = self._build_navigation().controls

        if len(self.content.controls) >= 3:
            self.content.controls[2] = AnimatedSwitcher(
                self.step_content,
                transition=self.transition,
                duration=self.transition_duration,
                expand=True,
            )
        self.update()

    # === Navegación lógica ===
    def prev_step(self, e):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_ui()

    def next_step(self, e):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._update_ui()
        else:
            if callable(self.on_complete):
                self.on_complete()
            self._on_complete()

    # === Pantalla final ===
    def _on_complete(self):
        self.completed = True
        self.content.controls.clear()
        self.content.controls.append(
            Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    Icon(name=Icons.CHECK_CIRCLE, color=Colors.GREEN, size=90),
                    Text("¡Proceso completado!", size=24, weight="bold"),
                    Text("Gracias por completar todos los pasos.", size=15, color=Colors.GREY_300),
                    FilledButton("Cerrar", on_click=lambda e: self._close_stepper()),
                ],
            )
        )
        self.update()

    def _close_stepper(self):
        if self.page and self in self.page.controls:
            self.page.controls.remove(self)
        else:
            self.page.controls.remove(self.parent)
        self.page.update()


# === Ejemplo ===
def main(page: Page):
    page.title = "Stepper Pro - Flet UI"
    page.bgcolor = Colors.BLACK
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.scroll = "adaptive"

    def handle_step_change(step_index):
        print(f"➡️ Paso actual: {step_index + 1}")

    def handle_complete():
        print("✅ Stepper finalizado correctamente.")

    steps = [
        StepperStepCard(
            title="Datos personales",
            subtitle="Información básica",
            description="Ingrese su nombre y correo electrónico.",
            icon=Icons.PERSON,
            content=Column([
                TextField(label="Nombre completo"),
                TextField(label="Correo electrónico")
            ]),
        ),
        StepperStepCard(
            title="Dirección",
            subtitle="Datos de envío",
            description="Complete los datos de su domicilio.",
            icon=Icons.HOME,
            content=Column([
                TextField(label="Calle y número"),
                TextField(label="Ciudad"),
                TextField(label="Código postal")
            ]),
        ),
        StepperStepCard(
            title="Confirmación",
            description="Verifique los datos antes de continuar.",
            icon=Icons.CHECKLIST,
            content=Checkbox(label="Confirmo que mis datos son correctos"),
        ),
        StepperStepCard(
            title="Aceptación",
            subtitle="Último paso",
            description="Acepte los términos y condiciones para finalizar.",
            icon=Icons.GAVEL,
            content=Checkbox(label="Acepto los términos y condiciones"),
        ),
    ]

    stepper = Stepper(
        steps=steps,
        on_complete=handle_complete,
        on_step_change=handle_step_change,
        orientation="horizontal",
        show_labels=True,
        transition=AnimatedSwitcherTransition.SCALE,
        active_color=Colors.CYAN,
    )

    page.add(Container(width=600, content=stepper))


if __name__ == "__main__":
    app(target=main)
