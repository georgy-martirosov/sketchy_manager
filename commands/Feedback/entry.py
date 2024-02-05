import adsk.core, adsk.fusion, adsk.cam, traceback
import os
from ...lib import fusion360utils as futil
from ... import config as cfg
from ... import sketchy_utils as sketchy
import webbrowser


handlers = []
app = adsk.core.Application.get()
ui = app.userInterface
cmdDefs = ui.commandDefinitions
rating = False

def openReviewPage():
    return False

def createRatingBlock(parent, id, label):
    ratingBlock = parent.addDropDownCommandInput(
        id + cfg.ADDIN_NAME,
        label,
        adsk.core.DropDownStyles.LabeledIconDropDownStyle
    )

    ratingBlockItems = ratingBlock.listItems
    ratingBlockItems.add(
        "Choose rating", 
        True
    )
    for r in range(1, 6):
        ratingBlockItems.add(
            str(r), 
            False
        )
    

    return ratingBlock

def CreateReviewDialog(ci):
    featuresRating = createRatingBlock(ci, "review_features", "Features")
    usabilityRating = createRatingBlock(ci, "review_usability", "Usability")
    overallRating = createRatingBlock(ci, "review_rating", "Overall rating")

class CreateHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        cmd = args.command
        ci = cmd.commandInputs

        onExecute = ActionHandler()
        cmd.execute.add(onExecute)
        handlers.append(onExecute)  # Add the handler to the global handlers list

        onDestroy = DestroyHandler()
        cmd.destroy.add(onDestroy)
        handlers.append(onDestroy)  # Add the handler to the global handlers list

        # CreateReviewDialog(ci)
        webbrowser.open(cfg.ADDIN_STORE_PAGE_URL)    
        


class DestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        cmd = args.command

class ActionHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        # sketchy.l("test")
        # futil.log(args.command.commandInputs.count)
        futil.log(args.command.commandInputs.item(0))

        # eventArgs = adsk.core.InputChangedEventArgs.cast(args)
        # inputs = cmd.inputs
        # cmdInput = cmd.input        

        
        futil.log("action, here we go")
        # futil.log(inputs)
        
          

def start(panel):
    try:
        sketchy.add_button(
            button_id='give_feedback'+cfg.BUTTON_NAME,
            button_title="Give feedback", 
            button_tooltip="Leave a review on app store page",
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
