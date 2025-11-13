# 📚 Flet Widgets Library

✨ A rich collection of **custom, animated UI components** for [**Flet**](https://flet.dev/) applications — designed to enhance user interfaces with smooth animations, elegant transitions, and engaging interactions.

---

## 🚀 Features

### 🌀 **Animated Components**
- **BubbleText** → Bubble-style animated markdown text.
- **TextFader** → Smooth fade-in/fade-out text transitions.
- **TypeWriter** → Classic typing animation effect.
- **SplitText** → Directional split text animations.
- **HighlightRotatingText** → Dynamic rotating phrases inside a highlight box.
- **ImageSlider** → Elegant image slider with transition effects ([inspired by DevSenate](https://github.com/navideveloper)).
- **Animated Lists** → Stylish unordered and ordered animated list components.

### 🧩 **Basic Components**
- **BasicButton** → Animated button with hover and click effects.
- **RestrictedInput** → Input with pattern validation rules.
- **Stepper** → Modern stepper widget for multi-step forms.

---

## 🎨 Components

### **AnimatedTextBubble**

Create text with bubble animation and full **Markdown support**.

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

## 🎬 Example:

<video src="videos/bubble-text.mp4" width="600" controls></video>

---

### 🌫️ **TextFader**

Smoothly fade between multiple text strings.

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

## 🎬 Example:

<video src="videos/text-fader.mp4" width="600" controls></video>

---

### ⌨️ **TypeWriter**

Simulates a typing effect for one or multiple phrases.

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

## 🎬 Example:

<video src="videos/type-writter.mp4" width="600" controls></video>

---

### ✂️ **SplitText**

Creates animated text that enters from a direction (top, bottom, left, right).

```python
SplitText(
    texts: list[str],
    speed: float = 0.1,
    pause: float = 1.5,
    loop: bool = True,
    size: int = 32,
    color: Colors = Colors.WHITE,
    bold: bool = True,
    direction: str = "bottom"
)
```

## 🎬 Example:

<video src="videos/split-text.mp4" width="600" controls></video>

---

### 💡 **HighlightRotatingText**

Combine static and dynamic text inside a highlight box.

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
    direction: str = "bottom",
    speed: float = 0.05,
    width_factor: int = 20,
)
```

## 🎬 Example:

<video src="videos/rotating-text.mp4" width="600" controls></video>

---

### 🖼️ **ImagesSlider**

An elegant image carousel with smooth transitions.

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

## 🎬 Example:

<video src="videos/image-carousel.mp4" width="600" controls></video>
---

### 🔘 **BasicButton**

A modern button with hover and click animations.

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

## 🎬 Example:

<video src="videos/basic-button.mp4" width="600" controls></video>

---

### ✏️ **RestrictedInput**

Input field with validation based on regular expressions. 
<p style="color:yellow">⚠ This widget is still under development, so its documentation is not yet complete and is subject to change.</p>

```python
RestrictedInput(
    pattern: str = None,
    on_validate=None,
    **kwargs
)
```

---

### 🧭 **Stepper**

A customizable multi-step UI widget for modern forms.
<p style="color:yellow">⚠ This widget is still under development, so some features may not work correctly.</p>
<h3>For example:</h3>
<ul>
    <li>Internal Null Input Values</li>
    <li>Values ​​within the False checkbox</li>
    <li>Animations</li>
</ul>

#### StepperEvent

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
)
```

#### StepperStepCard

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

#### Stepper

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

## 🎬 Example:

<video src="videos/stepper.mp4" width="600" controls></video>

---

### 📋 **Animated Lists**

Create beautiful animated ordered and unordered lists.

#### Unordered

```python
UnorderedList(
    items: List[ListItem],
    spacing: int = 5,
    item_color: str = Colors.AMBER_700,
    delay: float = 0.01
)
```

#### Ordered

```python
OrderedList(
    items: List[ListItem],
    spacing: int = 5,
    item_color: str = Colors.AMBER_700,
    delay: float = 0.01
)
```

## 🎬 Example:

<video src="videos/animated-list.mp4" width="600" controls></video>

---

## 🧪 Tested On

| Platform | TypeWriter | SplitText | ImagesSlider | TextFader | BubbleText | RotatingText | BasicButton | RestrictedInput | Stepper | UnorderedList | OrderedList |
|-----------|-------------|------------|---------------|------------|--------------|---------------|--------------|----------------|----------|----------------|--------------|
| Android   | ✅          | ✅         | ✅            | ✅         | ✅           | ✅            | ✅           | ✅             | ✅       | ✅             | ✅           |
| iOS       | ❌          | ❌         | ❌            | ❌         | ❌           | ❌            | ❌           | ❌             | ❌       | ❌             | ❌           |
| Windows   | ✅          | ✅         | ✅            | ✅         | ✅           | ✅            | ✅           | ✅             | ✅       | ✅             | ✅           |
| macOS     | ❌          | ❌         | ❌            | ❌         | ❌           | ❌            | ❌           | ❌             | ❌       | ❌             | ❌           |
| Linux     | ❌          | ❌         | ❌            | ❌         | ❌           | ❌            | ❌           | ❌             | ❌       | ❌             | ❌           |


---

## 📝 Examples

Explore the `Demo-Example.py` file for a complete showcase,
or open individual examples inside the `examples/` folder.

---

## 🤝 Contributing

Pull requests are welcome!
If you'd like to contribute, fork the repo and submit your improvements — code style, docs, or new widgets are all appreciated 💡

---

## ❤️ Powered By Flet

Built with love using [**Flet**](https://flet.dev/).