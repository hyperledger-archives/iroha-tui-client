#!/usr/bin/env python3

from loguru import logger
from torinaku.app import Torinaku
from torinaku.app.config.parser import CombinedArgumentParser


def main():
    logger.remove()

    config = CombinedArgumentParser().parse_args()

    torinaku = Torinaku(config)
    torinaku.run()


if __name__ == "__main__":
    main()
