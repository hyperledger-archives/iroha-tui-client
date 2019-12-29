from asciimatics.widgets import (
    Layout,
    Button,
    Divider,
    Label,
    Text,
    ListBox,
    VerticalDivider,
)
from iroha_tui.app.validators import quorum_validator
from iroha_tui.screens.base import BaseScreen
from iroha_tui.tui.dynamic_label import DynamicLabel


class TransactionEditorView(BaseScreen):
    _title = "Transaction Editor"

    def __init__(self, *args, **kwargs):
        self._init_focus_on = None
        self._command_list = None
        self._signature_list = None
        super().__init__(*args, **kwargs)

        self._update_lists()

    def _compose_layout(self):
        PADDING = 0
        tx_buttons_lay = Layout([1, 1, 1])
        self.add_layout(tx_buttons_lay)
        tx_buttons_lay.add_widget(Button("Save", on_click=self._model.save), 0)
        tx_buttons_lay.add_widget(
            Button("Save & Go back", on_click=self._model.save_go_back), 1
        )
        tx_buttons_lay.add_widget(Button("Go back", on_click=self._model.go_back), 2)

        hash_lay = Layout([PADDING, 18, PADDING])
        self.add_layout(hash_lay)
        hash_lay.add_widget(DynamicLabel(name="tx_hash"), 1)
        hash_lay.add_widget(Divider(), 1)

        lay1 = Layout([PADDING, 5, 13, PADDING])
        self.add_layout(lay1)
        self._init_focus_on = {"layout": lay1, "column": 2, "widget": 0}
        lay1.add_widget(Label("Creator Id"), 1)
        lay1.add_widget(
            Text(name=".payload.reduced_payload.creator_account_id"), 2,
        )
        lay1.add_widget(Label("Quorum"), 1)
        lay1.add_widget(
            Text(name=".payload.reduced_payload.quorum", validator=quorum_validator), 2
        )

        lay2 = Layout([PADDING, 5, 9, 4, PADDING])
        self.add_layout(lay2)
        lay2.add_widget(Label("Created Timestamp"), 1)
        lay2.add_widget(
            Text(
                name=".payload.reduced_payload.created_time",
                validator=self._model.validate_timestamp,
            ),
            2,
        )
        lay2.add_widget(Button("Use Now", on_click=self._model.set_timestamp_to_now), 3)

        lay3 = Layout([PADDING, 5, 13, PADDING])
        self.add_layout(lay3)
        lay3.add_widget(Label("Human Time"), 1)
        lay3.add_widget(DynamicLabel(name="human_time"), 2)
        lay3.add_widget(Label("Batch Summary"), 1)
        lay3.add_widget(DynamicLabel(name="batch_summary"), 2)

        lay4 = Layout([PADDING, 18, PADDING])
        self.add_layout(lay4)
        lay4.add_widget(Divider(), 1)

        lay4 = Layout([PADDING, 3, 2, 2, 2, 1, 3, 3, 2, PADDING])
        self.add_layout(lay4)
        lay4.add_widget(Label("Commands:"), 1)
        lay4.add_widget(Button("Add", on_click=self._model.add_command), 2)
        lay4.add_widget(Button("Edit", on_click=self._edit_command), 3)
        lay4.add_widget(Button("Del", on_click=self._remove_command), 4)
        lay4.add_widget(Label("Signatures:"), 6)
        lay4.add_widget(Button("Add/Sign", on_click=self._model.add_signature), 7)
        lay4.add_widget(Button("Del", on_click=self._remove_signature), 8)

        lay5 = Layout([PADDING, 9, 1, 8, PADDING])
        self.add_layout(lay5)
        self._command_list = ListBox(
            max(self._screen.height - 13, 4),
            [],
            name="commands",
            add_scroll_bar=True,
            on_select=self._edit_command,
        )
        lay5.add_widget(self._command_list, 1)
        lay5.add_widget(VerticalDivider(), 2)
        self._signature_list = ListBox(
            max(self._screen.height - 13, 4),
            [],
            name="signatures",
            add_scroll_bar=True,
            on_select=self._show_signature,
        )
        lay5.add_widget(self._signature_list, 3)
        self.fix()

    def reset(self):
        self._update_lists()
        super().reset()

    def _update_lists(self):
        self._model.reload_computed_lists()
        self._command_list.options = self._model.data["command_names"]
        self._signature_list.options = self._model.data["signatures"]

    def _edit_command(self):
        idx = self._command_list.value
        self._model.edit_command(idx)

    def _remove_command(self):
        idx = self.data["commands"]
        self._model.remove_command(idx)
        self._onload_handler()

    def _remove_signature(self):
        idx = self.data["signatures"]
        self._model.remove_signature(idx)
        self._onload_handler()

    def _show_signature(self):
        idx = self.data["signatures"]
        self._model.show_signature(idx)
        self._onload_handler()
