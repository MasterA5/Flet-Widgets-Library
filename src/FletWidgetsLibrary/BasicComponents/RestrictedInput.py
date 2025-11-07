from flet import *
from dataclasses import dataclass
import re
from typing import Callable, Optional, Type


# ================================================================
# ✅ Evento personalizado
# ================================================================
@dataclass
class RestrictedInputEvent(ControlEvent):
    valid: bool
    pattern_name: str
    value: str

    def __init__(
        self,
        name: str,
        data: str,
        control: Control,
        page: Page,
        target: str,
        valid: bool,
        pattern_name: str,
        value: str,
    ):
        super().__init__(name=name, data=data, control=control, page=page, target=target)
        self.valid = valid
        self.pattern_name = pattern_name
        self.value = value

# ================================================================
# ✅ Interfaz base para validadores personalizados
# ================================================================
class BaseValidator:
    """Clase base para crear validadores personalizados."""

    def validate(self, value: str) -> bool:
        """Debe retornar True si es válido, False si no."""
        raise NotImplementedError("Implementa el método 'validate' en tu validador.")

    def error_message(self) -> str:
        """Mensaje a mostrar cuando el valor no es válido."""
        return "Entrada inválida."

# ================================================================
# ✅ Componente principal
# ================================================================
class RestrictedInput(TextField):
    # Patrones predefinidos (regex)
    PATTERNS = {
        "email": r"^[\w\.-]+@[\w\.-]+\.\w+$",
        "phone": r"^\+?\d{7,15}$",
        "number": r"^-?\d+(\.\d+)?$",
        "letters": r"^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$",
        "alphanumeric": r"^[A-Za-z0-9]+$",
        "password": r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{6,}$",
    }

    # Registro de validadores personalizados
    CUSTOM_VALIDATORS: dict[str, Type[BaseValidator]] = {}

    def __init__(self, pattern: str = None, on_validate=None, **kwargs):
        """
        pattern: nombre del patrón (regex o clase personalizada)
        on_validate: callback que recibe un RestrictedInputEvent
        """
        super().__init__(**kwargs)
        self.pattern = pattern
        self.on_validate = on_validate
        self.on_submit = self._validate_input
        self.border_color = Colors.GREY_400
        self.error_text = None

    # ================================================================
    # ✅ Método estático para registrar validadores personalizados
    # ================================================================
    @classmethod
    def register_validator(cls, name: str, validator_cls: Type[BaseValidator]):
        """Registra un validador personalizado (hereda de BaseValidator)."""
        if not issubclass(validator_cls, BaseValidator):
            raise TypeError("El validador debe heredar de BaseValidator")
        cls.CUSTOM_VALIDATORS[name] = validator_cls

    # ================================================================
    # ✅ Lógica de validación
    # ================================================================
    def _validate_input(self, e: ControlEvent):
        value = e.control.value.strip()
        valid = True
        pattern_name = self.pattern or "custom"
        error_msg = None

        # Si es un validador personalizado
        if self.pattern in self.CUSTOM_VALIDATORS:
            validator = self.CUSTOM_VALIDATORS[self.pattern]()
            valid = validator.validate(value)
            error_msg = validator.error_message()

        # Si es un patrón regex
        elif self.pattern in self.PATTERNS or isinstance(self.pattern, str):
            regex = self.PATTERNS.get(self.pattern, self.pattern or ".*")
            valid = re.fullmatch(regex, value) is not None
            if not valid:
                error_msg = f"Entrada inválida ({pattern_name})"

        # === Estilo visual ===
        if valid or value == "":
            self.border_color = Colors.GREEN_400 if value else Colors.GREY_400
            self.error_text = None
        else:
            self.border_color = Colors.RED_400
            self.error_text = error_msg or "Entrada inválida."

        # === Evento personalizado ===
        if self.on_validate:
            event = RestrictedInputEvent(
                name="validate",
                data=value,
                control=e.control,
                page=self.page,
                target=e.control.id if hasattr(e.control, "id") else None,
                valid=valid,
                pattern_name=pattern_name,
                value=value,
            )
            self.on_validate(event)

        self.update()

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
