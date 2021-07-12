import datetime
from pathlib import Path
from typing import List, Optional


class Commands:
    """Commands for the Repl"""

    def __init__(self, current_path: Path) -> None:
        self.current_path = current_path
        self.alias = [
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
            "DATE",
        ]

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

    def tree(self, path: Path, level: int = 0, infix: str = "├──") -> None:
        """
        Makes a tree view of all files and directories

        Args:
            path: path of the specified directory
        """
        if path.is_dir():
            if level == 0:
                print("{}{}{}".format("", "└──", str(path.name)))
            else:
                print(
                    "{}{}{}".format(
                        "    " + (level - 1) * "│   ", "├──", str(path.name)
                    )
                )
            childs = [child for child in path.glob("*")]
            if childs == []:
                level -= 1
                return
            last_child = childs.pop()
            for child in childs:
                level += 1
                self.tree(child, level)
                level -= 1
            self.tree(last_child, level + 1, infix="└──")
        else:
            print("{}{}{}".format("    " + (level - 1) * "│   ", infix, str(path.name)))
        level -= 1

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

    def get_date(self, format: Optional[str] = None) -> None:
        """
        Prints the current date & time, format argument can be given with a unix format

        Args:
            format (optional): unix format to format the datetime. Defaults to None.
        """
        if format is not None:
            print(datetime.datetime.now().strftime(format))
        else:
            print(datetime.datetime.now().strftime("%d-%m-%Y"))
