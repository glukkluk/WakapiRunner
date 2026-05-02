import platform
import subprocess

from pathlib import Path
from time import sleep

from psutil import Process, process_iter


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

        self.editor_exec = self.editor + self.suffix

        self.run_polling = False

    def get_process_by_name(self, name: str) -> Process | None:
        for process in process_iter(attrs=["name"]):
            if process.info.get("name") == name:
                return process

    def run(self, message: str = "🚩 Wakapi polling was started") -> None:
        print(message)

        self.run_polling = True

        while self.run_polling:
            self.editor_process: Process | None = self.get_process_by_name(
                name=self.editor_exec
            )
            self.wakapi_process: Process | None = self.get_process_by_name(
                name=f"{self.app_to_run}{self.suffix}"
            )

            if self.editor_process:
                if self.wakapi_process is None:
                    subprocess.Popen(
                        [
                            f"{self.app_to_run}{self.suffix}",
                            "--config",
                            str(self.wakapi_config_path),
                        ],
                    )
                    print("✅ Wakapi was started")

            else:
                if self.wakapi_process:
                    self.stop(
                        message=f"🚫 Wakapi was stopped. Editor <{self.editor}> is not running."
                    )

            sleep(self.timeout)

    def stop(
        self,
        message: str,
        stop_polling: bool = False,
    ) -> None:
        if self.wakapi_process:
            self.wakapi_process.kill()
            self.wakapi_process = None

        print(message)

        if stop_polling:
            self.run_polling = False
