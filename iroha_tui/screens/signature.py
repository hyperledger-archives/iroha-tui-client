from asciimatics.widgets import Layout, TextBox

from iroha_tui.screens.base import BaseScreen


class SignatureView(BaseScreen):
    _width_mult = 3 / 4
    _title = "Signature"

    _public_key_height = 1
    _signature_height = 4

    def get_init_kwargs(self):
        return {
            **super().get_init_kwargs(),
            "height": 2 + self._public_key_height + self._signature_height,
        }

    def __init__(self, *args, **kwargs):
        self.data = self._model.data
        super().__init__(*args, **kwargs)

    def _compose_layout(self):
        main_layout = Layout([1, 1], fill_frame=True)
        self.add_layout(main_layout)
        main_layout.add_widget(
            TextBox(
                label="Public key",
                name="public_key",
                disabled=True,
                height=self._public_key_height,
                line_wrap=True,
                as_string=True,
            )
        )
        main_layout.add_widget(
            TextBox(
                label="Signature",
                name="signature",
                disabled=True,
                height=self._signature_height,
                line_wrap=True,
                as_string=True,
            )
        )

    def process_event(self, event):
        self._model.back()
