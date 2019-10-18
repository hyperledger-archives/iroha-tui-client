from asciimatics.widgets import Layout, TextBox, Divider, Button
from torinaku.screens.base import BaseScreen


class SignaturePickerView(BaseScreen):
    def get_init_kwargs(self):
        return {
            **super().get_init_kwargs(),
            "height": 7,
            "width": self._screen.width * 3 // 4,
        }

    def _compose_layout(self):
        input_layout = Layout([1])
        self.add_layout(input_layout)
        input_layout.add_widget(
            TextBox(
                name="private_key",
                label="Private key",
                height=3,
                line_wrap=True,
                as_string=True,
            )
        )
        input_layout.add_widget(Divider())

        action_layout = Layout([1, 1])
        self.add_layout(action_layout)
        action_layout.add_widget(Button(text="Sign", on_click=self._sign), 0)
        action_layout.add_widget(Button(text="Cancel", on_click=self._model.cancel), 1)

    def _sign(self):
        self.save()
        private_key = self.data["private_key"]
        self._model.sign(private_key)
