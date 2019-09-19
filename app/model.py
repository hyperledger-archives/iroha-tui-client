#!/usr/bin/env python3

from app.screensman import ScreensManager
from app.transactions import TransactionsPool
from tui import popup

from models.modeselector import ModeSelector
from models.txviewmodel import TransactionViewModel
from models.stub import StubModel

from screens import SCREENS


class AppModel:
  r"""
        __   __            __   __   ___
   /\  |__) |__)     |\/| /  \ |  \ |__  |
  /~~\ |    |        |  | \__/ |__/ |___ |___

  """

  def __init__(self,
               starting_screen: str):
    self._current_frame = None
    self._screen_manager = ScreensManager(starting_screen)

    self._submodels = {
        'Mode Selector': ModeSelector(self),
        'Transaction Editor': TransactionViewModel(self),
    }
    for screen_name in self._submodels:
      if screen_name not in SCREENS:
        raise Exception('Screen "{}" does not exists'.format(screen_name))

    self._stub_model = StubModel()
    self._txs_pool = TransactionsPool()
    self._current_tx_idx = None

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

  def previousscreen(self):
    self._screen_manager.back()
