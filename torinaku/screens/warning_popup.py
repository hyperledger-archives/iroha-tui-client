from asciimatics.widgets import Layout, TextBox, Button
from torinaku.screens.base import BaseScreen


class WarningScreen(BaseScreen):
    def get_init_kwargs(self):
        return {
            **super().get_init_kwargs(),
            "height": self._screen.height * 3 // 4,
            "width": self._screen.width * 3 // 4
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_theme("warning")

    def _compose_layout(self):
        self._compose_main_layout()
        self._compose_divider_layout()
        self._compose_actions_layout()

    def _compose_main_layout(self):
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(TextBox(
            height=self._canvas.height - 4,
            disabled=True,
            name="value",
            as_string=True
        ))

    def _compose_actions_layout(self):
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(Button(
            "Cancel",
            self._model.go_back
        ))

