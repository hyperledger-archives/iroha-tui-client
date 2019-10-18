from asciimatics.widgets import Layout, Divider, Text, Button
from torinaku.screens.base import BaseScreen
from torinaku.app.validators import make_validator


class PeerPickerView(BaseScreen):
    def get_init_kwargs(self):
        return {
            **super().get_init_kwargs(),
            "height": 5,
            "width": self._screen.width * 3 // 4,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _compose_layout(self):
        input_layout = Layout([1])
        self.add_layout(input_layout)
        input_layout.add_widget(
            Text(
                label="Peer address",
                name="address",
                validator=make_validator("peer_address"),
            )
        )
        input_layout.add_widget(Divider())

        actions_layout = Layout([1, 1])
        self.add_layout(actions_layout)
        actions_layout.add_widget(Button(text="Send", on_click=self._send), 0)
        actions_layout.add_widget(Button(text="Cancel", on_click=self._model.cancel), 1)

    def _send(self):
        self.save()
        self._model.choose(self.data["address"])
