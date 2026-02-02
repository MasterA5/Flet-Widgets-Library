from typing import List, Any, Optional, Callable, Dict, Union
from flet import (
    MainAxisAlignment,
    PopupMenuPosition,
    PopupMenuButton,
    AnimationCurve,
    PopupMenuItem,
    ControlEvent,
    AlertDialog,
    BottomSheet,
    TextButton,
    FontWeight,
    IconValue,
    Animation,
    TextField,
    Container,
    padding,
    Column,
    Colors,
    Icons,
    Icon,
    Text,
    Row,
)

class TreeNode:
    def __init__(
        self, 
        id: str = None,
        name: str = None, 
        children: List['TreeNode'] = None, 
        expanded: bool = False, 
        data: Any = None,
        icon: IconValue = None,
        content: Any = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        selectable: bool = True,
        draggable: bool = False,
        droppable: bool = False
    ):
        self.id = id or name  # Use name as ID if id not provided
        self.name = name
        self.children = children or []
        self.expanded = expanded
        self.data = data
        self.icon = icon
        self.content = content
        self.tags = tags or []
        self.metadata = metadata or {}
        self.selectable = selectable
        self.draggable = draggable
        self.droppable = droppable
        self.parent = None
        
        # Set parent for each child
        for child in self.children:
            child.parent = self

    def change_icon(self, new_icon: IconValue) -> None:
        self.icon = new_icon

class TreeViewConfig:
    def __init__(
        self,
        default_folder_icon: IconValue = Icons.FOLDER,
        default_file_icon: IconValue = Icons.INSERT_DRIVE_FILE,
        indent_size: int = 20,
        animation_duration: int = 300,
        show_expand_icons: bool = True,
        show_icons: bool = True,
        show_context_menu: bool = True,
        multi_select: bool = False,
        allow_drag_drop: bool = False,
        selection_color: str = Colors.BLUE_200,
        selection_text_color: str = Colors.WHITE,
        hover_color: str = Colors.TRANSPARENT,
        custom_icons: Dict[str, IconValue] = None,
        node_height: int = 32,
    ):
        self.default_folder_icon = default_folder_icon
        self.default_file_icon = default_file_icon
        self.indent_size = indent_size
        self.animation_duration = animation_duration
        self.show_expand_icons = show_expand_icons
        self.show_icons = show_icons
        self.show_context_menu = show_context_menu
        self.multi_select = multi_select
        self.allow_drag_drop = allow_drag_drop
        self.selection_color = selection_color
        self.selection_text_color = selection_text_color
        self.hover_color = hover_color
        self.custom_icons = custom_icons or {}
        self.node_height = node_height

