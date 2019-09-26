#!/usr/bin/env python3

from asciimatics.widgets import Frame, Layout, Button, Divider

from proto.commands import ProtoCommandLoader
from proto.message import MessageModel
from tui.adaptors import CommandTuiAdaptor


class CommandView(Frame):
  def __init__(self, screen_name, screen, model):
    self._screen_name = screen_name
    self._model = model
    self._submodel = self._model.submodel(self._screen_name, self)

    super().__init__(
        screen,
        screen.height,
        screen.width,
        hover_focus=True,
        has_border=True,
        has_shadow=True,
        can_scroll=True,
        title=screen_name,
        on_load=self._onload_handler,
    )
    self._compose_layout()

  def update(self, frame_no):
    self._submodel = self._model.submodel(self._screen_name, self)
    super().update(frame_no)

  def _onload_handler(self):
    self._submodel = self._model.submodel(self._screen_name, self)

  def _compose_layout(self):
    tx_buttons_lay = Layout([1, 1])
    self.add_layout(tx_buttons_lay)
    tx_buttons_lay.add_widget(Button('Save', on_click=self._save), 0)
    tx_buttons_lay.add_widget(Button('Cancel', on_click=self._cancel), 1)

    lay1 = Layout([1])
    self.add_layout(lay1)
    lay1.add_widget(Divider())

    self._submodel.draw_ui(self)
    self.fix()

  def _save(self):
    self.save()
    self._model.popup('test')

  def _cancel(self):
    self._model._temp_cmd = None
    self._model._current_cmd_idx = None
    self._model.previousscreen('Transaction Editor')
