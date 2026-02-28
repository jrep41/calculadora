# Copilot instructions for this repo

## Project overview
- Single-file CustomTkinter GUI calculator in [main.py](main.py).
- App class `Calculadora` owns all UI, state, and evaluation logic; no separate modules.
- Two modes: basic and scientific. Mode toggles change window size and show/hide extra buttons.

## Key flows and patterns
- UI is built in `Calculadora.__init__()` using `CTkButton` and `CTkEntry` with `grid` layout.
- Scientific buttons are created in `crear_botones_cientificos()` and stored in `self.botones_cientificos` for show/hide.
- Button callbacks route to `on_click()` for basic keys and `on_click_cientifico()` for scientific keys.
- Expression evaluation uses `evaluar_expresion()` with a restricted `safe_dict` (no `__builtins__`) and `eval()`.
- Trig functions respect degree/radian toggle via `self.usar_grados` and `toggle_angulo()`.

## Conventions specific to this codebase
- UI text and comments are in Spanish; keep new labels/messages consistent.
- Scientific buttons insert text fragments (`sin(`, `log10(`, `**2`) rather than computing immediately.
- Mode toggles also adjust the display column span (4 vs 8 columns).

## Dependencies and integration points
- Uses `customtkinter` on top of standard `tkinter` (`messagebox`) and `math`.
- No external services or data files.

## Developer workflow
- Run the app: `python main.py` from the repo root (assumes a venv with `customtkinter` installed).
- No tests or build scripts in this repo.
