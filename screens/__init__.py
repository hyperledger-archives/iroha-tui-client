
from asciimatics.scene import Scene

from .selector import SelectorView
from .transactions import TransactionsView
from .transaction import TransactionView

SCREENS = {
    'Mode Selector': SelectorView,
    'Transactions Browser': TransactionsView,
    'Transaction Editor': TransactionView,
}


def init_scenes(screen, app_model):
  for name, class_obj in SCREENS.items():
    obj = class_obj(name, screen, app_model)
    scene = Scene([obj], -1, name=name)
    yield scene
