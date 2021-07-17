import datetime
from pathlib import Path
from typing import List, Optional

from pythonping import ping


class Commands:
    """Commands for the Repl"""

    def __init__(self, current_path: Path):
        self.current_path = current_path
        self.alias = [
            "CD",
            "CLEAR",
            "CLS",
            "CWD",
            "DATE",
            "DEL",
            "DELTREE",
            "DIR",
            "ECHO",
            "EDIT",
            "EXIT",
            "FIND",
            "IMGVIEW",
            "MOVE",
            "PATH",
            "PING",
            "QUIT",
            "REN",
            "RD",
            "RMDIR",
            "TIME",
            "TREE",
            "TYPE",
        ]

    def change_dir(self, path: str) -> Path:
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
            self.current_path = dir_path.resolve()
        return self.current_path

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
            dir_path = self.current_path.joinpath(path).resolve()

        for dir in dir_path.iterdir():
            print(dir.name)

    def tree(self, path: Path, level: int = 0, infix: str = "├──") -> None:
        """
        Makes a tree view of all files and directories

        Args:
            path: path of the specified directory
        """
        path = self.current_path.joinpath(path).resolve()
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
        path_obj = self.current_path.joinpath(path).resolve()
        with path_obj.open("r") as f:
            print(f.read())

    def delete_file(self, file_paths: List[str]) -> None:
        """
        Delete one or multiple files

        Args:
            file_paths: list of file paths
        """
        for path_str in file_paths:
            path = self.current_path.joinpath(path_str).resolve()
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
        path = self.current_path.joinpath(dir_path).resolve()
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
        path = self.current_path.joinpath(dir).resolve()
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
        path = self.current_path.joinpath(name).resolve()
        base_path = path.parent
        if path.is_file():
            path.rename(base_path.joinpath(new_name).resolve())
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

    def move_file(self, src_path: str, dest_path: str) -> None:
        """
        Moves the specific file from one place to another

        Args:
            src_path: The source path where the file is located
            dest_path: The destination path where the file has to be moved
        """
        src_path_obj = self.current_path.joinpath(src_path).resolve()
        if not src_path_obj.exists():
            print(f"{src_path} does not exist")
            return
        elif not src_path_obj.is_file():
            print(f"{src_path} is not a file")
            return
        else:
            file_name = src_path_obj.name

        dest_path_obj = self.current_path.joinpath(dest_path).resolve()
        dest_path_obj = dest_path_obj.joinpath(file_name)

        if dest_path_obj.exists():
            while True:
                reply = input(
                    "The file exists do you want to replace it? (y/n): "
                ).lower()
                if reply == "y":
                    src_path_obj.replace(dest_path_obj)
                    break
                elif reply == "n":
                    print(end="")
                    break
                else:
                    print("Invalid option please enter the correct option")
        else:
            src_path_obj.replace(dest_path_obj)

    def ping_addr(self, addr: str) -> None:
        """
        Spawn a subprocess to ping the address

        Args:
            addr: The address of the website or the IP
            no_of_packets: No of packets to send. Defaults to 4.
        """
        ping(f"{addr}", verbose=True)

    def get_time(self, format: Optional[str] = None) -> None:
        """
        Show the time

        Args:
            format: Specify custom format if needed. Defaults to None.
        """
        if format is not None:
            print(datetime.datetime.now().strftime(format))
        else:
            print(datetime.datetime.now().strftime("%H:%M:%S"))

    def list_path(self, path: Optional[str] = None) -> None:
        """
        Print all the exe files in the given path

        Args:
            path: path to the directory
        """
        if path is not None:
            exe_files = list(self.current_path.joinpath(path).resolve().glob("*.exe"))
            for i in exe_files:
                print(self.current_path.joinpath(path).joinpath(i.name).resolve())
            if len(exe_files) < 1:
                print("No .exe files were found!")
        else:
            exe_files = list(self.current_path.resolve().glob("*.exe"))
            for i in exe_files:
                print(self.current_path.joinpath(i.name).resolve())
            if len(exe_files) < 1:
                print("No .exe files were found!")

    def find_text(self, filename: str, text: str) -> None:
        """
        Finds specific string in a given file

        Args:
            text: The string you want to search for.
            filename: The filename to search the string
        """
        ln_no = 1
        flag = 0
        try:
            with open(filename, "r") as f:
                for line in f:
                    if text in line:
                        ln_no += 1
                        flag = 1
                        print(f"String {text} found in line {ln_no}.")
        except FileNotFoundError:
            print(f"The file {filename} does not exist!")
        if flag == 0:
            print(f"String {text} was not found in the file!")
