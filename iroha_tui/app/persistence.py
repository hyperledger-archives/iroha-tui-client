import json
from typing import TYPE_CHECKING, Dict
from google.protobuf.json_format import MessageToDict, ParseDict
from iroha.transaction_pb2 import Transaction
from iroha.queries_pb2 import Query


if TYPE_CHECKING:
    from iroha_tui.app import IrohaTUI


class Persistence:
    """
    Saves intermediate state of the application into a file.
    Can also load into an existing application.
    """

    def __init__(self, filename):
        self.filename = filename

    def dump(self, application: "IrohaTUI"):
        data: Dict = {
            "transactions": [],
            "queries": []
        }

        for transaction in application.transactions:
            data["transactions"].append(MessageToDict(transaction))
        for query in application.queries:
            data["queries"].append(MessageToDict(query))

        with open(self.filename, "w") as f:
            json.dump(data, f)

    def load(self, application: "IrohaTUI"):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)

            for query in data["queries"]:
                query_pb2 = Query()
                application.queries.append(ParseDict(query, query_pb2))

            for transaction in data["transactions"]:
                transaction_pb2 = Transaction()
                application.transactions.append(ParseDict(transaction, transaction_pb2))
        except Exception:
            pass
