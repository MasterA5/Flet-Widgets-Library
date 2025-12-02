from FletWidgetsLibrary import (
    CupertinoMicrosoftButton,
    CupertinoLinkedinButton,
    CupertinoGoogleButton,
    CupertinoAmazonButton,
    CupertinoGithubButton,
    CupertinoAppleButton,
    MicrosoftButton,
    LinkedinButton,
    GoogleButton,
    AmazonButton,
    GithubButton,
    AppleButton,
)
from flet import *

def main(page:Page):
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    cupertino_microsoft_btn = CupertinoMicrosoftButton()
    cupertino_linkedin_btn = CupertinoLinkedinButton()
    cupertino_google_btn = CupertinoGoogleButton()
    cupertino_amazon_btn = CupertinoAmazonButton()
    cupertino_github_btn = CupertinoGithubButton()
    cupertino_apple_btn = CupertinoAppleButton()
    microsoft_btn = MicrosoftButton()
    linkedin_btn = LinkedinButton()
    google_btn = GoogleButton()
    amazon_btn = AmazonButton()
    github_btn = GithubButton()
    apple_btn = AppleButton()

    page.add(
        Row(
            controls=[
                Column(
                    controls=[
                        Text(
                            value="Oauth Providers Buttons",
                            color=Colors.WHITE,
                            weight="bold"
                        ),
                        Divider(height=2.5),
                        microsoft_btn,
                        Divider(height=2.5),
                        linkedin_btn,
                        Divider(height=2.5),
                        google_btn,
                        Divider(height=2.5),
                        amazon_btn,
                        Divider(height=2.5),
                        github_btn,
                        Divider(height=2.5),
                        apple_btn
                    ],
                    tight=True
                ),
                Column(
                    controls=[
                        Text(
                            value="Cupertino Oauth Providers\nButtons",
                            color=Colors.WHITE,
                            weight="bold"
                        ),
                        cupertino_microsoft_btn,
                        cupertino_linkedin_btn,
                        cupertino_google_btn,
                        cupertino_amazon_btn,
                        cupertino_github_btn,
                        cupertino_apple_btn
                    ],
                    tight=True
                ),
            ],
            spacing=30,
            alignment=MainAxisAlignment.CENTER
        ),
    )
    
app(target=main)