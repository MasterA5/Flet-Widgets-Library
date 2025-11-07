# 📚 Flet Widgets Library

A collection of custom, animated UI components for **Flet applications**, designed to enhance user interfaces with smooth animations and engaging interactions.

## 🌐 Live Demo

👉 [Try the Live Example](https://fletwidgetslibrarydemoexample.pages.dev)

---

## 🚀 Features

### **Animated Components**

- **BubbleText**: Bubble text animation effects with a complete refactor — now featuring richer and more dynamic behaviors.
- **TextFader**: Smooth text transitions with elegant fade effects.
- **TypeWriter**: Typewriter-style text animation for a classic typing effect.
- **SplitText**: Text splitting animation with multiple direction options.
- **HighlightRotatingText**: Static text combined with an animated, rotating text inside a dynamic highlight box.
- **ImageSlider**: Image slider with smooth transition animations and effects, inspired by [this video](https://www.youtube.com/watch?v=Vbu1UAaoJxw&t=63s). Credits to [DevSenate](https://github.com/navideveloper).

### **Basic Components**

- **BasicButton**: Basic Button With a default animations and styles
- **RestrictedInput**: Text field with rules to validate its value
- **Stepper**: Basic Stepper Widget For Make a Modern Form

---

## 🛠️ Usage

### Basic Setup

```python
from FletWidgetsLibrary import BubbleText, TextFader, TypeWriter, SplitText, HighlightRotatingText
from flet import *

def main(page: Page):
    page.title = "Flet Widgets Library Demo"
    page.theme_mode = ThemeMode.DARK
    page.padding = 50
    page.update()

    # Add your widgets here
    page.add(
        Row(
            controls=[
                AnimatedTextBubble(
                    texts="Hello Flet!!",
                    bgcolor=Colors.GREY_700,
                    speed=60,
                    MarkdownCodeTheme=MarkdownCodeTheme.DRAGULA,
                    ExtensionSet=MarkdownExtensionSet.GITHUB_WEB,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            width=400 # <- Adjust this value for the width of the bubble
        ),
        TextFader(
            text="Hello World And Hello Flet",
            loop=True,
            color=ft.Colors.RED,
            permanent=False
        ),
        TypeWriter(
            texts=["Welcome To Flet With A Typewriter Effect"],
            speed=30,
            size=40,
            color=ft.Colors.BLUE
        ),
        SplitText(
            texts=["Hello World", "Offset Animation With Loop"],
            speed=0.1,
            pause=1.5,
            loop=True,
            size=32,
            color=ft.Colors.BROWN,
            bold=True,
            direction="bottom"
        ),
        HighlightRotatingText(
            static_text="Creative",
            phrases=["thinking", "building", "coding"],
            interval=1.5,
            box_color=ft.Colors.DEEP_PURPLE,
            size=30,
            direction="top",
            speed=0.08,
            width_factor=22
        )
    )

app(target=main)
```

---

## 📚 Components

### AnimatedTextBubble

Creates text with a bubble animation effect and give a best Markdown themes.

> Complete Markdonw Support!!

```python
AnimatedTextBubble(
    texts: Union[str, List[str]],
    speed: int = 10,
    pause: float = 0,
    bgcolor: Colors = Colors.GREY_900,
    border_radius: int = 20,
    MarkdownCodeTheme: MarkdownCodeTheme = MarkdownCodeTheme.ATOM_ONE_DARK,
    ExtensionSet: MarkdownExtensionSet = MarkdownExtensionSet.GITHUB_WEB
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

Creates a split-text animation with directional entry.

```python
SplitText(
    texts: list[str] = ["Hello World", "Offset Animation With Loop"],
    speed: float = 0.1,
    pause: flota = 1.5,
    loop: bool = True,
    size: int = 32,
    color: Colors = Colors.BROWN,
    bold: bool = True,
    direction: str = "bottom"
)
```

### HighlightRotatingText

Combines a static text with a **highlight box** that dynamically animates rotating phrases, showing them letter by letter.

```python
HighlightRotatingText(
    static_text: str,
    phrases: list[str] | str,
    interval: float = 2.0,
    size: int = 28,
    color: str = Colors.WHITE,
    bold: bool = True,
    box_color: str = Colors.INDIGO,
    loop: bool = True,
    direction: str = "bottom",  # "bottom", "top", "left", "right"
    speed: float = 0.05,
    width_factor: int = 20,
    static_style: TextStyle | None = None
)
```

### ImagesSlider

Create A Images Slider More Easy With This Widget With A Better Animations And Transitions

```python
ImagesSlider(
    images: list[Image],
    auto_play: bool = False,
    interval: float = 3,
    buttons_color: str = Colors.GREY_900,
    selected_buttons_color: str = Colors.WHITE,
    animation_type: str = "FADE"
)
```

### BasicButton

Create a Basic Button With Easy Animations And Styles

```python
BasicButton(
    text: str,
    on_click: Optional[Callable] = None,
    bgcolor: Union[str, Colors] = Colors.BLUE,
    text_color: Union[str, Colors] = Colors.WHITE,
    icon: Optional[str] = None,
    hover_scale: float = 1.08,
    click_scale: float = 0.9,
    animation_duration: int = 200,
)
```

### RestrictedInput

Create a text field with rules to validate its content (This is not a final version).

```python
RestrictedInput(
    pattern: str = None,
    on_validate=None,
    **kwargs
)
```

### Stepper

Create a Modern Stepper More Easy
This widget include a custom dataclass for its events and make your custom ```StepperStepCard()```

## Stepper Event

```python
@dataclass
class StepperEvent:
    type: str
    current_step: int            
    total_steps: int             
    step: Control                
    is_first: bool
    is_last: bool
    completed: bool
    parent: Control
```

## Stepper Step Card

```python
StepperStepCard(
    title: str,
    subtitle: str = "",
    description: str = "",
    icon: Union[Control, Icons] = Icons.CIRCLE,
    icon_color: str = Colors.WHITE,
    icon_size: int = 30,
    content: Optional[Control] = None,
    color: str = Colors.BLUE_400,
    active_color: Optional[str] = None,
)
```

## Stepper

```python
Stepper(
    steps: list[StepperStepCard],
    on_event=None,
    on_complete=None,
    active_color=Colors.BLUE,
    inactive_color=Colors.GREY_700,
    completed_color=Colors.GREEN,
)
```

## 🧪 Tested On

| Platform | TypeWriter | SplitText | ImagesSlider | TextFader | BubbleText | RotatingText |
| -------- | ---------- | --------- | ------------ | --------- | ---------- | ------------ |
| Android  | ✅         | ✅        | ✅           | ✅        | ✅         | ✅           |
| iOS      | ❌         | ❌        | ❌           | ❌        | ❌         | ❌           |
| Windows  | ✅         | ✅        | ✅           | ✅        | ✅         | ✅           |
| MacOS    | ❌         | ❌        | ❌           | ❌        | ❌         | ❌           |
| Linux    | ❌         | ❌        | ❌           | ❌        | ❌         | ❌           |

## 📝 Examples

Check out the `Demo-Example.py` file for complete usage examples of each component or Check Any Examples Individualy.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

### Powered By [Flet](https://flet.dev/) ❤
