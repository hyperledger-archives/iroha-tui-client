from proto.message import MessageModel
from proto.commands import ProtoCommandLoader
from tui.adaptors import CommandTuiAdaptor


def command_screen_name_to_message_name(screen_name):
  """
  Converts 'Command Editor - Append Role' to 'AppendRole'
  """
  if not screen_name.startswith('Command Editor -'):
    raise Exception('Not possible to get command message name from screen name "{}"'.format(screen_name))
  command_name = screen_name.split('-')[1].strip()
  message_name = command_name.replace(' ', '')
  return message_name


class CommandViewModel:

  def __init__(self, model, command_name):
    self._pcl = ProtoCommandLoader()
    self._command = self._pcl.wrapped_command_by_name(command_name)
    self._message_model = MessageModel(self._command.unwrapped)
    self._ui_adaptor = None

  def draw_ui(self, frame):
    self._ui_adaptor = CommandTuiAdaptor(self._message_model, frame)
    self._ui_adaptor.draw_ui()
