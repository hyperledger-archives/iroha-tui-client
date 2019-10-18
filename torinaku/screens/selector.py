from asciimatics.widgets import Widget, Layout, ListBox, Divider, Button

from torinaku.screens.base import BaseScreen


class SelectorView(BaseScreen):
    def get_init_kwargs(self):
        return {
            **super().get_init_kwargs(),
            "height": self._screen.height * 3 // 4,
            "width": self._screen.width * 2 // 3,
        }

    def get_title(self):
        return self._model.title

    def _compose_layout(self):
        list_lay = Layout([1], fill_frame=True)
        self.add_layout(list_lay)
        list_lay.add_widget(
            ListBox(
                Widget.FILL_FRAME,
                list(self._model.screen_options.items()),
                name="list",
                add_scroll_bar=True,
                on_select=self._on_select,
            )
        )
        list_lay.add_widget(Divider())

        tx_buttons_lay = Layout([1, 1])
        self.add_layout(tx_buttons_lay)
        tx_buttons_lay.add_widget(Button("Proceed", on_click=self._on_select), 0)
        tx_buttons_lay.add_widget(Button("Cancel", on_click=self._model.cancel), 1)

    def _on_select(self):
        self.save()
        picked = self.data["list"]
        self._model.select(picked)
