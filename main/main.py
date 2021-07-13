import sys
from pathlib import Path
from typing import List

from commands import Commands
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
        self.commands = Commands(self.current_path)
        self.word_completer = WordCompleter(
            self.commands.alias + word_list,
            ignore_case=True,
        )

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
            if command_input:
                self.current_path = self.commands.change_dir(command_input[0])

        elif command == "dir":
            if command_input:
                self.commands.list_dir(command_input[0])
            else:
                self.commands.list_dir()

        elif command == "tree":
            if command_input:
                self.commands.tree(Path(command_input[0]))
            else:
                self.commands.tree(self.current_path)

        elif command == "type":
            if command_input:
                self.commands.show_file_content(command_input[0])
            else:
                print("Usage: TYPE file_name")

        elif command == "del":
            if command_input:
                self.commands.delete_file(command_input)

        elif command == "deltree":
            if command_input:
                self.commands.del_tree(command_input[0])
            else:
                print("Usage: DELTREE dir_name")

        elif command in ["rd", "rmdir"]:
            if command_input:
                self.commands.remove_dir(command_input[0])
            else:
                print("Usage: RD dir_name")

        elif command == "ren":
            if len(command_input) >= 2:
                self.commands.rename(command_input[0], command_input[1])
            else:
                print("Usage: REN old_name new_name")

        elif command == "date":
            if command_input:
                self.commands.get_date(command_input[0])
            else:
                self.commands.get_date()

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
