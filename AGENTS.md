# AGENTS.md

## Developer Commands
- Run app: `uv run src/main.py` or `python src/main.py`
- Install dependencies: `uv sync` or `pip install -r requirements.txt`

## Core Architecture & Configuration
- **Entrypoint**: `src/main.py`
- **Logic**: `src/logic.py` handles process polling and `wakapi` lifecycle.
- **Configuration**: Hardcoded in `src/main.py` (see `Logic` instantiation):
  - `editor`: Current target process name (e.g., `"Code"`).
  - `wakapi_config_path`: Path to `wakapi` config file.
  - `timeout`: Polling interval in seconds.
- **Supported Editors**: `Code`, `Code - Insiders`, `pycharm64` (defined in `src/logic.py:9`).

## Constraints & Requirements
- **OS**: Windows only (despite generic platform checks in code).
- **External Dependency**: Requires `wakapi` CLI installed and available on the system `PATH`.
- **Python Version**: 3.13+
