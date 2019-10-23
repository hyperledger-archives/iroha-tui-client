from iroha import Iroha, IrohaCrypto
from iroha.transaction_pb2 import Transaction
from iroha.commands_pb2 import Command


class FakeTransactionFactory:
    """
    Can create fake transactions for the sake of testing.
    """

    def make_transaction(self) -> Transaction:
        transaction = Transaction()
        transaction.payload.reduced_payload.quorum = 1
        transaction.payload.reduced_payload.creator_account_id = "admin@test"
        transaction.payload.reduced_payload.created_time = Iroha.now()

        transaction.payload.reduced_payload.commands.extend([self.make_command()])

        transaction = IrohaCrypto.sign_transaction(
            transaction,
            "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70",
        )

        return transaction

    def make_command(self) -> Command:
        command = Command()
        command.set_account_detail.account_id = "admin@test"
        command.set_account_detail.key = "example_key"
        command.set_account_detail.value = "example_value"
        return command
