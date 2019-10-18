from asciimatics.widgets import Layout, Divider, TextBox, Button
from torinaku.screens.base import BaseScreen


class TransactionStatusView(BaseScreen):
    _title = "Transaction Status"

    def _compose_layout(self):
        info_layout = Layout([1], fill_frame=True)
        self.add_layout(info_layout)
        info_layout.add_widget(
            TextBox(
                line_wrap=True,
                label="gRPC status",
                name="grpc_status",
                disabled=True,
                as_string=True,
                height=1,
            )
        )
        info_layout.add_widget(
            TextBox(
                line_wrap=True,
                label="Transaction status",
                name="tx_status",
                disabled=True,
                as_string=True,
                height=1,
            )
        )
        info_layout.add_widget(
            TextBox(
                line_wrap=True,
                label="Transaction hash",
                name="tx_hash",
                disabled=True,
                as_string=True,
                height=2,
            )
        )
        info_layout.add_widget(
            TextBox(
                line_wrap=True,
                label="Error or command name",
                name="err_or_cmd_name",
                disabled=True,
                as_string=True,
                height=2,
            )
        )
        info_layout.add_widget(
            TextBox(
                line_wrap=True,
                label="Failed command index",
                name="failed_cmd_index",
                disabled=True,
                as_string=True,
                height=1,
            )
        )
        info_layout.add_widget(
            TextBox(
                line_wrap=True,
                label="Error code",
                name="error_code",
                disabled=True,
                as_string=True,
                height=1,
            )
        )
        info_layout.add_widget(Divider())

        actions_layout = Layout([1])
        self.add_layout(actions_layout)
        actions_layout.add_widget(Button(text="Cancel", on_click=self._model.cancel))
