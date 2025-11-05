from typing import List, Dict, Any, Union, Optional
from flet import *

class TreeNode:
    def __init__(self, name: str, children: List['TreeNode'] = None, expanded: bool = False, data: Any = None):
        self.name = name
        self.children = children or []
        self.expanded = expanded
        self.data = data
        self.parent = None
        
        # Establecer parent para cada hijo
        for child in self.children:
            child.parent = self

class TreeView(Column):
    def __init__(
        self, 
        nodes: List[TreeNode], 
        on_node_select: Optional[Any] = None, 
        on_node_expand: Optional[Any] = None,
        show_context_menu: bool = True
    ):
        super().__init__()
        self.nodes = nodes
        self.on_node_select = on_node_select
        self.on_node_expand = on_node_expand
        self.selected_node = None
        self.show_context_menu = show_context_menu
        self.build_tree()
    
    def build_tree(self):
        self.controls = []
        for node in self.nodes:
            self.controls.append(self.create_node_widget(node))

    def create_node_widget(self, node: TreeNode) -> Column:
        # Icono de expansión/colapso
        expand_icon = Icon(
            name=Icons.KEYBOARD_ARROW_RIGHT if not node.expanded else Icons.KEYBOARD_ARROW_DOWN,
            size=16,
            animate_rotation=Animation(300, AnimationCurve.EASE_IN_OUT)
        ) if node.children else Icon(name=Icons.FILE_COPY, size=16, opacity=0.7)
        
        # Texto del nodo
        node_text = Text(
            value=node.name,
            size=14,
            weight=FontWeight.NORMAL
        )
        
        # Contenedor principal del nodo
        node_content = Row(
            controls=[
                expand_icon,
                node_text,
            ],
            spacing=8,
            tight=True
        )
        
        # Si show_context_menu es True, agregamos el PopupMenuButton
        if self.show_context_menu:
            node_content.controls.append(
                PopupMenuButton(
                    icon=Icons.MORE_VERT,
                    icon_size=16,
                    menu_position=PopupMenuPosition.UNDER,
                    items=[
                        PopupMenuItem(
                            text="Renombrar",
                            icon=Icons.EDIT,
                            on_click=lambda e, n=node: self.on_rename_node(n)
                        ),
                        PopupMenuItem(
                            text="Eliminar", 
                            icon=Icons.DELETE,
                            on_click=lambda e, n=node: self.on_delete_node(n)
                        ),
                        PopupMenuItem(
                            text="Propiedades",
                            icon=Icons.INFO,
                            on_click=lambda e, n=node: self.on_properties_node(n)
                        ),
                        PopupMenuItem(),  # Separador
                        PopupMenuItem(
                            text="Nuevo archivo",
                            icon=Icons.INSERT_DRIVE_FILE,
                            on_click=lambda e, n=node: self.on_new_file(n)
                        ),
                        PopupMenuItem(
                            text="Nueva carpeta",
                            icon=Icons.CREATE_NEW_FOLDER,
                            on_click=lambda e, n=node: self.on_new_folder(n)
                        ),
                    ]
                )
            )
        
        # Container principal del nodo
        node_container = Container(
            content=node_content,
            padding=padding.only(left=20 * self.get_node_level(node), top=2, bottom=2),
            on_click=lambda e, n=node: self.on_node_click(e, n),
            on_long_press=lambda e, n=node: self.on_node_long_press(e, n),
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
    
    def get_node_level(self, node: TreeNode) -> int:
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
        
        self.page.update()
    
    def on_node_long_press(self, e: ControlEvent, node: TreeNode):
        """Maneja el long press para mostrar el menú contextual"""
        self.select_node(node)
        print(f"Long press en nodo: {node.name}")
        self.page.update()
    
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
            self.selected_node._node_text.color = None
            if hasattr(self.selected_node, '_node_container'):
                self.selected_node._node_container.update()
        
        # Aplicar nueva selección
        node._node_container.bgcolor = Colors.TRANSPARENT
        node._node_text.weight = FontWeight.BOLD
        node._node_text.color = Colors.WHITE
        node._node_container.update()
        
        self.selected_node = node
    
    def add_child_node(self, parent_node: TreeNode, new_node: TreeNode):
        """Agrega un nuevo nodo hijo y actualiza la UI"""
        parent_node.children.append(new_node)
        new_node.parent = parent_node
        
        # Crear el widget para el nuevo nodo
        new_node_widget = self.create_node_widget(new_node)
        
        # Agregar el nuevo widget a la columna de hijos
        parent_node._children_column.controls.append(new_node_widget)
        
        # Expandir el nodo padre si no está expandido
        if not parent_node.expanded:
            parent_node.expanded = True
            self.toggle_node(parent_node)
        
        # Actualizar la UI
        parent_node._children_column.update()
        if self.page:
            self.page.update()
    
    def remove_node(self, node: TreeNode):
        """Elimina un nodo y actualiza la UI"""
        if node.parent:
            # Remover de la lista de hijos del padre
            node.parent.children.remove(node)
            
            # Encontrar y remover el widget correspondiente
            for i, control in enumerate(node.parent._children_column.controls):
                if hasattr(control.controls[0].data, 'name') and control.controls[0].data.name == node.name:
                    node.parent._children_column.controls.pop(i)
                    break
            
            # Actualizar la UI
            node.parent._children_column.update()
            if self.page:
                self.page.update()
    
    # Métodos del menú contextual
    def on_rename_node(self, node: TreeNode):
        print(f"Renombrar nodo: {node.name}")
        self.show_rename_dialog(node)
    
    def on_delete_node(self, node: TreeNode):
        print(f"Eliminar nodo: {node.name}")
        self.show_delete_confirmation(node)
    
    def on_properties_node(self, node: TreeNode):
        print(f"Propiedades del nodo: {node.name}")
        self.show_properties_dialog(node)
    
    def on_new_file(self, parent_node: TreeNode):
        print(f"Nuevo archivo en: {parent_node.name}")
        self.show_new_file_dialog(parent_node)
    
    def on_new_folder(self, parent_node: TreeNode):
        print(f"Nueva carpeta en: {parent_node.name}")
        self.show_new_folder_dialog(parent_node)
    
    def show_new_file_dialog(self, parent_node: TreeNode):
        """Muestra un diálogo para crear nuevo archivo"""
        def create_file_action(e):
            if name_field.value.strip():
                new_file = TreeNode(
                    name=name_field.value.strip(),
                    children=[]  # Archivo sin hijos
                )
                self.add_child_node(parent_node, new_file)
                self.page.close(dlg)
                self.page.update()
                print(f"Archivo creado: {new_file.name}")
        
        
        name_field = TextField(
            label="Nombre del archivo",
            hint_text="ejemplo.txt",
            autofocus=True,
            prefix_icon=Icons.INSERT_DRIVE_FILE
        )
        
        dlg = AlertDialog(
            title=Text("Nuevo archivo"),
            content=Column([
                Text(f"Crear en: {parent_node.name}"),
                name_field
            ], tight=True),
            actions=[
                TextButton(
                    text="Cancelar", 
                    on_click=lambda e: (
                        setattr(
                            e.control.parent,
                            "open",
                            not e.control.parent.open
                        ),
                        e.control.parent.update(),
                        self.page.update()
                    )
                ),
                TextButton(
                    text="Crear", 
                    on_click=create_file_action
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def show_new_folder_dialog(self, parent_node: TreeNode):
        """Muestra un diálogo para crear nueva carpeta"""
        def create_folder_action(e):
            if name_field.value.strip():
                new_folder = TreeNode(
                    name=name_field.value.strip(),
                    children=[],  # Carpeta vacía
                    expanded=False
                )
                self.add_child_node(parent_node, new_folder)
                self.page.close(dlg)
                self.page.update()
                print(f"Carpeta creada: {new_folder.name}")
        
        name_field = TextField(
            label="Nombre de la carpeta",
            hint_text="nueva_carpeta",
            autofocus=True,
            prefix_icon=Icons.CREATE_NEW_FOLDER
        )
        
        dlg = AlertDialog(
            title=Text("Nueva carpeta"),
            content=Column([
                Text(f"Crear en: {parent_node.name}"),
                name_field
            ], tight=True),
            actions=[
                TextButton(
                    text="Cancelar", 
                    on_click=lambda e: (
                        setattr(
                            e.control.parent,
                            "open",
                            not e.control.parent.open
                        ),
                        e.control.parent.update(),
                        self.page.update()
                    )
                ),
                TextButton(
                    text="Crear", 
                    on_click=create_folder_action
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def show_rename_dialog(self, node: TreeNode):
        """Muestra un diálogo para renombrar el nodo"""
        def rename_dialog_action(e):
            if new_name_field.value.strip():
                node.name = new_name_field.value.strip()
                node._node_text.value = new_name_field.value.strip()
                node._node_text.update()
                self.page.close(dlg)
                self.page.update()
                print(f"Nodo renombrado a: {node.name}")
        
        def close_dialog(e):
            self.page.close(dlg)
            self.page.update()
        
        
        new_name_field = TextField(
            label="Nuevo nombre",
            value=node.name,
            autofocus=True
        )
        
        dlg = AlertDialog(
            title=Text("Renombrar nodo"),
            content=new_name_field,
            actions=[
                TextButton("Cancelar", on_click=close_dialog),
                TextButton("Aceptar", on_click=rename_dialog_action),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def show_delete_confirmation(self, node: TreeNode):
        """Muestra un diálogo de confirmación para eliminar el nodo"""
        def delete_action(e):
            self.remove_node(node)
            self.page.close(dlg)
            self.page.update()
            print(f"Nodo eliminado: {node.name}")
        
        def cancel_action(e):
            self.page.close(dlg)
            self.page.update()
        
        
        dlg = AlertDialog(
            title=Text("Confirmar eliminación"),
            content=Text(f"¿Estás seguro de que quieres eliminar '{node.name}'?"),
            actions=[
                TextButton("Cancelar", on_click=cancel_action),
                TextButton("Eliminar", on_click=delete_action),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def show_properties_dialog(self, node: TreeNode):
        """Muestra las propiedades del nodo"""
        def close_dialog(e):
            self.page.close(dlg)
            self.page.update()
        
        content = Column(
            controls=[
                Text(f"Nombre: {node.name}", size=16),
                Text(f"Tipo: {'Carpeta' if node.children else 'Archivo'}", size=14),
                Text(f"Hijos: {len(node.children)}", size=14, visible=len(node.children)>0),
                Text(f"Expandido: {'Sí' if node.expanded else 'No'}", size=14),
                Text(f"Nivel: {self.get_node_level(node)}", size=14),
            ]
        )
        
        dlg = AlertDialog(
            title=Text("Propiedades del nodo"),
            content=content,
            actions=[
                TextButton(
                    text="Cerrar", 
                    on_click=lambda e: (
                        setattr(
                            e.control.parent, 
                            "open", 
                            not e.control.parent.open
                        ),
                        e.control.update(),
                        self.page.update()
                    )
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def expand_all(self):
        def expand_recursive(nodes: List[TreeNode]):
            for node in nodes:
                if node.children:
                    node.expanded = True
                    self.toggle_node(node)
                    expand_recursive(node.children)
        
        expand_recursive(self.nodes)
        if self.page:
            self.page.update()
    
    def collapse_all(self):
        def collapse_recursive(nodes: List[TreeNode]):
            for node in nodes:
                if node.children:
                    node.expanded = False
                    self.toggle_node(node)
                    collapse_recursive(node.children)
        
        collapse_recursive(self.nodes)
        if self.page:
            self.page.update()