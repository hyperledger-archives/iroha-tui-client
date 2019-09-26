from asciimatics.exceptions import StopApplication
from proto.commands import ProtoCommandLoader


class CommandSelector:

  def __init__(self, model):
    self._model = model
    self._commands = None
    self._proto_loader = ProtoCommandLoader()
    self._init_commands_list()

  @property
  def captions(self):
    return {
        'window': 'Choose a command',
        'proceed': 'Select',
        'cancel': 'Back'
    }

  @property
  def options(self):
    return self._commands

  def proceed(self, option):
    if isinstance(option, int):
      if 0 <= option < len(self._commands):
        command_human_name = self._commands[option][0]
        message_name = command_human_name.replace(' ', '').strip()
        command = self._proto_loader.wrapped_command_by_name(message_name)
        self._model._temp_cmd = command
        self._model._current_cmd_idx = len(self._model._temp_tx.payload.reduced_payload.commands)
        self._model.nextscreen('Command Editor - {}'.format(command_human_name))

    self._model.popup('Unknown option is picked: "{}"'.format(option))

  def cancel(self):
    self._model._temp_cmd = None
    self._model.previousscreen()

  def esc(self):
    self.cancel()

  def _init_commands_list(self):
    cmds = self._proto_loader.commands
    listbox_data = enumerate([n[0] for n in cmds])
    self._commands = [(t[1], t[0]) for t in listbox_data]
