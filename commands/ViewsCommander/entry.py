import adsk.core, adsk.fusion, adsk.cam, traceback
import os
from ...lib import fusion360utils as futil
from ... import config as cfg
from ... import sketchy_utils as sketchy

handlers = []
app = adsk.core.Application.get()
ui = app.userInterface
cmdDefs = ui.commandDefinitions

named_views_default = [
    'FRONT',
    'TOP',
    'HOME',
    'RIGHT'
    ]

named_views_all = []

def collect_named_views():    
    named_views = []
    
    if app.activeProduct.namedViews.count > 0:
        for index in range(0, app.activeProduct.namedViews.count):
            named_views.append(app.activeProduct.namedViews.item(index).name)

    named_views.extend(named_views_default)

    return named_views

def switch_through_named_views():
    global named_views_all

    app.activeProduct.namedViews.itemByName(named_views_all.pop()).apply()

class CreateHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        cmd = args.command

        onExecute = ActionHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)  # Add the handler to the global handlers list

        onDestroy = DestroyHandler()
        cmd.destroy.add(onDestroy)
        handlers.append(onDestroy)  # Add the handler to the global handlers list

class DestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        cmd = args.command

class ActionHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        global named_views_all
        cmd = args.command    
        if len(named_views_all) == 0:
            named_views_all = collect_named_views()
        
        switch_through_named_views()    

def start(panel):
    try:
        button_id = 'named_views_controls' + cfg.BUTTON_NAME

        button = sketchy.add_button(
            button_id=button_id,
            button_title="Cycle views", 
            button_tooltip="Cycle swithes between named views",
            panel=panel, 
            event_handler=CreateHandler, 
            handlers=handlers
            )

        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop():
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
