<p align="center">
    <img src="src/assets/images/logo.png" width="350">
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3130/"><img src="https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=fff" alt="Python 3.13+" /></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License: Apache 2.0" /></a>
  <a href="https://wakapi.dev/"><img src="https://img.shields.io/badge/wakapi-%E2%9A%A1%EF%B8%8F-green" alt="Wakapi" /></a>
  <a href="https://img.shields.io/badge/status-experimental-orange"><img src="https://img.shields.io/badge/status-experimental-orange" alt="Status: Experimental" /></a>
  <a href="https://img.shields.io/badge/maintained-yes-brightgreen"><img src="https://img.shields.io/badge/maintained-yes-brightgreen" alt="Maintained" /></a>
</p>

# WakapiRunner

**WakapiRunner** is a small cross-platform tray utility that automatically starts `wakapi` when a supported editor is running, and stops it when the editor exits.

It is designed to make using [Wakapi](https://wakapi.dev/) seamless by ensuring the wakapi daemon only runs while you are actively coding.

## 🚀 Features

- ✅ Automatically starts `wakapi` when a supported editor is detected running
- ✅ Stops `wakapi` when you close the editor
- ✅ Lightweight system tray UI with Start / Stop / Quit controls
- ✅ Configurable editor target and Wakapi config path

## 🧩 Supported Platforms

- Windows
- 🚫 macOS
- 🚫 Linux

## 🧰 Requirements

- Python 3.13+
- `wakapi` CLI installed and available on your PATH

## 📦 Dependencies

This project uses:

- `pillow` (for tray icon handling)
- `psutil` (to detect running processes)
- `pystray` (system tray menu)

## ⚙️ Configuration

By default, `WakapiRunner` is configured in `src/main.py` as follows:

- `editor`: `"Code"` (Visual Studio Code)
- `wakapi_config_path`: `~/wakapi/config.yml`
- `timeout`: `0.5` (seconds between polling cycles)

### Supported editors

The project currently supports these process names (case sensitive):

- `Code` (VS Code)
- `Code - Insiders` (VS Code Insiders)
- `pycharm64` (JetBrains PyCharm)

To use a different editor, update the `editor` argument in `src/main.py` and ensure it matches the running process name.

## ▶️ Usage

### Run directly

```bash
python src/main.py
```

### Run as a module (if your environment supports it)

```bash
python -m src.main
```

Once started, a tray icon is created. Use the menu to:

- **Start**: Begin polling for the editor and auto-launch `wakapi`.
- **Stop**: Stop polling and stop `wakapi` if it is running.
- **Quit**: Exit the tray application.

## 🧠 How it works

1. The tray app spawns a background polling thread.
2. Every `timeout` seconds it checks whether the configured editor process is running.
3. If the editor is running and `wakapi` is not, it starts `wakapi` with the configured `--config` path.
4. If the editor is not running, it stops `wakapi`.

## 🛠️ Development

Install dependencies:

Using [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

Or using [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

Run in development mode:

```bash
python src/main.py
```

Or via uv

```bash
uv run src/main.py
```

## 🧩 Packaging

This is a small Python project; feel free to package it with tools like `pyinstaller`, `shiv`, or `pipx`.

## 📝 Notes

- `WakapiRunner` assumes `wakapi` is on your PATH. If it is not, adjust your environment or invoke `wakapi` via a full path in `src/logic.py`.
- If you want to use a different wakapi config file, set `wakapi_config_path` accordingly.
