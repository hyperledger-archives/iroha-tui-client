from asciimatics.scene import Scene
from loguru import logger


def _build_frame(frame_cls, model_cls, screen, application, **model_kwargs):
    model = model_cls(**{"application": application, **model_kwargs})
    frame = frame_cls(screen, model)
    return frame


class ScreenManager:
    def __init__(self, scene, screen, application):
        """
        Initialize the manager and populate screen stack.

        Probably should not be used in normal code.
        Use factory functions `from_frame` and `from_scene` instead.

        :param first_frame: First frame to load into the scene.
        :param scene: Scene to play.
        :param screen: Screen object from asciimatics.
        :param application: Application instance.
        """
        self._scene = scene
        self._screen = screen
        self._application = application

    @property
    def scene(self):
        """
        Get the current scene.
        """
        return self._scene

    @classmethod
    def from_frame(
        cls, frame_cls, model_cls, screen, application, **model_kwargs
    ) -> "ScreenManager":
        """
        Build a ScreenManager from an initial frame.
        :param frame_cls: Frame class to use.
        :param model_cls: Model class for the frame.
        :param screen: Screen object from asciimatics.
        :param application: Application instance.
        :param model_kwargs: Model parameters.
        """
        frame = _build_frame(
            frame_cls=frame_cls,
            screen=screen,
            application=application,
            model_cls=model_cls,
            **model_kwargs,
        )
        scene = Scene([frame], -1, name="Iroha TUI")
        return cls(scene, screen, application)

    @classmethod
    def from_scene(cls, scene, screen, application) -> "ScreenManager":
        """
        Build a ScreenManager from a constructed scene,
        replacing the screen, and keeping the model for
        all frames.
        :param scene: Scene to copy effects from.
        :param screen: Screen object from asciimatics.
        :param application: Application instance.
        """
        new_frames = []
        for frame in scene.effects:
            new_frames.append(frame.copy_with_screen(screen))
        new_scene = Scene(new_frames, -1, name="Iroha TUI")
        return cls(new_scene, screen, application)

    def copy_with_screen(self, screen) -> "ScreenManager":
        """
        Build a new ScreenManager, which copies all current
        effects from self.
        :param screen: Screen object from asciimatics.
        """
        return ScreenManager.from_scene(self._scene, screen, self._application)

    def to(self, frame_cls, model_cls, keep=True, **model_kwargs):
        """
        Asciimatics transition to a scene appending to the stack.
        :param frame_cls: Frame class to use.
        """
        frame = _build_frame(
            frame_cls=frame_cls,
            model_cls=model_cls,
            screen=self._screen,
            application=self._application,
            **model_kwargs,
        )
        if not keep:
            self._scene.remove_effect(self._scene.effects[-1])
        self._scene.add_effect(frame)
        self._scene.reset()
        self._screen.clear()

    def back(self):
        """
        Asciimatics transition to a previous scene popping the stack.
        """
        self._scene.remove_effect(self._scene.effects[-1])
        while getattr(self._scene.effects[-1], "is_skippable", False):
            self._scene.remove_effect(self._scene.effects[-1])
        self._screen.clear()
        self._scene.reset()
        logger.debug(f"Transition back, screen stack {str(self)}")

    def __str__(self):
        return str(self._scene.effects)
