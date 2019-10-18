#!/usr/bin/env python3

import sys


def reraise(exception, message):
    """
  hrows the original exception preserving
  traceback with an additional message
  """
    raise type(exception)(str(exception) + " {}".format(message)).with_traceback(
        sys.exc_info()[2]
    )
