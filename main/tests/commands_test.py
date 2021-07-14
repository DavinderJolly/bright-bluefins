import datetime
from pathlib import Path

import pytest

from .. import commands


@pytest.fixture()
def cmds() -> commands.Commands:
    """
    Fixture that creates a Repl object

    Returns: Repl
    """
    return commands.Commands(Path.cwd())


def test_cd(cmds: commands.Commands) -> None:
    """
    Unit test for the cd command

    Args:
        cmds: object returned by the Commands class
    """
    check_path = cmds.current_path.joinpath("main")
    cmds.change_dir("./main")
    assert cmds.current_path == check_path
    check_path = cmds.current_path.parent
    cmds.change_dir("..")
    assert cmds.current_path == check_path


def test_dir(cmds: commands.Commands, capsys: pytest.CaptureFixture) -> None:
    """
    Unit test for the dir command

    Args:
        cmds: object returned by the Commands class
        capsys: CaptureFixture object
    """
    cmds.list_dir()
    out, err = capsys.readouterr()
    assert out == "\n".join([dir.name for dir in cmds.current_path.iterdir()]) + "\n"
    assert err == ""
    cmds.list_dir("./main")
    out, err = capsys.readouterr()
    assert (
        out
        == "\n".join([dir.name for dir in cmds.current_path.joinpath("main").iterdir()])
        + "\n"
    )
    assert err == ""


def test_del(cmds: commands.Commands) -> None:
    """
    Unit test for the del command

    Args:
        cmds: object returned by the Commands class
        capsys: CaptureFixture object
    """
    path = Path("hello.txt")
    with path.open("w") as f:
        f.write("hello world")

    assert path.exists()
    cmds.delete_file([str(path)])
    assert not path.exists()


def test_rd(cmds: commands.Commands, capsys: pytest.CaptureFixture) -> None:
    """
    Unit test for the rd command

    Args:
        cmds: object returned by the Commands class
        capsys: CaptureFixture object
    """
    path = Path("hello")
    path.mkdir()
    assert path.exists() and path.is_dir()
    cmds.remove_dir(path.name)
    assert not (path.exists() or path.is_dir())
    cmds.remove_dir(path.name)
    out, err = capsys.readouterr()
    assert out == f"{str(path.resolve())} is not a directory\n"
    assert err == ""


def test_type(cmds: commands.Commands, capsys: pytest.CaptureFixture) -> None:
    """
    Unit Test for type command

    Args:
        cmds: object returned by the Commands class
        capsys: CaptureFixture object
    """
    path = Path("hello.txt")
    with path.open("w") as f:
        f.write("hello world")
    cmds.show_file_content("hello.txt")
    out, err = capsys.readouterr()
    Path.unlink(path)
    assert out == "hello world\n"
    assert err == ""


def test_ren(cmds: commands.Commands, capsys: pytest.CaptureFixture) -> None:
    """
    Unit Test for ren command

    Args:
        cmds: object returned by the Commands class
        capsys: CaptureFixture object
    """
    path = Path("test_ren.txt")
    with path.open("w") as f:
        f.write("hello world")
    new_name = Path("test.txt")
    cmds.rename(path.name, new_name.name)
    assert new_name.exists()
    new_name.unlink()
    cmds.rename(new_name.name, "fail.txt")
    out, err = capsys.readouterr()
    assert out == f"{str(new_name.resolve())} is not a file\n"
    assert err == ""


def test_date(cmds: commands.Commands, capsys: pytest.CaptureFixture) -> None:
    """
    Unit Test for date command

    Args:
        cmds: object returned by the Commands class
        capsys: CaptureFixture object"""
    cmds.get_date()
    out, err = capsys.readouterr()
    assert out == datetime.datetime.now().strftime("%d-%m-%Y") + "\n"
    cmds.get_date("%H:%M")
    assert err == ""
    out, err = capsys.readouterr()
    assert out == datetime.datetime.now().strftime("%H:%M") + "\n"
    assert err == ""
