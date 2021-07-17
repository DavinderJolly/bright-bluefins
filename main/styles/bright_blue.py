from pygments.style import Style
from pygments.token import Comment, Keyword, Name, Number, Operator, String, Whitespace


class BrightBlueStyle(Style):
    """Theme style for notepad app"""

    styles = {
        Whitespace: "#AAAAAA",
        Comment: "noitalic #AAAA00",
        Keyword: "#00AA00",
        Keyword.Type: "#AA0000",
        Operator: "#666666",
        Operator.Word: "bold #AA0000",
        Name.Builtin: "#00AA00",
        Name.Function: "#000033",
        Name.Class: "#000033",
        Name.Namespace: "#000033",
        Name.Exception: "#AA0000",
        Name.Variable: "#0000AA",
        Name.Constant: "#AA0000",
        Name.Label: "#AAAA55",
        Name.Entity: "#AAAAAA",
        Name.Attribute: "#AAAA55",
        Name.Tag: "#00AA00",
        Name.Decorator: "#AA0000",
        String: "#AA0000",
        String.Doc: "noitalic #AAAA00",
        String.Symbol: "#AAAA00",
        Number: "#AAAAAA",
    }
