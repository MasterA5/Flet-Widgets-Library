# 📚 Flet Widgets Library

A collection of custom, animated UI components for Flet applications, designed to enhance user interfaces with smooth animations and engaging interactions.

## 🚀 Features

### Animated Components

- **BubbleText**: Text with bubble animation effects
- **TextFader**: Smooth text transitions with fade effects
- **TypeWriter**: Typewriter-style text animation
- **SplitText**: SplitText Animated with different animation directions

## 🛠️ Usage

### Basic Setup

```python
from FletWidgetsLibrary import BubbleText, TextFader, TypeWriter
import flet as ft

def main(page: ft.Page):
    page.title = "Flet Widgets Library Demo"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.update()

    # Add your widgets here
    page.add(
        Row(
            controls=[
                AnimatedTextBubble(
                    texts=demo_text, 
                    speed=60, 
                    bgcolor=Colors.PURPLE
                )
            ],
            alignment=MainAxisAlignment.START,
            width=400 # <- Adjust this value for the width of the bubble
        ),
        TextFader(
            text="Hello World And Hello Flet",
            loop=True,
            color=Colors.RED,
            permanent=False
        ),
        TypeWriter(
            texts=["Hello Welcome To Flet This Is A Type Writer Animated"],
            speed=30,
            size=40,
            color=Colors.BLUE
        ),
        SplitText(
            texts=["Hello World", "Offset Animation With Loop"],
            speed=0.1,
            pause=1.5,
            loop=True,
            size=32,
            color=Colors.BROWN,
            bold=True,
            direction="bottom"
        )
    )

ft.app(target=main)
```

## 📚 Components

### AnimatedTextBubble
Creates text with a bubble animation effect.

```python
AnimatedTextBubble(
    texts: List[str] | str,
    size: int = 24,
    bgcolor: Colors = Colors.WHITE,
    speed: int = 50,
    pause: int = 0,
    on_copied: Optional[callable] = None,
)
```

### TextFader
Creates a text component that fades between multiple strings.

```python
TextFader(
    text: str,
    color: Any = Colors.WHITE,
    size: int = 24,
    speed: float = 0.05,
    pause: float = 1,
    loop: bool = False,
    permanent: bool = False
)
```

### TypeWriter
Creates a typewriter effect for text.

```python
TypeWriter(
    texts: str | List[str],
    speed: int = 10,
    pause: float = 1,
    loop: bool = False,
    size: int = 24,
    color: Any = Colors.WHITE,
    bold: bool = False
)
```

### SplitText
```python
SplitText(
    texts=["Hello World", "Offset Animation With Loop"],
    speed=0.1,
    pause=1.5,
    loop=True,
    size=32,
    color=Colors.BROWN,
    bold=True,
    direction="bottom"
),
```

## 📝 Examples

Check out the `Demo-Example.py` file for complete usage examples of each component.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
---

### Powered By [Flet](https://flet.dev/) ❤
