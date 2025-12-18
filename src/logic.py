import platform
import subprocess

from pathlib import Path
from time import sleep

from psutil import Process, process_iter

SupportedEditors: list[str] = ["Code", "Code - Insiders", "pycharm64"]


class Logic:
    def __init__(self, editor: str, wakapi_config_path: Path, timeout: float) -> None:
        self.app_to_run = "wakapi"

        self.editor: str = editor
        self.wakapi_config_path: Path = wakapi_config_path
        self.timeout: float = timeout

        self.wakapi_process = None

        match platform.system():
            case "Windows":
                self.suffix = ".exe"

            case "Darwin":
                self.suffix = ""

            case "Linux":
                self.suffix = ""

            case _:
                raise Exception("Not supported OS.")

        self.wakapi_is_running = False

    def choose_editor(self) -> str | None:
        if self.editor in SupportedEditors:
            return f"{self.editor}{self.suffix}"

        else:
            raise Exception("Not supported editor.")

    def get_process_by_name(self, name) -> Process | None:
        for process in process_iter():
            if process.name() == name:
                return process

    def run(self) -> None:
        while True:
            self.editor_process: Process | None = self.get_process_by_name(
                name=self.choose_editor()
            )
            self.wakapi_process: Process | None = self.get_process_by_name(
                name=f"{self.app_to_run}{self.suffix}"
            )

            if self.editor_process:
                if not self.wakapi_is_running:
                    subprocess.Popen(
                        [
                            f"{self.app_to_run}{self.suffix}",
                            "--config",
                            f"{self.wakapi_config_path}",
                        ],
                    )
                    self.wakapi_is_running = True

            else:
                if self.wakapi_process:
                    self.wakapi_process.terminate()

                self.wakapi_is_running = False

            sleep(self.timeout)

    def stop(self):
        if self.wakapi_process:
            self.wakapi_process.kill()


if __name__ == "__main__":
    app = Logic(
        editor="Code",
        wakapi_config_path=Path("~/wakapi/config.yml").expanduser().resolve(),
        timeout=0.5,
    )

    app.run()
