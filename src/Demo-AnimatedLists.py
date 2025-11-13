from FletWidgetsLibrary import OrdenedList, UnorderedList
from flet import *

def main(page: Page):
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.START
    page.bgcolor = Colors.BLACK
    page.srcoll = "auto"
    page.padding = 30

    unordened_list = UnorderedList(
        items=[
            Text(f"Element {i}") for i in range(10)
        ],
        delay=0.01
    )

    ordened_list = OrdenedList(
        items=[
            Text(f"Element {i}") for i in range(10)
        ],
        delay=0.01
    )

    def add_task(e):
        if e.control.data == "unordened-list":
            unordened_list.add_item(Text("New Item Append"))
        else:
            ordened_list.add_item(Text("New Item Append"))

    page.add(
        Row(
            controls=[
                Column(
                    controls=[
                        Text("Unordened List"),
                        unordened_list,
                        ElevatedButton("Add Element", data="unordened-list", on_click=add_task)
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    scroll="auto",
                    expand=True
                ),
                Column(
                    controls=[
                        Text("Ordened List"),
                        ordened_list,
                        ElevatedButton("Add Element", data="ordened-list", on_click=add_task)
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    scroll="auto",
                    expand=True
                ),
            ]
        )
    )

app(target=main)
