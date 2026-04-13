# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file CustomTkinter desktop calculator app. The `Calculadora` class in `main.py` owns all UI, state, and evaluation logic.

## Running the App

```bash
python main.py
```

Requires a venv with `customtkinter` installed (`pip install -r requirements.txt`).

## Architecture

- **Single file:** `main.py` contains everything - UI construction in `__init__`, button creation in `crear_botones_basicos()` / `crear_botones_cientificos()`, callbacks in `on_click()` / `on_click_cientifico()`.
- **Two modes:** Basic and scientific. Mode toggle (`set_modo()`) changes window size and shows/hides scientific buttons via `grid()` / `grid_remove()`. Scientific buttons are stored in `self.botones_cientificos`.
- **Expression evaluation:** `evaluar_expresion()` uses a restricted `safe_dict` (no `__builtins__`) with `eval()`. Trig functions respect `self.usar_grados` (degrees/radians toggle via `toggle_angulo()`).
- **Display:** Uses digital-style fonts - tries DSEG fonts first, falls back to `Courier New` via `obtener_familia_fuente_digital()`.

## Conventions

- UI text and comments are in Spanish - keep new labels/messages consistent.
- Basic operators map to Python operators: `×`→`*`, `÷`→`/`.
- Scientific buttons insert text fragments (`sin(`, `sqrt(`, `**2`) rather than computing immediately.
- Error handling shows a blinking "INVALID OPERATION" overlay for 3 seconds.