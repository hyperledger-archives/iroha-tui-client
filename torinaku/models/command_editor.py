from torinaku.models.base import BaseModel
from torinaku.proto.commands import CommandWrapper, ProtoCommandLoader
from torinaku.proto.commands_pb2 import Command
from torinaku.proto.message import ProtoMessageProxy
from torinaku.tui.adaptors import CommandTuiAdaptor


class CommandEditorModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.transaction = kwargs.pop("transaction", None)
        self.target_command = kwargs.pop("command", None)
        command_name = kwargs.pop("command_name", None)

        if not ((self.transaction and command_name) or self.target_command):
            raise ValueError("Either transaction or command should be set")

        if self.target_command:
            command = Command()
            command.CopyFrom(self.target_command)
            self.command = CommandWrapper(wrapped_command=command)
        else:
            self.command = ProtoCommandLoader().wrapped_command_by_name(command_name)
        self.command_proxy = ProtoMessageProxy(self.command.unwrapped)

        super().__init__(*args, **kwargs)

    def draw_ui(self, frame):
        CommandTuiAdaptor(self.command_proxy, frame).draw_ui()

    def get_init_data(self):
        data = {}
        for field in self.command_proxy.descriptor:
            path = field["field_path"]
            data[path] = self.command_proxy.read(path)
        return data

    def update(self, data):
        try:
            for key, value in data.items():
                self.command_proxy.set_to(key, value)
        except (ValueError, TypeError):
            pass  # TODO: validation

    def save(self):
        if self.target_command:
            self.target_command.CopyFrom(self.command_proxy.wrapped)
        else:
            self.transaction.payload.reduced_payload.commands.extend(
                [self.command.wrapped]
            )
        self._application.screen_manager.back()
