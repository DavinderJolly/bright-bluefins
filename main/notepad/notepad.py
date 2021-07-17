import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.styles.style import _MergedStyle
from prompt_toolkit.widgets import MenuContainer, MenuItem, TextArea
from pygments.lexers import find_lexer_class_for_filename
from pygments.util import ClassNotFound


class NotepadApp:
    """Creating the Notepad App"""

    def __init__(
        self,
        file_name: Optional[Union[str, Path]] = None,
        style: Optional[_MergedStyle] = None,
    ):
        """
        Initialize the class

        Args:
            style: Takes in the style. Defaults to {}.
        """
        if file_name is None:
            self.file_name = self.parse_args()
        else:
            if isinstance(file_name, str):
                file_name = Path(file_name)
            self.file_name = file_name
        self.style = style
        self.text = ""
        self.lexer = None
        self.show_status_bar = True
        self.ask_for_filename = False
        self.text = self.get_text_from_file(self.file_name)
        self.lexer = self.add_lexer(self.file_name)
        self.text_field = self.make_text_field()
        self.filename_prompt_field = self.make_filename_prompt_field()
        self.Key_bindings = self.make_key_bindings()
        self.root_container = self.make_root_container()
        self.application = self.make_application()

    @staticmethod
    def parse_args() -> Optional[Path]:
        """
        Parses the arguments given when running the file

        Returns:
            Path: returns filename
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("file_name", type=str, nargs="?")
        args = vars(parser.parse_args())
        file_name = args.get("file_name", None)
        return Path(file_name) if file_name is not None else None

    @staticmethod
    def get_text_from_file(file_name: Optional[Path]) -> str:
        """
        Reads text from a file

        Args:
            file_name: Name of the file to read

        Returns:
            str: text read from the file
        """
        text = ""
        if file_name is not None and file_name.exists():
            with file_name.open("r") as f:
                text = f.read()
        return text

    def save_file(self) -> None:
        """Saves the file"""
        if self.file_name is not None:
            with self.file_name.open("w") as f:
                f.write(self.text_field.text)
        else:
            self.show_status_bar = False
            self.ask_for_filename = True
            get_app().layout.focus(self.filename_prompt_field)

    def add_lexer(self, file_name: Optional[Path]) -> Optional[PygmentsLexer]:
        """
        Returns the lexer based on the file name

        Args:
            file_name: Takes the name of the file

        Returns:
            Optional[PygmentsLexer]: Returns PygmentsLexer class
        """
        lexer_name = None
        if file_name is not None:
            try:
                lexer_name = find_lexer_class_for_filename(file_name.name)
                if lexer_name is not None:
                    self.lexer = PygmentsLexer(lexer_name)

            except ClassNotFound:
                self.lexer = None
        return self.lexer

    # Adding keybindings
    def make_key_bindings(self) -> KeyBindings:
        """
        Creates necessary keybindings for the app

        Returns:
            KeyBindings: Returns the key bindings
        """
        kb = KeyBindings()

        @kb.add("c-d")
        def _exit(event: KeyPressEvent) -> None:
            """
            Exits from the app

            Args:
                event: Takes an KeyPress event
            """
            event.app.exit()

        @kb.add("c-s")
        def _save_file(event: Optional[KeyPressEvent] = None) -> None:
            """
            Saves the file

            Args:
                event: Takes an Optional KeyPress event. Defaults to None.
            """
            self.save_file()

        @kb.add("c-c")
        def _focus(event: KeyPressEvent) -> None:
            """Focuses the window

            Args:
                event: Takes an KeyPress event
            """
            event.app.layout.focus(self.root_container.window)

        return kb

    # Make UI elements
    def make_text_field(self) -> TextArea:
        """Makes text field

        Returns:
            TextArea: returns an instance of text area
        """
        return TextArea(
            text=self.text,
            lexer=self.lexer,
            scrollbar=True,
            line_numbers=True,
            style="class:text-area",
        )

    def make_filename_prompt_field(self) -> TextArea:
        """Creates a Prompt for the path to save the file

        Returns:
            TextArea: Returns TextArea class
        """

        def _no_name_handler(buffer: Buffer) -> bool:
            """Handles when no filename is given

            Args:
                buffer (Buffer): Takes the buffer class
            Returns:
                bool: True if text should be kept after accepting else False
            """
            self.file_name = Path(buffer.text.strip())
            self.save_file()
            get_app().layout.focus(self.text_field)
            self.show_status_bar = True
            self.ask_for_filename = False
            return False

        return TextArea(
            height=1,
            multiline=False,
            wrap_lines=False,
            accept_handler=_no_name_handler,
        )

    def make_body(self) -> HSplit:
        """Returns the body of the program

        Returns:
            HSplit: Class
        """

        def get_datetime() -> str:
            """Get datetime in (dd/mm/yyyy, hh:mm:ss) format"""
            return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        def get_pos() -> str:
            """Get line and column number"""
            return "Ln {}, Col {}".format(
                self.text_field.document.cursor_position_row + 1,
                self.text_field.document.cursor_position_col + 1,
            )

        body = HSplit(
            [
                self.text_field,
                ConditionalContainer(
                    content=VSplit(
                        [
                            Window(FormattedTextControl(get_datetime)),
                            Window(
                                FormattedTextControl(get_pos),
                                width=25,
                                align=WindowAlign.RIGHT,
                            ),
                        ],
                        height=1,
                        style="class:bottom",
                    ),
                    filter=Condition(lambda: self.show_status_bar),
                ),
                ConditionalContainer(
                    content=VSplit(
                        [
                            Window(FormattedTextControl("Path To Save File: ")),
                            self.filename_prompt_field,
                        ],
                        height=1,
                    ),
                    filter=Condition(lambda: self.ask_for_filename),
                ),
            ],
            style="class:body",
        )
        return body

    def make_root_container(self) -> MenuContainer:
        """Returns an instance of the MenuContainer

        Returns:
            MenuContainer: Class
        """

        def exit_app() -> None:
            """Exit from the app"""
            get_app().exit()

        def status_bar_handler() -> None:
            """Show/hide the status bar"""
            self.show_status_bar = not self.show_status_bar

        container = MenuContainer(
            body=self.make_body(),
            menu_items=[
                MenuItem(
                    "File  ",
                    children=[
                        MenuItem("New"),
                        MenuItem("Save"),
                        MenuItem("-", disabled=True),
                        MenuItem("Exit", handler=exit_app),
                    ],
                ),
                MenuItem(
                    "View  ",
                    children=[MenuItem("Status Bar", handler=status_bar_handler)],
                ),
                MenuItem("Info  ", children=[MenuItem("About")]),
            ],
            key_bindings=self.Key_bindings,
        )
        return container

    def make_layout(self) -> Layout:
        """
        Creates an instance of Layout

        Returns:
            Layout: Class
        """
        return Layout(
            HSplit(
                [
                    Window(
                        FormattedTextControl("Notepad"),
                        height=1,
                        align=WindowAlign.CENTER,
                        style="class:top",
                    ),
                    self.root_container,
                ]
            ),
            focused_element=self.text_field,
        )

    def make_application(self) -> Application:
        """
        Creates an application instance

        Returns:
            Application: Class
        """
        return Application(
            layout=self.make_layout(),
            style=self.style,
            full_screen=True,
            color_depth=ColorDepth.TRUE_COLOR,
        )

    def run(self) -> None:
        """Runs the app"""
        self.application.run()


if __name__ == "__main__":
    NotepadApp().run()
