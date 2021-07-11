import sys
from pathlib import Path
from typing import List

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.styles import Style


class Repl:
    """REPL class"""

    def __init__(self, style: Style, word_list: List[str] = []) -> None:
        """
        Constructor for class Repl

        Args:
            style (prompt_toolkit.styles.Style): styles for the REPL
            word_list: list of extra words to add to the word_completer. Defaults to [].
        """
        self.current_path: Path = Path.cwd()
        self.style = style
        self.word_completer = WordCompleter(
            [
                "CD",
                "DIR",
                "CLS",
                "CLEAR",
                "ECHO",
                "EXIT",
                "QUIT",
                "RD",
                "RMDIR",
                "REN",
                "DELTREE",
                "TYPE",
            ]
            + word_list,
            ignore_case=True,
        )

    def change_dir(self, path: str) -> None:
        """
        Change the current directory

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
        """
        Lists all the files and directories in the path

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
        """
        Get the file content and show it in the REPL

        Args:
            path: path of the specified file
        """
        with open(path, "r") as f:
            print(f.read())

    def delete_file(self, file_paths: List[str]) -> None:
        """
        Delete one or multiple files

        Args:
            file_paths: list of file paths
        """
        for path_str in file_paths:
            path = Path(path_str)
            if path.is_file():
                path.unlink()
            else:
                print(f"{str(path)} is not a file")

    def del_tree(self, dir_path: str) -> None:
        """
        Delete directory and its files recursively

        Args:
            path: path of directory
        """
        path = Path(dir_path)
        for child in path.glob("*"):
            if child.is_file():
                child.unlink()
            else:
                self.del_tree(str(child))
        path.rmdir()

    def remove_dir(self, dir: str) -> None:
        """
        Removes an empty directory

        Args:
            dir: name of the directory to remove
        """
        path = Path(dir)
        if path.is_dir():
            if len(list(path.glob("*"))) == 0:
                path.rmdir()
            else:
                print("directory is not empty")
        else:
            print(f"{path} is not a directory")

    def rename(self, name: str, new_name: str) -> None:
        """
        Rename a file

        Args:
            dirname : a file to be renamed
            newname : the new name
        """
        path = Path("name")
        if path.is_file():
            path.rename(new_name)
        else:
            print(f"{path} is not a file")

    def call_commands(self, input_text: str) -> None:
        """
        Simple function to call some commands after parsing args

        Args:
            input_text: input from the user
        """
        # Parse the input
        args_list = input_text.strip().split()
        command_input = []
        if len(args_list) > 0:
            command = args_list[0].lower()
            if len(args_list) > 1:
                command_input = args_list[1:]
        else:
            print()
            return

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

        elif command == "deltree":
            self.del_tree(command_input[0])

        elif command in ["rd", "rmdir"]:
            self.remove_dir(command_input[0])

        elif command == "ren":
            if len(command_input) >= 2:
                self.rename(command_input[0], command_input[1])
            else:
                print("File name and new name required")

        elif command in ["cls", "clear"]:
            clear()

        elif command in ["exit", "quit"]:
            sys.exit()

        else:
            print(f"Command {command} not found")

    def start_repl(self) -> None:
        """Starts a REPL session in the terminal"""
        session: PromptSession = PromptSession(
            completer=self.word_completer, style=self.style
        )

        while True:
            try:
                text = session.prompt(str(self.current_path) + ">")
            except KeyboardInterrupt:
                print("^C")
                continue
            except EOFError:
                break

            self.call_commands(text)


if __name__ == "__main__":
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )
    Repl(style).start_repl()
