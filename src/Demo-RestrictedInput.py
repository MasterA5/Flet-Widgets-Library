from FletWidgetsLibrary import RestrictedInput, BaseValidator, RestrictedInputEvent
from flet import *
import re

# ================================================================
# ✅ Ejemplo de validador personalizado
# ================================================================
class DNIValidator(BaseValidator):
    """Valida que un DNI argentino tenga 7 u 8 dígitos."""

    def validate(self, value: str) -> bool:
        return bool(re.fullmatch(r"^\d{7,8}$", value))

    def error_message(self) -> str:
        return "El DNI debe tener entre 7 y 8 números."

# ================================================================
# ✅ Ejemplo de uso
# ================================================================
import time
def main(page: Page):
    page.title = "RestrictedInput Extensible Demo"

    # Registrar el validador personalizado
    RestrictedInput.register_validator("dni", DNIValidator)

    def handle_validation(e: RestrictedInputEvent):
        print(f"[{e.pattern_name}] -> '{e.value}' válido? {e.valid}")

    email_input = RestrictedInput(
        label="Correo electrónico",
        pattern="email",
        on_validate=handle_validation,
        width=300,
    )

    dni_input = RestrictedInput(
        label="DNI Argentino",
        pattern="dni",
        on_validate=handle_validation,
        width=300,
    )

    password_input = RestrictedInput(
        label="Contraseña segura",
        pattern="password",
        password=True,
        can_reveal_password=True,
        on_validate=handle_validation,
        width=300,
    )

    page.add(email_input, dni_input, password_input)


if __name__ == "__main__":
    app(target=main)
