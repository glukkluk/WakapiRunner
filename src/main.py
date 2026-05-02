from logic import Logic
from tray import Tray
from config import settings


logic = Logic(
    editor=settings.editor,
    wakapi_config_path=settings.get_wakapi_config_path(),
    timeout=settings.timeout,
)
Tray(name="WakapiRunner", logic=logic).run()
