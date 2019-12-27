import os
from asciimatics.widgets import Layout, Text, Divider, Button, FileBrowser
from iroha_tui.screens.base import BaseScreen
from iroha_tui.tui.popup import popup


class SaveFileView(BaseScreen):
    def get_init_kwargs(self):
        return {
            **super().get_init_kwargs(),
            "height": 18,
            "width": self._screen.width * 3 // 4,
        }

    def _compose_layout(self):
        input_layout = Layout([1])
        self.add_layout(input_layout)
        self._path_input = Text(name='file_path', label='Path:')
        input_layout.add_widget(self._path_input)

        self._compose_file_picker_layout()

        action_layout = Layout([1, 1])
        self.add_layout(action_layout)
        action_layout.add_widget(
            Button(text="Save", on_click=self._on_save_clicked), 0)
        action_layout.add_widget(
            Button(text="Cancel", on_click=self._model.cancel), 1)

    def _compose_file_picker_layout(self):
        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(FileBrowser(
            height=11,
            root=os.getcwd(),
            on_change=self._on_browser_change,
            on_select=self._on_file_selected_in_browser,
            name="file_browser"))
        layout.add_widget(Divider())

    def _on_browser_change(self):
        self.save()
        new_path = self.data['file_browser']
        if new_path is None:
            return
        prev_filename = self._path_input.value and os.path.basename(
            self._path_input.value)
        if prev_filename:
            new_path = os.path.join(os.path.dirname(new_path), prev_filename)
        self._path_input.value = new_path

    def _on_file_selected_in_browser(self):
        self.save()
        self._path_input.value = self.data['file_browser']
        self._on_file_selected()

    def _on_save_clicked(self):
        self._on_file_selected()

    def _on_file_selected(self):
        self.save()
        path = self.data['file_path']
        self._model.on_file_selected(path)
