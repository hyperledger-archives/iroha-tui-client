#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, MultiColumnListBox, Label, VerticalDivider, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
from copy import deepcopy

from datetime import datetime

from tui.indicators import Indicators


class DateUtils:

  @staticmethod
  def now_ts():
    """Timestamp in milliseconds"""
    return int(datetime.now().timestamp() * 1000)

  @staticmethod
  def epochms_to_human(timestamp):
    """Return locale’s appropriate date and time representation."""
    ts = int(timestamp)
    millis = ts % 1000
    dt = datetime.fromtimestamp(int(ts)/1000)
    return dt.strftime("%c {:03d}ms".format(millis))


class TransactionView(Frame, Indicators):
  def __init__(self, screen, model):
    super().__init__(
        screen,
        screen.height,
        screen.width,
        hover_focus=True,
        has_border=True,
        can_scroll=False,
        title='Transaction Composer'
    )
    self._screen_height = screen.height
    self.init_indicators()
    self._on_load = self._init_focus

    self._model = model
    self._init_focus_on = None
    self._compose_layout()

    self.data = {
        'human_time': 'Tue, 13 Aug 2019 20:54:36 +0000',
        'batch_type': 'Non-batched transaction',
        'batch_txs_count': '0',
        'created_time': str(DateUtils.now_ts()),
        'quorum': '1',
    }

    self.indicators_data = {
        'tx_hash': '4a4883bc2167f04a7f64c373b88c100095804d537da384446c236087b8934555',
    }

  def _init_focus(self):
    if self._init_focus_on:
      to = self._init_focus_on
      self.switch_focus(to['layout'], to['column'], to['widget'])

  def dummy(self):
    pass

  def _set_current_timestamp(self):
    self.data = {
        'created_time': str(DateUtils.now_ts())
    }

  def _ts_change(self, x):
    human_time = ''
    result = False
    try:
      human_time = DateUtils.epochms_to_human(x)
      result = True
    except:
      pass
    self.indicators_data = {
        'human_time': human_time
    }
    return result

  def _compose_layout(self):
    PADDING = 0
    tx_buttons_lay = Layout([1, 1])
    self.add_layout(tx_buttons_lay)
    tx_buttons_lay.add_widget(Button('Save', on_click=self.dummy), 0)
    tx_buttons_lay.add_widget(Button('Cancel', on_click=self.dummy), 1)

    hash_lay = Layout([PADDING, 18, PADDING])
    self.add_layout(hash_lay)
    hash_lay.add_widget(self.Indicator(name='tx_hash'), 1)
    hash_lay.add_widget(Divider(), 1)

    lay1 = Layout([PADDING, 5, 13, PADDING])
    self.add_layout(lay1)
    self._init_focus_on = {
        'layout': lay1,
        'column': 2,
        'widget': 0
    }
    lay1.add_widget(Label('Creator Id'), 1)
    lay1.add_widget(Text(name='creator_id'), 2)
    lay1.add_widget(Label('Quorum'), 1)
    self._q = Text(name='quorum')
    lay1.add_widget(self._q, 2)

    lay2 = Layout([PADDING, 5, 9, 4, PADDING])
    self.add_layout(lay2)
    lay2.add_widget(Label('Created Timestamp'), 1)
    lay2.add_widget(Text(name='created_time', validator=self._ts_change), 2)
    lay2.add_widget(Button('Use Now', on_click=self._set_current_timestamp), 3)

    lay3 = Layout([PADDING, 5, 13, PADDING])
    self.add_layout(lay3)
    lay3.add_widget(Label('Human Time'), 1)
    lay3.add_widget(self.Indicator(name='human_time'), 2)
    lay3.add_widget(Label('Batch Type'), 1)
    lay3.add_widget(self.Indicator(name='batch_type', label='Non-batched transaction'), 2)
    lay3.add_widget(Label('Txs in Batch'), 1)
    lay3.add_widget(self.Indicator(name='batch_txs_count', label='0'), 2)

    lay4 = Layout([PADDING, 18, PADDING])
    self.add_layout(lay4)
    lay4.add_widget(Divider(), 1)

    lay4 = Layout([PADDING, 3, 2, 2, 2, 1, 3, 3, 2, PADDING])
    self.add_layout(lay4)
    lay4.add_widget(Label('Commands:'), 1)
    lay4.add_widget(Button('Add', on_click=self.dummy), 2)
    lay4.add_widget(Button('Edit', on_click=self.dummy), 3)
    lay4.add_widget(Button('Del', on_click=self.dummy), 4)
    lay4.add_widget(Label('Signatures:'), 6)
    lay4.add_widget(Button('Add/Sign', on_click=self.dummy), 7)
    lay4.add_widget(Button('Del', on_click=self.dummy), 8)

    lay5 = Layout([PADDING, 9, 1, 8, PADDING])
    self.add_layout(lay5)
    lay5.add_widget(ListBox(
        max(self._screen_height - 13, 4),
        [('sadf', 1), ('sadfxcc', 2), ('sdfxcv', 3), ('sadf', 4), ('sadfxcc', 5),
         ('sdfxcv', 6), ('sadf', 7), ('sadfxcc', 8), ('sdfxcv', 9)],
        name='commands',
        add_scroll_bar=True,
        on_change=self.dummy,
        on_select=self.cmd_select
    ), 1)
    lay5.add_widget(VerticalDivider(), 2)
    lay5.add_widget(ListBox(
        max(self._screen_height - 13, 4),
        {},
        name='signatures',
        add_scroll_bar=True,
        on_change=self.dummy,
        on_select=self.dummy
    ), 3)
    self.fix()

  def cmd_select(self):
    self.save()
    selected = self.data['commands']
    # self._scene.add_effect(PopUpDialog(self._screen, str(selected), ['OK']))
    self.data = {'quorum': str(selected)}
    # self._scene.add_effect(PopUpDialog(self._screen, self.data['quorum'], ['OK']))


class Model:
  pass


def play_wrapper(screen, scene):
  model = Model()
  scenes = [
      Scene([TransactionView(screen, model)], -1, name='Transaction Composer'),
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
