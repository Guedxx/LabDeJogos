# King Pong

Climb the tower and become the King of Pong.

## About

King Pong is a reimagined Pong where you clear six opponents in sequence.
This version runs on `pygame-ce` with a scene-based architecture.

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

- `W`: move up
- `S`: move down
- `SPACE`: dash
- `ESC`: pause menu
- `N`: skip current level (goes to credits on final level)

## Testing

```bash
pytest -q
```

Headless mode is supported in tests via dummy SDL drivers.

## Code Overview

- `game.py`: top-level game loop and scene switching.
- `scenes/`: splash, menu, gameplay, pause, level-clear, game-over, and credits scenes.
- `logic/`: extracted pure gameplay rules (physics, AI core, collisions, power-up rules, helper movement).
- `assets.py`: cached image/audio loading.
- `settings.py`: gameplay constants and level configuration.
- `tests/`: unit and smoke tests.

