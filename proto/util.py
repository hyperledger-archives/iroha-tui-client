#!/usr/bin/env python3

from . import commands_pb2
from commons import reraise
import re


class ProtoCommands:
  ROOT_MSG = 'Command'
  MSG_FIELD = 'command'

  def __init__(self):
    self._descr = commands_pb2.DESCRIPTOR
    self._cmd_message = None
    self._cmd_field = None
    self._preload_cmd_field()

  def _preload_cmd_field(self):
    try:
      self._cmd_message = self._descr.message_types_by_name[self.ROOT_MSG]
    except KeyError as ke:
      reraise(ke, 'Message {} not found in commands proto descriptor, '
              'the schema or client needs to be updated'.format(self.ROOT_MSG))

    try:
      self._cmd_field = self._cmd_message.oneofs_by_name[self.MSG_FIELD]
    except KeyError as ke:
      reraise(ke, 'Field {} for commands listing was not found in proto message {}'.
              format(self.MSG_FIELD, self.ROOT_MSG))

  def list_commands(self, pretty_names=False):
    """
    returns list of tuples with message names and field names
    """
    commands = []
    for cmd in self._cmd_field.fields:
      message_name = cmd.message_type.name
      if pretty_names:
        message_name = re.sub(r'([A-Z])', r' \1', message_name).strip()
      commands.append((message_name, cmd.name))
    return commands
