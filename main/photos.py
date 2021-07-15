import sys

from PIL import Image
from prompt_toolkit import ANSI, Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.output.color_depth import ColorDepth


class ImageViewer:
    """Image viewer class"""

    def __init__(self, path: str, mode: str = "ANSI", size: tuple = (100, 50)):
        self.path = path
        self.mode = mode.upper()
        self.size = size
        self.image_string: str = ""

    @staticmethod
    def rgb2ascii(rgb: list) -> str:
        """Returns the ASCII pixel value

        Args:
            r, g, b: rgb color channel
        """
        return ".,-_~:;^+?*#&$@"[int(sum(rgb) / (3 * 255) * 14)]

    @staticmethod
    def ansi_fg(r: int, g: int, b: int) -> str:
        """Returns the ANSI 24-bit foreground color

        Args:
            r, g, b: rgb color channel
        """
        return "\x1b[38;2;{};{};{}m".format(r, g, b)

    @staticmethod
    def ansi_bg(r: int, g: int, b: int) -> str:
        """Returns the ANSI 24-bit background color

        Args:
            r, g, b: rgb color channel
        """
        return "\x1b[48;2;{};{};{}m".format(r, g, b)

    def view_ansi(self, image: Image) -> None:
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

    def view_ascii(self, image: Image) -> None:
        """View the image in ASCII mode"""
        for y in range(0, image.height):
            for x in range(0, image.width):
                try:
                    color = image.getpixel((x, y))[:3]
                except IndexError:
                    continue

                self.image_string += self.rgb2ascii(color)
            self.image_string += "\n"

    def run_app(self) -> None:
        """Run the ImageViewer app"""
        image = Image.open(self.path)
        image.thumbnail(self.size, Image.HAMMING)

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
                        text=ANSI(self.image_string), key_bindings=kb
                    )
                )
            ]
        )
        layout = Layout(container)
        app = Application(
            color_depth=ColorDepth.TRUE_COLOR, layout=layout, full_screen=True
        )
        return app


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            mode = sys.argv[2]
        else:
            mode = "ANSI"
        ImageViewer(path=path, mode=mode).run_app()
    else:
        print("Usage: photos img_path")
