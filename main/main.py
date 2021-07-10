from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

word_completer = WordCompleter([], ignore_case=True)

style = Style.from_dict(
    {
        "completion-menu.completion": "bg:#008888 #ffffff",
        "completion-menu.completion.current": "bg:#00aaaa #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)


def main() -> None:
    """Starts a REPL in the terminal."""
    session = PromptSession(completer=word_completer, style=style)

    current_path = str(Path.cwd())

    while True:
        try:
            text = session.prompt(current_path + ">")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            print(text)

    print("Exiting...")


if __name__ == "__main__":
    main()
