from asciimatics.exceptions import NextScene


class ScreensManager:

  def __init__(self, preloaded_screen):
    """
    Initialize the manager and populate screens stack.
    :param preloaded_screen: The name of currently active scene.
    """
    self._screens = [preloaded_screen]

  @property
  def active(self):
    """
    The name of currently active scene.
    """
    return self._screens[-1]

  def reset(self, screen):
    """
    Asciimatics transition to a scene clearing the stack.
    :param screen: The name of the next scene.
    """
    self._screens = [screen]
    raise NextScene(screen)

  def to(self, screen):
    """
    Asciimatics transition to a scene appending to the stack.
    :param screen: The name of the next scene.
    """
    self._screens.append(screen)
    raise NextScene(screen)

  def back(self):
    """
    Asciimatics transition to a previous scene popping the stack.
    """
    self._screens.pop()
    raise NextScene(self._screens[-1])
