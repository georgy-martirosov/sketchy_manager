from .ToggleVisibilityForSketches import entry as ToggleVisibilityForSketches
from .ViewsCommander import entry as ViewsCommander

commands = [
    ToggleVisibilityForSketches,
    ViewsCommander
]

def start(panel=False):
    for command in commands:
        command.start(panel=panel)

def stop():
    for command in commands:
        command.stop()