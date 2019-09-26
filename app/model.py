#!/usr/bin/env python3

from app.screensman import ScreensManager
from app.transactions import TransactionsPool
from tui import popup

from models.modeselector import ModeSelector
from models.txviewmodel import TransactionViewModel
from models.stub import StubModel
from models.cmdselector import CommandSelector
from models.cmdview import CommandViewModel, command_screen_name_to_message_name

from screens import SCREENS


class TempObj:
  """
  A container to store temp transaction or command alongside with its meta information.
  """

  def __init__(self):
    self.obj = None
    self.idx = None

  def reset(self):
    self.obj = None
    self.idx = None

  def load_from_txs_pool(self, txs_pool, idx=None):
    if idx is None:
      idx = self.idx
    else:
      self.idx = idx
    self.obj = txs_pool[idx]

  @property
  def initialized(self):
    return not (self.obj is None or self.idx is None)


class AppModel:
  r"""
        __   __            __   __   ___
   /\  |__) |__)     |\/| /  \ |  \ |__  |
  /~~\ |    |        |  | \__/ |__/ |___ |___

  """

  def __init__(self, starting_screen: str):
    self._current_frame = None
    self._screen_manager = ScreensManager(starting_screen)

    self._submodels = {
        'Mode Selector': ModeSelector(self),
        'Transaction Editor': TransactionViewModel(self),
        'Command Selector': CommandSelector(self),
    }

    for screen_name in SCREENS:
      if screen_name.startswith('Command Editor'):
        command_name = command_screen_name_to_message_name(screen_name)
        self._submodels[screen_name] = CommandViewModel(self, command_name)

    for screen_name in self._submodels:
      if screen_name not in SCREENS:
        raise Exception('Screen "{}" does not exists'.format(screen_name))

    self._stub_model = StubModel()
    self.txs_pool = TransactionsPool()

    # self.temp_tx = TempObj()
    # self.temp_cmd = TempObj()

    self._current_tx_idx = None
    self._temp_tx = None
    self._temp_cmd = None
    self._current_cmd_idx = None

  def popup(self, message, buttons=None, handler=None):
    if self._current_frame:
      popup.popup(self._current_frame, message, buttons, handler)

  def submodel(self, name, frame):
    active_screen = self._screen_manager.active
    if name == active_screen:
      self._current_frame = frame
    if name not in self._submodels:
      return self._stub_model
    return self._submodels[name]

  def nextscreen(self, name):
    self._screen_manager.to(name)

  def previousscreen(self, screen_name=None):
    if screen_name is None:
      self._screen_manager.back()
    else:
      self._screen_manager.backto(screen_name)
