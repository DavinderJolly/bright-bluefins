import sys

from PIL import Image
from prompt_toolkit import ANSI, Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout


class ImageViewer:
    """Image viewer class"""

    def __init__(self, path: str, mode: str = "ANSI", size: tuple = (100, 50)):
        self.path = path
        if mode in ["ANSI", "ASCII"]:
            self.mode = mode
        else:
            print("Supported image mode: ANSI, ASCII")
        self.size = size

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

    def view(self) -> None:
        """View the image"""
        image = Image.open(self.path)
        image.thumbnail(self.size, Image.HAMMING)

        string: str = ""
        for y in range(0, image.height, 2):
            for x in range(0, image.width):
                try:
                    fg_color = image.getpixel((x, y + 1))[:3]
                    bg_color = image.getpixel((x, y))[:3]
                except IndexError:
                    continue

                fg = self.ansi_fg(*fg_color)
                bg = self.ansi_bg(*bg_color)
                string += "{}{}▄".format(fg, bg)
            string += "\n"

        app = self.make_app(string)
        app.run()

    def make_app(self, string: str) -> Application:
        """Create the app to show image

        Args:
            string: Image string in ANSI or ASCII
        """
        kb = KeyBindings()

        @kb.add("c-d")
        def _exit(event: KeyPressEvent) -> None:
            """Exits from the app

            Args:
                event (KeyPressEvent): Takes an KeyPress event
            """
            event.app.exit()

        container = VSplit(
            [Window(content=FormattedTextControl(text=ANSI(string), key_bindings=kb))]
        )
        layout = Layout(container)
        app: Application = Application(layout=layout, full_screen=True)
        return app


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ImageViewer(sys.argv[1]).view()
    else:
        print("Usage: photos img_path")
