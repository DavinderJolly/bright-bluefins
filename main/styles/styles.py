from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls

from .bright_blue import BrightBlueStyle


class AppStyles:
    """Create unified styles"""

    notepad_style = Style.from_dict(
        {
            "top": "bg:#00AAAA #000000",
            "bottom": "bg:#00AAAA #000000",
            "shadow": "bg:#000000",
            "text-area": "bg:#0000AA #AAAAAA",
        }
    )
    photos_style = Style.from_dict({"frame": "bg:#AAAAAA #000000"})
    lexer_style = style_from_pygments_cls(BrightBlueStyle)

    style = merge_styles(
        [
            notepad_style,
            photos_style,
            lexer_style,
        ]
    )
