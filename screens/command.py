#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, MultiColumnListBox, Label, VerticalDivider
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
from copy import deepcopy

from datetime import datetime

from proto.commands import ProtoCommandLoader
from proto.message import MessageModel
from tui.adaptors import CommandTuiAdaptor


class CommandView(Frame):
  def __init__(self, screen, model):
    super().__init__(
        screen,
        screen.height,
        screen.width,
        hover_focus=True,
        has_border=True,
        has_shadow=True,
        can_scroll=True,
        title='Command Editor'
    )
    self._model = model
    self._compose_layout()

  def dummy(self):
    pass

  def _compose_layout(self):
    tx_buttons_lay = Layout([1, 1])
    self.add_layout(tx_buttons_lay)
    tx_buttons_lay.add_widget(Button('Save', on_click=self.dummy), 0)
    tx_buttons_lay.add_widget(Button('Cancel', on_click=self.dummy), 1)

    lay1 = Layout([1])
    self.add_layout(lay1)
    lay1.add_widget(Divider())

    self._model.draw_ui(self)

    self.fix()


class Model:

  def __init__(self):
    pcl = ProtoCommandLoader()
    self._command = pcl.wrapped_command_by_name('AddPeer')
    self._message_model = MessageModel(self._command.unwrapped)
    self._ui_adaptor = None

  def draw_ui(self, frame):
    if not self._ui_adaptor:
      self._ui_adaptor = CommandTuiAdaptor(self._message_model, frame)
    self._ui_adaptor.draw_ui()


def play_wrapper(screen, scene):
  model = Model()
  scenes = [
      Scene([CommandView(screen, model)], -1, name='Command Editor'),
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
