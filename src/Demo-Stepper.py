from FletWidgetsLibrary import Stepper, StepperEvent, StepperStepCard
from flet import *

# === Ejemplo de uso ===
def main(page: Page):
    page.bgcolor = Colors.BLACK
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    # === Evento de finalización ===
    def handle_complete(ev: StepperEvent):
        dlg = AlertDialog(
            title=Text("🎉 Completed!"),
            content=Text("All Steps Make Compelte Succefull"),
            open=True,
            actions=[
                TextButton(
                    text="Close", 
                    on_click=lambda e: (
                        setattr(
                            page.overlay[0], 
                            "open", 
                            False
                        ), 
                        page.update()
                    )
                )
            ],
        )
        page.overlay.append(dlg)
        page.controls.remove(ev.parent)
        page.update()

    steps = [
        StepperStepCard(
            title="User", 
            description="Basic Data", 
            icon=Icons.PERSON, 
            content=Column(
                controls=[
                    TextField(label="Name"), 
                    TextField(label="Email")
                ]
            )
        ),
        StepperStepCard(
            title="Address", 
            description="Send Data", 
            icon=Icons.HOME, 
            content=Column(
                controls=[
                    TextField(label="City"), 
                    TextField(label="Street")
                ]
            )
        ),
        StepperStepCard(
            title="Confirm", 
            description="Validation", 
            icon=Icons.CHECKLIST, 
            content=Checkbox(label="I will confirm my data")
        )
    ]

    stepper = Stepper(steps=steps, on_complete=handle_complete)
    page.add(Container(width=500, content=stepper))


app(target=main)
