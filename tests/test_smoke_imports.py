import importlib


def test_core_modules_importable():
    modules = [
        "game",
        "ai",
        "logic.physics",
        "logic.ai_core",
        "logic.powerups",
        "scenes.gameplay_scene",
    ]
    for module in modules:
        importlib.import_module(module)

