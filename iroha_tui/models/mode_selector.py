from iroha_tui.models.selector import BaseSelectorModel
from iroha_tui.screens.transactions import TransactionsView
from iroha_tui.models.transaction_list import TransactionListModel

from iroha_tui.screens.query_manager import QueryManagerView
from iroha_tui.models.query_manager import QueryManagerModel


class ModeSelectorModel(BaseSelectorModel):
    title = "Iroha TUI"

    @property
    def options(self):
        return {
            "Transaction Browser": self._go_to_tx_browser,
            "Query Manager": self._go_to_query_manager,
        }

    def _go_to_tx_browser(self):
        self.go_to(TransactionsView, TransactionListModel)

    def _go_to_query_manager(self):
        self.go_to(QueryManagerView, QueryManagerModel)
