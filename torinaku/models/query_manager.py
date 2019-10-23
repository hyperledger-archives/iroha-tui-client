from torinaku.models.base import BaseModel

from torinaku.models.query_editor import QueryEditorModel
from torinaku.screens.query_editor import QueryEditorView


class QueryManagerModel(BaseModel):
    @property
    def queries(self):
        return self._application.queries

    def go_to_tx_browser(self):
        from torinaku.screens.transactions import TransactionsView
        from torinaku.models.transaction_list import TransactionListModel
        self.go_to(
            TransactionsView,
            TransactionListModel,
            keep=False
        )

    def create_query(self):
        self.go_to(QueryEditorView, QueryEditorModel)

    def edit_query(self, query_idx):
        query = self.queries[query_idx]
        self.go_to(QueryEditorView, QueryEditorModel, query=query)

    def remove_queries(self, query_idxs):
        to_remove = list(reversed(sorted(query_idxs)))
        for query_idx in to_remove:
            del self.queries[query_idx]
