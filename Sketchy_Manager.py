# Assuming you have not changed the general structure of the template no modification is needed in this file.
from . import commands
from .lib import fusion360utils as futil
import adsk.core, adsk.fusion, adsk.cam, traceback
import os
from . import config as cfg
from . import sketchy_utils as sketchy

def run(context):
    try:
        
        sketchy_manager_panel = sketchy.add_panel(panel_name=cfg.PANEL_NAME, panel_title=cfg.ADDIN_NAME)
        commands.start(panel=sketchy_manager_panel)  

    except:
        futil.handle_error('run')


def stop(context):
    try:
        # Remove all of the event handlers your app has created
        futil.clear_handlers()

        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.stop()

    except:
        futil.handle_error('stop')