from asciimatics.widgets import Layout, Button, Divider

from torinaku.screens.base import BaseScreen


class CommandEditorView(BaseScreen):
    _title = "Command Editor"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self._model.get_init_data()

    def update(self, frame_no):
        self.save()
        self._model.update(self.data)
        super().update(frame_no)

    def _compose_layout(self):
        tx_buttons_lay = Layout([1, 1])
        self.add_layout(tx_buttons_lay)
        tx_buttons_lay.add_widget(Button("Save", on_click=self._model.save), 0)
        tx_buttons_lay.add_widget(Button("Cancel", on_click=self._model.cancel), 1)

        lay1 = Layout([1])
        self.add_layout(lay1)
        lay1.add_widget(Divider())

        self._model.draw_ui(self)
        self.fix()
