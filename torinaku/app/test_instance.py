from torinaku.app import Torinaku
from torinaku.app.fake_tx_factory import FakeTransactionFactory


class TestTorinaku(Torinaku):
    def __init__(self):
        super().__init__()
        self.transactions = [FakeTransactionFactory().make_transaction()]
        self.last_chosen_peer = "127.0.0.1:50051"