class TreeView(Column):
    def __init__(
        self, 
        nodes: List[TreeNode] = None,
        config: TreeViewConfig = None,
        # Main callbacks
        on_node_select: Optional[Callable[[TreeNode], None]] = None,
        on_node_expand: Optional[Callable[[TreeNode], None]] = None,
        on_node_collapse: Optional[Callable[[TreeNode], None]] = None,
        # Context callbacks
        on_rename: Optional[Callable[[TreeNode, str], bool]] = None,
        on_delete: Optional[Callable[[TreeNode], bool]] = None,
        on_properties: Optional[Callable[[TreeNode], None]] = None,
        on_new_item: Optional[Callable[[TreeNode, str, str], Optional[TreeNode]]] = None,
        # Callbacks
        on_drag_start: Optional[Callable[[TreeNode], bool]] = None,
        on_drop: Optional[Callable[[TreeNode, TreeNode], bool]] = None,
        on_double_click: Optional[Callable[[TreeNode], None]] = None,
        on_right_click: Optional[Callable[[TreeNode, ControlEvent], None]] = None,
        # Customizing the context menu
        context_menu_items: List[Dict[str, Any]] = None,
        custom_node_renderer: Optional[Callable[[TreeNode, 'TreeView'], Any]] = None,
    ):
        super().__init__()
        self.nodes = nodes or []
        self.config = config or TreeViewConfig()
        self.on_node_select = on_node_select
        self.on_node_expand = on_node_expand
        self.on_node_collapse = on_node_collapse
        self.on_rename = on_rename
        self.on_delete = on_delete
        self.on_properties = on_properties
        self.on_new_item = on_new_item
        self.on_drag_start = on_drag_start
        self.on_drop = on_drop
        self.on_double_click = on_double_click
        self.on_right_click = on_right_click
        self.custom_node_renderer = custom_node_renderer
        self.context_menu_items = context_menu_items or self._get_default_context_menu_items()
        
        self.selected_nodes = [] if self.config.multi_select else None
        self.selected_node = None
        self.hovered_node = None
        
        self.build_tree()
    
    def _get_default_context_menu_items(self) -> List[Dict[str, Any]]:
        """Returns the default items from the context menu."""
        return [
            {
                "text": "Rename",
                "icon": Icons.EDIT,
                "action": self._on_rename_node,
                "enabled": lambda n: True,
            },
            {
                "text": "Delete",
                "icon": Icons.DELETE,
                "action": self._on_delete_node,
                "enabled": lambda n: n.parent is not None,  # Do not remove root
            },
            {
                "text": "Properties",
                "icon": Icons.INFO,
                "action": self._on_properties_node,
                "enabled": lambda n: True,
            },
            None,  # Separator
            {
                "text": "New Item",
                "icon": Icons.ADD,
                "action": self._on_new_item,
                "enabled": lambda n: True,
            }
        ]
    
    def build_tree(self):
        self.controls = []
        for node in self.nodes:
            self.controls.append(self.create_node_widget(node))
    
    def get_node_icon(self, node: TreeNode) -> IconValue:
        """Get the appropriate icon for the node"""
        if node.icon:
            return node.icon
        
        # Check custom icons by type/tag
        for tag in node.tags:
            if tag in self.config.custom_icons:
                return self.config.custom_icons[tag]
        
        # Default icon based on whether it has children
        if node.children:
            return self.config.default_folder_icon
        else:
            return self.config.default_file_icon
    
    def create_node_widget(self, node: TreeNode) -> Column:
        # Determine whether to show the expansion icon
        has_children = bool(node.children)
        
        # Expansion/collapse icon
        expand_icon = None
        if self.config.show_expand_icons and has_children:
            expand_icon = Icon(
                name=Icons.KEYBOARD_ARROW_RIGHT if not node.expanded else Icons.KEYBOARD_ARROW_DOWN,
                size=16,
                animate_rotation=Animation(
                    self.config.animation_duration, 
                    AnimationCurve.EASE_IN_OUT
                )
            )
        elif self.config.show_expand_icons:
            expand_icon = Icon(name=Icons.REMOVE, size=16, opacity=0.3)
        
        # Node icon
        node_icon = None
        if self.config.show_icons:
            node_icon = Icon(
                self.get_node_icon(node), 
                size=20,
                visible=node.icon is not None or self.config.show_icons
            )
        
        # Custom node rendering
        if self.custom_node_renderer:
            node_content = self.custom_node_renderer(node, self)
        else:
            node_content = self._create_default_node_content(node, expand_icon, node_icon)
        
        # Main container of the node
        node_container = Container(
            content=node_content,
            padding=padding.only(
                left=self.get_node_level(node) * self.config.indent_size,
                top=2,
                bottom=2,
                right=8
            ),
            height=self.config.node_height,
            on_click=lambda e, n=node: self.on_node_click(e, n),
            on_hover=lambda e, n=node: self.on_node_hover(e, n),
            on_long_press=lambda e, n=node: self.on_node_long_press(e, n),
            data=node,
            bgcolor=Colors.TRANSPARENT,
        )
        
        # Configure drag & drop events if enabled
        if self.config.allow_drag_drop:
            if node.draggable:
                node_container.on_drag_start = lambda e, n=node: self.on_drag_start_handler(e, n)
            if node.droppable:
                node_container.on_drop = lambda e, n=node: self.on_drop_handler(e, n)
                node_container.on_drag_over = lambda e, n=node: self.on_drag_over_handler(e, n)
                node_container.on_drag_leave = lambda e, n=node: self.on_drag_leave_handler(e, n)
        
        # Container for children
        children_column = Column(
            controls=[self.create_node_widget(child) for child in node.children],
            spacing=0,
            visible=node.expanded
        )
        
        # Main column containing the node and its children
        main_column = Column(
            controls=[node_container, children_column],
            spacing=0
        )
        
        # Save references so you can update them.
        node._expand_icon = expand_icon
        node._children_column = children_column
        node._node_container = node_container
        node._node_content = node_content
        
        return main_column
    
    def _create_default_node_content(self, node: TreeNode, expand_icon: Icon = None, node_icon: Icon = None) -> Row:
        """Create the default content for a node"""
        controls = []
        
        # Add expansion icon
        if expand_icon:
            controls.append(expand_icon)
        
        # Add node icon
        if node_icon:
            controls.append(node_icon)
        
        # Node text
        node_text = Text(
            value=node.name,
            size=14,
            weight=FontWeight.NORMAL
        )
        controls.append(node_text)
        
        # Additional custom content
        if node.content:
            if isinstance(node.content, list):
                controls.extend(node.content)
            else:
                controls.append(node.content)
        
        # Context menu if enabled
        if self.config.show_context_menu:
            controls.append(self._create_context_menu_button(node))
        
        return Row(controls=controls, spacing=8, tight=True)
    
    def _create_context_menu_button(self, node: TreeNode) -> PopupMenuButton:
        """Create the context menu button"""
        menu_items = []
        
        for item_config in self.context_menu_items:
            if item_config is None:  # Separator
                menu_items.append(PopupMenuItem())
                continue
            
            # Check if the item is enabled
            enabled = item_config.get("enabled", lambda n: True)(node)
            
            menu_items.append(
                PopupMenuItem(
                    text=item_config["text"],
                    icon=item_config.get("icon"),
                    on_click=lambda e, n=node, action=item_config["action"]: action(n),
                    disabled=not enabled,
                )
            )
        
        return PopupMenuButton(
            icon=Icons.MORE_VERT,
            icon_size=16,
            menu_position=PopupMenuPosition.UNDER,
            items=menu_items
        )
    
    def get_node_level(self, node: TreeNode) -> int:
        level = 0
        current = node.parent
        while current:
            level += 1
            current = current.parent
        return level
    
    def on_node_click(self, e: ControlEvent, node: TreeNode):
        # Double-click operation
        if e.data == "2":  # Double click
            if self.on_double_click:
                self.on_double_click(node)
            return
        
        # Manage expand/collapse
        if node.children:
            was_expanded = node.expanded
            node.expanded = not node.expanded
            self.toggle_node(node)
            
            if node.expanded and self.on_node_expand:
                self.on_node_expand(node)
            elif not node.expanded and self.on_node_collapse:
                self.on_node_collapse(node)
        
        # Handle selection if the node is selectable
        if node.selectable:
            self.select_node(node, e.ctrl if hasattr(e, 'ctrl') else False)
        
        if self.page:
            self.page.update()
    
    def on_node_hover(self, e: ControlEvent, node: TreeNode):
        """Maneja el hover sobre un nodo"""
        if e.data == "true":  # Mouse enter
            self.hovered_node = node
            if hasattr(node, '_node_container'):
                node._node_container.bgcolor = self.config.hover_color
                node._node_container.update()
        else:  # Mouse leave
            if self.hovered_node == node:
                self.hovered_node = None
            # Only remove hover if it is not selected
            if node not in (self.selected_nodes or [] if self.selected_nodes else [self.selected_node]):
                if hasattr(node, '_node_container'):
                    node._node_container.bgcolor = Colors.TRANSPARENT
                    node._node_container.update()
    
    def on_node_long_press(self, e: ControlEvent, node: TreeNode):
        """Handles long click to display context menu"""
        if self.on_right_click:
            self.on_right_click(node, e)
        
        # Select the node
        self.select_node(node)
        
        if self.page:
            self.page.update()
    
    def toggle_node(self, node: TreeNode):
        if node.children and hasattr(node, '_children_column'):
            node._children_column.visible = node.expanded
            if node._expand_icon:
                if node.expanded:
                    node._expand_icon.name = Icons.KEYBOARD_ARROW_DOWN
                else:
                    node._expand_icon.name = Icons.KEYBOARD_ARROW_RIGHT
                node._expand_icon.update()
            node._children_column.update()
    
    def select_node(self, node: TreeNode, multi_select: bool = False):
        if not node.selectable:
            return
        
        if self.config.multi_select:
            multi_select = True  # Force multi-selection if enabled
        
        if multi_select:
            if self.selected_nodes is None:
                self.selected_nodes = []
            
            if node in self.selected_nodes:
                # Deselect
                self.selected_nodes.remove(node)
                self._update_node_appearance(node, selected=False)
            else:
                # Select
                self.selected_nodes.append(node)
                self._update_node_appearance(node, selected=True)
            
            if self.on_node_select:
                self.on_node_select(node, self.selected_nodes)
        else:
            # Unique selection
            if self.selected_nodes:
                # Clear previous multiple selection
                for selected_node in self.selected_nodes:
                    self._update_node_appearance(selected_node, selected=False)
                self.selected_nodes = None
            
            # Deselect previous node
            if self.selected_node:
                self._update_node_appearance(self.selected_node, selected=False)
            
            # Select new node
            self.selected_node = node
            self._update_node_appearance(node, selected=True)
            
            if self.on_node_select:
                self.on_node_select(node)
    
    def _update_node_appearance(self, node: TreeNode, selected: bool = True):
        """Updates the node's appearance based on its selection state"""
        if not hasattr(node, '_node_container'):
            return
        
        if selected:
            node._node_container.bgcolor = self.config.selection_color
            # Find and update the text
            for control in node._node_content.controls:
                if isinstance(control, Text):
                    control.weight = FontWeight.BOLD
                    control.color = self.config.selection_text_color
                    break
        else:
            node._node_container.bgcolor = Colors.TRANSPARENT
            # Find and update the text
            for control in node._node_content.controls:
                if isinstance(control, Text):
                    control.weight = FontWeight.NORMAL
                    control.color = None
                    break
        
        node._node_container.update()
    
    # Methods for node manipulation
    def add_node(self, parent_node: TreeNode, new_node: TreeNode, index: int = None):
        """Add a new child node and update the UI"""
        if parent_node is None:  # Add to root
            self.nodes.append(new_node)
            self.controls.append(self.create_node_widget(new_node))
        else:
            if index is None:
                parent_node.children.append(new_node)
            else:
                parent_node.children.insert(index, new_node)
            
            new_node.parent = parent_node
            
            # Create the widget for the new node
            new_node_widget = self.create_node_widget(new_node)
            
            # Add the new widget to the child column
            if index is None:
                parent_node._children_column.controls.append(new_node_widget)
            else:
                parent_node._children_column.controls.insert(index, new_node_widget)
            
            # Expand the parent node if it is not expanded
            if not parent_node.expanded and parent_node.children:
                parent_node.expanded = True
                self.toggle_node(parent_node)
        
        if self.page:
            self.page.update()
        
        return new_node
    
    def remove_node(self, node: TreeNode):
        """Remove a node and update the UI"""
        if node.parent:
            # Remove from parent's children list
            node.parent.children.remove(node)
            
            # Find and remove the corresponding widget
            for i, control in enumerate(node.parent._children_column.controls):
                if hasattr(control.controls[0].data, 'id') and control.controls[0].data.id == node.id:
                    node.parent._children_column.controls.pop(i)
                    break
            
            # Update UI
            node.parent._children_column.update()
        else:
            # Is root node
            for i, n in enumerate(self.nodes):
                if n.id == node.id:
                    self.nodes.pop(i)
                    self.controls.pop(i)
                    break
        
        if self.page:
            self.page.update()
    
    def update_node(self, node: TreeNode, **kwargs):
        """Update the properties of a node"""
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)
        
        # Recreate the widget if necessary
        if node.parent:
            # Find the index of the node in the children of the parent
            index = node.parent.children.index(node)
            
            # Recreate the widget
            new_widget = self.create_node_widget(node)
            
            # Replace the old widget
            node.parent._children_column.controls[index] = new_widget
            node.parent._children_column.update()
        
        if self.page:
            self.page.update()
    
    # Context menu methods
    def _on_rename_node(self, node: TreeNode):
        if self.on_rename:
            # Use custom callback
            self.show_rename_dialog(node)
        else:
            self.show_rename_dialog(node)
    
    def _on_delete_node(self, node: TreeNode):
        if self.on_delete:
            # Use custom callback
            if self.on_delete(node):
                self.remove_node(node)
        else:
            self.show_delete_confirmation(node)
    
    def _on_properties_node(self, node: TreeNode):
        if self.on_properties:
            self.on_properties(node)
        else:
            self.show_properties_dialog(node)
    
    def _on_new_item(self, parent_node: TreeNode):
        if self.on_new_item:
            # The callback should return the new node or None.
            new_node = self.on_new_item(parent_node, "item", "Item")
            if new_node:
                self.add_node(parent_node, new_node)
        else:
            self.show_new_item_dialog(parent_node)
    
    # Drag & drop handlers
    def on_drag_start_handler(self, e: ControlEvent, node: TreeNode):
        if self.on_drag_start:
            if not self.on_drag_start(node):
                return
        
        # Configure drag data
        e.data = {
            "node_id": node.id,
            "node_name": node.name,
        }
    
    def on_drop_handler(self, e: ControlEvent, target_node: TreeNode):
        if not target_node.droppable:
            return
        
        # Get drag data
        dragged_node_id = e.data.get("node_id")
        if not dragged_node_id:
            return
        
        # Find the dragged node
        dragged_node = self.find_node_by_id(dragged_node_id)
        if not dragged_node or dragged_node == target_node:
            return
        
        # Verify callback
        if self.on_drop:
            if not self.on_drop(dragged_node, target_node):
                return
        
        # Move node
        self.move_node(dragged_node, target_node)
    
    def on_drag_over_handler(self, e: ControlEvent, node: TreeNode):
        if node.droppable:
            e.accept = True
            if hasattr(node, '_node_container'):
                node._node_container.bgcolor = Colors.TRANSPARENT
                node._node_container.update()
    
    def on_drag_leave_handler(self, e: ControlEvent, node: TreeNode):
        if hasattr(node, '_node_container'):
            # Restore original color (considering selection/hover)
            if node in (self.selected_nodes or [] if self.selected_nodes else [self.selected_node]):
                node._node_container.bgcolor = self.config.selection_color
            elif node == self.hovered_node:
                node._node_container.bgcolor = self.config.hover_color
            else:
                node._node_container.bgcolor = Colors.TRANSPARENT
            node._node_container.update()
    
    def move_node(self, node: TreeNode, new_parent: TreeNode):
        """Move a node to a new parent"""
        # Delete from current parent
        old_parent = node.parent
        if old_parent:
            old_parent.children.remove(node)
            # Update the parent UI of the old parent
            self._refresh_node_children(old_parent)
        else:
            # is root node
            self.nodes.remove(node)
            self.controls = []
            self.build_tree()
        
        # Add new parent
        new_parent.children.append(node)
        node.parent = new_parent
        
        # Update the new parent's UI
        self._refresh_node_children(new_parent)
        
        # Expand the new parent if it is not already expanded
        if not new_parent.expanded:
            new_parent.expanded = True
            self.toggle_node(new_parent)
        
        if self.page:
            self.page.update()
    
    def _refresh_node_children(self, node: TreeNode):
        """Recreates the child widgets of a node"""
        if not hasattr(node, '_children_column'):
            return
        
        node._children_column.controls = [
            self.create_node_widget(child) for child in node.children
        ]
        node._children_column.update()
    
    # Useful methods
    def find_node_by_id(self, node_id: str, nodes: List[TreeNode] = None) -> Optional[TreeNode]:
        """Find a node by its ID"""
        nodes = nodes or self.nodes
        for node in nodes:
            if node.id == node_id:
                return node
            if node.children:
                found = self.find_node_by_id(node_id, node.children)
                if found:
                    return found
        return None
    
    def find_nodes_by_tag(self, tag: str, nodes: List[TreeNode] = None) -> List[TreeNode]:
        """Find all nodes with a specific tag"""
        result = []
        nodes = nodes or self.nodes
        for node in nodes:
            if tag in node.tags:
                result.append(node)
            if node.children:
                result.extend(self.find_nodes_by_tag(tag, node.children))
        return result
    
    def get_selected_nodes(self) -> List[TreeNode]:
        """Returns the selected nodes"""
        if self.config.multi_select:
            return self.selected_nodes or []
        else:
            return [self.selected_node] if self.selected_node else []
    
    def expand_all(self):
        """Expand all nodes"""
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
        """Collapse all nodes"""
        def collapse_recursive(nodes: List[TreeNode]):
            for node in nodes:
                if node.children:
                    node.expanded = False
                    self.toggle_node(node)
                    collapse_recursive(node.children)
        
        collapse_recursive(self.nodes)
        if self.page:
            self.page.update()
    
    # Dialogues (may be overwritten)
    def show_rename_dialog(self, node: TreeNode):
        """Displays a dialog box to rename the node"""
        def rename_action(e):
            if new_name_field.value.strip():
                new_name = new_name_field.value.strip()
                if self.on_rename:
                    if self.on_rename(node, new_name):
                        node.name = new_name
                        self.update_node(node)
                else:
                    node.name = new_name
                    self.update_node(node)
                self.page.close(dlg)
                self.page.update()
        
        new_name_field = TextField(
            label="New Name",
            value=node.name,
            autofocus=True
        )
        
        dlg = AlertDialog(
            title=Text("Rename"),
            content=new_name_field,
            actions=[
                TextButton("Cancel", on_click=lambda e: self.page.close(dlg)),
                TextButton("Accept", on_click=rename_action),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def show_new_item_dialog(self, parent_node: TreeNode):
        """Displays a dialog box to create a new item"""
        def create_action(e):
            if name_field.value.strip():
                item_type = type_field.value
                new_node = TreeNode(
                    name=name_field.value.strip(),
                    children=[] if item_type == "folder" else [],
                    expanded=False,
                    icon=Icons.FOLDER if item_type == "folder" else Icons.INSERT_DRIVE_FILE
                )
                self.add_node(parent_node, new_node)
                self.page.close(dlg)
                self.page.update()
        
        name_field = TextField(
            label="Name",
            hint_text="New item",
            autofocus=True
        )
        
        type_field = TextField(
            label="Type",
            value="item",
            read_only=True,
            suffix=PopupMenuButton(
                items=[
                    PopupMenuItem(text="Folder", on_click=lambda e: setattr(type_field, "value", "folder")),
                    PopupMenuItem(text="File", on_click=lambda e: setattr(type_field, "value", "file")),
                    PopupMenuItem(text="Item", on_click=lambda e: setattr(type_field, "value", "item")),
                ]
            )
        )
        
        dlg = AlertDialog(
            title=Text("New Item"),
            content=Column([
                Text(f"Create on: {parent_node.name}"),
                name_field,
                type_field
            ], tight=True),
            actions=[
                TextButton("Cancel", on_click=lambda e: self.page.close(dlg)),
                TextButton("Create", on_click=create_action),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def show_delete_confirmation(self, node: TreeNode):
        """Displays a confirmation dialog for deletion"""
        def delete_action(e):
            self.remove_node(node)
            self.page.close(dlg)
            self.page.update()
        
        dlg = AlertDialog(
            title=Text("Confirm Delete"),
            content=Text(f"¿Delete '{node.name}'?"),
            actions=[
                TextButton("Cancel", on_click=lambda e: self.page.close(dlg)),
                TextButton("Delete", on_click=delete_action),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)
    
    def show_properties_dialog(self, node: TreeNode):
        """Displays the node properties"""
        content = Column(
            controls=[
                Text(f"Name: {node.name}", size=16),
                Text(f"ID: {node.id}", size=14),
                Text(f"Type: {'Folder' if node.children else 'File'}", size=14),
                Text(f"Children: {len(node.children)}", size=14),
                Text(f"Tags: {', '.join(node.tags) if node.tags else 'None'}", size=14),
                Text(f"Expanded: {'Yes' if node.expanded else 'No'}", size=14),
                Text(f"Level: {self.get_node_level(node)}", size=14),
            ],
            tight=True
        )
        
        dlg = AlertDialog(
            title=Text("Properties"),
            content=content,
            actions=[
                TextButton("Close", on_click=lambda e: self.page.close(dlg)),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.open(dlg)