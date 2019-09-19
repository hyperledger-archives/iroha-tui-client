#!/usr/bin/env python3

from .parsers import ProtoMessageExplorer


class MessageModel:
  r""""
        ___  __   __        __   ___           __   __   ___
  |\/| |__  /__` /__`  /\  / _` |__      |\/| /  \ |  \ |__  |
  |  | |___ .__/ .__/ /~~\ \__> |___     |  | \__/ |__/ |___ |___

  NOTE This class does not support addressing items in repeated fields
  """

  def __init__(self, proto_message):
    self._message = proto_message
    self._message_descriptor = ProtoMessageExplorer(message=proto_message).descriptor
    self._fields = {}
    for field in self._message_descriptor:
      self._fields[field['field_path']] = field

  @property
  def descriptor(self):
    return self._message_descriptor

  @property
  def name(self):
    return self._message.DESCRIPTOR.name

  def read(self, field_path):
    needle, _ = self._locate_field(field_path)
    return needle

  def set_to(self, field_path, value):
    needle, field_name = self._locate_field(field_path, get_parent=True)
    if self._fields[field_path]['repeated']:
      needle.ClearField(field_name)
      needle = getattr(needle, field_name)
      needle.extend(value)
    else:
      setattr(needle, field_name, self._smart_cast(field_path, value))

  def clear(self, field_path):
    needle, field_name = self._locate_field(field_path, get_parent=True)
    needle.ClearField(field_name)

  """
  @
  @
  @ Private part
  @
  @
  """

  def _locate_field(self, field_path, get_parent=False):
    self._verify_path(field_path)
    right_boundary = -1 if get_parent else None
    path_levels = field_path.split('.')[1:]
    field_name = path_levels[-1]
    needle = self._message
    for level in path_levels[:right_boundary]:
      needle = getattr(needle, level)
    return needle, field_name

  def _verify_path(self, field_path):
    if field_path not in self._fields:
      err_str = 'Specified field path does not exit within '\
          'the message (message="{}", field_path="{}").'
      raise KeyError(err_str.format(self.name, field_path))

  def _smart_cast(self, field_path, value):
    cpp_type = self._fields[field_path]['cpp_type']
    if 'INT' in cpp_type or 'ENUM' in cpp_type:
      return int(value)
    if 'FLOAT' in cpp_type or 'DOUBLE' in cpp_type:
      return float(value)
    if 'BOOL' in cpp_type:
      return bool(value)
    if 'STRING' in cpp_type:
      return str(value)
    return value
