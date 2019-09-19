from asciimatics.widgets import PopUpDialog


def popup(frame, message, buttons=None, handler=None):
  if buttons is None:
    buttons = ['OK']
  frame._scene.add_effect(PopUpDialog(
      frame._screen, message, buttons, on_close=handler
  ))
