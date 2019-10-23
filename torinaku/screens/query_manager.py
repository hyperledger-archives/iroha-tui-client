from asciimatics.widgets import Layout, Label, Button, Widget, Divider
from torinaku.screens.base import BaseScreen
from torinaku.tui.multicolumnchecklistbox import MultiColumnCheckListBox
from torinaku.app.queries import QueryViewer


class QueryManagerView(BaseScreen):
    def __init__(self, *args, **kwargs):
        self._query_list = MultiColumnCheckListBox(
            Widget.FILL_FRAME,
            titles=["Creator", "Type", "Payload", "S"],
            columns=["<18", "<16", "0", "^3"],
            options=[],
            name="query_list",
            on_select=self._edit_current_query,
            on_change=self._refresh_buttons_state,
            add_scroll_bar=True,
        )
        self._remove_button = None
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
        nav_lay.add_widget(Button("Transaction browser", self._model.go_to_tx_browser), 2)

    def _compose_divider_layout(self):
        divider_layout = Layout([1])
        self.add_layout(divider_layout)
        divider_layout.add_widget(Divider())

    def _compose_list_layout(self):
        list_layout = Layout([1], fill_frame=True)
        self.add_layout(list_layout)
        list_layout.add_widget(self._query_list)

    def _compose_actions_layout(self):
        actions_layout = Layout([1, 1])
        self.add_layout(actions_layout)
        actions_layout.add_widget(
            Button(
                "Create",
                self._model.create_query
            ),
            0
        )
        self._remove_button = Button(
            "Remove",
            self._remove_queries,
            disabled=True
        )
        actions_layout.add_widget(self._remove_button, 1)

    def _compose_help_layout(self):
        help_layout = Layout([1])
        self.add_layout(help_layout)
        help_layout.add_widget(Label(
            "[Return] to edit, [Space] to pick several, [Esc] to go to main menu",
            align="^",
        ))
        help_layout.add_widget(Label(
            "S - signature status (+ if valid, - if invalid, <blank> if not present)",
            align="^",
        ))

    def reset(self):
        self._reload_list()
        super().reset()

    def _reload_list(self):
        self._query_list.options = []
        for i, query in enumerate(self._model.queries):
            data = QueryViewer(query).data
            self._query_list.options.append(((
                data["creator"],
                data["type"],
                data["payload"],
                data["signature"]
            ), i))
        self._refresh_buttons_state()

    def _refresh_buttons_state(self):
        disabled = not bool(len(self._query_list._selected))
        self._remove_button.disabled = disabled

    def _edit_current_query(self):
        self._model.edit_query(self._query_list.value[0])

    def _remove_queries(self):
        self._model.remove_queries(self._query_list._selected)
        self._query_list._selected = []
        self._reload_list()
