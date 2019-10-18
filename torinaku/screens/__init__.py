from asciimatics.scene import Scene

from torinaku.screens.selector import SelectorView
from torinaku.screens.transactions import TransactionsView

#  from .transaction import TransactionView
#  from .command import CommandView

#  from proto.commands import ProtoCommandLoader

SCREENS = {
    "Mode Selector": SelectorView,
    "Transaction Browser": TransactionsView,
    #  "Transaction Editor": TransactionView,
    #  "Command Selector": SelectorView,
}


#  def _populate_screens_with_command_editors():
#  global SCREENS
#  commands = ProtoCommandLoader().commands
#  for cmd in commands:
#  human_label = cmd[0]
#  screen_name = "Command Editor - {}".format(human_label)
#  SCREENS[screen_name] = CommandView


#  _populate_screens_with_command_editors()


def init_scenes(screen, torinaku):
    screen_map = {}
    scenes = []
    for name, class_obj in SCREENS.items():
        obj = class_obj(name, screen, torinaku)
        scene = Scene([obj], -1, name=name)
        screen_map[name] = obj
        scenes.append(scene)

    return scenes, screen_map
