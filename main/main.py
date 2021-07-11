import sys
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.styles import Style

word_completer = WordCompleter(
    ["cd", "dir", "cls", "clear", "echo", "exit", "quit", "rd", "type"],
    ignore_case=True,
)

style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


class Repl:
    """REPL class"""

    def __init__(self) -> None:
        self.current_path: Path = Path.cwd()

    def change_dir(self, path: str) -> None:
        """Change the current directory

        Args:
            path: directory path to switch to
        """
        dir_path = self.current_path.joinpath(path)
        if not dir_path.exists():
            print(f"{path} does not exist")
        elif not dir_path.is_dir():
            print(f"{path} is not a directory")
        else:
            self.current_path = Path(dir_path.resolve())

    def list_dir(self, path: str = "") -> None:
        """Lists all the files and directories in the path

        if None then use the current working dir as path

        Args:
            path: path of the specified directory
        """
        if path == "":
            dir_path = self.current_path
        else:
            dir_path = Path(path)

        for dir in dir_path.iterdir():
            print(dir)

    def show_file_content(self, path: str) -> None:
        """Get the file content and show it in the REPL

        Args:
            path: path of the specified file
        """
        with open(path, "r") as f:
            print(f.read())

    def delete_file(self, file_paths: list) -> None:
        """Delete one or multiple files

        Args:
            file_paths: list of file paths
        """
        for path in file_paths:
            path = Path(path)
            if path.is_file():
                path.unlink()
            else:
                print(f"{str(path)} is not a file")

    def remove_dir(self, dir_path: str) -> None:
        """Delete directory and its files recursively

        Args:
            path: path of directory
        """
        path = Path(dir_path)
        for child in path.glob("*"):
            if child.is_file():
                child.unlink()
            else:
                self.remove_dir(str(child))
        path.rmdir()

    def call_commands(self, input_text: str) -> None:
        """
        Simple function to call some commands after parsing args

        Args:
            input_text: input from the user
        """
        # Parse the input
        args_list = input_text.lower().split()
        try:
            command = args_list[0]
        except IndexError:
            print()
            return

        if len(args_list) == 1:
            command_input = []
        else:
            command_input = args_list[1:]

        # Call the commands
        if command == "echo":
            print(" ".join(command_input))

        elif command == "cd":
            self.change_dir(command_input[0])

        elif command == "dir":
            try:
                self.list_dir(command_input[0])
            except IndexError:
                self.list_dir()

        elif command == "type":
            self.show_file_content(command_input[0])

        elif command == "del":
            self.delete_file(command_input)

        elif command == "rd":
            self.remove_dir(command_input[0])

        elif command in ["cls", "clear"]:
            clear()

        elif command in ["exit", "quit"]:
            sys.exit()

        else:
            print(f"Command {command} not found")

    def start_repl(self) -> None:
        """Starts a REPL session in the terminal"""
        session: PromptSession = PromptSession(completer=word_completer, style=style)

        while True:
            try:
                text = session.prompt(str(self.current_path) + ">")
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

            self.call_commands(text)


if __name__ == "__main__":
    Repl().start_repl()
