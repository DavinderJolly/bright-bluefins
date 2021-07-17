import os
import sys
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image
from prompt_toolkit import ANSI, Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.styles import Style


class ImageViewer:
    """Image viewer class"""

    def __init__(
        self,
        path: Path,
        mode: str = "ANSI",
        size: Tuple[int, int] = (100, 50),
        style: Optional[Style] = None,
    ):
        self.path = path
        self.mode = mode.upper()
        self.size = size
        self.style = style
        self.image_string: str = ""

    @staticmethod
    def resize_image(image: Image.Image) -> Image.Image:
        """
        Returns the resized image

        Args:
            image: image to be resized
        """
        (w, h) = image.size
        new_height = os.get_terminal_size()[1]
        # Aspect ratio with height
        aspect_ratio = w / h
        new_width = int(aspect_ratio * new_height)
        image = image.resize((new_width, new_height), Image.HAMMING)
        return image

    @staticmethod
    def rgb2ascii(px: int) -> str:
        """
        Returns the ASCII pixel value

        Args:
            px: greyscale pixel value
        """
        ASCII_PIXELS = ".,-~:;^+?*#&$@"
        n = len(ASCII_PIXELS)
        return ASCII_PIXELS[int((px / 255) * (n - 1))]

    @staticmethod
    def ansi_fg(r: int, g: int, b: int) -> str:
        """
        Returns the ANSI 24-bit foreground color

        Args:
            r, g, b: rgb color channel
        """
        return "\x1b[38;2;{};{};{}m".format(r, g, b)

    @staticmethod
    def ansi_bg(r: int, g: int, b: int) -> str:
        """
        Returns the ANSI 24-bit background color

        Args:
            r, g, b: rgb color channel
        """
        return "\x1b[48;2;{};{};{}m".format(r, g, b)

    def view_ansi(self, image: Image.Image) -> None:
        """View the image in ANSI mode"""
        for y in range(0, image.height, 2):
            for x in range(0, image.width):
                try:
                    fg_color = image.getpixel((x, y + 1))[:3]
                    bg_color = image.getpixel((x, y))[:3]
                except IndexError:
                    continue

                fg = self.ansi_fg(*fg_color)
                bg = self.ansi_bg(*bg_color)
                self.image_string += "{}{}▄".format(fg, bg)
            self.image_string += "\n"

    def view_ascii(self, image: Image.Image) -> None:
        """View the image in ASCII mode"""
        image = self.resize_image(image)
        # Convert image to greyscale
        image = image.convert("L")

        for y in range(0, image.height):
            for x in range(0, image.width):
                color = image.getpixel((x, y))

                self.image_string += self.rgb2ascii(color)
            self.image_string += "\n"

    def run_app(self) -> None:
        """Run the ImageViewer app"""
        image = Image.open(self.path)
        image.thumbnail(self.size, Image.HAMMING)
        # image = self.resize_image(image)

        if self.mode == "ANSI":
            self.view_ansi(image)
        elif self.mode == "ASCII":
            self.view_ascii(image)

        app = self.make_app()
        app.run()

    def make_app(self) -> Application:
        """Create the app to show image"""
        kb = KeyBindings()

        @kb.add("c-d")
        def _exit(event: KeyPressEvent) -> None:
            """Exits from the app

            Args:
                event (KeyPressEvent): Takes an KeyPress event
            """
            event.app.exit()

        container = VSplit(
            [
                Window(
                    content=FormattedTextControl(
                        text=ANSI(self.image_string),
                    ),
                    always_hide_cursor=True,
                    align=WindowAlign.CENTER,
                )
            ]
        )
        layout = Layout(
            HSplit(
                [
                    Window(
                        content=FormattedTextControl(
                            "Photos - {}".format(self.path.name)
                        ),
                        height=1,
                        always_hide_cursor=True,
                        align=WindowAlign.CENTER,
                        style="class:frame",
                    ),
                    Window(content="", height=1),
                    container,
                    Window(
                        content=FormattedTextControl("<Ctrl+D=Exit>"),
                        height=1,
                        always_hide_cursor=True,
                        align=WindowAlign.LEFT,
                        style="class:frame",
                    ),
                ],
                key_bindings=kb,
            )
        )
        app: Application = Application(
            layout=layout,
            full_screen=True,
            style=self.style,
            color_depth=ColorDepth.TRUE_COLOR,
        )
        return app


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            mode = sys.argv[2]
        else:
            mode = "ANSI"
        ImageViewer(path=Path(path), mode=mode).run_app()
    else:
        print("Usage: photos img_path")
