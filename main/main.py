import sys
from pathlib import Path
from typing import Callable, List, Sequence, Union

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

    def print_function(self, msg: str = "") -> None:
        """Print text without newline character"""
        print(msg, end="")

    def exec_command(
        self,
        command: Callable,
        args: Sequence[Union[str, List[str], Path]] = (),
        fallback_command: Callable = print_function,
        fallback_arg: Union[str, Path] = "",
    ) -> None:
        """
        Execute the command with right input or fallback

        Args:
            command: command method name
            args: arguments of the command
            idx: index of argument, if idx == -1 it is not used
            fallback_command: alternate command
            fallback_arg: argument of the fallback command
        """
        try:
            command(*args)
        except IndexError:
            fallback_command(fallback_arg)

    def call_commands(self, input_text: str) -> None:
        """
        Simple function to call some commands after parsing args

        Args:
            input_text: input from the user
        """
        # Parse the input
        if '"' in input_text:
            args_list = input_text.strip().split('"')
            args_list = [i for i in args_list if i != "" and i != " "]
            args_list = [i.strip() for i in args_list]
        else:
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
            else:
                self.print_function()

        elif command == "dir":
            if command_input:
                self.exec_command(
                    command=self.commands.list_dir,
                    args=(command_input[0],),
                    fallback_command=self.commands.list_dir,
                )
            else:
                self.exec_command(
                    command=self.commands.list_dir,
                    fallback_command=self.commands.list_dir,
                )

        elif command == "tree":
            if command_input:
                self.exec_command(
                    command=self.commands.tree,
                    args=(Path(command_input[0]),),
                    fallback_command=self.commands.tree,
                    fallback_arg=self.current_path,
                )
            else:
                self.exec_command(
                    command=self.commands.tree,
                    args=(self.current_path,),
                )

        elif command == "type":
            if command_input:
                self.exec_command(
                    command=self.commands.show_file_content, args=(command_input[0],)
                )
            else:
                print("Usage: TYPE file_name")

        elif command == "del":
            self.exec_command(command=self.commands.delete_file, args=(command_input,))

        elif command == "deltree":
            if command_input:
                self.exec_command(command=self.commands.del_tree, args=(command_input,))
            else:
                print("Usage: DELTREE dir_name")

        elif command in ["rd", "rmdir"]:
            if command_input:
                self.exec_command(
                    command=self.commands.remove_dir, args=(command_input,)
                )
            else:
                print("Usage: RD dir_name")

        elif command == "ren":
            if len(command_input) >= 2:
                self.exec_command(
                    command=self.commands.rename,
                    args=(command_input[0], command_input[1]),
                )

            else:
                print("Usage: REN old_name new_name")

        elif command == "date":
            if command_input:
                self.exec_command(
                    command=self.commands.get_date,
                    args=(command_input[0],),
                    fallback_command=self.commands.get_date,
                )
            else:
                self.exec_command(
                    command=self.commands.get_date,
                    args=(),
                    fallback_command=self.commands.get_date,
                )

        elif command == "move":
            if len(command_input) >= 2:
                self.exec_command(
                    command=self.commands.move_file,
                    args=(command_input[0], command_input[1]),
                    fallback_command=self.commands.move_file,
                )
            else:
                print("Usage: MOVE path_to_source_file destination_for_file")

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
