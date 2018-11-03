import pygame

from ..base.context import Context
from ..base.sprite import SpriteType, Sprite
from ..res import IMG_DIR


class Background(Sprite):
    __BASE_SURFACE: pygame.surface = None
    __SURFACE: pygame.surface = None

    def __init__(self, name: str):
        super().__init__()
        if not Background.__BASE_SURFACE:
            Background.__BASE_SURFACE = pygame.image.load(IMG_DIR + "room/room_" + name + ".png")
        self.width = 13
        self.height = 9

    def update(self, context: Context):
        pass

    @classmethod
    def update_render_context(self, render_context):
        Background.__SURFACE = pygame.transform.smoothscale(
            Background.__BASE_SURFACE,
            [
                render_context.resolution[0] - self.sidebar_width,
                render_context.resolution[1]
            ]
        )

    @property
    def image(self) -> pygame.Surface:
        return Background.__SURFACE

    @property
    def sprite_type(self) -> SpriteType:
        return SpriteType.GHOST
