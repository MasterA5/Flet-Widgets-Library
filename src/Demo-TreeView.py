from FletWidgetsLibrary import TreeView, TreeNode, TreeViewConfig
from flet import *

def main(page: Page):
    
    # Create example nodes
    root_nodes = [
        TreeNode(
            name="Projects",
            icon=Icons.FOLDER_SPECIAL,
            children=[
                TreeNode(name="Frontend", icon=Icons.WEB, tags=["web", "frontend"]),
                TreeNode(name="Backend", icon=Icons.STORAGE, tags=["server"]),
            ],
            expanded=True
        ),
        TreeNode(
            name="Documents",
            icon=Icons.DESCRIPTION,
            children=[
                TreeNode(name="Report.pdf", icon=Icons.PICTURE_AS_PDF),
                TreeNode(name="Presentation.pptx", icon=Icons.SLIDESHOW),
            ]
        ),
    ]
    
    # Custom config
    config = TreeViewConfig(
        selection_color=Colors.TRANSPARENT,
        custom_icons={
            "web": Icons.WEB,
            "server": Icons.CLOUD,
            "important": Icons.STAR,
        }
    )
    
    # Callbacks
    def on_node_selected(node, selected_nodes=None):
        if selected_nodes:
            print(f"Selected Nodes: {[n.name for n in selected_nodes]}")
        else:
            print(f"Select Node: {node.name}")
    
    def on_rename(node, new_name):
        print(f"Renamed {node.name} a {new_name}")
        return True  # Allow renaming
    
    def on_new_item(parent, item_type, default_name):
        print(f"Creating {item_type} en {parent.name}")
        return TreeNode(
            name=default_name,
            icon=Icons.ADD_CIRCLE if item_type == "item" else Icons.FOLDER
        )
    
    # Create TreeView
    tree = TreeView(
        nodes=root_nodes,
        config=config,
        on_node_select=on_node_selected,
        on_rename=on_rename,
        on_new_item=on_new_item,
    )
    
    # Additional controls
    toolbar = Row([
        IconButton(Icons.EXPAND, on_click=lambda e: tree.expand_all()),
        IconButton(Icons.EXPAND_LESS, on_click=lambda e: tree.collapse_all()),
    ])
    
    page.add(toolbar, Divider(), tree)

app(target=main)