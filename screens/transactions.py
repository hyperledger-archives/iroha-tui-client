#!/usr/bin/env python3

"""

Transactions browser

"""

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, MultiColumnListBox, Label
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys


class TransactionsFrame(Frame):
  def __init__(self, screen, model):
    super(TransactionsFrame, self).__init__(
        screen,
        screen.height,
        screen.width,
        on_load=self._reload_transactions_list,
        hover_focus=True,
        can_scroll=False
    )

    self._transactions_view = MultiColumnListBox(
        Widget.FILL_FRAME,
        columns=["<2", "<7", ">10", "<18", ">3", ">3", ">3", "0", ">3"],
        options=[
            ([' ', 'd9ed67', '1564516657', 'admin@test', '1', '0', '3', 'AddAst RmSig TrAst', '0'], 1),
            (['>', 'd746a7', '1564516683', 'adminlong_acc@test_domain', '1', '0', '23', 'AddSig SetQrm', '0'], 2),
        ],
        titles=['', 'Hash', 'Timestamp', 'Creator', 'Q', 'B', 'C', 'Commands', 'S'],
        name="txs_list"
    )
    self._model = model

    tabs = Layout([1, 1, 1, 1])
    self.add_layout(tabs)
    txs_tab = Button('Transactions', self.dummy, add_box=True)
    txs_tab.custom_colour = 'selected_control'
    txs_tab.disabled = True
    queries_tab = Button('Queries', self.dummy, add_box=True)
    exit_tab = Button('Quit', self.dummy, add_box=True)
    tabs.add_widget(Label('Active view:'), 0)
    tabs.add_widget(txs_tab, 1)
    tabs.add_widget(queries_tab, 2)
    # tabs.add_widget(Button('[Keypairs]', self.dummy, add_box=False), 3)
    tabs.add_widget(exit_tab, 3)

    layout = Layout(
        [1],
        fill_frame=True
    )
    self.add_layout(layout)
    layout.add_widget(Divider())
    layout.add_widget(self._transactions_view)
    layout.add_widget(Divider())
    buttons = Layout([1, 1, 1, 1, 1, 1, 1])
    self.add_layout(buttons)
    buttons.add_widget(Button('Create', self.dummy), 0)
    buttons.add_widget(Button('Send', self.dummy), 1)
    buttons.add_widget(Button('Status', self.dummy), 2)
    buttons.add_widget(Button('Remove', self.dummy), 3)
    buttons.add_widget(Button('Sav/Ld', self.dummy, disabled=True), 4)
    buttons.add_widget(Button('Batch', self.dummy), 5)
    buttons.add_widget(Button('Sign', self.dummy), 6)
    help_messages = Layout([1])
    self.add_layout(help_messages)
    label1 = Label('[Return] to edit, [Shift + Return] to pick several (for batch/multiple send)', align='^')
    label2 = Label('Q - quorum, B - batch size, C - commands quantity, S - signatures quantity', align='^')
    help_messages.add_widget(Divider())
    help_messages.add_widget(label2)
    help_messages.add_widget(label1)

    self.fix()

  def _reload_transactions_list(self):
    pass

  def dummy(self):
    pass


class Model:
  pass


def play_wrapper(screen, scene):
  model = Model()
  scenes = [
      Scene([TransactionsFrame(screen, model)], -1, name="Transactions"),
  ]

  screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
while True:
  try:
    Screen.wrapper(play_wrapper, catch_interrupt=False, arguments=[last_scene])
    sys.exit(0)
  except ResizeScreenError as e:
    last_scene = e.scene
  except KeyboardInterrupt:
    sys.exit(0)
