"""Provides AppHandler class in order to implement 'importing' of other apps into the OS"""
import typing as t
import warnings

import gui_automation
import PIL
import pyautogui
import pywinauto
from pywinauto.timings import Timings

warnings.simplefilter(
    "ignore", category=UserWarning
)  # Ignore automating 32-Bit with 64-Bit warning


class AppHandler:
    """Class to help with controlling applications and implement 'importing' of applications into the OS"""

    def __init__(
        self,
        selected_app: pywinauto.application.Application = None,
        backend: str = "win32",
    ):
        """
        Creates a new instance of the AppHandler class

        Args:
            selected_app: an app that will have methods performed on it (such as hide_app or show_app)
            backend: the backend to use. Acceptable options include 'win32' for win32 and 'uia' for MS Ui
        """
        Timings.fast()
        self.backend = backend
        self.selected_app = selected_app
        Timings.window_find_retry = 0.001

    def get_open_apps(self) -> t.List[pywinauto.application.Application]:
        """
        Returns a list of all open applications

        Returns:
            list[pywinauto.application.Application]: A list of all open applications

        """
        open_windows = [
            w
            for w in pywinauto.Desktop(backend=self.backend).windows(visible_only=True)
            if w.window_text() not in ("", "Taskbar")
        ]

        # Get a list of all open apps, only appends suitable apps and not background apps
        open_apps = []
        for window in open_windows:
            try:
                app = pywinauto.application.Application(backend=self.backend).connect(
                    process=window.process_id()
                )
            except pywinauto.application.ProcessNotFoundError:
                continue

            open_apps.append(app)

        return open_apps

    def get_open_app_names(
        self, apps: t.List[pywinauto.application.Application] = None
    ) -> t.List[str]:
        """
        Returns a list of all open app names/titles

        Args:
            apps: if not provided, calls `self.get_open_apps` and uses that

        Returns:
            A list of app names/titles
        """
        if apps is None:
            apps = self.get_open_apps()

        return [app.top_window().window_text() for app in apps]

    def hide_app(self, pos: t.List[int] = None) -> None:
        """
        Hides the selected_app by resizing it and moving it to an obscure position on the screen

        Args:
            pos: Optional arg, position where the window will move

        Returns:
            None

        """
        if self.selected_app is None:
            raise ValueError(
                "`self.selected_app` not assigned an app, cannot perform operation"
            )
        if pos is None:
            # Get the screen's size and add an offset to the y coordinate
            pos = list(pyautogui.size())
            pos[1] += 1000

        if self.backend == "win32":
            self.selected_app.window().wrapper_object().move_window(
                x=pos[0], y=pos[1], width=0, height=0
            )

        elif self.backend == "uia":
            # TODO Prevent window from receiving focus when moving and resizing
            self.selected_app.top_window().wrapper_object().iface_transform.resize(
                200, 200
            )
            self.selected_app.top_window().wrapper_object().iface_transform.move(
                pos[0], pos[1]
            )

    def show_app(self, pos: t.List[int] = None, size: t.List[int] = None) -> None:
        """
        Shows the app by moving and resizing it

        Opposite of hide_app, attempts to 'show' the selected_app by increasing size and bringing it towards the centre
        of the screen

        Args:
            pos: Optional arg, position where the window will move
            size: Optional arg, determines the size of the resized window

        Returns:
            None

        """
        if self.selected_app is None:
            raise ValueError(
                "`self.selected_app` not assigned an app, cannot perform operation"
            )

        if pos is None:
            # halves the screen size
            pos = [n // 1.5 for n in pyautogui.size()]

        if size is None:
            # Makes measurements by accounting for screen size
            size = [
                (sum(pyautogui.size()) * 2) // 10,
                (sum(pyautogui.size()) * 2) // 10,
            ]

        if self.backend == "win32":
            self.selected_app.window().wrapper_object().move_window(
                x=pos[0], y=pos[1], width=size[0], height=size[1]
            )

        elif self.backend == "uia":
            # TODO Prevent window from receiving focus when moving and resizing
            self.selected_app.top_window().wrapper_object().iface_transform.Move(
                0, pos[1]
            )
            self.selected_app.top_window().wrapper_object().iface_transform.Resize(
                size[0], size[1]
            )

    def get_screenshot_of_app(self) -> PIL.Image:
        """
        Takes a screenshot of the app and returns it

        Returns:
            PIL.Image
        """
        if self.selected_app is None:
            raise ValueError(
                "`self.selected_app` not assigned an app, cannot perform operation"
            )
        # self.selected_app.top_window().wrapper_object().set_focus()
        pywinauto.timings.wait_until(
            2,
            0.05,
            self.selected_app.top_window().wrapper_object().is_visible,
            True,
        )
        if self.backend == "win32":
            background_handler = (
                gui_automation.background_handler.BackgroundHandlerWin32(
                    self.selected_app.window().window_text()
                )
            )
            img = PIL.Image.fromarray(background_handler.screenshot())
        else:
            img = self.selected_app.window().wrapper_object().capture_as_image()
        return img
