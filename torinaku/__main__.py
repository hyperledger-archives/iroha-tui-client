#!/usr/bin/env python3

import argparse
import sys
from loguru import logger
from torinaku.app import Torinaku
from torinaku.app.test_instance import TestTorinaku


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug-log", "-d", help="Enable debug log",
                        action="store_true")
    parser.add_argument("--test-data", "-t", help="Enable test sample data",
                        action="store_true")
    args = parser.parse_args(sys.argv[1:])

    logger.remove()
    if args.debug_log:
        logger.add("debug_log", level="DEBUG")

    if args.test_data:
        torinaku = TestTorinaku()
    else:
        torinaku = Torinaku()

    torinaku.run()


if __name__ == "__main__":
    main()
