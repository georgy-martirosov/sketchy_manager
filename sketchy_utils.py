import os
import inspect
import traceback
import adsk.core
from .lib import fusion360utils as futil

app = adsk.core.Application.get()
ui = app.userInterface
cmdDefs = ui.commandDefinitions
workspaces = ui.workspaces


def get_resources_path():
    frame = inspect.stack()[2]
    p = frame[0].f_code.co_filename
    dir = os.path.dirname(os.path.realpath(p))
    resource_folder = os.path.join(dir, 'resources')
    return resource_folder

def add_panel(panel_name="not_so_default_panel", panel_title=""):
    modeling_workspace = workspaces.itemById('FusionSolidEnvironment')
    toolbarPanels = modeling_workspace.toolbarPanels
    custom_panel = toolbarPanels.itemById(panel_name)
    if not custom_panel:
        custom_panel = toolbarPanels.add(panel_name, 
                                            panel_title, 
                                            panel_name, 
                                            False)
    
    return custom_panel

def add_button(button_id="not_so_default_button", button_title="", button_tooltip="", panel=False, event_handler=False, handlers=[], resources=""):

    # script_folder = get_resources_path()
    # resource_folder = os.path.join(script_folder, 'resources')
    resource_folder = get_resources_path()
    if (resources):
        resource_folder = os.path.join(resource_folder, resources)

    button = cmdDefs.itemById(button_id)
    if not button:
        button = cmdDefs.addButtonDefinition(button_id, 
                                                button_title, 
                                                button_tooltip, 
                                                resource_folder)

    onCommandCreated = event_handler()
    button.commandCreated.add(onCommandCreated)
    handlers.append(onCommandCreated)  # Add the handler to the global handlers list

    toolbarControl = panel.controls.itemById(button_id)

    if not toolbarControl:
        toolbarControl = panel.controls.addCommand(button)

    return button, toolbarControl