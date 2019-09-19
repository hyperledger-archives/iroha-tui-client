#!/usr/bin/env python3


class ProtoFieldProps:
  r"""
   __   __   __  ___  __      ___    ___       __      __   __   __   __   __
  |__) |__) /  \  |  /  \    |__  | |__  |    |  \    |__) |__) /  \ |__) /__`
  |    |  \ \__/  |  \__/    |    | |___ |___ |__/    |    |  \ \__/ |    .__/
  """

  def __init__(self, proto_field_descriptor):
    self._field_descriptor = proto_field_descriptor

  @property
  def label(self):
    """
    Proto field label as string. E.g. 'LABEL_REPEATED'.

    None is returned when unable to define.
    """
    f = self._field_descriptor
    mapping = {
        f.LABEL_OPTIONAL: 'LABEL_OPTIONAL',
        f.LABEL_REPEATED: 'LABEL_REPEATED',
        f.LABEL_REQUIRED: 'LABEL_REQUIRED',
    }
    if f.label not in mapping:
      return None
    else:
      return mapping[f.label]

  @property
  def is_repeated(self):
    """
    Returns whether the field is repeated or not.
    """
    return 'LABEL_REPEATED' == self.label

  @property
  def is_optional_primitive(self):
    """
    Returns whether the field is not of a message type,
    is a part of oneof field
    and enclosing oneof field has only one (that) field inside.

    Within messages of Hyperledger Iroha proto schema
    sometimes we use oneof for a single field of primitive type.
    That is used to indicate optionality of the field without introducing
    "magic constants" that imply unset state of the field.
    """
    f = self._field_descriptor
    enclosing_oneof = f.containing_oneof
    is_primitive = f.CPPTYPE_MESSAGE != f.cpp_type
    if enclosing_oneof and is_primitive:
      if 1 == len(enclosing_oneof.fields):
        return True
    return False

  @property
  def cpp_type(self):
    """
    Proto field C++ type as a string. E.g. 'CPPTYPE_INT32'.

    None is returned when unable to define.
    """
    f = self._field_descriptor
    mapping = {
        f.CPPTYPE_INT32: 'CPPTYPE_INT32',
        f.CPPTYPE_INT64: 'CPPTYPE_INT64',
        f.CPPTYPE_UINT32: 'CPPTYPE_UINT32',
        f.CPPTYPE_UINT64: 'CPPTYPE_UINT64',
        f.CPPTYPE_DOUBLE: 'CPPTYPE_DOUBLE',
        f.CPPTYPE_FLOAT: 'CPPTYPE_FLOAT',
        f.CPPTYPE_BOOL: 'CPPTYPE_BOOL',
        f.CPPTYPE_ENUM: 'CPPTYPE_ENUM',
        f.CPPTYPE_STRING: 'CPPTYPE_STRING',
        f.CPPTYPE_MESSAGE: 'CPPTYPE_MESSAGE',
    }
    if f.cpp_type not in mapping:
      return None
    else:
      return mapping[f.cpp_type]


class ProtoMessageExplorer:
  r"""
   __   __   __  ___  __            ___  __   __        __   ___     ___      __        __   __   ___  __
  |__) |__) /  \  |  /  \     |\/| |__  /__` /__`  /\  / _` |__     |__  \_/ |__) |    /  \ |__) |__  |__)
  |    |  \ \__/  |  \__/     |  | |___ .__/ .__/ /~~\ \__> |___    |___ / \ |    |___ \__/ |  \ |___ |  \
  """

  def __init__(self, message=None, descriptor=None):
    assert bool(message) != bool(descriptor)  # xor
    if message:
      self._proto_descriptor = message.DESCRIPTOR
    else:
      self._proto_descriptor = descriptor
    self._descriptor = self._parse_message_descriptor(self._proto_descriptor)

  @property
  def descriptor(self):
    return self._descriptor

  """
  @
  @
  @ Private part
  @
  @
  """

  def _parse_message_descriptor(self, proto_message_descriptor, message_path=None, field_path=None):
    result = []
    if not message_path:
      message_path = proto_message_descriptor.name
    else:
      message_path = "{}.{}".format(message_path, proto_message_descriptor.name)
    if not field_path:
      field_path = ''
    for field in proto_message_descriptor.fields:
      next_field_path = '{}.{}'.format(field_path, field.name)
      if field.message_type:
        result.extend(self._parse_message_descriptor(field.message_type, message_path, next_field_path))
      else:
        result.append(self._parse_field_descriptor(field, message_path, next_field_path))
    return result

  def _parse_field_descriptor(self, proto_field_descriptor, message_path, field_path):
    f = proto_field_descriptor
    props = ProtoFieldProps(f)
    response = {
        'message_path': message_path,
        'field_path': field_path,
        'name': f.name,
        'cpp_type': props.cpp_type,
        'repeated': props.is_repeated,
        'optional_primitive': props.is_optional_primitive
    }
    if f.enum_type:
      response['enum_name'] = f.enum_type.name
      response['enum_options'] = [(x.name, x.number) for x in f.enum_type.values]
    return response
