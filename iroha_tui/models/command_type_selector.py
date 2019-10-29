from iroha_tui.models.selector import BaseSelectorModel

from iroha_tui.proto.commands import ProtoCommandLoader
from iroha_tui.models.command_editor import CommandEditorModel
from iroha_tui.screens.command_editor import CommandEditorView


class CommandTypeSelectorModel(BaseSelectorModel):
    is_skippable = True
    title = "Add command"

    @property
    def options(self):
        return {
            human_name: self.make_proceeder(name)
            for human_name, name, _ in ProtoCommandLoader().commands
        }

    def __init__(self, *args, **kwargs):
        self.transaction = kwargs.pop("transaction")
        super().__init__(*args, **kwargs)

    def make_proceeder(self, command_name: str):
        def proceed():
            self._application.screen_manager.to(
                CommandEditorView,
                CommandEditorModel,
                transaction=self.transaction,
                command_name=command_name,
            )

        return proceed
