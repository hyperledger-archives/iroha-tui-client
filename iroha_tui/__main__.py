#!/usr/bin/env python3

from loguru import logger
from iroha_tui.app import IrohaTUI
from iroha_tui.app.config.parser import CombinedArgumentParser


def main():
    logger.remove()

    config = CombinedArgumentParser().parse_args()

    app = IrohaTUI(config)
    app.run()


if __name__ == "__main__":
    main()
