import re

from iroha import commands_pb2

from torinaku.commons import reraise
from torinaku.proto.message import ProtoMessageProxy
from torinaku.proto.helpers import shorten_command_name


class CommandWrapper:
    def __init__(self, unwrapped_command=None, wrapped_command=None):
        if not (bool(unwrapped_command) != bool(wrapped_command)):
            raise ValueError(
                "Either raw command or wrapped has to be passed to CommandWrapper"
            )
        self._wrapped = None
        self._unwrapped = None
        if unwrapped_command:
            self._wrap(unwrapped_command)
        else:
            self._init_from_wrapped(wrapped_command)

    @property
    def wrapped(self):
        return self._wrapped

    @property
    def unwrapped(self):
        return self._unwrapped

    """
    @
    @
    @ Private part
    @
    @
    """

    def _wrap(self, unwrapped_command):
        commands = ProtoCommandLoader().commands
        name = unwrapped_command.DESCRIPTOR.name
        field_name = None
        for command in commands:
            if command[1] == name:
                field_name = command[2]
                break
        proto_command = commands_pb2.Command()
        target_command = getattr(proto_command, field_name)
        target_command.CopyFrom(unwrapped_command)
        self._init_from_wrapped(proto_command)

    def _init_from_wrapped(self, wrapped_command):
        field_name = wrapped_command.WhichOneof(ProtoCommandLoader.MSG_FIELD)
        self._wrapped = wrapped_command
        self._unwrapped = getattr(wrapped_command, field_name)


class ProtoCommandLoader:
    ROOT_MSG = "Command"
    MSG_FIELD = "command"

    def __init__(self):
        self._descr = commands_pb2.DESCRIPTOR
        self._cmd_message = None
        self._cmd_field = None
        self._preload_cmd_fields()
        self._commands = self._preload_command_messages()

    @property
    def commands(self):
        """
        List of tuples of pretty message name, message name and field name within
        Command message.

        E.g. [('Message Name', 'MessageName', 'message_name'), ]
        """
        return self._commands

    def wrapped_command_by_name(self, message_name):
        """
        Provides proto message without Command wrapper by its name (e.g. 'CreateRole').
        """
        message_class = getattr(commands_pb2, message_name)
        message_instance = message_class()
        return CommandWrapper(unwrapped_command=message_instance)

    """
    @
    @
    @ Private part
    @
    @
    """

    def _preload_cmd_fields(self):
        try:
            self._cmd_message = self._descr.message_types_by_name[self.ROOT_MSG]
        except KeyError as ke:
            reraise(
                ke,
                "Message {} not found in commands proto descriptor, "
                "the schema or client needs to be updated".format(self.ROOT_MSG),
            )

        try:
            self._cmd_field = self._cmd_message.oneofs_by_name[self.MSG_FIELD]
        except KeyError as ke:
            reraise(
                ke,
                "Field {} for commands listing was not found "
                "in proto message {}".format(
                    self.MSG_FIELD, self.ROOT_MSG
                ),
            )

    def _preload_command_messages(self):
        commands = []
        for cmd in self._cmd_field.fields:
            message_name = cmd.message_type.name
            pretty_message_name = re.sub(r"([A-Z])", r" \1", message_name).strip()
            commands.append((pretty_message_name, message_name, cmd.name))
        return commands


class CommandPreview:
    """
    Only non-repeated primitives are displayed
    """

    def __init__(self, unwrapped_command=None, wrapped_command=None):
        if not (bool(unwrapped_command) != bool(wrapped_command)):
            raise ValueError(
                "Either raw command or wrapped has to be passed to CommandWrapper"
            )
        unwrapped = (
            unwrapped_command if unwrapped_command else wrapped_command.unwrapped
        )
        self._message_model = ProtoMessageProxy(unwrapped)
        self._name = unwrapped.DESCRIPTOR.name
        self._short_name = shorten_command_name(self._name)
        self._content = None
        self._brief = None
        self._full = None
        self._read_content()

    @property
    def brief(self):
        if not self._brief:
            self._calc_brief()
        return self._brief

    @property
    def full(self):
        if not self._full:
            self._calc_full()
        return self._full

    """
    @
    @
    @ Private part
    @
    @
    """

    def _read_content(self):
        self._content = []
        for field in self._message_model.descriptor:
            if (
                (not field["repeated"])
                and ("ENUM" not in field["cpp_type"])
                and ("MESSAGE" not in field["cpp_type"])
            ):
                value = self._message_model.read(field["field_path"])
                self._content.append(str(value))

    def _calc_brief(self):
        self._brief = "{} {}".format(
            self._short_name,
            " ".join([p[:6] + u"…" if len(p) > 6 else p for p in self._content]),
        )
        self._brief = re.sub(" +", " ", self._brief).strip()

    def _calc_full(self):
        self._full = "{} {}".format(self._name, " ".join(self._content))
        self._full = re.sub(" +", " ", self._full).strip()
