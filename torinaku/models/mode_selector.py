from torinaku.models.selector import BaseSelectorModel
from torinaku.screens.transactions import TransactionsView
from torinaku.models.transaction_list import TransactionListModel

from torinaku.screens.query_editor import QueryEditorView
from torinaku.models.query_editor import QueryEditorModel


class ModeSelectorModel(BaseSelectorModel):
    title = "Iroha TUI"

    @property
    def options(self):
        return {
            "Transaction Browser": self._go_to_tx_browser,
            "Query Editor [WIP]": self._go_to_query_manager,
        }

    def _go_to_tx_browser(self):
        self.go_to(TransactionsView, TransactionListModel)

    def _go_to_query_manager(self):
        self.go_to(QueryEditorView, QueryEditorModel)
