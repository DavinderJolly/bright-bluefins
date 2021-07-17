import sys
from pathlib import Path
from typing import List

from commands import Commands
from notepad.notepad import NotepadApp
from photos.photos import ImageViewer
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.styles import Style
from styles.styles import AppStyles


class Repl:
    """REPL class"""

    def __init__(self, style: Style, word_list: List[str] = []):
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

    def parse_args(self, input_text: str) -> List[str]:
        """
        Takes a string with arguments and splits them intu a list of strings

        Args:
            input_text: arguments in a single string

        Returns:
            List[str]: arguments as a list of strings
        """
        if '"' in input_text:
            args_list = input_text.strip().split('"')
            args_list = [i for i in args_list if i != "" and i != " "]
            args_list = [i.strip() for i in args_list]
        else:
            args_list = input_text.strip().split()

        return args_list

    def call_commands(self, input_text: str) -> None:
        """
        Simple function to call some commands after parsing args

        Args:
            input_text: input from the user
        """
        args_list = self.parse_args(input_text)
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

        elif command == "edit":
            if command_input:
                path = self.current_path.joinpath(command_input[0]).resolve()
                if path.exists() and path.is_file():
                    NotepadApp(style=style, file_name=path).run()
            else:
                NotepadApp(style=style).run()

        elif command == "imgview":
            if command_input:
                path = self.current_path.joinpath(command_input[0]).resolve()
                if len(command_input) == 2:
                    mode = command_input[1]
                else:
                    mode = "ANSI"
                if path.exists() and path.is_file():
                    ImageViewer(path=path, mode=mode).run_app()

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
            else:
                print("Usage: DEL file1 file2 file3 ...")

        elif command == "deltree":
            if command_input:
                self.commands.del_tree(command_input[0])
            else:
                print("Usage: DELTREE dir_name")

        elif command == "move":
            if len(command_input) == 2:
                self.commands.move_file(command_input[0], command_input[1])
            else:
                print("Usage: MOVE source_path destination_path")

        elif command == "ping":
            if command_input:
                self.commands.ping_addr(command_input[0])
            else:
                print("Usage: PING address Optional[no_of_packets]")

        elif command == "path":
            if len(command_input) == 1:
                self.commands.list_path(command_input[0])
            elif len(command_input) == 0:
                self.commands.list_path()
            else:
                print("Usage: PATH Optional[path]")

        elif command in ["rd", "rmdir"]:
            if command_input:
                self.commands.remove_dir(command_input[0])
            else:
                print("Usage: RD dir_name")

        elif command == "ren":
            if len(command_input) == 2:
                self.commands.rename(command_input[0], command_input[1])
            else:
                print("Usage: REN old_name new_name")

        elif command == "date":
            if len(command_input) == 1:
                self.commands.get_date(command_input[0])
            elif len(command_input) == 0:
                self.commands.get_date()
            else:
                print("Usage: DATE Optional[format]")

        elif command == "time":
            if len(command_input) == 1:
                self.commands.get_time(command_input[0])
            elif len(command_input) == 0:
                self.commands.get_time()
            else:
                print("Usage: TIME Optional[format]")

        elif command == "find":
            if len(command_input) == 2:
                self.commands.find_text(command_input[0], command_input[1])
            else:
                print("Usage: FIND text path_to_file")

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
    style = AppStyles.style
    Repl(style).start_repl()
