from asciimatics.widgets import Layout, Divider, Button, Text, DropdownList, Label
from iroha_tui.screens.base import BaseScreen
from iroha_tui.app.validators import (
    account_id_validator,
    uint64_validator,
    uint32_validator,
)
from iroha_tui.tui.layout_composers.proto import ProtoLayoutComposer
from iroha_tui.tui.dynamic_label import DynamicLabel


class QueryEditorView(BaseScreen):
    _title = "Query Editor"

    def __init__(self, *args, **kwargs):
        self.query_specific_layout = None
        self.query_specific_layout_footer = None
        super().__init__(*args, **kwargs)
        self._on_query_type_change()

    def _compose_layout(self):
        self._compose_actions_layout()
        self._compose_query_common_layout()
        self._compose_query_specific_layout()

    def _compose_actions_layout(self):
        actions_layout = Layout([3, 2, 4, 3])
        self.add_layout(actions_layout)
        actions_layout.add_widget(
            Button(text="Save & Go back", on_click=self._model.save_go_back), 0
        )
        actions_layout.add_widget(
            Button(text="Execute", on_click=self._model.execute), 1
        )
        if self._model.last_peer_address:
            actions_layout.add_widget(
                Button(
                    text=f"Exec @ {self._model.last_peer_address}",
                    on_click=self._model.execute_at_last_peer,
                ),
                2,
            )
        actions_layout.add_widget(Button(text="Cancel", on_click=self._model.cancel), 3)

    def _compose_query_common_layout(self):
        divider_layout = Layout([1])
        self.add_layout(divider_layout)
        divider_layout.add_widget(Divider())
        divider_layout.add_widget(DynamicLabel(name="proto_status"))

        self._compose_created_time_layout()

        common_layout = Layout([5, 13])
        self.add_layout(common_layout)
        common_layout.add_widget(Label("Creator account id"), 0)
        common_layout.add_widget(
            Text(
                name=".payload.meta.creator_account_id", validator=account_id_validator
            ),
            1,
        )
        common_layout.add_widget(Label("Query counter"), 0)
        common_layout.add_widget(
            Text(name=".payload.meta.query_counter", validator=uint32_validator), 1
        )

        common_layout.add_widget(Label("Query type"), 0)
        common_layout.add_widget(
            DropdownList(
                options=self._model.query_type_options,
                on_change=self._on_query_type_change,
                name="query_type",
            ),
            1,
        )

        self._compose_signature_layout()

    def _compose_signature_layout(self):
        signature_layout = Layout([5, 9, 4])
        self.add_layout(signature_layout)
        signature_layout.add_widget(Label("Signature"), 0)
        signature_layout.add_widget(DynamicLabel("signature_status"), 1)
        signature_layout.add_widget(Button("Sign", on_click=self._model.sign), 2)

    def _compose_created_time_layout(self):
        time_layout = Layout([5, 9, 4])
        self.add_layout(time_layout)
        time_layout.add_widget(Label("Created time"), 0)
        time_layout.add_widget(
            Text(name=".payload.meta.created_time", validator=uint64_validator), 1
        )
        time_layout.add_widget(
            Button("Use Now", on_click=lambda: 0), 2  # TODO: implement
        )

    def _compose_query_specific_layout(self):
        divider_layout = Layout([1])
        self.add_layout(divider_layout)
        divider_layout.add_widget(Divider())

        self.query_specific_layout = Layout(ProtoLayoutComposer.layout_columns[0])
        self.query_specific_layout_footer = Layout(
            ProtoLayoutComposer.layout_columns[1]
        )
        self.add_layout(self.query_specific_layout)
        self.add_layout(self.query_specific_layout_footer)
        self._reset_query_specific_layout()

    def _reset_query_specific_layout(self):
        if not self.query_specific_layout:
            # weird asciimatics behaviour when resizing the terminal
            return
        self.query_specific_layout.clear_widgets()
        self.query_specific_layout_footer.clear_widgets()
        ProtoLayoutComposer.compose_on_layouts(
            [self.query_specific_layout, self.query_specific_layout_footer],
            self._model.payload_proxy,
            prefix=".payload." + self._data["query_type"],
        )
        self.fix()

    def reset(self):
        super().reset()
        self._reset_query_specific_layout()

    def _on_query_type_change(self):
        self.update_data()
        self._reset_query_specific_layout()
