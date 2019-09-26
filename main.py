#!/usr/bin/env python3

import sys
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from app.model import AppModel

from screens import init_scenes
from screens.selector import SelectorView
from screens.transactions import TransactionsView

START_SCREEN = 'Mode Selector'
MODEL = AppModel(START_SCREEN)


def play_wrapper(screen, scene):
  scenes = list(init_scenes(screen, MODEL))
  screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
while True:
  try:
    Screen.wrapper(play_wrapper, catch_interrupt=False, arguments=[last_scene])
    sys.exit(0)
  except ResizeScreenError as e:
    last_scene = e.scene
  except KeyboardInterrupt:
    sys.exit(0)
