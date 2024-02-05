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
        futil.clear_handlers()

        commands.stop()

    except:
        futil.handle_error('stop')