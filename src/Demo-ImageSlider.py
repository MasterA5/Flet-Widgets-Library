from FletWidgetsLibrary import ImagesSlider
from flet import (
    Page,
    app,
    Row,
    Image,
    ImageFit
)

# Demo Example
def main(page:Page):
    page.vertical_alignment = "center"
    page.window.height = 1000
    page.window.width = 800

    images_1 = [
        Image(
            src=f"https://picsum.photos/800/450?{i}", 
            fit=ImageFit.COVER
        )
        for i in range(10)
    ]

    images_2 = [
        Image(
            src=f"https://picsum.photos/800/450?{i*2}", 
            fit=ImageFit.COVER
        )
        for i in range(10)
    ]

    SliderWithAutoPlay = ImagesSlider(images=images_1, auto_play=True, interval=1, animation_type="FADE")
    SliderWithOutAutoPlay = ImagesSlider(images=images_2, animation_type="SCALE")

    page.add(SliderWithAutoPlay, SliderWithOutAutoPlay)

app(target=main)