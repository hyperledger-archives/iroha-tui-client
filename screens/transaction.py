#!/usr/bin/env python3

from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, Button, Divider, Label, Text, ListBox, VerticalDivider
from asciimatics.screen import Screen
from tui.indicators import Indicators

from iroha import IrohaCrypto
from datetime import datetime
from app.validators import uint64_validator, account_id_validator, quorum_validator


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
  def __init__(self, screen_name, screen, model):
    self._screen_name = screen_name
    self._model = model
    self._submodel = self._model.submodel(screen_name, self)

    self._init_focus_on = None
    self._commands_list = None
    self._signatures_list = None

    super().__init__(
        screen,
        screen.height,
        screen.width,
        hover_focus=True,
        has_border=True,
        can_scroll=False,
        on_load=self._onload_handler,
        title='Transaction Editor'
    )
    self._screen_height = screen.height
    self.init_indicators()

    self._compose_layout()

  def update(self, frame_no):
    # Used to ensure that model._current_frame is set correctly
    self._submodel = self._model.submodel(self._screen_name, self)
    self._semi_save()
    return super().update(frame_no)

  def _onload_handler(self):
    self._submodel.load()
    if self._submodel.initialized:
      tx_hash = IrohaCrypto.hash(self._model._temp_tx).hex()
      data = self._submodel.data
      self._commands_list.options = data['commands_names']
      del data['commands_names']
      self.data = data
      data['tx_hash'] = tx_hash
      self.indicators_data = data

    self._init_focus()

  def _init_focus(self):
    if self._init_focus_on:
      to = self._init_focus_on
      self.switch_focus(to['layout'], to['column'], to['widget'])

  def _set_current_timestamp(self):
    self.data = {
        '.payload.reduced_payload.created_time': str(DateUtils.now_ts())
    }

  def _ts_change(self, x):
    if not uint64_validator(x):
      return False
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
    tx_buttons_lay = Layout([1, 1, 1])
    self.add_layout(tx_buttons_lay)
    tx_buttons_lay.add_widget(Button('Save', on_click=self._save), 0)
    tx_buttons_lay.add_widget(Button('Save & Go back', on_click=self._save_go_back), 1)
    tx_buttons_lay.add_widget(Button('Go back', on_click=self._cancel), 2)

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
    lay1.add_widget(Text(name='.payload.reduced_payload.creator_account_id', validator=account_id_validator), 2)
    lay1.add_widget(Label('Quorum'), 1)
    lay1.add_widget(Text(name='.payload.reduced_payload.quorum', validator=quorum_validator), 2)

    lay2 = Layout([PADDING, 5, 9, 4, PADDING])
    self.add_layout(lay2)
    lay2.add_widget(Label('Created Timestamp'), 1)
    lay2.add_widget(Text(name='.payload.reduced_payload.created_time', validator=self._ts_change), 2)
    lay2.add_widget(Button('Use Now', on_click=self._set_current_timestamp), 3)

    lay3 = Layout([PADDING, 5, 13, PADDING])
    self.add_layout(lay3)
    lay3.add_widget(Label('Human Time'), 1)
    lay3.add_widget(self.Indicator(name='human_time'), 2)
    lay3.add_widget(Label('Batch Summary'), 1)
    lay3.add_widget(self.Indicator(name='batch_summary'), 2)

    lay4 = Layout([PADDING, 18, PADDING])
    self.add_layout(lay4)
    lay4.add_widget(Divider(), 1)

    lay4 = Layout([PADDING, 3, 2, 2, 2, 1, 3, 3, 2, PADDING])
    self.add_layout(lay4)
    lay4.add_widget(Label('Commands:'), 1)
    lay4.add_widget(Button('Add', on_click=self._add_command), 2)
    lay4.add_widget(Button('Edit', on_click=self._edit_command), 3)
    lay4.add_widget(Button('Del', on_click=self._remove_command), 4)
    lay4.add_widget(Label('Signatures:'), 6)
    lay4.add_widget(Button('Add/Sign', on_click=self._add_signature), 7)
    lay4.add_widget(Button('Del', on_click=self._remove_signature), 8)

    lay5 = Layout([PADDING, 9, 1, 8, PADDING])
    self.add_layout(lay5)
    self._commands_list = ListBox(
        max(self._screen_height - 13, 4),
        [],
        name='commands',
        add_scroll_bar=True,
        on_select=self._edit_command
    )
    lay5.add_widget(self._commands_list, 1)
    lay5.add_widget(VerticalDivider(), 2)
    self._signatures_list = ListBox(
        max(self._screen_height - 13, 4),
        {},
        name='signatures',
        add_scroll_bar=True,
        on_select=self._show_signature_public_key
    )
    lay5.add_widget(self._signatures_list, 3)
    self.fix()

  """
  C o m m a n d s
  """

  def _add_command(self):
    self._semi_save()
    self._model.nextscreen('Command Selector')

  def _edit_command(self):
    pass

  def _remove_command(self):
    pass

  """
  S i g n a t u r e s
  """

  def _add_signature(self):
    pass

  def _remove_signature(self):
    pass

  def _show_signature_public_key(self):
    pass  # popup with public key

  """
  Global buttons handlers
  """

  def _semi_save(self):
    self.save()
    if self._submodel.initialized:
      try:
        self._submodel.data = self.data
        tx_hash = IrohaCrypto.hash(self._model._temp_tx).hex()
        self.indicators_data = {'tx_hash': tx_hash}
      except ValueError:
        self.indicators_data = {'tx_hash': 'Invalid data entered'}
        return False
    return True

  def _save(self):
    if self._submodel.initialized:
      self._semi_save()
      self._submodel.commit()

  def _save_go_back(self):
    self._save()
    self._cancel()

  def _cancel(self):
    self._model._current_tx_idx = None
    self._model._temp_tx = None
    self._model._temp_cmd = None
    self._model._current_cmd_idx = None
    self._submodel.reset()
    self._model.previousscreen()

  def process_event(self, event):
    if isinstance(event, KeyboardEvent):
      if event.key_code == Screen.KEY_ESCAPE:
        self._cancel()
    super().process_event(event)
