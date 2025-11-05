from Treevieww import TreeView, TreeNode
from flet import *

def main(page: Page):
    page.title = "TreeView con Menú Contextual - Flet 0.28.3"
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
                        TreeNode("React App"),
                        TreeNode("Vue.js Site"),
                    ],
                    expanded=False
                ),
                TreeNode(
                    name="Backend",
                    children=[
                        TreeNode("API Rest"),
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
    ]

    # Crear el TreeView con menú contextual
    tree_view = TreeView(
        nodes=root_nodes,
        show_context_menu=True
    )

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
        ],
    )

    # Contenedor principal
    container = Container(
        content=Column(
            controls=[
                Text("TreeView con Menú Contextual", size=20, weight=FontWeight.BOLD),
                controls_row,
                Container(
                    content=tree_view,
                    border=border.all(1, Colors.GREY_700),
                    border_radius=8,
                    padding=10,
                    width=500
                )
            ],
            expand=True,
            scroll="auto"
        ),
    )

    page.add(container)

if __name__ == "__main__":
    app(target=main)