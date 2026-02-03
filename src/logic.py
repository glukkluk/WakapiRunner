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

        if self.editor not in SupportedEditors:
            raise Exception("Not supported editor.")

        self.editor_exec = self.editor + self.suffix

        self.wakapi_is_running = False
        self.run_polling = False

    def get_process_by_name(self, name: str) -> Process | None:
        for process in process_iter(attrs=["name"]):
            if process.info.get("name") == name:
                return process

    def run(self) -> None:
        print("🚩 Wakapi polling was started")

        self.run_polling = True

        while self.run_polling:
            self.editor_process: Process | None = self.get_process_by_name(
                name=self.editor_exec
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

                    print("🚩 Wakapi was started")

            else:
                self.stop(message=f"🚩 Editor {self.editor} is not running")

            sleep(self.timeout)

    def stop(
        self, stop_polling: bool = False, message: str = "🚩 Wakapi polling was stopped"
    ) -> None:
        if self.wakapi_process:
            self.wakapi_process.kill()
            self.wakapi_process = None

        self.wakapi_is_running = False

        print(message)

        if stop_polling:
            self.run_polling = False
