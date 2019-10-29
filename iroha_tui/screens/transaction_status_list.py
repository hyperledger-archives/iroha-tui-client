from asciimatics.widgets import Layout, MultiColumnListBox, Button, Divider
from iroha_tui.screens.base import BaseScreen


class TransactionStatusListView(BaseScreen):
    _title = "Transaction status request"

    def __init__(self, *args, **kwargs):
        self._statuses = None
        super().__init__(*args, **kwargs)

    def update(self, frame_no):
        self._statuses.options = self._model.statuses
        super().update(frame_no)

    def _compose_layout(self):
        list_layout = Layout([1], fill_frame=True)
        self.add_layout(list_layout)
        self._statuses = MultiColumnListBox(
            height=self._canvas.height - 4,
            columns=("40%", "20%", "40%"),
            titles=("Hash", "gRPC", "Status"),
            options=[],
            name="statuses",
            on_select=self._show_status,
        )
        list_layout.add_widget(self._statuses)
        list_layout.add_widget(Divider())

        action_layout = Layout([1, 1, 1])
        self.add_layout(action_layout)
        action_layout.add_widget(Button(text="Show", on_click=self._show_status))
        action_layout.add_widget(
            Button(text="Refresh", on_click=lambda: self._model.request_statuses()), 1
        )
        action_layout.add_widget(Button(text="Cancel", on_click=self._model.cancel), 2)

    def _show_status(self):
        self.save()
        self._model.show_status(self.data["statuses"])
