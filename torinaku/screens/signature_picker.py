import os
from asciimatics.widgets import Layout, TextBox, Divider, Button, FileBrowser
from torinaku.screens.base import BaseScreen


class SignaturePickerView(BaseScreen):
    def get_init_kwargs(self):
        return {
            **super().get_init_kwargs(),
            "height": 18,
            "width": self._screen.width * 3 // 4,
        }

    def _compose_layout(self):
        input_layout = Layout([1])
        self.add_layout(input_layout)
        input_layout.add_widget(
            TextBox(
                name="private_key",
                label="Private key",
                height=2,
                line_wrap=True,
                as_string=True,
            )
        )
        input_layout.add_widget(Divider())

        self._compose_file_picker_layout()

        action_layout = Layout([1, 1])
        self.add_layout(action_layout)
        action_layout.add_widget(Button(text="Sign", on_click=self._sign), 0)
        action_layout.add_widget(Button(text="Cancel", on_click=self._model.cancel), 1)

    def _compose_file_picker_layout(self):
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(FileBrowser(
            height=11,
            root=os.getcwd(),
            on_select=self._model.on_file_selected,
            name="file_picker"
        ))
        layout.add_widget(Divider())

    def _sign(self):
        self.save()
        private_key = self.data["private_key"]
        self._model.sign(private_key)
