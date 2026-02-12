from typing import TYPE_CHECKING

from threading import Thread

from PIL import Image
from pystray import Icon, Menu, MenuItem

from logic import Logic

if TYPE_CHECKING:
    from logic import Logic


class Tray(Icon):
    def __init__(self, name, logic: Logic):
        super().__init__(
            name=name,
            icon=Image.open("src/assets/images/logo.png"),
            menu=self.create_menu(),
        )
        self.logic: Logic = logic
        self.logic_thread = None

        self.is_running = True

        self.start_polling()

    def buttons_actions(self, icon, item):
        match item.text:
            case "Start":
                self.start_polling()

            case "Stop":
                self.stop_polling()

            case "Quit":
                self.stop_polling()
                icon.stop()
                print("🚩 Tray app was stopped")

    def change_buttons_visible(self, item):
        return item.text == ("Stop" if self.is_running else "Start")

    def create_menu(self):
        self.start_button = MenuItem(
            text="Start",
            action=self.buttons_actions,
            visible=self.change_buttons_visible,
        )
        self.stop_button = MenuItem(
            text="Stop",
            action=self.buttons_actions,
            visible=self.change_buttons_visible,
        )

        self.quit_button = MenuItem(text="Quit", action=self.buttons_actions)

        main_menu = Menu(
            self.start_button,
            self.stop_button,
            Menu.SEPARATOR,
            self.quit_button,
        )

        return main_menu

    def start_polling(self):
        if not self.logic_thread:
            self.logic_thread = Thread(target=self.logic.run)
            self.logic_thread.start()

        self.is_running = True

    def stop_polling(self):
        self.logic.stop(stop_polling=True)
        self.logic_thread = None
        self.is_running = False
