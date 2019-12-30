"""
Transactions browser
"""

from asciimatics.widgets import Widget, Layout, Divider, Button, Label
from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen

from iroha_tui.tui.multicolumnchecklistbox import MultiColumnCheckListBox
from iroha_tui.app.transactions import TransactionsPoolViewer
from iroha_tui.screens.base import BaseScreen


class TransactionsView(BaseScreen):
    _title = "Transaction Browser"

    def __init__(self, *args, **kwargs):
        self._transactions_list = MultiColumnCheckListBox(
            Widget.FILL_FRAME,
            columns=["<7", ">14", "<18", ">3", ">3", ">3", "0", ">3"],
            options=[],
            titles=["Hash", "Timestamp", "Creator", "Q", "B", "C", "Commands", "S"],
            name="txs_list",
            on_select=self._edit_current_tx,
            on_change=self._refresh_buttons_state,
            add_scroll_bar=True,
        )
        super().__init__(*args, **kwargs)
        self._reload_list()

    def _compose_layout(self):
        nav_lay = Layout([1, 1, 1])
        self.add_layout(nav_lay)
        nav_lay.add_widget(Label("Go to:"))
        nav_lay.add_widget(Button("Main menu", self._model.go_back), 1)
        nav_lay.add_widget(
            Button("Queries manager", self._model.go_to_query_manager), 2
        )

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Divider())
        layout.add_widget(self._transactions_list)
        layout.add_widget(Divider())
        buttons = Layout([1] * 8)
        self.add_layout(buttons)
        self._send_button = Button("Send", self._send_txs)
        self._status_button = Button("Status", self._get_tx_statuses)
        self._remove_button = Button("Remove!", self._remove_txs)
        self._batch_button = Button("Batch", self._batch_txs)
        self._sign_button = Button("Sign", self._sign_txs)
        self._gen_block_button = Button("GenBlock", self._save_genesis_block)
        buttons.add_widget(Button("Create", self._create_tx), 0)
        buttons.add_widget(self._send_button, 1)
        buttons.add_widget(self._status_button, 2)
        buttons.add_widget(self._remove_button, 3)
        buttons.add_widget(Button("Sav/Ld", self.dummy, disabled=True), 4)
        buttons.add_widget(self._batch_button, 5)
        buttons.add_widget(self._sign_button, 6)
        buttons.add_widget(self._gen_block_button, 7)
        help_messages = Layout([1])
        self.add_layout(help_messages)
        label1 = Label(
            "[Return] to edit, [Space] to pick several, [Esc] to go to main menu",
            align="^",
        )
        label2 = Label(
            "Q - quorum, B - batch size, "
            "C - commands quantity, S - signatures quantity",
            align="^",
        )
        help_messages.add_widget(Divider())
        help_messages.add_widget(label2)
        help_messages.add_widget(label1)

    def reset(self):
        super().reset()
        self._reload_list()

    def _reload_list(self, new_value=None):
        viewer = TransactionsPoolViewer(self._model.transactions)
        data = []
        i = 0
        for tx in viewer.data:
            data.append(
                (
                    [
                        tx["hash"],
                        tx["timestamp"],
                        tx["creator"],
                        tx["quorum"],
                        tx["batch_type"][0] + tx["batch"],
                        tx["commands"],
                        tx["brief"],
                        tx["signatures"],
                    ],
                    i,
                )
            )
            i += 1

        self._transactions_list.options = data
        self._transactions_list.value = new_value
        self._transactions_list._selected = []
        self._refresh_buttons_state()

    def _create_tx(self):
        self._model.create_tx()

    def _send_txs(self):
        to_send = list(reversed(sorted(self._transactions_list._selected)))
        self._model.send_txs(to_send)

    def _get_tx_statuses(self):
        to_request = list(reversed(sorted(self._transactions_list._selected)))
        self._model.get_tx_statuses(to_request)

    def _remove_txs(self):
        to_remove = list(reversed(sorted(self._transactions_list._selected)))
        for txidx in to_remove:
            del self._model.transactions[txidx]
        self._reload_list()

    def _batch_txs(self):
        to_batch = list(reversed(sorted(self._transactions_list._selected)))
        self._model.batch_txs(to_batch)

    def _sign_txs(self):
        to_sign = list(reversed(sorted(self._transactions_list._selected)))
        self._model.sign_txs(to_sign)

    def _save_genesis_block(self):
        to_sign = list(reversed(sorted(self._transactions_list._selected)))
        self._model.save_genesis_block(to_sign)

    def _refresh_buttons_state(self):
        disabled = not bool(len(self._transactions_list._selected))
        self._send_button.disabled = disabled
        self._status_button.disabled = disabled
        self._remove_button.disabled = disabled
        self._batch_button.disabled = disabled
        self._sign_button.disabled = disabled

    def _edit_current_tx(self):
        if self._transactions_list.value[0] is None:
            return
        self._model.edit_tx(self._transactions_list.value[0])

    def dummy(self):
        pass
