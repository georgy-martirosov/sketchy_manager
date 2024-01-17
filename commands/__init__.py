from .ToggleVisibilityForSketches import entry as ToggleVisibilityForSketches

commands = [
    ToggleVisibilityForSketches
]

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()