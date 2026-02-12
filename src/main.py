from pathlib import Path

from logic import Logic
from tray import Tray


logic = Logic(
    editor="Code",
    wakapi_config_path=Path("~/wakapi/config.yml").expanduser().resolve(),
    timeout=0.5,
)
Tray(name="WakapiRunner", logic=logic).run()
