from asciimatics.widgets import Layout, Label, Button, Widget
from torinaku.screens.base import BaseScreen
from torinaku.tui.multicolumnchecklistbox import MultiColumnCheckListBox


class QueryManager(BaseScreen):
    def __init__(self, *args, **kwargs):
        self._query_list = MultiColumnCheckListBox(
            Widget.FILL_FRAME,
            titles=["Creator", "Type", "Payload", "S"],
            columns=["<18", "<16", "0", ">3"],
            options=[],
            name="query_list",
            on_select=self._edit_current_query,
            on_change=self._refresh_buttons_state,
            add_scroll_bar=True,
        )
        super().__init__(*args, **kwargs)
        self._reload_list()

    def _compose_layout(self):
        self._compose_navigation_layout()
        self._compose_divider_layout()
        self._compose_list_layout()
        self._compose_divider_layout()
        self._compose_actions_layout()
        self._compose_divider_layout()
        self._compose_help_layout()

    def _compose_navigation_layout(self):
        nav_lay = Layout([1, 1, 1])
        self.add_layout(nav_lay)
        nav_lay.add_widget(Label("Go to:"))
        nav_lay.add_widget(Button("Main menu", self._model.go_back), 1)
        nav_lay.add_widget(Button("Queries manager", self.dummy, disabled=True), 2)
