#!/usr/bin/env python3

from asciimatics.widgets import Frame, Widget, Layout, ListBox, Divider, Button
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen


class SelectorView(Frame):
  def __init__(self, screen_name, screen, model):
    self._screen_name = screen_name
    self._model = model
    self._submodel = self._model.submodel(self._screen_name, self)
    super().__init__(
        screen,
        screen.height * 3 // 4,
        screen.width * 2 // 3,
        hover_focus=True,
        has_border=True,
        has_shadow=True,
        can_scroll=False,
        title=self._submodel.captions['window']
    )
    self._compose_layout()

  def update(self, frame_no):
    self._submodel = self._model.submodel(self._screen_name, self)
    super().update(frame_no)

  def _compose_layout(self):
    list_lay = Layout([1], fill_frame=True)
    self.add_layout(list_lay)
    list_lay.add_widget(ListBox(
        Widget.FILL_FRAME,
        self._submodel.options,
        name='list',
        add_scroll_bar=True,
        on_select=self._on_select
    ))
    list_lay.add_widget(Divider())

    tx_buttons_lay = Layout([1, 1])
    self.add_layout(tx_buttons_lay)
    tx_buttons_lay.add_widget(Button(self._submodel.captions['proceed'], on_click=self._on_select), 0)
    tx_buttons_lay.add_widget(Button(self._submodel.captions['cancel'], on_click=self._submodel.cancel), 1)

    self.fix()

  def _on_select(self):
    self.save()
    picked = self.data['list']
    if isinstance(picked, int):
      self._submodel.proceed(picked)
    else:
      self._model.popup('Nothing is selected')

  def process_event(self, event):
    if self._submodel is not None and hasattr(self._submodel, 'esc'):
      if isinstance(event, KeyboardEvent):
        if event.key_code == Screen.KEY_ESCAPE:
          self._submodel.esc()
    super().process_event(event)
