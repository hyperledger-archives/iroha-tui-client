from typing import TYPE_CHECKING, Iterable

from datetime import datetime

from iroha.block_pb2 import Block

if TYPE_CHECKING:
    from iroha.transaction_pb2 import Transaction


def create_genesis_block(txs: Iterable['Transaction']) -> Block:
    """
    Generate a genesis block with the passed transactions.
    @param txs - iterable of transactions.
    """
    block = Block()
    for tx in txs:
        block.block_v1.payload.transactions.append(tx)
    block.block_v1.payload.created_time = int(datetime.now().timestamp())
    block.block_v1.payload.height = 1
    block.block_v1.payload.prev_block_hash = b'0' * 64
    block.block_v1.payload.tx_number = len(block.block_v1.payload.transactions)
    return block
