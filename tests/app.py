from iroha_tui.app import IrohaTUI
from tests.fake_tx_factory import FakeTransactionFactory
from tests.fake_query_factory import FakeQueryFactory


class TestIrohaTUI(IrohaTUI):
    def __init__(self):
        super().__init__({})
        self.transactions = [FakeTransactionFactory().make_transaction()]
        self.queries = [FakeQueryFactory().make_query()]
        self.last_chosen_peer = "127.0.0.1:50051"
