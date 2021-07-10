import sys
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.styles import Style

word_completer = WordCompleter(
    ["cls", "clear", "exit", "quit", "echo"], ignore_case=True
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
        self.current_path = self.current_path / path
        self.current_path = Path(self.current_path.resolve())

    def parse_commands(self, command: str) -> None:
        """
        Simple function to parse some commands

        Args:
            command: a command input by the user
            session
        """
        if command.lower().startswith("echo"):
            print(command.replace(command.split()[0] + " ", ""))

        elif command.lower().startswith("cd "):
            self.change_dir(command[3:])

        elif command.lower() in ["cls", "clear"]:
            clear()

        elif command.lower() in ["exit", "quit"]:
            sys.exit()

        else:
            print(f"command {command.split()[0]} not found")

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

            self.parse_commands(text)

        print("Exiting...")


if __name__ == "__main__":
    Repl().start_repl()
