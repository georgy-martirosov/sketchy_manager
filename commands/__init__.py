from .ToggleVisibilityForSketches import entry as ToggleVisibilityForSketches
from .ViewsCommander import entry as ViewsCommander
from .Feedback import entry as Feedback

commands = [
    ToggleVisibilityForSketches,
    ViewsCommander,
    Feedback
]

def start(panel=False):
    for command in commands:
        command.start(panel=panel)

def stop():
    for command in commands:
        command.stop()