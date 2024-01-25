import adsk.core, adsk.fusion, adsk.cam, traceback
import os
from ...lib import fusion360utils as futil
from ... import config as cfg
from ... import sketchy_utils as sketchy


# Global list to keep references to handlers to avoid premature garbage collection
handlers = []
app = adsk.core.Application.get()
ui = app.userInterface
design = adsk.fusion.Design.cast(app.activeProduct)
cmdDefs = ui.commandDefinitions
sketches = []
hidden_sketches = []
currentStateIsHidden = False
currentStateIsHiddenAll = False


def toggleVisibility(components, isToggle=True):
    global hidden_sketches, currentStateIsHidden

    if currentStateIsHidden:
        # show logic    
        for sketch in hidden_sketches:
            sketch.isVisible = True
        
        hidden_sketches = []
        currentStateIsHidden = False
    else:
        # hide logic    
        for component in components:
            for sketch in component.sketches:
                if sketch.isVisible:
                    sketch.isVisible = False
                    hidden_sketches.append(sketch)

        currentStateIsHidden = True
    
def showHideAll(components):
    global currentStateIsHiddenAll, currentStateIsHidden

    for component in components:
        for sketch in component.sketches:
            if currentStateIsHiddenAll or currentStateIsHidden:
                sketch.isVisible = True
            else:
                sketch.isVisible = False

    currentStateIsHiddenAll = not currentStateIsHiddenAll
    currentStateIsHidden = currentStateIsHiddenAll

def hide_sketches(sketch_array):
    for sketch in sketch_array:
        sketch.isVisible = False
        sketch.attributes.add(name="user_hidden", groupName="sketchy_manager", value="True")
    

def show_sketches(sketch_array):
    for sketch in sketch_array:
        sketch.isVisible = True
        sketch.attributes.add(name="user_hidden", groupName="sketchy_manager", value="False")


class CreateHandlerToggle(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):    
        global hidden_sketches

        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)
        cmd = args.command

        onExecute = ActionHandlerToggle()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)  # Add the handler to the global handlers list

        onDestroy = DestroyHandlerToggle()
        cmd.destroy.add(onDestroy)
        handlers.append(onDestroy)  # Add the handler to the global handlers list

class ActionHandlerToggle(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            design = adsk.fusion.Design.cast(app.activeProduct)
            all_components = design.allComponents

            toggleVisibility(all_components)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class DestroyHandlerToggle(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        pass  # Don't terminate the add-in

class CreateHandlerShowAll(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):    
        global hidden_sketches

        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)
        cmd = args.command

        onExecute = ActionHandlerShowAll()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)  # Add the handler to the global handlers list

        onDestroy = DestroyHandlerShowAll()
        cmd.destroy.add(onDestroy)
        handlers.append(onDestroy)  # Add the handler to the global handlers list

class ActionHandlerShowAll(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            design = adsk.fusion.Design.cast(app.activeProduct)
            all_components = design.allComponents

            showHideAll(all_components)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class DestroyHandlerShowAll(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        pass  # Don't terminate the add-in

class CreateHandlerShowActive(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):    
        global hidden_sketches

        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)
        all_components = design.allComponents
        cmd = args.command

        onExecute = ActionHandlerShowActive()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)  # Add the handler to the global handlers list

        onDestroy = DestroyHandlerShowActive()
        cmd.destroy.add(onDestroy)
        handlers.append(onDestroy)  # Add the handler to the global handlers list

class ActionHandlerShowActive(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            global design
            component = design.activeComponent

            showHideAll([component])

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class DestroyHandlerShowActive(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        pass  # Don't terminate the add-in

# Startup function for the add-in
def start(panel):
    try:
        sketchy.add_button(
            button_id='sketch_visibility_toggle' + cfg.BUTTON_NAME    ,
            button_title="Toggle sketches visibility", 
            button_tooltip="Toggle the visibility of sketches in the active design.",
            panel=panel, 
            event_handler=CreateHandlerToggle, 
            handlers=handlers)
        sketchy.add_button(
            button_id='show_hide_all_sketches' + cfg.BUTTON_NAME    ,
            button_title="Show/hide all sketches", 
            # button_tooltip="Toggle the visibility of sketches in the active design.",
            panel=panel, 
            event_handler=CreateHandlerShowAll, 
            handlers=handlers)
        sketchy.add_button(
            button_id='show_hide_active_component_sketches' + cfg.BUTTON_NAME    ,
            button_title="Show/hide sketches in active component", 
            # button_tooltip="Toggle the visibility of sketches in the active design.",
            panel=panel, 
            event_handler=CreateHandlerShowActive, 
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

