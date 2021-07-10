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


def parse_commands(command: str) -> None:
    """
    Simple function to parse some commands

    Args:
        command: a command input by the user
        session
    """
    if command.lower().startswith("echo"):
        print(command.replace(command.split()[0] + " ", ""))

    elif command.lower() in ["cls", "clear"]:
        clear()

    elif command.lower() in ["exit", "quit"]:
        sys.exit()

    else:
        print(f"command {command.split()[0]} not found")


def main() -> None:
    """Starts a REPL in the terminal."""
    session: PromptSession = PromptSession(completer=word_completer, style=style)

    while True:
        try:
            current_path = str(Path.cwd())
            command = session.prompt(current_path + "> ").strip()

            parse_commands(command)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

    sys.exit()


if __name__ == "__main__":
    main()
