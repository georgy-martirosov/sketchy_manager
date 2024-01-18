import adsk.core, adsk.fusion, adsk.cam, traceback
import os
from ...lib import fusion360utils as futil
from ... import config as cfg
from ... import sketchy_utils as sketchy


# Global list to keep references to handlers to avoid premature garbage collection
handlers = []
app = adsk.core.Application.get()
ui = app.userInterface
cmdDefs = ui.commandDefinitions


def collect_visible_sketches(components):
    visible_sketches_array_local = []
    for component in components:
        for sketch in component.sketches:
            if sketch.isVisible:
                visible_sketches_array_local.append(sketch)
            elif sketch.attributes.itemByName(name="user_hidden", groupName="sketchy_manager"):
                visible_sketches_array_local.append(sketch)

    return visible_sketches_array_local
    
def hide_sketches(sketch_array):
    for sketch in sketch_array:
        sketch.isVisible = False
        sketch.attributes.add(name="user_hidden", groupName="sketchy_manager", value="True")
    

def show_sketches(sketch_array):
    for sketch in sketch_array:
        sketch.isVisible = True
        sketch.attributes.add(name="user_hidden", groupName="sketchy_manager", value="False")


class ToggleSketchVisibilityCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):    
        cmd = args.command

        onExecute = ToggleSketchVisibilityHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)  # Add the handler to the global handlers list

        onDestroy = ToggleSketchVisibilityDestroyHandler()
        cmd.destroy.add(onDestroy)
        handlers.append(onDestroy)  # Add the handler to the global handlers list

class ToggleSketchVisibilityHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            design = adsk.fusion.Design.cast(app.activeProduct)
            all_components = design.allComponents

            is_sketches_hidden = app.activeProduct.rootComponent.attributes.itemByName(name="visible_sketches_hidden", groupName="sketchy_manager")

            if not is_sketches_hidden:
                is_sketches_hidden = False
            else:
                is_sketches_hidden = eval(is_sketches_hidden.value)
            
            visible_sketches_array = collect_visible_sketches(all_components)

            if not visible_sketches_array:
                visible_sketches_array = []
            else:
                visible_sketches_array = collect_visible_sketches(all_components)
            
            
            if is_sketches_hidden:
                hide_sketches(visible_sketches_array)
            else:
                show_sketches(visible_sketches_array)

            is_sketches_hidden = not is_sketches_hidden    
            app.activeProduct.rootComponent.attributes.add(value=str(is_sketches_hidden), name="visible_sketches_hidden", groupName="sketchy_manager")

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class ToggleSketchVisibilityDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        pass  # Don't terminate the add-in

# Startup function for the add-in
def start(panel):
    try:

        button_id = 'sketch_visibility_toggle' + cfg.BUTTON_NAME    

        button = sketchy.add_button(
            button_id=button_id,
            button_title="Toggle sketches visibility", 
            button_tooltip="Toggle the visibility of sketches in the active design.",
            panel=panel, 
            event_handler=ToggleSketchVisibilityCreatedHandler, 
            handlers=handlers)
    
        # Register the add-in to run continuously
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Shutdown function for the add-in
def stop():
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Clean up the UI
        cmdDef = ui.commandDefinitions.itemById('toggleSketchVisibilityButton')
        if cmdDef:
            cmdDef.deleteMe()

        workspaces = ui.workspaces
        modeling_workspace = workspaces.itemById('FusionSolidEnvironment')
        toolbarPanels = modeling_workspace.toolbarPanels
        custom_panel = toolbarPanels.itemById(cfg.PANEL_NAME)
        if custom_panel:
            toolbarControl = custom_panel.controls.itemById('toggleSketchVisibilityButton')
            if toolbarControl:
                toolbarControl.deleteMe()
            custom_panel.deleteMe()

        # Remove event handlers
        button = ui.commandDefinitions.itemById('toggleSketchVisibilityButton')
        if button:
            for handler in handlers:
                button.commandCreated.remove(handler)

        # Clear the handlers list
        handlers.clear()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

