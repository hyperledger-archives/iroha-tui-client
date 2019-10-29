from iroha import Iroha, IrohaCrypto
from iroha.queries_pb2 import Query


class FakeQueryFactory:
    def make_query(self) -> Query:
        query = Query()
        query.payload.meta.creator_account_id = "admin@test"
        query.payload.meta.query_counter = 1
        query.payload.meta.created_time = Iroha.now()
        #  query.payload.get_account.account_id = "admin@test"
        query.payload.get_transactions.tx_hashes.append("asdf")
        query.payload.get_transactions.tx_hashes.append("asdfasdf")
        query = IrohaCrypto.sign_query(
            query,
            "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70",
        )
        return query
