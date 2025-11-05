from typing import List, Dict, Any, Union
from flet import *

class TreeNode:
    def __init__(self, name: str, children: List[Any] = None, expanded: bool = False, data: Any = None):
        self.name = name
        self.children = children or []
        self.expanded = expanded
        self.data = data
        self.parent = None
        
        # Establecer parent para cada hijo
        for child in self.children:
            child.parent = self

class TreeView(Column):
    def __init__(self, nodes: List[TreeNode], on_node_select: OptionalEventCallable=None, on_node_expand: OptionalEventCallable=None):
        super().__init__()
        self.nodes = nodes
        self.on_node_select = on_node_select
        self.on_node_expand = on_node_expand
        self.selected_node = None
        self.build_tree()
    
    def build_tree(self):
        self.controls = []
        for node in self.nodes:
            self.controls.append(self.create_node_widget(node))
    
    def create_node_widget(self, node: TreeNode):
        # Icono de expansión/colapso
        expand_icon = Icon(
            name=Icons.KEYBOARD_ARROW_RIGHT if not node.expanded else Icons.KEYBOARD_ARROW_DOWN,
            size=16,
            animate_rotation=Animation(300, AnimationCurve.EASE_IN_OUT)
        ) if node.children else Icon(name=Icons.FILE_COPY, size=16, opacity=1)
        
        # Texto del nodo
        node_text = Text(
            value=node.name,
            size=14,
            weight=FontWeight.NORMAL
        )
        
        # Contenedor del nodo
        node_row = Row(
            controls=[
                expand_icon,
                node_text,
            ],
            spacing=8,
            tight=True
        )
        
        # Container principal del nodo
        node_container = Container(
            content=node_row,
            padding=padding.only(left=20 * self.get_node_level(node), top=2, bottom=2),
            on_click=lambda e, n=node: self.on_node_click(e, n),
            data=node
        )
        
        # Contenedor para hijos
        children_column = Column(
            controls=[self.create_node_widget(child) for child in node.children],
            spacing=0,
            visible=node.expanded
        )
        
        # Columna principal que contiene el nodo y sus hijos
        main_column = Column(
            controls=[node_container, children_column],
            spacing=0
        )
        
        # Guardar referencias para poder actualizarlas
        node._expand_icon = expand_icon
        node._children_column = children_column
        node._node_container = node_container
        node._node_text = node_text
        
        return main_column
    
    def get_node_level(self, node: TreeNode):
        level = 0
        current = node.parent
        while current:
            level += 1
            current = current.parent
        return level
    
    def on_node_click(self, e: ControlEvent, node: TreeNode):
        
        # Manejar expansión/colapso
        if node.children:
            node.expanded = not node.expanded
            self.toggle_node(node)
            if self.on_node_expand:
                self.on_node_expand(node)
        
        # Manejar selección
        self.select_node(node)
        if self.on_node_select:
            self.on_node_select(node)
        
        e.control.page.update()
    
    def toggle_node(self, node: TreeNode):
        if node.children:
            node._children_column.visible = node.expanded
            if node.expanded:
                node._expand_icon.name = Icons.KEYBOARD_ARROW_DOWN
            else:
                node._expand_icon.name = Icons.KEYBOARD_ARROW_RIGHT
            node._expand_icon.update()
            node._children_column.update()
    
    def select_node(self, node: TreeNode):
        # Remover selección anterior
        if self.selected_node:
            self.selected_node._node_container.bgcolor = None
            self.selected_node._node_text.weight = FontWeight.NORMAL
            self.selected_node._node_container.update()
        
        # Aplicar nueva selección
        node._node_container.bgcolor = Colors.TRANSPARENT
        node._node_text.weight = FontWeight.BOLD
        node._node_container.update()
        
        self.selected_node = node
    
    def expand_all(self):
        def expand_recursive(nodes):
            for node in nodes:
                if node.children:
                    node.expanded = True
                    self.toggle_node(node)
                    expand_recursive(node.children)
        
        expand_recursive(self.nodes)
        self.page.update()
    
    def collapse_all(self):
        def collapse_recursive(nodes):
            for node in nodes:
                if node.children:
                    node.expanded = False
                    self.toggle_node(node)
                    collapse_recursive(node.children)
        
        collapse_recursive(self.nodes)
        self.page.update()

def main(page: Page):
    page.title = "TreeView Example - Flet 0.28.3"
    page.theme_mode = ThemeMode.DARK
    page.padding = 20
    
    # Crear datos de ejemplo para el árbol
    root_nodes = [
        TreeNode(
            name="Proyectos", 
            children=[
                TreeNode(
                    name="Frontend", 
                    children=[
                        TreeNode("React App", expanded=False),
                        TreeNode("Vue.js Site", expanded=False),
                    ], 
                    expanded=False
                ),
                TreeNode(
                    name="Backend", 
                    children=[
                        TreeNode("API Rest", expanded=False),
                        TreeNode(
                            name="Microservicios", 
                            children=[
                                TreeNode("Auth Service"),
                                TreeNode("User Service"),
                                TreeNode("Payment Service"),
                            ], 
                            expanded=False
                        ),
                    ], 
                    expanded=False
                ),
            ], 
            expanded=True
        ),
        TreeNode(
            name="Documentación", 
            children=[
                TreeNode("Manual de usuario"),
                TreeNode("API Docs"),
                TreeNode("Guías de instalación"),
            ], 
            expanded=False
        ),
        TreeNode(
            name="Configuración", 
            children=[
                TreeNode("Desarrollo"),
                TreeNode("Producción"),
                TreeNode("Testing"),
            ], 
            expanded=True
        ),
    ]
    
    # Crear el TreeView
    tree_view = TreeView(nodes=root_nodes)
    
    # Botones de control
    controls_row = Row(
        controls=[
            ElevatedButton(
                "Expandir Todo",
                icon=Icons.EXPAND,
                on_click=lambda e: tree_view.expand_all()
            ),
            ElevatedButton(
                "Colapsar Todo", 
                icon=Icons.COMPRESS,
                on_click=lambda e: tree_view.collapse_all()
            ),
            ElevatedButton(
                "Nodo Seleccionado",
                icon=Icons.INFO,
                on_click=lambda e: print(f"Seleccionado: {tree_view.selected_node.name if tree_view.selected_node else 'Ninguno'}")
            ),
        ]
    )
    
    # Contenedor principal
    container = Container(
        content=Column(
            controls=[
                Text("TreeView Personalizado", size=20, weight=FontWeight.BOLD),
                controls_row,
                Container(
                    content=tree_view,
                    border=border.all(1, Colors.GREY_300),
                    border_radius=8,
                    padding=10,
                    width=400
                )
            ]
        ),
    )
    
    page.add(container)

if __name__ == "__main__":
    app(target=main)