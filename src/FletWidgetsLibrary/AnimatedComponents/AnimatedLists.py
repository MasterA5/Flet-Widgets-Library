from typing import List
from flet import (
    CrossAxisAlignment,
    AnimationCurve,
    Animation,
    Container,
    ListView,
    Control,
    margin,
    Colors,
    Scale,
    Icons,
    Icon,
    Text,
    Row,
)
import asyncio

class ListItem(Container):
    def __init__(
        self,
        index: int,
        content: Control,
        icon: str = Icons.CIRCLE,
        color: str = Colors.AMBER_700,
        delay: float = 0.01
    ):
        super().__init__()
        self.index = index
        self.content = content

        # Contenido visual
        self.content = Row(
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Icon(icon, size=12, color=color),
                Text(str(self.index)),
                Container(width=8),
                self.content
            ]
        )

        # Estilos visuales
        self.padding = 8
        self.border_radius = 10
        self.scale = Scale(0)  # comienza invisible
        self.animate_scale = Animation(300, AnimationCurve.DECELERATE)
        self.bgcolor = Colors.with_opacity(0.05, color)
        self.margin = margin.only(bottom=5)
        self.delay = delay

    def did_mount(self):
        """Se llama automáticamente cuando el control se monta en pantalla"""
        self.page.run_task(self._animate_did_mount)
        self.content.controls[0].visible=self.parent.data != "ordened-list"
        self.content.controls[0].update()
        self.content.controls[1].visible=self.parent.data == "ordened-list"
        self.content.controls[1].update()
        return super().did_mount()

    async def _animate_did_mount(self):
        """Anima la aparición del item"""
        await asyncio.sleep(self.delay * self.index)  # pequeño delay escalonado
        self.scale = Scale(1)
        self.update()

class UnorderedList(ListView):
    def __init__(
        self, 
        items: List[ListItem], 
        spacing: int = 5, 
        item_color: str = Colors.AMBER_700, 
        delay: float = 0.01
    ):
        super().__init__(spacing=spacing)
        self.items = items
        self.item_color = item_color
        self.data = "unordened-list"
        self.delay = delay
        self._build_list()

    def _build_list(self):
        self.controls.clear()
        for i, item in enumerate(self.items):
            self.controls.append(ListItem(i, item, color=self.item_color, delay=self.delay))

    def add_item(self, item: Control):
        """Agrega un nuevo elemento y anima solo ese"""
        index = len(self.items)
        self.items.append(item)

        new_item = ListItem(index, item, color=self.item_color, delay=self.delay)
        self.controls.append(new_item)
        self.update()  # actualiza la vista (solo nuevo item)
        self.page.run_task(new_item._animate_did_mount)

class OrdenedList(ListView):
    def __init__(self, items: List[Control], spacing: int = 5, item_color: str = Colors.AMBER_700, delay: float = 0.01):
        super().__init__(spacing=spacing)
        self.items = items
        self.item_color = item_color
        self.delay = delay
        self.data = "ordened-list"
        self._build_list()

    def _build_list(self):
        self.controls.clear()
        for i, item in enumerate(self.items):
            self.controls.append(ListItem(i, item, color=self.item_color, delay=self.delay))

    def add_item(self, item: Control):
        """Agrega un nuevo elemento y anima solo ese"""
        index = len(self.items)
        self.items.append(item)

        new_item = ListItem(index, item, color=self.item_color, delay=self.delay) if not isinstance(item, ListItem) else item
        self.controls.append(new_item)
        self.update()  # actualiza la vista (solo nuevo item)
        self.page.run_task(new_item._animate_did_mount)