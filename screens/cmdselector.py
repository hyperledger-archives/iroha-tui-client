#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, MultiColumnListBox, Label, VerticalDivider
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
from copy import deepcopy

from datetime import datetime

from proto.util import ProtoCommands


class CommandSelectorView(Frame):
  def __init__(self, screen, model):
    super().__init__(
        screen,
        screen.height * 3 // 4,
        screen.width * 2 // 3,
        hover_focus=True,
        has_border=True,
        has_shadow=True,
        can_scroll=False,
        title='Select a Command'
    )
    self._model = model
    self._compose_layout()

  def dummy(self):
    pass

  def _get_commands_list(self):
    pc = ProtoCommands()
    cmds = pc.list_commands(pretty_names=True)
    listbox_data = enumerate([n[0] for n in cmds])
    return [(t[1], t[0]) for t in listbox_data]

  def _compose_layout(self):
    list_lay = Layout([1], fill_frame=True)
    self.add_layout(list_lay)
    list_lay.add_widget(ListBox(
        Widget.FILL_FRAME,
        self._get_commands_list(),
        name='command_names',
        add_scroll_bar=True,
        on_change=self.dummy,
        on_select=self.dummy
    ))
    list_lay.add_widget(Divider())

    tx_buttons_lay = Layout([1, 1])
    self.add_layout(tx_buttons_lay)
    tx_buttons_lay.add_widget(Button('Next', on_click=self.dummy), 0)
    tx_buttons_lay.add_widget(Button('Cancel', on_click=self.dummy), 1)

    self.fix()


class Model:
  pass


def play_wrapper(screen, scene):
  model = Model()
  scenes = [
      Scene([CommandSelectorView(screen, model)], -1, name='Command Selector'),
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
