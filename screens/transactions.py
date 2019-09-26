#!/usr/bin/env python3

"""

Transactions browser

"""

from asciimatics.widgets import Frame, Widget, Layout, Divider, Button, Label
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

from tui.multicolumnchecklistbox import MultiColumnCheckListBox
from app.transactions import TransactionsPoolViewer


class TransactionsView(Frame):

  def __init__(self, screen_name, screen, model):
    self._screen_name = screen_name
    self._model = model
    self._submodel = self._model.submodel(self._screen_name, self)

    super(TransactionsView, self).__init__(
        screen,
        screen.height,
        screen.width,
        on_load=self._reload_list,
        hover_focus=True,
        can_scroll=False,
        title='Transactions Browser'
    )

    self._transactions_list = MultiColumnCheckListBox(
        Widget.FILL_FRAME,
        columns=["<7", ">14", "<18", ">3", ">3", ">3", "0", ">3"],
        options=[],
        titles=['Hash', 'Timestamp', 'Creator', 'Q', 'B', 'C', 'Commands', 'S'],
        name="txs_list",
        on_select=self._edit_current_tx,
        on_change=self._refresh_buttons_state,
        add_scroll_bar=True
    )
    self._model = model

    nav_lay = Layout([1, 1, 1])
    self.add_layout(nav_lay)
    nav_lay.add_widget(Label('Go to:'))
    nav_lay.add_widget(Button('Main menu', self._main_menu), 1)
    nav_lay.add_widget(Button('Queries manager', self.dummy, disabled=True), 2)

    layout = Layout(
        [1],
        fill_frame=True
    )
    self.add_layout(layout)
    layout.add_widget(Divider())
    layout.add_widget(self._transactions_list)
    layout.add_widget(Divider())
    buttons = Layout([1, 1, 1, 1, 1, 1, 1])
    self.add_layout(buttons)
    self._send_button = Button('Send', self.dummy)
    self._status_button = Button('Status', self.dummy)
    self._remove_button = Button('Remove!', self._remove_txs)
    self._batch_button = Button('Batch', self.dummy)
    self._sign_button = Button('Sign', self.dummy)
    buttons.add_widget(Button('Create', self._create_tx), 0)
    buttons.add_widget(self._send_button, 1)
    buttons.add_widget(self._status_button, 2)
    buttons.add_widget(self._remove_button, 3)
    buttons.add_widget(Button('Sav/Ld', self.dummy, disabled=True), 4)
    buttons.add_widget(self._batch_button, 5)
    buttons.add_widget(self._sign_button, 6)
    help_messages = Layout([1])
    self.add_layout(help_messages)
    label1 = Label('[Return] to edit, [Space] to pick several, [Esc] to go to main menu', align='^')
    label2 = Label('Q - quorum, B - batch size, C - commands quantity, S - signatures quantity', align='^')
    help_messages.add_widget(Divider())
    help_messages.add_widget(label2)
    help_messages.add_widget(label1)

    self.fix()

  def _reload_list(self, new_value=None):
    viewer = TransactionsPoolViewer(self._model.txs_pool)
    data = []
    i = 0
    for tx in viewer.data:
      data.append(([
          tx['hash'],
          tx['timestamp'],
          tx['creator'],
          tx['quorum'],
          tx['batch_type'][0] + tx['batch'],
          tx['commands'],
          tx['brief'],
          tx['signatures']
      ], i))
      i += 1

    self._transactions_list.options = data
    self._transactions_list.value = new_value
    self._transactions_list._selected = []
    self._refresh_buttons_state()

  def _create_tx(self):
    self._model._current_tx_idx = self._model.txs_pool.add()
    # self._model.temp_tx.idx = self._model.txs_pool.add()
    self._model._temp_tx = self._model.txs_pool[self._model._current_tx_idx]
    # self._model.temp_tx.load_from_txs_pool(self._model.txs_pool)
    self._reload_list()
    self._model.nextscreen('Transaction Editor')

  def _remove_txs(self):
    to_remove = list(reversed(sorted(self._transactions_list._selected)))
    for txidx in to_remove:
      del self._model.txs_pool[txidx]
    self._reload_list()

  def update(self, frame_no):
    self._submodel = self._model.submodel(self._screen_name, self)
    super().update(frame_no)

  def _refresh_buttons_state(self):
    disabled = not bool(len(self._transactions_list._selected))
    self._send_button.disabled = disabled
    self._status_button.disabled = disabled
    self._remove_button.disabled = disabled
    self._batch_button.disabled = disabled
    self._sign_button.disabled = disabled

  def process_event(self, event):
    if isinstance(event, KeyboardEvent):
      if event.key_code == Screen.KEY_ESCAPE:
        self._model.previousscreen()
    super().process_event(event)

  def _edit_current_tx(self):
    if self._transactions_list.value[0] is None:
      return
    self._model._current_tx_idx = self._transactions_list.value[0]
    # self._model.temp_tx.idx = self._transactions_list.value[0]
    self._model._temp_tx = self._model.txs_pool[self._model._current_tx_idx]
    # self._model.temp_tx.load_from_txs_pool(self._model.txs_pool)
    self._model.nextscreen('Transaction Editor')

  def _main_menu(self):
    self._model.previousscreen()

  def dummy(self):
    pass
